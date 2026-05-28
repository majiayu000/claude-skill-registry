---
name: superpowers-factory-bridge
version: "1.0"
status: active
layer: skill
owner: wade
last_reviewed: 2026-01-13
baseline: AI_CODE_FACTORY_DEV_GUIDE_v2.4, SoT Freeze v2.6, SUPERCLAUDE_INTEGRATION_GUIDE_v2.2
description: |
  统一开发编排器：将 Superpowers 方法论框架与 AI 代码工厂深度整合，
  创建统一的开发工作流，结合 TDD 纪律、SoT 合规和自动化代码生成。
---

# Superpowers + AI 代码工厂 桥接技能

> **版本**: 1.0
> **核心价值**: 方法论 (Superpowers) + 领域知识 (AI Factory) + 分析增强 (SuperClaude)

## 1. 概述

本技能作为统一开发编排器，协调以下三个系统：

| 系统 | 职责 | 核心技能 |
|------|------|----------|
| **Superpowers** | 开发方法论 | TDD, 计划编写, 系统化调试, 子代理开发 |
| **AI Code Factory** | 领域知识 | SoT 合规, 代码生成, 规格治理 |
| **SuperClaude** | 分析增强 | 前置分析, 后置审查, 智能建议 |

## 2. 架构

```
┌─────────────────────────────────────────────────────────────────────┐
│                    统一开发编排器 (本技能)                            │
│                                                                      │
│   命令: /udev full | /udev:brainstorm | /udev:plan | /udev:tdd      │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
        ▼                       ▼                       ▼
┌───────────────┐      ┌───────────────┐      ┌───────────────┐
│  SUPERPOWERS  │      │ AI CODE FACTORY│      │  SUPERCLAUDE  │
│  (方法论)      │      │  (领域知识)    │      │   ENHANCER    │
├───────────────┤      ├───────────────┤      ├───────────────┤
│ brainstorming │      │ ai-ad-be-gen  │      │ /sc:analyze   │
│ writing-plans │      │ ai-ad-fe-gen  │      │ /sc:research  │
│ test-driven-  │      │ ai-ad-test-gen│      │ /sc:improve   │
│   development │      │ flow-orch     │      │ /sc:troublesh │
│ subagent-dev  │      │ spec-governor │      │               │
│ systematic-   │      │               │      │ Pre/Post Hook │
│   debugging   │      │               │      │               │
└───────┬───────┘      └───────┬───────┘      └───────┬───────┘
        │                      │                      │
        └──────────────────────┼──────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       SoT 合规层                                     │
├─────────────────────────────────────────────────────────────────────┤
│ MASTER.md v4.9 → DATA_SCHEMA.md v5.10 → STATE_MACHINE.md v2.9       │
│ → BUSINESS_RULES.md v5.1 → API_SOT.md → ERROR_CODES_SOT.md          │
└─────────────────────────────────────────────────────────────────────┘
```

## 3. 统一命令接口

| 命令 | 描述 | 工作流阶段 |
|------|------|-----------|
| `/udev full <task>` | 完整开发周期 | BRAINSTORM → PLAN → EXECUTE → FINISH |
| `/udev:brainstorm <idea>` | 设计+SoT上下文 | Phase 1 only |
| `/udev:plan <requirements>` | SoT感知计划 | Phase 2 only |
| `/udev:tdd <feature>` | TDD+工厂测试 | RED → GREEN → REFACTOR |
| `/udev:impl <task>` | 子代理+工厂生成 | Phase 3 only |
| `/udev:debug <issue>` | 系统化调试 | Systematic debugging |
| `/udev:finish` | 完成分支 | Phase 4 only |

## 4. 完整开发工作流

### 4.1 Phase 1: BRAINSTORM

**触发**: 用户请求新功能或设计
**技能调用**: `superpowers:brainstorming` + `/sc:research`

**执行步骤**:
1. `/sc:research` 搜索相关模式和最佳实践
2. 调用 `superpowers:brainstorming` 苏格拉底式设计
3. 检测模块关键词，自动注入 SoT 依赖
4. 输出设计文档: `docs/plans/YYYY-MM-DD-<topic>-design.md`

