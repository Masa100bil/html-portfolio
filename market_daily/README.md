# Market Daily Report

市場データのスナップショットからMarkdownレポートを生成するツールです。

## 実行方法

```bash
python daily_report.py
```

実行すると、`market_snapshot.json` を読み込み、`daily_report.md` を生成します。

## ファイル構成

| ファイル | 説明 |
|----------|------|
| `market_snapshot.json` | 入力データ（市場スナップショット） |
| `daily_report.py` | レポート生成スクリプト |
| `daily_report.md` | 出力レポート（自動生成） |

## JSON フォーマット

`market_snapshot.json` は以下の形式で記述します。

```json
{
  "date": "YYYY-MM-DD",
  "equity": [...],
  "commodities": [...],
  "crypto": [...]
}
```

### 各セクションの詳細

#### equity（株式指数）

```json
{
  "symbol": "SPX",
  "name": "S&P 500",
  "price": 6120.50,
  "change": 45.30,
  "change_pct": 0.74
}
```

| フィールド | 型 | 説明 |
|------------|------|------|
| `symbol` | string | ティッカーシンボル |
| `name` | string | 指数名 |
| `price` | number | 現在価格 |
| `change` | number | 前日比（絶対値） |
| `change_pct` | number | 前日比（%） |

#### commodities（コモディティ）

```json
{
  "symbol": "GOLD",
  "name": "Gold",
  "price": 2085.40,
  "unit": "USD/oz",
  "change": 12.30,
  "change_pct": 0.59
}
```

| フィールド | 型 | 説明 |
|------------|------|------|
| `symbol` | string | シンボル |
| `name` | string | 商品名 |
| `price` | number | 価格 |
| `unit` | string | 単位（例: USD/oz, USD/bbl） |
| `change` | number | 前日比（絶対値） |
| `change_pct` | number | 前日比（%） |

#### crypto（暗号資産）

```json
{
  "symbol": "BTC",
  "name": "Bitcoin",
  "price": 102500.00,
  "change": 3250.00,
  "change_pct": 3.27
}
```

| フィールド | 型 | 説明 |
|------------|------|------|
| `symbol` | string | ティッカーシンボル |
| `name` | string | 通貨名 |
| `price` | number | 価格（USD） |
| `change` | number | 前日比（絶対値） |
| `change_pct` | number | 前日比（%） |

## 注意事項

- 出力は事実（数値）と一般的な補足情報のみを含みます
- 価格変動の要因についての断定的な分析は行いません
- 投資助言を目的としたものではありません
