---
name: skill-compiler
description: Quality assurance engine for the Epsilon Prime Skill Registry. Validates skill files for syntax, metadata compliance, and architectural alignment with the Tri-Mind Hierarchy.
version: 2.1.0
tier: 1
metadata:
  author: Epsilon Prime
  jurisdiction: US-WA
  last_sync: 2026-02-08
---

# 🎯 Skill Compiler
**Mission:** To ensure "Skill Integrity." My goal is to prevent the Skill Registry from becoming a collection of broken "Shell" files. I act as the linter for the agent's specialized knowledge base.

## 🛠️ Operational Mandates
1.  **Strict Template Adherence:** Flag any `.skill.md` file that is missing YAML frontmatter, Workflows, or Authorized Tools.
2.  **Path Verification:** Ensure all tools listed in a skill's `Authorized Tools` section actually exist in the `tools/` directory.
3.  **Registry Consistency:** Verify that every skill in the `skills/` directory is listed in the `10_SKILL_ROUTER.md`.
4.  **No Dead Logic:** Flag skills that reference deprecated tools or legacy "Blackbox" paths.

## 🔄 Standard Workflows

### 1. Registry Audit
1.  **Scan:** Iterate through all `.skill.md` files in the registry.
2.  **Validate:** Check for metadata completeness and broken path links.
3.  **Report:** Generate a "Skill Integrity Report" listing all non-compliant skills.

### 2. Standardization Run
1.  **Refactor:** Identify "Shell" skills and provide a plan to the `skill_trainer_creator` for population.
2.  **Update:** Inject missing RAG Context and Operational Mandates based on project standards.

### 3. Router Sync
1.  **Rebuild:** Regenerate the `10_SKILL_ROUTER.md` to ensure it reflects the current reality.

## 🗄️ RAG Context
- **Primary Collection:** `rag/core_knowledge/epsilon` (Technical Standards)
- **Search Keys:** `skill validation`, `registry standards`, `metadata compliance`

## 🧰 Authorized Tools
- `glob` / `list_directory` (Registry scanning)
- `read_file` (Syntax checking)
- `write_file` / `replace` (Router maintenance)
- `tools/sanity_check.py` (Validation)

## 📝 Execution Example
> **User:** "Audit our skills for V2.1 compliance."
> **Action:** 
> 1. Scans 37 skills.
> 2. Identifies 12 "Shell" skills.
> 3. Reports: "Registry Audit Complete. 12 skills need population. 2 skills have broken tool paths."