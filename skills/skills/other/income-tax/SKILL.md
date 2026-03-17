---
name: income-tax
description: >
  This skill should be used when the user needs to calculate their income tax
  (所得税), compute deductions, or import withholding slips. Trigger phrases
  include: "所得税を計算", "確定申告書を作成", "控除を計算",
  "源泉徴収票を取り込む", "所得税額", "納付額を計算", "還付額を計算",
  "第一表", "第二表", "申告書B", "所得控除", "税額控除".
---

# 所得税計算（Income Tax Calculation）

事業所得・各種控除から所得税額を計算するスキル。
settlement スキルで決算書の作成が完了していることを前提とする。
計算結果は `/e-tax` スキル（Claude in Chrome）で確定申告書等作成コーナーに入力する。

## 設定の読み込み（最初に実行）

1. `shinkoku.config.yaml` を Read ツールで読み込む
2. ファイルが存在しない場合は `/setup` スキルの実行を案内して終了する
3. 設定値を把握し、相対パスは CWD を基準に絶対パスに変換する:
   - `db_path`: CLI スクリプトの `--db-path` 引数に使用
   - `output_dir`: 進捗ファイル等の出力先ベースディレクトリ
   - 各ディレクトリ: ファイル参照時に使用

### パス解決の例

config の `db_path` が `./shinkoku.db` で CWD が `/home/user/tax-2025/` の場合:
- `shinkoku tax calc-income --input /home/user/tax-2025/output/income_input.json`

## 進捗情報の読み込み

設定の読み込み後、引継書ファイルを読み込んで前ステップの結果を把握する。

1. `.shinkoku/progress/progress-summary.md` を Read ツールで読み込む（存在する場合）
2. 以下の引継書を Read ツールで読み込む（存在する場合）:
   - `.shinkoku/progress/06-settlement.md`
   - `.shinkoku/progress/02-assess.md`
   - `.shinkoku/progress/05-furusato.md`
3. 読み込んだ情報を以降のステップで活用する（ユーザーへの再質問を避ける）
4. ファイルが存在しない場合はスキップし、ユーザーに必要情報を直接確認する

## 基本方針

- settlement スキルで青色申告決算書が完成しているか確認してから開始する
- 所得の計算 → 控除の計算 → 税額の計算 の順序で進める
- 各ステップの計算結果をユーザーに提示し、確認を得る
- references/form-b-fields.md の各欄に正しく値を設定する
- 端数処理ルールを厳守する:
  - 課税所得: 1,000円未満切捨て（国税通則法118条）
  - 復興特別所得税: 1円未満切捨て（復興財源確保法13条）
  - ㊺ 所得税及び復興特別所得税の額: 端数処理なし
  - 申告納税額（納付の場合のみ）: 100円未満切捨て（国税通則法119条）
  - 還付金: 1円単位・切捨てなし（国税通則法120条）

## 前提条件の確認

所得税計算を開始する前に以下を確認する:

1. **青色申告決算書が完成しているか**: settlement スキルの出力を確認する
2. **納税者プロファイルの読み込み**: `skills/setup/scripts/profile.py get-taxpayer` で config から納税者情報を取得する
   - 氏名・住所・税務署名 → 確定申告書等作成コーナーへの入力に使用
   - 寡婦/ひとり親・障害者・勤労学生の状態 → 人的控除の計算に使用
3. **事業所得以外の所得**: 給与所得・雑所得・配当所得・一時所得等がある場合は情報を収集する
4. **源泉徴収票**: 給与所得がある場合は取り込みを案内する
5. **各種控除の適用状況**: 適用可能な控除を網羅的に確認する
6. **予定納税額**: assess で確認済みの予定納税額を取得する
   - 未確認の場合は、前年の確定申告書（㊺欄）から判定する
   - 予定納税額は源泉徴収税額とは別に管理する
7. **分離課税の確認**: 株式・FX の分離課税（第三表）は対象外。該当する場合は税理士への相談を案内する

## 必須確認チェックリスト（スキップ不可）

所得税計算を開始する前に、以下の項目が**すべて確認済み**であることを検証する。
config・引継書に記載がない項目は、ユーザーに直接確認してから先に進む。

- [ ] **家族構成**: 配偶者の有無・扶養親族の有無を確認済みか？
  - 未確認 → ユーザーに確認し、ステップ1.5 で詳細を登録する
  - 確認済み（該当なし）→ ステップ1.5 をスキップ可
- [ ] **住宅ローン控除**: 適用有無を確認済みか？
  - 未確認 → ユーザーに確認する
  - 適用あり（初年度）→ ステップ3.7 で明細書を作成する
