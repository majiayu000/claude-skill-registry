# Skill Authoring Best Practices

Practical authoring decisions for writing Skills that Claude can discover and use effectively. Good Skills are concise, well-structured, and tested with real usage.

For conceptual background on how Skills work, see the Skills overview on platform.claude.com.

## Core Principles

### Concise Is Key

The context window is a public good. Your Skill shares the context window with everything else Claude needs to know, including:
- The system prompt
- Conversation history
- Other Skills' metadata
- Your actual request

Not every token in your Skill has an immediate cost. At startup, only the metadata (name and description) from all Skills is pre-loaded. Claude reads SKILL.md only when the Skill becomes relevant, and reads additional files only as needed. However, being concise in SKILL.md still matters: once Claude loads it, every token competes with conversation history and other context.

**Default assumption**: Claude is already very smart

Only add context Claude doesn't already have. Challenge each piece of information:
- "Does Claude really need this explanation?"
- "Can I assume Claude knows this?"
- "Does this paragraph justify its token cost?"

**Good example: Concise** (approximately 50 tokens):
````markdown
## Extract PDF text

Use pdfplumber for text extraction:

```python
import pdfplumber

with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```
````

**Bad example: Too verbose** (approximately 150 tokens):
```markdown
## Extract PDF text

PDF (Portable Document Format) files are a common file format that contains
text, images, and other content. To extract text from a PDF, you'll need to
use a library. There are many libraries available for PDF processing, but
pdfplumber is recommended because it's easy to use and handles most cases well.
First, you'll need to install it using pip. Then you can use the code below...
```

#### Skill Files Are Instructions, Not Documentation

A skill file tells Claude what to do. It is not a place to explain what the skill is, why it exists, how it fits into the broader collection, or what its design history is. Claude does not benefit from narrator prose — a human reader might, but skills are loaded into an agent's context, not read by humans at design time.

Common drift patterns to strip on sight:

- **Meta-framing** — sentences that describe the skill file to its own reader: "This SKILL.md is the router...", "This skill wraps X with Y...", "This file acts as..." If Claude is reading the file, it already knows it's reading the file.
- **Cross-skill commentary** — "This skill is the sibling/counterpart/successor of /other-skill." Skills should be self-contained and not reference which pipelines call them or which siblings they relate to.
- **Marketing or positioning copy** — "X is the structured alternative to Y" or "X is the preferred way to do Z." That kind of framing belongs in a README, not a skill file.
- **Architecture commentary** — explaining the data model or file layout as standalone prose when the instructions already imply the structure. If the steps tell Claude to "write the index to `<path>`," a separate sentence saying "the index is a thin manifest" adds nothing.
- **Historical rationale** — "X happens here because Y would cause Z." Keep only the rule; drop the backstory unless it actively prevents a rationalization the agent would otherwise make.
- **Tautological boundary statements** — "X is Y's job; this skill only does Z." If the positive instructions are correct, boundaries are already implicit.
- **"Caller" phrasing** — "the caller," "caller passed," "caller provides." Skills run in a conversational context, not a function-call context. This is narrator language about who invoked the skill rather than instruction to the agent, and it is ambiguous about whether "the caller" is the user, another skill, or the pipeline agent. Prefer passive voice ("if a shell path was provided") or a named role when the distinction actually matters.

When in doubt, compare a new or edited skill against the simplest existing skills in the same collection. If a lean neighbor skill opens with a one-line purpose and jumps straight into Task Tracking or Step 1, and your skill has three paragraphs of context before the first instruction, the extra paragraphs are almost certainly drift.

### Set Appropriate Degrees of Freedom

Match the level of specificity to the task's fragility and variability.

**High freedom** (text-based instructions):

Use when:
- Multiple approaches are valid
- Decisions depend on context
- Heuristics guide the approach

Example:
```markdown
## Code review process

1. Analyze the code structure and organization
2. Check for potential bugs or edge cases
3. Suggest improvements for readability and maintainability
4. Verify adherence to project conventions
```

**Medium freedom** (pseudocode or scripts with parameters):

Use when:
- A preferred pattern exists
- Some variation is acceptable
- Configuration affects behavior

Example:
````markdown
## Generate report

Use this template and customize as needed:

```python
def generate_report(data, format="markdown", include_charts=True):
    # Process data
    # Generate output in specified format
    # Optionally include visualizations
```
````

**Low freedom** (specific scripts, few or no parameters):

Use when:
- Operations are fragile and error-prone
- Consistency is critical
- A specific sequence must be followed

Example:
````markdown
## Database migration

Run exactly this script:

```bash
python scripts/migrate.py --verify --backup
```

Do not modify the command or add additional flags.
````

### Test with All Models You Plan to Use

Skills act as additions to models, so effectiveness depends on the underlying model. Test your Skill with each model you plan to use — what works for Opus may need more guidance for Haiku, and what's clear for Haiku may over-explain for Opus.

## Skill Metadata and Structure

### YAML Frontmatter

The SKILL.md frontmatter requires two fields:

`name`:
- Maximum 64 characters
- Must contain only lowercase letters, numbers, and hyphens
- Cannot contain XML tags
- Cannot contain reserved words: "anthropic", "claude"

`description`:
- Must be non-empty
- Maximum 1024 characters
- Cannot contain XML tags
- Should describe what the Skill does and when to use it

**Quoting values**: Quote frontmatter values that contain YAML special characters. Unquoted `: ` (colon-space) breaks parsing. When in doubt, wrap the value in double quotes and escape inner quotes with `\"`.

```yaml
# Bad — colon-space breaks YAML parsing
description: Adapts to repo mode: fork creates a PR

# Good — quoted value
description: "Adapts to repo mode: fork creates a PR"
```

