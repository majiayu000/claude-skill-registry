---
description: Audit a skill against Anthropic skill-creator standards
argument-hint: <skill-name-or-path>
---

# /local:audit-skill

Audit a skill against the Anthropic skill-creator standards and provide structured recommendations for improvement.

## Usage

```bash
# By skill name (looks in .claude/skills/)
/local:audit-skill dignified-python

# By file path
/local:audit-skill /path/to/skill/SKILL.md
```

---

## Agent Instructions

Execute the skill audit workflow following these phases carefully.

### Phase 1: Resolve Target Skill

Determine the skill to audit based on the argument provided: `$ARGUMENTS`

**Resolution logic:**

1. If the argument contains `/`, treat it as a file path
   - If it ends with `SKILL.md`, use the parent directory
   - Otherwise, assume it's the skill directory and look for `SKILL.md` inside
2. If the argument does not contain `/`, treat it as a skill name
   - Look for `.claude/skills/<skill-name>/SKILL.md`

**Validation:**

- Confirm the resolved path exists
- If not found, display an error message and stop:
  ```
  Error: Skill not found at <resolved-path>
  ```

### Phase 2: Fetch Standards from GitHub

Fetch the authoritative skill-creator standards from Anthropic's GitHub repository.

**Step 2.1: Discover repository structure**

Use WebFetch to browse the skill-creator directory and discover all available files:

1. `https://github.com/anthropics/skills/tree/main/skills/skill-creator`
   - Prompt: "List all files and directories in this skill-creator folder"

2. For each subdirectory found (e.g., `references/`, `scripts/`), fetch its contents:
   - `https://github.com/anthropics/skills/tree/main/skills/skill-creator/<subdir>`
   - Prompt: "List all files in this directory"

**Step 2.2: Fetch discovered files**

For each `.md` file discovered, fetch its contents using raw URLs:

- Base URL: `https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/`
- Example: For `SKILL.md` → `https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md`
- Example: For `references/output-patterns.md` → `https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/references/output-patterns.md`

Use prompts that extract the relevant guidance from each file.

**Error handling:**

- If directory listing fails, fall back to known files: `SKILL.md`, `references/output-patterns.md`, `references/workflows.md`
- If any file fetch fails, note it and continue with available standards
- At minimum, the main SKILL.md must be fetched successfully

### Phase 3: Read Target Skill

**3.1 Read the SKILL.md file:**

- Use Read tool to get the full content of the target skill's SKILL.md

**3.2 List directory contents:**

- Use Bash to list the skill directory structure
- Identify what exists in `scripts/`, `references/`, `assets/`

**3.3 Read bundled resources:**

- Read files in `references/` to understand what documentation is bundled
- Note scripts and assets without reading them fully (just note their presence)

### Phase 4: Analyze Against Standards

Evaluate the skill against these criteria based on the fetched standards:

#### 4.1 Frontmatter Quality

| Check               | Criteria                                                                          |
| ------------------- | --------------------------------------------------------------------------------- |
| `name` field        | Exists and matches directory name                                                 |
| `description` field | Explains what the skill does AND when to use it                                   |
| Third person        | Description uses "This skill should be used when..." not "Use this skill when..." |

#### 4.2 Structure

| Check              | Criteria                                       |
| ------------------ | ---------------------------------------------- |
| SKILL.md size      | Less than 5,000 words (progressive disclosure) |
| No README          | No README.md or other auxiliary top-level docs |
| Clean organization | Bundled resources in proper directories        |

#### 4.3 Writing Style

| Check            | Criteria                          |
| ---------------- | --------------------------------- |
| Imperative form  | Uses "Do X" not "You should do X" |
| Verb-first       | Instructions start with verbs     |
| Concise          | No unnecessary verbosity          |
| No second person | Avoids "you" in instructions      |

#### 4.4 Progressive Disclosure

| Check                 | Criteria                                           |
| --------------------- | -------------------------------------------------- |
| Core in SKILL.md      | Essential workflow is in main file                 |
| Details in references | Detailed information moved to `references/`        |
| No duplication        | Information lives in one place only                |
| Size appropriate      | SKILL.md < 5k words, references for larger content |

#### 4.5 Resource Organization

| Check             | Criteria                                    |
| ----------------- | ------------------------------------------- |
| scripts/          | Executable code for deterministic tasks     |
| references/       | Documentation loaded into context as needed |
| assets/           | Output files (templates, images, fonts)     |
| Proper separation | Each file in correct directory type         |

#### 4.6 Local Conventions (erk-specific)

These are project-specific conventions that differ from or extend Anthropic's standards:

| Check               | Criteria                                                                                                   |
| ------------------- | ---------------------------------------------------------------------------------------------------------- |
| No embedded scripts | Skills MUST NOT have a `scripts/` directory; use `erk exec` commands instead                               |
| erk exec pattern    | Executable logic lives in `src/erk/cli/commands/exec/scripts/` and is invoked via `erk exec <script-name>` |

**Rationale:** Centralizing scripts in `erk exec` provides:

- Single location for all executable scripts
- Consistent CLI interface (`erk exec <name>`)
- Easier testing and maintenance
- No need to discover/read scripts from skill directories

### Phase 5: Generate Report

Present the audit findings in this structured format:

```markdown
## Skill Audit: <skill-name>

### Summary

[1-2 sentence overview of skill health and main areas for improvement]

### Compliance Scorecard

| Criterion              | Status         | Notes               |
| ---------------------- | -------------- | ------------------- |
| Frontmatter            | PASS/WARN/FAIL | [Brief explanation] |
| Structure              | PASS/WARN/FAIL | [Brief explanation] |
| Writing Style          | PASS/WARN/FAIL | [Brief explanation] |
| Progressive Disclosure | PASS/WARN/FAIL | [Brief explanation] |
| Resource Organization  | PASS/WARN/FAIL | [Brief explanation] |
| Local Conventions      | PASS/WARN/FAIL | [Brief explanation] |

### Recommendations

[Numbered list of specific, actionable recommendations ordered by priority]

1. [Most critical issue and how to fix it]
2. [Second priority item]
   ...

### Detailed Findings

#### Frontmatter

[Expanded analysis]

#### Structure

[Expanded analysis]

#### Writing Style

[Specific examples of issues if any]

#### Progressive Disclosure

[Analysis of information organization]

#### Resource Organization

[Analysis of bundled resources]

#### Local Conventions

[Analysis of erk-specific patterns: no scripts/ directory, erk exec usage]
```

**Status definitions:**

- **PASS**: Fully compliant with standards
- **WARN**: Minor issues or room for improvement
- **FAIL**: Does not meet standards, needs correction

### Key Principles

1. **Be specific** - Cite exact lines or sections when identifying issues
2. **Be actionable** - Every recommendation should be implementable
3. **Prioritize** - Order recommendations by impact
4. **Be fair** - Acknowledge what the skill does well
5. **Reference standards** - Connect findings back to the fetched standards
