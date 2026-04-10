---
name: llm-wiki
version: "1.0.0"
updated: 2026-04-10
description: "Karpathy 风格 LLM Wiki / markdown knowledge base 工作流。用于 ingest、query、lint 持久化知识库；先做 orientation，再按 analysis -> generation 维护 wiki。"
---
用于维护 **Karpathy 风格的 LLM Wiki**：把长期有价值的知识编译进一个可持续更新的 markdown wiki，而不是每次查询都从原始材料重做检索。

这个 skill 只定义**共享流程**，不绑定具体 Vault、taxonomy、目录名或项目路径。项目现场规则必须继续从 wiki 自身读取。

# 何时使用

当用户出现以下意图时使用本 skill：

- 明确提到 `llm wiki`、`wiki`、`knowledge base`、`知识库`
- 要求 `ingest` / `query` / `lint` 一个 markdown wiki
- 要把文章、推文、笔记、论文吸收到现有 wiki
- 要基于已有 wiki 回答问题，而不是直接临时总结
- 要检查 wiki 的断链、孤儿页、索引遗漏、重复页或证据漂移

若当前环境存在 `orbit-os`、`bird-twitter` 等 skill，可与本 skill 协作：

- Obsidian / Vault 结构约束：先读 `orbit-os`
- X/Twitter 来源采集：先用 `bird-twitter` 获取原文或桥接 source，再回到 wiki ingest

# 会话起步（每次都做）

在 ingest / query / lint 之前，先定位 wiki 根目录，然后做 orientation。

wiki 路径优先级：

1. 用户显式给出的路径
2. 当前仓库或工作区内明显存在的 wiki 目录
3. 若仍不明确，再问用户

orientation 顺序：

1. 读 `SCHEMA.md`
2. 若存在，读 `purpose.md`
3. 读 `index.md`
4. 扫描最近 `log.md`
5. 若 wiki 根目录有 `AGENTS.md` 或 `_meta/quickstart-prompts.md`，把它们视为项目现场补充规则

只有完成 orientation 后，才能决定是否新建页面、更新页面或回答 query。

# 核心操作

## Ingest

默认采用 **analysis -> generation** 两步，而不是直接写页面。

analysis 阶段至少要回答：

- 这条 source 的核心信息是什么
- 它与现有 wiki 哪些页面重合
- 应更新哪些已有页面
- 是否值得新建页面；如果值得，页类型是什么
- 是否存在冲突、证据补强或范围外信息
- 是否应使用 source bridge，而不是把外部 canonical 路径直接塞进 frontmatter

如果 wiki 已经定义 `_meta/ingest-analysis/` 或等价目录，先把 analysis 落到该目录；如果没有，就先在回复里给出 analysis 摘要，再执行 generation。

generation 阶段要求：

- 遵守本地 `SCHEMA.md` / `purpose.md`
- 优先更新已有页面，再决定是否新建页面
- 更新 `updated` 字段
- 补上必要的 `[[wikilinks]]`
- 把新页或变更同步进 `index.md`
- 把动作记录进 `log.md`
- `raw/` 视为原始层，默认不重写既有 source

除非用户明确要求“跳过 analysis”或本地规则明确允许，否则不要直接一把写入 wiki。

## Query

query 不是普通聊天，先判断它是否属于 wiki 的长期主题范围。

步骤：

1. 先看 `purpose.md` 是否覆盖当前问题
2. 再从 `index.md` 和相关页面定位已有知识
3. 优先基于现有 wiki 回答，而不是重新从外部材料发挥
4. 如果答案具有长期价值，再决定是否沉淀到 `queries/` 或回写现有页面

当 wiki 规模变大时，可使用轻量 relevance 扩展：

- 标题命中
- wikilink 邻居页
- source overlap
- 最近更新页

但不要在没有本地约束的情况下，擅自发明复杂 graph ranking。

## Lint

lint 关注结构健康，而不是重写内容。

至少检查：

- `index.md` 是否漏页
- 是否存在孤儿页
- 是否存在断开的 wikilink
- frontmatter 是否缺关键字段
- 最近 source 是否已真正消化进知识层
- 是否出现重复页或明显分页失衡
- 冲突结论是否被标记，而不是被静默覆盖

lint 的产出默认是问题清单和建议动作；除非用户要求，不要在 lint 阶段顺手大改内容。

# 可选模式

## Source Bridge

如果 canonical 原文位于 wiki 外部的知识库或归档系统，优先在 wiki 的 `raw/` 层写一份桥接 source，再把 frontmatter 指向桥接文件。这样可以避免源路径频繁漂移。

## 瘦 Frontmatter

如果页面 `sources` 过长，可采用“瘦头部”策略：

- frontmatter 只保留少量核心来源
- 完整来源列表放入页面内或独立 registry
- 若本地 schema 允许，可增加 `source_count`

不要在没有本地 schema 支持的情况下强行改写。

# 不要做的事

- 不要把具体 Vault 路径、项目 taxonomy、目录命名习惯硬编码进共享 skill
- 不要假设所有 wiki 都有 `purpose.md`、`_meta/ingest-analysis/` 或相同目录结构
- 不要绕过本地 `SCHEMA.md` 自创结构
- 不要把临时聊天结论默认当成长期知识入库
- 不要把 Hermes / Claude / Codex 的运行态 patch 直接当作 wiki 规则

# 成功标准

一次合格的 wiki 操作，至少满足：

- 先 orientation，再行动
- 写入遵循本地规则，不污染项目现场
- ingest 有 analysis 痕迹
- query 优先复用现有知识
- lint 输出的是结构问题，不是随意重写
