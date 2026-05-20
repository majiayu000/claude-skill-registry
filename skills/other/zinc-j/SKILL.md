---
name: zinc-j
description: 本项目 .j 文件中的 Zinc（//! zinc ... //! endzinc）语法与约定：库/结构体写法、匿名函数（无闭包）最佳实践、回调参数传递、资源释放/置空、以及 JASS->Zinc 迁移要点。
---

# Zinc（本项目）语法与约定

## 必须遵守

- 用 `//! zinc` / `//! endzinc` 包裹 Zinc 代码块。
- 禁用 `++/--`；用 `+= 1` / `-= 1`。
- 禁用 `break/continue`；用 `if` 分支或布尔开关改写。
- 数组声明一律用 `type name[];`，不要写大小（例如 `integer a[10]` 是错的）。
- 返回类型用 `-> type` 写在参数列表后；无返回可省略。
- 局部变量统一在函数/匿名函数开头声明：先基础类型，后句柄类型。
- `library` 作用域只允许 `function` 与普通全局变量；不要写 `static method`、`method`、`private static integer` 这类结构体语法。需要 `method/static` 时请放进 `struct`。

## 匿名函数（无闭包）

- 匿名函数内不能直接访问外层局部变量；需要显式传参。
- 传参优先用结构体/库的 `static` 成员变量，并在回调结束后立刻清理为默认值（`null/0/""`）。
- 临时触发器回调用 `CreateTrigger` + `TriggerAddCondition` + `TriggerEvaluate`，随后 `DestroyTrigger` 并置 `null`。

## 句柄生命周期（资源释放）

- 创建出来的句柄资源（`timer/trigger/group/effect/location/...`）：按对应 `Destroy*` / `Remove*` API 释放，并在作用域末尾 `= null`。
- 结构体析构只写 `method onDestroy()`；不要自定义 `destroy()`。

## 结构体/方法写法

- 静态方法：`static method foo(...) -> type { ... }`
- 实例方法：`method foo(...) -> type { ... }`
- 纯静态“管理器”可用 `struct X [] { ... }`（避免 `create/destroy`）。

## JASS -> Zinc 迁移要点

- JASS 默认 `public`；Zinc 默认 `private`：需要对外可见的函数/全局变量要显式 `public`。
- `loop/exitwhen/endloop` 优先改写为 Zinc 的范围 `for (a <= i <= b)` 或常规 for。
- timer/trigger 的一次性逻辑优先改成匿名回调。

## References（按需加载）

- `references/jass-to-zinc.md`
- `references/anonymous-functions.md`
- `references/callback-params.md`
- `references/method-syntax.md`