- [ ] **予定納税**: 有無・金額を確認済みか？
  - 未確認 → 前年の確定申告書（㊺欄）から判定するようユーザーに確認する
  - 金額未確定 → `estimated_tax_payment` パラメータに正しい値を設定できるまで進まない

## ステップ1: 源泉徴収票の取り込み

給与所得がある場合、源泉徴収票からデータを取り込む。

### `import_data.py import-withholding` の呼び出し

```bash
shinkoku import import-withholding --input withholding_input.json
```
入力 JSON:
```json
{
  "file_path": "path/to/withholding_slip.pdf"
}
```
出力:
```json
{
  "payer_name": "支払者名",
  "payment_amount": 5000000,
  "deduction_amount": 3560000,
  "income_tax_withheld": 100000,
  "social_insurance": 700000,
  "life_insurance": 50000,
  "spouse_deduction": 0
}
```

#### 画像ファイルの場合: OCR 読み取り

`extracted_text` が空の場合（画像ファイルまたはスキャン PDF）、画像の読み取りは `/reading-withholding` スキルを使用する。
スキルの指示に従い、デュアル検証（2つの独立した読み取り結果の照合）を行って結果を取得する。

**結果照合:** 両方の読み取り結果から `payment_amount`, `withheld_tax`, `social_insurance` を比較する

**一致の場合:** そのまま採用。「2つの独立した読み取りで結果が一致しました」と報告

**不一致の場合:** ユーザーに元画像パスと両方の結果を提示し、正しい方を選択してもらう:
- 差異のあるフィールドを明示する
- A を採用 / B を採用 / 手動入力 の3択を AskUserQuestion で提示する

**取り込み後の検算（必須）:**

OCR 結果の整合性を検証するため、「所得控除の額の合計額」と各内訳の合計を照合する:

```
検算: 所得控除の額の合計額 ≟ 社会保険料等の金額          ← 小規模企業共済等掛金を含む（内数）
                            + 生命保険料の控除額
                            + 地震保険料の控除額
                            + 配偶者（特別）控除の額
                            + 扶養控除額                ← 人数×単価から算出（特定63万/老人48万or58万/その他38万）
                            + 障害者控除                ← 人数×単価から算出（一般27万/特別40万/同居特別75万）
                            + 寡婦控除（27万）またはひとり親控除（35万） ← 該当時
                            + 勤労学生控除（27万）       ← 該当時
                            + 基礎控除の額              ← 源泉徴収票の記載額を使用。未記載なら所得と年度から算出
```

注意:
- 「（うち小規模企業共済等掛金の額）」は社会保険料等の金額の**内数**。別途加算すると二重計上になる
- 扶養控除・障害者控除は金額欄ではなく人数欄で記載されるため、人数×単価で算出する
- 基礎控除の額は源泉徴収票に記載があればその値を使う。未記載の場合は合計所得と年度に応じて算出する（令和7・8年は特例加算あり、令和9年以降は一律58万）

- **一致の場合:** 各フィールドの OCR 精度が確認できたものとして採用する
- **不一致の場合:** 差額を明示し、どのフィールドが誤読の可能性があるかユーザーに提示する。元画像と突き合わせて修正する

**その他の確認事項:**

1. 複数の勤務先がある場合は各社分を取り込む
2. 年末調整済みの控除を確認し、追加控除の有無を判定する

## ステップ1.5: 扶養親族・配偶者情報の確認

所得控除の計算前に、扶養親族の情報を収集する。
まず DB に登録済みのデータを確認し、不足があれば追加入力する。

### DB からの読み込み

1. `ledger.py get-spouse --db-path DB_PATH` で配偶者情報を取得する（登録済みの場合）
2. `ledger.py list-dependents --db-path DB_PATH` で扶養親族のリストを取得する（登録済みの場合）

### 未登録の場合の確認項目

1. **配偶者**: 配偶者の有無と年間所得金額を確認する
   - 所得48万円以下 → 配偶者控除（38万円）
   - 所得48万円超133万円以下 → 配偶者特別控除（段階的）
   - 納税者の所得が1,000万円超 → 配偶者控除なし
   - 確認後 `ledger.py set-spouse --db-path DB_PATH --input spouse.json` で DB に登録する

2. **扶養親族**: 以下の情報を収集する
   - 氏名、続柄、生年月日、年間所得、障害の有無、同居の有無
   - 16歳未満: 扶養控除なし（児童手当対象）
   - 16歳以上: 一般扶養38万円
   - 19歳以上23歳未満: 特定扶養63万円
   - 70歳以上: 老人扶養48万円（同居58万円）
   - 確認後 `ledger.py add-dependent --db-path DB_PATH --input dependent.json` で各人を DB に登録する

