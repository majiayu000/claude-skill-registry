---
name: constitution
description: "Create or update the project constitution - personalized governance and coding principles. Use when starting a project or updating project standards. Triggers on: create constitution, update principles, set project rules."
---

# Project Constitution Generator

Create a personalized project constitution that defines your team's coding principles, patterns, and governance.

---

## The Job

1. Ask the user about their project's coding philosophy and standards
2. Analyze the project structure and documentation
3. Generate personalized constitution based on their answers → `relentless/constitution.md`
4. Generate personalized agent prompt based on the same analysis → `relentless/prompt.md`
5. Ensure consistency with project templates and documentation

**Important:** The constitution is the foundation for all feature work - create this before generating features.

---

## Upgrade Detection (For Existing Users)

If `relentless/constitution.md` and/or `relentless/prompt.md` already exist:

### Step 0: Check for Template Updates

1. **Read current files:**
   - Check version in existing constitution.md (look for `<!-- TEMPLATE_VERSION: X.Y.Z -->` or `**Template Version:**`)
   - Check generated date in existing prompt.md

2. **Compare with templates:**
   - Read `.claude/skills/constitution/templates/constitution.md`
   - Read `.claude/skills/constitution/templates/prompt.md`
   - Check template VERSION comments for changes

3. **Detect changes:**
   - If template version > existing version → Offer upgrade
   - If template has new sections → Offer selective merge
   - If quality commands changed → Offer prompt.md refresh

4. **Offer upgrade options:**
   ```markdown
   ## Upgrade Available

   Your constitution.md is v2.0.0, template is v2.1.0.

   Changes in v2.1.0:
   - Added SpecKit workflow documentation
   - Enhanced TDD requirements
   - Added quality gates section

   Options:
   A. Full upgrade (backup existing, apply template changes)
   B. Selective merge (show diff, choose sections)
   C. Skip upgrade (keep existing)
   D. Regenerate from scratch (lose customizations)
   ```

5. **If upgrading:**
   - Backup existing files to `*.backup`
   - Apply template changes preserving customizations
   - Update version number
   - Update `LAST_AMENDED_DATE` to today

---

## Step 1: Gather Project Information

Ask essential questions about the project:

**Project Identity:**
- Project name?
- Primary programming language(s)?
- Tech stack (frameworks, libraries)?

**Testing Philosophy:**
- Testing approach? (TDD, test after, pragmatic)
- Required test coverage?
- Testing frameworks preferred?

**Code Quality:**
- Linting/formatting tools?
- Required checks before commit? (typecheck, lint, test)
- Code review requirements?

**Architecture Principles:**
- Preferred patterns? (MVC, clean architecture, etc.)
- Modularity requirements?
- Performance expectations?

**Version Control:**
- Branch naming conventions?
- Commit message format?
- CI/CD requirements?

---

## Step 2: Generate Constitution

Load the template from `templates/constitution.md` and:

1. Replace all `[PLACEHOLDER]` tokens with concrete values from user answers
2. Add/remove principles based on project needs (template is a starting point)
3. Ensure each principle has:
   - **MUST** rules (enforced, blocking)
   - **SHOULD** rules (best practices, warnings)
   - Clear rationale
4. Set version to `1.0.0` for new constitutions
5. Set ratification date to today
6. Add governance section with amendment procedures

---

## Step 3: Analyze Project Structure

Read and analyze project documentation:

**Core Files:**
- `README.md` - Project overview, setup instructions
- `AGENTS.md` or `CLAUDE.md` - Developer guidelines
- `package.json` - Scripts, dependencies, tech stack
- `CONTRIBUTING.md` - Contribution workflow (if exists)

**Extract:**
- Tech stack (TypeScript, React, Node, etc.)
- Testing framework (vitest, jest, playwright)
- Quality commands (`typecheck`, `lint`, `test`)
- Build system (bun, npm, turbo, vite)
- Linting setup (eslint, biome)
- File structure patterns

---

## Step 4: Generate Personalized Prompt

Load the base template from `templates/prompt.md` and personalize it:

**Must include spec/plan/tasks awareness** so the agent reads `spec.md` and `plan.md` in full before execution, and reads only the relevant user story section from `tasks.md` for the current story.

