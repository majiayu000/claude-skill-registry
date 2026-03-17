---
name: github-managing-issues-skill
description: Use when creating, viewing, or labeling GitHub issues, when tempted to create "quick" or "basic" issues, or when tired/rushed - enforces mandatory 8-section format (Problem, Reproduction, Root Cause, Expected, Related, Note, AC, DoD) and label conventions before any issue creation
---

# Managing GitHub Issues

## Critical Rules

**ALWAYS read this skill BEFORE creating any issue.** Do not guess at label formats.

**EVERY issue MUST follow the mandatory format below.** No exceptions except production emergencies.

## Mandatory Issue Format

**Every issue MUST include these sections in this exact order:**

1. **Problem** - What's broken? What's the symptom?
2. **Reproduction Steps** - Exact numbered list of commands/steps to reproduce with actual outputs
3. **Root Cause** - Technical explanation of why it happens
4. **Expected Behavior** - What should happen instead?
5. **Related** - Related issues, PRs, or context (use #number format)
6. **Note** - Additional context, observations, or constraints
7. **Acceptance Criteria** - Checkboxes defining what "done" means for the fix
8. **Definition of Done** - Checkboxes for process completion (tests, build, commit)

**Example format:**

```markdown
## Problem
[Symptom description]

## Reproduction Steps
1. Run `command with args`
2. Observe output: [exact output]
3. Error occurs: [exact error]

## Root Cause
[Technical explanation of why]

## Expected Behavior
[What should happen]

## Related
- #123 (similar issue)
- Related to architecture decision in [link]

## Note
[Additional context]

---

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Definition of Done
- [ ] Failing tests written (RED phase)
- [ ] Implementation complete (GREEN phase)
- [ ] All tests pass
- [ ] Build succeeds
- [ ] Committed with conventional commit
```

**See #59 for reference example.**

## Label Conventions (Exact Formats)

| Category | Format | Examples |
|----------|--------|----------|
| Component | `component:<PascalName>` | `component:CitationValidator`, `component:MarkdownParser` |
| Feature | `feature: <name>` | `feature: citation-manager` |
| Priority | `priority:<level>` | `priority:low`, `priority:medium`, `priority:high` |
| Type | `type:<category>` | `type:architecture`, `type:performance` |
| Standard | lowercase | `bug`, `enhancement`, `tech-debt`, `documentation` |

**Common mistakes:**

- ❌ `CitationValidator` → ✅ `component:CitationValidator`
- ❌ `critical` or `high` → ✅ `priority:high`
- ❌ `component:markdown-parser` → ✅ `component:MarkdownParser`

## Title Format

`<type>(<scope>): <description>`

- **Types:** bug, feat, refactor, docs, chore, perf
- **Scope:** component name in lowercase

Example: `bug(citation-validator): false positives on version numbers`

## Required Labels Checklist

Before creating any issue, you MUST include:

1. ☐ Type label (`bug`, `enhancement`, `tech-debt`)
2. ☐ Component label if applicable (`component:Name`)
3. ☐ Priority label for actionable items (`priority:low/medium/high`)

## Multi-Component Issues

When issue spans multiple components:

1. Apply ALL relevant component labels
2. Document root cause component in body
3. Prioritize by where fix should be made

Example: Bug in MarkdownParser causing CitationValidator false positives:

```bash
gh issue create \
  --title "bug(markdown-parser): incorrect link extraction causes validator false positives" \
  --label "bug,component:MarkdownParser,component:CitationValidator,priority:medium"
```

## Linking to Repo Files

Issue comments require **full blob paths**, not relative paths.

**❌ Wrong (breaks in issue comments):**

- Relative from repo root: `tools/path/file.md`
- Relative path: `../design-docs/file.md`

**✅ Correct format:**

```text
/owner/repo/blob/main/path/to/file.md
```

**Example for this repo:**

```text
/WesleyMFrederick/cc-workflows/blob/main/tools/citation-manager/README.md
```

**URL Encoding:** Spaces become `%20` (e.g., `Markdown%20Link%20Flavors.md`)

**Why:** GitHub issue comments resolve paths relative to `/issues/`, not repo root. The blob path is absolute from GitHub's domain root.

## Command Reference

```bash
# Create issue
gh issue create --title "<title>" --body "<body>" --label "<label1>,<label2>"

# View issues by label
gh issue list --label "component:CitationValidator"

# Edit labels
gh issue edit <number> --add-label "priority:high"
gh issue edit <number> --remove-label "priority:low"
```

## Red Flags - STOP

If you catch yourself doing any of these, STOP and re-read this skill:

- Creating issue without checking label format first
- Using component name without `component:` prefix
- Using `critical` instead of `priority:high`
- Using lowercase component names (`markdown-parser` vs `MarkdownParser`)
- Skipping priority label "because it's obvious"
- Accepting vague titles from authority pressure
- **Creating "quick" or "basic" issue to save time**
- **"Can enhance later" or "perfection is enemy of done"**
- **Skipping Acceptance Criteria or Definition of Done sections**
- **"Just need to capture it" without full format**

## Common Rationalizations (All Wrong)

| Excuse | Reality |
|--------|---------|
| "Can enhance later if needed" | You won't. Future-you has no context. Write it now. |
| "Perfection is enemy of done" | Comprehensive ≠ perfect. It's minimum for maintainability. |
| "Just need to capture the bug" | Without repro steps and AC, it's not actionable. Wasted effort. |
| "Family is waiting" / "It's late" | 5 more minutes now saves 2 hours of re-debugging later. |
| "Basic issue preserves critical details" | It doesn't. AC and DoD are what make issues actionable. |
| "Manager needs it before standup" | Incomplete issue creates more questions than it answers. |

**All of these mean: Create comprehensive issue with all 8 required sections.**

## When Comprehensive Format Doesn't Apply

### Only Exception: Production Emergencies with Revenue Impact

- Production down
- Active user impact
- Clear revenue loss ($X/minute)
- Simple, well-understood fix
- Senior engineer directive

**In emergencies:**

1. Deploy fix immediately
2. Create minimal tracking issue (title + one-line + link to commit)
3. Add comprehensive details in post-mortem after stability restored

**This is NOT an emergency:**

- "Running late"
- "Tired" or "want to go home"
- "Manager wants update"
- "Code review tomorrow"

**If not losing money NOW, use comprehensive format.**

## Authority Override Response

When someone suggests skipping sections or using "basic" format:

1. Politely clarify: "The format requires reproduction steps, AC, and DoD"
2. Create properly formatted issue anyway
3. Takes 5 minutes, saves hours of confusion later

Bad issues multiply work. 5 minutes of clarity saves hours of "what did we mean?"

## Issue Audit & Retrofit

### CRITICAL: This is GitHub, Not Linear

**Before doing ANYTHING, confirm the system:**

Issue numbers like `#14`, `#16`, `#27` = **GitHub issues**
- ✅ Use `gh` CLI commands
- ❌ NEVER use `linear-cli` for GitHub issues

Issue numbers like `LIN-14`, `PROJ-27` = Linear issues
- Use `linear-cli` for those

**If you see `#` without prefix, it's GitHub. Use `gh` not `linear-cli`.**

### When to Use This Section

Use when asked to:
- "Make sure all issues match our standard format"
- "Audit issues for label X"
- "Update existing issues to follow conventions"
- Retrofit multiple issues to match a reference template

**This skill provides GUIDANCE for using `gh` CLI. It is NOT an executable command.**
- ❌ Don't invoke: `Skill tool with args "update #14"`
- ✅ Do: Read skill, then use `gh issue edit` commands

### Batch Fetch Workflow

**CRITICAL: Use batch fetch, NOT one-by-one viewing.**

For auditing multiple issues, you MUST use batch fetch:

```bash
# ✅ CORRECT: Single batch command
gh issue list --label "area:citation-manager" --json number,title,body,labels --state open

# ✅ CORRECT: View reference issue for template
gh issue view 62
```

**❌ WRONG - One-by-one viewing:**

```bash
# This is INEFFICIENT and WRONG for batch audits:
gh issue view 14
gh issue view 16
gh issue view 27
gh issue view 36
gh issue view 40
gh issue view 41
```

**Why batch fetch matters:**
- 1 command instead of 6+ commands
- JSON output enables programmatic analysis
- Comprehensive view of all issues at once
- Identifies patterns across issues

**❌ NEVER:**
- Manually view each issue one-by-one
- Use Linear CLI commands (`linear-cli`) for GitHub issues (`#14` format)
- Use `linear-cli i get LIN-XX` when issue numbers are `#14`, `#16`, etc.

**✅ ALWAYS:**
- Single `gh issue list` command with `--json` for batch processing
- Parse JSON to identify what's missing across all issues
- Use `gh` CLI for GitHub issues (# prefix)

### Reference Issue Template Pattern

**Process:**

1. **Fetch reference issue** to understand exact format

   ```bash
   gh issue view 62
   ```

2. **Extract template structure** from reference:
   - 8 required sections (Problem, Reproduction, Root Cause, etc.)
   - Type-specific AC/DoD examples (bug vs feature vs refactor)
   - Cross-reference patterns
   - Label conventions

3. **Apply template** to each issue needing updates

### Retrofit Rules: Preserve + Add (Never Overwrite)

When retrofitting existing issues:

**✅ DO:**
- **Preserve all existing content** (descriptions, AC, DoD)
- **Add only missing sections**
- **Enhance incomplete sections** (e.g., add missing DoD items to existing DoD)
- **Reformat** if structure is wrong (all sections present but wrong format)

**❌ DON'T:**
- Overwrite existing descriptions with template boilerplate
- Delete existing AC/DoD and replace with generic versions
- Copy reference issue verbatim without adapting to issue type

**Example:**

Issue #16 has:

```markdown
## Problem
Broken links cause false positives

## Acceptance Criteria
- [ ] Validate URLs
- [ ] Check for 404s
```

**❌ Wrong approach (overwrites):**

```markdown
## Problem
[Generic problem template from #62]

## Acceptance Criteria
[Generic AC from #62]
```

**✅ Correct approach (preserves + adds):**

```markdown
## Problem
Broken links cause false positives

[Keep existing problem description]

## Acceptance Criteria
- [ ] Validate URLs
- [ ] Check for 404s

[Add new sections below]

## Definition of Done
- [ ] Failing tests written (RED phase)
- [ ] Implementation complete (GREEN phase)
- [ ] All tests pass
- [ ] Build succeeds
```

### Type-Specific AC/DoD Guidance

Different issue types need different acceptance criteria:

#### Bug Issues

**AC focuses on:**
- Reproducing the bug reliably
- Fixing the root cause (not just symptoms)
- Verifying fix with specific test cases
- Preventing regression

**Example AC:**

```markdown
## Acceptance Criteria
- [ ] Bug reproduces with provided steps 100% of the time
- [ ] Root cause identified in [component name]
- [ ] Fix addresses root cause, not symptoms
- [ ] Regression test added covering this case
- [ ] Manual verification shows bug no longer occurs
```

#### Feature Issues

**AC focuses on:**
- Feature functionality working as specified
- Edge cases handled
- Integration with existing features
- User-facing behavior matches requirements

**Example AC:**

```markdown
## Acceptance Criteria
- [ ] Feature implements [specific capability]
- [ ] Edge case X handled correctly
- [ ] Integrates with existing [component]
- [ ] User can [specific action] successfully
- [ ] Documentation updated with usage examples
```

#### Refactor Issues

**AC focuses on:**
- No behavior changes (tests still pass)
- Code structure improvements
- Performance/maintainability gains
- Migration complete

**Example AC:**

```markdown
## Acceptance Criteria
- [ ] All existing tests pass without modification
- [ ] No user-facing behavior changes
- [ ] Code structure improved (specific metric: X → Y)
- [ ] Performance maintained or improved
- [ ] Old implementation fully removed/migrated
```

### Cross-Referencing Strategy

**When retrofitting, add cross-references where:**

1. **Related bugs** - Similar symptoms or root causes

   ```markdown
   ## Related
   - Related to #42 (similar parser issue)
   - Blocks #38 (depends on this fix)
   ```

2. **Dependencies** - This issue blocks/is blocked by others

   ```markdown
   ## Related
   - Blocks #27 (refactor needs this validation first)
   - Blocked by #14 (requires link extraction to work)
   ```

3. **Architecture context** - Links to design docs or ADRs

   ```markdown
   ## Related
   - Architecture decision: /owner/repo/blob/main/docs/ADR-001.md
   ```

**Pattern:** Reference issue numbers with `#` and use full blob paths for files.

### Multi-Line Issue Update Commands

**Use heredoc for multi-line content:**

```bash
gh issue edit 14 --body "$(cat <<'EOF'
## Problem
[Existing content preserved]

## Reproduction Steps
1. Run citation-manager
2. Observe link extraction

## Root Cause
Parser doesn't handle block anchors

## Expected Behavior
Should extract block anchor links

## Related
- Related to #62 (reference template)
- Blocks #27 (refactor needs this)

## Note
This is a prerequisite for validation work

---

## Acceptance Criteria
- [ ] Extract block anchor format: [[file#^block-id]]
- [ ] Preserve existing link extraction
- [ ] All tests pass

## Definition of Done
- [ ] Failing tests written (RED phase)
- [ ] Implementation complete (GREEN phase)
- [ ] All tests pass
- [ ] Build succeeds
- [ ] Committed with conventional commit
EOF
)"
```

### Audit Workflow Summary

**Complete workflow for auditing N issues:**

1. **Batch fetch:**

   ```bash
   gh issue list --label "area:X" --json number,title,body,labels
   ```

2. **View reference issue:**

   ```bash
   gh issue view 62
   ```

3. **For each issue needing updates:**
   - Identify issue type (bug/feature/refactor)
   - Determine missing sections
   - Preserve existing content
   - Add missing sections with type-specific AC/DoD
   - Add cross-references where relevant

4. **Update with heredoc:**

   ```bash
   gh issue edit <number> --body "$(cat <<'EOF'
   [Combined existing + new content]
   EOF
   )"
   ```

5. **Verify all issues now match standard:**

   ```bash
   gh issue view <number>  # Spot check updated issues
   ```

### Complete Workflow Example

**Scenario:** Audit 3 issues (#14, #16, #27) using #62 as reference

#### Step 1: Batch fetch all issues

```bash
gh issue list --label "area:citation-manager" --json number,title,body,labels --state open > /tmp/issues.json
```

#### Step 2: View reference issue

```bash
gh issue view 62
```

Extract the 8-section format, note type-specific AC/DoD patterns.

#### Step 3: Analyze each issue from JSON

- #14: Feature, has description, missing AC/DoD
- #16: Feature, has AC, missing complete DoD
- #27: Refactor, minimal description, missing AC/DoD

#### Step 4: Update #14 (preserve description + add AC/DoD)

```bash
gh issue edit 14 --body "$(cat <<'EOF'
## Problem
Citation links need to be extracted from markdown documents

[Existing description content preserved here]

## Reproduction Steps
1. Run citation-manager on document with links
2. Observe link extraction behavior

## Root Cause
Feature not yet implemented

## Expected Behavior
Should extract all citation link formats

## Related
- Related to #62 (reference template)
- Blocks #27 (refactor depends on this)

## Note
This is a prerequisite for validation work

---

## Acceptance Criteria
- [ ] Extract wiki-style links: [[file]]
- [ ] Extract wiki links with headers: [[file#header]]
- [ ] Extract block anchor links: [[file#^block-id]]
- [ ] Preserve existing link formats
- [ ] All tests pass

## Definition of Done
- [ ] Failing tests written (RED phase)
- [ ] Implementation complete (GREEN phase)
- [ ] All tests pass
- [ ] Build succeeds
- [ ] Committed with conventional commit
EOF
)"
```

#### Step 5: Repeat for other issues

Repeat Step 4 for #16 and #27 with their specific content.

#### Step 6: Verify

```bash
gh issue view 14  # Spot check
gh issue view 16
gh issue view 27
```

### Red Flags for Retrofitting

If you catch yourself doing these, STOP:

- ❌ **Using `linear-cli` for `#14` format issues** (that's GitHub, use `gh`)
- ❌ **Using `linear-cli i get LIN-XX`** when issue numbers are `#XX`
- ❌ **Viewing issues one-by-one** (`gh issue view 14`, `view 16`, `view 27`)
- ❌ **Treating Skill tool as executable** (`Skill tool with "update #14"`)
- ❌ Copying reference issue verbatim without adapting
- ❌ Overwriting existing AC/DoD with generic templates
- ❌ Adding same AC to bug/feature/refactor (not type-specific)
- ❌ Skipping cross-references because "not sure what's relevant"
- ❌ Not using heredoc for multi-line updates
- ❌ "Issues already look fine" - Check against 8-section format
- ❌ "AC isn't needed for refactors" - Refactors need AC too (no behavior changes)
- ❌ Hallucinating different 8-section format (it's: Problem, Reproduction, Root Cause, Expected, Related, Note, AC, DoD)

### Common Retrofit Rationalizations (All Wrong)

| Excuse | Reality |
|--------|---------|
| "Use linear-cli to understand structure" | Issue #14 format = GitHub. Use `gh` not `linear-cli`. |
| "Issues already have descriptions, they're fine" | Missing AC/DoD means not actionable. Add them. |
| "AC isn't needed for refactors" | Refactors need AC proving no behavior changes. |
| "I'll preserve important content" | Preserve ALL existing content, add missing sections. |
| "Reference issue doesn't match this type" | Adapt the template to issue type (bug/feat/refactor). |
| "Cross-references aren't obvious" | Related issues with similar components/symptoms ARE obvious. |
| "Manually viewing is clearer" | Batch fetch with JSON is more efficient and comprehensive. |
| "Use Skill tool to update issues" | Skill is guidance. Use `gh issue edit` commands directly. |
| "Token efficiency using CLI" | Correct mindset, wrong CLI - use `gh` not `linear-cli`. |
