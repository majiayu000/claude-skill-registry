---
name: funnel-builder
description: |
  Kindle/note/YouTube/SNSからLINE→VSLへ誘導する統合ファネル構築スキル。
  Use when: (1) user says「ファネル構築」「導線設計」「リード獲得フロー」,
  (2) user wants end-to-end marketing funnel,
  (3) user mentions「Kindle→LINE」「note→VSL」「集客→販売」.
  Do NOT use for: 単体LP作成（lp-designを使用）、
  単体ステップメール（taiyo-style-step-mailを使用）。
---

# Funnel Builder (統合ファネル構築)

## Description
Kindle、note、その他のプラットフォームからLINE→VSLへ誘導するファネルを統合構築。

## Supported Platforms

### 1. Kindle → LINE → VSL
- Kindle本からのリード獲得
- LINE友達追加誘導
- VSLへの自動誘導

### 2. note → LINE → VSL
- note記事からのリード獲得
- 無料コンテンツ提供
- 有料商品への誘導

### 3. YouTube → LINE → VSL
- 動画からの誘導
- 視聴者を見込み客へ変換

### 4. SNS → LINE → VSL
- Twitter/Instagram/Facebook対応
- 各プラットフォーム最適化

## Funnel Components

### Step 1: リードマグネット
- 無料コンテンツ設計
- 価値提供フォーマット

### Step 2: LINE誘導
- 登録特典設計
- 友達追加CTA最適化

### Step 3: ステップ配信
- 教育コンテンツ
- 信頼構築メッセージ

### Step 4: VSL誘導
- タイミング最適化
- セールスメッセージ

### Step 5: 販売ページ
- LP/VSL統合
- 決済連携

## Usage

```
/funnel-builder [platform] [options]

Platforms:
  kindle   - Kindle本ファネル
  note     - note記事ファネル
  youtube  - YouTube動画ファネル
  sns      - SNSファネル

Options:
  --product [name]     - 商品名
  --price [amount]     - 価格
  --lead-magnet [type] - リードマグネット種類
```

## Examples

```
# Kindleファネル構築
/funnel-builder kindle --product "コピーライティング講座" --price 298000

# noteファネル構築
/funnel-builder note --product "動画編集マスター" --lead-magnet ebook
```

## Integrations
- step-mail: ステップメール配信
- vsl: ビデオセールスレター作成
- lp-generator: LP作成
