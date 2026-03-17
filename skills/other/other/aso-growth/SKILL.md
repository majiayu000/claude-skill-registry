---
name: aso-growth
description: ASO/ASA growth optimization skill. Manages App Store metadata, Apple Search Ads campaigns, keyword strategy, and tracks performance metrics. Invoked when working on app distribution, ASO, ASA, or marketing optimization.
---

# ASO/ASA Growth Optimization

## When This Skill Activates

- ASO作業（Title/Subtitle/Keywords/Screenshots変更）
- ASAキャンペーン管理（キーワード追加/停止/Bid変更）
- マーケティングメトリクス分析
- Product Page改善
- 「ASA」「ASO」「キーワード」「インストール数」「CVR」に関する会話

## 必ず最初に読むファイル

```
.claude/skills/aso-growth/current-state.md  ← 今の全設定
.claude/skills/aso-growth/changelog.md      ← 変更履歴（因果関係追跡用）
.cursor/plans/ios/aso/Apple_Ads_Guide.md    ← ベストプラクティス（参照用）
```

## ベストプラクティス要約（Apple_Ads_Guide.md から）

### キャンペーン構造

| ルール | 内容 |
|--------|------|
| プレースメント | **Search Results のみ**（他は小予算では非効率） |
| Search Match | **OFF**（常に） |
| Default Match Type | **Exact match**（Discovery キャンペーンのみ Broad） |
| 1国1キャンペーン | 勝ちの国を見つけたら分離 |
| キーワード重複禁止 | 同じキーワードを複数キャンペーンに入れない |

### 国選び

| 優先度 | 国 |
|--------|-----|
| 最初にテスト | Croatia, Czech Republic, Estonia, Hungary, Latvia, Poland, Romania, Slovakia, Slovenia |
| 第2段階 | Austria, Belgium, Denmark, Finland, France, Germany, Italy, Netherlands, Norway, Spain, Sweden, Switzerland |
| 最後 | US, UK, Canada, Australia, NZ |
| 避ける | India, Africa, Pakistan, Bangladesh |

理由: 「iPhone所有者は既に購買力でフィルタリングされている」「USは競争激しすぎて小予算では燃える」

### Bid 戦略

| 状況 | Bid |
|------|-----|
| 初回（データなし） | Appleの推奨の**20-30%下**から開始 |
| 勝ちキーワード | Impression Share 90-100%を目指して上げる |
| 負けキーワード | 停止 or 下げる |
| 変更後 | **24時間待ってから**次の調整 |

### キーワード戦略

| ルール | 内容 |
|--------|------|
| 「〜 free/無料」バリアント | テスト必須。著者の最も利益率高いKW |
| 競合キーワード | テスト推奨。特にインフルエンサーマーケ中の競合 |
| Imp ゼロのEXACT | BROAD に変更してテスト |
| 停止判断 | CPA > ARPU or タップあり0 install が2週間続いたら |

### Product Page（最大レバレッジ）

| 要素 | ルール |
|------|--------|
| Title | 「Keyword - App Name」形式。キーワードを前に |
| Subtitle | 2位以降のキーワードを詰め込む |
| スクショ1-2枚目 | **2-3秒で判断される。** Feature じゃなく Outcome/Pain を見せる |
| スクショ1枚目 | **テキスト + UI画面の組み合わせ**（テキストのみはNG） |

### 判断基準

| 指標 | 良い | 悪い | アクション |
|------|------|------|-----------|
| TTR | >5% | <2% | Product Page改善 |
| CR (タップ→DL) | >40% | <15% | Product Page改善 |
| CPA | < ¥500 | > ¥1,000 | Bid下げ or 停止 |
| Imp→プロダクトページ | >5% | <2% | Title/Icon/スクショ1枚目改善 |

### 最適化の原則

> 「The only correct way to decide if a keyword is successful: financial metrics – specifically ROAS.」
> 「Low CPI ≠ low trial cost. Low trial cost ≠ low cost per paying user.」
> 「The smaller your budget, the more you rely on early metrics.」

### 週次レビューフロー

```
1. Apple Ads ダッシュボードからCSVダウンロード
2. 勝ちキーワード（Install あり + CPA良い）→ Bid上げ
3. 負けキーワード（タップあり + 0 install 2週間）→ PAUSE
4. Imp ゼロのキーワード → BROAD変更 or Bid上げ
5. 新キーワード候補追加（ASO ツール / Apple推奨 / 競合分析）
6. changelog.md に記録
7. current-state.md を更新
```

## 変更時の必須ルール

1. **変更前に current-state.md を読む**（現状把握）
2. **変更内容を changelog.md に記録**（日付 + 何を変えた + 理由）
3. **Title/Subtitle 変更はユーザーに Before/After を見せてから実行**
4. **24時間ルール**: Bid変更後は24時間待ってから次の調整
5. **A/Bテストは週100 DL以上ないと統計的に無意味**

## ファイル更新タイミング

| ファイル | いつ更新 |
|---------|---------|
| current-state.md | ASC/ASA設定を変更した後 |
| changelog.md | 何か変更するたびに追記 |