**SoT 依赖注入规则**:
```yaml
keywords_to_sot:
  日报|投放|CPL|投手:
    - STATE_MACHINE.md#daily_report
    - BR-RPT-*
  充值|流水|账本|资金:
    - DATA_SCHEMA.md §3.4.4
    - BR-FIN-*
    - STATE_MACHINE.md#topup
  账户|开户|授权:
    - BR-ACCT-*
    - STATE_MACHINE.md#ad_account
  项目|成员|盈亏:
    - BR-PROJ-*
    - DATA_SCHEMA.md#projects
  对账|差异|调整:
    - BR-RECON-*
    - STATE_MACHINE.md#reconciliation
```

### 4.2 Phase 2: PLAN

**触发**: 设计文档已批准
**技能调用**: `superpowers:writing-plans` + `sot-aware-planning`

**执行步骤**:
1. 调用 `superpowers:writing-plans` 创建细粒度任务
2. 每个任务自动注入 SoT 引用
3. 生成 `/gen` 命令提示
4. 输出计划文档: `docs/plans/YYYY-MM-DD-<topic>.md`

**任务模板**:
```markdown
### Task N: [组件名称]

**SoT 依赖**:
- STATE_MACHINE.md#<entity>: [相关状态]
- BUSINESS_RULES.md#BR-XXX-YYY: [规则摘要]
- ERROR_CODES_SOT.md: [预期错误码]

**TDD 步骤**:

Step 1: 写失败测试
- 调用 /gen test 生成带 SoT 注解的测试
- 断言状态转换符合 STATE_MACHINE.md
- 断言错误码符合 ERROR_CODES_SOT.md

Step 2: 验证测试失败
Run: pytest tests/path/test.py::test_name -v
Expected: FAIL

Step 3: 最小实现
- 调用 /gen be 或 /gen fe 生成代码
- 使用 frozenset 白名单值

Step 4: 验证测试通过
Run: pytest tests/path/test.py::test_name -v
Expected: PASS

Step 5: SoT 合规检查
Run: /sot-check <changed_files>
Expected: 无违规

Step 6: 提交
git commit -m "feat: <描述>"
```

### 4.3 Phase 3: EXECUTE (子代理驱动)

**触发**: 计划已批准
**技能调用**: `superpowers:subagent-driven-development` + AI Factory generators

**执行流程**:
```
For each task in plan:
  ┌─────────────────────────────────────────────────┐
  │ 1. Dispatch Implementer Subagent                │
  │    - 使用 ./prompts/implementer-with-factory.md │
  │    - TDD: /gen test → fail → /gen be|fe → pass │
  │    - SoT 上下文预加载                            │
  └─────────────────────────────────────────────────┘
                        ↓
  ┌─────────────────────────────────────────────────┐
  │ 2. Dispatch Spec Reviewer                       │
  │    - 使用 ./prompts/sot-spec-reviewer.md        │
  │    - /sot-check 验证合规                         │
  │    - 验证实现匹配计划规格                         │
  └─────────────────────────────────────────────────┘
                        ↓
          ┌─────────────────────────┐
          │ Spec issues?            │
          │ YES → Implementer fixes │
          │       → Re-review       │
          │ NO  → Continue          │
          └─────────────────────────┘
                        ↓
  ┌─────────────────────────────────────────────────┐
  │ 3. Dispatch Quality Reviewer                    │
  │    - 使用 ./prompts/quality-reviewer-enhanced.md│
  │    - /sc:analyze 代码质量                        │
  │    - 安全、模式、命名检查                         │
  └─────────────────────────────────────────────────┘
                        ↓
          ┌─────────────────────────┐
          │ Quality issues?         │
          │ YES → Implementer fixes │
          │       → Re-review       │
          │ NO  → Continue          │
          └─────────────────────────┘
                        ↓
  ┌─────────────────────────────────────────────────┐
  │ 4. Mark task complete in TodoWrite              │
  └─────────────────────────────────────────────────┘
```

### 4.4 Phase 4: FINISH

**触发**: 所有任务完成
**技能调用**: `superpowers:finishing-a-development-branch` + `/sot-check`

**执行步骤**:
1. 最终代码审查（全量变更）
2. `/sot-check` 所有变更文件
3. CONFIRM 阶段（防幻觉验证）:
   - 追溯每个状态值到 STATE_MACHINE.md
   - 追溯每个角色到 6-role frozenset
   - 追溯每个错误码到 ERROR_CODES_SOT.md
4. 调用 `superpowers:finishing-a-development-branch`
5. 呈现选项: merge / PR / keep / discard

## 5. TDD 铁律整合

