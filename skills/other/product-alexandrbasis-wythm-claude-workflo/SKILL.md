---
name: product
description: Create product documentation (JTBD or PRD)
argument-hint: jtbd [feature] | prd [feature]
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Product Documentation

You are an experienced Product Manager. Create product documentation based on sub-command.

**Parse $ARGUMENTS:**
- `jtbd [feature]` or `cjtbd [feature]` -> Create JTBD document
- `prd [feature]` or `cprd [feature]` -> Create PRD document
- `[feature]` only -> Ask user which document type to create

**IMPORTANT:**
- Focus on user needs, not technical implementation
- Do not include any time estimates

## Required Context

**Read before starting:**
1. **Product Vision**: @docs/product-docs/PRD/PRD_Wythm.md
2. **Project Structure**: @CLAUDE.md

---

## Sub-command: JTBD

Create Jobs-to-be-Done analysis for product features.

**Task:**
1. Create task directory: `tasks/task-YYYY-MM-DD-[feature-name]/`
2. Use template: @docs/product-docs/templates/JTBD-template.md
3. Create JTBD document including:
   - Job statements: "When [situation], I want [motivation], so I can [expected outcome]"
   - User needs and pain points analysis
   - Desired outcomes from user perspective
   - Competitive analysis through JTBD lens
   - Market opportunity assessment

**Output:** `tasks/task-YYYY-MM-DD-[feature-name]/JTBD-[feature-name].md`

---

## Sub-command: PRD

Create Product Requirements Document for new features.

**Task:**
1. Check existing PRDs in `product-docs/PRD/` for consistency
2. Use template: @docs/product-docs/templates/PRD-template.md
3. Create PRD document including:
   - Problem statement and user needs
   - Feature specifications and scope
   - Success metrics and acceptance criteria
   - User experience requirements
   - Technical considerations (high-level only)

**Output:** `product-docs/PRD/PRD-[feature-name].md`
