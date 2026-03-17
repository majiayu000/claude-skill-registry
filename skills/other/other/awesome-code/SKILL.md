---
name: awesome-code
description: 当用户明确要求"使用 awesome-code / 多代理协作 / 并行协调开发"时使用。通过脚本解析任务，推荐合适的子代理与协作策略，并输出可执行的下一步。⚠️ 不适用：用户仅需单一角色的简单修改或咨询、用户未明确表达多代理协作意图、用户只是了解技能概念。
metadata:
  short-description: 智能多代理软件开发协调系统
  keywords:
    - 多代理协调
    - 任务拆解
    - 并行执行
    - 软件工程
    - 专业化代理
    - awesome-code
  category: 软件开发工具
  author: Bensz Conan
  platform: Claude Code | OpenAI Codex | ChatGPT
---

# Awesome Code - 智能多代理软件开发协调系统

本技能用于“复杂开发任务”的多代理编排：先用确定性脚本做任务拆解与路径发现，再按推荐策略加载子代理规范并执行。

## 执行前置：动态发现技能安装路径（硬编码部分）

在调用任何脚本之前，必须先运行 `scripts/get_path.py` 动态发现真实安装路径，并使用返回的绝对路径执行后续命令（避免硬编码 `~/.claude/skills/` / `.claude/skills/`）。

```bash
python3 ~/.claude/skills/awesome-code/scripts/get_path.py
python3 ~/.codex/skills/awesome-code/scripts/get_path.py
# 或（项目级安装）
python3 .claude/skills/awesome-code/scripts/get_path.py
python3 .codex/skills/awesome-code/scripts/get_path.py
```

从 JSON 输出中读取：
- `skill_root`
- `executable_scripts.*`（例如 `executable_scripts.agent_coordinator`）

## 核心理念

- 智能任务识别：用脚本把“需求描述”转成可执行的任务拆解/策略建议
- 多代理协调：对独立子任务并行，对有依赖的子任务顺序执行
- 专业化分工：每个子代理专注一个领域，降低单模型的认知负担
- 渐进式信息披露：只在需要时加载对应子代理的 `SKILL.md`

## 代理团队（14 个子代理）

| role | 领域 |
|------|------|
| tdd-workflow | TDD 测试驱动开发 |
| systematic-debugging | 系统化调试与根因分析 |
| code-reviewer | 代码审查与质量保证 |
| git-workflow | Git 工作流与版本控制 |
| frontend-specialist | 前端开发与组件设计 |
| backend-specialist | 后端开发与 API 设计 |
| devops-specialist | DevOps 与自动化运维 |
| security-specialist | 应用安全与合规 |
| documentation-specialist | 技术文档与 API 文档 |
| context-optimizer | 上下文管理与优化 |
| brainstorming | 交互式设计优化 |
| mirror-optimizer | 镜像源优化 |
| writing-plans | 实施计划与任务拆解 |
| multi-agent-coordinator | 多代理协调 |

## 核心工作流（AI 执行）

1. 运行 `get_path.py`，拿到 `executable_scripts.agent_coordinator` 的绝对路径。
2. 调用 `agent_coordinator.py` 进行任务分析，得到：推荐代理列表 + 协调策略（single / sequential / parallel）。
3. 对每个推荐代理，按需加载其子代理规范：`awesome-code/agents/{role}/SKILL.md`。
4. 按协调策略执行：
   - 并行：相互独立的任务（例如“写测试 + 改文档 + 做静态检查”）
   - 顺序：存在依赖链的任务（例如“先修 bug → 再补测试 → 再重构”）
5. 聚合结果：
   - 统一口径（术语/目标/约束）
   - 标注 P0/P1/P2 优先级
   - 给出可执行的下一步（含验证方式）

最小示例：

```bash
python3 ~/.claude/skills/awesome-code/scripts/get_path.py
python3 /ABS/PATH/awesome-code/scripts/agent_coordinator.py "fix login bug"
```

## 常用脚本（确定性操作）

注意：脚本路径以 `get_path.py` 输出为准。

- `scripts/get_path.py`：输出 `skill_root` 与可执行脚本绝对路径（JSON）
- `scripts/agent_coordinator.py`：任务分析 → 推荐代理 + 协调策略
- `scripts/create_test_session.py`：创建 A/B 轮会话目录与计划骨架（便于追溯）
- `scripts/test_runner.py`：运行测试/覆盖率
- `scripts/code_analyzer.py`：静态分析与质量检查
- `scripts/performance_benchmark.py`：基准测试与报告

## 配置管理（Single Source of Truth）

- 版本号仅在 `awesome-code/config.yaml:skill_info.version` 维护；`SKILL.md` 不记录版本历史。
- 代理启用与优先级：`awesome-code/config.yaml:multi_agent.*`
- 质量阈值/开关：`awesome-code/config.yaml:tdd`、`awesome-code/config.yaml:code_review` 等
- 变更记录：`awesome-code/CHANGELOG.md`

## 参考资料（仅一层深度；需要时按需加载）

- TDD：`awesome-code/references/tdd-best-practices.md`
- 系统化调试：`awesome-code/references/debugging-systematic.md`
- 代码审查清单：`awesome-code/references/code-review-checklist.md`
- Git 工作流：`awesome-code/references/git-workflow.md`
- 多代理协调模式：`awesome-code/references/multi-agent-patterns.md`
- 上下文优化策略：`awesome-code/references/context-optimization.md`
- 批判性思维与测试优化：`awesome-code/references/CRITICAL_THINKING_GUIDE.md`
- A 轮计划模板：`awesome-code/references/A_ROUND_PLAN_TEMPLATE.md`
- 建设性建议：`awesome-code/references/CONSTRUCTIVE_SUGGESTION_GUIDELINES.md`
- 问题挖掘技巧：`awesome-code/references/ISSUE_DISCOVERY_TECHNIQUES.md`
- 反例库：`awesome-code/references/ANTI_PATTERNS_LIBRARY.md`
- 脚本调用策略：`awesome-code/references/SCRIPT_PATH_STRATEGY.md`
