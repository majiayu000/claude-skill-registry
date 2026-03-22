---
name: ieee-reference-manager
description: IEEE Trans 论文参考文献全流程管理助手。负责参考文献的格式校验、引用审查、BibTeX 条目修复、期刊名标准化、DOI/元数据在线验证、Early Access 处理、作者数量合规、重复条目检测等。当用户需要"检查参考文献"、"修复引用格式"、"验证 DOI"、"整理 bib 文件"、"参考文献审查"时触发。
allowed-tools: Read, Edit, Write, Bash, Glob, Grep, WebSearch, WebFetch, Agent
model: opus
---

# IEEE Trans 论文参考文献管理助手

## 核心能力

### 1. BibTeX 文件审查与修复
- 检测重复条目（相同 DOI / 相似标题 / 重复 key）
- 检测缺失必要字段（author, title, year, journal/booktitle, pages, volume, number）
- Early Access 文章识别与格式修正（删除占位 pages，添加 `note = {early access}`）
- 作者数量合规检查（IEEE 规范：≤6 位全列，≥7 位用 et al.）
- BSTcontrol 配置检查与建议
- 清理未引用的冗余条目

### 2. 引用格式审查
- 连续 `\cite{}` 合并检查（如 `\cite{a}, \cite{b}` → `\cite{a, b}`）
- 引用键名与 .bib 文件交叉验证（检测 missing/undefined references）
- 检查是否有被引用但 .bib 中不存在的条目
- 检查 .bib 中存在但未被引用的条目

### 3. 期刊名标准化
- 检查 journal 字段是否使用 IEEE 标准宏（如 `IEEE_J_WCOM`、`IEEE_J_VT`）
- 检测直接写全名或非标准缩写的条目
- 利用 IEEEabrv.bib / IEEEfull.bib 进行自动匹配和替换建议
- Conference 条目检查 `booktitle` 是否完整

### 4. DOI 与元数据在线验证
- 通过 DOI 在线查询验证论文元数据（标题、作者、年份、期刊）
- 检测 DOI 与实际论文是否匹配
- 检测疑似错误的 DOI（格式不正确、无法解析）
- 验证论文标题是否存在明显拼写错误

### 5. 格式规范检查
- `@article` vs `@inproceedings` 类型检查（期刊用 article，会议用 inproceedings）
- Conference 条目是否有 `booktitle`（不应用 `journal`）
- 页码格式检查（应使用 `--` 而非 `-`）
- 年份合理性检查
- 检查 `copyright`、`langid` 等非必要字段（可建议清理）
- 标题大小写保护检查（缩写词、专有名词是否用 `{{}}` 包裹）

### 6. 扩展条目类型支持
- `@book` / `@incollection`：书籍和章节（需 publisher + address）
- `@techreport`：技术报告（需 institution + number）
- `@standard`：技术标准（IEEE / 3GPP / ISO，需 organization + number）
- `@electronic`：在线资源和网页（需 url + year）
- `@misc`：arXiv 预印本、待发表论文、RFC、白皮书等
- `@phdthesis` / `@mastersthesis`：学位论文（需 school + address）
- `@patent`：专利（需 nationality + number）

## 工作流程

### 模式 A：全面审查（用户说"检查参考文献"、"审查 ref"、"review references"）

**步骤 1：文件定位**
- 自动查找工作目录下的 `.bib` 文件和主 `.tex` 文件
- 识别 IEEEabrv.bib / IEEEfull.bib（标准宏文件，不修改）
- 识别用户的 Ref.bib（待审查文件）

**步骤 2：结构性检查**
- 解析所有 .bib 条目，提取 key、类型、字段
- 检测重复条目（基于 DOI 精确匹配 + 标题模糊匹配）
- 检测缺失必要字段
- 检查条目类型是否正确（article/inproceedings）

**步骤 3：引用交叉验证**
- 从 main.tex 提取所有 `\cite{...}` 引用键
- 与 .bib 文件条目交叉比对
- 报告：missing references（cited but not in bib）、unused entries（in bib but not cited）

**步骤 4：格式检查**
- 连续 \cite 合并检查
- 期刊名宏检查
- Early Access 识别
- 作者数量 + BSTcontrol 检查
- 页码格式检查

**步骤 5：输出报告**
以表格形式汇总所有问题，按严重程度排序：
- **严重**（会导致编译错误或参考文献列表错误）
- **警告**（格式不规范但不影响编译）
- **建议**（可改可不改的优化项）

### 模式 B：DOI 验证（用户说"验证 DOI"、"verify references"、"检查论文真实性"）

**步骤 1**：提取所有 .bib 条目的 DOI
**步骤 2**：逐条通过 WebSearch 或 DOI resolver 验证
**步骤 3**：比对返回的元数据与 .bib 中的 title/author/year
**步骤 4**：标记不匹配或无法解析的条目

