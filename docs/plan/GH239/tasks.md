# GH239 任务计划

关联 issue: https://github.com/majiayu000/claude-skill-registry-core/issues/239
产品规格: `docs/plan/GH239/product.md`
技术规格: `docs/plan/GH239/tech.md`
状态: `Approved for implementation by implx auth_mode:auto`

## 执行边界

- 单一顺序 lane：`implementation_lane`。任务共享 workflow/test 文件，不并行写入。
- 本次 `implx auth_mode:auto` invocation 本身授权执行 `SP239-T1` 至 `SP239-T3`，无需再次请求
  spec implementation approval。
- 只允许实现阶段修改 `.github/workflows/sync-data.yml` 与
  `tests/test_pipeline_contracts.py`。
- 当前 spec-writer lane 仍不修改实现文件，也不执行 live workflow dispatch。后续 implx
  implementation lane 可在当前授权内实施并形成 PR；合并必须等待独立 review 与完整、当前的
  CI/review threads/merge state/PR gate evidence。真实 GitHub run 只由 maintainer 受控触发。

## `SP239-T1`：建立 main authority、早期配置与串行边界

- Owner（负责人）: `implementation_lane`
- Dependencies（依赖）: none
- Covers（覆盖）: `GH239-INV-01`, `GH239-INV-02`, `GH239-INV-03`, `GH239-INV-04`
- Files（文件）: `.github/workflows/sync-data.yml`, `tests/test_pipeline_contracts.py`
- 工作内容:
  1. 添加无 checkout 的 `preflight` first step 与 fail-closed data/main access checks。
  2. 将 concurrency 改为 `cancel-in-progress: false`。
  3. 让 core/data checkout、rebase、push 显式使用 `main`。
  4. 添加覆盖顺序、失败语义和显式 branch target 的 contract tests。
- Done when（完成标准）:
  - non-main/config/permission 失败路径都位于 checkout/discovery/push 前；无 warning-and-skip。
  - active run 不可取消，所有写入目标显式为 `main`。
  - 对应 contract tests 通过，既有 pipeline order tests 不回归。
- Verify（验证）:

```bash
python -m pytest -q tests/test_pipeline_contracts.py -k 'sync_data'
git diff --check
```

## `SP239-T2`：固化 tuple、拆分 publish 并实现 rerun replay

- Owner（负责人）: `implementation_lane`
- Dependencies（依赖）: `SP239-T1`
- Covers（覆盖）: `GH239-INV-05`, `GH239-INV-06`, `GH239-INV-07`, `GH239-INV-08`, `GH239-INV-09`
- Files（文件）: `.github/workflows/sync-data.yml`, `tests/test_pipeline_contracts.py`
- 工作内容:
  1. 将 mutation 与 dispatch 拆为 `sync`/`publish` jobs，并设置严格 `needs`/attempt 条件。
  2. 在两次 push 后生成、校验并上传 `sync-publish-handoff` 的两个 JSON 文件。
  3. 让 `publish` 只从 artifact 读取并原样发送 payload，失败时输出 secret-free replay evidence。
  4. 覆盖 rerun failed jobs、rerun all jobs、坏/缺失 handoff 与 build-index 顺序。
- Done when（完成标准）:
  - 首次 run 在 dispatch 前有完整、hash 可验证、无 secret 的 handoff。
  - 任一 rerun 不进入 core/data mutation；有效 handoff 重放相同 bytes，无效 handoff fail closed。
  - main dispatch 非 2xx 使 workflow 失败且 `build-index` 不运行。
- Verify（验证）:

```bash
python -m pytest -q tests/test_pipeline_contracts.py -k 'sync_data'
git diff --check
```

## `SP239-T3`：全量验证与 human handoff

- Owner（负责人）: `implementation_lane`
- Dependencies（依赖）: `SP239-T1`, `SP239-T2`
- Covers（覆盖）: `GH239-INV-01` through `GH239-INV-10`
- Files（文件）: 无计划中的 production edit，仅生成 evidence/handoff
- 工作内容:
  1. 运行 focused 与 full test suite，确认现有 download/security/size gates 顺序未变。
  2. 审查 diff 仅包含两个授权实现文件，且无 token、测试弱化或 main/data 直接修改。
  3. 在 PR 中附 invariant → test evidence；合并后将受控失败 dispatch/live rerun 明确交给
     maintainer 执行。
- Done when（完成标准）:
  - 所有 deterministic checks fresh pass；每个 invariant 有 test 名称或明确 live human gate。
  - 合并前具备独立 reviewer lane 与当前 CI、review threads、merge state、PR gate evidence。
  - live workflow dispatch 未由 implementation agent 执行；maintainer 可在受控运行中从
    artifact 复制 payload，并确认 rerun 不产生新的 core/data SHA。
- Verify（验证）:

```bash
python -m pytest -q tests/test_pipeline_contracts.py
python -m pytest -q
git diff --check
git status --short
```

## 追踪矩阵

| 不变量 | Primary task | Final gate |
| --- | --- | --- |
| `GH239-INV-01` - `GH239-INV-04` | `SP239-T1` | `SP239-T3` |
| `GH239-INV-05` - `GH239-INV-09` | `SP239-T2` | `SP239-T3` |
| `GH239-INV-10` | `SP239-T3` | maintainer review |

## Human gates（人工门禁）

1. 实施授权：已由本次 `implx auth_mode:auto` invocation 满足，不再等待额外 spec approval。
2. 合并前：必须有独立 reviewer lane，并核对 contract tests、workflow job conditions、当前
   CI、review threads、merge state 与 PR gate evidence；不得以自审替代。
3. 上线验证：maintainer 在 `main` 受控触发，并核对失败 evidence、rerun tuple 与下游
   publish；`implx auth_mode:auto` 不授权 implementation agent 执行该 live dispatch。
