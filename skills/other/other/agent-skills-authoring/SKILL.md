---
name: agent-skills-authoring
description: >-
  Guides agents through creating, validating, and optimizing Agent Skills (SKILL.md files)
  from user requests. Covers all YAML frontmatter fields, directory layout, progressive
  disclosure, scripts, quality patterns, and evaluation workflows. Use when a user asks you
  to create, edit, audit, or improve an Agent Skill, even if they don't use the word "skill"
  — any request about reusable agent instructions, workflow packaging, or capability extension
  should trigger this skill.
license: MIT
compatibility: >-
  Any AI agent generating SKILL.md files. Compatible with the Agent Skills open standard
  (agentskills.io), Claude Code, Claude.ai, and the Claude API.
metadata:
  spec-version: "1.4"
  sources: "agentskills.io/specification, docs.anthropic.com, github.com/anthropics/skills"
  audience: "ai-agents"
allowed-tools: Bash(skills-ref:*) Read Write
---

# Agent Skills Authoring Guide

This is your authoritative reference for producing high-quality SKILL.md files. When a user
asks you to create, edit, or improve a skill, follow these instructions to produce the best
possible result — one that any consuming agent can discover, activate, and apply effectively.

---

## 1. Core Principles

These principles come from Anthropic's official best practices. Apply them to every skill.

**Claude is already very smart.** Only add context Claude doesn't already have. Challenge
each piece of content: "Does Claude really need this explanation?" "Can I assume Claude
knows this?" "Does this paragraph justify its token cost?" Concise skills perform better
because the context window is shared with conversation history, system prompts, and other
skills' metadata.

**Explain WHY, not just WHAT.** Anthropic's guidance: "Explain to the model why things are
important in lieu of heavy-handed musty MUSTs." When agents understand reasoning, they
generalize correctly across novel situations. Rigid imperative-only rules cause brittle,
over-literal behavior.

**Match specificity to fragility.** Use high freedom (general text guidance) when multiple
approaches are valid. Use medium freedom (pseudocode/parameterized scripts) when a preferred
pattern exists. Use low freedom (exact scripts, no modifications) when operations are fragile
and consistency is critical. Think of it as: narrow bridge (one safe path, give exact steps)
vs. open field (many valid routes, give direction and trust the agent).

**Use consistent terminology.** Pick one term and use it throughout. Don't mix "API endpoint"
/ "URL" / "path" or "extract" / "pull" / "get" / "retrieve" in the same skill.

---

## 2. Directory Structure

```
skill-name/
├── SKILL.md          # REQUIRED — frontmatter + instructions
├── scripts/          # Optional — executable code (runs without loading into context)
│   └── validate.py
├── references/       # Optional — docs loaded on demand
│   ├── REFERENCE.md
│   └── domain.md
└── assets/           # Optional — templates, data files, schemas
    └── template.json
```

- Directory name must match the `name` field in frontmatter exactly
- `scripts/` — self-contained executables. Handle errors explicitly ("solve, don't punt").
  Scripts execute via bash and only their output enters context, not their code
- `references/` — additional docs loaded on demand. Keep files focused. Add a table of
  contents at the top of any reference file over 100 lines
- `assets/` — static resources: templates, configuration files, schemas, lookup tables
- Use forward slashes in all paths, even on Windows: `scripts/validate.py` not `scripts\validate.py`

**Domain organization:** For skills supporting multiple variants, split into references:

```
cloud-deploy/
├── SKILL.md           # Overview + variant selection
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```

The agent loads only the relevant reference, saving context.

---

## 3. YAML Frontmatter — Complete Field Reference

### Base Spec Fields (agentskills.io)

The open standard defines exactly **six fields**:

#### `name` (REQUIRED)

Unique identifier. 1–64 chars. Lowercase alphanumeric + hyphens only.
No leading/trailing/consecutive hyphens. No XML tags. Cannot contain reserved words
"anthropic" or "claude". Must match the parent directory name.

**Prefer gerund naming** (verb + -ing): `processing-pdfs`, `analyzing-spreadsheets`,
`testing-code`. Also acceptable: noun phrases (`pdf-processing`) or action-oriented
(`process-pdfs`). Avoid vague names (`helper`, `utils`, `tools`).

```yaml
name: processing-pdfs
```

#### `description` (REQUIRED)

