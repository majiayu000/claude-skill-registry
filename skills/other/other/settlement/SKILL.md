---
name: settlement
description: >
  This skill should be used when the user needs to perform year-end closing
  adjustments (決算整理), review financial statements (決算書), compute
  depreciation, or review their trial balance. Trigger phrases include:
  "決算", "決算整理", "決算書を作る", "減価償却", "試算表", "残高試算表",
  "損益計算書", "貸借対照表", "BS", "PL", "期末処理",
  "棚卸し", "未払計上", "前払処理".
---

# 決算整理・決算書作成（Year-End Settlement）

会計年度末の決算整理仕訳を登録し、残高試算表・損益計算書・貸借対照表を確認するスキル。
journal スキルで日常仕訳の入力が完了していることを前提とする。

## 設定の読み込み（最初に実行）

1. `shinkoku.config.yaml` を Read ツールで読み込む
2. ファイルが存在しない場合は `/setup` スキルの実行を案内して終了する
3. 設定値を把握し、相対パスは CWD を基準に絶対パスに変換する:
   - `db_path`: CLI スクリプトの `--db-path` 引数に使用
   - `output_dir`: 進捗ファイル等の出力先ベースディレクトリ
   - 各ディレクトリ: ファイル参照時に使用

### パス解決の例

config の `db_path` が `./shinkoku.db`、`output_dir` が `./output` で CWD が `/home/user/tax-2025/` の場合:
- `ledger.py trial-balance --db-path /home/user/tax-2025/shinkoku.db --input query.json`
- `shinkoku ledger bs --db-path /home/user/tax-2025/shinkoku.db --input query.json`

## 進捗情報の読み込み

設定の読み込み後、引継書ファイルを読み込んで前ステップの結果を把握する。

1. `.shinkoku/progress/progress-summary.md` を Read ツールで読み込む（存在する場合）
2. 以下の引継書を Read ツールで読み込む（存在する場合）:
   - `.shinkoku/progress/04-journal.md`
   - `.shinkoku/progress/02-assess.md`
3. 読み込んだ情報を以降のステップで活用する（ユーザーへの再質問を避ける）
4. ファイルが存在しない場合はスキップし、ユーザーに必要情報を直接確認する

## 基本方針

- journal スキルでの仕訳入力が完了しているか確認してから開始する
- 残高試算表で勘定残高を確認し、決算整理仕訳の必要性を判定する
- 減価償却は references/depreciation-rules.md のルールに基づいて計算する
- 決算整理仕訳も登録前に必ずユーザーに確認する
- 最終的に貸借対照表の貸借一致を検証する

## 前提条件の確認

決算処理を開始する前に以下を確認する:

1. **日常仕訳が完了しているか**: 未記帳の取引がないか確認を促す
2. **会計年度**: 対象年度を確認する（例: 2025年1月1日〜12月31日）
3. **青色申告の種類**: 65万円控除（複式簿記 + e-Tax/電子帳簿保存）、55万円控除（複式簿記 + 書面提出）、10万円控除（簡易帳簿）
4. **前年確定申告の確認**: 以下を assess の結果または前年の申告書から確認する
   - 予定納税の有無と金額（所得税の前払い）
   - 純損失の繰越控除の有無
   - 前年の期末残高（当年の期首残高と一致するか）
   - 前年の減価償却累計額（固定資産がある場合）

※ 前年データが未確認の場合は、先に assess スキルで確認するか、
   ユーザーに前年の確定申告書を提示してもらう。

### 0-1. 期首残高の確認・設定

1. `ledger.py ob-list --db-path DB --fiscal-year YEAR` で期首残高が設定済みか確認
2. **未設定の場合**、ユーザーに以下を確認:
   - 開業初年度か？（→ 期首残高なし、スキップ）
   - 前年の確定申告書（青色申告決算書の貸借対照表）の期末列を提示してもらう
   - 画像/PDFの場合は OCR で読み取り
3. 前年の期末残高を `ob-set-batch` で一括登録
4. 登録後、`ob-list` で内容を確認し、ユーザーに承認を得る

## ステップ1: 残高試算表の確認

### `ledger.py trial-balance` の呼び出し

```bash
shinkoku ledger trial-balance --db-path DB_PATH --input query.json
```
入力 JSON:
```json
{
  "fiscal_year": 2025
}
```
出力:
- `accounts`: 各勘定科目の借方合計・貸方合計・残高
- `total_debit`: 借方合計
- `total_credit`: 貸方合計

