---
name: e2e-refactor
description: |
  Refactor existing E2E tests to use Page Object Model pattern and semantic locators.
  Triggers: 「テストをリファクタリング」「ロケータを改善」「Page Objectに変換」「refactor test」
  Use when: Tests don't use semantic locators, Page Object pattern not applied, tests use deprecated patterns.
  Outputs: Updated/new Page Objects and refactored spec files.
---

# E2E Test Refactorer

既存のE2Eテストをリファクタリングし、Page Object Modelパターンとセマンティックロケータを適用するスキル。

## When to use

- 既存のE2Eテストがセマンティックロケータを使用していないとき
- Page Objectパターンが適用されていないテストを改善するとき
- 固定waitや非推奨なロケータを使用しているテストを発見したとき

## Instructions

### 1. 既存テストを分析

対象テストファイルを読み取り、以下を特定:
- 使用されているページ/URL
- 直接使用されているロケータ
- 繰り返し使用されているパターン
- 非推奨なロケータ（クラス名、ID等）

### 2. 変換ルール

#### 非推奨ロケータの変換

```typescript
// Before - 実装依存
page.locator('.submit-btn')              // ❌
page.locator('#email')                   // ❌
page.locator('[data-testid="password"]') // ❌

// After - セマンティック
page.getByRole('button', { name: '送信' })     // ✅
page.getByRole('textbox', { name: /メール/ })   // ✅
page.getByLabel('パスワード')                    // ✅
```

#### 固定waitの変換

```typescript
// Before
await page.waitForTimeout(3000);  // ❌

// After
await expect(page.getByRole('heading')).toBeVisible();  // ✅
```

#### 直接ロケータ → Page Object

```typescript
// Before
await page.locator('input#email').fill('test@example.com');
await page.getByRole('button', { name: 'ログイン' }).click();

// After
await loginPage.login('test@example.com', 'password');
```

### 3. セクションスコープの適用

```typescript
// Before - ページ全体から検索
get searchLink() {
  return this.page.getByRole('link', { name: /検索/ });
}

// After - 親要素でスコープ
get featuresSection() {
  return this.page.getByRole('region', { name: /features/i });
}
get searchLink() {
  return this.featuresSection.getByRole('link', { name: /検索/ });
}
```

## Checklist

- [ ] `page.locator('.class')` → `page.getByRole()` / `page.getByLabel()`
- [ ] `page.locator('#id')` → セマンティックロケータ
- [ ] `waitForTimeout()` → auto-retry assertions
- [ ] 繰り返しロケータ → Page Objectのgetter
- [ ] 繰り返しアクション → Page Objectのメソッド
- [ ] 複数要素マッチ → 親要素でスコープ（推奨）or `.first()`
- [ ] 不必要な `.first()` の削除

## Output

1. 更新された/新規のPage Object
2. リファクタリングされたテストファイル
3. テスト実行確認（`cd frontend && npm run test:e2e -- [test-file].spec.ts`）
