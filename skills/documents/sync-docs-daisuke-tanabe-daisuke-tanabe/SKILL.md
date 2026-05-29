---
name: sync-docs
description: docs/project/ 配下の仕様書とコードの整合性をチェックする。 実装後・リネーム後・スキーマ変更後の仕様書更新漏れ検出に使用する。 ドキュメント新規作成には使わない（手動で書くこと）。
argument-hint: 'チェック対象（例: "直近の変更" or "スキーマ変更"）'
allowed-tools: Read, Glob, Grep, Bash(git diff *), Bash(git log *)
---

# 仕様書整合性チェック

## Use when

- 実装完了後、コミット前の仕様書更新漏れチェック
- スキーマ変更・リネーム・機能追加の後
- 「仕様書と合ってる？」と聞かれたとき

## Don't use when

- 仕様書の新規作成（→ 手動で書く）
- コードの実装やリファクタリング（→ /implement or /tdd）

## 進捗管理

スキル開始時に全ステップを TaskCreate で登録し、各ステップの開始・完了時に TaskUpdate で状態を更新すること。

タスク一覧:

1. Step 1: 変更範囲の特定（activeForm: "変更範囲を特定中"）
2. Step 2: データモデル整合性チェック（activeForm: "データモデルをチェック中"）
3. Step 3: Server Actions 整合性チェック（activeForm: "Server Actions をチェック中"）
4. Step 4: 用語・その他の整合性チェック（activeForm: "用語をチェック中"）

---

## 対象

$ARGUMENTS

---

## Step 1: 変更範囲の特定

直近の変更内容を把握する。

1. `$ARGUMENTS` の内容に応じて変更範囲を特定する
   - 「直近の変更」→ `git diff HEAD~1` または `git diff --cached` で差分を確認
   - 特定のファイル・機能が指定された場合 → そのファイルを読む
2. 変更に関連する仕様書ファイルを特定する
   - `docs/project/specification.md` — データモデル、Server Actions、変動率計算、バッチ設計
   - `docs/project/requirements.md` — ユースケース、機能要件、画面定義

---

## Step 2: データモデル整合性チェック

`specification.md` のデータモデルと `prisma/schema.prisma` を突合する。

### チェック項目

- [ ] テーブル名が一致している（`@@map` の値）
- [ ] カラム名が一致している（`@map` の値）
- [ ] FK のリレーション先が一致している
- [ ] UNIQUE 制約が一致している
- [ ] 新規追加・削除されたテーブル/カラムが仕様書に反映されている

### 手順

1. `prisma/schema.prisma` を読む
2. `docs/project/specification.md` のデータモデルセクションを読む
3. 両者を突合し、差分を洗い出す

---

## Step 3: Server Actions 整合性チェック

`specification.md` の Server Actions 一覧と `src/actions/` 内の実装を突合する。

### チェック項目

- [ ] Action 名が一致している（関数名）
- [ ] 入力の型/引数が一致している
- [ ] 出力の型が一致している
- [ ] 新規追加・削除された Action が仕様書に反映されている

### 手順

1. `src/actions/` 配下の全ファイルから export された関数を Grep で抽出する
2. `docs/project/specification.md` の Server Actions セクションを読む
3. 両者を突合し、差分を洗い出す

---

## Step 4: 用語・その他の整合性チェック

仕様書全体の用語とコードの命名の一貫性を確認する。

### チェック項目

- [ ] モデル名・テーブル名の用語が仕様書とコードで一致している
- [ ] UI に表示されるラベル（ドメイン用語）が requirements.md の記述と矛盾していない
- [ ] 変動率計算の期間一覧が実装と一致している（specification.md）
- [ ] バッチ設計の記述が実装と矛盾していない（specification.md）

---

## 結果報告

```
## 仕様書整合性チェック結果

### チェック対象
- {変更範囲の概要}

### 齟齬一覧
| # | 仕様書 | セクション | 内容 | 修正案 |
|---|--------|-----------|------|--------|
| 1 | specification.md | データモデル | {差分の説明} | {修正案} |

### 総評
{整合性の全体評価}
```

齟齬がない場合は「齟齬なし — 仕様書は最新の実装と一致しています」と明記する。
齟齬がある場合は修正案を提示するが、自動修正はしない（ユーザーの確認を得てから修正する）。