3. **マイナンバーの収集**（申告書B第二表に記載が必要）:
   - 配偶者のマイナンバー（12桁）
   - 扶養親族（16歳以上）全員のマイナンバー
   - 16歳未満の子供のマイナンバー（住民税に関する事項の記載に必要）
   - 取扱注意: DB に保存するが、ツール出力やログには表示しない

4. **事業専従者の確認**:
   - 配偶者が青色事業専従者として給与を受けている場合 → 配偶者控除の対象外
   - 扶養親族が青色事業専従者・白色事業専従者の場合 → 扶養控除の対象外
   - 該当する場合は控除計算から除外し、ユーザーに明示する

5. **障害者控除**: 扶養親族に障害がある場合
   - 一般障害者: 27万円、特別障害者: 40万円、同居特別障害者: 75万円

**重要: 16歳未満の扶養親族も必ず登録する**

16歳未満の子供は扶養控除の対象外だが、以下の理由で申告書への記載が必要:
- 住民税の非課税限度額の判定（扶養人数に16歳未満も含む）
- 住民税の均等割の非課税判定
- 申告書B第二表「住民税に関する事項 - 16歳未満の扶養親族」欄への記載

`ledger.py add-dependent` で登録する際、16歳未満でもスキップせずに登録すること。

## ステップ1.6: iDeCo・小規模企業共済の確認

掛金払込証明書がある場合は `import_data.py import-deduction-certificate` で取り込むことができる。

1. iDeCo（個人型確定拠出年金）の年間掛金を確認する
   - 小規模企業共済等掛金払込証明書から金額を確認
   - 全額が所得控除（上限: 自営業者は年額81.6万円）
2. 小規模企業共済の掛金がある場合も同様に確認する

#### 画像ファイルの場合: OCR 読み取り

`extracted_text` が空の場合（画像ファイルまたはスキャン PDF）、画像の読み取りは `/reading-deduction-cert` スキルを使用する。
スキルの指示に従い、デュアル検証（2つの独立した読み取り結果の照合）を行って結果を取得する。

**結果照合:** 両方の読み取り結果から `annual_premium`, `certificate_type` を比較する

**一致の場合:** そのまま採用。「2つの独立した読み取りで結果が一致しました」と報告

**不一致の場合:** ユーザーに元画像パスと両方の結果を提示し、正しい方を選択してもらう:
- 差異のあるフィールドを明示する
- A を採用 / B を採用 / 手動入力 の3択を AskUserQuestion で提示する

## ステップ1.7: 医療費明細の集計

医療費控除を適用する場合、明細を集計する。

### 医療費の登録・集計

1. `ledger.py list-medical-expenses --db-path DB_PATH --input query.json` で登録済み医療費明細を取得する
2. 未登録の医療費がある場合は `ledger.py add-medical-expense --db-path DB_PATH --input medical.json` で登録する:
   ```json
   {
     "fiscal_year": 2025,
     "detail": {
       "date": "2025-03-15",
       "patient_name": "山田太郎",
       "medical_institution": "ABC病院",
       "amount": 150000,
       "insurance_reimbursement": 0,
       "description": null
     }
   }
   ```
3. 集計結果（total_amount - total_reimbursement）を医療費控除の計算に使用する

## ステップ1.8: 事業所得の源泉徴収（支払調書）

取引先から受け取った支払調書の情報を登録する。

### 支払調書の取り込み

1. `import_data.py import-payment-statement --input payment_input.json` で支払調書PDF/画像からデータを抽出する

#### 画像ファイルの場合: OCR 読み取り

`extracted_text` が空の場合（画像ファイルまたはスキャン PDF）、画像の読み取りは `/reading-payment-statement` スキルを使用する。
スキルの指示に従い、デュアル検証（2つの独立した読み取り結果の照合）を行って結果を取得する。

**結果照合:** 両方の読み取り結果から `gross_amount`, `withholding_tax`, `payer_name` を比較する

**一致の場合:** そのまま採用。「2つの独立した読み取りで結果が一致しました」と報告

**不一致の場合:** ユーザーに元画像パスと両方の結果を提示し、正しい方を選択してもらう:
- 差異のあるフィールドを明示する
- A を採用 / B を採用 / 手動入力 の3択を AskUserQuestion で提示する

2. `ledger.py add-business-withholding --db-path DB_PATH --input withholding.json` で取引先別の源泉徴収情報を登録する:
   ```json
   {
     "fiscal_year": 2025,
     "detail": {
       "client_name": "取引先名",
       "gross_amount": 1000000,
       "withholding_tax": 102100
     }
   }
   ```
