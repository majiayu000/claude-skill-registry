---
description: 提供安全审计、风险评估和合规检查能力。当需要进行安全审查、风险评估或合规验证时使用。
name: security-specialist
---
# Security Specialist

提供安全审计、风险评估和合规检查能力。当需要进行安全审查、风险评估或合规验证时使用。

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

#### agentic-identity-trust (1)
- `agentic-identity-trust-architect`
  - 触发语义: Designs identity, authentication, and trust verification systems for autonomous AI agents operating in multi-agent environments. Ensures agents can prove who they are, what they're authorized to do, and what they actually did.
  - 入口文件: `.claude/skills/security-specialist/references/domains/agentic-identity-trust/SKILL.md`

#### blockchain-security-auditor (1)
- `blockchain-security-auditor`
  - 触发语义: Expert smart contract security auditor specializing in vulnerability detection, formal verification, exploit analysis, and comprehensive audit report writing for DeFi protocols and blockchain applications.
  - 入口文件: `.claude/skills/security-specialist/references/domains/blockchain-security-auditor/SKILL.md`

#### compliance-auditor (1)
- `compliance-auditor`
  - 触发语义: Expert technical compliance auditor specializing in SOC 2, ISO 27001, HIPAA, and PCI-DSS audits — from readiness assessment through evidence collection to certification.
  - 入口文件: `.claude/skills/security-specialist/references/domains/compliance-auditor/SKILL.md`

#### identity-graph-operator (1)
- `identity-graph-operator`
  - 触发语义: Operates a shared identity graph that multiple AI agents resolve against. Ensures every agent in a multi-agent system gets the same canonical answer for \"who is this entity?\" - deterministically, even under concurrent writes.
  - 入口文件: `.claude/skills/security-specialist/references/domains/identity-graph-operator/SKILL.md`

#### security-engineer (1)
- `security-engineer`
  - 触发语义: Expert application security engineer specializing in threat modeling, vulnerability assessment, secure code review, and security architecture design for modern web and cloud-native applications.
  - 入口文件: `.claude/skills/security-specialist/references/domains/security-engineer/SKILL.md`

#### threat-detection-engineer (1)
- `threat-detection-engineer`
  - 触发语义: Expert detection engineer specializing in SIEM rule development, MITRE ATT&CK coverage mapping, threat hunting, alert tuning, and detection-as-code pipelines for security operations teams.
  - 入口文件: `.claude/skills/security-specialist/references/domains/threat-detection-engineer/SKILL.md`

<!-- AUTO-GENERATED-SKILL-INDEX:END -->

## Notes

- 顶层 `SKILL.md` 仅做索引导航，不承载大体量细节内容。
- 详细资料下沉到 `references/domains/`，按树形结构组织。
