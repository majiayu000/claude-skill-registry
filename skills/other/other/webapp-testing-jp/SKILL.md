---
name: webapp-testing-jp
description: Simplified Japanese web application testing skill covering unit tests, E2E tests, integration tests, Japanese text validation, IME input testing, and naming conventions. Triggers on requests for Webテスト, テスト自動化, E2Eテスト, 日本語テスト, Japanese web testing.
---

# Webアプリケーション テスト支援スキル

## 概要

Webアプリケーションのテスト設計・実装を支援するスキルです。日本語テキスト検証、IME入力テスト、全角・半角混在処理など、日本語Webアプリ特有のテスト観点をカバーします。

## テストの種類

| 種類 | ツール | 対象 |
|------|--------|------|
| **ユニットテスト** | Vitest, Jest | 関数、コンポーネント単体 |
| **統合テスト** | Vitest, Jest | 複数モジュールの連携 |
| **E2Eテスト** | Playwright | ブラウザ上のユーザー操作全体 |

## 日本語テキスト検証

### 全角・半角混在テスト

```typescript
describe("全角・半角変換", () => {
  test("全角英数字を半角に変換できる", () => {
    expect(toHalfWidth("Ａ Ｂ Ｃ１２３")).toBe("ABC123");
  });

  test("半角カタカナを全角に変換できる", () => {
    expect(toFullWidthKatakana("ｶﾀｶﾅ")).toBe("カタカナ");
  });

  test("全角・半角混在文字列を正しく処理する", () => {
    expect(normalize("Ｔｅｓｔテスト123")).toBe("Testテスト123");
  });
});
```

### 文字コードテスト

```typescript
describe("文字コード処理", () => {
  test("UTF-8の日本語文字列を正しく処理する", () => {
    const text = "日本語テスト文字列🎌";
    expect(processText(text)).toHaveLength(10);
  });

  test("Shift_JISからUTF-8への変換が正しい", () => {
    const sjisBuffer = encodeShiftJIS("日本語");
    expect(decodeToUTF8(sjisBuffer)).toBe("日本語");
  });

  test("サロゲートペア文字を正しく扱う", () => {
    const text = "𠮷野家"; // 𠮷はサロゲートペア
    expect([...text]).toHaveLength(3);
  });
});
```

### 日本語バリデーション

```typescript
describe("日本語入力バリデーション", () => {
  test("電話番号の形式を検証する", () => {
    expect(isValidPhoneNumber("03-1234-5678")).toBe(true);
    expect(isValidPhoneNumber("090-1234-5678")).toBe(true);
    expect(isValidPhoneNumber("0120-123-456")).toBe(true);
    expect(isValidPhoneNumber("12345")).toBe(false);
  });

  test("郵便番号の形式を検証する", () => {
    expect(isValidPostalCode("123-4567")).toBe(true);
    expect(isValidPostalCode("1234567")).toBe(true);
    expect(isValidPostalCode("123-456")).toBe(false);
  });

  test("全角カタカナのみを許可する", () => {
    expect(isFullWidthKatakana("カタカナ")).toBe(true);
    expect(isFullWidthKatakana("ｶﾀｶﾅ")).toBe(false);
    expect(isFullWidthKatakana("かたかな")).toBe(false);
  });
});
```

## IME入力テスト

### 変換確定前後の挙動

```typescript
describe("IME入力処理", () => {
  test("composition中はバリデーションを実行しない", async ({ page }) => {
    const input = page.locator("#name-input");

    // IME入力開始（compositionstart）
    await input.dispatchEvent("compositionstart");
    await input.fill("にほんご");
    // 変換確定前はエラー表示されないことを確認
    await expect(page.locator(".error-message")).not.toBeVisible();

    // IME変換確定（compositionend）
    await input.dispatchEvent("compositionend");
    // 確定後にバリデーションが走ることを確認
    await expect(input).toHaveValue("にほんご");
  });
});
```

### Composition Events のテスト観点

| イベント | テスト内容 |
|---------|-----------|
| `compositionstart` | バリデーションの一時停止 |
| `compositionupdate` | 変換候補表示中の挙動 |
| `compositionend` | 確定後のバリデーション実行 |
| 変換キャンセル | Escキーによる入力取消の処理 |

## ツール設定

### Playwright（E2Eテスト）

```typescript
// playwright.config.ts
export default defineConfig({
  use: {
    locale: "ja-JP",
    timezoneId: "Asia/Tokyo",
  },
});
```

### Vitest（ユニット・統合テスト）

```typescript
// vitest.config.ts
export default defineConfig({
  test: {
    globals: true,
    environment: "jsdom",
  },
});
```

## テストケース日本語命名規則

### 命名のルール

```typescript
// describe: 「テスト対象」を記述
describe("郵便番号入力フォーム", () => {

  // test: 「条件 → 期待結果」の形式
  test("正しい形式の郵便番号を入力すると住所が自動補完される", () => { });
  test("不正な形式の場合はエラーメッセージが表示される", () => { });
  test("ハイフンなしの7桁数字でも受け付ける", () => { });
});
```

### 命名のポイント

- `test()` の説明文は「〜すると〜される」の形式で統一
- 正常系・異常系・境界値を明確に区別する
- テスト実行結果のログが日本語で読めるようにする

## テスト設計時の確認事項

1. **対象ブラウザ**: テスト実行環境（Chromium / Firefox / WebKit）
2. **入力パターン**: 全角・半角・絵文字・サロゲートペア文字の考慮
3. **ロケール依存**: 日付形式、通貨表示、ソート順の検証
4. **文字数カウント**: `String.length` と `[...str].length` の違いに注意