### Naming Conventions

Use consistent naming patterns to make Skills easier to reference and discuss. Consider using **gerund form** (verb + -ing) for Skill names, as this clearly describes the activity or capability the Skill provides.

Remember that the `name` field must use lowercase letters, numbers, and hyphens only.

**Good naming examples (gerund form)**:
- `processing-pdfs`
- `analyzing-spreadsheets`
- `managing-databases`
- `testing-code`
- `writing-documentation`

**Acceptable alternatives**:
- Noun phrases: `pdf-processing`, `spreadsheet-analysis`
- Action-oriented: `process-pdfs`, `analyze-spreadsheets`

**Avoid**:
- Vague names: `helper`, `utils`, `tools`
- Overly generic: `documents`, `data`, `files`
- Reserved words: `anthropic-helper`, `claude-tools`
- Inconsistent patterns within your skill collection

### Writing Effective Descriptions

The `description` field enables Skill discovery and should include both what the Skill does and when to use it.

> **Warning: Always write in third person**. The description is injected into the system prompt, and inconsistent point-of-view can cause discovery problems.
>
> - **Good:** "Processes Excel files and generates reports"
> - **Avoid:** "I can help you process Excel files"
> - **Avoid:** "You can use this to process Excel files"

**Be specific and include key terms**. Include both what the Skill does and specific triggers/contexts for when to use it.

Each Skill has exactly one description field. The description is critical for skill selection: Claude uses it to choose the right Skill from potentially 100+ available Skills. Your description must provide enough detail for Claude to know when to select this Skill, while the rest of SKILL.md provides the implementation details.

Effective:
```yaml
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
```

Avoid vague descriptions like `Helps with documents`, `Processes data`, or `Does stuff with files`.

### Progressive Disclosure Patterns

SKILL.md serves as an overview that points Claude to detailed materials as needed, like a table of contents in an onboarding guide.

**Practical guidance:**
- Keep SKILL.md body under 500 lines for optimal performance
- Split content into separate files when approaching this limit
- Use the patterns below to organize instructions, code, and resources effectively

A Skill can grow from a single SKILL.md to a directory of bundled content that Claude loads only when needed:

```text
pdf/
├── SKILL.md              # Main instructions (loaded when triggered)
├── FORMS.md              # Form-filling guide (loaded as needed)
├── reference.md          # API reference (loaded as needed)
├── examples.md           # Usage examples (loaded as needed)
└── scripts/
    ├── analyze_form.py   # Utility script (executed, not loaded)
    ├── fill_form.py      # Form filling script
    └── validate.py       # Validation script
```

#### Pattern 1: High-Level Guide with References

````markdown
---
name: pdf-processing
description: Extracts text and tables from PDF files, fills forms, and merges documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
---

# PDF Processing

## Quick start

Extract text with pdfplumber:
```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

## Advanced features

**Form filling**: See [FORMS.md](FORMS.md) for complete guide
**API reference**: See [REFERENCE.md](REFERENCE.md) for all methods
**Examples**: See [EXAMPLES.md](EXAMPLES.md) for common patterns
````

Claude loads FORMS.md, REFERENCE.md, or EXAMPLES.md only when needed.

#### Pattern 2: Domain-Specific Organization

For Skills with multiple domains, organize content by domain to avoid loading irrelevant context. When a user asks about sales metrics, Claude only needs to read sales-related schemas, not finance or marketing data. This keeps token usage low and context focused.

```text
bigquery-skill/
├── SKILL.md (overview and navigation)
└── reference/
    ├── finance.md (revenue, billing metrics)
    ├── sales.md (opportunities, pipeline)
    ├── product.md (API usage, features)
    └── marketing.md (campaigns, attribution)
```

````markdown SKILL.md
# BigQuery Data Analysis

## Available datasets

**Finance**: Revenue, ARR, billing → See [reference/finance.md](reference/finance.md)
**Sales**: Opportunities, pipeline, accounts → See [reference/sales.md](reference/sales.md)
**Product**: API usage, features, adoption → See [reference/product.md](reference/product.md)
**Marketing**: Campaigns, attribution, email → See [reference/marketing.md](reference/marketing.md)

## Quick search

Find specific metrics using grep:

```bash
grep -i "revenue" reference/finance.md
grep -i "pipeline" reference/sales.md
grep -i "api usage" reference/product.md
```
````

#### Pattern 3: Conditional Details

Show basic content, link to advanced content:

```markdown
# DOCX Processing

## Creating documents

Use docx-js for new documents. See [DOCX-JS.md](DOCX-JS.md).

## Editing documents

For simple edits, modify the XML directly.

**For tracked changes**: See [REDLINING.md](REDLINING.md)
**For OOXML details**: See [OOXML.md](OOXML.md)
```

Claude reads REDLINING.md or OOXML.md only when the user needs those features.

### Avoid Deeply Nested References

Claude may partially read files when they're referenced from other referenced files. When encountering nested references, Claude might use commands like `head -100` to preview content rather than reading entire files, resulting in incomplete information.

**Keep references one level deep from SKILL.md**. All reference files should link directly from SKILL.md to ensure Claude reads complete files when needed.

**Bad example: Too deep**:
```markdown
# SKILL.md
See [advanced.md](advanced.md)...

# advanced.md
See [details.md](details.md)...

# details.md
Here's the actual information...
```

**Good example: One level deep**:
```markdown
# SKILL.md