**確認項目:**

1. 借方合計と貸方合計が一致しているか
2. 各科目の残高が妥当か（マイナス残高の有無）
3. 以下の科目に残高がある場合、決算整理が必要:
   - 仮払金（1060）→ 精算して適切な科目に振り替える
   - 仮受金（2060）→ 内容を確定して振り替える
   - 仮払消費税（1090）/ 未払消費税（2070）→ 消費税の計算結果を反映する

## ステップ2: 決算整理仕訳の登録

以下の決算整理項目を順に確認・処理する。各仕訳は `ledger.py add-journal --db-path DB_PATH --input journal.json` で登録する。

### 2-1. 減価償却費の計上

固定資産（1100〜1160）に残高がある場合、減価償却費を計上する。

**計算ツールの呼び出し:**

```bash
shinkoku tax calc-depreciation --input depreciation_input.json
```

定額法の場合:
```json
{
  "method": "straight_line",
  "acquisition_cost": 300000,
  "useful_life": 4,
  "business_use_ratio": 100,
  "months": 12
}
```

定率法の場合:
```json
{
  "method": "declining_balance",
  "acquisition_cost": 300000,
  "book_value": 200000,
  "useful_life": 4,
  "declining_rate": 500,
  "business_use_ratio": 100,
  "months": 12
}
```

**仕訳の登録:**
```
借方: 減価償却費(5200) / 貸方: 該当の固定資産科目
金額: 計算された償却額
```

- 耐用年数は references/depreciation-rules.md を参照する
- 事業供用開始日が期中の場合は月割り計算を行う
- 一括償却資産（1160）は取得原価の1/3を計上する（3年均等償却）
- 家事按分がある場合は事業使用割合を乗じた金額のみ計上する

### 2-2. 棚卸資産の評価

期末に在庫がある場合、棚卸高を計上する。

#### 在庫データの登録

まず `ledger.py list-inventory --db-path DB_PATH --input query.json` で登録済みの棚卸データを確認する。
未登録の場合は `ledger.py set-inventory --db-path DB_PATH --input inventory.json` で期首・期末の棚卸高を登録する:

```json
{
  "fiscal_year": 2025,
  "detail": {
    "period": "ending",
    "amount": 200000,
    "method": "cost",
    "details": "品目の明細等"
  }
}
```

#### 棚卸仕訳の登録

```
期末棚卸仕訳:
借方: 棚卸資産(1030) / 貸方: 仕入(5001)  金額: 期末棚卸高

期首棚卸仕訳（翌期首に自動振替する場合の備忘）:
借方: 仕入(5001) / 貸方: 棚卸資産(1030)  金額: 期首棚卸高
```

- 期末の在庫数量と単価をユーザーに確認する
- 評価方法（最終仕入原価法等）を確認する
- **売上原価の計算**: 期首棚卸高 + 仕入高 - 期末棚卸高
- 登録した棚卸データは `ledger.py pl` と青色申告決算書 PDF に自動反映される

### 2-3. 未払費用の計上

年度末時点で発生しているが未払いの費用を計上する。

```
借方: 該当の費用科目 / 貸方: 未払費用(2031)
```

- 12月分の家賃（翌月払いの場合）
- 12月分の通信費・光熱費
- 社会保険料の未払い分

### 2-4. 前払費用の計上

翌期分を当期に支払い済みの場合、前払費用に振り替える。

```
借方: 前払費用(1041) / 貸方: 該当の費用科目
```

- 年払いの保険料のうち翌期対応分
- 年払いのサブスクリプション料金のうち翌期対応分

### 2-5. 売掛金・買掛金の確認

- 売掛金（1010）残高と未回収の請求書一覧が一致するか確認する
- 買掛金（2001）残高と未払いの仕入先一覧が一致するか確認する
- 回収不能な売掛金がある場合は貸倒金（5260）への振替を検討する

### 2-6. 事業主勘定の確認

- 事業主貸（1200）: 事業資金から個人利用分の合計
- 事業主借（3010）: 個人資金から事業利用分の合計
- これらは決算で相殺しない（翌期首に元入金で繰越処理する）

## ステップ2.7: 地代家賃の内訳登録

事業で地代家賃を計上している場合、内訳を登録する（青色申告決算書の添付資料）。

### `ledger.py add-rent-detail` の呼び出し

