---
name: zotero-citation
description: Zotero 文献引用工作流助手。通过 Zotero 本地 API 读取文献库，为用户指定的文字段落或论文全文自动匹配参考文献，生成规范格式的 Reference。当用户需要"引用文献"、"分配参考文献"、"从 Zotero 选文献"、"生成 Reference 列表"、"匹配引用位置"、"添加参考文献"、"给这段话配引用"、"帮我找合适的参考文献"时触发。也适用于查询 Zotero 文献库、获取文献元数据、或管理论文 citation 的场景。
allowed-tools: Read, Edit, Bash, Write, Glob, Grep
model: opus
---

# Zotero 文献引用工作流

## 核心功能

从 Zotero 本地文献库中检索文献，为用户提供的**任意文字段落或论文全文**智能匹配参考文献，生成规范格式的 Reference。

## 使用模式

本 skill 支持两种使用模式，根据用户输入自动判断：

### 模式 A：段落级匹配（用户提供特定段落）

用户直接粘贴一段或多段文字，为其中的论点匹配合适的参考文献。

**工作流**：
1. 分析段落中的每个论点/声明
2. 从 Zotero 候选文献中匹配
3. 输出：标注了引用位置的段落 + Reference 条目

### 模式 B：全文匹配（用户指定论文文件）

读取整篇论文，逐段分析并分配参考文献。

**工作流**：
1. 读取论文文件（⚠️ 先确认版本）
2. 逐段提取论点并匹配
3. 输出：引用位置表 + 完整 Reference 列表

---

## 前置条件

1. **Zotero Desktop 必须运行**
2. **本地 API 已启用**：Zotero → 编辑 → 设置 → 高级 → 允许其他应用程序通过 API 访问

验证连接：
```bash
curl -s "http://localhost:23119/api/users/0/items?limit=1"
```

⚠️ URL 必须加引号，否则 zsh 会因 `?` 报 `no matches found` 错误。

## 支持文件

- Zotero API 端点与查询详情：见 [references/zotero-api-reference.md](references/zotero-api-reference.md)

---

## 工作流程

### 步骤 1：确认输入与环境

1. 判断使用模式：
   - 用户直接给出了文字段落 → **模式 A**
   - 用户指定了论文文件或说"全文" → **模式 B**（需确认文件版本）
2. 验证 Zotero 本地 API 连接
3. 确认目标 Collection（文献分类），询问用户从哪个 Zotero 分类中选取候选文献

### 步骤 2：获取候选文献

获取 Collection 结构并拉取候选文献列表。

```bash
curl -s "http://localhost:23119/api/users/{USER_ID}/collections" | python3 -c "
import json, sys
data = json.load(sys.stdin)
for c in data:
    print(f\"{c['key']}: {c['data']['name']} (parent: {c['data'].get('parentCollection', 'none')})\")"
```

⚠️ **子分类文献需单独查询**，父分类 API 不自动返回子分类条目。

获取条目时必须过滤 `itemType` 为 `attachment` 和 `note` 的条目。

详细 API 调用见 `references/zotero-api-reference.md`。

### 步骤 3：文献-文本匹配

**分析目标文本**（段落或全文），提取每个需要引用支撑的论点，然后与候选文献摘要进行语义匹配。

**深度阅读**：当用户要求精读某篇特定文献时，通过本地路径提取 PDF 全文：

1. 查询附件 key：`GET /api/users/{ID}/items/{ITEM_KEY}/children`（筛选 `itemType=attachment`）
2. 用 `pdftotext` 提取全文：
```bash
pdftotext ~/Zotero/storage/{ATTACHMENT_KEY}/文件名.pdf -
```

仅在用户明确要求时使用，常规匹配只需摘要即可。

**匹配原则**：

| 文本内容类型 | 匹配文献类型 |
|-------------|-------------|
| 背景/综述性论点 | survey / tutorial 类 |
| 具体技术声明（如 "RAG enhances..."） | 该技术代表性论文 |
| 概念定义（如 "Agentic AI augments..."） | 定义该概念的论文 |
| 方法论论点（如 "LLM reward shaping"） | 提出该方法的论文 |
| 应用场景描述 | 与场景最匹配的论文 |
| 数据/结论引用（如 "studies show..."） | 提供该数据的原始论文 |

**匹配质量检查**：
- 每个引用必须有明确的支撑关系，不做"凑数"引用
- 全文模式下，检查引用分布均匀性，避免全集中在 Introduction
- 同一论点可配多篇文献（如 [1]-[3]），但需各有侧重

### 步骤 4：确认输出格式

**在生成输出前，询问用户两个问题**：

1. **引用格式**：默认 IEEE，可选 APA、GB/T 7714、Chicago 等
2. **输出形式**：
   - **Reference 文本**（默认）：直接可粘贴的参考文献列表
   - **BibTeX 条目**：`.bib` 格式，适用于 LaTeX 工作流

如用户未指定，默认输出 IEEE 格式的 Reference 文本。

### 步骤 5：生成输出

#### IEEE Reference 格式模板

**期刊文章**：
```
[N] A. B. Author1, C. D. Author2, and E. F. Author3, "Title," Journal Name, vol. X, no. Y, pp. XX–YY, Mon. Year.
```

**预印本**：
```
[N] A. B. Author1 et al., "Title," arXiv preprint arXiv:XXXX.XXXXX, Mon. Year.
```

**会议论文**：
```
[N] A. B. Author1 and C. D. Author2, "Title," in Proc. Conference Name, City, Country, Year, pp. XX–YY.
```

格式要点：
- 超过 3 位作者用 "et al."
- 期刊名使用标准缩写（IEEE 缩写表见 reference 文件）
- 页码用 en-dash（–）而非连字符（-）

#### BibTeX 格式模板

```bibtex
@article{AuthorYear,
  author    = {Author1, A. B. and Author2, C. D.},
  title     = {Title of Article},
  journal   = {Journal Name},
  volume    = {X},
  number    = {Y},
  pages     = {XX--YY},
  year      = {2024},
  doi       = {10.xxxx/xxxxx}
}
```

BibTeX 的 cite key 使用 `第一作者姓+年份` 格式（如 `Wang2024`），重名时加后缀 `a/b/c`。

⚠️ Zotero API 也支持直接导出 BibTeX：在 API 请求中添加 `format=bibtex` 参数。

#### 模式 A 输出（段落级）

直接在用户段落中标注引用位置，并附上对应的 Reference / BibTeX 条目：

```
原文标注：
"...多模态架构普遍采用视觉-文本特征序列拼接的统一接口机制 [1], [2]。"

Reference:
[1] A. Author, "Title...," Journal, ...
[2] B. Author, "Title...," Journal, ...
```

#### 模式 B 输出（全文级）

1. **引用位置表**：

| 编号 | 文献简称 | 引用位置 | 引用理由 |
|------|----------|----------|----------|
| [1]  | Author2024 | Sec. I, 第2段 | 支撑XXX论点 |

2. **完整 Reference 列表**（或 BibTeX 文件内容）

---

## 常见问题

| 问题 | 解决方案 |
|------|----------|
| zsh 报 `no matches found` | URL 加双引号 |
| 查不到子分类文献 | 单独用子分类 key 查询 |
| 读错论文版本 | 先 `glob **/*.tex **/*.docx` 列出所有版本让用户确认 |
| 混入 PDF 附件 | 过滤 `itemType` 非 attachment/note |
| 需要 BibTeX | 可手动组装或用 API `format=bibtex` 直接导出 |
