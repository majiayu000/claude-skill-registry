---
name: auto-test-project
category: normal
description: 当用户明确要求"测试项目"、"运行 auto-test-project"或"进行项目级测试"时使用。对完整项目进行多轮 A 轮批判性测试 + B 轮质量检查，系统化发现、记录、修复问题。⚠️ 不适用：用户只是想优化功能（应直接修改）、只是询问项目问题（应直接回答）、没有明确"测试"意图。
metadata:
  author: Bensz Conan
  short-description: 多轮 A 轮测试 + B 轮质量检查 的项目级测试驱动优化流水线
  keywords:
    - auto-test-project
    - 项目级测试
    - project QA
---

# auto-test-project（项目级自动化测试驱动优化）

## Quick Start（最快路径）

1. 在“目标项目根目录”创建本轮会话骨架（会自动创建 `plans/` 与 `tests/`）：

```bash
python3 auto-test-project/scripts/create_test_session.py --project-root . --kind a --create-plan
```

安全提示：该脚本会在 `--project-root` 下创建 `plans/` 与 `tests/`。为防止误用，默认拒绝将系统根目录或用户主目录作为 project-root；如你确有需要，可显式加 `--allow-unsafe-root` 覆盖。

2. 在 `plans/vYYYYMMDDHHMM.md` 写出本轮问题清单（至少 10 个），并使用可引用编号（如 `P0-1`）。
3. 按计划修复，并补齐 `tests/vYYYYMMDDHHMM/TEST_PLAN.md` 与 `tests/vYYYYMMDDHHMM/TEST_REPORT.md` 的可复现证据。
4. 运行验证脚本（推荐收尾用严格模式）：

```bash
python3 auto-test-project/scripts/verify_test_session.py --require-plan tests/vYYYYMMDDHHMM
```

5. 重复 A 轮 N 次后，进入 B 轮质量检查与验证。

## 目标

为完整项目（包括技能项目、工作流项目、或其他具有 `CLAUDE.md` 或类似指令文件的项目）提供系统性的测试驱动优化能力，通过多轮迭代实现持续改进。

## 项目定义

本技能中的"项目"是指：
- 具有项目指令文件（如 `CLAUDE.md`、`AGENTS.md`、`PROJECT.md` 等）
- 具有明确的目录结构和功能模块
- 包含可执行的代码、脚本、或流程定义
- 类似 `init-project` 定义的项目结构

