---
description: 提供后端开发、API 设计、数据库交互和框架特定开发能力。当需要实现后端功能、设计 API 或处理数据层逻辑时使用。
name: backend-specialist
---
# Backend Specialist

提供后端开发、API 设计、数据库交互和框架特定开发能力。当需要实现后端功能、设计 API 或处理数据层逻辑时使用。

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

#### backend-architect (1)
- `backend-architect`
  - 触发语义: Senior backend architect specializing in scalable system design, database architecture, API development, and cloud infrastructure. Builds robust, secure, performant server-side applications and microservices
  - 入口文件: `.claude/skills/backend-specialist/references/domains/backend-architect/SKILL.md`

#### embedded-firmware-engineer (1)
- `embedded-firmware-engineer`
  - 触发语义: Specialist in bare-metal and RTOS firmware - ESP32/ESP-IDF, PlatformIO, Arduino, ARM Cortex-M, STM32 HAL/LL, Nordic nRF5/nRF Connect SDK, FreeRTOS, Zephyr
  - 入口文件: `.claude/skills/backend-specialist/references/domains/embedded-firmware-engineer/SKILL.md`

#### feishu-integration-developer (1)
- `feishu-integration-developer`
  - 触发语义: Full-stack integration expert specializing in the Feishu (Lark) Open Platform — proficient in Feishu bots, mini programs, approval workflows, Bitable (multidimensional spreadsheets), interactive message cards, Webhooks, SSO authentication, and workflow automation, building enterprise-grade collaboration and automation solutions within the Feishu ecosystem.
  - 入口文件: `.claude/skills/backend-specialist/references/domains/feishu-integration-developer/SKILL.md`

#### senior-developer (1)
- `senior-developer`
  - 触发语义: Premium implementation specialist - Masters Laravel/Livewire/FluxUI, advanced CSS, Three.js integration
  - 入口文件: `.claude/skills/backend-specialist/references/domains/senior-developer/SKILL.md`

#### solidity-smart-contract-engineer (1)
- `solidity-smart-contract-engineer`
  - 触发语义: Expert Solidity developer specializing in EVM smart contract architecture, gas optimization, upgradeable proxy patterns, DeFi protocol development, and security-first contract design across Ethereum and L2 chains.
  - 入口文件: `.claude/skills/backend-specialist/references/domains/solidity-smart-contract-engineer/SKILL.md`

<!-- AUTO-GENERATED-SKILL-INDEX:END -->

## Notes

- 顶层 `SKILL.md` 仅做索引导航，不承载大体量细节内容。
- 详细资料下沉到 `references/domains/`，按树形结构组织。