Natural-language summary. 1–1,024 chars. Plain text only. No XML tags.
This is the primary triggering mechanism — agents use it to decide which skills to load.

**Always write in third person.** "Processes Excel files..." not "I can help you..." or
"You can use this..." (inconsistent POV causes discovery problems).

**Make descriptions slightly "pushy."** Claude tends to undertrigger skills. Include both
what the skill does AND specific trigger contexts. List keywords users would say. Add
"even if they don't explicitly ask for X" where appropriate.

```yaml
description: >-
  Extracts text and tables from PDF files, fills forms, and merges documents.
  Use when working with PDF files or when the user mentions PDFs, forms, or
  document extraction, even if they don't explicitly ask for "PDF processing."
```

#### `license` (OPTIONAL)

SPDX identifier or bundled file reference. Omit if unknown.

#### `compatibility` (OPTIONAL)

Environment requirements. 1–500 chars. Plain text. Only include if the skill has
genuine requirements — most skills don't need this field.

#### `metadata` (OPTIONAL)

String key-value map. Use reasonably unique key names to avoid collisions.

```yaml
metadata:
  author: "your-org"
  version: "1.0"
  category: "document-processing"
```

#### `allowed-tools` (OPTIONAL, EXPERIMENTAL)

Space-delimited list. Use scoped format where the platform supports it.

```yaml
allowed-tools: Bash(git:*) Bash(jq:*) Read Write
```

### Claude Code Extended Fields

Claude Code extends the open standard with additional fields. These are platform-specific
and not part of the base agentskills.io spec:

| Field                      | Purpose                                                      |
| -------------------------- | ------------------------------------------------------------ |
| `argument-hint`            | Autocomplete hint: `[issue-number]` or `[filename] [format]` |
| `disable-model-invocation` | `true` to prevent auto-loading (manual `/name` only)         |
| `user-invocable`           | `false` to hide from / menu (background knowledge skills)    |
| `model`                    | Model override when this skill is active                     |
| `context`                  | `fork` to run in a forked subagent context                   |
| `agent`                    | Subagent type to use when `context: fork` is set             |
| `hooks`                    | Hooks scoped to this skill's lifecycle                       |

In Claude Code, `name` falls back to directory name if omitted, and `description` falls
back to the first paragraph of the markdown body.

---

## 4. Body Content

Everything after the closing `---` is free-form Markdown. Keep the body under **500 lines**.
If approaching this limit, move detail into `references/` and add clear pointers.

### Recommended Structure

```markdown
# [Skill Name]

[1-3 sentence overview]

## When to use this skill

[Trigger conditions — what user requests or contexts activate this]

## How to [primary action]

[Step-by-step instructions]

## Examples

[Input/output pairs]

## Common edge cases

[Boundary conditions and handling]

## Guidelines

[Key principles with reasoning]
```

### Progressive Disclosure

| Level | Content                          | Budget                    | When Loaded                |
| ----- | -------------------------------- | ------------------------- | -------------------------- |
| 1     | Frontmatter (name + description) | ~100 tokens               | Always — at agent startup  |
| 2     | SKILL.md body                    | < 500 lines / < 5K tokens | When skill activates       |
| 3     | scripts/, references/, assets/   | Unlimited                 | On demand during execution |

Level 3 scripts execute without loading into context — only their output enters the
context window. Reference files are read on demand. This means you can bundle
comprehensive resources with no context penalty until they're accessed.

### File References

Use standard Markdown links with relative paths:

```markdown
See [the reference guide](references/REFERENCE.md) for detailed API documentation.
Run the extraction script: `python scripts/extract.py`
For TypeScript specifics, see [TypeScript patterns](references/typescript.md).
```

Keep references **one level deep** from SKILL.md. Avoid nested reference chains —
Claude may partially read files referenced from other referenced files.

### Script Guidance

When referencing scripts, be explicit about intent:

- **Execute** (most common): "Run `scripts/analyze.py` to extract fields"
- **Read as reference** (for complex logic): "See `scripts/analyze.py` for the algorithm"

Scripts should handle errors explicitly. Don't let scripts fail and expect Claude to
figure it out — provide fallbacks, helpful error messages, and document dependencies.

For MCP tools, use fully-qualified references: `ServerName:tool_name` (e.g.,
`BigQuery:bigquery_schema`, `GitHub:create_issue`).

---

## 5. Creating a Skill from a User Request

### Step 1: Capture Intent

