---
description: 提供测试策略、测试编写、测试执行和测试结果分析能力。当需要编写测试、修复测试或优化测试流程时使用。
name: testing-specialist
---
# Testing Specialist

提供测试策略、测试编写、测试执行和测试结果分析能力。当需要编写测试、修复测试或优化测试流程时使用。

## Skill Index

<!-- AUTO-GENERATED-SKILL-INDEX:START -->
以下索引由 `node scripts/update-skill-index.js` 自动生成，用于让 Claude 在顶层专家触发后继续路由到最相关的子技能。

### Claude 使用说明

1. 先将用户当前任务与每个子技能的 `触发语义` 进行语义匹配，不要只看目录名。
2. 一旦找到最相关的子技能，立即打开其 `入口文件` 指向的 `SKILL.md`，把它作为下一层入口。
3. 进入子技能后，再根据该子技能自己的说明按需加载同目录下的 `references/`、`scripts/`、`assets/`，不要在顶层专家中预先展开大段细节。
4. 如果多个子技能都相关，先加载最贴近主目标的那个，再按需补充其他子技能，避免一次性加载过多上下文。
5. 下方 `入口文件` 路径相对于项目根目录，可直接用于 `Read` 操作。

### 子技能索引

#### accessibility-auditor (1)
- `accessibility-auditor`
  - 触发语义: Expert accessibility specialist who audits interfaces against WCAG standards, tests with assistive technologies, and ensures inclusive design. Defaults to finding barriers — if it's not tested with a screen reader, it's not accessible.
  - 入口文件: `.claude/skills/testing-specialist/references/domains/accessibility-auditor/SKILL.md`

#### api-tester (1)
- `api-tester`
  - 触发语义: Expert API testing specialist focused on comprehensive API validation, performance testing, and quality assurance across all systems and third-party integrations
  - 入口文件: `.claude/skills/testing-specialist/references/domains/api-tester/SKILL.md`

#### evidence-collector (1)
- `evidence-collector`
  - 触发语义: Screenshot-obsessed, fantasy-allergic QA specialist - Default to finding 3-5 issues, requires visual proof for everything
  - 入口文件: `.claude/skills/testing-specialist/references/domains/evidence-collector/SKILL.md`

#### performance-benchmarker (1)
- `performance-benchmarker`
  - 触发语义: Expert performance testing and optimization specialist focused on measuring, analyzing, and improving system performance across all applications and infrastructure
  - 入口文件: `.claude/skills/testing-specialist/references/domains/performance-benchmarker/SKILL.md`

#### reality-checker (1)
- `reality-checker`
  - 触发语义: Stops fantasy approvals, evidence-based certification - Default to \"NEEDS WORK\", requires overwhelming proof for production readiness
  - 入口文件: `.claude/skills/testing-specialist/references/domains/reality-checker/SKILL.md`

#### test-results-analyzer (1)
- `test-results-analyzer`
  - 触发语义: Expert test analysis specialist focused on comprehensive test result evaluation, quality metrics analysis, and actionable insight generation from testing activities
  - 入口文件: `.claude/skills/testing-specialist/references/domains/test-results-analyzer/SKILL.md`

#### tool-evaluator (1)
- `tool-evaluator`
  - 触发语义: Expert technology assessment specialist focused on evaluating, testing, and recommending tools, software, and platforms for business use and productivity optimization
  - 入口文件: `.claude/skills/testing-specialist/references/domains/tool-evaluator/SKILL.md`

#### webapp-testing (1)
- `webapp-testing`
  - 触发语义: 使用 Playwright 与本地 Web 应用程序交互和测试的工具包。支持验证前端功能、调试 UI 行为、捕获浏览器截图和查看浏览器日志。
  - 入口文件: `.claude/skills/testing-specialist/references/domains/webapp-testing/SKILL.md`

#### workflow-optimizer (1)
- `workflow-optimizer`
  - 触发语义: Expert process improvement specialist focused on analyzing, optimizing, and automating workflows across all business functions for maximum productivity and efficiency
  - 入口文件: `.claude/skills/testing-specialist/references/domains/workflow-optimizer/SKILL.md`

<!-- AUTO-GENERATED-SKILL-INDEX:END -->

## Notes

- 顶层 `SKILL.md` 仅做索引导航，不承载大体量细节内容。
- 详细资料下沉到 `references/domains/`，按树形结构组织。