### 模式 C：单条修复（用户指定某个条目或某个问题）

直接定位并修复，遵循学术写作工作流（先展示 Before/After，等确认后修改）。

### 模式 D：新增参考文献（用户提供论文信息，需要生成 BibTeX 条目）

**步骤 1**：根据用户提供的信息（DOI / 标题 / 作者）搜索论文
**步骤 2**：生成规范的 BibTeX 条目（使用 IEEE 宏、完整字段）
**步骤 3**：检查是否与现有条目重复
**步骤 4**：建议插入位置和引用键命名

## 核心规则

### IEEE 参考文献格式规范

1. **作者**：BibTeX 中使用全名（`Last, First Middle`），IEEEtran.bst 自动缩写为首字母
2. **期刊名**：必须使用 IEEE 标准宏（IEEEabrv.bib 中定义），不要硬编码全名或缩写
3. **作者数量**：
   - ≤6 位：全部列出
   - ≥7 位：列第 1 位 + *et al.*
   - 通过 BSTcontrol 的 `ctluse_forced_etal`、`ctlmax_names_forced_et_al`、`ctlnames_show_etal` 控制
4. **Early Access 文章**：
   - 删除 `pages` 字段（`pages = {1--1}` 是 IEEE Xplore 占位符）
   - 添加 `note = {early access}`
   - 保留 `doi` 字段（唯一永久标识符）
   - 不需要 `volume` 和 `number`
5. **引用合并**：相邻的 `\cite{a}, \cite{b}` 应合并为 `\cite{a, b}`
6. **条目类型**：
   - 期刊论文 → `@article`（需要 `journal`）
   - 会议论文 → `@inproceedings`（需要 `booktitle`，不用 `journal`）
7. **页码**：使用双连字符 `--`（如 `pages = {100--110}`）
8. **DOI**：标准 IEEEtran.bst 默认不显示 DOI，但保留 `doi` 字段无害且有助于验证
9. **BSTcontrol**：必须在 .bib 文件开头定义，且在 .tex 中用 `\bstctlcite{IEEEexample:BSTcontrol}` 调用

### 命名约定

BibTeX key 推荐格式：`首作者姓年份+关键词`，如 `zhao2019computation`、`li2025secrecy`

### 常见错误清单

| 错误类型 | 示例 | 修复方法 |
|---------|------|---------|
| 重复条目 | 同一论文两个不同 key | 删除重复，统一引用 |
| \cite 未合并 | `\cite{a}, \cite{b}` | → `\cite{a, b}` |
| Early Access 保留占位页码 | `pages = {1--1}` | 删除 pages，加 note |
| Conference 用了 @article | `@article` + `booktitle` | 改为 `@inproceedings` |
| 期刊名硬编码 | `journal = {IEEE Trans. Wireless Commun.}` | → `journal = IEEE_J_WCOM` |
| 标题拼写错误 | "Computation Computational" | 核实原文实际标题 |
| 作者过多未截断 | 7+ 作者全列 | BSTcontrol 启用 et al. |
| 缺失必要字段 | 无 volume/number/pages | 通过 DOI 补全 |

## 辅助工具集成

项目中可能存在以下辅助脚本，如存在则优先利用：

### analyze_bib.py
- 功能：解析 .bib 文件，检测重复、分析引用覆盖率
- 调用：`python analyze_bib.py`
- 输出：详细分析报告

### nameTranslate.py
- 功能：将 .bib 中硬编码的期刊名替换为 IEEE 标准宏
- 调用：`python nameTranslate.py`
- 依赖：IEEEfull.bib 用于全名匹配

## 参考文件

- [IEEE 参考文献格式规范详细手册](references/ieee-reference-rules.md) - 各条目类型的必需字段、格式要求、IEEE 标准宏用法等完整规范
- [参考文献辅助脚本核心逻辑](references/utility-scripts.md) - analyze_bib.py 和 nameTranslate.py 的核心逻辑提取，可直接调用或参考实现

## 注意事项

1. **不修改 IEEEabrv.bib 和 IEEEfull.bib**——这些是 IEEE 官方标准宏文件
2. **修改前必须展示 Before/After**，等用户确认后再执行（遵循全局 CLAUDE.md 规则）
3. **DOI 验证时注意**：部分新发表或 Early Access 文章可能尚未被搜索引擎索引
4. **标题中的特殊格式**（如 `{{...}}`）是 BibTeX 的大小写保护，不要随意删除
5. **搜索验证论文时**，优先使用 DOI 查询，其次使用标题+作者搜索
6. **不要自动删除未引用条目**——用户可能正在写作中，留待确认
