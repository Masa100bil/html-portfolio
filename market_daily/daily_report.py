#!/usr/bin/env python3
"""
Market Daily Report Generator

market_snapshot.json を読み込み、daily_report.md を生成します。
"""

import json
import os
from pathlib import Path


def load_snapshot(filepath: str) -> dict:
    """JSONファイルを読み込む"""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def format_change(change: float, change_pct: float) -> str:
    """変動率を見やすくフォーマット"""
    sign = "+" if change >= 0 else ""
    return f"{sign}{change:,.2f} ({sign}{change_pct:.2f}%)"


def generate_markdown(data: dict) -> str:
    """スナップショットデータからMarkdownレポートを生成"""
    lines = []

    # ヘッダー
    report_date = data.get("date", "N/A")
    lines.append(f"# Market Daily Report")
    lines.append(f"")
    lines.append(f"**Date:** {report_date}")
    lines.append(f"")

    # Equity（株式指数）
    lines.append("## Equity (株式指数)")
    lines.append("")
    if data.get("equity"):
        lines.append("| Symbol | Name | Price | Change |")
        lines.append("|--------|------|------:|-------:|")
        for item in data["equity"]:
            change_str = format_change(item["change"], item["change_pct"])
            lines.append(f"| {item['symbol']} | {item['name']} | {item['price']:,.2f} | {change_str} |")
        lines.append("")
        lines.append("> 株式指数は市場全体の動向を示す指標です。値動きは様々な要因により変動します。")
    else:
        lines.append("データがありません。")
    lines.append("")

    # Commodities（コモディティ）
    lines.append("## Commodities (コモディティ)")
    lines.append("")
    if data.get("commodities"):
        lines.append("| Symbol | Name | Price | Unit | Change |")
        lines.append("|--------|------|------:|------|-------:|")
        for item in data["commodities"]:
            change_str = format_change(item["change"], item["change_pct"])
            unit = item.get("unit", "-")
            lines.append(f"| {item['symbol']} | {item['name']} | {item['price']:,.2f} | {unit} | {change_str} |")
        lines.append("")
        lines.append("> コモディティ価格は需給バランスや市場環境により日々変動します。")
    else:
        lines.append("データがありません。")
    lines.append("")

    # Crypto（暗号資産）
    lines.append("## Crypto (暗号資産)")
    lines.append("")
    if data.get("crypto"):
        lines.append("| Symbol | Name | Price (USD) | Change |")
        lines.append("|--------|------|------------:|-------:|")
        for item in data["crypto"]:
            change_str = format_change(item["change"], item["change_pct"])
            lines.append(f"| {item['symbol']} | {item['name']} | {item['price']:,.2f} | {change_str} |")
        lines.append("")
        lines.append("> 暗号資産は高いボラティリティを持つ資産クラスです。価格は24時間変動します。")
    else:
        lines.append("データがありません。")
    lines.append("")

    # フッター
    lines.append("---")
    lines.append("")
    lines.append("*本レポートは市場データの記録を目的としており、投資助言ではありません。*")
    lines.append("")

    return "\n".join(lines)


def main():
    """メイン処理"""
    # スクリプトのディレクトリを基準にパスを設定
    script_dir = Path(__file__).parent.resolve()
    snapshot_path = script_dir / "market_snapshot.json"
    report_path = script_dir / "daily_report.md"

    try:
        # JSONを読み込み
        print(f"Loading: {snapshot_path}")
        data = load_snapshot(snapshot_path)
        print(f"  -> Loaded successfully (date: {data.get('date', 'N/A')})")

        # Markdownを生成
        print(f"Generating report...")
        markdown = generate_markdown(data)

        # ファイルに書き出し
        print(f"Writing: {report_path}")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(markdown)
        print(f"  -> Report generated successfully!")

    except FileNotFoundError as e:
        print(f"[ERROR] ファイルが見つかりません: {e}")
    except json.JSONDecodeError as e:
        print(f"[ERROR] JSONの解析に失敗しました: {e}")
    except PermissionError as e:
        print(f"[ERROR] ファイルへのアクセス権限がありません: {e}")
    except Exception as e:
        print(f"[ERROR] 予期しないエラーが発生しました: {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()
