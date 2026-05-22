---
name: managing-testing
description: >
  テストワークフローパターン：E2Eテスト生成、テストオーケストレーション。
  自動テストのためのテンプレートとプロセスを提供。
  トリガー: testing, E2E, end-to-end, playwright, test runner, テストオーケストレーション。
allowed-tools: Read, Write, Glob, Task, Bash
user-invocable: false
---

# テストワークフロー管理

自動テスト実行とE2Eテスト生成のためのテストワークフローパターン。

## 目的

個々のコマンドに埋め込まれていたテストワークフローパターンを集約。
コマンドはテストロジックのためにこのスキルを参照する薄いオーケストレーターとなる。

## ワークフローリファレンス

| ワークフロー | リファレンス                                                                                                          | コマンド |
| ------------ | --------------------------------------------------------------------------------------------------------------------- | -------- |
| E2Eテスト    | [@../../skills/managing-testing/references/e2e-workflow.md](../../skills/managing-testing/references/e2e-workflow.md) | /e2e     |

**注**: 自動テストイテレーションには `/ralph-loop`（公式プラグイン）を使用。

## クイックリファレンス

### E2Eテストフロー

```text
1. ブラウザ自動化 (claude-in-chrome)
2. ユーザー操作を記録
3. Playwrightテストコードを生成
4. テストシナリオをドキュメント化
```

### テスト発見優先順位

1. `README.md` を読む → Scriptsセクション
2. `package.json` をチェック → scripts
3. テストファイルを検索 (`*.test.*`, `*.spec.*`)
4. 見つからない場合はユーザーに質問

### 一般的なテストコマンド

| パッケージマネージャ | コマンド     |
| -------------------- | ------------ |
| npm                  | `npm test`   |
| yarn                 | `yarn test`  |
| pnpm                 | `pnpm test`  |
| vitest               | `npx vitest` |
| jest                 | `npx jest`   |

## TDDとの統合

### RGRC + Ralph Loop

```text
/code (RGRCサイクル)
    │
    ├── Red: 失敗するテストを作成
    ├── Green: 最小限の実装
    ├── Refactor: 原則を適用
    └── Commit: 状態を保存

/ralph-loop (自動イテレーション)
    │
    ├── テスト実行
    ├── 失敗を修正
    └── completion-promiseまで繰り返し
```

## ブラウザ自動化 (E2E)

### Claude in Chrome ツール

| ツール        | 目的               |
| ------------- | ------------------ |
| `navigate`    | URLに移動          |
| `click`       | 要素をクリック     |
| `form_input`  | フォーム入力       |
| `read_page`   | ページ内容を読む   |
| `screenshot`  | スクリーンショット |
| `gif_creator` | 操作を記録         |

### E2Eテスト出力

```typescript
test("user can login", async ({ page }) => {
  await page.goto("/login");
  await page.fill("#email", "user@example.com");
  await page.fill("#password", "password");
  await page.click('button[type="submit"]');
  await expect(page).toHaveURL("/dashboard");
});
```

## 参照

### 原則 (rules/)

- [@../../rules/development/COMPLETION_CRITERIA.md](../../rules/development/COMPLETION_CRITERIA.md) - 品質ゲート

### 関連スキル

- `generating-tdd-tests` - TDDの基本
- `automating-browser` - ブラウザ自動化
- `orchestrating-workflows` - 実装ワークフロー

### 使用元コマンド

- `/e2e` - E2Eテスト生成
- `/test` - 手動テスト実行
- `/ralph-loop` - 自動イテレーション（公式プラグイン）
