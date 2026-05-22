---
name: webapp-testing
description: |
  Test and verify local web applications using browser automation.
  Triggers: 「ブラウザでテスト」「UIの動作確認」「スクリーンショット」「実際に動かして確認」
  Use when: Verifying frontend functionality, debugging UI behavior, capturing screenshots.
  Uses AntiGravity's browser_subagent for browser interaction.
---

# Web Application Testing

ブラウザ自動化を使用してローカルWebアプリケーションをテスト・検証するスキル。

> [!NOTE]
> エージェントによって使用するツールが異なります:
> - **AntiGravity**: `browser_subagent` (内蔵ツール)
> - **Claude Code**: `playwright` (MCPツール)
>
> [!WARNING]
> このスキルはAntiGravityの `browser_subagent` に最適化されています。Claude Codeで使用する場合は、`browser_subagent` ツールが利用できないため、手動で `playwright` MCPツールを呼び出す必要があります。自動実行は失敗する可能性があります。

## Decision Tree

```text
タスク → 静的HTML?
    ├─ Yes → HTMLファイルを直接読んでセレクタを特定
    │         └─ browser_subagent / Playwright MCP
    │
    └─ No (動的Webapp) → サーバーが起動している?
        ├─ No → run_commandでサーバーを起動
        │        → browser_subagent / Playwright MCP
        │
        └─ Yes → Reconnaissance-then-action
```

## AntiGravity Usage (browser_subagent)

`browser_subagent` ツールを呼び出す際のタスク記述例:

```text
1. http://localhost:<port> にアクセス
2. ページのロードを待つ
3. [対象要素]が表示されていることを確認
4. スクリーンショットを撮影
5. 結果を報告
```

## Claude Code Usage (Playwright MCP)

Claude Codeでは、Playwright MCPサーバーを使用してブラウザ操作を行います。

### 1. Setup & Tools

必要に応じてPlaywrightブラウザをインストール:
```bash
npx playwright install --with-deps chromium
```

主要ツール:
- `playwright_navigate`: ページ遷移
- `playwright_click`: 要素のクリック
- `playwright_fill`: フォーム入力
- `playwright_evaluate`: JS実行
- `playwright_screenshot`: スクリーンショット

### 2. Page Object Model Example

テストコードを作成する場合の推奨パターン:

```typescript
// pages/LoginPage.ts
export class LoginPage {
  constructor(private page: Page) {}

  get emailInput() { return this.page.getByLabel('Email'); }
  get loginButton() { return this.page.getByRole('button', { name: 'Login' }); }

  async login(email: string) {
    await this.emailInput.fill(email);
    await this.loginButton.click();
  }
}
```

### 3. Example Workflow

1. **Navigate**: `playwright_navigate(url="http://localhost:3000")`
2. **Inspect**: `playwright_screenshot` でページ状態を確認
3. **Action**: `playwright_click(selector="text=Login")`


### 3. Reconnaissance-Then-Action

**重要**: 動的アプリでは、DOM検査の前にページの完全なロードを待つこと。

1. **ページに移動** → ロード完了を待つ
2. **DOM/スクリーンショットを確認** → セレクタを特定
3. **アクション実行** → 特定したセレクタを使用

## Best Practices

- サーバー起動は `run_command` で行い、バックグラウンドで実行
- `browser_subagent` のタスク記述は具体的かつ明確にする
- テスト完了条件を明示する
- セマンティックなセレクタを優先（`text=`, `role=`, aria属性）
- スクリーンショットは検証結果の証拠として活用
