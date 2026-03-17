---
name: app-review-analyzer
description: アプリストア レビュー CSV データを分析して視覚化するスキル。ユーザーがアプリストア レビュー CSV ファイルを提供するか レビュー 分析を要求する時に使用する。CSV は id, date, user_name, title, content, rating, app_version 列を含まなければならない。
doc_contract:
  review_interval_days: 90
---

# App Review Analyzer

## Overview

アプリストア レビュー CSV データを分析してグラフで視覚化するスキル。評点 分布、時間別 トレンド、バージョン別 評点、主要 キーワード 等を分析する。

## CSV データ 形式

分析 対象 CSV は 次の 列を含まなければならない:

| 列          | タイプ        | 説明                          |
| ----------- | ------------- | ----------------------------- |
| id          | integer       | レビュー 固有 ID              |
| date        | datetime      | 作成 日時 (タイムゾーン 含む) |
| user_name   | string        | ユーザー名                    |
| title       | string        | レビュー タイトル             |
| content     | string        | レビュー 内容                 |
| rating      | integer (1-5) | 評点                          |
| app_version | string        | アプリ バージョン             |

## 分析 ワークフロー

### Step 1: CSV ファイル ロード および 検証

1. ユーザーが 提供した CSV ファイル パス 確認
2. `scripts/analyze_reviews.py` スクリプト 実行
3. データ 形式 検証 および 基本 統計 出力

### Step 2: 分析 実行

スクリプトを 実行して 次の 分析を 実行する:

```bash
python3 /path/to/skill/scripts/analyze_reviews.py <csv_path> <output_dir>
```

### Step 3: 結果 解釈

生成された グラフと 統計を 元に インサイトを 提供する:

- **評点 分布**: 全般的な ユーザー 満足度 把握
- **時間別 トレンド**: アプリ 品質 変化 推移
- **バージョン別 評点**: 特定 バージョンの 問題点 識別
- **否定 レビュー 分析**: 主要 不満 事項 把握

## 分析 項目

### 1. 基本 統計

- 総 レビュー 数
- 平均 評点
- 評点別 分布

### 2. 視覚化 グラフ

- 評点 分布 棒 グラフ
- 月別/週別 レビュー トレンド
- バージョン別 平均 評点
- 評点別 レビュー 数 パイ チャート

### 3. テキスト 分析

- 否定 レビュー (1-2点) 主要 キーワード
- 肯定 レビュー (4-5点) 主要 キーワード

## Resources

### scripts/

`analyze_reviews.py` - レビュー 分析 および 視覚化 スクリプト

使用法:

```bash
python3 scripts/analyze_reviews.py <csv_path> [output_dir]
```

- `csv_path`: 分析する CSV ファイル パス
- `output_dir`: グラフ 保存 ディレクトリ (デフォルト値: CSV ファイルと 同じ ディレクトリ)

出力 ファイル:

- `rating_distribution.png`: 評点 分布 グラフ
- `monthly_trend.png`: 月別 レビュー トレンド
- `version_rating.png`: バージョン別 平均 評点
- `analysis_report.txt`: 分析 要約 レポート
