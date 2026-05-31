---
name: fec-typescript-type-safety
description: Use when designing, implementing, or reviewing TypeScript type contracts, advanced generics, discriminated unions, type guards, API DTOs, component props, public utility types, or type-level regressions in frontend projects. Prefer code review for broad PR review; Chinese triggers include TypeScript 类型安全, 类型建模, 泛型, 判别联合, 类型收窄.
---

# TypeScript 类型安全

## Purpose

为前端代码建立可演进的类型契约，减少 `any`、断言和运行时形状漂移。

## Procedure

### 1. 先确定类型边界

把类型分为外部输入、领域模型、UI view model、组件 props、工具函数 API。不要让后端 DTO、表单模型和 UI 展示模型互相冒充。

```ts
interface UserDto {
  id: string;
  display_name: string;
  status: "ACTIVE" | "DISABLED";
}

interface UserViewModel {
  id: string;
  displayName: string;
  status: "active" | "disabled";
}

export function mapUserDto(dto: UserDto): UserViewModel {
  return {
    id: dto.id,
    displayName: dto.display_name,
    status: dto.status === "ACTIVE" ? "active" : "disabled",
  };
}
```

### 2. 用 `unknown` 和收窄处理不可信数据

外部输入先校验再使用。不要用 `as` 让编译器闭嘴。

```ts
interface ApiErrorBody {
  message: string;
}

function isApiErrorBody(value: unknown): value is ApiErrorBody {
  return (
    typeof value === "object" &&
    value !== null &&
    "message" in value &&
    typeof value.message === "string"
  );
}

export function getApiErrorMessage(value: unknown): string {
  return isApiErrorBody(value) ? value.message : "Unexpected error";
}
```

### 3. 用判别联合表达状态机

异步状态、权限分支、支付状态等有限状态，用判别字段让新增分支在编译期暴露。

```ts
type Loadable<T> =
  | { state: "idle" }
  | { state: "loading" }
  | { state: "success"; data: T }
  | { state: "error"; error: Error };

function assertNever(value: never): never {
  throw new Error(`Unhandled state: ${JSON.stringify(value)}`);
}

export function renderUserState(user: Loadable<{ name: string }>): string {
  switch (user.state) {
    case "idle":
      return "Ready";
    case "loading":
      return "Loading";
    case "success":
      return user.data.name;
    case "error":
      return user.error.message;
    default:
      return assertNever(user);
  }
}
```

### 4. 让泛型服务调用方，而不是炫技

泛型应减少重复并保持调用方推断清晰。复杂类型超过阅读成本时，优先拆具名类型。

```ts
interface SelectOption<TValue extends string | number> {
  label: string;
  value: TValue;
}

interface SelectProps<TValue extends string | number> {
  value: TValue;
  options: Array<SelectOption<TValue>>;
  onChange: (value: TValue) => void;
}

export function Select<TValue extends string | number>({
  value,
  options,
  onChange,
}: SelectProps<TValue>) {
  return (
    <select value={value} onChange={(event) => onChange(event.target.value as TValue)}>
      {options.map((option) => (
        <option key={option.value} value={option.value}>
          {option.label}
        </option>
      ))}
    </select>
  );
}
```

### 5. 用类型测试保护公共类型

公共工具类型、组件库类型和 SDK 类型，应有轻量类型测试或编译期断言。

```ts
type Equal<TLeft, TRight> =
  (<T>() => T extends TLeft ? 1 : 2) extends <T>() => T extends TRight ? 1 : 2
    ? true
    : false;

type Expect<T extends true> = T;

type UserStatus = UserViewModel["status"];
type _UserStatusTest = Expect<Equal<UserStatus, "active" | "disabled">>;
```

## Detailed References

涉及高级泛型约束、映射类型、模板字面量类型、类型测试、DTO 映射或类型审查清单时，加载 [references/type-safety-patterns.md](references/type-safety-patterns.md)。

## Constraints

- 避免 `any`、无守卫的非空断言和不相关类型之间的强制 `as`。
- 不把大型匿名类型堆在函数参数或 JSX props 上；提取具名类型表达业务含义。
- 不为简单业务过度设计递归条件类型；类型复杂度应服务可维护性。
- 公共 API 的输入输出必须显式标注，局部变量可依赖推断。
- 类型建模不能替代运行时校验；外部数据仍需 schema 或 type guard。

## Expected Output

产出清晰的类型边界、可收窄的数据模型、必要的类型测试和验证命令。评审时应列出类型风险、运行时影响、推荐建模方式和是否需要专项修复。