3. `ledger.py list-business-withholding --db-path DB_PATH --input query.json` で登録済み情報を確認する
4. 源泉徴収税額の合計を `business_withheld_tax` として所得税計算に使用する

## ステップ1.8.5: 税理士等報酬の登録

税理士・弁護士等に報酬を支払っている場合、報酬明細を登録する。

1. `ledger.py list-professional-fees --db-path DB_PATH --input query.json` で登録済みの税理士等報酬を確認する
2. 未登録の場合は `ledger.py add-professional-fee --db-path DB_PATH --input fee.json` で登録する:
   ```json
   {
     "fiscal_year": 2025,
     "detail": {
       "payer_address": "支払者住所",
       "payer_name": "税理士名",
       "fee_amount": 300000,
       "expense_deduction": 0,
       "withheld_tax": 30630
     }
   }
   ```
3. 源泉徴収税額は `business_withheld_tax` に合算する

## ステップ1.9: 損失繰越の確認

前年以前に事業で損失が発生し、青色申告している場合、繰越控除を適用できる。

1. `ledger.py list-loss-carryforward --db-path DB_PATH --input query.json` で登録済みの繰越損失を確認する
2. 未登録の場合は `ledger.py add-loss-carryforward --db-path DB_PATH --input loss.json` で登録する:
   ```json
   {
     "fiscal_year": 2025,
     "detail": {
       "loss_year": 2023,
       "amount": 500000
     }
   }
   ```
3. 繰越損失の合計を `loss_carryforward_amount` として所得税計算に使用する

## ステップ1.10: その他の所得の確認（雑所得・配当所得・一時所得・年金所得・退職所得）

事業所得・給与所得以外の総合課税の所得を確認・登録する。

### 公的年金等の雑所得

公的年金等の収入がある場合、年金控除を計算して雑所得を求める。

1. 年金収入の有無を確認する
2. `skills/income-tax/scripts/tax_calc.py calc-pension` で公的年金等控除を計算する:
   ```bash
   shinkoku tax calc-pension --input pension_input.json
   ```
   入力 JSON:
   ```json
   {
     "pension_income": 2000000,
     "is_over_65": true,
     "other_income": 0
   }
   ```
   出力:
   ```json
   {
     "pension_income": 2000000,
     "deduction_amount": 1100000,
     "taxable_pension_income": 900000,
     "other_income_adjustment": 0
   }
   ```
3. `taxable_pension_income` を雑所得として `misc_income` に加算する
4. 令和7年改正: 65歳未満の最低保障額60万→70万、65歳以上の最低保障額110万→130万

### 退職所得

退職金を受け取った場合、退職所得を計算する。

1. 退職金の有無を確認する
2. `skills/income-tax/scripts/tax_calc.py calc-retirement` で退職所得を計算する:
   ```bash
   shinkoku tax calc-retirement --input retirement_input.json
   ```
   入力 JSON:
   ```json
   {
     "severance_pay": 10000000,
     "years_of_service": 20,
     "is_officer": false,
     "is_disability_retirement": false
   }
   ```
   出力:
   ```json
   {
     "severance_pay": 10000000,
     "retirement_income_deduction": 8000000,
     "taxable_retirement_income": 1000000,
     "half_taxation_applied": true
   }
   ```
3. 退職所得は原則分離課税（退職時に源泉徴収済み）だが、確定申告で精算する場合もある
4. 役員等の短期退職（勤続5年以下）は1/2課税が適用されない

### 雑所得（miscellaneous）

副業の原稿料、暗号資産の売却益、その他の雑収入。

1. `ledger.py list-other-income --db-path DB_PATH --input query.json` で登録済み雑所得を確認する
2. 未登録の収入がある場合は `ledger.py add-other-income --db-path DB_PATH --input other_income.json` で登録する:
   ```json
   {
     "fiscal_year": 2025,
     "detail": {
       "income_type": "miscellaneous",
       "description": "収入の内容",
       "revenue": 500000,
       "expenses": 50000,
       "withheld_tax": 51050,
       "payer_name": "支払者名"
     }
   }
   ```
3. 雑所得 = 収入 - 経費（特別控除なし）

### 仮想通貨（暗号資産）

暗号資産の売却益は雑所得（総合課税）として申告する。

1. `ledger.py list-crypto-income --db-path DB_PATH --input query.json` で登録済み仮想通貨所得を確認する
2. 未登録の場合は `ledger.py add-crypto-income --db-path DB_PATH --input crypto.json` で取引所別に登録する:
   ```json
   {
     "fiscal_year": 2025,
     "detail": {
       "exchange_name": "取引所名",
       "gains": 300000,
       "expenses": 10000
     }
   }
   ```
3. 合計を雑所得として total_income に加算する

