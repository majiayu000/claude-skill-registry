---
name: zinc-ui-async-separation
description: War3Lib UI 组件开发行为规范（Zinc in .j）：约束 UI 本地异步行为与同步数据逻辑分离；规范 onClick/onEnter/onLeave 与 spClick/spEnter/spLeave 的使用边界；规范本地事件转同步事件时的数据打包与触发器接收。用于创建或重构 Jass/ui/composite 下的 UI（如 HeroSelector/Selector/Museum）及相关回调。
---

# War3 UI 异步分层规范

## 强制规则

- 保持 `UI 展示层` 与 `数据/游戏状态层` 分离。
- 把 `GetLocalPlayer()` 分支内的逻辑视为异步本地逻辑；禁止在其中修改同步状态（单位、计时器、全局对局数据等）。
- `show/hide/refresh` 等 UI 生命周期方法禁止做业务数据写入；尤其禁止在 UI 操作链路内执行 `DzAPI_Map_Store*`和其他会导致数据变动的操作。
- 在 UI 回调里只做三类事情：
1. 本地 UI 更新（show/hide/text/texture/位置）
2. 事件参数写入（`currentPosAsync` / `args*` / `eventdata.bind*`）
3. 触发异步到同步桥接（如 `syncBus.DzSyncDataEx`）

## 事件绑定选择

- 无数据绑定的事件用 `onClick/onEnter/onLeave`。
- 需要携带绑定数据（frame -> eventdata -> 业务参数）时用 `spClick/spEnter/spLeave`。
- 使用 `sp*` 时，先绑定 `uiHashTable(frame).eventdata`，再在回调中解包；禁止直接依赖外层局部变量闭包。

## 异步转同步（本地事件出网）

- 本地点击/交互不直接执行业务数据修改；先编码 payload 并发送（示例：`syncBus.DzSyncDataEx(channel, payload)`）。
- 在 `onDataSync(channel, ...)` 中解码并做权限校验（owner/player/对象存在性），通过后才触发 `trClick/trClose/trBtn1` 等同步逻辑。
- payload 至少包含三段信息：
1. 事件类型（如 `D/C/F/L/R`）
2. 对象标识（如 `sd`、英雄索引）
3. 位置信息（如 `pos`）

## 回调参数传递

- 为匿名回调准备静态参数槽（如 `currentSDAsync/currentPosAsync/argsHeroIndex`）。
- 触发器前写入参数，触发后按需清理或覆盖，避免跨回调污染。
- 提供统一读取函数（`Get*Async` / `Get*Pos`）给外部逻辑层。

## 生命周期与清理

- 销毁 UI 时，补发必要的离开事件（若存在“进入未离开”状态）。
- 销毁顺序保持“子组件 -> 主组件”，并把句柄置零。
- 本地 UI 关闭仅处理本地资源；同步状态变更交给同步事件处理器。

## 硬性检查清单（CR Gate）

在提交 UI 代码前，逐条检查。任意 `FAIL` 均禁止合并。

1. `GetLocalPlayer()` 分支内不修改同步状态
PASS: 仅做 UI 显示、本地参数写入、发送同步消息。
FAIL: 创建/销毁单位、改全局业务数据、改计时器/组等对局同步状态。

2. 本地 UI 回调不直改业务数据
PASS: `onClick/spClick` 只编码 payload 或写 `current*Async/args*`。
FAIL: 在 UI 点击回调里直接执行奖励发放、状态切换、背包改动等。

3. 正确选择 `on*` vs `sp*`
PASS: 无绑定数据用 `onClick/onEnter/onLeave`；有 frame 数据解包需求用 `spClick/spEnter/spLeave`。
FAIL: 需要 `eventdata` 却使用 `on*`，或无数据需求滥用 `sp*`。

4. `sp*` 回调前完成 eventdata 绑定
PASS: 对应按钮存在 `uiHashTable(btn.ui).eventdata.bind*`。
FAIL: 回调中读取 `eventdata` 但未绑定或绑定不完整（缺少 bind2/bind3）。

5. 本地事件统一走“发送 -> 接收 -> 处理”链路
PASS: `DzSyncDataEx(channel, payload)` 发出后，在 `onDataSync(channel, ...)` 解码并处理。
FAIL: 本地事件绕过总线直接触发同步业务逻辑。

6. `onDataSync` 完成安全校验
PASS: 校验对象存在性、`owner/player` 一致性、索引范围合法性后再触发业务触发器。
FAIL: 未校验即执行 `trClick/trClose/...`。

7. payload 结构可逆且稳定
PASS: payload 至少含 `事件类型 + 对象标识 + 位置信息`，解码规则与编码规则一一对应。
FAIL: 拼接格式歧义、长度位错误、解码位置错位。

8. 异步参数槽完整可读
PASS: 提供 `Get*Async/Get*Pos` 读取接口，并在触发前写入对应参数。
FAIL: 回调依赖外层局部变量或隐式状态，导致异步读取不稳定。

9. UI 销毁流程完整
PASS: 销毁前补发必要 leave，按子到父销毁并置零，避免悬空句柄。
FAIL: 直接销毁主框导致子组件泄漏，或 leave 状态丢失。

10. 外部回调职责清晰
PASS: UI 层只发事件与展示；数据层在外部触发器/总线接收端处理。
FAIL: UI 文件内混入业务数据写入分支。

## 快速判定

- 全部 10 项 `PASS`：允许合并。
- 任意 1 项 `FAIL`：先修复再提审。
- 若无法判定：默认按 `FAIL` 处理并补充注释说明边界。

## 参考实现（按需阅读）

- `references/war3lib-ui-examples.md`
