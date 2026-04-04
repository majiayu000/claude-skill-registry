---
name: entry-point-check
description: 验证 VS 的 entry_points 字段是否与 SPEC_PRJ_ENTRYPOINTS（入口类型标签）一致，生成缺失入口清单和补充建议。当准备 CONSTRAINT 验收前使用。
stage: DESIGN
level_supported: [L2, L3]
---

## entry-point-check: 入口设计检查

### 描述
验证 VS 的 `entry_points` 字段是否与 `SPEC_PRJ_ENTRYPOINTS`（`WEB_APP`/`API`/`JOB`/`CLI`/`LIB`/`MIXED`/`TBD`）一致，生成缺失入口清单和补充建议。

### 适用场景
- **WORKFLOW_STEP_4 Task S4-2 Round 2**：生成 VS 后
- **WEB_APP/API/JOB/CLI/LIB/MIXED 项目**：忘记设计 entry_points
- **WORKFLOW_STEP_4 Task S4-5 前**：准备 CONSTRAINT 验收前

### 输入
- design/ 目录（所有 VS）
- 入口类型标签（从 `spec/spec_variables.md` 读取 `SPEC_PRJ_ENTRYPOINTS`）

### 输出
- Entry Point 检查报告（markdown）
- 缺失入口清单（哪些 VS 缺少 entry_points）
- 补充建议（建议添加哪些入口）

### 执行策略
1. 读取 `spec/spec_variables.md`，获取 `SPEC_PRJ_ENTRYPOINTS`
2. 扫描所有 VS，检查 `entry_points` 字段是否存在且结构化（至少包含 `name` 与 `type`）
   - **格式约束**: 使用业务语言（如 "Dashboard entry"），不写 URL/路由/HTTP 端点字符串
3. 基于 `SPEC_PRJ_ENTRYPOINTS` 做最小一致性检查（不做实现细节推断）：
   - `WEB_APP`: 至少包含 1 个 `type: UI` 的入口
   - `API`: 至少包含 1 个 `type: API` 的入口
   - `JOB`: 至少包含 1 个 `type: JOB` 的入口（`trigger` 建议写调度触发方式）
   - `CLI`: 至少包含 1 个 `type: CLI` 的入口
   - `LIB`: 至少包含 1 个 `type: LIB` 的入口（按“集成点/使用方式”描述）
   - `MIXED`: 同时满足实际存在的入口组合（例如 UI + API）
   - `TBD`: 标记为待确认并提示 HITL 澄清
4. 识别缺失入口或类型不匹配的 VS，并给出补充建议（基于 VS 的 `value_path` 推断入口语义）

### 价值
- **SPEC 组织**：提前发现入口设计缺失，避免 CONSTRAINT 验收失败
- **PM/BA**：确保设计完整
- **Dev**：明确系统入口