### 配当所得（総合課税選択分）

総合課税を選択した配当は配当控除（税額控除）の対象となる。

1. `ledger.py list-other-income --db-path DB_PATH --input query.json` で `income_type: "dividend_comprehensive"` を確認する
2. 未登録の場合は `ledger.py add-other-income --db-path DB_PATH --input dividend.json` で登録する
3. 配当控除: 課税所得1,000万以下の部分 → 配当の10%、超える部分 → 5%

### 一時所得

保険満期金、懸賞金等の一時的な所得。

1. `ledger.py list-other-income --db-path DB_PATH --input query.json` で `income_type: "one_time"` を確認する
2. 未登録の場合は `ledger.py add-other-income --db-path DB_PATH --input one_time.json` で登録する
3. 一時所得 = max(0, (収入 - 経費 - 特別控除50万円)) × 1/2

### `calc_income_tax` への反映

上記のその他所得は以下のパラメータで `calc_income_tax` に渡す:
- `misc_income`: 雑所得合計（仮想通貨含む）
- `dividend_income_comprehensive`: 配当所得（総合課税選択分）
- `one_time_income`: 一時所得の収入金額（1/2 計算は内部で実施）
- `other_income_withheld_tax`: その他所得の源泉徴収税額合計

## ステップ1.11: （対象外）分離課税

分離課税（株式・FX の第三表）は対象外。該当する場合は税理士への相談を案内する。

## ステップ1.12: 社会保険料の種別別内訳の登録

所得控除の内訳書に種別ごとの記載が必要なため、社会保険料を種別別に登録する。

社会保険料の控除証明書がある場合は `import_data.py import-deduction-certificate` で取り込むことができる。

1. `ledger.py list-social-insurance-items --db-path DB_PATH --input query.json` で登録済み項目を確認する
2. 未登録の場合は `ledger.py add-social-insurance-item --db-path DB_PATH --input insurance.json` で種別ごとに登録する:
   ```json
   {
     "fiscal_year": 2025,
     "detail": {
       "insurance_type": "national_health",
       "name": "保険者名",
       "amount": 300000
     }
   }
   ```
   insurance_type: national_health / national_pension / national_pension_fund / nursing_care / labor_insurance / other
3. 合計額を `social_insurance` として控除計算に使用する

## ステップ1.13: 保険契約の保険会社名の登録

所得控除の内訳書に保険会社名の記載が必要なため、保険契約を登録する。

控除証明書の画像・PDFがある場合は `import_data.py import-deduction-certificate` で取り込むことができる。
取り込み後、抽出データに基づいて `ledger.py add-insurance-policy` で登録する。

1. `ledger.py list-insurance-policies --db-path DB_PATH --input query.json` で登録済み項目を確認する
2. 未登録の場合は `ledger.py add-insurance-policy --db-path DB_PATH --input policy.json` で登録する:
   ```json
   {
     "fiscal_year": 2025,
     "detail": {
       "policy_type": "life_general_new",
       "company_name": "保険会社名",
       "premium": 80000
     }
   }
   ```
   policy_type: life_general_new / life_general_old / life_medical_care / life_annuity_new / life_annuity_old / earthquake / old_long_term
3. 生命保険料は `life_insurance_detail` パラメータに、地震保険料は `earthquake_insurance_premium` に反映する

## ステップ1.14: ふるさと納税以外の寄附金の確認

政治活動寄附金、認定NPO法人、公益社団法人等への寄附金を確認する。

1. `ledger.py list-donations --db-path DB_PATH --input query.json` で登録済み寄附金を確認する
2. 未登録の場合は `ledger.py add-donation --db-path DB_PATH --input donation.json` で登録する:
   ```json
   {
     "fiscal_year": 2025,
     "detail": {
       "donation_type": "npo",
       "recipient_name": "寄附先名",
       "amount": 50000,
       "date": "2025-06-01",
       "receipt_number": null
     }
   }
   ```
   donation_type: political / npo / public_interest / specified / other
3. 寄附金控除の計算:
   - **所得控除**: 全寄附金 - 2,000円（総所得金額の40%上限）
   - **税額控除（政治活動寄附金）**: (寄附金 - 2,000円) × 30%（所得税額の25%上限）
   - **税額控除（認定NPO等）**: (寄附金 - 2,000円) × 40%（所得税額の25%上限）
4. `calc_deductions` の `donations` パラメータに寄附金レコードのリストを渡す

## ステップ2: 所得控除の計算

### `tax_calc.py calc-deductions` の呼び出し

