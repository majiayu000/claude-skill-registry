---
name: adr-write
description: Write ADR document from discovered candidates with GitHub context research
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebFetch, Task
---

# ADR Write Command

Write ADR documents based on discovered candidates from `adr-candidates.md`.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding.

---

## Overview

Generate complete ADR documents by researching GitHub commits/PRs and applying the ADR template.

**Multi-Agent Collaboration Pipeline**:

```
┌─────────────────────────────────────────────────────────────────┐
│                    ADR Writing Pipeline                          │
├─────────────────────────────────────────────────────────────────┤
│  Phase 1: specvital-specialist                                   │
│    → Search related commits/PRs via GitHub API                   │
│    → Extract decision context and rationale                      │
│    → Identify options that were considered                       │
├─────────────────────────────────────────────────────────────────┤
│  Phase 2: product-strategist                                     │
│    → Analyze decision trade-offs                                 │
│    → Evaluate consequences (positive/negative)                   │
│    → Structure options comparison                                │
├─────────────────────────────────────────────────────────────────┤
│  Phase 3: Write ADR Documents                                    │
│    → Generate English version (docs/en/adr/)                     │
│    → Generate Korean version (docs/ko/adr/)                      │
│    → Update all required index files                             │
│    → Update sidebar configuration                                │
└─────────────────────────────────────────────────────────────────┘
```

---

## Input Interpretation

### Numeric Reference

Reference candidates by number from `adr-candidates.md`:

```bash
/adr-write 1          # Platform Level candidate #1
/adr-write core/1     # Core repository candidate #1
/adr-write worker/1   # Worker repository candidate #1
```

### Natural Language

Describe what ADR to write:

```bash
/adr-write billing and quota system
/adr-write write the AI spec document generation ADR
/adr-write domain hints extraction for core repository
```

### Parsing Logic

1. **Numeric only** (e.g., `1`, `2`): Match Platform Level candidate by number
2. **Prefixed numeric** (e.g., `core/1`, `web/2`): Match repository-level candidate
3. **Natural language**: Search candidate titles and descriptions for best match

---

## Execution Flow

### Phase 0: Load Candidate Information

Read `adr-candidates.md` and identify the target ADR:

```
1. Parse user input to identify candidate
2. Extract from adr-candidates.md:
   - Title
   - Target location (e.g., /en/adr/13-xxx.md)
   - Related repositories
   - Complexity and priority
3. Determine ADR number and file paths
```

**File Path Determination**:

| Candidate Type | English Path                         | Korean Path                          |
| -------------- | ------------------------------------ | ------------------------------------ |
| Platform Level | `docs/en/adr/{num}-{slug}.md`        | `docs/ko/adr/{num}-{slug}.md`        |
| Core           | `docs/en/adr/core/{num}-{slug}.md`   | `docs/ko/adr/core/{num}-{slug}.md`   |
| Worker         | `docs/en/adr/worker/{num}-{slug}.md` | `docs/ko/adr/worker/{num}-{slug}.md` |
| Web            | `docs/en/adr/web/{num}-{slug}.md`    | `docs/ko/adr/web/{num}-{slug}.md`    |

---

### Phase 1: Context Research (specvital-specialist)

**Task tool invocation**:

```
Task(subagent_type="specvital-specialist", prompt="""
Research GitHub context for ADR: {candidate_title}

**Target Repositories**: {related_repos}

**Research Tasks**:

1. **Search Related Commits**
   - Use gh CLI or GitHub MCP to search commits
   - Keywords: {extracted_keywords}
   - Timeframe: Last 90 days
   - Command: `gh search commits "{keyword}" --repo specvital/{repo} --limit 20`

2. **Search Related PRs**
   - Find PRs that introduced or modified this feature
   - Command: `gh pr list --repo specvital/{repo} --search "{keyword}" --state all --limit 10`

3. **Extract Decision Context**
   For each relevant commit/PR:
   - What problem was being solved?
   - What approach was taken?
   - Any alternatives mentioned in discussions?

4. **Output Format**
```

## Relevant Commits

- {commit_sha}: {message} - {date}

## Relevant PRs

- #{pr_number}: {title} - {state}

## Context Summary

- Problem: ...
- Decision: ...
- Alternatives mentioned: ...

```
""")
```

---

### Phase 2: Decision Analysis (product-strategist)

**Task tool invocation**:

```
Task(subagent_type="product-strategist", prompt="""
Analyze the architectural decision for ADR: {candidate_title}

**Input**: Context from Phase 1

**Analysis Tasks**:

1. **Structure the Context**
   - What was the problem/need?
   - Why was a decision required?
   - What constraints existed?

2. **Identify Options**
   Based on commits/PRs and common patterns:
   - Option A (selected): What was chosen and why
   - Option B: What alternatives existed
   - Option C: Any other approaches considered

3. **Evaluate Consequences**
   For the selected option:
   - Positive outcomes (benefits, improvements)
   - Negative outcomes (trade-offs, limitations)
   - Technical implications

4. **Output Format**
   Structured content ready for ADR template sections:
   - Context section content
   - Decision section content
   - Options Considered section content
   - Consequences section content
""")
```

---

### Phase 3: Write ADR Documents

