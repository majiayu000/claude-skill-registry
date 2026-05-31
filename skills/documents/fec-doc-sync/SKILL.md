---
name: fec-doc-sync
description: Use when synchronizing frontend project documentation with source-of-truth files such as package.json, runtime templates, CLI commands, public skills, agents, reports, environment examples, or repository structure. Do not use for general prose polishing only; Chinese triggers include 文档同步, 更新 README, docs sync, 命令清单, 能力表同步.
---

# 文档同步

## Purpose

从代码、模板和元数据同步公开文档，避免 README、runtime 文档、能力表和报告说明与实际安装内容漂移。

## Procedure

1. 找到事实来源：
   - `package.json`：版本、脚本、bin、files。
   - `skills/metadata.json`、`skills/eval_queries.json`：公开 skill 清单。
   - `agents/`、`commands/`、`templates/shared/rules/`：安装内容。
   - `docs/project-structure.md` 和 runtime docs：分发说明。
2. 比对文档中的数量、名称、命令、报告文件名和运行时支持矩阵。
3. 更新所有受影响语言版本；若仓库有多语言 README，保持信息一致。
4. 对生成型报告或示例，只更新稳定约定，不把临时报告内容写入公开文档。
5. 若变更来自依赖升级、架构决策或公共能力调整，同步轻量 ADR、变更说明、示例 prompt 和迁移注意事项。
6. 运行文档/元数据一致性测试或相关打包检查。

## Constraints

- 不把 README 变成完整实现细节；公开文档保留高信号摘要。
- 不引入与事实来源不一致的命令、路径或能力名称。
- 不修改用户项目私有文档，除非用户明确指定。
- 多语言文档若无法完整翻译，至少保持数量、命令名、skill id、agent id 和报告格式一致。
- 不把 ADR 当作长篇复盘；只记录背景、决策、取舍、影响范围、验证和回滚线索。

## Expected Output

- README、runtime docs、项目结构和 changelog 中的公开能力清单与代码一致。
- 相关 metadata、marketplace 描述和测试期望同步。
- 总结事实来源、更新范围、验证命令和仍需人工校对的翻译风险。