```
╔════════════════════════════════════════════════════════════════════╗
║                         TDD 铁律                                    ║
║                                                                     ║
║   没有失败的测试，就不能写生产代码                                    ║
║   NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST                  ║
║                                                                     ║
╚════════════════════════════════════════════════════════════════════╝
```

### TDD + Factory 工作流

**RED Phase (写失败测试)**:
1. 检测测试类型: `service` | `api` | `state_machine` | `ledger`
2. 加载 SoT 上下文:
   - STATE_MACHINE.md: 状态转换规则
   - ERROR_CODES_SOT.md: 预期错误码
   - BUSINESS_RULES.md: BR-XXX 引用
3. 调用 `/gen test` 生成带 SoT 注解的测试
4. 运行测试，验证 FAIL

**GREEN Phase (最小实现)**:
1. 检测代码类型: `backend` | `frontend`
2. 调用 `/gen be` 或 `/gen fe` 生成 SoT 约束代码
3. 运行测试，验证 PASS
4. `/sot-check` 验证合规

**REFACTOR Phase (重构)**:
1. `/sc:improve` 代码质量建议
2. 应用改进（保持测试绿色）
3. `/sot-check` 验证无 SoT 漂移
4. 提交语义化 commit

**违规处理**:
```
如果检测到先写代码再写测试:
  → 删除代码
  → 从 RED Phase 重新开始
  → 无例外
```

## 6. SoT 合规检查点

| 阶段 | 检查点 | 工具 | 阻断? |
|------|--------|------|-------|
| Brainstorm | SoT 依赖识别 | Manual | 否 |
| Plan | 任务 SoT 引用注入 | sot-aware-planning | 否 |
| TDD RED | 测试 SoT 注解 | ai-ad-test-gen | **是** |
| TDD GREEN | 代码 SoT 注解 | ai-ad-be/fe-gen | **是** |
| Execute | 状态/角色/错误码白名单 | /sot-check | **是** |
| Spec Review | SoT 合规检查 | sot-spec-reviewer | **是** |
| Quality | 代码质量+模式 | /sc:analyze | 条件 |
| Final | 防幻觉验证 | CONFIRM phase | **是** |

## 7. 子代理提示词模板

本技能使用以下子代理提示词（位于 `./prompts/` 目录）:

| 文件 | 用途 |
|------|------|
| `implementer-with-factory.md` | 实现者子代理 - TDD + SoT 约束 |
| `sot-spec-reviewer.md` | SoT 规格审查子代理 |
| `quality-reviewer-enhanced.md` | 质量审查子代理 + SuperClaude |

## 8. 依赖声明

```yaml
dependencies:
  superpowers:
    - brainstorming
    - writing-plans
    - test-driven-development
    - subagent-driven-development
    - executing-plans
    - systematic-debugging
    - finishing-a-development-branch

  ai_code_factory:
    - ai-ad-be-gen
    - ai-ad-fe-gen
    - ai-ad-test-gen
    - ai-ad-flow-orchestrator
    - ai-ad-spec-governor

  superclaude:
    - superclaude-enhancer

sot_documents:
  - docs/sot/MASTER.md
  - docs/sot/DATA_SCHEMA.md
  - docs/sot/STATE_MACHINE.md
  - docs/sot/BUSINESS_RULES.md
  - docs/sot/API_SOT.md
  - docs/sot/ERROR_CODES_SOT.md
```

## 9. 使用示例

### 完整开发周期
```bash
/udev full 实现充值审批功能

# 自动执行:
# 1. BRAINSTORM: 设计讨论 + SoT 依赖识别
# 2. PLAN: 生成 TDD 任务计划 + SoT 引用注入
# 3. EXECUTE: 子代理实现 + 两阶段审查
# 4. FINISH: 最终验证 + PR/Merge
```

### TDD 开发
```bash
/udev:tdd 添加金额验证规则

# 自动执行:
# 1. RED: /gen test 生成测试 → 验证失败
# 2. GREEN: /gen be 生成代码 → 验证通过
# 3. REFACTOR: /sc:improve → /sot-check
```

### 调试问题
```bash
/udev:debug 状态转换异常

# 自动执行:
# 1. /sc:troubleshoot 问题诊断
# 2. superpowers:systematic-debugging 4阶段分析
# 3. 根因定位 + 修复建议
```

## 10. 版本历史

| 日期 | 版本 | 变更 |
|------|------|------|
| 2026-01-13 | 1.0 | 初始版本 - Superpowers + AI Code Factory 整合 |
