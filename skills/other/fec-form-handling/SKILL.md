---
name: fec-form-handling
description: 用于构建或审查较复杂表单，包括 React Hook Form、Zod schema、类型化校验、动态字段、受控第三方输入、文件上传、多步骤流程、依赖校验或表单性能。不要用于没有校验的 1-3 个字段小表单；中文触发词包括 表单、表单校验、动态字段。
---

# 表单处理

## 用途

管理表单状态、校验和提交，避免复杂表单输入卡顿。

## 流程

1. 先识别框架、项目既有表单库、schema 校验库、组件库和复杂度；10+ 字段、动态字段、联动校验、文件上传、多步流程或输入卡顿时再引入专门表单方案。
2. 按项目栈选型：React 可考虑 React Hook Form + Zod；Vue 可考虑 vee-validate / FormKit + Zod、Yup 或 Valibot；简单表单可用框架原生状态和基础校验。
3. 用运行时 schema 或明确校验函数守住外部输入边界；TypeScript 类型可从 schema 推导，但不要只写 TS 类型。
4. 明确默认值、字段注册、受控/非受控边界和组件库适配；错误提示用 `aria-invalid`、`aria-describedby` 和 `role="alert"`。
5. 提交时处理 loading、服务端错误、重复提交和 reset；大型表单用局部订阅和子组件隔离控制重渲染。

## React 快速开始

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

## 详细参考

涉及是否需要表单库、框架选型、`Controller`、`useFieldArray`、联动校验、文件上传、多步表单、异步校验和性能模式时，加载 [references/advanced-form-patterns.md](references/advanced-form-patterns.md)。

## 约束

- 沿用仓库既有表单库、schema 库和组件库适配方式，不为单个表单引入第二套体系。
- 默认值必须完整，避免 undefined 触发受控/非受控警告或初始化抖动。
- reset 应传服务器返回或明确的完整默认对象。
- 异步校验必须 debounce 或放到提交边界，避免每次键入请求。
- schema 级联动校验的错误 path 必须指向实际字段。

## 预期输出

产出类型安全、可访问、提交状态明确的表单；复杂字段和文件上传有 schema 约束，输入过程无明显卡顿，服务端错误能回填到用户可理解的位置。
