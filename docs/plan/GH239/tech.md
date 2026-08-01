# GH239 技术规格：sync-data authority 与 replay handoff

关联 issue: https://github.com/majiayu000/claude-skill-registry-core/issues/239
产品规格: `docs/plan/GH239/product.md`
基线: `8710eaddb2159130c6f4ccfa9792387d56f3482e`
状态: `Approved for implementation by implx auth_mode:auto`

## 约束与既有契约

- `AGENTS.md` 与 `CLAUDE.md` 指定 core 是 publish orchestration authority；main 由固定的
  `core_sha` + `data_sha` 重建，不能在 main 直接修补生成物。
- `docs/plan/sync-download-failure-gate.md` 的 download fail-closed 与 failure artifact
  必须保留。
- `docs/plan/malware-supply-chain-remediation-spec.md` 的 security fail-closed 顺序不得弱化。
- `docs/plan/registry-sharding-spec.md` 要求 size guard 位于 registry rebuild 后、data/core
  commit 前；本改动不得移动该边界。
- `docs/plan/release-readiness-reporting.md` 仍是 report-only，不得借本 issue 变成 publish gate。

## 当前根因（基线精确证据）

1. `.github/workflows/sync-data.yml:33-36` 的第一个 repository step 是 `Checkout core`；
   workflow 没有 branch guard。`workflow_dispatch` 可选择非 `main` ref，因此 data checkout
   仍可指向 data 默认分支，而 core checkout/push 使用触发分支，形成跨分支 tuple。
2. `.github/workflows/sync-data.yml:38-50` 只在 core checkout 后检查 data 变量/secret 是否
   非空；没有校验 repo 格式、默认分支、访问性或 write permission。无效 push credential
   可能直到长时间 discovery/build 后才暴露。
3. `.github/workflows/sync-data.yml:25-27` 使用固定 concurrency group，但
   `cancel-in-progress: true`。后来的 run 可在 data push 与 core push/dispatch 之间取消当前 run。
4. `.github/workflows/sync-data.yml:487-548` 先执行 data/core push，且两个 `git push` 都依赖
   当前 tracking branch；没有显式 `origin HEAD:main` authority boundary。
5. `.github/workflows/sync-data.yml:556-572` 在两个 push 后才校验 main 配置；缺失配置仅输出
   warning、写 `ready=false` 并 `exit 0`，所以已提交但未 publish 的 workflow 仍可成功。
6. `.github/workflows/sync-data.yml:574-593` 的 `curl --fail-with-body` 已能让 HTTP 非成功响应
   失败；真正缺口是 payload 只存在于瞬时 shell variable，失败前没有持久化 target/tuple/
   request，也没有独立 replay 路径。
7. 所有 mutation 与 dispatch 位于同一个 `sync` job。GitHub rerun 会沿用原事件的
   `GITHUB_SHA`/`GITHUB_REF`，重跑该 job 会再次进入 discovery 与两次 push，不能保证复用
   已提交 tuple。行为依据：
   https://docs.github.com/en/actions/how-tos/manage-workflow-runs/re-run-workflows-and-jobs
8. `tests/test_pipeline_contracts.py:225-273` 只覆盖 rebuild/guard 顺序、staging、cleanup 与
   discovery output；没有 branch、credential、concurrency、dispatch evidence 或 rerun contract。

## 技术决策

### 1. Workflow 级 authority 与串行化

- 保留 `concurrency.group: sync-data-pipeline`，将 `cancel-in-progress` 固定为 `false`。
- 将 workflow 拆为顺序 jobs：`preflight`、`sync`、`publish`。只有 `sync` 可 checkout 或写仓库。
- `preflight` 的第一个用户 step 不 checkout；它断言 `github.ref == refs/heads/main`。
  失败时后续 jobs 因 `needs` 不运行。
- `sync` 仅在 `github.run_attempt == 1` 且没有 replay handoff 时运行。任何 rerun 都不得重新
  进入 mutation job；无有效 handoff 的 rerun 由 `preflight`/`publish` 失败。

