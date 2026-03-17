---
name: setup
description: >
  This skill should be used when the user wants to set up shinkoku for the first
  time, initialize their configuration, or update their existing settings.
  Trigger phrases include: "セットアップ", "初期設定", "設定ファイルを作る",
  "shinkokuの設定", "config", "setup", "始め方", "使い方", "設定を更新",
  "configを作り直す".
---

# セットアップウィザード（Setup Wizard）

shinkoku の初回セットアップを対話的に行うスキル。
設定ファイル（`shinkoku.config.yaml`）の生成とデータベースの初期化を実施する。

## ステップ0: CLI のインストール確認

`shinkoku` コマンドが利用可能か確認する。

1. `shinkoku --version` を実行する
2. **コマンドが存在しない場合**: `uv tool install git+https://github.com/kazukinagata/shinkoku` を実行してインストールする
3. **コマンドが存在する場合**: `uv tool upgrade shinkoku` を実行して最新版に更新する

## ステップ1: 既存設定の確認

CWD の `shinkoku.config.yaml` を Read ツールで読み込む。

- **ファイルが存在する場合**: 内容を表示し、更新するか確認する。更新しない場合はスキルを終了する。
- **ファイルが存在しない場合**: セットアップウィザードを開始する。

## ステップ2: 基本設定のヒアリング

以下の項目を AskUserQuestion で確認する:

### 2-1. 対象年度

- `tax_year`: 確定申告の対象年度（デフォルト: 2025）

### 2-1b. 事業所得の有無

- `has_business_income`: 事業所得（副業含む）の有無（true / false）

事業所得がない場合、以下のステップをスキップする:
- 2-2（インボイス登録番号）
- 2.6-3（事業所住所）
- 2.7（事業情報）
- 2.8 の申告の種類（blue/white）・記帳方法の質問（給与所得のみなら不要）

### 2-2. 適格請求書発行事業者の登録番号（事業所得がある場合のみ）

- `invoice_registration_number`: T + 13桁の番号（任意、スキップ可）

## ステップ2.5: 納税者情報のヒアリング

以下の項目を AskUserQuestion で段階的に確認する。すべて任意（スキップ可能）だが、確定申告書等作成コーナーへの入力や人的控除の判定に使用される。

### 2.5-1. 氏名

- `taxpayer.last_name`: 姓
- `taxpayer.first_name`: 名
- `taxpayer.last_name_kana`: 姓（カタカナ）
- `taxpayer.first_name_kana`: 名（カタカナ）

### 2.5-2. 基本情報

- `taxpayer.gender`: 性別（male / female）
- `taxpayer.date_of_birth`: 生年月日（YYYY-MM-DD）
- `taxpayer.phone`: 電話番号
- `taxpayer.relationship_to_head`: 世帯主との続柄（本人/妻/夫/子等）

### 2.5-3. マイナンバー

- `taxpayer.my_number`: マイナンバー12桁（取扱注意 — config に保存するが、ツール出力やログには一切表示しない）

### 2.5-4. 人的控除に関する状態（任意）

- `taxpayer.widow_status`: 寡婦/ひとり親の区分（none / widow / single_parent）
- `taxpayer.disability_status`: 障害者の区分（none / general / special）
- `taxpayer.working_student`: 勤労学生に該当するか（true / false）

## ステップ2.6: 住所情報のヒアリング

### 2.6-1. 自宅住所

- `address.postal_code`: 郵便番号
- `address.prefecture`: 都道府県
- `address.city`: 市区町村
- `address.street`: 番地
- `address.building`: 建物名・部屋番号（任意）

### 2.6-2. 1月1日時点の住所（異なる場合のみ）

- `address.jan1_address`: 1/1 時点の住所（住民税の課税自治体判定に使用）

### 2.6-3. 事業所住所（事業所得がある場合のみ。自宅と異なる場合のみ）

- `business_address.postal_code` 〜 `business_address.building`

## ステップ2.7: 事業情報のヒアリング

事業所得がある場合に確認する。

- `business.trade_name`: 屋号
- `business.industry_type`: 業種
- `business.business_description`: 事業内容
- `business.establishment_year`: 開業年

## ステップ2.8: 申告方法の確認

以下の項目を順に確認し、青色申告特別控除額を**自動判定**する。

### ヒアリング項目

- `filing.submission_method`: 提出方法（e-tax / mail / in-person）
  - **mail / in-person を選択した場合**、選択直後に以下を伝える:
    > このプラグインの帳簿管理・税額計算機能はご利用いただけますが、確定申告書等作成コーナーへの自動入力（`/e-tax` スキル）は e-Tax 提出専用のため利用できません。作成コーナーへの入力はご自身で行っていただく必要があります。
  - e-tax を選択した場合は通知不要（フルサポート）
