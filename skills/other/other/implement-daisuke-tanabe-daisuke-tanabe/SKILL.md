---
name: implement
description: テスト不要なタスクを実装する。 UI 変更・スタイル調整・設定変更・コンポーネント追加など、ユニットテストが不要な変更に使用する。 テストが必要なロジック実装には /tdd を使うこと。
argument-hint: 'タスクの説明（例: "ヘッダーにロゴを追加"）'
allowed-tools: Read, Edit, Write, Glob, Grep, Bash(pnpm --filter *), Bash(mkdir *)
---

# 実装フロー

## Use when

- UI コンポーネントの追加・変更
- スタイル・レイアウト調整
- 設定ファイルの変更
- テスト不要な軽微な変更

## Don't use when

- テストが必要なロジック実装（→ /tdd）
- コードレビューのみ（→ /review）

## 進捗管理

スキル開始時に全ステップを TaskCreate で登録し、各ステップの開始・完了時に TaskUpdate で状態を更新すること。

タスク一覧:

1. Step 1: 分析（activeForm: "要件を分析中"）
2. Step 2: 設計（activeForm: "設計中"）
3. Step 3: 実装（activeForm: "実装中"）
4. Step 4: 検証（activeForm: "検証中"）
5. Step 5: レビュー（activeForm: "レビュー中"）

---

テスト不要なタスク（UI 変更、設定変更など）を実装する。
小規模タスクでは各ステップを簡潔にまとめてよいが、省略はしない。

## 前提

- プロジェクト規約: `CLAUDE.md` に従う
- Lint: `pnpm --filter web lint`
- 型チェック: `pnpm --filter web typecheck`

## タスク

$ARGUMENTS

---

## Step 1: 分析

タスクの要件を整理する。

1. 要件・制約・非要件を明確にする
2. 変更対象のファイルを特定する
3. 影響範囲を確認する

---

## Step 2: 設計

実装の構造を決定する。

1. 責務の分割とインターフェースを決める
2. 既存コードとの統合方針を決める

※ 単純な変更ならファイルと変更箇所の列挙だけでよい。

---

## Step 3: 実装

1. 必要な変更を実装する
2. CLAUDE.md のレイヤー設計・命名規約に従う
3. 最小限の変更に留める

---

## Step 4: 検証

以下をパスすることを確認する:

- `pnpm --filter web lint`
- `pnpm --filter web typecheck`

失敗する場合は TaskUpdate で activeForm を更新し（例: "lint エラーを修正中"）、修正後に再度検証する。

---

## Step 5: レビュー

### 危険フラグ

以下が含まれていないことを確認する:

- ハードコードされた秘密情報
- デバッグ用 `console.log`
- コメントアウトされたコード
- 放置された TODO / FIXME
- `any` 型の乱用

### コード品質

- [ ] CLAUDE.md の規約に準拠している
- [ ] レイヤー設計（依存の方向）を守っている
- [ ] 不要な変更が含まれていない
- [ ] 影響範囲に問題がない

### 完了報告

```
## 実装完了
- 変更ファイル: {ファイル一覧}
- lint: PASS
- typecheck: PASS
- 危険フラグ: なし / あり（詳細）
- 総評: {一言コメント}
```