### 2. 早期 fail-closed 配置校验

`preflight` 在 checkout/discovery 前完成以下只读校验：

1. 四个配置值均非空；repo 值匹配 GitHub `owner/name` 形状，core/data/main 三个 target 互异。
2. 用 `DATA_REPO_TOKEN` 对 `REGISTRY_DATA_REPO` 执行非 mutation repository GET；要求响应成功、
   `default_branch == "main"` 且 authenticated `permissions.push == true`。
3. 用 `MAIN_REPO_TOKEN` 对 `REGISTRY_MAIN_REPO` 做同样检查；不发送“探测 dispatch”。
4. 任一网络、JSON、字段或权限校验失败均 `exit 1`；response 与日志不得包含 token。

presence-only 的 `Validate data repo config` 与 late `Validate main publish config` 被统一替代；
不再保留 `ready=false`、warning 后跳过 publish 的路径。

### 3. 显式 main 写入

- core/data `actions/checkout` 都指定 `ref: main` 与 `fetch-depth: 0`。
- 冲突重试继续 `fetch origin main` / `rebase origin/main`，push 改为
  `git push origin HEAD:main`。
- 无 staged change 时仍读取当前 `main` HEAD；有 rebase 时只在 push 成功后捕获最终 SHA。
- 现有 discovery、download、security、metadata、rebuild 与 size guard 的相对顺序不变。

### 4. Secret-free handoff contract

`sync` 在 data/core push 完成后、`publish` 启动前生成并上传阻塞式 artifact
`sync-publish-handoff`，保留 30 天，包含两个文件：

`publish-dispatch-payload.json` 是将原样发送到 GitHub API 的 request body：

```json
{
  "event_type": "publish_from_core",
  "client_payload": {
    "core_repo": "owner/claude-skill-registry-core",
    "core_sha": "40-hex",
    "data_repo": "owner/claude-skill-registry-data",
    "data_sha": "40-hex"
  }
}
```

`publish-dispatch-evidence.json` 使用固定 schema：

```json
{
  "schema_version": 1,
  "run_id": "github.run_id",
  "run_attempt": 1,
  "target_repo": "owner/claude-skill-registry",
  "core_repo": "owner/claude-skill-registry-core",
  "core_sha": "40-hex",
  "data_repo": "owner/claude-skill-registry-data",
  "data_sha": "40-hex",
  "event_type": "publish_from_core",
  "payload_sha256": "64-hex"
}
```

生成器只接收 repo、SHA 和 GitHub run metadata，不接收任何 token。payload 使用稳定 JSON
编码并以实际文件 bytes 计算 SHA-256。artifact 上传失败必须阻止 `publish`。

### 5. Replay state machine

| 状态 | `sync` | `publish` |
| --- | --- | --- |
| 首次 attempt，无 handoff | 运行完整 pipeline，上传 handoff | 下载、校验并 dispatch |
| dispatch/build-index 失败后 rerun failed jobs | 不重新运行已成功的 `sync` | 下载同一 run artifact，重放 |
| rerun all jobs，有有效 handoff | 由 `preflight` 恢复，`sync` skipped | 重放同一 bytes |
| 任一 rerun，无/坏/过期 handoff | 禁止 mutation，fail closed | 不猜测 tuple |

恢复使用同一 `github.run_id` 范围内的 `actions/download-artifact`；artifact 名固定，因此不会
跨 run 选错。校验必须在 dispatch 前验证：exact key allowlist、`schema_version`、`run_id`、
repo 与当前配置一致、两个完整 40-hex SHA、payload/evidence 字段一致，以及
`payload_sha256` 匹配。多余 key 也失败，以结构 allowlist 保证不存在 secret 字段。

### 6. Dispatch 失败语义

- `publish` 总是从已校验文件发送 payload，不在 shell 中重新拼 tuple。
- 调用保留 `curl --fail-with-body`；非 2xx 明确输出安全的 `target_repo`、两个 SHA、hash 与
  payload，写入 `GITHUB_STEP_SUMMARY` 后 `exit 1`。
