---
name: improve-doc
description: Analyze and improve existing documentation using Diataxis principles
disable-model-invocation: true
---

# Improve Doc

Analyze an existing markdown document, classify sections by Diataxis type, identify issues, and interactively refine each section.

## Arguments

- **Path:** Path to the markdown document to improve (required)

## Workflow Overview

Invoke the **improve-doc** skill with a document path, e.g. `improve-doc docs/guides/getting-started.md`.

The skill runs in two phases:

1. **Analysis Phase:** Parse document, classify sections, identify issues
2. **Refinement Phase:** Interactive loop to improve each section

## Gates

Hard sequencing — advance only when the **pass condition** is met (artifact or explicit user input, not assumed).

**Before Phase 2 (refinement):**

1. **Read** — Full contents of the file at **Path** are loaded.
   - **Pass:** Enumerated sections (from `#` / `##` / `###` headings) cover every heading in the file; titles match the source.
2. **Core skill** — [docs-style](../docs-style/SKILL.md) is loaded (or its path read) before classification.
   - **Pass:** Analysis output reflects at least one concrete principle from that skill (name it or quote briefly).
3. **Handoff** — User saw an analysis summary (template in Step 5 or equivalent) and entered **`start`** to begin refinement, or **`abort`** to exit.
   - **Pass:** If `abort`, no writes to **Path**. If `start`, proceed to Phase 2.

**Before overwriting the file (Phase 2, Step 4):**

1. **Choices** — Every section with open issues has a terminal outcome: applied **`yes`**, unchanged **`skip`**, or **`modify`** loop finished with **`yes`** or **`skip`**.
   - **Pass:** No section left in a pending `modify` state unless the user aborted the whole session (then do not write).
2. **Skips** — Content for every **`skip`** matches the original section text (copy preserved, not paraphrased).
   - **Pass:** Full block equality check against the initial read (line-for-line, including whitespace).
3. **Write** — Only after the above.
   - **Pass:** Single save to **Path**; completion report notes backup or major restructure if applicable (Rules).

**Ambiguous Diataxis type** — If classification is uncertain, do not edit that section until the user answers the clarifying fork (Step 2b) or explicitly confirms your stated default.

## Phase 1: Analysis

### Step 1: Read Document

Read the target markdown file and parse into sections based on headings:

- Each `#`, `##`, `###` heading starts a new section
- Capture heading level, title, and content
- Preserve hierarchy for context

### Step 2: Load Core Skill

Load [docs-style](../docs-style/SKILL.md) for core writing principles that apply to all documentation types.

### Step 3: Classify Each Section

For each section, determine the Diataxis type using these indicators:

| Type | Indicators |
|------|------------|
| **Tutorial** | "Let's", "we will", step-by-step learning, builds toward a project, minimal explanation of why |
| **How-To** | "How to" title, task-focused steps, assumes prior knowledge, goal-oriented |
| **Reference** | Parameter tables, type signatures, API specs, factual descriptions, no narrative |
| **Explanation** | "Why", "because", history, trade-offs, alternatives, conceptual discussion |

**Classification rules:**

1. Check title first - "How to X" is always How-To, "Why X" is always Explanation
2. Look for structural patterns - tables with parameters/types suggest Reference
3. Analyze language - learning-oriented ("Let's learn") vs task-oriented ("To accomplish X")
4. Consider context - what comes before/after this section
5. Mark as "Mixed" if section blends types (this is an issue to fix)

### Step 4: Identify Issues

For each section, check for issues based on its detected type:

**Tutorial issues:**
- Explains "why" instead of just guiding the learner
- Skips steps assuming prior knowledge
- No clear learning outcome
- Missing "you will build/learn" framing

**How-To issues:**
- Includes explanatory tangents
- Missing prerequisites
- Steps not atomic (multiple actions per step)
- No verification that goal was achieved

**Reference issues:**
- Missing parameter types or return values
- Narrative text instead of factual description
- Incomplete coverage of options/parameters
- No code examples

**Explanation issues:**
- Includes procedural steps
- Missing context for "why"
- No trade-offs or alternatives discussed
- Reads like reference material

**Cross-type issues (any section):**
- Mixed Diataxis types in single section
- Unclear who the audience is
- Missing or vague heading
- Wall of text without structure

### Step 5: Present Analysis

Display analysis summary to user:

```markdown
## Document Analysis

**File:** `docs/guides/getting-started.md`
**Sections found:** 8
**Estimated time:** ~15 minutes to refine

### Type Breakdown

| Type | Sections | Health |
|------|----------|--------|
| Tutorial | 2 | 1 issue |
| How-To | 3 | 4 issues |
| Reference | 1 | Clean |
| Explanation | 1 | 2 issues |
| Mixed | 1 | Needs split |

### Top Issues

1. **Section "Setting Up"** (How-To): Contains explanatory tangent about architecture
2. **Section "Configuration Options"** (Mixed): Blends reference table with tutorial steps
3. **Section "Authentication"** (How-To): Missing prerequisites, steps not atomic
4. **Section "Why We Built This"** (Explanation): Includes procedural steps

### Ready to Refine?

I'll go through each section with issues. For each one, you can:
- **yes** - Accept the proposed improvement
- **skip** - Keep original, move to next section
- **modify** - Tell me what to change about the proposal

Type "start" to begin refinement, or "abort" to exit without changes.
```

## Phase 2: Interactive Refinement

### Step 1: Load Type-Specific Skills

As you encounter each section type, load the relevant skill if not already loaded:

