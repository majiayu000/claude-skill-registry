# GH239 产品规格：跨仓同步仅限 main、串行且可重放

关联 issue: https://github.com/majiayu000/claude-skill-registry-core/issues/239
状态: `Approved for implementation by implx auth_mode:auto`
语言: `zh-CN`

## 问题

`sync-data` 同时写入 core、data，并把固定的 `core_sha` + `data_sha`
分发给 main。当前手动运行可从非 `main` ref 进入流程；配置校验、跨仓 push
和 publish dispatch 之间也没有完整的 fail-closed 与重放边界。结果可能是 data/core
已经提交，但 main 未发布，或者运行在两次跨仓写入之间被取消。

维护者需要看到一个明确结果：一次运行要么在任何写路径前被拒绝，要么形成一个可审计、
可重放的固定 tuple；dispatch 失败不能被报告成成功，也不能通过 rerun 再生成另一组 tuple。

## 目标

1. 只允许 `main` ref 进入任何 checkout、discovery、commit、push 或 dispatch 路径。
2. 在 discovery 与任一 push 前，fail closed 校验 data/main 目标和 credentials。
3. 串行执行跨仓写路径，新的运行不得取消正在运行的写事务。
4. 在 main dispatch 前固化完整 tuple 与不含 secret 的精确 replay payload。
5. dispatch 失败时保留可复现证据并使 workflow 失败；同一 run 的 rerun 只重放同一 tuple。
6. 用 deterministic workflow contract tests 固化顺序、失败语义和重放边界。

## 非目标

- 不提供跨 Git 仓库的原子事务或自动回滚已推送 commit。
- 不承诺 `repository_dispatch` exactly-once；幂等性指重试使用相同 target 与 payload，
  且不再写 core/data。
- 不修改 data/main 仓库的 skill 内容、生成物或 main-owned workflow。
- 不改变 discovery、download、security、metadata 或 size gate 的业务判定。
- 不为非 `main` 增加 dry-run 例外。
- 不自动恢复尚未形成有效 handoff 的旧 run；该情况必须 fail closed，维护者核对远端状态后
  发起新的 `main` `workflow_dispatch`。

## 可观察行为不变量

1. `GH239-INV-01`：任一 `github.ref != refs/heads/main` 的运行必须失败；失败发生在第一个
   repository checkout 之前，且该 run 不执行 discovery、commit、push 或 dispatch。
2. `GH239-INV-02`：`REGISTRY_DATA_REPO`、`DATA_REPO_TOKEN`、
   `REGISTRY_MAIN_REPO`、`MAIN_REPO_TOKEN` 任一缺失、格式错误、目标不可访问、目标默认分支
   不是 `main`，或对应 credential 不具备 write 能力时，workflow 必须在 discovery 与任一
   push 前失败；日志不得输出 credential 值。
3. `GH239-INV-03`：core/data 的 checkout、rebase 与 push 都显式指向 `main`；不得依赖触发
   ref、当前 tracking branch 或目标仓默认值来决定写入分支。
4. `GH239-INV-04`：同一 `sync-data-pipeline` concurrency group 中，运行中的 workflow
   不会被后来的 run 取消；后来的 run 只能等待写路径空闲。此契约不声明 FIFO 顺序。
5. `GH239-INV-05`：data 与 core push 都成功（或确认无变更）后、main dispatch 前，workflow
   必须固化完整 `core_sha`、`data_sha`、`core_repo`、`data_repo`、`target_repo`、
   `event_type` 与精确 request payload；两个 SHA 必须是实际将被发布的完整 commit SHA。
6. `GH239-INV-06`：main dispatch 返回非成功状态时，workflow 必须失败，并在日志/summary
   及 retained artifact 中提供 `target_repo`、`core_sha`、`data_sha`、`payload_sha256` 与
   replay payload；证据只允许公开仓库标识、SHA、run 标识和 payload，不得包含 token、
   authorization header 或其他 secret。
7. `GH239-INV-07`：同一 `github.run_id` 的 rerun 如果已有有效 handoff，必须复用完全相同的
   target、tuple、payload bytes 与 `payload_sha256`，并跳过 checkout、discovery、commit 和
   core/data push；dispatch 可安全重复提交。
8. `GH239-INV-08`：`github.run_attempt > 1` 时，缺失、过期、字段不匹配、hash 不匹配或
   repo/SHA 非法的 handoff 必须在任何新写路径前 fail closed；不得猜测当前 branch head
   作为替代 tuple。
9. `GH239-INV-09`：首次成功运行仍保持 canonical flow：data push → core push → 固化 tuple
   → main `publish_from_core` dispatch → core `build-index` dispatch。main dispatch 失败时
   不得继续 dispatch `build-index`。
10. `GH239-INV-10`：contract tests 必须分别证明 main-only 顺序、早期配置失败、显式
    `main` 写入、`cancel-in-progress: false`、handoff 先于 dispatch、dispatch failure、
    rerun 跳过写路径，以及 secret-free evidence；仅检查一个关键词存在不算完整证明。

## 验收场景

| 场景 | 预期结果 | 覆盖 |
| --- | --- | --- |
| 从 feature branch 手动运行 | checkout 前失败，无外部 mutation | `GH239-INV-01` |
| data/main 配置或权限无效 | discovery 前失败，不降级为 warning/skip | `GH239-INV-02` |
| 两个 run 重叠 | 已运行者继续，后来的 run 等待 | `GH239-INV-04` |
| 两次 push 后 main dispatch 返回 4xx/5xx | run 失败，安全证据可下载并可复制 payload | `GH239-INV-05`, `GH239-INV-06` |
| 对该失败 run 执行 rerun | 不再写 core/data，只发送原 payload | `GH239-INV-07` |
| rerun 的 handoff 缺失或被修改 | 写路径前失败，不生成新 tuple | `GH239-INV-08` |

## 完成条件

本次 `implx auth_mode:auto` invocation 已授权按本规格实施，无需额外等待 spec approval。
全部 `GH239-INV-01` 至 `GH239-INV-10` 仍须有实现证据与通过的 deterministic checks；
合并仍须具备独立 PR review、当前 CI/review threads/merge state/PR gate 证据。受控 live
workflow dispatch 是独立的 maintainer gate，不属于本次实施授权。