典型项目类型：
- **Agent Skills**：符合 [Agent Skills 开放标准](https://agentskills.io) 的技能
- **工作流项目**：定义了开发流程的项目
- **脚本工具集**：一组协同工作的脚本和工具
- **文档项目**：具有结构化文档和模板的项目

## 你要产出的东西

本 skill 的交付不是"口头建议"，而是一组可追溯的文件：

- `plans/vYYYYMMDDHHMM.md`：A 轮问题分析与改进计划（每轮 1 份）
- `tests/vYYYYMMDDHHMM/`：A 轮测试会话目录（包含 `TEST_PLAN.md` + `TEST_REPORT.md`）
- `plans/B轮-vYYYYMMDDHHMM.md`：B 轮质量检查报告（维度以 `config.yaml:b_round_check.dimensions` 为准）
- `tests/B轮-vYYYYMMDDHHMM/`：B 轮验证会话目录（包含 `TEST_PLAN.md` + `TEST_REPORT.md`）

## 目录与命名规范

- 测试会话 ID：`vYYYYMMDDHHMM`（分钟级时间戳）
- 规划文档：放在 `plans/`
- 测试会话：放在 `tests/`
- B 轮统一加前缀：`B轮-`

## 工作流程

### 概览

```
用户输入（项目根目录 + 问题列表/优化目标）
  ↓
[项目初始化]：验证项目结构、识别项目类型
  ↓
[A轮 × N]：分析 → 计划 → 优化 → 轻量测试
  ↓
B轮：质量原则检查（以 `config.yaml:b_round_check.dimensions` 为准） → 针对性优化 → 轻量验证
  ↓
完成（文档齐全 + 问题闭环 + 项目 CHANGELOG.md 已更新）
```

### 项目初始化

#### P.1 验证项目结构

目标：确认目标是一个有效的"项目"，并识别项目类型。

检查项：
- [ ] 是否存在项目指令文件（`CLAUDE.md`、`AGENTS.md`、`PROJECT.md` 等）
- [ ] 是否存在配置文件（`config.yaml`、`package.json`、`pyproject.toml` 等）
- [ ] 是否有明确的目录结构（源码、文档、脚本等）

输出：`PROJECT_TYPE.md`（可选，记录项目类型和关键信息）

#### P.2 识别测试边界

目标：确定测试范围和优先级。

分析维度：
- **核心模块**：哪些文件/目录是项目的核心功能？
- **测试路径**：哪些功能需要优先测试？
- **依赖关系**：模块间的依赖关系是什么？

输出：在首个 A 轮计划中记录测试边界。

### A 轮测试（可重复 N 次）

#### A.1 初始化会话（生成测试 ID + 目录）

目标：创建本轮的 `plans/` 与 `tests/` 骨架。

推荐使用确定性脚本：

```bash
python3 auto-test-project/scripts/create_test_session.py --project-root . --kind a --id vYYYYMMDDHHMM --create-plan

# 可选：如果你希望 TEST_PLAN.md 直接以计划文档为“种子”，再手动补齐测试细节
python3 auto-test-project/scripts/create_test_session.py --project-root . --kind a --id vYYYYMMDDHHMM --seed-test-plan-from-plan
```

最低要求：
- `plans/` 与 `tests/` 存在
- `tests/vYYYYMMDDHHMM/TEST_PLAN.md` 与 `tests/vYYYYMMDDHHMM/TEST_REPORT.md` 存在

#### A.2 问题分析与计划生成（写入 plans/）

目标：把本轮要解决的问题写成可执行计划，按 P0/P1/P2 排序。

输出：`plans/vYYYYMMDDHHMM.md`

**⭐️ 核心价值**：本项目级测试的核心价值在于**系统视角和批判性思维**，而非替代 linter 进行表面检查。

**数量要求**（强制）：
- 每轮至少发现 10 个问题（P0 + P1 + P2 总和）⚠️ **强制门槛**
- 建议目标范围 15-25 个问题（考虑跨模块复杂性）

**⚠️ 质量要求**（批判性思维门槛）：
- 每轮至少有 **1-2 个痛点级问题**（架构级/设计级问题，非表面问题）
- 每轮至少有 **3 个系统性问题**（架构/过度设计/一致/安全等；项目级优先关注跨模块/跨文件矛盾）
- 每轮问题类型分布推荐：痛点级 ~20%、隐患级 ~50%、噪音级 ~30%
- **每个 P0/P1 问题必须包含批判性思维字段**（批判性质疑、根本原因、价值判断）
- **P0 + P1 占比必须 ≥ 60%**（确保问题有价值；小项目可在计划中说明为何达不到）

说明：默认口径以 `config.yaml:test_rounds.min_issues_per_round` 与 `config.yaml:test_rounds.target_issues_range` 为准。

**核心要求**：
- **独立评估原则**（默认启用，除非用户明确要求“沿上轮跟进修复”）：
  - 每轮 A 轮基于目标项目的**当前工作状态**独立分析
  - 默认**不查看**历史 `plans/` 与 `tests/`（避免确认偏差/路径依赖）
  - 排除范围建议以 `config.yaml:a_round_check.independent_review.exclude_patterns` 为准（历史产物/缓存/依赖目录应排除）
- **批判性思维优先**：**优先使用技巧 0（批判性分析框架）**，再辅以技术检查技巧（技巧 1-8）
  - 技巧 0.1：第一性原理思考（评估项目是否偏离核心目标）
  - 技巧 0.2：架构合理性质疑（评估模块划分、依赖方向、抽象层次）
  - 技巧 0.3：价值导向的问题分类（避免噪音级问题，聚焦痛点级/隐患级）
  - 技巧 0.4：根本原因分析（5 Whys）（挖掘问题本质，而非修复表象）
- **全局意识**：明确本轮在优化 journey 中的位置（首轮/中间/收尾）
- **上下文连贯**：说明与上轮的关联，避免孤立的问题清单
- **项目视野**：考虑跨模块影响和依赖关系，记录涉及的模块
- **优先级依据**：P0/P1/P2 必须有明确的判定标准和价值判断
  - P0: 阻塞性问题、安全风险、核心功能缺陷、架构级偏离
  - P1: 重要优化、模块间接口优化、测试覆盖不足、技术债务
  - P2: 锦上添花、文档改进、后续迭代项
- **可追溯性**：每个问题必须包含位置、涉及模块、影响、修复建议、验证方法
- **问题深度**：每个 P0/P1 问题必须有批判性质疑和根本原因分析（至少 3 次"为什么"）

**详细结构模板**：`references/A_ROUND_PLAN_TEMPLATE.md`（包含"系统视角与批判性分析"章节）

**批判性思维必读**：
- `references/CRITICAL_THINKING_GUIDE.md` ⚠️ **核心文档，必须使用**
- `references/CONSTRUCTIVE_SUGGESTION_GUIDELINES.md` 建设性建议标准（避免“空洞建议/不可验证”）
- `references/ANTI_PATTERNS_LIBRARY.md` 反例库（快速识别常见项目级反模式）

**问题挖掘技巧**：`references/PROJECT_ISSUE_DISCOVERY_TECHNIQUES.md`
- ⚠️ **强制要求**：每轮**必须使用技巧 0（批判性分析框架）**
  - ⚠️ **强烈建议**：每轮使用 3-5 个技巧组合（如技巧 0.1 + 0.2 + 技巧 1 跨模块一致性检查）

**如首轮无明确问题列表**：先做静态检查与一致性检查，再给出问题清单。

#### A.3 执行优化与轻量测试（写入 tests/）

目标：按计划逐项修复，并用轻量测试验证。

输出：`tests/vYYYYMMDDHHMM/TEST_PLAN.md` 和 `tests/vYYYYMMDDHHMM/TEST_REPORT.md`

**⚠️ 强制要求 - 防止"假计划、空报告"**：

**禁止行为**：
- ❌ 保留模板占位符（`{{TEST_ID}}`、`{{MODULE_1}}` 等）
- ❌ 使用"（填入...）"、"待补充"等占位文本
- ❌ 报告内容少于 500 字（排除模板）
- ❌ 缺少具体证据（命令输出、文件路径、截图）

**必须满足**：
- ✅ TEST_PLAN.md 和 TEST_REPORT.md 必须完全替换模板占位符
- ✅ 每个验证点必须有具体的执行记录（命令、输出、结果）
- ✅ 每个问题修复必须有前后对比或可复现证据
- ✅ 报告必须包含明确的结论（通过/失败/部分通过）

**验证方法**（每轮结束后必须执行）：

```bash
# 检查是否还有未替换的模板占位符
grep -r "{{" tests/vYYYYMMDDHHMM/
# 如果有输出，说明模板未被正确替换，必须修复

# 使用验证脚本（推荐）
python3 auto-test-project/scripts/verify_test_session.py tests/vYYYYMMDDHHMM

# 可选：更严格模式（要求 plans/vYYYYMMDDHHMM.md 存在且包含 P0-1 等编号，才能做计划-报告一致性检查）
python3 auto-test-project/scripts/verify_test_session.py --require-plan tests/vYYYYMMDDHHMM
```

**轻量测试原则**：
- 只验证"核心路径"与"本轮变更点"
- 每条结论必须有可复现证据（命令输出、文件、对比结果）
- 中间产物放入 `tests/vYYYYMMDDHHMM/_artifacts/`，不污染主目录
- 项目级测试需要考虑模块间交互

**TEST_PLAN.md 最低内容标准**：
- 具体的测试目标（非模板，明确本轮要验证什么）
- 明确的测试范围和边界（哪些模块/文件）
- 可执行的验证点（至少 3 个，每个包含：描述、方法、预期结果）
- 清晰的通过标准（可衡量的成功条件）

**TEST_REPORT.md 最低内容标准**：
- 执行摘要（状态：✅ 通过 / ❌ 失败 / ⚠️ 部分通过）
- 每个验证点的执行结果（包含实际执行的命令、输出、截图路径等）
- 问题修复记录（每个 P0/P1 问题必须记录：修复前状态 → 修复措施 → 修复后状态）
- 遗留问题清单（未解决的问题及原因）
- 下一步建议（是否需要下一轮、重点是什么）

#### A.4 是否进入下一轮

**⚠️ 数量验证**（强制检查）：

在进入下一轮之前，**必须**确认：

- [ ] 本轮已提出至少 10 个问题（P0 + P1 + P2 总和）
- 如未达到，必须继续挖掘问题（使用跨模块分析、依赖关系分析等技巧）

**⚠️ 进入下一轮前的强制检查**：

在进入下一轮 A 轮之前，**必须**执行以下验证：

```bash
# 1. 检查模板占位符是否被替换
python3 auto-test-project/scripts/verify_test_session.py tests/vYYYYMMDDHHMM

# 2. 检查计划与报告的一致性
# - plans/vYYYYMMDDHHMM.md 中的每个问题是否在 TEST_REPORT.md 中有对应记录
# - 成功标准是否在报告中有验证结论
```

**验证失败的处理**：
- 如果发现模板占位符未替换、报告空白、计划与执行脱节等问题
- 必须先修复当前轮次的测试报告，不得进入下一轮
- 修复标准：满足 A.3 节的所有"必须满足"条件

**验证通过的判断标准**：
- ✅ 问题数量 ≥ 10 个（P0 + P1 + P2 总和）
- ✅ 所有模板占位符已替换
- ✅ TEST_REPORT.md 内容 ≥ 500 字
- ✅ 每个 P0/P1 问题都有修复记录
- ✅ 计划中的成功标准都有验证结论

进入下一轮 A 轮的典型条件：
- 用户指定的轮次数未完成
- 仍存在未解决的 P0 / P1
- 轻量测试报告中出现阻塞性失败
- 发现新的跨模块问题需要解决

**重要**：A 轮结束后（无论多少轮），必须进入 B 轮质量检查，不得跳过。

### B 轮质量检查（维度以 config.yaml:b_round_check.dimensions 为准）

⚠️ **强制执行**：B 轮质量检查是项目级自动测试流程的强制性环节，除非用户明确要求跳过，否则不得省略。

#### B.1 产出质量检查报告（写入 plans/）

目标：对 A 轮后的最新状态做系统性质量检查。

输出：`plans/B轮-vYYYYMMDDHHMM.md`

**建议数量与修复门槛**（默认口径以 `config.yaml:b_round_check.*` 为准）：
- 建议数量：至少 10 条（P0+P1+P2，总和），目标范围 10-20
- 修复率门槛：P0 = 100%，P1 ≥ 80%

检查维度（以 `config.yaml:b_round_check.dimensions` 为准）：
- 硬编码/AI 功能规划
- 冗余残留错误检查
- 安全性检查
- 过度设计检查
- 通用性检查
- 一致性检查
- **项目指令文件瘦身检查**（新增）：检查 CLAUDE.md/AGENTS.md 等项目指令文件是否过于冗长，应将详细内容模块化到各模块的 `references/` 或 `docs/`
- 配置集中化检查：检查可配置参数是否集中到配置文件作为单一真相来源，避免散落造成口径漂移

模板：`templates/B_ROUND_CHECK_TEMPLATE.md`

#### B.2 B 轮优化与验证（写入 tests/）

目标：对 B 轮发现的 P0/P1 进行针对性修复并验证。

推荐创建独立会话目录：

建议显式提供 `--a-test-id`（对应 A 轮会话 ID），避免 B 轮文档中 A/B 关联被默认值误导。

```bash
python3 auto-test-project/scripts/create_test_session.py --project-root . --kind b --id vYYYYMMDDHHMM --a-test-id vYYYYMMDDHHMM
```

输出：`tests/B轮-vYYYYMMDDHHMM/TEST_REPORT.md`

## 完成条件（验收）

- [ ] 用户指定的 A 轮次数已完成（或明确说明提前结束原因）
- [ ] B 轮质量检查已完成并形成报告（⚠️ 强制要求，参考 `config.yaml` 的 `b_round_check.mandatory`）
- [ ] 关键问题（P0/P1）已闭环：计划 → 修复 → 证据 → 结论
- [ ] `plans/` 与 `tests/` 结构完整且可追溯
- [ ] 目标项目的 `CHANGELOG.md` 已更新
- [ ] **每轮测试会话都通过验证脚本检查**（防止"假计划、空报告"）

**最终验证命令**：

```bash
# 验证所有测试会话的完整性
for session in tests/v*/; do
    echo "验证: $session"
    python3 auto-test-project/scripts/verify_test_session.py "$session"
done

# 验证 B 轮会话（如有）
for session in tests/B轮-*/; do
    echo "验证: $session"
    python3 auto-test-project/scripts/verify_test_session.py "$session"
done
```

## 与 auto-test-skill 的区别

| 维度 | auto-test-skill | auto-test-project |
|------|-----------------|-------------------|
| **目标对象** | 单个 Agent Skill | 完整项目（多模块、多文件） |
| **测试范围** | 单个 skill 目录 | 整个项目目录 |
| **问题分析** | skill 级别（SKILL.md、config.yaml） | 项目级别（跨模块、跨文件） |
| **质量检查** | 维度以 `config.yaml:b_round_check.dimensions` 为准 | 维度以 `config.yaml:b_round_check.dimensions` 为准（项目级扩展） |
| **输出位置** | 在 skill 内部创建 `plans/` 和 `tests/` | 在项目根目录创建 `plans/` 和 `tests/` |
| **CHANGELOG** | 更新 skill 的 CHANGELOG.md | 更新项目的 CHANGELOG.md |

## 可复用资源

- 配置：`config.yaml`
- 模板：`templates/`
- 参考：
  - `references/FAQ.md`：常见问题（如何检测“假计划/空报告”、证据标准、避免会话污染等）
  - `references/PROJECT_TESTING_BEST_PRACTICES.md`：项目级测试最佳实践
  - `references/PROJECT_ISSUE_DISCOVERY_TECHNIQUES.md`：项目级问题挖掘技巧 ⚠️ 强烈建议每轮使用 3-5 个技巧组合
  - `references/CRITICAL_THINKING_GUIDE.md`：批判性思维指南 ⚠️ A 轮必须使用
  - `references/CONSTRUCTIVE_SUGGESTION_GUIDELINES.md`：建设性建议标准（可执行、可验证、有证据）
  - `references/ANTI_PATTERNS_LIBRARY.md`：反例库（快速识别项目级反模式）
  - `references/EXAMPLE_STRICT_MINIMAL.md`：严格模式最小示例（P0-1 编号如何让计划-报告一致性检查落地）
  - `references/EXAMPLE_TEST_REPORT.md`：完整的测试报告示例（12 个问题，展示期望的输出质量）
- 辅助脚本：
  - `scripts/create_test_session.py`：创建测试会话目录（支持模板变量自动替换）
  - `scripts/verify_test_session.py`：验证测试会话完整性（包含计划-执行一致性检查）
  - `scripts/verify_all_sessions.py`：批量验证 `tests/` 下的所有会话（可选严格模式）
  - `scripts/verify_skill.py`：一键自检本 skill（必需文件、脚本可用、模板关键占位符自动填充）

## 常见问题与最佳实践

为避免 `SKILL.md` 过长，常见问题与最佳实践下沉到 references：

- `references/FAQ.md`
- `references/PROJECT_TESTING_BEST_PRACTICES.md`