```bash
shinkoku tax calc-deductions --input deductions_input.json
```
入力 JSON:
```json
{
  "total_income": 5000000,
  "social_insurance": 700000,
  "life_insurance_premium": 80000,
  "earthquake_insurance_premium": 30000,
  "medical_expenses": 200000,
  "furusato_nozei": 50000,
  "housing_loan_balance": 0,
  "spouse_income": null,
  "ideco_contribution": 276000,
  "dependents": [],
  "fiscal_year": 2025,
  "housing_loan_detail": null,
  "donations": null
}
```
出力 (DeductionsResult):
- `income_deductions`: 所得控除の一覧（basic_deduction, social_insurance_deduction, life_insurance_deduction, earthquake_insurance_deduction, ideco_deduction, medical_deduction, furusato_deduction, donation_deduction, spouse_deduction, dependent_deduction, disability_deduction）
- `tax_credits`: 税額控除の一覧（housing_loan_credit, political_donation_credit, npo_donation_credit）
- `total_income_deductions`: 所得控除合計
- `total_tax_credits`: 税額控除合計

**各控除の確認事項:**

- 基礎控除: 合計所得金額に応じた段階的控除（令和7年分の改正を反映、132万以下=95万）
- 社会保険料控除: 国民年金・国民健康保険・その他の年間支払額
- 生命保険料控除: 新旧制度 × 3区分（一般/介護医療/個人年金）で計算する
  - `life_insurance_detail` パラメータで5区分の保険料を指定:
    - `general_new`: 一般（新制度）、`general_old`: 一般（旧制度）
    - `medical_care`: 介護医療（新制度のみ）
    - `annuity_new`: 個人年金（新制度）、`annuity_old`: 個人年金（旧制度）
  - 各区分の上限: 新制度 40,000円 / 旧制度 50,000円 / 合算上限 40,000円
  - 3区分合計の上限: 120,000円
  - 源泉徴収票に生命保険料5区分の記載がある場合はそのまま使用する
- 地震保険料控除: 地震保険（上限5万円）+ 旧長期損害保険（上限1.5万円）、合算上限5万円
  - `old_long_term_insurance_premium` パラメータで旧長期損害保険料を指定可能
- 小規模企業共済等掛金控除: 3サブタイプ個別追跡
  - iDeCo（個人型確定拠出年金）
  - 小規模企業共済
  - 心身障害者扶養共済
  - `small_business_mutual_aid` パラメータで小規模企業共済掛金を指定
- 医療費控除: 支払額から保険金等の補填額を差し引き、10万円（または所得の5%）を超える部分
  - **セルフメディケーション税制との選択適用**: OTC医薬品の購入額 - 12,000円（上限 88,000円）
  - 医療費控除とセルフメディケーションは併用不可。有利な方を選択する
- 配偶者控除/特別控除: 配偶者の所得に応じて段階的に控除額が変動
- 扶養控除: 年齢区分に応じた控除額（一般38万/特定63万/老人48万or58万）
- 障害者控除: 障害の程度に応じた控除額
- **人的控除**（config の納税者情報から自動判定）:
  - 寡婦控除: 27万円（所得500万以下）
  - ひとり親控除: 35万円（所得500万以下）
  - 障害者控除（本人）: 一般 27万円 / 特別 40万円
  - 勤労学生控除: 27万円（所得75万以下）
- ふるさと納税: 寄附金 − 2,000円（確定申告ではワンストップ特例分も含める）
- 住宅ローン控除: 住宅区分別の年末残高上限と控除率0.7%（令和4年以降入居）

## ステップ3: 所得税額の計算

### `tax_calc.py calc-income` の呼び出し

```bash
shinkoku tax calc-income --input income_input.json
```
入力 JSON (IncomeTaxInput):
```json
{
  "fiscal_year": 2025,
  "salary_income": 5000000,
  "business_revenue": 3000000,
  "business_expenses": 1000000,
  "blue_return_deduction": 650000,
  "social_insurance": 700000,
  "life_insurance_premium": 80000,
  "earthquake_insurance_premium": 30000,
  "medical_expenses": 0,
  "furusato_nozei": 50000,
  "housing_loan_balance": 0,
  "spouse_income": null,
  "ideco_contribution": 276000,
  "withheld_tax": 100000,
  "business_withheld_tax": 30000,
  "estimated_tax_payment": 0,
  "loss_carryforward_amount": 0
}
```
出力 (IncomeTaxResult):
- `salary_income_after_deduction`: 給与所得控除後の金額
- `business_income`: 事業所得
- `total_income`: 合計所得金額（繰越損失適用後）
- `total_income_deductions`: 所得控除合計
- `taxable_income`: 課税所得金額（1,000円未満切り捨て）
- `income_tax_base`: 算出税額
- `total_tax_credits`: 税額控除合計
- `income_tax_after_credits`: 税額控除後
- `reconstruction_tax`: 復興特別所得税（基準所得税額 x 2.1%）
- `total_tax`: 所得税及び復興特別所得税の額（端数処理なし）
- `withheld_tax`: 源泉徴収税額（給与分）
- `business_withheld_tax`: 事業所得の源泉徴収税額
- `estimated_tax_payment`: 予定納税額
- `loss_carryforward_applied`: 適用した繰越損失額
- `tax_due`: 申告納税額（= total_tax - withheld_tax - business_withheld_tax - estimated_tax_payment）