**Basic usage**: [instructions in SKILL.md]
**Advanced features**: See [advanced.md](advanced.md)
**API reference**: See [reference.md](reference.md)
**Examples**: See [examples.md](examples.md)
```

### Separation of Concerns Between Layers

When SKILL.md links to sub-files, each layer must own exactly one concern:

- **SKILL.md (router)**: Routing decisions, shared config, links to sub-files. Does not summarize or repeat sub-file content.
- **Sub-files (leaves)**: Self-contained instructions for one mode or topic. Assumes the routing decision is already made. Does not contain cross-mode routing tables.

Routing tables, decision logic, and shared config belong in SKILL.md only. Sub-files should never route back to siblings, and SKILL.md should not summarize sub-file commands. When other skills reference a sub-file, they should point to the skill and name the sub-file: "Run `/skill-name` skill and consult sub-file.md to ..."

### Use Forward Slashes in Paths

Always use forward slashes in file paths, even on Windows:

- ✓ **Good**: `scripts/helper.py`, `reference/guide.md`
- ✗ **Avoid**: `scripts\helper.py`, `reference\guide.md`

Unix-style paths work across all platforms; Windows-style paths cause errors on Unix systems.

### Compute Relative Paths from the File's Actual Location

When a skill file references another file in the same skill, the relative path resolves from the file's own location, not from `SKILL.md`. A reference file at `skills/X/references/foo.md` linking to a sibling at `skills/X/references/bar.md` writes `bar.md`, not `references/bar.md`.

Use markdown links rather than inline code for cross-references. `[bar.md](bar.md)` matches how `SKILL.md` links to its references and how skills link to each other; inline `` `bar.md` `` reads as a path mention but loses the click-through and the convention.

- ✗ **Avoid**: From `skills/X/references/spec-mode.md`: "follow `references/plan-mode.md`" — broken path; not a link.
- ✓ **Good**: From `skills/X/references/spec-mode.md`: "follow [plan-mode.md](plan-mode.md)".

### Structure Longer Reference Files with Table of Contents

For reference files longer than 100 lines, include a table of contents at the top. This ensures Claude can see the full scope of available information even when previewing with partial reads.

**Example**:
```markdown
# API Reference

## Contents
- Authentication and setup
- Core methods (create, read, update, delete)
- Advanced features (batch operations, webhooks)
- Error handling patterns
- Code examples

## Authentication and setup
...

## Core methods
...
```

Claude can then read the complete file or jump to specific sections as needed.

## Writing the Body

### Keep a Short Intro Paragraph

YAML frontmatter (name, description) is stripped before the skill body is loaded into context. If the title and steps don't make the skill's purpose obvious, a one-line intro paragraph after the `# Title` heading can help orient execution. Keep it short, avoid restating the description verbatim, and omit it entirely if the steps already make the purpose clear.

### Use Consistent Terminology

Choose one term and use it throughout the Skill:

**Good - Consistent**:
- Always "API endpoint"
- Always "field"
- Always "extract"

**Bad - Inconsistent**:
- Mix "API endpoint", "URL", "API route", "path"
- Mix "field", "box", "element", "control"
- Mix "extract", "pull", "get", "retrieve"

Consistency helps Claude understand and follow instructions.

### Use Generic Examples

Skills may be used across different projects. Avoid project-specific details in examples — use generic placeholders instead.

**Bad example: Project-specific**:
```markdown
Run `python3 manage.py migrate` to update the Acme database schema.
Click the "Deploy to Acme Staging" button.
```

**Good example: Generic placeholders**:
```markdown
Run the project's migration command to update the database schema.
Click the deployment button for the target environment.
```

If a skill is project-specific by design (lives in the project repo, not in a shared location), project-specific examples are acceptable. But skills intended for reuse across projects should use generic placeholders.

Also consider whether inline examples are needed at all. Parenthetical examples like "(e.g. click the Submit button)" often add no value when the instruction is already clear. Prefer concise instructions without examples over instructions cluttered with obvious ones.

### Prefer Positive Phrasing

State what to do. Imperative verbs ("defer", "limit", "exclude", "halt", "describe") give the agent a clear action; chains of "Never X. Don't Y. Avoid Z." force the agent to invert the prohibition into an action before acting on it.

**Bad example: Negative**:
```markdown
- Never modify files in `vendor/`. Files there are managed by the package manager.
```

**Good example: Positive**:
```markdown
- Treat files in `vendor/` as read-only.
```

The positive form names the action and drops the explanatory clause that just restates the boundary.

Use negative phrasing only when a positive imperative cannot articulate the rule unambiguously. When an explicit enumeration of prohibited items is load-bearing, prefer positive verbs ("Exclude", "Omit", "Reserve X for Y") over "Never include" or "Don't add". Redundant negative restatements — a rule paired with a tautological-boundary clause that says the same thing — are always trim targets.

### State Conditions Explicitly

If a step has a clear condition for when to execute and when to skip, state both directly. Don't soften it with "optionally" — that creates ambiguity about whether the step should actually run.

- ✗ **Avoid**: "Optionally spawn a subagent to verify findings."
- ✓ **Good**: "Spawn a subagent when there are 3+ non-trivial findings. **Skip** when all findings are clear-cut."

### Address Subagents Directly

When a skill's body needs to constrain how a subagent invoking it should behave, address that subagent directly using "If you are a subagent" gating. Phrasings like "from inside an Agent subagent" or "when wrapped in a subagent" read as third-person references and are ambiguous: the reader may parse them as "from inside an Agent subagent that I would spawn" rather than "if I am that subagent".

- ✗ **Avoid**: "When this skill is invoked from inside an Agent subagent, the Agent prompt must include..."
- ✗ **Avoid**: "Subagents wrapping this skill should..."
- ✓ **Good**: "If you are a subagent, follow these guardrails..."

