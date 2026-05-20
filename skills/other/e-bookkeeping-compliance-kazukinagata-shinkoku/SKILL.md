---
name: e-bookkeeping-compliance
description: >
  優良な電子帳簿の要件チェック・コンプライアンス診断を実行する。
  「優良な電子帳簿」「電帳法対応」「電子帳簿の要件確認」
  「税務調査の準備」「75万円控除の条件」「帳簿の要件を満たしているか」
  「e-bookkeeping compliance」で起動。
---

# 優良な電子帳簿コンプライアンス診断

税務調査への備え、または優良な電子帳簿の要件充足状況を診断するスキル。
電子帳簿保存法施行規則第5条第5項（優良な電子帳簿の要件）に基づき、
shinkoku の帳簿データが要件を満たしているかを自動チェックする。

## 前提知識

- 電帳法の要件詳細: `skills/tax-advisor/reference/electronic-bookkeeping.md`
- システム概要書: `docs/system-overview.md`

---

## Step 0: 前提確認

ユーザーに以下を確認する:

1. **DB パス**: `--db-path` に使用するデータベースファイルのパス
2. **対象年度**: `--fiscal-year` に使用する会計年度
3. **届出書の提出状況**: 「国税関係帳簿の電磁的記録等による保存等に係る届出書」を所轄税務署に提出済みか

> **届出について**: 優良な電子帳簿の保存を適用するには、あらかじめ届出書の提出が必要です。
> 令和9年分から適用する場合は、令和8年中に届出書を提出する必要があります。
> 届出書の様式は国税庁ウェブサイトからダウンロードできます。

---

## Step 1: 自動診断 & サマリー出力

以下のコマンドを実行してシステムの適合状況を診断する。
結果はテーブル形式でユーザーに提示する。

### チェック項目と実行コマンド

| # | 要件 | 条文 | チェック方法 |
|---|------|------|------------|
| G1 | システム関係書類の備付け | 施行規則2条2項1号 | `docs/system-overview.md` ファイルの存在を確認 |
| G2 | 見読可能性の確保 | 施行規則2条2項2号 | `shinkoku ledger trial-balance --db-path <db> --fiscal-year <year>` を実行し、正常出力を確認 |
| G3 | ダウンロード対応 | 施行規則2条2項3号 | `shinkoku ledger search --db-path <db> --input <params> --format csv` を実行し、CSV出力を確認 |
| G4 | 訂正・削除履歴 | 施行規則5条5項1号イ | `shinkoku ledger audit-log --db-path <db>` を実行し、テーブルが機能することを確認 |
| G5 | 相互関連性の確保 | 施行規則5条5項1号ロ | `shinkoku ledger general-ledger --db-path <db> --fiscal-year <year> --account-code <code>` を実行し、仕訳帳⇔総勘定元帳の関連を確認 |
| G6 | 取引先検索 | 施行規則5条5項1号ハ | `counterparty_contains` パラメータで検索を実行 |
| G7 | 日付・金額の範囲指定検索 | 施行規則5条5項1号ハ | `date_from`/`date_to`/`amount_min`/`amount_max` パラメータで検索を実行 |
| G8 | 組合せ検索 | 施行規則5条5項1号ハ | 日付+取引先+金額を組み合わせた検索を実行 |

### 診断手順

1. G1: `docs/system-overview.md` の存在を確認する
2. G2: 残高試算表を生成する
   ```bash
   shinkoku ledger trial-balance --db-path <db> --fiscal-year <year>
   ```
3. G3: 仕訳をCSV形式で出力する
   ```bash
   shinkoku ledger search --db-path <db> --input <params> --format csv
   ```
   （params には `{"fiscal_year": <year>, "limit": 5}` を指定）
4. G4: 監査ログを取得する
   ```bash
   shinkoku ledger audit-log --db-path <db>
   ```
5. G5: 任意の勘定科目で総勘定元帳を出力する（仕訳が存在する科目を使用）
   ```bash
   shinkoku ledger general-ledger --db-path <db> --fiscal-year <year> --account-code <code>
   ```