- main dispatch 成功后才 dispatch core `build-index`。若后者失败，rerun 仍重发同一 main
  payload，再重试 build-index；上游 core/data 不变。
- 幂等键定义为 `(target_repo, event_type, core_sha, data_sha, payload_sha256)`；本 issue
  不要求下游 exactly-once 去重。

## 影响文件

| 文件 | 计划变更 |
| --- | --- |
| `.github/workflows/sync-data.yml` | jobs/authority/config/concurrency、显式 main push、handoff 与 replay |
| `tests/test_pipeline_contracts.py` | 新增顺序、fail-closed、evidence 与 rerun contract tests |

不修改 data/main repo，不新增 runtime script 或持久化 schema。

## 不变量到实现/验证映射

| 产品不变量 | 实现区域 | Deterministic evidence |
| --- | --- | --- |
| `GH239-INV-01` | `preflight` first step | branch guard index 早于任何 checkout；non-main 失败语义断言 |
| `GH239-INV-02` | early config/access checks | 四值、repo shape、default branch、push permission 与顺序断言 |
| `GH239-INV-03` | `sync` checkout/rebase/push | `ref: main` 与 `origin HEAD:main` contract test |
| `GH239-INV-04` | workflow concurrency | group 保持且仅存在 `cancel-in-progress: false` |
| `GH239-INV-05` | handoff generation/upload | 两次 push < capture/upload < publish 的位置断言与 schema 断言 |
| `GH239-INV-06` | artifact/summary/error branch | non-2xx exit、safe fields、secret key absence断言 |
| `GH239-INV-07` | job `needs` 与 rerun restore | attempt > 1 跳过 `sync`，payload 文件原样发送 |
| `GH239-INV-08` | handoff validator | missing/invalid/hash mismatch 均在 checkout/push 前失败 |
| `GH239-INV-09` | `sync`/`publish` dependency | data → core → handoff → main → build-index 顺序断言 |
| `GH239-INV-10` | `tests/test_pipeline_contracts.py` | focused 与 full pytest 通过 |

## 风险与缓解

- GitHub concurrency 不保证无限 pending/FIFO；规格只依赖“不取消 active run”和单一 mutation
  lane，不声明队列顺序。
- GitHub API 或 permission metadata 暂时不可用会阻止 sync；这是预期 fail-closed，避免在
  credential 未证明可写时开始长流程。
- artifact 最长 30 天且可能被人工删除；rerun 窗口内缺失时阻止 mutation，维护者需核对
  remote heads 后发起新的首次 run。
- job 拆分条件写错可能跳过 publish；contract tests 必须同时验证 normal、skipped sync 与
  failure dependency 条件。
- duplicate dispatch 可产生下游重复 run，但必须绑定同一 tuple；不得以生成新 tuple规避。

## 回滚

1. 在尚未产生跨仓 commit 时，可 revert workflow/test commit，恢复上一版 workflow。
2. 若新 workflow 已形成 handoff 但 dispatch 未成功，先用 artifact 中的原 payload 完成或
   明确放弃该 tuple；不得通过回滚到旧 workflow 后 rerun 来生成替代 tuple。
3. 回滚不涉及 data/main 数据迁移；已推送 commit 保持可审计，不 force push。
4. 若仅 early permission probe 误判，仍保持 main-only 与 `cancel-in-progress: false`，在单独
   follow-up 中修正 probe，不恢复 warning-and-skip 行为。

## Deterministic checks

```bash
python -m pytest -q tests/test_pipeline_contracts.py
python -m pytest -q
git diff --check
```

本次 `implx auth_mode:auto` invocation 已授权实施本技术规格；合并仍须满足独立 reviewer
lane 与当前 CI、review threads、merge state、PR gate evidence。真实失败 run 的
artifact/summary 检查属于合并后的受控 live workflow dispatch human gate，用于确认 payload
可重放且 artifact 内不存在 secret；本次授权不包含 live dispatch，该检查也不替代
deterministic tests。
