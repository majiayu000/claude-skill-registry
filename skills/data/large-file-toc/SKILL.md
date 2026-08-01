---
name: large-file-toc
description: 为大文件生成目录概要。当入库的 Markdown 文件超过阈值（默认30KB）时，提取标题结构创建导航文件。触发条件：Markdown 文件大小
  >= 30KB。
---

---
name: large-file-toc
description: Generate table of contents overview for large files. When onboarded Markdown file exceeds threshold (default 30KB), extract heading structure to create navigation file. Trigger condition: Markdown file size >= 30KB.
---

# Large File Table of Contents Overview Generation

Generate table of contents overview for large Markdown files for quick user navigation.

## Applicable Conditions

- Markdown file size >= 30KB
- Automatically triggered at onboarding stage 5 (write and update)

## Quick Workflow

1. **Extract headings**: Use Grep to search `^#+\s+.*$`
2. **Generate overview**: Create `contents_overview/{filename}_overview.md`
3. **Update README**: Record overview file path

## Grep Extract Headings

```bash
grep -n '^#' knowledge_base/path/to/file.md
```

Output example:
```
10:# Chapter 1 Introduction
150:## 1.1 Background
180:## 1.2 Objectives
400:# Chapter 2 Methodology
```

## Table of Contents Overview Format

See [TOC_TEMPLATE.md](TOC_TEMPLATE.md)

## README Update Format

```markdown
- [filename.md](path/to/file.md) (XXX KB) - Brief description [Table of Contents](contents_overview/filename_overview.md)
```