**寄附金控除の反映:**

ふるさと納税以外の寄附金控除（ステップ1.14で登録）は、`calc_deductions` の結果に含まれている。
`calc_income_tax` は内部で `calc_deductions` を呼び出すため、以下のパラメータが正しく渡されていれば自動的に反映される:
- `furusato_nozei`: ふるさと納税の寄附金合計
- 政治活動寄附金・認定NPO等の税額控除は `calc_deductions` の `donations` パラメータ経由で計算される

所得税計算前に `calc_deductions` を個別に呼び出す場合は、`donations` パラメータにステップ1.14で登録した寄附金レコードのリストを必ず渡すこと。

**青色申告特別控除の自動キャップ:**

`blue_return_deduction` は config の値をそのまま渡してよい。計算エンジンが事業利益を上限として自動キャップする（租特法25条の2）。
結果の `effective_blue_return_deduction` と `warnings` を必ず確認すること。

**計算結果の確認:**

1. 合計所得金額の内訳を表示する
2. `effective_blue_return_deduction` を確認し、自動調整があれば `warnings` の内容を表示する
3. 繰越損失が適用されている場合はその額を明示する
4. 所得税の速算表の適用が正しいか確認する
5. 復興特別所得税が正しく加算されているか確認する
6. 源泉徴収税額（給与分 + 事業分）が正しく控除されているか確認する
7. 予定納税額が正しく控除されているか確認する
8. 最終的な納付額（または還付額）を明示する

所得税の速算表・配偶者控除テーブル・住宅ローン限度額等は `references/deduction-tables.md` を参照。

## ステップ3.1: サニティチェック（必須）

`calc-income` の結果を自動検証する。このステップはスキップ不可。

### `tax_calc.py sanity-check` の呼び出し

```bash
shinkoku tax sanity-check --input sanity_input.json
```
入力 JSON:
```json
{
  "input": { ... },
  "result": { ... }
}
```
- `input`: ステップ3で `calc-income` に渡した IncomeTaxInput
- `result`: ステップ3で `calc-income` から返された IncomeTaxResult

出力 (TaxSanityCheckResult):
- `passed`: true/false
- `items`: チェック項目のリスト（severity, code, message）
- `error_count`: エラー件数
- `warning_count`: 警告件数

### 結果に応じた対応

- **error > 0**: 計算結果に問題があります。エラー内容を確認し、入力を修正してステップ3を再実行してください
- **warning > 0**: 警告内容をユーザーに提示し、確認してから続行してください
- **passed = true**: 問題なし。次のステップに進む

## ステップ3.5: 住宅ローン控除明細の DB 登録（該当者のみ）

住宅ローン控除（初年度）を適用する場合、詳細情報を DB に登録する。

1. `ledger.py add-housing-loan-detail --db-path DB_PATH --input housing.json` で住宅ローン控除の明細を登録する:
   ```json
   {
     "fiscal_year": 2025,
     "detail": {
       "housing_type": "new_custom",
       "housing_category": "certified",
       "move_in_date": "2024-03-15",
       "year_end_balance": 30000000,
       "is_new_construction": true,
       "is_childcare_household": false,
       "has_pre_r6_building_permit": false,
       "purchase_date": "2024-01-20",
       "purchase_price": 40000000,
       "total_floor_area": 8000,
       "residential_floor_area": 8000,
       "property_number": null,
       "application_submitted": false
     }
   }
   ```

住宅区分別の年末残高上限テーブルは `references/deduction-tables.md` を参照。

## ステップ6: 計算結果サマリーの提示

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
所得税の計算結果（令和○年分）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

■ 所得金額（総合課税）
  事業所得:           ○○○,○○○円
  給与所得:           ○○○,○○○円
  雑所得:             ○○○,○○○円（該当者のみ）
  配当所得:           ○○○,○○○円（総合課税分、該当者のみ）
  一時所得:           ○○○,○○○円（該当者のみ）
  合計所得金額:       ○○○,○○○円

■ 所得控除
  社会保険料控除:     ○○○,○○○円
  生命保険料控除:      ○○,○○○円
  基礎控除:           480,000円
  [その他の控除...]
  所得控除合計:       ○○○,○○○円