Generate both English and Korean versions following the template.

**ADR Template Structure**:

```markdown
---
title: { Title }
description: ADR for {brief description}
---

# ADR-{num}: {Title}

> [Korean Version](/ko/adr/{path}) OR 🇰🇷 [한국어 버전](/ko/adr/{path})

| Date       | Author    | Repos            |
| ---------- | --------- | ---------------- |
| YYYY-MM-DD | @{author} | {repo1}, {repo2} |

## Context

{Problem situation and why a decision was needed}

## Decision

{The decision made and its rationale}

## Options Considered

### Option A: {Name} (Selected)

{Description, pros, cons}

### Option B: {Name}

{Description, pros, cons}

## Consequences

**Positive:**

- {Benefit 1}
- {Benefit 2}

**Negative:**

- {Trade-off 1}
- {Trade-off 2}

## References

- [Related ADR](/en/adr/XX-related.md)
- [Related PR](https://github.com/specvital/{repo}/pull/{num})
```

---

## Post-Write Updates (CRITICAL)

After writing ADR documents, you **MUST** update all required files per CLAUDE.md rules.

### For Platform Level ADR (e.g., `adr/13-xxx.md`)

Update **6 files**:

```
☐ docs/en/index.md           ← Homepage ADR links section
☐ docs/ko/index.md           ← Homepage ADR links section
☐ docs/en/adr/index.md       ← ADR overview
☐ docs/ko/adr/index.md       ← ADR overview
☐ docs/.vitepress/config.mts ← Sidebar navigation
```

### For Repository Level ADR (e.g., `adr/core/16-xxx.md`)

Update **6 files**:

```
☐ docs/en/index.md                 ← Homepage ADR links section
☐ docs/ko/index.md                 ← Homepage ADR links section
☐ docs/en/adr/index.md             ← ADR overview (repository section)
☐ docs/ko/adr/index.md             ← ADR overview (repository section)
☐ docs/en/adr/{category}/index.md  ← Category index
☐ docs/ko/adr/{category}/index.md  ← Category index
☐ docs/.vitepress/config.mts       ← Sidebar navigation
```

---

## Language Rules

### English Version (`/en/`)

- Write entirely in English
- Use technical terminology appropriately
- Clear, concise prose

### Korean Version (`/ko/`)

- Write entirely in Korean
- **MUST use noun-ending style** (명사형 종결)
- **NEVER use verb-ending style** (동사 종결어미 금지)

**Korean Style Examples**:

| ✅ Correct                   | ❌ Incorrect                         |
| ---------------------------- | ------------------------------------ |
| 데이터 무결성 검증           | 데이터 무결성을 검증합니다           |
| API 호출 최소화              | API 호출이 최소화됩니다              |
| 정적 분석 기반 테스트 카운트 | 정적 분석을 통해 테스트를 카운트한다 |

---

## Key Rules

### Must Do

- Load candidate info from `adr-candidates.md`
- Research actual GitHub commits/PRs for context
- Follow ADR template structure exactly
- Generate both English and Korean versions
- Update ALL required index files (check CLAUDE.md for complete list)
- Update sidebar in `config.mts`
- Use noun-ending style for Korean

### Must Not Do

- Skip GitHub research (must base on actual commits)
- Write only one language version
- Forget to update index files
- Use verb endings in Korean documents
- Guess content without evidence from commits/PRs

---

## Output Summary

After completion, report:

```
## ADR Written

| Item | Value |
|------|-------|
| Title | {ADR Title} |
| Number | ADR-{num} |
| English | docs/en/adr/{path} |
| Korean | docs/ko/adr/{path} |

## Files Updated

- [x] docs/en/adr/{path} (created)
- [x] docs/ko/adr/{path} (created)
- [x] docs/en/index.md
- [x] docs/ko/index.md
- [x] docs/en/adr/index.md
- [x] docs/ko/adr/index.md
- [x] docs/.vitepress/config.mts

## Source References

- {commit_sha}: {message}
- PR #{num}: {title}
```

---

## Usage Examples

```bash
# Write Platform Level candidate #1 (Billing and Quota)
/adr-write 1

# Write Core repository candidate #1
/adr-write core/1

# Natural language - matches "AI-Based Spec Document Generation Pipeline"
/adr-write AI spec generation

# Natural language with context
/adr-write write the billing ADR, focus on quota tracking aspects
```

---

## Related Commands

- `/adr-discover`: Discover ADR candidates
- `/document-business-rule`: Business rule documentation
- `/commit`: Commit message generation

## Related Agents

- `specvital-specialist`: GitHub context research
- `product-strategist`: Decision analysis and trade-offs
- `prompt-engineer`: Document quality optimization
- `claude-code-specialist`: Command and workflow optimization

---

## Execution

Now execute the workflow:

1. **Parse $ARGUMENTS**: Identify target candidate from `adr-candidates.md`
2. **Phase 1**: Invoke Task(specvital-specialist) for GitHub research
3. **Phase 2**: Invoke Task(product-strategist) for decision analysis
4. **Phase 3**: Write ADR documents (English + Korean)
5. **Update Index Files**: Per CLAUDE.md requirements
6. **Report**: Summary of created/updated files
