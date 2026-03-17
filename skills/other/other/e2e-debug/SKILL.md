---
name: e2e-debug
description: |
  Analyze and fix failing E2E tests. Includes CI auto-repair mode for GitHub Actions failures.
  Triggers: 「テストが失敗」「CIが落ちている」「テストをデバッグ」「test failed」「flaky test」
  Use when: E2E tests are failing, tests are flaky/unstable, error messages need investigation.
  Outputs: Fixed Page Object and spec files, error analysis reports.
---

# E2E Test Debugger

E2Eテストの失敗を分析し、修正するスキル。

## When to use

- E2Eテストが失敗しているとき
- テストがフレーキー（不安定）なとき
- CI/GitHub Actionsでテストが落ちているとき

## Instructions

### 1. エラーを分析

テストを実行し、エラーメッセージを確認:

```bash
cd frontend && npm run test:e2e -- [test-file].spec.ts
```

### 2. 一般的なエラーパターンと解決策

| エラータイプ | 原因 | 解決策 |
|-------------|------|--------|
| Strict Mode Violation | ロケータが複数要素にマッチ | `.first()` or 親要素でスコープ |
| Element Not Found / Timeout | 要素が見つからない | ロケータ確認、`--headed` で確認 |
| Navigation Timeout | ページ遷移タイムアウト | タイムアウト延長、`waitForURL` |
| net::ERR_ABORTED | 並列実行の不安定性 | `--workers=1` で確認 |
| Hydration Issues | Zustandハイドレーション | ストレージ設定後リロード |
| API Mock Not Working | ルートが先に設定されていない | `page.route()` → `page.goto()` の順序 |

### 3. デバッグツール

```bash
# Playwright Inspector（ステップ実行）
cd frontend && npx playwright test --debug [test-file].spec.ts

# Headed Mode（ブラウザ表示）
cd frontend && npx playwright test --headed [test-file].spec.ts

# Trace Viewer（トレース記録）
cd frontend && npx playwright test --trace on [test-file].spec.ts
cd frontend && npx playwright show-trace test-results/[test-name]/trace.zip
```

### 4. CI自動修復モード

GitHub Actionsからの失敗レポートを分析:

```bash
# JSONレポートから失敗テストを抽出
cd frontend && cat test-results/test-results.json | jq '.. | .specs?[] | select(.ok | not) | {title: .title, file: .file}'
```

### 5. ロケータ変換ルール

| HTML要素 | 属性 | 生成ロケータ |
|----------|------|-------------|
| `<input>` | `aria-label="X"` | `getByLabel('X')` |
| `<button>` | テキスト "X" | `getByRole('button', { name: 'X' })` |
| `<a>` | テキスト "X" | `getByRole('link', { name: 'X' })` |
| `<h1-h6>` | テキスト "X" | `getByRole('heading', { name: 'X' })` |
| 任意 | `data-testid="X"` | `getByTestId('X')` （最終手段） |

## Output

1. エラーの原因分析
2. 修正されたコード
3. テスト成功の確認（`npm run test:e2e`）