■ 税額計算
  課税所得金額:       ○○○,○○○円
  算出税額:           ○○○,○○○円
  税額控除:            ○○,○○○円
  復興特別所得税:       ○,○○○円
  所得税及び復興特別所得税: ○○○,○○○円
  源泉徴収税額:       ○○○,○○○円
  予定納税額:          ○○,○○○円
  ---------------------------------
  申告納税額:          ○○,○○○円（納付 / 還付）

■ 次のステップ:
  → /consumption-tax で消費税の計算を行う
  → /e-tax で確定申告書等作成コーナーに入力する（Claude in Chrome）
  → /submit で提出準備を行う
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## 引継書の出力

サマリー提示後、以下のファイルを Write ツールで出力する。
これにより、セッションの中断や Compact が発生しても次のステップで結果を引き継げる。

### ステップ別ファイルの出力

`.shinkoku/progress/07-income-tax.md` に以下の形式で出力する:

```
---
step: 7
skill: income-tax
status: completed
completed_at: "{当日日付 YYYY-MM-DD}"
fiscal_year: {tax_year}
---

# 所得税計算・確定申告書作成の結果

## 所得金額の内訳

- 事業所得: {金額}円
- 給与所得: {金額}円
- 雑所得: {金額}円（該当者のみ、仮想通貨含む）
- 配当所得（総合課税）: {金額}円（該当者のみ）
- 一時所得: {金額}円（該当者のみ）
- 合計所得金額: {金額}円

## 扶養親族・配偶者

- 配偶者控除/特別控除: {適用あり（控除額）/適用なし}
- 扶養控除: {適用あり（控除額、人数）/適用なし}

## iDeCo・小規模企業共済

- 小規模企業共済等掛金控除: {金額}円（{iDeCo/小規模企業共済/なし}）

## 医療費控除

- 適用: {あり/なし}
- 医療費控除額: {金額}円

## 事業所得の源泉徴収

- 源泉徴収税額（事業分）: {金額}円

## 損失繰越控除

- 適用: {あり/なし}
- 繰越損失控除額: {金額}円

## 所得控除の内訳

| 控除項目 | 金額 |
|---------|------|
| 基礎控除 | {金額}円 |
| 社会保険料控除 | {金額}円 |
| 生命保険料控除 | {金額}円 |
| 地震保険料控除 | {金額}円 |
| 小規模企業共済等掛金控除 | {金額}円 |
| 医療費控除 | {金額}円 |
| 寄附金控除 | {金額}円 |
| 配偶者控除/特別控除 | {金額}円 |
| 扶養控除 | {金額}円 |
| 障害者控除 | {金額}円 |
| **所得控除合計** | **{金額}円** |

## 税額計算

- 課税所得金額: {金額}円
- 算出税額: {金額}円
- 税額控除（住宅ローン控除等）: {金額}円
- 復興特別所得税: {金額}円
- 所得税及び復興特別所得税: {金額}円
- 源泉徴収税額（給与分）: {金額}円
- 源泉徴収税額（事業分）: {金額}円
- 予定納税額: {金額}円
- **申告納税額: {金額}円（{納付/還付}）**

## 次のステップ

/consumption-tax で消費税の計算を行う
/e-tax で確定申告書等作成コーナーに入力する（Claude in Chrome）
/submit で提出準備を行う
```

### 進捗サマリーの更新

`.shinkoku/progress/progress-summary.md` を更新する（存在しない場合は新規作成）:

- YAML frontmatter: fiscal_year、last_updated（当日日付）、current_step: income-tax
- テーブル: 全ステップの状態を更新（income-tax を completed に）
- 次のステップの案内を記載

### 出力後の案内

ファイルを出力したらユーザーに以下を伝える:
- 「引継書を `.shinkoku/progress/` に保存しました。セッションが中断しても次のスキルで結果を引き継げます。」
- 次のステップの案内

## Additional Resources

### Reference Files

詳細なテーブル・パラメータは以下を参照:
- **`references/form-b-fields.md`** — 確定申告書B様式の各欄の対応
- **`references/deduction-tables.md`** — 所得税速算表、配偶者控除テーブル、基礎控除テーブル、住宅ローン限度額、生命保険料控除等

## 免責事項

- この計算は一般的な所得税の計算ロジックに基づく
- 分離課税（株式・FX）は対象外 — 第三表の計算は行わない
- 白色申告（収支内訳書）は対象外
- 不動産所得、譲渡所得（不動産売却等）、退職所得は現時点で未対応
- 最終的な申告内容は税理士等の専門家に確認することを推奨する
