---
name: fec-component-testing
description: Use when authoring or reviewing frontend unit, component, or light integration tests close to UI code, including React Testing Library, Vue Test Utils, hooks/composables, props/emits, callbacks, accessible queries, user-event interactions, mocks, loading/error/empty states, and regression coverage. For layer planning, real-browser journeys, or existing validation failures, choose the matching testing or validation workflow first; Chinese triggers include 组件测试, 组件单测, 单元测试, 轻量集成测试.
---

# 组件测试

## Purpose

用贴近代码和用户行为的测试验证纯逻辑、组件契约与轻量模块协作，减少重构和 UI 交互回归。

## Procedure

### 1. 先确定测试层级

- 单元测试：纯函数、hooks/composables、utils、状态逻辑、schema。
- 组件测试：props/emits、回调、用户交互、loading/error/empty、mock 边界。
- 轻量集成测试：表单 + API mock + Router/Store/Provider 上下文。

跨页面真实浏览器流程分流到 E2E workflow；测试层选择不清楚时先做测试分层规划。

### 2. 优先按用户可感知行为测试

```tsx
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { SearchBox } from "./SearchBox";

test("submits the entered keyword", async () => {
  const user = userEvent.setup();
  const onSearch = vi.fn();

  render(<SearchBox onSearch={onSearch} />);

  await user.type(screen.getByRole("searchbox", { name: /keyword/i }), "orders");
  await user.click(screen.getByRole("button", { name: /search/i }));

  expect(onSearch).toHaveBeenCalledWith("orders");
});
```

### 3. Vue 组件使用可访问查询或明确文本断言

```ts
import { mount } from "@vue/test-utils";
import UserMenu from "./UserMenu.vue";

test("emits logout when the logout item is clicked", async () => {
  const wrapper = mount(UserMenu, {
    props: { userName: "Ada" },
  });

  await wrapper.get('[data-testid="logout-button"]').trigger("click");

  expect(wrapper.emitted("logout")).toHaveLength(1);
});
```

优先使用角色、标签和可见文本；仅在没有稳定语义时使用 `data-testid`。

### 4. 控制 mock 边界

```ts
vi.mock("../api/users", () => ({
  fetchUsers: vi.fn(async () => [{ id: "1", name: "Ada" }]),
}));
```

- mock 网络、时间、路由和浏览器 API。
- 不 mock 被测组件的内部函数。
- 对设计系统基础组件只做轻量 mock，保留可访问行为。

### 5. 覆盖关键状态

每个复杂组件至少覆盖：

- 默认渲染。
- 用户交互和回调。
- loading / empty / error。
- 权限或禁用态。
- 键盘交互和焦点行为（适用时）。

### 6. 保持测试可维护

```ts
function setup() {
  const user = userEvent.setup();
  const onSubmit = vi.fn();
  render(<ProfileForm onSubmit={onSubmit} />);
  return { user, onSubmit };
}
```

将重复渲染逻辑放入 `setup`，但不要隐藏测试的核心操作和断言。

## Constraints

- 避免测试实现细节，例如内部 state 名称、私有函数调用、DOM 层级快照。
- 不把 snapshot 作为交互组件的主要断言；它只能辅助检查稳定静态输出。
- 异步断言使用 `findBy*` 或 `waitFor`，不要用固定延迟。
- 测试名称应描述用户场景，而不是函数名。
- 组件测试不能替代 E2E；路由、真实浏览器兼容和跨页流程仍需 E2E。

## Expected Output

产出与组件同目录或项目约定目录下的测试文件，覆盖核心交互、状态和回归场景。验证时运行项目现有 test 命令，确认失败信息能定位到用户行为或组件契约。
