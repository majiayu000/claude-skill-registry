---
name: update-docs
description: Update documentation based on codebase changes. Use when documentation needs updates after code changes, or to ensure docs stay accurate.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - Edit
  - Write
  - WebSearch
user-invocable: true
---

# Update Docs

## Purpose

Update documentation based on codebase changes, ensuring docs stay accurate and complete.

## When to Use

- After code changes that affect documentation
- When documentation is out of sync with code
- To ensure docs stay accurate after refactoring
- When new features need documentation

## Agent Delegation

Documentation updates are delegated to the **Technical Writer agent** for accuracy and clarity expertise.

### Flow

```
Coordinator → Spawn Technical Writer "update docs for scope X" → Writer analyzes & proposes → User approves → Writer applies
```

### How It Works

| Step | Actor            | Action                                             |
| ---- | ---------------- | -------------------------------------------------- |
| 1    | Coordinator      | Detects scope (recent changes / path / full audit) |
| 2    | Coordinator      | Spawns Technical Writer agent with scope           |
| 3    | Technical Writer | Analyzes changes, discovers affected docs          |
| 4    | Technical Writer | Compares docs against code, identifies issues      |
| 5    | Technical Writer | Proposes updates with prioritization               |
| 6    | User             | Reviews and approves/rejects proposed changes      |
| 7    | Technical Writer | Applies approved changes                           |

### Technical Writer Task Prompt Template

```
Update documentation based on codebase changes.

## Scope
{scope description - recent changes / specific path / full audit}

## Instructions
1. Read the update-docs skill at `.claude/skills/update-docs/SKILL.md`
2. Follow the workflow phases (analyze → discover → compare → propose → apply)
3. Use dynamic discovery, not hardcoded mappings
4. Prioritize: Critical (incorrect) > High (missing APIs) > Medium (examples) > Low (wording)
5. Ask for user confirmation before applying changes
```

## Workflow

### Phase 1: Analyze Changes

1. **Check recent git changes:**

   ```bash
   git diff --name-only HEAD~5
   git diff --stat
   ```

2. **Identify what changed:**
   - Which directories/packages were affected?
   - What type of changes? (new files, modifications, deletions)
   - Any new patterns or APIs introduced?

3. **Ask clarifying questions** if scope is unclear

### Phase 2: Discover Affected Documentation

**Use dynamic discovery, not hardcoded mappings.**

1. **Find nearby CLAUDE.md files:**

   ```bash
   # For each changed directory, look for CLAUDE.md
   find {changed_directory} -name "CLAUDE.md" -type f
   ```

2. **Search rules for mentions:**

   ```bash
   # Search rules that might reference changed areas
   grep -l "{changed_area}" .claude/rules/*.md
   ```

3. **Check root CLAUDE.md** if changes affect:
   - Commands (`.claude/commands/`)
   - Rules (`.claude/rules/`)
   - Agents (`.claude/agents/`)
   - Skills (`.claude/skills/`)
   - Project structure

4. **Common discovery patterns:**

   | Change Type     | Where to Search                                           |
   | --------------- | --------------------------------------------------------- |
   | Package code    | Package's CLAUDE.md, grep rules for package name          |
   | Components      | Grep rules for "component", check testing/storybook rules |
   | Tokens          | Grep rules for "token", check related packages            |
   | Commands/Agents | Root CLAUDE.md slash commands table                       |
   | New patterns    | Grep rules for pattern keywords                           |

### Phase 3: Review and Compare

For each discovered documentation file:

1. **Read the current documentation**
2. **Compare against actual code** to identify:
   - Outdated information
   - Missing documentation for new features
   - Examples that no longer work
   - Incorrect paths or references

3. **Prioritize changes:**
   - **Critical:** Incorrect information
   - **High:** Missing documentation for public APIs
   - **Medium:** Missing examples
   - **Low:** Minor wording improvements

### Phase 4: Propose Updates

For each documentation file that needs changes:

```markdown
### {filename}

**Current:** {what it says}

**Actual:** {what the code does}

**Proposed change:** {specific edit}
```

### Phase 5: Confirm and Apply

1. **Present all proposed changes** to user
2. **Ask for confirmation:** "Apply these changes? (all / select / none)"
3. **Apply approved changes** using Edit tool
4. **Verify changes** are correct

## Output Format

```markdown
## Documentation Updates

### Files Analyzed

- {list of doc files checked}

### Changes Made

| File | Change | Status  |
| ---- | ------ | ------- |
| ...  | ...    | Applied |

### Verification

- [ ] All changes applied
- [ ] Links still work
- [ ] Examples are accurate
```

## Key Principle

**Discover, don't assume.** The codebase structure evolves. Instead of maintaining hardcoded mappings that get stale, use search and discovery to find what documentation exists and what might need updates.