Understand what the user needs before writing anything:

- What should this skill enable an agent to do?
- When should it trigger? (phrases, tasks, contexts)
- What's the expected output format?
- Are there edge cases or constraints?
- Does this need testing? (Verifiable outputs benefit from evals; subjective outputs
  like writing style often don't)

If the conversation already contains a workflow ("turn this into a skill"), extract
answers from context first — tools used, step sequence, corrections the user made.

### Step 2: Choose the Name

Prefer gerund form: `{verb-ing}-{noun}` → `processing-pdfs`, `testing-code`.
Validate: lowercase, hyphens only, 1-64 chars, no leading/trailing/consecutive hyphens,
no XML tags, no "anthropic" or "claude" in the name.

### Step 3: Write the Description

Third person always. Start with action verb. Include keyword triggers. State "Use when..."
Make it slightly pushy to prevent undertriggering. Aim for 200-400 characters.

### Step 4: Set Optional Fields

- **license:** User-specified, or `MIT`/`Apache-2.0`, or omit
- **compatibility:** Only if genuine environment requirements exist
- **metadata:** Add `author`, `version`, `category` at minimum
- **allowed-tools:** Use scoped format: `Bash(git:*) Read`
- **Claude Code fields:** Set `disable-model-invocation`, `argument-hint`, etc. if relevant

### Step 5: Write the Body

Start with a draft. Then review with fresh eyes and improve.

- 1-3 sentence overview
- "When to use this skill" with trigger conditions
- Step-by-step instructions explaining WHY, not just WHAT
- Input/output examples (crucial for quality)
- Edge cases
- For complex workflows: provide a copyable checklist Claude can check off as it progresses

Provide a **default approach with an escape hatch** rather than listing many options.
"Use pdfplumber for text extraction. For scanned PDFs requiring OCR, use pdf2image instead."

### Step 6: Iterate (Eval-First)

Anthropic's recommended pattern uses two Claude instances:

1. **Establish baseline** — run Claude on representative tasks WITHOUT the skill
2. **Write minimal draft** — only enough to address observed gaps
3. **Test with Claude B** — a fresh instance with the skill loaded on 2-3 realistic prompts
4. **Observe Claude B's behavior** — note where it struggles or misses instructions
5. **Return to Claude A** to refine — share what you observed, ask for improvements
6. **Repeat** until satisfied, then expand the test set

This is evaluation-driven development: create evals BEFORE writing extensive documentation.
Test without the skill first, then with the skill, and measure the improvement.

### Step 7: Validate

- Directory name matches `name` field exactly
- Description: 1-1,024 chars, third person, action verb, keyword triggers, "Use when..."
- No XML tags in name or description
- All Markdown links resolve to files that exist
- SKILL.md body under 500 lines
- Reference files over 100 lines have a table of contents
- Run `skills-ref validate ./skill-directory` if available
- Run `skills-ref to-prompt ./skill-directory` to preview the XML agents see

---

## 6. Quality Patterns

### Phased Workflows

```markdown
## Phase 1: Analyze

[Understand the domain, gather context]

## Phase 2: Implement

[Execute the primary task]

## Phase 3: Validate

[Check quality, run validation]
```

### Feedback Loops

The run-validate-fix pattern dramatically improves output quality:

```markdown
1. Make changes
2. Run: `python scripts/validate.py`
3. If validation fails: fix and return to step 1
4. Only proceed when validation passes
```

### Copyable Checklists

For complex multi-step tasks:

```markdown
Copy this checklist and track progress:

- [ ] Step 1: Analyze input
- [ ] Step 2: Create plan
- [ ] Step 3: Validate plan
- [ ] Step 4: Execute
- [ ] Step 5: Verify output
```

### Verifiable Intermediate Outputs

For high-stakes operations: plan → validate plan → execute → verify.
The plan file is machine-verifiable before changes are applied.

### Decision Tables

| Scenario      | Approach          | Why                    |
| ------------- | ----------------- | ---------------------- |
| < 100 items   | Inline array      | No pagination overhead |
| 100-10K items | Cursor pagination | Stable ordering        |
| > 10K items   | Keyset pagination | O(1) page fetch        |

### Before/After Examples

```markdown
**Before:** `app.get('/getUser', ...)`
**After:** `app.get('/users/:id', ...)`
```

---

## 7. Anti-Patterns

| Anti-Pattern                    | Why It Fails                        | Fix                                         |
| ------------------------------- | ----------------------------------- | ------------------------------------------- |
| Vague description               | Agents can't match to requests      | Keyword triggers + "Use when..." + be pushy |
| First/second person description | Discovery problems                  | Third person: "Processes..." not "I can..." |
| Over-explaining basics          | Wastes tokens; Claude already knows | Only add what Claude doesn't have           |
| Too many options                | Confusing; agent may pick wrong one | Default approach + escape hatch             |
| Rigid MUST-only rules           | Brittle; agents over-literalize     | Explain reasoning so agent generalizes      |
| Body over 500 lines             | Context waste, agent may truncate   | Move detail to `references/`                |
| Code in description             | Violates spec, breaks parsers       | Code in body only                           |
| Nested file references          | Claude partially reads deeper files | One level deep from SKILL.md                |
| Name with "anthropic"/"claude"  | Reserved words; validation fails    | Choose different name                       |
| Backslash paths                 | Break on Unix systems               | Forward slashes always                      |
| Time-sensitive info             | Becomes wrong; no auto-update       | Use "old patterns" section                  |
| No examples                     | Agent guesses output format         | 2-3 input/output pairs minimum              |

---

## 8. Security

- Never include secrets, API keys, or credentials in any skill file
- Never instruct agents to disable security controls
- Scripts should handle errors explicitly with fallbacks
- Include input validation guidance for skills handling user data
- Include sanitization guidance for skills generating browser-rendered output
- Flag destructive tools in `allowed-tools` so users can review

---

## 9. Testing

1. **Syntax:** `skills-ref validate ./skill-name`
2. **Prompt preview:** `skills-ref to-prompt ./skill-name` — generates XML agents see
3. **Activation test:** Prompt that SHOULD trigger → confirm it fires
4. **Negative test:** Prompt that should NOT trigger → confirm it stays dormant
5. **Quality test:** Agent executes skill → review output quality
6. **Multi-model test:** Test with Haiku, Sonnet, AND Opus — what works for Opus may need more detail for Haiku

For verifiable outputs, create structured evaluations comparing with-skill vs without-skill.

---

## 10. Platform Usage

- **Claude Code:** `/plugin marketplace add anthropics/skills` → `/plugin install <name>@anthropic-agent-skills`
  - Skills at: `~/.claude/skills/` (personal) or `.claude/skills/` (project)
- **Claude.ai:** Pre-built skills on paid plans. Custom skills uploaded via settings
- **Claude API:** Container parameter with `skills-2025-10-02` beta flag

---

## 11. Resources

| Resource                             | URL                                                                             |
| ------------------------------------ | ------------------------------------------------------------------------------- |
| Agent Skills Specification           | https://agentskills.io/specification                                            |
| Anthropic Skills Repo (79.5K+ stars) | https://github.com/anthropics/skills                                            |
| **Anthropic Best Practices**         | https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/best-practices |
| Claude Code Skills Docs              | https://docs.anthropic.com/en/docs/claude-code/skills                           |
| skills-ref CLI                       | https://agentskills.io/tools                                                    |

---

## 12. Pre-Delivery Checklist

### Frontmatter

- [ ] `name`: 1-64 chars, lowercase alphanum + hyphens, gerund preferred, matches directory
- [ ] `name`: no XML tags, no "anthropic"/"claude"
- [ ] `description`: 1-1,024 chars, third person, action verb, trigger keywords, "Use when..."
- [ ] `description`: slightly pushy to prevent undertriggering
- [ ] Optional fields set where relevant — no invented fields

### Body

- [ ] 1-3 sentence overview
- [ ] Trigger section explaining when this skill activates
- [ ] Instructions explain WHY, not just WHAT
- [ ] 2-3 input/output examples minimum
- [ ] Edge cases covered
- [ ] Under 500 lines, pure Markdown
- [ ] Consistent terminology throughout

### Files

- [ ] All Markdown links resolve to real files, one level deep
- [ ] Reference files >100 lines have table of contents
- [ ] Scripts handle errors explicitly with helpful messages
- [ ] No secrets in any file
- [ ] Forward slashes in all paths

### Quality

- [ ] Description alone determines relevance
- [ ] Body alone enables execution without reading references
- [ ] Tested with representative prompts (activation + negative + quality)
- [ ] A real user would find the output useful, not just spec-compliant
