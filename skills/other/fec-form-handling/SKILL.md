---
name: fec-form-handling
description: Use when building or reviewing substantial forms with React Hook Form, Zod schemas, typed validation, dynamic fields, controlled third-party inputs, file upload, multi-step flows, dependent validation, or form performance. Do not use for trivial 1-3 field forms without validation; Chinese triggers include 表单, 表单校验, 动态字段.
---

# 表单处理

## Purpose

管理表单状态、校验和提交，避免复杂表单输入卡顿。

## Procedure

1. 先判断复杂度：10+ 字段、动态字段、联动校验、文件上传、多步流程或输入卡顿时使用 React Hook Form + Zod；极简表单可用原生受控组件。
2. 用 Zod 定义运行时 schema，并用 `z.infer` 推导 TypeScript 类型；schema 是外部输入边界，不要只写 TS 类型。
3. `useForm` 必须提供 `defaultValues`，通过 `zodResolver` 统一校验；错误提示用 `aria-invalid`、`aria-describedby` 和 `role="alert"`。
4. 第三方受控组件用 `Controller`，原生 input 优先 `register`；不要混用两套状态源。
5. 提交时处理 loading、服务端错误、重复提交和 reset；大型表单用局部订阅和子组件隔离控制重渲染。

## Quick Start

```tsx
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";

const loginSchema = z.object({
  email: z.string().email("请输入有效的邮箱地址"),
  password: z.string().min(8, "密码至少 8 个字符"),
});

type LoginForm = z.infer<typeof loginSchema>;

export function LoginFormView() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginForm>({
    resolver: zodResolver(loginSchema),
    defaultValues: { email: "", password: "" },
  });

  return (
    <form onSubmit={handleSubmit((data) => api.login(data))} noValidate>
      <label htmlFor="email">邮箱</label>
      <input id="email" {...register("email")} aria-invalid={!!errors.email} />
      {errors.email && <span role="alert">{errors.email.message}</span>}

      <label htmlFor="password">密码</label>
      <input id="password" type="password" {...register("password")} />
      {errors.password && <span role="alert">{errors.password.message}</span>}

      <button disabled={isSubmitting}>
        {isSubmitting ? "提交中..." : "提交"}
      </button>
    </form>
  );
}
```

## Detailed References

涉及 `Controller`、`useFieldArray`、联动校验、文件上传、多步表单、异步校验和性能模式时，加载 [references/advanced-form-patterns.md](references/advanced-form-patterns.md)。

## Constraints

- React Hook Form 默认非受控；只有第三方受控组件才用 `Controller`。
- `defaultValues` 必须完整，避免 undefined 触发受控/非受控警告。
- `reset()` 应传服务器返回或明确的完整默认对象。
- 异步校验必须 debounce 或放到提交边界，避免每次键入请求。
- Zod `refine` / `superRefine` 的 `path` 必须指向实际字段。

## Expected Output

产出类型安全、可访问、提交状态明确的表单；复杂字段和文件上传有 schema 约束，输入过程无明显卡顿，服务端错误能回填到用户可理解的位置。