```bash
shinkoku ledger add-rent-detail --db-path DB_PATH --input rent.json
```
入力 JSON:
```json
{
  "fiscal_year": 2025,
  "detail": {
    "property_type": "自宅兼事務所",
    "usage": "自宅兼事務所",
    "landlord_name": "賃貸先の名称",
    "landlord_address": "賃貸先の住所",
    "monthly_rent": 100000,
    "annual_rent": 1200000,
    "deposit": 0,
    "business_ratio": 50
  }
}
```

**確認項目:**

- 自宅兼事務所の場合、事業割合が適切に設定されているか
- 年間賃料 = 月額賃料 × 支払月数 で正しいか
- 複数の物件がある場合はすべて登録する


## ステップ3: 決算書の生成

決算整理仕訳がすべて登録された後、決算書を生成する。

### 3-1. 損益計算書の確認（`ledger.py pl`）

```bash
shinkoku ledger pl --db-path DB_PATH --input query.json
```
入力 JSON:
```json
{
  "fiscal_year": 2025
}
```
出力:
- `revenue`: 収益の内訳と合計
- `expenses`: 費用の内訳と合計
- `net_income`: 当期純利益（収益合計 - 費用合計）

**確認項目:**
- 売上金額が実績と一致するか
- 各経費科目が妥当か（異常に大きい・小さい科目がないか）
- 青色申告特別控除前の所得金額を確認する

### 3-2. 貸借対照表の確認（`ledger.py bs`）

```bash
shinkoku ledger bs --db-path DB_PATH --input query.json
```
入力 JSON:
```json
{
  "fiscal_year": 2025
}
```
出力:
- `assets`: 資産の内訳と合計
- `liabilities`: 負債の内訳と合計
- `equity`: 純資産の内訳と合計

**確認項目:**
- 資産合計 = 負債合計 + 純資産合計 であるか（貸借一致）
- 現金・預金残高が実際の残高と一致するか
- 固定資産の帳簿価額が減価償却後の金額であるか

## ステップ4: 決算結果サマリーの提示

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
決算結果サマリー（令和○年分）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

■ 損益計算書
  売上高:         ○○○,○○○円
  売上原価:       ○○○,○○○円
  経費合計:       ○○○,○○○円
  青色申告特別控除前の所得: ○○○,○○○円

■ 貸借対照表
  資産合計:       ○○○,○○○円
  負債合計:       ○○○,○○○円
  純資産合計:     ○○○,○○○円
  貸借差額:       0円（一致）

■ 決算整理仕訳: N件
  - 減価償却費: ○○○,○○○円
  - 棚卸調整:   ○○○,○○○円
  - 未払計上:   ○○○,○○○円

■ 次のステップ:
  → /income-tax で所得税の計算を行う
  → /consumption-tax で消費税の計算を行う
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## 引継書の出力

サマリー提示後、以下のファイルを Write ツールで出力する。
これにより、セッションの中断や Compact が発生しても次のステップで結果を引き継げる。

### ステップ別ファイルの出力

`.shinkoku/progress/06-settlement.md` に以下の形式で出力する:

```
---
step: 6
skill: settlement
status: completed
completed_at: "{当日日付 YYYY-MM-DD}"
fiscal_year: {tax_year}
---

# 決算整理・決算書作成の結果

## 損益計算書（PL）サマリー

- 売上高: {金額}円
- 売上原価: {金額}円
- 経費合計: {金額}円
- 青色申告特別控除前の所得: {金額}円

## 貸借対照表（BS）サマリー

- 資産合計: {金額}円
- 負債合計: {金額}円
- 純資産合計: {金額}円
- 貸借差額: {金額}円（一致/不一致）

## 決算整理仕訳の一覧

| 内容 | 借方科目 | 貸方科目 | 金額 |
|------|---------|---------|------|
| {減価償却費等} | {科目名} | {科目名} | {金額}円 |
（減価償却、地代家賃按分、棚卸調整、未払計上等を記載）

## 次のステップ

/income-tax で所得税の計算を行う
/consumption-tax で消費税の計算を行う
```

### 進捗サマリーの更新

`.shinkoku/progress/progress-summary.md` を更新する（存在しない場合は新規作成）:

- YAML frontmatter: fiscal_year、last_updated（当日日付）、current_step: settlement
- テーブル: 全ステップの状態を更新（settlement を completed に）
- 次のステップの案内を記載

### 出力後の案内

ファイルを出力したらユーザーに以下を伝える:
- 「引継書を `.shinkoku/progress/` に保存しました。セッションが中断しても次のスキルで結果を引き継げます。」
- 次のステップの案内
