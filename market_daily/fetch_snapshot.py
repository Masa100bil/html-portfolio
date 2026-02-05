#!/usr/bin/env python3
"""
Fetch Market Snapshot

Alpha Vantage API から USDJPY を取得し、sources.csv と合わせて
market_snapshot.json を生成します。API失敗時は CSV のみで生成します。
"""

import csv
import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta
from pathlib import Path


def fetch_usdjpy(api_key: str) -> dict | None:
    """Alpha Vantage API から USDJPY を取得"""
    url = (
        "https://www.alphavantage.co/query"
        "?function=CURRENCY_EXCHANGE_RATE"
        "&from_currency=USD"
        "&to_currency=JPY"
        f"&apikey={api_key}"
    )

    try:
        print(f"Fetching USDJPY from Alpha Vantage API...")
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))

        rate_data = data.get("Realtime Currency Exchange Rate")
        if not rate_data:
            print(f"[WARN] API response missing exchange rate data: {data}")
            return None

        price = float(rate_data.get("5. Exchange Rate", 0))
        last_refreshed = rate_data.get("6. Last Refreshed", "")

        print(f"  -> USDJPY: {price:.2f} (as of {last_refreshed})")

        return {
            "symbol": "USDJPY",
            "name": "USD/JPY",
            "price": price,
            "change": 0.0,
            "change_pct": 0.0,
            "last_refreshed": last_refreshed,
        }

    except urllib.error.URLError as e:
        print(f"[WARN] API request failed: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"[WARN] Failed to parse API response: {e}")
        return None
    except (KeyError, ValueError) as e:
        print(f"[WARN] Failed to extract data from API response: {e}")
        return None


def load_sources(filepath: Path) -> list[dict]:
    """CSVファイルを読み込む"""
    rows = []
    with open(filepath, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def build_snapshot(rows: list[dict], fx_data: dict | None = None) -> dict:
    """CSVの行データからスナップショット形式に変換"""
    # JST (UTC+9) で今日の日付を取得
    jst = timezone(timedelta(hours=9))
    today = datetime.now(jst).strftime("%Y-%m-%d")

    snapshot = {
        "date": today,
        "equity": [],
        "commodities": [],
        "crypto": [],
        "fx": [],
    }

    for row in rows:
        category = row.get("category", "").strip().lower()
        if category not in ["equity", "commodities", "crypto"]:
            print(f"[WARN] Unknown category: {category}, skipping row: {row}")
            continue

        item = {
            "symbol": row.get("symbol", "").strip(),
            "name": row.get("name", "").strip(),
            "price": float(row.get("price", 0)),
            "change": float(row.get("change", 0)),
            "change_pct": float(row.get("change_pct", 0)),
        }

        # commodities の場合は unit を追加
        if category == "commodities":
            unit = row.get("unit", "").strip()
            if unit:
                item["unit"] = unit

        snapshot[category].append(item)

    # FXデータを追加
    if fx_data:
        snapshot["fx"].append(fx_data)

    return snapshot


def save_snapshot(filepath: Path, data: dict) -> None:
    """JSONファイルに書き出す"""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def main() -> int:
    """メイン処理。成功時は 0、失敗時は 1 を返す"""
    script_dir = Path(__file__).parent.resolve()
    sources_path = script_dir / "sources.csv"
    snapshot_path = script_dir / "market_snapshot.json"

    # 環境変数からAPIキーを取得
    api_key = os.environ.get("ALPHAVANTAGE_API_KEY", "")

    try:
        # Alpha Vantage API から USDJPY を取得（APIキーがあれば）
        fx_data = None
        if api_key:
            fx_data = fetch_usdjpy(api_key)
            if fx_data is None:
                print("[INFO] API fetch failed, continuing with CSV data only")
        else:
            print("[INFO] ALPHAVANTAGE_API_KEY not set, skipping API fetch")

        # CSV からデータを読み込み
        print(f"Loading: {sources_path}")
        rows = load_sources(sources_path)
        print(f"  -> Loaded {len(rows)} rows")

        # スナップショットを構築
        print("Building snapshot...")
        snapshot = build_snapshot(rows, fx_data)
        print(f"  -> Date: {snapshot['date']}")
        print(f"  -> Equity: {len(snapshot['equity'])} items")
        print(f"  -> Commodities: {len(snapshot['commodities'])} items")
        print(f"  -> Crypto: {len(snapshot['crypto'])} items")
        print(f"  -> FX: {len(snapshot['fx'])} items")

        # ファイルに保存
        print(f"Writing: {snapshot_path}")
        save_snapshot(snapshot_path, snapshot)
        print("  -> Snapshot saved successfully!")

        return 0

    except FileNotFoundError as e:
        print(f"[ERROR] ファイルが見つかりません: {e}")
        return 1
    except csv.Error as e:
        print(f"[ERROR] CSVの解析に失敗しました: {e}")
        return 1
    except ValueError as e:
        print(f"[ERROR] データの変換に失敗しました: {e}")
        return 1
    except PermissionError as e:
        print(f"[ERROR] ファイルへのアクセス権限がありません: {e}")
        return 1
    except Exception as e:
        print(f"[ERROR] 予期しないエラーが発生しました: {type(e).__name__}: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
