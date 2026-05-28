---
name: project-os
description: AI project OS for autonomous loop, automated orchestration, and rule-driven execution.
version: 0.1.2
author: Peiiii
license: MIT
tags:
  - governance
  - process
  - release
  - logs
---

# Project OS

用于在新项目中快速落地“开发规范 + 迭代日志 + 发布闭环”的通用体系（Project OS），面向未来演进为可自治、可编排、自动驱动研发流程的 AI 操作系统。

## 三段式定位

1) 自治闭环  
覆盖需求—实现—验证—发布—线上冒烟—复盘的端到端闭环，系统自动推动流程完成并形成可追踪证据链。

2) 自动化编排  
将研发流程拆解为可编排的步骤与指令（commands/skills/workflows），以最小人工干预串联执行、回滚与验收。

3) 规则驱动执行  
所有行为由 Rulebook 统一约束与裁决，确保执行一致性、合规性与可审计性；如需例外必须显式声明并记录。

## 适用场景

- 想把一套严格交付流程迁移到其他项目。
- 需要在团队内统一验证/冒烟/发布规范。

## 启用方式（必须先初始化才生效）

本 Skill 安装后不会自动生效，首次使用时需要初始化；初始化完成后规则与流程才会被执行。

## 初始化流程（首次使用）

1) 用户安装本 Skill 并开始与 agent 对话。  
2) agent 检测到目标项目尚未初始化（如缺少 `AGENTS.md`/`commands`/`docs/logs`）。  
3) agent 主动提示初始化必要性与影响，并请求确认。  
4) 用户确认后，agent 自动完成初始化并反馈结果。  

## 初始化会做什么

- 生成/更新 `AGENTS.md`（若已存在，则合并而非覆盖）
- 生成/更新 `commands/commands.md`
- 生成/更新 `docs/logs` 与 `docs/workflows`
- 保证规则、指令索引、日志制度完整落地

## 手动初始化（仅作为兜底）

将本 Skill 的模板复制到目标项目根目录（若已有文件，需合并而非覆盖）：

```bash
cp -R <skill>/assets/commands ./commands
cp -R <skill>/assets/docs ./docs
cp <skill>/assets/AGENTS.template.md ./AGENTS.md
```

## 关键约束

- “完成所有/完成全部”默认执行完整上线闭环（migrations -> deploy -> 线上冒烟）。
- 冒烟测试默认使用非仓库目录环境，禁止写入仓库子目录。
- 每次开发阶段结束必须完成 build/lint/tsc + 冒烟（如适用）。

## 扩展与维护

- 新增/修改指令：更新 `commands/commands.md` 并同步 AGENTS 索引。
- 新增/修改规则：只在 AGENTS 的 Rulebook 维护。
- 发布流程统一写入 `docs/workflows/npm-release-process.md`。

## 模板索引

- `assets/AGENTS.template.md`
- `assets/commands/commands.md`
- `assets/docs/logs/TEMPLATE.md`
- `assets/docs/logs/README.md`
- `assets/docs/workflows/npm-release-process.md`