Skills are loaded by the subagent itself when it invokes the skill via the Skill tool. The body's instructions arrive in the subagent's own context, so direct second-person address is correct.

### Prefer Qualitative Descriptions for Judgment Calls

When a skill describes a threshold the agent must judge (when something is too large, when to split, when to combine), prefer qualitative descriptions over numeric heuristics. Numbers like "more than 15 files" or "3+ subsystems" feel precise but encourage box-ticking — agents tally and cross the threshold without engaging the underlying judgment. Qualitative descriptions ("the work would exhaust a session", "too many distinct conventions to absorb") force the agent to evaluate the actual situation.

- ✗ **Avoid**: "Split when a shell would touch more than 15-20 files or span 3+ unrelated subsystems."
- ✓ **Good**: "Split when the combined work would exhaust a single session: too much code to read in full, or too many distinct conventions to absorb."

Use numbers only when the threshold is mechanically verifiable and the count is the actual signal (e.g., "cap at 3 retries", "every R-id must appear in at least one Covers field").

### Avoid Time-Sensitive Information

Don't include information that will become outdated:

- ✗ **Avoid**: "Before August 2025, use the old API. After August 2025, use the new API."
- ✓ **Good**: Document the current method directly. If legacy guidance is needed, isolate it under an "Old patterns" section so it doesn't clutter primary instructions.

### Avoid Redundant Rules Sections

A Rules section should only contain information not already conveyed by the skill body. Before adding a rule, check whether the Process, workflow steps, or tables already encode the same behavior. If they do, the rule is wasted tokens.

### Provide a Default Rather Than Too Many Options

Don't present multiple approaches unless necessary:

````markdown
**Bad example: Too many choices** (confusing):
"You can use pypdf, or pdfplumber, or PyMuPDF, or pdf2image, or..."

**Good example: Provide a default** (with escape hatch):
"Use pdfplumber for text extraction:
```python
import pdfplumber
```

For scanned PDFs requiring OCR, use pdf2image with pytesseract instead."
````

### Verify Code Fence Pairing After Multi-Template Edits

When inserting a second fenced code block alongside an existing one in the same skill section, verify that both fences pair correctly. Multi-template edits commonly produce orphan closing fences, especially when shared scaffolding (XML output contracts, output specs, dig-deeper nudges) needs to apply to both templates.

Two safe patterns:

1. **Each template fully self-contained**: Each fenced block contains its own copy of the shared scaffolding. Repetitive but unambiguous.
2. **Shared scaffolding in its own fence**: The shared content lives in a separate labeled fenced block, with prose explaining how to concatenate it with the template-specific blocks.

- ✗ **Avoid**: Two fenced template blocks where shared XML scaffolding appears as raw markdown between them, leaving an orphan closing ` ``` ` somewhere. Readers see the shared content as unparsed prose; rendering breaks.
- ✓ **Good**: Three fenced blocks (template A, template B, shared scaffolding) with `### ` subheadings naming each. Or two fenced blocks where each repeats the shared scaffolding internally.

## Workflows and Feedback Loops

### Use Workflows for Complex Tasks

Break complex operations into clear, sequential steps. Use `## Step N:` headings for the steps. For particularly complex workflows with distinct phases, nest steps under phases using `## Phase N` with `### Step N:` subheadings.

**Simple workflow:**
```markdown
## Step 1: Analyze Input
...
## Step 2: Transform Data
...
## Step 3: Validate Output
...
```

**Complex multi-phase workflow:**
```markdown
## Phase 1: Planning

### Step 1: Gather Requirements
...
### Step 2: Design Solution
...

## Phase 2: Execution

### Step 1: Implement Changes
...
### Step 2: Run Tests
...
```

**Avoid** wrapper sections like `## Process` with `### 1.` numbered subsections. Steps should be top-level, not nested under a generic heading.

**Avoid** any section whose only purpose is to inspect input or detect a mode, regardless of what it is labeled. This includes numbered "Step 0" headings, unnumbered `## Mode Selection` sections, or any subheading that collapses to "if X, read file A; otherwise read file B." A step or section should do work the agent executes. Trivial input inspection and mode routing are one-line branches — fold them into the skill's opening prose rather than giving them their own heading.

For particularly complex workflows, provide a checklist that Claude can copy into its response and check off as it progresses. The pattern works for any multi-step process — code-based or analysis-only.

````markdown
## PDF form filling workflow

Copy this checklist and check off items as you complete them:

```
Task Progress:
- [ ] Step 1: Analyze the form (run analyze_form.py)
- [ ] Step 2: Create field mapping (edit fields.json)
- [ ] Step 3: Validate mapping (run validate_fields.py)
- [ ] Step 4: Fill the form (run fill_form.py)
- [ ] Step 5: Verify output (run verify_output.py)
```

**Step 1: Analyze the form**

Run: `python3 scripts/analyze_form.py input.pdf`

This extracts form fields and their locations, saving to `fields.json`.

**Step 2: Create field mapping**

Edit `fields.json` to add values for each field.

**Step 3: Validate mapping**

Run: `python3 scripts/validate_fields.py fields.json`

Fix any validation errors before continuing.

**Step 4: Fill the form**

Run: `python3 scripts/fill_form.py input.pdf fields.json output.pdf`

**Step 5: Verify output**

Run: `python3 scripts/verify_output.py output.pdf`

If verification fails, return to Step 2.
````

Clear steps prevent Claude from skipping critical validation. The checklist helps both Claude and you track progress through multi-step workflows.

### Implement Feedback Loops

**Common pattern**: Run validator → fix errors → repeat. The validator can be a script, a reference document, or a checklist — what matters is the loop.

