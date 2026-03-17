---
name: compose-hooks
description: |
  ComposeHooks 项目使用指南 - 为 Jetpack Compose/Compose Multiplatform 提供 React Hooks 风格的状态管理和副作用处理。
  使用此技能当需要：(1) 在 Compose 中管理组件状态 (useState, useGetState, useReducer)，
  (2) 处理副作用和生命周期 (useEffect, useMount, useUnmount)，
  (3) 管理网络请求 (useRequest)，(4) 使用防抖/节流 (useDebounce, useThrottle)，
  (5) 管理列表/Map状态 (useList, useMap)，(6) 使用定时器 (useInterval, useTimeoutFn/useTimeoutPoll/useCountdown)，
  (7) 全局状态管理 (useSelector, useDispatch)，(8) 使用无头表格 (useTable/useTableRequest)。
  关键词: Compose, Hooks, 状态管理, useRequest, useReducer, useState, useEffect
---

# ComposeHooks 使用指南

ComposeHooks 是一个为 Jetpack Compose/Compose Multiplatform 设计的 Hooks 库，灵感来自 React Hooks 和 ahooks。

## 核心概念

所有 `useXxx` 函数都有对应的 `rememberXxx` 别名，选择你喜欢的命名风格。

## 快速参考

### 状态管理 Hooks

| Hook | 用途 | 示例 |
|------|------|------|
| `useState` | 基础状态管理（推荐用 by 委托） | `var state by useState("")` |
| `useGetState` | 解构使用的状态管理（推荐） | `val (state, setState, getState) = useGetState(0)` |
| `useBoolean` | 布尔状态管理 | `val (state, toggle, setValue, setTrue, setFalse) = useBoolean(false)` |
| `useReducer` | Redux 风格状态管理 | `val (state, dispatch) = useReducer(reducer, initialState)` |
| `useRef` | 不触发重组的引用 | `val ref = useRef(0)` |
| `useList` | 列表状态管理 | `val list = useList(1, 2, 3)` |
| `useMap` | Map 状态管理 | `val map = useMap("key" to "value")` |

### 副作用 Hooks

| Hook | 用途 | 示例 |
|------|------|------|
| `useEffect` | 副作用处理 | `useEffect(dep) { /* effect */ }` |
| `useMount` | 组件挂载时执行 | `useMount { loadData() }` |
| `useUnmount` | 组件卸载时执行 | `useUnmount { cleanup() }` |
| `useUpdateEffect` | 跳过首次执行的 Effect | `useUpdateEffect(dep) { /* effect */ }` |

### 网络请求

| Hook | 用途 | 示例 |
|------|------|------|
| `useRequest` | 网络请求管理 | `val (data, loading, error, request) = useRequest(requestFn)` |

### 工具 Hooks

| Hook | 用途 | 示例 |
|------|------|------|
| `useDebounce` | 防抖值 | `val debouncedValue = useDebounce(value)` |
| `useThrottle` | 节流值 | `val throttledValue = useThrottle(value)` |
| `useInterval` | 定时器 | `useInterval { tick() }` |
| `useTimeoutFn` | 延时执行 | `useTimeoutFn(fn, 1.seconds)` |
| `useUndo` | 撤销/重做 | `val (state, set, reset, undo, redo) = useUndo(initial)` |

## 详细参考

- **状态管理 Hooks**: 见 [references/state-hooks.md](references/state-hooks.md)
- **副作用 Hooks**: 见 [references/effect-hooks.md](references/effect-hooks.md)
- **工具 Hooks**: 见 [references/utility-hooks.md](references/utility-hooks.md)
- **网络请求 Hooks**: 见 [references/request-hooks.md](references/request-hooks.md)
- **Table 相关 Hooks**: 见 [references/table-hooks.md](references/table-hooks.md)

## 常见模式

### 1. 受控组件

