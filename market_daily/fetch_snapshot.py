#!/usr/bin/env python3
"""
Fetch Market Snapshot

sources.csv を読み込み、market_snapshot.json を生成します。
"""

import csv
import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path


def load_sources(filepath: Path) -> list[dict]:
    """CSVファイルを読み込む"""
    rows = []
    with open(filepath, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def build_snapshot(rows: list[dict]) -> dict:
    """CSVの行データからスナップショット形式に変換"""
    # JST (UTC+9) で今日の日付を取得
    jst = timezone(timedelta(hours=9))
    today = datetime.now(jst).strftime("%Y-%m-%d")

    snapshot = {
        "date": today,
        "equity": [],
        "commodities": [],
        "crypto": [],
    }

    for row in rows:
        category = row.get("category", "").strip().lower()
        if category not in snapshot:
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

    try:
        print(f"Loading: {sources_path}")
        rows = load_sources(sources_path)
        print(f"  -> Loaded {len(rows)} rows")

        print("Building snapshot...")
        snapshot = build_snapshot(rows)
        print(f"  -> Date: {snapshot['date']}")
        print(f"  -> Equity: {len(snapshot['equity'])} items")
        print(f"  -> Commodities: {len(snapshot['commodities'])} items")
        print(f"  -> Crypto: {len(snapshot['crypto'])} items")

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