- `filing.return_type`: 申告の種類（blue / white）— **事業所得がある場合のみ質問する**（事業所得がない場合はスキップ）
  - **white を選択した場合**、選択直後に以下を伝える:
    > 白色申告に対応しています。決算書コーナーでは収支内訳書を使用します。なお、帳簿機能は複式簿記ベースで設計されているため、白色申告に必要な水準以上の記帳が行われます。
  - blue を選択した場合は通知不要
- `filing.tax_office_name`: 所轄税務署名

### 青色申告特別控除の自動判定フロー

`return_type` が `blue` の場合、以下のフローで控除額を判定する:

1. 記帳方法を聞く（複式簿記 / 簡易帳簿）
2. **簡易帳簿の場合** → `simple_bookkeeping: true`、控除額 = 100,000円で確定
3. **複式簿記の場合**:
   - **e-Tax提出** (`submission_method: e-tax`) → 控除額 = 650,000円で確定（`electronic_bookkeeping` は不問）
   - **書面提出** (`submission_method: mail` or `in-person`) → `electronic_bookkeeping` を聞く
     - `true`（優良な電子帳簿保存あり） → 控除額 = 650,000円
       - **true を選択した場合**、選択直後に以下を伝える:
         > 優良な電子帳簿保存の適用には、あらかじめ「国税関係帳簿の電磁的記録等による保存等に係る届出書」を所轄税務署に提出する必要があります。届出書の様式は国税庁ウェブサイトからダウンロードできます。
         > 令和9年分から適用する場合は、令和8年中に届出書を提出してください。
         > なお、届出済みかどうかの確認や、システムの要件充足状況の診断は `/e-bookkeeping-compliance` スキルで実行できます。
     - `false` → 控除額 = 550,000円

4. 判定結果をユーザーに表示して確認する

### 関連フィールド

- `filing.blue_return_deduction`: 青色申告特別控除額（自動判定される。手動指定も可）
  - 650,000: 複式簿記 + (e-Tax提出 又は 電子帳簿保存) + 期限内申告
  - 550,000: 複式簿記 + 書面提出 + 期限内申告（e-Tax/電子帳簿保存なし）
  - 100,000: 簡易帳簿 又は 期限後申告
- `filing.simple_bookkeeping`: 簡易帳簿かどうか（true / false、デフォルト: false）
- `filing.electronic_bookkeeping`: 優良な電子帳簿保存の有無（true / false）。e-Tax提出の場合は不問（65万円控除にはe-Taxだけで十分）

## ステップ2.9: 控除・申告に影響する重要事項の確認（スキップ不可）

以下の項目は所得税額・住民税に大きく影響するため、**全項目について必ず確認する**。
「該当なし」も含め、明示的な回答を得ること。未確認のまま次のステップに進んではならない。

### 2.9-1. 家族構成（配偶者・扶養親族）

以下を確認し、config に保存する。詳細（所得金額・障害区分等）は `/income-tax` で登録する。

- `family.has_spouse`: 配偶者の有無（true / false）
  - true の場合:
    - 配偶者の年間所得（概算）を確認し、配偶者控除/特別控除の適用可能性を把握する
    - 所得48万円以下 → 配偶者控除、48万〜133万円 → 配偶者特別控除
    - **事業専従者かどうか**: 青色事業専従者として給与を受けている配偶者は配偶者控除の対象外
- `family.has_dependents`: 扶養親族の有無（true / false）
  - true の場合: 人数と概要（子・親など）を確認する
  - **16歳未満の子供も含める**: 扶養控除は対象外だが、住民税の非課税判定・均等割判定に
    必要なため、申告書第二表「住民税に関する事項」に記載が必要
  - **事業専従者は除外**: 青色事業専従者・白色事業専従者は扶養親族に該当しない
- `family.dependent_count`: 扶養親族の人数（16歳未満を含む）

※ 配偶者・扶養親族のマイナンバーは `/income-tax` スキルのステップ1.5 で収集する。

### 2.9-2. 住宅ローン控除

- `housing_loan.applicable`: 住宅ローン控除の適用有無（true / false）
  - true の場合:
    - `housing_loan.first_year`: 初年度かどうか（true / false）
    - 初年度 → `/income-tax` のステップ3.7 で計算明細書を作成する（添付書類が別途必要）
    - 2年目以降 → 年末調整で適用済みなら確定申告での追加手続きは原則不要

### 2.9-3. 予定納税

- `estimated_tax.applicable`: 予定納税の有無（true / false）
  - 判定基準: 前年の確定申告書の㊺欄（申告納税額）が **15万円以上** → 予定納税あり
  - true の場合:
    - `estimated_tax.amount`: 予定納税の合計額（第1期 + 第2期、int 円）を確認する
    - 減額申請をした場合は減額後の金額を記入する

