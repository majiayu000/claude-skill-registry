---
name: prompt-engineering
description: 通用提示词工程与提示词改写技能，用于设计、优化、评审、模板化与迭代 LLM 提示词；当任务涉及明确目标/约束/输出格式、角色与指令层级、few-shot 示例、结构化标签、链式分解、长上下文管理、评估与回归测试、跨模型迁移或提示词标准化时使用。
---

# Prompt Engineering

## Overview

面向生产场景的通用提示词工程流程与工具箱，帮助把模糊需求转化为可评估、可复用、可迭代的提示词方案。

## Workflow (Production-Ready)

1) 明确目标与评估
- 任务目标、成功标准、失败示例、输出格式与长度上限
- 约束：合规/安全/语气/受众/工具使用/延迟与成本

2) 收集上下文与输入
- 必要背景信息、数据来源、上下文边界、知识盲区
- 需要补充的信息列表；不清楚就先问

3) 选择策略与结构
- 简单任务：清晰直接 + 明确格式
- 复杂任务：few-shot / 分步 / 链式 / XML / 长上下文

4) 设计提示词骨架
- 角色/身份、任务指令、上下文、输入、输出格式、约束、示例
- 使用模板变量分离固定与动态内容

5) 评估与迭代
- 用边界/异常/反例做回归
- 记录版本与变化原因，保留可复用模板

## Strategy Selector

- 清晰直接：需求含糊或目标复杂但步骤清晰
- 模板与变量：高频重复任务或多客户场景
- Few-shot：需要模式学习、风格一致、格式固定
- XML/结构化：长上下文、多段输入、可解析输出
- 角色与层级：需要稳定风格与约束时设置 system/developer
- Chain prompts：任务可拆分或需要自检/复核
- Long context：多文档或超长输入，要求引用证据
- Prompt generator/improver：从 0 起草或改写现有提示词
- Prefill：强制输出前缀或格式起始（平台支持时）
- Extended thinking：高难推理任务（注意成本与时延）

## Deliverables

- Prompt 规范（必含）：目标、输入、约束、输出格式、示例、评估用例
- 测试用例：至少 5 个（正常/边界/异常/反例）

## References (按需加载)

- `prompt-engineering/references/overview.md`: 通用流程与常见问题
- `prompt-engineering/references/be-clear-and-direct.md`: 清晰直接写法
- `prompt-engineering/references/multishot-prompting.md`: few-shot 设计
- `prompt-engineering/references/chain-of-thought.md`: 复杂推理提示
- `prompt-engineering/references/use-xml-tags.md`: XML 标签结构化
- `prompt-engineering/references/system-prompts.md`: 角色与指令层级
- `prompt-engineering/references/prefill-response.md`: 预填充输出
- `prompt-engineering/references/chain-prompts.md`: 链式/分步提示
- `prompt-engineering/references/long-context-tips.md`: 长上下文技巧
- `prompt-engineering/references/extended-thinking-tips.md`: 扩展思考
- `prompt-engineering/references/prompt-templates-and-variables.md`: 模板与变量
- `prompt-engineering/references/prompt-generator.md`: 生成器
- `prompt-engineering/references/prompt-improver.md`: 改写器
- `prompt-engineering/references/claude-4-best-practices.md`: 供应商参考
- `prompt-engineering/references/openai-prompt-engineering.md`: 供应商参考