6. G6-G8: 検索機能のテスト
   ```bash
   # G6: 取引先検索
   shinkoku ledger search --db-path <db> --input <params>
   # params: {"fiscal_year": <year>, "counterparty_contains": "<取引先名の一部>"}

   # G7: 範囲指定検索
   # params: {"fiscal_year": <year>, "date_from": "<開始日>", "date_to": "<終了日>", "amount_min": 1, "amount_max": 1000000}

   # G8: 組合せ検索
   # params: {"fiscal_year": <year>, "date_from": "...", "counterparty_contains": "...", "amount_min": 1}
   ```

### サマリー出力形式

診断結果を以下のテーブル形式で出力する:

```
## 優良な電子帳簿 コンプライアンス診断結果

| # | 要件 | 条文 | 結果 | 備考 |
|---|------|------|------|------|
| G1 | システム関係書類 | 施行規則2条2項1号 | ✓ / ✗ | ... |
| G2 | 見読可能性 | 施行規則2条2項2号 | ✓ / ✗ | ... |
| G3 | ダウンロード対応 | 施行規則2条2項3号 | ✓ / ✗ | ... |
| G4 | 訂正・削除履歴 | 施行規則5条5項1号イ | ✓ / ✗ | ... |
| G5 | 相互関連性 | 施行規則5条5項1号ロ | ✓ / ✗ | ... |
| G6 | 取引先検索 | 施行規則5条5項1号ハ | ✓ / ✗ | ... |
| G7 | 範囲指定検索 | 施行規則5条5項1号ハ | ✓ / ✗ | ... |
| G8 | 組合せ検索 | 施行規則5条5項1号ハ | ✓ / ✗ | ... |
```

不適合項目がある場合は、対応方法を案内する。

---

## Step 2: エビデンス出力（任意）

ユーザーが「詳細を確認」「エビデンスを出力」と依頼した場合に実行する。

### (a) 帳簿出力

以下のコマンドで各帳簿を出力し、テーブル形式でユーザーに提示する:

```bash
# 残高試算表
shinkoku ledger trial-balance --db-path <db> --fiscal-year <year>

# 損益計算書
shinkoku ledger pl --db-path <db> --fiscal-year <year>

# 貸借対照表
shinkoku ledger bs --db-path <db> --fiscal-year <year>

# 総勘定元帳（主要科目）
shinkoku ledger general-ledger --db-path <db> --fiscal-year <year> --account-code <code>
```

CSV出力も可能であることを案内:
```bash
# CSV 形式で出力する場合は --format csv を追加
shinkoku ledger trial-balance --db-path <db> --fiscal-year <year> --format csv
```

### (b) 監査ログ

```bash
shinkoku ledger audit-log --db-path <db> --fiscal-year <year>
```

変更履歴をテーブル形式で表示する。

### (c) 検索デモ

日付範囲・金額範囲・取引先の各検索を実演し、検索機能が正常に動作することを確認する。

### (d) システム関係書類

`docs/system-overview.md` の場所を案内する。必要に応じて内容を表示する。

---

## Step 3: 結果サマリー & 次のアクション

### 全要件充足の場合

```
## 診断結果: 全要件適合

shinkoku は優良な電子帳簿の要件（施行規則第5条第5項）を
技術的に充足しています。

### 次のアクション
1. 届出書の提出（未提出の場合）
   - 「国税関係帳簿の電磁的記録等による保存等に係る届出書」を所轄税務署に提出
2. 定期的なバックアップの実施
3. 帳簿データの7年間保存の確保
```

### 不足事項がある場合

不足事項と対応アクションを一覧で表示する。

### 免責事項

```
> **注記**: 本システムは電子帳簿保存法施行規則第5条第5項に定める優良な電子帳簿の
> 技術的要件を満たすよう設計されています。令和3年度税制改正により事前承認制度は
> 廃止されており、JIIMA認証等の第三者認証は法令上の要件ではありません
> （ただし要件充足の確認手段として活用できます）。
> 優良な電子帳簿の保存の適用にあたっては、あらかじめ所轄税務署への届出書の
> 提出が必要です（電子帳簿保存法第8条第4項）。
```

### 制限事項

```
> **制限事項**:
> - 監査ログ（journal_audit_log）はアプリケーション層で記録しており、
>   データベースの直接操作による変更は記録されません。
>   改ざん防止のためのデータベーストリガーは今後の対応予定です。
> - タイムスタンプは UTC で記録されています（JST への変換は今後対応予定）。
> - 操作者情報の記録は個人利用を前提としているため、現在は未実装です。
```