**Base Template Location:** `templates/prompt.md`

Create a personalized `prompt.md` with:

**Section 1: Quality Gates**
```markdown
## CRITICAL: Quality Gates (Non-Negotiable)

Before marking ANY story as complete:

\`\`\`bash
# TypeScript (detected from package.json)
[actual typecheck command from package.json scripts]

# Linting (detected from package.json)
[actual lint command from package.json scripts]

# Tests (detected from package.json)
[actual test command from package.json scripts]
\`\`\`

**If ANY check fails, DO NOT mark the story as complete.**
```

**Section 2: Project-Specific Patterns** (from README/AGENTS.md)
- Monorepo structure (if applicable)
- Component locations
- Test file patterns
- Database/backend info
- Styling approach

**Section 3: TDD Workflow** (MANDATORY)
- Test-first workflow (write tests BEFORE implementation)
- Test location patterns
- Test commands
- Verification that tests FAIL before implementation

**Section 4: Routing Awareness**
- Explanation of routing metadata in prd.json
- Complexity levels (simple/medium/complex/expert)
- Cost optimization modes (free/cheap/good/genius)

**Section 5: SpecKit Workflow**
- Full workflow: specify → plan → tasks → convert → analyze → implement
- Artifact awareness: spec.md, plan.md, tasks.md, checklist.md, prd.json

**Section 6: Common Pitfalls** (from AGENTS.md/docs)
- Project-specific gotchas
- Known issues
- Best practices

**Footer:**
```markdown
---
**Personalized for [Project Name]**
**Generated:** [date]
**Re-generate:** /relentless.constitution
```

Save to: `relentless/prompt.md`

---

## Step 5: Validate & Save

Before saving:

**Constitution:**
- No `[PLACEHOLDER]` tokens remain
- All dates in ISO format (YYYY-MM-DD)
- Principles are declarative and testable
- Version format is semantic (X.Y.Z)

**Prompt:**
- All quality commands are actual commands from package.json
- File patterns match project structure
- No generic placeholders remain

Save both files:
- `relentless/constitution.md`
- `relentless/prompt.md`

---

## Step 6: Report

Output summary:
```
✓ Created constitution.md
  - Version: 1.0.0
  - Principles: [count]
  - Key rules: [summary]

✓ Created prompt.md
  - Quality gates: [count]
  - Tech stack: [detected stack]
  - Test framework: [detected]

Next steps:
1. Review both files
2. Create your first feature: /relentless.specify "feature description"
```

---

## Updating Existing Files

If `relentless/constitution.md` or `relentless/prompt.md` exist:

**For Constitution Updates:**
1. Load current version
2. Ask what needs to change
3. Increment version appropriately:
   - **MAJOR**: Breaking changes to principles
   - **MINOR**: New principles added
   - **PATCH**: Clarifications, typo fixes
4. Update `LAST_AMENDED_DATE` to today
5. Add amendment notes at top

**For Prompt Updates:**
1. Re-analyze project structure (package.json, docs)
2. Detect any new quality commands or patterns
3. Regenerate personalized sections
4. Preserve any manual customizations in comments
5. Update "Generated" date

**Both files can be regenerated at any time by running `/relentless.constitution` again.**

---

## Example Constitution Structure

```markdown
# Project Constitution

**Version:** 1.0.0  
**Ratified:** 2026-01-11  
**Last Amended:** 2026-01-11

## Principles

### Principle 1: Type Safety
**MUST:**
- All code must pass TypeScript strict mode
- No `any` types except in documented cases

**SHOULD:**
- Use Zod for runtime validation
- Prefer inference over explicit types

**Rationale:** Type safety prevents runtime errors and improves maintainability.

### Principle 2: Testing
**MUST:**
- All features must have unit tests
- CI must pass before merging

**SHOULD:**
- Aim for 80% coverage
- Write tests before implementation (TDD)

**Rationale:** Tests document behavior and prevent regressions.

## Governance

**Amendment Process:**
1. Propose changes via PR
2. Discuss with team
3. Update version semantically
4. Document rationale

**Compliance:**
- Constitution checked before each feature implementation
- Violations block PR merge
```
