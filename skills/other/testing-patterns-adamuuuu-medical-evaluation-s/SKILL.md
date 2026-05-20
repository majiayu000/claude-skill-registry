---
name: testing-patterns
description: Jest测试模式、工厂函数、模拟策略和TDD工作流。在编写单元测试、创建测试工厂或遵循TDD红绿重构循环时使用。
---

# 测试模式和工具

## 测试哲学

**测试驱动开发（TDD）：**

- 首先编写失败的测试
- 实现最少代码以通过
- 绿灯后重构
- 从不在没有失败测试的情况下编写生产代码

**行为驱动测试：**

- 测试行为，而非实现
- 关注公共API和业务需求
- 避免测试实现细节
- 使用描述行为的清晰测试名称

**工厂模式：**

- 创建`getMockX(overrides?: Partial<X>)`函数
- 提供合理的默认值
- 允许覆盖特定属性
- 保持测试干燥易维护

## 测试工具

### 自定义Render函数

创建一个自定义render，使用必需的providers包装组件：

```typescript
// src/utils/testUtils.tsx
import { render } from '@testing-library/react-native';
import { ThemeProvider } from './theme';

export const renderWithTheme = (ui: React.ReactElement) => {
  return render(
    <ThemeProvider>{ui}</ThemeProvider>
  );
};
```

**使用方法：**

```typescript
import { renderWithTheme } from 'utils/testUtils';
import { screen } from '@testing-library/react-native';

it('应该渲染组件', () => {
  renderWithTheme(<MyComponent />);
  expect(screen.getByText('Hello')).toBeTruthy();
});
```

## 工厂模式

### 组件Props工厂

```typescript
import { ComponentProps } from 'react';

const getMockMyComponentProps = (
  overrides?: Partial<ComponentProps<typeof MyComponent>>
) => {
  return {
    title: '默认标题',
    count: 0,
    onPress: jest.fn(),
    isLoading: false,
    ...overrides,
  };
};

// 在测试中使用
it('应该使用自定义标题渲染', () => {
  const props = getMockMyComponentProps({ title: '自定义标题' });
  renderWithTheme(<MyComponent {...props} />);
  expect(screen.getByText('自定义标题')).toBeTruthy();
});
```

### 数据工厂

```typescript
interface User {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'user';
}

const getMockUser = (overrides?: Partial<User>): User => {
  return {
    id: '123',
    name: '约翰·多伊',
    email: 'john@example.com',
    role: 'user',
    ...overrides,
  };
};

// 使用方法
it('应该为管理员用户显示管理员徽章', () => {
  const user = getMockUser({ role: 'admin' });
  renderWithTheme(<UserCard user={user} />);
  expect(screen.getByText('管理员')).toBeTruthy();
});
```

## 模拟模式

### 模拟模块

```typescript
// 模拟整个模块
jest.mock("utils/analytics");

// 使用工厂函数模拟
jest.mock("utils/analytics", () => ({
  Analytics: {
    logEvent: jest.fn(),
  },
}));

// 在测试中访问模拟
const mockLogEvent = jest.requireMock("utils/analytics").Analytics.logEvent;
```

### 模拟GraphQL Hooks

```typescript
jest.mock("./GetItems.generated", () => ({
  useGetItemsQuery: jest.fn(),
}));

const mockUseGetItemsQuery = jest.requireMock("./GetItems.generated")
  .useGetItemsQuery as jest.Mock;

// 在测试中
mockUseGetItemsQuery.mockReturnValue({
  data: { items: [] },
  loading: false,
  error: undefined,
});
```

## 测试结构

```typescript
describe("ComponentName", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe("渲染", () => {
    it("应该使用默认props渲染组件", () => {});
    it("加载时应该显示加载状态", () => {});
  });

  describe("用户交互", () => {
    it("点击按钮时应该调用onPress", async () => {});
  });

  describe("边界情况", () => {
    it("应该优雅处理空数据", () => {});
  });
});
```

## 查询模式

```typescript
// 元素必须存在
expect(screen.getByText("Hello")).toBeTruthy();

// 元素不应该存在
expect(screen.queryByText("Goodbye")).toBeNull();

// 元素异步出现
await waitFor(() => {
  expect(screen.findByText("已加载")).toBeTruthy();
});
```

## 用户交互模式

```typescript
import { fireEvent, screen } from '@testing-library/react-native';

it('点击按钮时应该提交表单', async () => {
  const onSubmit = jest.fn();
  renderWithTheme(<LoginForm onSubmit={onSubmit} />);

  fireEvent.changeText(screen.getByLabelText('电子邮件'), 'user@example.com');
  fireEvent.changeText(screen.getByLabelText('密码'), 'password123');
  fireEvent.press(screen.getByTestId('login-button'));

  await waitFor(() => {
    expect(onSubmit).toHaveBeenCalled();
  });
});
```

## 要避免的反模式

### 测试模拟行为而非真实行为

```typescript
// 坏 - 测试模拟
expect(mockFetchData).toHaveBeenCalled();

// 好 - 测试实际行为
expect(screen.getByText("约翰·多伊")).toBeTruthy();
```

### 不使用工厂

```typescript
// 坏 - 重复、不一致的测试数据
it("测试1", () => {
  const user = { id: "1", name: "John", email: "john@test.com", role: "user" };
});
it("测试2", () => {
  const user = { id: "2", name: "Jane", email: "jane@test.com" }; // 缺少role！
});

// 好 - 可重用工厂
const user = getMockUser({ name: "自定义名称" });
```

## 最佳实践

1. **始终为props和数据使用工厂函数**
2. **测试行为，而非实现**
3. **使用清晰的测试名称**
4. **使用describe块组织**
5. **在测试之间清除模拟**
6. **保持测试专注** - 每个测试一个行为

## 运行测试

```bash
# 运行所有测试
npm test

# 运行覆盖率
npm run test:coverage

# 运行特定文件
npm test ComponentName.test.tsx
```

## 与其他技能的集成

- **react-ui-patterns**: 测试所有UI状态（加载、错误、空、成功）
- **systematic-debugging**: 编写重现错误的测试，然后修复