```kotlin
// 推荐：使用 useGetState 解构
val (text, setText) = useGetState("")
OutlinedTextField(
    value = text.value,
    onValueChange = setText,
    label = { Text("输入") }
)

// 或使用 by 委托
var text by useState("")
OutlinedTextField(
    value = text,
    onValueChange = { text = it },
    label = { Text("输入") }
)
```

### 2. 解决闭包问题（来自 UseStateExample.kt）

```kotlin
// 方式1: 使用 useGetState 函数式更新
val (state, setState) = useGetState("initial")
LaunchedEffect(Unit) {
    repeat(10) {
        delay(1.seconds)
        setState { "$it." }  // 函数式更新，避免闭包问题
    }
}

// 方式2: 使用 by 委托
var byState by useState("initial")
LaunchedEffect(Unit) {
    repeat(10) {
        delay(1.seconds)
        byState += "."  // 直接修改，无闭包问题
    }
}

// 方式3: 使用 useLatestRef
val (state, setState) = useState("initial")
val stateRef = useLatestRef(state)
LaunchedEffect(Unit) {
    repeat(10) {
        delay(1.seconds)
        setState("${stateRef.current}.")  // 通过 ref 获取最新值
    }
}
```

### 3. 网络请求（来自 Auto&Manual.kt）

```kotlin
// 自动请求
val (userInfoState, loadingState, errorState) = useRequest(
    requestFn = { NetApi.userInfo(it) },
    optionsOf = {
        defaultParams = "junerver"  // 自动请求必须设置默认参数
    }
)
val userInfo by userInfoState
val loading by loadingState

if (loading) {
    Text(text = "loading ...")
}
userInfo?.let { Text(text = it.toString()) }

// 手动请求
val (repoInfoState, loadingState, errorState, request) = useRequest(
    requestFn = { it: Tuple2<String, String> ->
        NetApi.repoInfo(it.first, it.second)
    },
    optionsOf = {
        manual = true
        defaultParams = tuple("junerver", "ComposeHooks")
    }
)
TButton(text = "request") { request() }
```

### 4. Redux 风格状态管理（来自 UseReducerExample.kt）

```kotlin
// 定义 State 和 Action
data class SimpleData(val name: String, val age: Int)

sealed interface SimpleAction {
    data class ChangeName(val newName: String) : SimpleAction
    data object AgeIncrease : SimpleAction
}

// 定义 Reducer
val simpleReducer: Reducer<SimpleData, SimpleAction> = { prevState, action ->
    when (action) {
        is SimpleAction.ChangeName -> prevState.copy(name = action.newName)
        is SimpleAction.AgeIncrease -> prevState.copy(age = prevState.age + 1)
    }
}

// 使用
val (state, dispatch) = useReducer(
    simpleReducer,
    initialState = SimpleData("default", 18),
    middlewares = arrayOf(logMiddleware())
)

TButton(text = "Change Name") { dispatch(SimpleAction.ChangeName("Alice")) }
TButton(text = "Increase Age") { dispatch(SimpleAction.AgeIncrease) }
Text(text = "State: ${state.value}")
```

### 5. 列表操作（来自 UseListExample.kt）

```kotlin
val listState = useList(1, 2, 3)

// 操作方法
listState.add(4)              // 添加
listState.add(0, 0)           // 插入
listState.removeAt(0)         // 删除
listState.removeLast()        // 删除最后一个
listState[0] = 10             // 修改
listState.clear()             // 清空
listState.shuffle()           // 打乱

// 配合 useListReduce
val sum by useListReduce(listState) { a, b -> a + b }
```

### 6. 防抖输入（来自 UseDebounceExample.kt）

```kotlin
var inputValue by useState("")
val debouncedValue by useDebounce(
    value = inputValue,
    optionsOf = {
        wait = 500.milliseconds
    }
)

OutlinedTextField(
    value = inputValue,
    onValueChange = { inputValue = it },
    label = { Text("Type something...") }
)

Text(text = "Debounced: $debouncedValue")
```
