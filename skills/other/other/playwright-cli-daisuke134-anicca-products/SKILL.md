---
name: playwright-cli
description: Automates browser interactions for web testing, form filling, screenshots, and data extraction. Use when testing Anicca (landing, webapp) via Tailscale/local URL. Token-efficient (context ~1.3%) vs Playwright MCP (~8%).
---

# playwright-cli

Browser automation CLI. コンテキストを抑えつつブラウザ自動化するため、MCP ではなく CLI + Skills を使う。

## セットアップ（済）

- **インストール**: リポジトリルートの `devDependencies` に `@playwright/cli` を追加済み。ルートで `npx playwright-cli` で実行。
- **.gitignore**: `.playwright-cli/` を除外済み。

## MCP と CLI の使い分け

| 観点 | MCP | CLI (Skills) |
|------|-----|--------------|
| コンテキスト増加量 | 約8% | 約1.3% |
| 操作方式 | ツール呼び出し | Bash コマンド |
| 向いている用途 | インタラクティブなデバッグ | 定型的なフロー確認 |
| セットアップ | .mcp.json に設定 | この SKILL を参照 |

## Quick Start

```bash
npx playwright-cli open https://example.com/
npx playwright-cli snapshot
npx playwright-cli click e3
```

## Core Workflow

1. `open` でページを開く
2. `snapshot` で要素の ref を取得
3. `click`, `fill`, `type` で操作

## Commands

### Core
```bash
npx playwright-cli open <url>              # open url
npx playwright-cli close                   # close the page
npx playwright-cli click <ref>            # perform click
npx playwright-cli fill <ref> <text>      # fill text
npx playwright-cli type <text>            # type text
npx playwright-cli snapshot               # capture page snapshot
npx playwright-cli screenshot [ref]       # take screenshot
```

### Sessions
```bash
npx playwright-cli -s=<name> open <url>   # 名前付きセッションで開く（例: -s=test）
npx playwright-cli -s=<name> open http://localhost:3000 --headed
npx playwright-cli close-all              # 全セッション終了
npx playwright-cli kill-all               # 強制終了
```

### DevTools
```bash
npx playwright-cli tracing-start          # トレース開始
npx playwright-cli tracing-stop           # トレース終了
npx playwright-cli console [min-level]    # コンソールメッセージ
```

## 実際のワークフロー

### Step 1: Skills でフローを確認する

例: 「カテゴリ選択 → サブカテゴリへの遷移」を確認する場合。

1. セッション付きでブラウザを開く:  
   `npx playwright-cli -s=test --headed open http://localhost:3000`  
   （Anicca の場合は PORT や Tailscale URL を必要に応じて変更）
2. `npx playwright-cli -s=test snapshot` で要素の ref を取得。YAML で例:
   - `button "カテゴリ選択" [ref=e39]`
   - `generic "決定" [ref=e15]`
3. モーダルを閉じる: `npx playwright-cli -s=test click e15`
4. カテゴリ選択: `npx playwright-cli -s=test click e39` → snapshot → 選択肢を click
5. サブカテゴリへ: 該当 ref を click
6. 必要なら `npx playwright-cli -s=test screenshot` で確認

この対話でテストに必要な情報（セレクタ、遷移先 URL、モーダルの有無）を収集する。

### Step 2: テストコードを実装する

Step 1 で確認したフローを元に `@playwright/test` でテストを実装。

- `npm install -D @playwright/test` / `npx playwright install chromium`
- `playwright.config.ts` の `baseURL: "http://localhost:3000"`（または Tailscale URL）
- `screenshot: "only-on-failure"`, `video: "on"` などで結果を残す

### Step 3: テスト実行

```bash
npx playwright test --headed
```

動画は `test-results/` に webm で出力される。

## playwright-cli の作業ファイル

| ファイル | 役割 |
|----------|------|
| `.playwright-cli/*.yml` | snapshot の結果（アクセシビリティツリー）。ref 確認用。 |
| `.playwright-cli/*.png` | screenshot の結果。 |

テスト完了後に削除してよい。

```bash
npx playwright-cli close-all
rm -rf .playwright-cli/
```

## まとめ

| ツール | 役割 | タイミング |
|--------|------|------------|
| Playwright CLI + Skills | ブラウザとの対話的なフロー確認 | テスト設計時 |
| @playwright/test | テストコードの実装・実行 | テスト実装・CI |
| Playwright MCP | 複雑なインタラクティブデバッグ | 必要に応じて |

## Reference

- [Playwright CLI (microsoft/playwright-cli)](https://github.com/microsoft/playwright-cli)
- [Zenn: Playwright CLIとClaude Code Skillsで効率的なブラウザテストを実現する](https://zenn.dev/dk_/articles/9db1e90ce8e28f)