### 2.9-4. 世帯主の氏名（本人でない場合）

ステップ2.5-2 で `relationship_to_head` が「本人」以外の場合:
- `taxpayer.household_head_name`: 世帯主の氏名を確認する（申告書に記載が必要）

## ステップ3: パス設定

以下のパスを確認する。デフォルト値を提示し、変更がなければそのまま採用する。

- `db_path`: データベースファイルのパス（デフォルト: `./shinkoku.db`）
- `output_dir`: 進捗ファイル等の出力先ディレクトリ（デフォルト: `./output`）

## ステップ4: 書類ディレクトリの設定（任意）

以下のディレクトリを設定するか確認する。スキップ可能。

- `invoices_dir`: 請求書PDF等のディレクトリ
- `withholding_slips_dir`: 源泉徴収票のディレクトリ
- `receipts_dir`: レシート・領収書のディレクトリ
- `bank_statements_dir`: 銀行明細CSVのディレクトリ
- `credit_card_statements_dir`: クレジットカード明細CSVのディレクトリ
- `deductions_dir`: 控除関連書類のディレクトリ
- `past_returns_dir`: 過去の確定申告データのディレクトリ

## ステップ5: 設定のプレビューと保存

1. 収集した設定内容を YAML 形式でプレビュー表示する
2. ユーザーの確認を得る
3. Write ツールで CWD に `shinkoku.config.yaml` を保存する

YAML の形式は以下のテンプレートに従う:

```yaml
# shinkoku ユーザー設定ファイル
# /setup スキルで対話的に生成できます。

# 対象年度
tax_year: {tax_year}

# 事業所得の有無（副業含む）
has_business_income: {has_business_income}

# データベースファイルのパス
db_path: {db_path}

# 進捗ファイル等の出力先ディレクトリ
output_dir: {output_dir}

# 適格請求書発行事業者の登録番号（T + 13桁）
invoice_registration_number: {invoice_registration_number}

# --- 納税者情報 ---
taxpayer:
  last_name: {last_name}
  first_name: {first_name}
  last_name_kana: {last_name_kana}
  first_name_kana: {first_name_kana}
  gender: {gender}
  date_of_birth: {date_of_birth}
  phone: {phone}
  my_number: {my_number}
  widow_status: {widow_status}
  disability_status: {disability_status}
  working_student: {working_student}
  relationship_to_head: {relationship_to_head}

# --- 住所 ---
address:
  postal_code: {postal_code}
  prefecture: {prefecture}
  city: {city}
  street: {street}
  building: {building}
  jan1_address: {jan1_address}

# --- 事業所住所（自宅と異なる場合のみ） ---
business_address:
  postal_code:
  prefecture:
  city:
  street:
  building:

# --- 事業情報 ---
business:
  trade_name: {trade_name}
  industry_type: {industry_type}
  business_description: {business_description}
  establishment_year: {establishment_year}

# --- 申告方法 ---
filing:
  submission_method: {submission_method}
  return_type: {return_type}
  blue_return_deduction: {blue_return_deduction}
  simple_bookkeeping: {simple_bookkeeping}
  electronic_bookkeeping: {electronic_bookkeeping}
  tax_office_name: {tax_office_name}

# --- 家族構成 ---
family:
  has_spouse: {has_spouse}
  has_dependents: {has_dependents}
  dependent_count: {dependent_count}

# --- 住宅ローン控除 ---
housing_loan:
  applicable: {applicable}
  first_year: {first_year}

# --- 予定納税 ---
estimated_tax:
  applicable: {applicable}
  amount: {amount}

# --- 書類ディレクトリ（任意） ---
invoices_dir: {invoices_dir}
withholding_slips_dir: {withholding_slips_dir}
past_returns_dir: {past_returns_dir}
deductions_dir: {deductions_dir}
receipts_dir: {receipts_dir}
bank_statements_dir: {bank_statements_dir}
credit_card_statements_dir: {credit_card_statements_dir}
```

未設定の項目は値を空にする（`key:` のみ）。

**`my_number` の取扱い**: マイナンバーは config YAML に保存するが、`profile.py` の出力では `has_my_number: true/false` のみ返す。ログ・会話には出力しない。確定申告書等作成コーナーへの入力時のみ config から直接読み取る。

```bash
shinkoku profile --config PATH
```

## ステップ5.5: Git セーフティ設定

ユーザーの個人情報・財務データが誤って git にコミットされないよう、`.gitignore` を設定する。

### 手順

1. `git rev-parse --is-inside-work-tree` を実行し、CWD が git リポジトリかどうか確認する

2. **git リポジトリでない場合** → 以下のメッセージを表示してスキップする:
   > 現在のディレクトリは git リポジトリではありません。今後 git リポジトリ化する場合は、`.gitignore` に shinkoku 関連ファイルを追加して個人情報の漏洩を防いでください。

