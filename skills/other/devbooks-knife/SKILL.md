---
name: devbooks-knife
description: devbooks-knife：把 Epic 级需求切成可拓扑排序的 Slice 队列，并落盘机读 Knife Plan（用于高风险/史诗级变更的 G3 强制闸门）。
recommended_experts: ["System Architect", "Product Manager"]
allowed-tools:
  - Glob
  - Grep
  - Read
  - Write
  - Edit
  - Bash
---

# DevBooks：Knife（Epic 切片与 Knife Plan）

## 目标

把“大需求（Epic）”切成可并行、可收敛、可验收的 **Slice 队列**，并把切片计划落盘为 **Knife Plan（机读合同）**，作为后续 DevBooks 变更包的上游约束与验证锚点集合。

## 何时必须使用（MUST）

当满足任一条件时，本 skill 必须执行并落盘 Knife Plan：

- `risk_level=high`
- `request_kind=epic`

原因：严格闸门将把 Knife Plan 作为 **G3 强制项** 校验（缺失/路径错/字段不对齐会阻断）。

## 输入

最小输入（建议从 Bootstrap/Proposal 汇总）：

- `epic_id`（稳定且全局唯一）
- Epic 级 AC 清单（或可枚举的验收标准集合）
- 风险等级 `risk_level`
- `request_kind`（应为 `epic`）
- 依赖与假设（允许不完整，但必须显式）

## 输出（必须落盘）

### 1) Knife Plan（机读，MUST）

落点（MUST）：

- `dev-playbooks/specs/_meta/epics/<epic_id>/knife-plan.yaml`（或 `knife-plan.json`）

一致性（MUST）：

- `knife-plan.(yaml|json)` 内的 `epic_id` 必须等于目录名 `<epic_id>`
- 若变更包声明了 `slice_id`，则 Knife Plan 的 `slice_id` 必须与之对齐

### 2) Slice 队列（建议）

以 `slices[]` 表达 Slice DAG（依赖拓扑），每个 Slice 至少包含：

- `slice_id`
- `change_id`（建议预分配变更包目录名）
- `ac_subset[]`（MECE 子集）
- `verification_anchors[]`（确定性验证锚点：命令/测试/证据路径）
- `rollback_strategy`（摘要或指向详细说明）

## 执行步骤（提示词层）

1. 先做配置发现（优先 `.devbooks/config.yaml`），读取 `agents_doc` 与 `constitution.md`。
2. 确认 `epic_id` / 风险等级 / `request_kind=epic`（缺失则在 Delivery/Void 先补齐）。
3. 产出 Slice DAG：保证每个 Slice 都能以单一变更包闭环（≤12 tasks）。
4. 落盘 Knife Plan 到规定路径，并在内容中显式绑定 `epic_id` / `slice_id`。
5. 输出下一步路由建议：进入 `devbooks-delivery-workflow`（或先进入 Proposal/Design/Spec/Plan），并给出升级条件。

## 并行执行调度

当 Knife Plan 包含多个 Slice 时，可以使用 `knife-parallel-schedule.sh` 生成并行执行清单：

```bash
# 生成 Markdown 格式的并行调度清单
knife-parallel-schedule.sh <epic-id> --format md --out parallel-schedule.md

# 生成 JSON 格式（供程序消费）
knife-parallel-schedule.sh <epic-id> --format json --out parallel-schedule.json
```

### 输出内容

1. **最大并行度**：可同时启动的最大 Agent 数量
2. **分层执行清单**：
   - Layer 0：无依赖，可立即启动
   - Layer 1：依赖 Layer 0 完成
   - Layer N：依赖 Layer N-1 完成
3. **关键路径**：串行依赖深度
4. **启动命令模板**：每个 Slice 的 Agent 启动命令
5. **溯源信息**：Epic ID、Plan ID、Plan Revision

### 使用场景

由于当前 AI 编程工具不支持二级子代理调用，Epic 拆分后需要人类协调多个独立 Agent 并行完成：

1. 运行 `knife-parallel-schedule.sh` 生成清单
2. 根据清单的 Layer 0 启动多个独立 Agent
3. 等待 Layer 0 全部完成后，启动 Layer 1
4. 重复直到所有 Layer 完成
5. 运行 `requirements-ledger-derive.sh` 更新账本

## 参考

- `dev-playbooks/specs/knife/spec.md`（Knife 的规范与闸门接线要求）
- `dev-playbooks/specs/_meta/epics/README.md`（Epic 工件目录约束）
- `skills/devbooks-delivery-workflow/scripts/knife-parallel-schedule.sh`（并行调度脚本）
