---
name: skill-auditor
description: >
  审查自定义 Claude Code Skills 的质量与规范性。
  检查 SKILL.md 渐进式披露、行数、frontmatter、参考文件链接、目录结构等。
  触发词：审查skill、检查skill质量、skill audit、review skills、
  检查技能规范、skill质量检查
allowed-tools: Read, Bash, Glob, Grep
model: sonnet
---

# Skill Auditor — 自定义 Skill 质量审查

审查当前项目中所有自定义 Claude Code Skills，确保符合渐进式披露规范和最佳实践。

## 审查维度

### 1. Frontmatter 质量（YAML 头部）

| 检查项 | 规范 | 严重度 |
|--------|------|--------|
| `name` | 必填，简洁 | 严重 |
| `description` | 必填，含触发词，50-200 字 | 严重 |
| `allowed-tools` | 按需列出，不多不少 | 警告 |
| `model` | 按复杂度选择（sonnet/opus） | 建议 |
| 触发词覆盖 | description 中包含中英文触发短语 | 警告 |

**Description 要点**：Stage 1 只加载 frontmatter（~50 tokens/skill），description 是触发匹配的唯一依据，必须包含用户可能说的关键词和短语。

### 2. SKILL.md 正文

| 检查项 | 规范 | 严重度 |
|--------|------|--------|
| 总行数 | ≤500 行 | 警告 |
| 核心工作流 | 必须清晰描述阶段/步骤 | 严重 |
| 参考文件链接 | `references/` 下的文件必须有 markdown 链接 | 警告 |
| 冗余内容 | 大段模板/示例/列表应拆到 references | 建议 |
| 术语一致性 | 文件内术语前后一致 | 建议 |

### 3. 目录结构

```
skill-name/
├── SKILL.md              <- 必须
├── README.md             <- 建议（公开发布时）
├── references/           <- 建议（补充文档）
│   ├── *.md
├── scripts/              <- 可选（辅助脚本）
├── templates/            <- 可选（输出模板）
└── config/               <- 可选（配置文件）
```

### 4. 参考文件完整性

- `references/` 下的 `.md` 文件是否都被 SKILL.md 链接
- SKILL.md 中的 `references/` 路径是否都指向存在的文件
- 参考文件行数是否合理（单个建议 ≤200 行）

## 工作流程

### 步骤 1：扫描 Skills 目录

扫描目标路径下所有包含 `SKILL.md` 的子目录，识别为 skill。

默认扫描路径：当前工作目录。

### 步骤 2：逐个审查

对每个 skill 执行以下检查：

```
1. 读取 SKILL.md
2. 解析 frontmatter（name, description, allowed-tools, model）
3. 统计正文行数
4. 检查是否有 references/ 目录
5. 如有 references/，检查双向链接完整性：
   - SKILL.md → references/*.md（链接目标是否存在）
   - references/*.md → SKILL.md（文件是否被引用）
6. 检查 README.md 是否存在
7. 汇总问题清单
```

### 步骤 3：生成审查报告

按以下格式输出：

```markdown
# Skill 审查报告

## 总览

| Skill | 行数 | Frontmatter | 参考链接 | README | 总评 |
|-------|------|-------------|----------|--------|------|
| literature-search | 168 | ✅ | ✅ | ✅ | 通过 |
| knowledge-base-manager | 306 | ✅ | ✅ | ❌ | 警告 |

## 详细问题

### skill-name
- ⚠️ [警告] 缺少 README.md
- 💡 [建议] description 可增加英文触发词
```

严重度图标：
- ❌ 严重：影响 skill 加载或功能
- ⚠️ 警告：不规范但不影响功能
- 💡 建议：可优化项

### 步骤 4：修复建议

对每个问题给出具体修复建议。如用户确认，可直接执行修复。

## 渐进式披露加载原理速查

供审查时参考的 Claude Code skill 加载机制：

| 阶段 | 触发时机 | 加载内容 | Token 开销 |
|------|----------|----------|------------|
| Stage 1 | 会话启动 | 仅 YAML frontmatter | ~50/skill |
| Stage 2 | 用户输入匹配 description | 完整 SKILL.md | 1000-5000 |
| Stage 3 | Skill 执行中按需读取 | references/ scripts/ | 按需 |

**核心原则**：Stage 2 加载的 SKILL.md 是 Claude 理解任务的主要依据，必须自包含核心工作流；大段辅助内容放 Stage 3 按需加载。