3. **git リポジトリの場合**:
   a. CWD の `.gitignore` を Read ツールで読み込む（存在しなければ新規作成前提で進める）
   b. 以下の必須エントリが `.gitignore` に含まれているか確認する:
      ```
      # shinkoku 確定申告データ（個人情報を含む — 削除しないこと）
      shinkoku.config.yaml
      shinkoku.db
      shinkoku.db-wal
      shinkoku.db-shm
      .shinkoku/
      output/
      ```
   c. ステップ4で設定された書類ディレクトリ（`invoices_dir`, `receipts_dir` 等）があれば、それも追加対象にする
   d. 不足しているエントリがある場合:
      - 追加するエントリの一覧をユーザーに提示する
      - ユーザーの確認を得てから `.gitignore` に追記する（既存の内容は保持し、末尾に追加する）
   e. 既に全エントリが含まれている場合 → 「`.gitignore` は設定済みです」と表示してスキップする

## ステップ6: データベースの初期化

1. `db_path` の値を確認し、相対パスの場合は CWD を基準に絶対パスに変換する
2. `ledger.py init` コマンドでデータベースを初期化する:
   ```bash
   shinkoku ledger init --db-path DB --fiscal-year YEAR
   ```
   - `--fiscal-year`: ステップ2 で設定した `tax_year`
   - `--db-path`: 絶対パスに変換した値

## ステップ7: 次のステップの案内

セットアップ完了後、以下を案内する:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
セットアップ完了
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

■ 生成されたファイル:
  → shinkoku.config.yaml（設定ファイル）
  → {db_path}（データベース）

■ 次のステップ:
  1. /assess — 申告要否・種類の判定
  2. /gather — 必要書類の確認・収集
  3. /journal — 仕訳入力・帳簿管理
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## 引継書の出力

サマリー提示後、以下のファイルを Write ツールで出力する。
これにより、セッションの中断や Compact が発生しても次のステップで結果を引き継げる。

### ステップ別ファイルの出力

`.shinkoku/progress/01-setup.md` に以下の形式で出力する:

```
---
step: 1
skill: setup
status: completed
completed_at: "{当日日付 YYYY-MM-DD}"
fiscal_year: {tax_year}
---

# セットアップ結果

## 設定内容

- 対象年度: {tax_year}
- データベースパス: {db_path}
- 出力ディレクトリ: {output_dir}
- インボイス登録番号: {invoice_registration_number}

## 納税者情報

- 氏名: {last_name} {first_name}
- 生年月日: {date_of_birth}
- マイナンバー: {登録済み/未登録}
- 寡婦/ひとり親: {widow_status}
- 障害者区分: {disability_status}
- 勤労学生: {working_student}
- 世帯主との続柄: {relationship_to_head}

## 住所

- 自宅: {postal_code} {prefecture}{city}{street}{building}
- 1/1時点の住所: {jan1_address}（同上/異なる住所）
- 事業所住所: {設定あり/自宅と同じ}

## 事業情報

- 屋号: {trade_name}
- 業種: {industry_type}
- 事業内容: {business_description}

## 申告方法

- 提出方法: {submission_method}
- 申告の種類: {return_type}
- 青色申告特別控除: {blue_return_deduction}円
- 所轄税務署: {tax_office_name}

## 控除・申告に影響する重要事項

- 配偶者: {あり（概算所得: ○万円）/ なし}
- 扶養親族: {あり（○人、うち16歳未満○人）/ なし}
- 住宅ローン控除: {適用あり（初年度/2年目以降）/ 適用なし}
- 予定納税: {あり（合計○円）/ なし}
- 世帯主: {本人 / ○○（氏名）}

## 書類ディレクトリ

- 請求書: {invoices_dir}
- 源泉徴収票: {withholding_slips_dir}
- レシート: {receipts_dir}
- 銀行明細: {bank_statements_dir}
- クレカ明細: {credit_card_statements_dir}
- 控除関連: {deductions_dir}
- 過去の申告: {past_returns_dir}

## DB初期化

- 初期化結果: 成功
- 勘定科目マスタ: 登録済み

## 次のステップ

/assess で申告要否・種類を判定する
```

未設定の項目は「未設定」と記載する。

### 進捗サマリーの更新

`.shinkoku/progress/progress-summary.md` を新規作成する:

- YAML frontmatter: fiscal_year、last_updated（当日日付）、current_step: setup
- テーブル: 全ステップの状態を記載（setup を completed に、他は pending に）
- 次のステップの案内を記載

### 出力後の案内

ファイルを出力したらユーザーに以下を伝える:
- 「引継書を `.shinkoku/progress/` に保存しました。セッションが中断しても次のスキルで結果を引き継げます。」
- 次のステップの案内
