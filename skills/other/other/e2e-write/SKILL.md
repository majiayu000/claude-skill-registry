---
name: e2e-write
description: |
  Create new E2E tests using Playwright with Page Object Model pattern and semantic locators.
  Triggers: 「E2Eテストを書いて」「テストを作成して」「新機能のテストが必要」「E2E test」「create test」
  Use when: Creating E2E tests for new pages or components, after implementing new features.
  Outputs: Page Object files (frontend/e2e/pages/) and spec files (frontend/e2e/*.spec.ts)
---

# E2E Test Writer

新しいE2Eテストを作成するスキル。Page Object Modelパターンに従い、セマンティックロケータを使用した高品質なテストを生成する。

## When to use

- 新しいページやコンポーネントのE2Eテストを作成するとき
- ユーザーが「E2Eテストを書いて」「テストを作成して」と依頼したとき
- 新機能の実装後にテストが必要なとき

## Instructions

### 1. 対象ページのコンポーネントを調査

対象ページのReactコンポーネントを読み取り、以下を把握する:
- ページのURL
- フォーム要素（input, button, select等）
- aria-label, role属性
- 表示されるテキスト・見出し
- APIエンドポイント

### 2. Page Objectを作成

`frontend/e2e/pages/` に新しいPage Objectを作成:

```typescript
import { Page, expect } from '@playwright/test';
import { BasePage } from './BasePage';

export class [PageName]Page extends BasePage {
  constructor(page: Page) {
    super(page);
  }

  // Locators（セマンティック優先順位を厳守）
  // 1. getByRole - 最優先
  // 2. getByLabel - フォーム要素
  // 3. getByText - テキストコンテンツ
  // 4. getByTestId - 最終手段

  get emailInput() {
    return this.page.getByLabel('メールアドレス*');
  }

  get submitButton() {
    return this.page.getByRole('button', { name: '送信' });
  }

  // Actions
  async goto() {
    await this.page.goto('/path');
  }

  // Assertions
  async expectVisible() {
    await expect(this.emailInput).toBeVisible();
    await expect(this.submitButton).toBeVisible();
  }
}
```

### 3. Page Objectをエクスポート

`frontend/e2e/pages/index.ts` に追加:
```typescript
export { [PageName]Page } from './[PageName]Page';
```

### 4. デスクトップテストファイルを作成

`frontend/e2e/[page-name].spec.ts` を作成:

```typescript
import { test, expect } from '@playwright/test';
import { [PageName]Page } from './pages/[PageName]Page';

test.describe('[PageName]', () => {
  test('should display main content when page is loaded', async ({ page }) => {
    const [pageName]Page = new [PageName]Page(page);
    await [pageName]Page.clearStorage();
    await [pageName]Page.goto();
    await [pageName]Page.expectVisible();
  });
});
```

> **Note**: テスト名は `should [expected behavior] when [condition]` の形式に従うこと。

### 5. モバイルテストファイルを作成

プロジェクト規約に従い、`frontend/e2e/[page-name].mobile.spec.ts` も作成:

```typescript
import { test, expect, devices } from '@playwright/test';
import { [PageName]Page } from './pages/[PageName]Page';

test.use({ ...devices['iPhone 14'] });

test.describe('[PageName] Mobile', () => {
  test('should display main content when viewed on mobile', async ({ page }) => {
    const [pageName]Page = new [PageName]Page(page);
    await [pageName]Page.clearStorage();
    await [pageName]Page.goto();
    await [pageName]Page.expectVisible();
  });
});
```

## Rules

### ロケータの優先順位（必須）

```typescript
// Good - セマンティックロケータ
page.getByRole('button', { name: '送信' })
page.getByLabel('パスワード')

// NG - 実装依存
page.locator('.btn-submit')   // ❌ クラス名
page.locator('#email-input')  // ❌ ID
```

### セクションスコープの使用

ページ内に同じテキストの要素が複数ある場合、親要素でスコープ:

```typescript
// Good - 親要素でスコープ
get featuresSection() {
  return this.page.getByRole('region', { name: /features/i });
}
get searchTeamLink() {
  return this.featuresSection.getByRole('link', { name: /チームデータ検索/ });
}

// NG - ページ全体から検索
this.page.locator('#features')  // ❌ IDセレクタ
```

### 待機処理（必須）

```typescript
// Good - auto-retry assertions
await expect(page.getByRole('button')).toBeVisible();
await expect(page).toHaveURL('/dashboard');

// NG - 固定wait
await page.waitForTimeout(3000);  // ❌
```

### APIモック

```typescript
await page.route('**/api/v2/endpoint', async (route) => {
  await route.fulfill({
    status: 200,
    contentType: 'application/json',
    body: JSON.stringify({ data: 'mock' }),
  });
});
```

## Output

1. `frontend/e2e/pages/[PageName]Page.ts` - Page Object
2. `frontend/e2e/[page-name].spec.ts` - デスクトップテストファイル
3. `frontend/e2e/[page-name].mobile.spec.ts` - モバイルテストファイル
4. `frontend/e2e/pages/index.ts` の更新

> **Important**: テスト作成時はデスクトップ・モバイル**両方**のファイルを生成すること。

作成後、`cd frontend && npm run test:e2e -- [page-name].spec.ts` でテストを実行して動作確認する。
