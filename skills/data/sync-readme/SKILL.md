---
name: sync-readme
description: Synchronize English README.md with Chinese README_ZH.md, maintaining content parity.
---

# Sync README

## Purpose

Keep the English (README.md) and Chinese (README_ZH.md) documentation in sync. When one is updated, this skill helps translate and synchronize changes to the other.

## Instructions

1. **Compare Both Files**
   - Read README.md and README_ZH.md
   - Identify sections that differ
   - Note new sections in either file

2. **Determine Sync Direction**
   - If English was updated more recently: translate EN → ZH
   - If Chinese was updated more recently: translate ZH → EN
   - If unclear, ask user which is the source of truth

3. **Translate Content**
   - Preserve all code blocks unchanged
   - Translate prose sections accurately
   - Keep technical terms consistent:
     - "rules" → "规则"
     - "commands" → "命令"
     - "skills" → "技能"
     - "agents" → "代理"
     - "instructions" → "指令"
     - "adapter" → "适配器"
     - "symbolic link" → "软链接"

4. **Preserve Structure**
   - Keep same heading hierarchy
   - Maintain table formats
   - Preserve all links and badges
   - Keep code examples identical

5. **Update Language Links**
   - Ensure language toggle links are present
   - English: `[English](./README.md) | [中文](./README_ZH.md)`
   - Chinese: `[English](./README.md) | [中文](./README_ZH.md)`

6. **Verify Completeness**
   - All sections present in both files
   - All features documented in both
   - Examples work in both versions

## Translation Guidelines

### Section Headers
| English | Chinese |
|---------|---------|
| Install | 安装 |
| Commands | 命令 |
| Architecture | 架构 |
| Tab Completion | Tab 补全 |
| Legacy compatibility | Legacy 兼容说明 |
| Supported Sync Types | 支持的同步类型 |

### Common Phrases
| English | Chinese |
|---------|---------|
| Default mapping | 默认映射 |
| Source directory | 源目录 |
| Target directory | 目标目录 |
| Run this command | 运行此命令 |
| This command will | 该命令会 |

## Output

After running this skill:
- Both README files contain identical information
- All features documented in both languages
- Formatting consistent across both files
