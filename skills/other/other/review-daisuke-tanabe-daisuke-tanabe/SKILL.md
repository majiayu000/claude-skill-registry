---
name: review
description: コードの品質をレビューする。 コミット前の最終チェック・PR レビュー・既存コードの品質監査に使用する。 仕様準拠・危険フラグ・CLAUDE.md 規約の 3 観点で検査する。
argument-hint: 'レビュー対象（例: "src/lib/date.ts" or "直近の変更"）'
allowed-tools: Read, Glob, Grep, Bash(pnpm --filter *), Bash(git diff *), Bash(git log *)
---

# コードレビュー

## Use when

- コミット前の最終チェック
- PR レビュー・既存コードの品質監査
- 特定ファイルや直近の変更のレビュー

## Don't use when

- 実装を伴うタスク（→ /tdd or /implement）

## 進捗管理

スキル開始時に全ステップを TaskCreate で登録し、各ステップの開始・完了時に TaskUpdate で状態を更新すること。

タスク一覧:

1. Step 1: 対象コード読み取り（activeForm: "対象コードを読み取り中"）
2. Step 2: 仕様準拠チェック（activeForm: "仕様準拠をチェック中"）
3. Step 3: 危険フラグ検出（activeForm: "危険フラグを検出中"）
4. Step 4: 規約準拠チェック（activeForm: "規約準拠をチェック中"）
5. Step 5: 検証（activeForm: "検証コマンドを実行中"）

---

指定されたコードをレビューし、問題点を報告する。

## 前提

- プロジェクト規約: `CLAUDE.md` に従う
- Lint: `pnpm --filter web lint`
- 型チェック: `pnpm --filter web typecheck`
- テスト: `pnpm --filter web test:run`

## 対象

$ARGUMENTS

---

## Step 1: 対象コードの読み取り

- ファイルパスが指定された場合: そのファイルを読む
- 「直近の変更」等の場合: `git diff` や `git diff --cached` で差分を確認する
- 関連するテストファイルも確認する

---

## Step 2: 仕様準拠チェック

- [ ] 要件を満たしている
- [ ] エッジケースが考慮されている
- [ ] テストが十分にカバーしている（テストがある場合）

※ 仕様が不明な場合は「仕様未確認」として報告し、確認を推奨する

---

## Step 3: 危険フラグ検出

以下が含まれていないか確認する:

- ハードコードされた秘密情報
- デバッグ用 `console.log`
- コメントアウトされたコード
- 放置された TODO / FIXME
- `any` 型の乱用
- 危険な関数（`eval`, `dangerouslySetInnerHTML` 等）

---

## Step 4: CLAUDE.md 規約準拠チェック

- [ ] レイヤー設計（依存の方向）を守っている
- [ ] 命名規約に従っている（DB: snake_case / コード: camelCase）
- [ ] コンポーネント配置ルールに従っている
- [ ] 不要な変更が含まれていない

---

## Step 5: 検証

該当する検証コマンドを実行する:

- `pnpm --filter web lint`
- `pnpm --filter web typecheck`
- `pnpm --filter web test:run`

---

### 重要度の判定基準

| 重要度 | 基準                                       | 例                                   |
| ------ | ------------------------------------------ | ------------------------------------ |
| high   | セキュリティ・データ損失・本番障害のリスク | 秘密情報のハードコード、未検証の入力 |
| medium | バグの可能性・保守性の低下                 | any 型、テスト不足、命名規約違反     |
| low    | スタイル・推奨事項                         | console.log 残留、TODO 放置          |

## 結果報告

```
## レビュー結果

### 対象
- {ファイル一覧 or 差分の概要}

### 問題一覧
| # | 重要度 | ファイル | 行 | 内容 |
|---|--------|----------|----|------|
| 1 | high/medium/low | {path} | {line} | {説明} |

### 検証結果
- lint: PASS / FAIL
- typecheck: PASS / FAIL
- test: PASS / FAIL

### 総評
{全体的な品質評価と改善提案}
```

問題がない場合は「問題なし」と明記する。
