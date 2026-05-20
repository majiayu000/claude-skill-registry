---
name: gather-code-examples
description: Generate code example checklists for Developer Documentation lessons based on readiness assessment.
license: MIT
metadata:
  author: Andamio
  version: 1.0.0
---

# Skill: Gather Code Examples

## Description

Generates a structured code example checklist from a course's readiness assessment. Used during Phase 6 (Gather Context) of the course workflow to prepare assets for Developer Documentation lessons.

## When to Use

- After `/self-assess-readiness` identifies Developer Documentation SLTs as "Needs Context"
- When the Context Shopping List includes code examples or API references
- Before building Developer Documentation lessons

## Invocation

```
/gather-code-examples                           # Interactive: asks which course
/gather-code-examples andamio-for-api-developers  # Specify course
```

## Instructions

### 1. Identify Course

If no course specified, scan `courses-in-progress/` and ask which course to generate checklist for.

### 2. Read Readiness Assessment

Read `04-readiness-assessment.md` to identify:
- Which SLTs are "Needs Context" or "Needs Human"
- Which of those are Developer Documentation lesson type (cross-reference with `03-lesson-type-classification.md`)
- What specific code examples are needed (from Gap Analysis sections)
- What API references or docs are needed

### 3. Read Course Outline

Read `00-course.md` to get:
- Lesson focus for each SLT (what code patterns to demonstrate)
- Lesson inputs specified (what examples were already anticipated)
- Any specific libraries, frameworks, or APIs mentioned

### 4. Generate Checklist

Create `assets/code-examples/README.md` with:

```markdown
# Code Example Checklist: [Course Name]

**Generated from:** `04-readiness-assessment.md`
**Primary language:** [language]
**Key libraries:** [list]
**Last updated:** [date]

## Environment Requirements

- **Language version:** [e.g., Go 1.21+, Node 18+]
- **Required packages:** [list with versions if known]
- **Test environment:** [e.g., Cardano preprod, local devnet]

## Naming Convention

```
[slt-number]-[example-name].[ext]
```

## Checklist

### SLT [X.Y]: [SLT text]

| # | Filename | What to Demonstrate | Status |
|---|----------|---------------------|--------|
| 1 | `X.Y-example-name.go` | [specific code pattern] | [ ] |

**Code requirements:**
- [ ] Compiles without errors
- [ ] Runs against [test environment]
- [ ] Includes comments explaining key steps
- [ ] Error handling demonstrated

**API references needed:**
- [ ] [specific API doc or function signature]

**Verification:**
- [ ] Output matches expected result
- [ ] Tested on [date] against [environment]

---

[Repeat for each Developer Documentation SLT]

## Summary

| SLT | Examples Needed | Verified | Notes |
|-----|-----------------|----------|-------|
| X.Y | [count] | 0 | [brief note] |

**Total:** [n] code examples

## API Documentation Links

| Library | Doc URL | Version | Status |
|---------|---------|---------|--------|
| [name] | [url] | [version] | [ ] Verified current |

## Gathering Session Notes

_Use this space to record observations:_

- Date:
- Tester:
- Environment version:
- Issues encountered:
```

### 5. Create Directory Structure

Ensure `assets/code-examples/` directory exists:

```
courses-in-progress/[course-slug]/
  assets/
    code-examples/
      README.md           # The checklist
      1.2-api-auth.ts     # Example files
      2.1-query-courses.ts
      ...
```

### 6. Output Summary

After generating, report:

```markdown
## Code Example Checklist Generated

**Course:** [name]
**Location:** `assets/code-examples/README.md`

| SLT | Example | Language | Dependencies |
|-----|---------|----------|--------------|
| X.Y | [name] | [lang] | [libs] |

**Total:** [n] examples across [m] SLTs

### Dependency Tiers

| Tier | SLTs | What's Needed | Est. Effort |
|------|------|---------------|-------------|
| 1: Standalone | [list] | Language + standard lib only | Low |
| 2: External API | [list] | API key + network access | Medium |
| 3: On-chain | [list] | Test wallet + test ADA | Higher |

**Next step:** Verify API docs are current, then write Tier 1 examples.
```

## Naming Convention

### Format

```
[slt]-[example-name].[ext]
```

### Parts

| Part | Format | Example | Purpose |
|------|--------|---------|---------|
| `slt` | `X.Y` | `1.2` | SLT number |
| `example-name` | `kebab-case` | `api-auth` | What the example demonstrates |
| `ext` | language extension | `.ts`, `.go`, `.py` | File type |

### Examples

| Filename | Description |
|----------|-------------|
| `1.2-api-auth.ts` | Authentication example |
| `2.1-query-courses.ts` | Querying course data |
| `3.1-build-transaction.go` | Building unsigned transaction |
| `3.2-sign-submit.go` | Signing and submitting |

## Code Quality Requirements

Every code example must:

### 1. Compile/Run
- No syntax errors
- All imports resolve
- Runs without runtime errors (on valid input)

### 2. Be Complete
- Self-contained (can copy-paste and run)
- Includes necessary imports
- Shows setup and teardown if needed

### 3. Be Documented
- Comments explain "why" not just "what"
- Key steps are labeled
- Expected output is shown (in comments or separate file)

### 4. Handle Errors
- Shows error handling pattern
- Doesn't silently fail
- Demonstrates realistic error cases

### 5. Be Verified
- Tested against stated environment
- Output captured and compared
- Date of last verification recorded

## Verification Template

For each example, record:

```markdown
### Verification: [filename]

- **Tested:** [date]
- **Environment:** [language version, library versions]
- **Test network:** [preprod/mainnet/local]
- **Result:** Pass / Fail
- **Output:**
  ```
  [actual output]
  ```
- **Notes:** [any observations]
```

## Common Example Types

| Type | Purpose | Template Pattern |
|------|---------|------------------|
| **Auth** | Authenticate with API | Setup credentials → make auth call → store token |
| **Query** | Fetch data | Auth → build query → handle response → parse data |
| **Transaction** | Build/submit tx | Auth → build unsigned → sign → submit → confirm |
| **CRUD** | Create/Read/Update/Delete | Auth → operation → verify result |
| **Webhook** | Handle callbacks | Setup server → register webhook → handle event |

## Guidelines

- **One checklist per course** — Don't split across files
- **Working code only** — Never include code that doesn't run
- **Version pin dependencies** — Record exact versions tested
- **Test before lesson** — Verify examples work before writing lesson content
- **Update on API changes** — Re-verify when libraries update
- **Flat directory** — No subdirectories per SLT (simpler for organization)
- **Include expected output** — Either in comments or companion `.output` file