- Tutorial sections: [tutorial-docs](../tutorial-docs/SKILL.md)
- How-To sections: [howto-docs](../howto-docs/SKILL.md)
- Reference sections: [reference-docs](../reference-docs/SKILL.md)
- Explanation sections: [explanation-docs](../explanation-docs/SKILL.md)

### Step 2: Refinement Loop

For each section with issues, in document order:

#### 2a: Show Current State

```markdown
---

## Section 3 of 5: "Setting Up" (How-To)

### Current Content

> ## Setting Up
>
> Before we begin, it's important to understand why the architecture
> works this way. The system uses a microservices pattern because...
> [explanatory content]
>
> To set up the project:
> 1. Clone the repo and install dependencies
> 2. Configure the environment variables
> 3. Start the server

### Issues Found

1. **Explanatory tangent** (lines 1-3): How-To should assume reader knows why; move explanation to dedicated Explanation section
2. **Non-atomic steps** (step 1): "Clone and install" is two actions; split into separate steps
3. **Missing verification**: No way to confirm setup succeeded

```

#### 2b: Ask Clarifying Question (if needed)

If the type classification is uncertain:

```markdown
### Quick Question

This section has characteristics of both How-To (task steps) and Explanation (why content). How would you like to handle it?

1. **Split** - Create separate How-To and Explanation sections
2. **How-To** - Remove explanation, keep as pure How-To
3. **Explanation** - Remove steps, keep as pure Explanation
```

#### 2c: Propose Improvement

```markdown
### Proposed Improvement

> ## Setting Up
>
> **Prerequisites:** Familiarity with microservices architecture
>
> ### Steps
>
> 1. Clone the repository
>    ```bash
>    git clone https://github.com/example/project.git
>    ```
>
> 2. Install dependencies
>    ```bash
>    cd project && npm install
>    ```
>
> 3. Configure environment variables
>    ```bash
>    cp .env.example .env
>    ```
>
> 4. Start the server
>    ```bash
>    npm start
>    ```
>
> ### Verify
>
> Open http://localhost:3000 - you should see the welcome page.

**Changes made:**
- Removed explanatory content (suggest creating "Architecture Overview" section)
- Split "clone and install" into separate steps
- Added verification step
- Added prerequisites reference

---

**Your choice:** [yes / skip / modify]
```

#### 2d: Handle User Choice

**yes** - Apply the proposed changes to the section, continue to next

**skip** - Keep original content unchanged, continue to next

**modify** - User provides feedback:

```markdown
> modify: Keep the explanation but move it to a collapsible "Why?" block

### Revised Proposal

> ## Setting Up
>
> <details>
> <summary>Why this architecture?</summary>
>
> The system uses a microservices pattern because...
>
> </details>
>
> ### Steps
> [same as before]

**Your choice:** [yes / skip / modify]
```

### Step 3: Handle Mixed Sections

For sections classified as "Mixed":

```markdown
---

## Section 5 of 5: "Configuration Options" (Mixed)

### Current Content

> ## Configuration Options
>
> Let's walk through configuring your application. First, you'll need
> to understand the available options:
>
> | Option | Type | Default | Description |
> |--------|------|---------|-------------|
> | port | number | 3000 | Server port |
> | debug | boolean | false | Enable debug mode |
>
> Now let's configure each one step by step...

### Issues Found

1. **Mixed types**: Tutorial framing ("Let's walk through") with Reference content (options table)

### Recommendation

Split into two sections:

1. **Reference section** - "Configuration Reference" with the options table
2. **Tutorial section** - "Configuring Your First App" with learning-oriented walkthrough

Would you like me to:
1. **Split** - Create both sections
2. **Reference only** - Keep just the table, remove tutorial framing
3. **Tutorial only** - Expand into full tutorial, move table to appendix
```

### Step 4: Write Updated Document

After all sections processed:

1. **Build updated content** from accepted changes
2. **Preserve unchanged sections** exactly as they were
3. **Overwrite original file** with updated content

### Step 5: Report Results

```markdown
## Refinement Complete

**File:** `docs/guides/getting-started.md`

### Changes Summary

| Section | Action | Type |
|---------|--------|------|
| Setting Up | Improved | How-To |
| Configuration Options | Split | Reference + Tutorial |
| Authentication | Improved | How-To |
| Why We Built This | Skipped | Explanation |

### Sections Modified

- **Setting Up**: Removed tangent, split steps, added verification
- **Configuration Options**: Split into "Configuration Reference" and "Configuring Your App"
- **Authentication**: Added prerequisites, made steps atomic

### New Sections Created

- **Configuration Reference** (Reference): Options table from split
- **Configuring Your App** (Tutorial): Learning walkthrough from split

### Recommendations

Consider creating these additional documents:
- `docs/explanation/architecture-overview.md` - For content removed from "Setting Up"

The original file has been updated.
```

## Rules

- Follow **Gates** for phase transitions and before saving to **Path**
- Always load `docs-style` skill before analysis
- Load type-specific skills lazily as sections are encountered
- Never modify the file until refinement phase completes (see Gates: overwrite)
- Preserve sections marked "skip" exactly as-is
- When splitting sections, maintain logical reading order
- Ask clarifying questions when type classification is ambiguous (confidence < 70%)
- For "Mixed" sections, always offer split as the first option
- Include specific line references when identifying issues
- Show diff-style changes in proposals when helpful
- Respect user's "modify" feedback - iterate until they say "yes" or "skip"
- Create backup note in output if major restructuring occurred
