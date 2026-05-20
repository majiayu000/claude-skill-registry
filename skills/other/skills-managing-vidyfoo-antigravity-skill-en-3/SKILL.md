---
name: skills-managing
description: Create and manage ASE skills following best practices. Use when creating new skills, importing skills, understanding the Registry V3.1 structure, or debugging skill activation.
---

# ASE Skill Management Guide (V3.1)

## Purpose

Comprehensive guide for creating and managing skills in the Antigravity Skill Engine (ASE), following the **Registry V3.1** architecture with domain-based organization and semantic matching.

## When to Use This Skill

- Creating or adding new skills
- Importing skills from external sources
- Understanding registry structure and routing
- Debugging skill activation issues
- Maintaining skill documentation

---

## System Architecture (V3.1)

### Directory Structure

Skills are organized by **domain categories**:

```
.agent/skills/
├── registry.json              # V3.1 索引 (唯一真理来源)
│
├── 1-dev/                     # 开发域
│   └── {skill-name}/SKILL.md
├── 2-audit/                   # 审计域
│   └── {skill-name}/SKILL.md
├── 3-sys/                     # 系统域
│   └── {skill-name}/SKILL.md
├── 4-tools/                   # 工具域
│   └── {skill-name}/SKILL.md
└── external/                  # 外部依赖
    └── {skill-name}/SKILL.md
```

### Skill Folder Structure

```
{skill-name}/
├── SKILL.md (required)       # Main skill content
├── resources/                # Templates, guides, assets
└── scripts/                  # Optional executable tooling
```

### Registry V3.1 Schema

```json
{
    "version": "3.1.0",
    "categories": {
        "1-dev": "DEV (开发域)",
        "2-audit": "AUDIT (审计域)",
        "3-sys": "SYS (系统域)",
        "4-tools": "TOOLS (工具域)",
        "external": "EXTERNAL (外部依赖)"
    },
    "skills": {
        "X.Y": {
            "id": "skill-name",
            "name": "X.Y Display Name",
            "category": "category-id",
            "description": "Copied from SKILL.md frontmatter",
            "skill_path": ".agent/skills/{category}/{skill-name}/SKILL.md"
        }
    }
}
```

> **关键变更 (V3.1)**: 移除了 `intent_keywords`，仅使用 `description` 进行语义匹配。

---

## Mode Selection

| Mode | Trigger | Description |
|------|---------|-------------|
| **CREATE** | create, new, add | Create a new skill from scratch |
| **INGEST** | import, clone, ingest | Import an existing skill from git |
| **HARVEST** | harvest, archive, save resource | Archive a reusable resource to a skill |

---

## 1. CREATE Mode (Protocol)

### Step 1: Determine Category

| Category | Use When |
|----------|----------|
| `1-dev` | 功能架构、开发规范、会话管理 |
| `2-audit` | 代码审计、调试、测试 |
| `3-sys` | 生态维护、技能管理、文档初始化 |
| `4-tools` | 文档处理、视觉设计 |
| `external` | 公司专属、外部依赖 |

### Step 2: Create Directory

```bash
mkdir -p .agent/skills/{category}/{skill-name}/resources
```

### Step 3: Write SKILL.md

**Required Frontmatter:**
```yaml
---
name: skill-name
description: Clear description including trigger scenarios. This is used for semantic matching - be descriptive!
---
```

**Body Structure:**
1. Purpose (what this skill does)
2. When to Use (activation conditions)
3. Mode Selection (if multi-mode)
4. Protocols (step-by-step instructions)
5. Resources (links to reference files)
6. Anti-Patterns (what to avoid)

### Step 4: Register in registry.json

```json
"X.Y": {
    "id": "skill-name",
    "name": "X.Y Display Name",
    "category": "{category}",
    "description": "Copy from SKILL.md frontmatter",
    "skill_path": ".agent/skills/{category}/{skill-name}/SKILL.md"
}
```

---

## 2. INGEST Mode (Protocol)

1. **Clone**: `git clone {repo} .agent/skills/_import`
2. **Select**: Ask user which skill to import
3. **Categorize**: Determine target category (1-dev, 2-audit, etc.)
4. **Install**: Move to `.agent/skills/{category}/{skill-name}/`
5. **Register**: Add entry to `registry.json`
6. **Clean**: Remove `_import` directory

---

## 3. HARVEST Mode (Protocol)

When reusable resources are identified during task execution (or manually triggered):

### Step 1: Identify Target Skill
- Which skill produced or would benefit from this resource?
- If unclear, default to the currently active skill.

### Step 2: Generalize Content
- Remove project-specific references (file paths, names)
- Replace hardcoded values with `{{PLACEHOLDER}}` syntax
- Add usage instructions as YAML frontmatter or comments

### Step 3: Archive
```bash
write_to_file .agent/skills/{category}/{skill}/resources/{resource-name}.md
```

### Step 4: Document
Update the skill's SKILL.md `Resource Files` section with a link to the new resource.

## Key Principles

| Principle | Rule |
|-----------|------|
| **500-Line Rule** | SKILL.md 不超过 500 行 |
| **Progressive Disclosure** | 详细文档放 `resources/` |
| **Gerund Naming** | 使用动名词后缀 (*-ing) |
| **Single Source** | `description` 从 SKILL.md 复制到 registry |

---

## Best Practices

### ✅ DO:
- Keep SKILL.md concise and actionable
- Write rich, descriptive `description` for semantic matching
- Use gerund naming (e.g., `architecting`, `debugging`)
- Test activation with real prompts
- Include anti-patterns section

### ❌ DON'T:
- Exceed 500 lines in SKILL.md
- Use overly generic descriptions
- Create flat directories (use category subdirectories)
- Duplicate description between SKILL.md and registry (copy, don't rewrite)

---

## Troubleshooting

**Quick Debug:**
1. Is skill listed in `registry.json`?
2. Is `skill_path` pointing to correct location?
3. Is SKILL.md valid YAML frontmatter + markdown?
4. Is `description` rich enough for semantic matching?

---

## Resource Files

| Topic | File |
|-------|------|
| Ingestion Protocol | [ingestion-protocol.md](resources/ingestion-protocol.md) |
| Skill Review Checklist | [skill-review.md](resources/skill-review.md) |
| MCP Integration | [mcp-integration-guide.md](resources/mcp-integration-guide.md) |

---

**Skill Status**: COMPLETE ✅  
**Line Count**: < 200 ✅  
**Registry Version**: V3.1 ✅