```markdown
## Document editing process

1. Make your edits to `word/document.xml`
2. **Validate immediately**: `python3 ooxml/scripts/validate.py unpacked_dir/`
3. If validation fails:
   - Review the error message carefully
   - Fix the issues in the XML
   - Run validation again
4. **Only proceed when validation passes**
5. Rebuild: `python3 ooxml/scripts/pack.py unpacked_dir/ output.docx`
6. Test the output document
```

### Use Recursive Self-Invocation for Convergence Loops

When a skill needs to repeat its workflow until stable (e.g., simplify → review → test → repeat if changed), have the last step re-invoke the skill itself rather than encoding an internal loop. This keeps each step distinct and the flow linear. Use "skipping Step N" to bypass one-time setup steps on re-runs.

```markdown
## Step 1: Setup (first run only)
...
## Step 2: Do work
...
## Step 3: Re-run if changed

If any prior step produced changes, run the `/this-skill` skill again, skipping Step 1.

## Rules

- Cap at 3 consecutive runs to prevent runaway loops.
```

### Use Neutral Exit Signals So Parent Pipelines Can Continue

When a skill detects a clean early-exit case (a degenerate input that doesn't warrant the full output), the exit instructions need to allow parent pipelines to detect and reroute. Phrasing like "Halt and tell the user X" reads as a hard stop and terminates the agent's flow, including any parent pipeline that called the skill.

Phrasing like "Present this message: <factual summary>. Then use the TaskList tool and proceed to any remaining task." lets the agent surface what happened and continue to whatever task is next. The signal that the early-exit fired lives in the side effects (no file written, factual message shown), and the parent pipeline reads them via filesystem checks or remaining-task detection.

Blocker gates (covered in "Using AskUserQuestion") handle a different case: when the agent needs the user to choose between recoveries. Use neutral exit signals when the work simply terminates earlier than the full path.

- ✗ **Avoid**: "Halt and tell the user 'no shells produced — run `/draft-plan` instead.'"
- ✓ **Good**: "Present this message: '<factual summary>'. Then use the TaskList tool and proceed to any remaining task."

## Common Patterns

### Template Pattern

Provide templates for output format. Match the level of strictness to your needs — open with "ALWAYS use this exact template" for strict requirements (API responses, data formats), or "Here is a sensible default; use your best judgment" when adaptation is useful.

````markdown
## Report structure

ALWAYS use this exact template structure:

```markdown
# [Analysis Title]

## Executive summary
[One-paragraph overview of key findings]

## Key findings
- Finding 1 with supporting data
- Finding 2 with supporting data

## Recommendations
1. Specific actionable recommendation
2. Specific actionable recommendation
```
````

### Examples Pattern

For Skills where output quality depends on seeing examples, provide input/output pairs just like in regular prompting:

````markdown
## Commit message format

Generate commit messages following these examples:

**Example 1:**
Input: Added user authentication with JWT tokens
Output:
```
feat(auth): implement JWT-based authentication

Add login endpoint and token validation middleware
```

**Example 2:**
Input: Fixed bug where dates displayed incorrectly in reports
Output:
```
fix(reports): correct date formatting in timezone conversion

Use UTC timestamps consistently across report generation
```

Follow this style: type(scope): brief description, then detailed explanation.
````

Examples help Claude understand the desired style and level of detail more clearly than descriptions alone.

### Conditional Workflow Pattern

Guide Claude through decision points:

```markdown
## Document modification workflow

1. Determine the modification type:

   **Creating new content?** → Follow "Creation workflow" below
   **Editing existing content?** → Follow "Editing workflow" below

2. Creation workflow:
   - Use docx-js library
   - Build document from scratch
   - Export to .docx format

3. Editing workflow:
   - Unpack existing document
   - Modify XML directly
   - Validate after each change
   - Repack when complete
```

> **Tip:** If workflows become large or complicated with many steps, consider pushing them into separate files and tell Claude to read the appropriate file based on the task at hand.

### Align Output Formats Across Parallel Producers

When two or more skills produce findings that feed a shared downstream pipeline (for example, an evaluation or triage skill), align their default output formats so the consumer can concatenate findings without transforming them. Drift in finding shape (different metadata labels, missing source attribution, divergent priority scales) forces the consumer to reformat, which invites bugs and defeats composition.

- **Match field names** — if one producer emits `**File:** <path> (lines <start>-<end>)`, the other's default should use the same label and slot, even if the line-range slot is optional for some inputs.
- **Include source attribution** — when findings from multiple producers merge, each should carry a `**Reviewer:**` (or equivalent) line so the consumer can distinguish them.
- **Share the priority scale** — use the same labels and semantics (e.g., P0–P3) across producers so the downstream can rank findings uniformly.
- **Let callers override the default** — alignment applies to the producer's *default* format. Specific callers can still pass a tailored output format when they need extra fields.

## Cross-Skill Composition

### Cross-Skill Dependencies

When a skill depends on another skill, make it an explicit numbered step. Use "Run `/skill-name` Skill" as the heading and "Run the `/skill-name` skill" in the step body. Including "skill" signals to invoke via the Skill tool rather than treating it as a general reference.

```markdown
## Step 1: Run `/<rules-skill>` Skill

Run the `/<rules-skill>` skill to load shared rules and conventions.

## Step 2: Do the Work

- The actual steps of this skill
```

**Style-guide dependencies as Step 1:** When a skill depends on a style-guide skill that loads conventions, place it as Step 1. Style guides shape all subsequent work. Burying them in a later step risks them being skipped.

### Explicitly Invoke Skills When the Verb Matches a Skill Name

When a step body uses an action verb that is also the name of an existing skill, the bare verb reads as inline reasoning and the agent skips the actual Skill tool call. Name the skill explicitly so the invocation is unambiguous.

- ✗ **Avoid**: "If a check fails, halt and `<verb>`."
- ✓ **Good**: "If a check fails, run the `/<verb>` skill."

This complements the explicit numbered-step rule above by covering verb collisions inside step bodies.

### Bundle Parallel Fan-Out Inside One Skill, Not Across Siblings

When a workflow needs N parallel reviewers/dimensions/perspectives (e.g., internal review + peer review, or multiple review types in one pass), put the fan-out inside one skill body rather than asking a parent to load several sibling skills "in parallel" via the Skill tool. The parent's "load A and B" pattern can't actually parallelize the sibling skills' work, and it leaks the siblings' implementation details into the parent step.

The right shape is a single skill that emits N+1 Agent tool calls in one message. Add an opt-out (e.g., "skip peer review") for callers who want only the internal pass.

- ✗ **Avoid**: Parent skill Step says "Run `/<review-skill>` and `/<peer-review-skill>` skills concurrently" and tries to batch two Skill calls.
- ✓ **Good**: `/<review-skill>` internally launches both internal reviewer Agents and a peer reviewer Agent in one message; the parent just calls `/<review-skill>`.

## Tool Usage in Skills

### Dispatching Agent Tool Calls

When a skill spawns subagents, always specify `model` and `run_in_background` explicitly in a parenthetical. Vague phrasing like "launch concurrently" or "in parallel" causes flaky behavior where Claude sometimes sets `run_in_background: true` and sometimes doesn't.

Multiple foreground Agent tool calls in a single message already run in parallel. Prefer foreground agents over background agents:

- **Foreground parallel** (recommended): Multiple Agent calls in one message run concurrently and return all results in the same turn. Reliable and simple.
- **Background** (`run_in_background: true`): The model must later retrieve results via `TaskOutput` or `SendMessage`, which frequently fails with "Invalid tool parameters" — causing agent output to be silently lost. Only use background agents when the main thread has genuinely independent work to do and does not need the agent's output to proceed.

- ✗ **Avoid**: "Launch all four agents concurrently in a single message."
- ✗ **Avoid**: "Spawn a subagent to review the output."
- ✓ **Good**: "Launch all four agents in a single message (`model: "opus"`, do not set `run_in_background`)."

#### Phrase Multi-Agent Parallel Dispatch Imperatively

Tool calls within a single assistant message run concurrently. Tool calls across separate messages run sequentially. To fan out N Agents in parallel, emit one assistant message containing N Agent tool calls.

Write the dispatch step as one imperative sentence followed by uniform bulleted Agent roles:

> Use the Agent tool to launch all <N> agents below in a single assistant message so they run concurrently. Each Agent call uses `model: "opus"` and does not set `run_in_background`.

State the total call count as a number, even when a single bullet expands to multiple calls (e.g., "one Agent per active type, expect <N> total"). The number anchors the fan-out so the full set goes out in one batch.

When the items being parallelized are themselves skills, each parallel item is an Agent tool call whose prompt invokes the target skill via the Skill tool. The Agent fan-out parallelizes; the Skill load is the work each Agent does.

#### Hoist Conditional Opt-Out Checks Above Dispatch Logic

When a step has a conditional opt-out (e.g., "skip peer review" reduces N+1 to N Agents), put the check at the top of the step before describing the dispatch. If the opt-out subsection appears after the per-Agent subsections, a reader plans the full dispatch and only learns about the opt-out after — easy to ignore at execution time.

- ✗ **Avoid**: Describe Agent A, Agent B, Agent C — then add a final "Skipping C" subsection.
- ✓ **Good**: Open the step with "Determine whether to skip C: if the caller asked to skip, set the dispatch to A+B; otherwise A+B+C." Then describe each Agent.

#### Skill Tool Calls Don't Parallelize with Agent Calls

The Skill tool loads instructions and returns immediately — the actual work (Bash calls, agent spawns, etc.) happens in subsequent turns, after any parallel Agent calls have already completed. To truly parallelize a skill's work with other agents, wrap it in an Agent that loads and executes the skill internally.

- ✗ **Avoid**: Launching Agent + Agent + Skill in one message expecting all three to do work concurrently.
- ✓ **Good**: Launching three Agents in one message, each running its respective skill.

### Dispatching Bash Tool Calls

When a skill's Bash invocation needs non-default parameters (`timeout`, `dangerouslyDisableSandbox`), specify them in a parenthetical the same way as for Agent calls. Vague phrasing like "use a generous timeout" leaves Claude to guess which timeout (Bash tool parameter vs. shell `timeout` command) and what value.

- ✗ **Avoid**: "Use a generous timeout."
- ✗ **Avoid**: "Wrap the command in a shell `timeout` of 1 hour: `timeout 3600 X`."
- ✓ **Good**: "Run X via the Bash tool (`timeout: 3600000`, do not set `run_in_background`)."

The parenthetical names parameters and values directly, parallel to (`model: "opus"`, do not set `run_in_background`) for Agent calls. Specify whatever value the operation actually requires in milliseconds. Documented timeout ceilings are not enforced as hard limits. Reach for a shell wrapper like GNU `timeout` only when the Bash tool's parameter cannot achieve the goal.

### Using AskUserQuestion

When a skill needs user input, reference the tool by name (`AskUserQuestion`) instead of vague phrasing like "ask the user" or "wait for user confirmation." Naming the tool directly ensures the executing Claude instance uses the right mechanism.

- ✗ **Avoid**: "Ask the user which option they prefer."
- ✓ **Good**: "Use `AskUserQuestion` to determine which option the user prefers."

#### Output Content as Text Before AskUserQuestion

When a skill presents structured content (tables, plans, reports) before asking for approval, output the content as text first. `AskUserQuestion` has limited UI space and should only carry the approval prompt, not the content being reviewed.

- ✗ **Avoid**: "Present the test plan to the user with `AskUserQuestion` before executing."
- ✗ **Avoid**: "Show the drafted context to the user via `AskUserQuestion` for approval."
- ✓ **Good**: "Output the plan as text. Then use `AskUserQuestion` to ask for approval."

#### Prefer AskUserQuestion Gates over Anti-Skip Prose Rules

Workflow skills often need to prevent the agent from skipping steps ("don't rationalize away the re-run") or stopping early at iteration caps. Verbose "Do NOT" blocks and anti-rationalization prose are unreliable: the agent reads the rule and still finds ways to rationalize around it. Convert soft rules into hard gates using `AskUserQuestion`.

- **Skip gate**: When the agent might want to skip a re-run that should happen (e.g., changes were made but the agent judges re-running unnecessary), require it to use `AskUserQuestion` to request skip permission. This converts "don't skip silently" into "can't skip silently."
- **Exhaustion gate**: When a loop reaches its iteration cap but hasn't stabilized, use `AskUserQuestion` to ask whether to continue for another iteration or escalate to a different approach. This replaces the hard stop with a human-in-the-loop decision.
- **Blocker gate**: When a step is blocked by a missing dependency, unclear requirement, or environmental issue that needs user input to resolve, use `AskUserQuestion` to surface the blocker and let the user choose how to proceed. Phrasing like "halt and report" or "stop" leaves no recovery path; an `AskUserQuestion` gate keeps the workflow live.

```markdown
**If changes were made**, run `/this-skill` again using the Skill tool.

**If changes were made but you believe re-running is unnecessary**, use `AskUserQuestion` to ask for skip permission. Do not skip silently.

**If this is iteration 3 and changes were still made**, the hard cap is reached. Use `AskUserQuestion` to tell the user that 3 iterations were not enough to stabilize, summarize what is still changing, and offer two options: continue for another iteration, or escalate to a different approach for the remaining issues.
```

Removing verbose "Do NOT" blocks and "Rules" sections that restate the anti-skip rule often wins alongside adding the gates: the prose was unreliable anyway, and the gates replace it with enforceable behavior.

#### AskUserQuestion Doesn't Work in Sub-Agents

`AskUserQuestion` only reaches the user when the skill runs in the main conversation. When a skill runs inside an `Agent` tool call, the question cannot be surfaced — the sub-agent either errors or drops the call silently. Skills that commonly run as sub-agents (invoked by workflow skills that fan out via the Agent tool) need deterministic fallbacks instead of interactive questions.

- **Missing input** — stop and state what could not be resolved. The parent agent reads the sub-agent's output and can relay or act on it.
- **Disambiguation** — pick a deterministic default (e.g., most recently modified file) rather than asking which option to use.
- **Main-context-only fallbacks** — a sub-agent can in principle self-detect via system-prompt phrasing and branch on whether to call `AskUserQuestion`, but the cost of that branching is usually worse than just removing the question entirely.

### Referencing MCP Tools

When referencing a *specific known* MCP (Model Context Protocol) tool, always use fully qualified tool names to avoid "tool not found" errors.

**Format**: `ServerName:tool_name`

**Example**:
```markdown
Use the BigQuery:bigquery_schema tool to retrieve table schemas.
Use the GitHub:create_issue tool to create issues.
```

Where `BigQuery` and `GitHub` are MCP server names and `bigquery_schema` and `create_issue` are the tool names within those servers. Without the server prefix, Claude may fail to locate the tool, especially when multiple MCP servers are available.

When a skill needs a *category* of tool rather than a specific one (e.g., documentation lookup), reference the category generically. Different projects have different MCP servers installed.

- ✗ **Avoid**: "Use the context7 MCP to look up library docs."
- ✓ **Good**: "Use documentation MCP tools or WebSearch to look up library docs."

## Evaluation and Iteration

### Build Evaluations First

**Create evaluations BEFORE writing extensive documentation.** This ensures your Skill solves real problems rather than documenting imagined ones.

**Evaluation-driven development:**
1. **Identify gaps**: Run Claude on representative tasks without a Skill. Document specific failures or missing context
2. **Create evaluations**: Build three scenarios that test these gaps
3. **Establish baseline**: Measure Claude's performance without the Skill
4. **Write minimal instructions**: Create just enough content to address the gaps and pass evaluations
5. **Iterate**: Execute evaluations, compare against baseline, and refine

This approach ensures you're solving actual problems rather than anticipating requirements that may never materialize.

**Evaluation structure**:
```json
{
  "skills": ["pdf-processing"],
  "query": "Extract all text from this PDF file and save it to output.txt",
  "files": ["test-files/document.pdf"],
  "expected_behavior": [
    "Successfully reads the PDF file using an appropriate PDF processing library or command-line tool",
    "Extracts text content from all pages in the document without missing any pages",
    "Saves the extracted text to a file named output.txt in a clear, readable format"
  ]
}
```

> **Note:** This example demonstrates a data-driven evaluation with a simple testing rubric. There is not currently a built-in way to run these evaluations. Users can create their own evaluation system. Evaluations are your source of truth for measuring Skill effectiveness.

### Develop Skills Iteratively with Claude

The most effective Skill development process involves Claude itself. Work with one instance ("Claude A") to design and refine the Skill, and test it with a fresh instance ("Claude B") on real tasks. Claude A understands agent needs; Claude B reveals gaps through real usage.

1. **Complete a task without a Skill** with Claude A. Notice what context you repeatedly provide.
2. **Ask Claude A to create the Skill**, capturing that context. Claude understands the Skill format natively and will generate properly structured SKILL.md content.
3. **Review for conciseness** and information architecture. Ask Claude A to remove explanations Claude already knows, and to split reference content into separate files when it grows.
4. **Test with Claude B** (a fresh instance with the Skill loaded) on related tasks. Observe whether it finds the right information, applies rules correctly, and succeeds.
5. **Return to Claude A with specifics** when Claude B struggles: "It forgot to filter by date — should we make that more prominent?" Apply refinements, then test again.
6. **Gather team feedback**: share with teammates and ask whether the Skill activates when expected, whether instructions are clear, and what's missing.

### Observe How Claude Navigates Skills

As you iterate on Skills, pay attention to how Claude actually uses them in practice. Watch for:

- **Unexpected exploration paths**: Does Claude read files in an order you didn't anticipate? This might indicate your structure isn't as intuitive as you thought
- **Missed connections**: Does Claude fail to follow references to important files? Your links might need to be more explicit or prominent
- **Overreliance on certain sections**: If Claude repeatedly reads the same file, consider whether that content should be in the main SKILL.md instead
- **Ignored content**: If Claude never accesses a bundled file, it might be unnecessary or poorly signaled in the main instructions

Iterate based on these observations rather than assumptions. The 'name' and 'description' in your Skill's metadata are particularly critical. Claude uses these when deciding whether to trigger the Skill in response to the current task. Make sure they clearly describe what the Skill does and when it should be used.

## Skills with Executable Code

The sections below focus on Skills that include executable scripts.

### Solve, Don't Punt

When writing scripts for Skills, handle error conditions rather than punting to Claude.

**Good example: Handle errors explicitly**:
```python
def process_file(path):
    """Process a file, creating it if it doesn't exist."""
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        # Create file with default content instead of failing
        print(f"File {path} not found, creating default")
        with open(path, "w") as f:
            f.write("")
        return ""
    except PermissionError:
        # Provide alternative instead of failing
        print(f"Cannot access {path}, using default")
        return ""
```

**Bad example: Punt to Claude**:
```python
def process_file(path):
    # Just fail and let Claude figure it out
    return open(path).read()
```

Configuration parameters should also be justified and documented to avoid "voodoo constants" (Ousterhout's law). If you don't know the right value, how will Claude determine it?

**Good example: Self-documenting**:
```python
# HTTP requests typically complete within 30 seconds
# Longer timeout accounts for slow connections
REQUEST_TIMEOUT = 30

# Three retries balances reliability vs speed
# Most intermittent failures resolve by the second retry
MAX_RETRIES = 3
```

**Bad example: Magic numbers**:
```python
TIMEOUT = 47  # Why 47?
RETRIES = 5  # Why 5?
```

### Provide Utility Scripts

Pre-made scripts are more reliable than generated code, save tokens (no need to include code in context), and ensure consistency. Claude can execute them without loading their contents into context.

Make clear whether Claude should **execute** the script (most common: "Run `analyze_form.py` to extract fields") or **read it as reference** for complex logic. Prefer execution.

````markdown
## Utility scripts

**analyze_form.py**: Extract all form fields from PDF

```bash
python scripts/analyze_form.py input.pdf > fields.json
```

Output format:
```json
{
  "field_name": {"type": "text", "x": 100, "y": 200},
  "signature": {"type": "sig", "x": 150, "y": 500}
}
```

**fill_form.py**: Apply field values to PDF

```bash
python scripts/fill_form.py input.pdf fields.json output.pdf
```
````

### Use Visual Analysis

When inputs can be rendered as images, have Claude analyze them:

````markdown
## Form layout analysis

1. Convert PDF to images:
   ```bash
   python scripts/pdf_to_images.py form.pdf
   ```

2. Analyze each page image to identify form fields
3. Claude can see field locations and types visually
````

> **Note:** In this example, you'd need to write the `pdf_to_images.py` script.

Claude's vision capabilities help understand layouts and structures.

### Create Verifiable Intermediate Outputs

For batch operations, destructive changes, or high-stakes work, use the **plan-validate-execute** pattern: Claude first creates a plan in a structured format (e.g., `changes.json`), a script validates the plan against reality, and only then is the plan executed. The workflow becomes: analyze → create plan file → validate plan → execute → verify.

This catches errors before any changes are applied, and lets Claude iterate on the plan without touching originals. Make validation errors specific ("Field 'signature_date' not found. Available fields: customer_name, order_total") so Claude can fix issues without guessing.

### Package Dependencies

Don't assume packages are available. Declare them explicitly with install commands:

````markdown
**Bad example: Assumes installation**:
"Use the pdf library to process the file."

**Good example: Explicit about dependencies**:
"Install required package: `pip install pypdf`

Then use it:
```python
from pypdf import PdfReader
reader = PdfReader("file.pdf")
```"
````

Skills run in the code execution environment with platform-specific limitations:

- **claude.ai**: Can install packages from npm and PyPI and pull from GitHub repositories
- **Claude API**: Has no network access and no runtime package installation

List required packages in your SKILL.md and verify they're available in your execution environment.

### Runtime Environment

- **Scripts produce output, not context**: Utility scripts can be executed via bash without loading their contents into context. Only the script's output consumes tokens.
- **Name files descriptively**: Use names that indicate content: `form_validation_rules.md`, not `doc2.md`
- **Bundle comprehensive resources**: Include complete API docs, extensive examples, large datasets; no context penalty until accessed
- **Test file access patterns**: Verify Claude can navigate your directory structure by testing with real requests

For complete details on the technical architecture, see the Skills overview on platform.claude.com.
