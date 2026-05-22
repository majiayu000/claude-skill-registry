---
name: unit-test
description: 単体テストの作成。「テストを書きたい」「ユニットテストを追加」「関数をテスト」などのリクエスト時に使用。
---

# Unit Test

コンポーネント・関数の単体テストを作成するスキル。

## 推奨テストフレームワーク

- **Vitest**: 高速なテストランナー（Vite ベース）
- **React Testing Library**: コンポーネントテスト
- **@testing-library/user-event**: ユーザー操作シミュレーション

## セットアップ（未設定の場合）

```bash
pnpm add -D vitest @vitejs/plugin-react jsdom
pnpm add -D @testing-library/react @testing-library/jest-dom @testing-library/user-event
```

### vitest.config.ts

```typescript
import react from "@vitejs/plugin-react";
import { defineConfig } from "vitest/config";

export default defineConfig({
  plugins: [react()],
  test: {
    environment: "jsdom",
    globals: true,
    setupFiles: ["./vitest.setup.ts"],
    include: ["src/**/*.{test,spec}.{ts,tsx}"],
  },
  resolve: {
    alias: {
      "@": "./src",
    },
  },
});
```

### vitest.setup.ts

```typescript
import "@testing-library/jest-dom/vitest";
```

## テストファイル配置

```text
src/
├── components/
│   ├── Button.tsx
│   └── Button.test.tsx      # コンポーネントと同階層
├── lib/
│   ├── utils.ts
│   └── utils.test.ts        # ユーティリティと同階層
└── __tests__/               # 統合テスト用（オプション）
```

## テストテンプレート

### コンポーネントテスト

```typescript
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import { Button } from "./Button";

describe("Button", () => {
  it("renders with text", () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole("button", { name: /click me/i })).toBeInTheDocument();
  });

  it("calls onClick when clicked", async () => {
    const user = userEvent.setup();
    const handleClick = vi.fn();

    render(<Button onClick={handleClick}>Click me</Button>);
    await user.click(screen.getByRole("button"));

    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it("is disabled when disabled prop is true", () => {
    render(<Button disabled>Click me</Button>);
    expect(screen.getByRole("button")).toBeDisabled();
  });
});
```

### 関数テスト

```typescript
import { describe, expect, it } from "vitest";

import { formatDate, slugify } from "./utils";

describe("formatDate", () => {
  it("formats date correctly", () => {
    expect(formatDate("2025-01-01")).toBe("2025年1月1日");
  });

  it("handles invalid date", () => {
    expect(formatDate("invalid")).toBe("Invalid Date");
  });
});

describe("slugify", () => {
  it("converts string to slug", () => {
    expect(slugify("Hello World")).toBe("hello-world");
  });
});
```

### 非同期テスト

```typescript
import { render, screen, waitFor } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { AsyncComponent } from "./AsyncComponent";

describe("AsyncComponent", () => {
  it("shows loading state initially", () => {
    render(<AsyncComponent />);
    expect(screen.getByText(/loading/i)).toBeInTheDocument();
  });

  it("shows data after loading", async () => {
    render(<AsyncComponent />);
    await waitFor(() => {
      expect(screen.getByText(/data loaded/i)).toBeInTheDocument();
    });
  });
});
```

## テスト実行コマンド

```bash
# 全テスト実行
pnpm test

# ウォッチモード
pnpm test:watch

# カバレッジ付き
pnpm test:coverage

# 特定ファイル
pnpm test src/lib/utils.test.ts
```

## package.json scripts

```json
{
  "scripts": {
    "test": "vitest run",
    "test:watch": "vitest",
    "test:coverage": "vitest run --coverage"
  }
}
```

## テスト作成の手順

1. テスト対象のコード確認
2. テストケースの洗い出し
   - 正常系
   - 異常系
   - 境界値
3. テストファイル作成（`*.test.ts(x)`）
4. describe でグループ化
5. it/test で個別ケース記述
6. テスト実行・確認

## ベストプラクティス

- **AAA パターン**: Arrange（準備）→ Act（実行）→ Assert（検証）
- **1テスト1検証**: 各テストは1つの振る舞いを検証
- **実装詳細をテストしない**: 内部実装ではなく振る舞いをテスト
- **getByRole 優先**: アクセシビリティを意識したクエリ
- **ユーザー視点**: ユーザーの操作をシミュレート

## クエリ優先順位

1. `getByRole` - アクセシビリティ
2. `getByLabelText` - フォーム要素
3. `getByPlaceholderText` - 入力フィールド
4. `getByText` - テキストコンテンツ
5. `getByTestId` - 最終手段
