---
name: claude-skill-builder
description: Guides creation and improvement of Claude Code skills using Anthropic's official
  methodology. Use when user wants to "create a skill", "build a skill", "make a new skill",
  "write a new skill", "improve an existing skill", "audit my skill", "refine my skill",
  "test a skill", "package a skill for distribution", or needs guidance on skill structure,
  progressive disclosure, description quality, testing, or distribution.
version: 1.1.0
allowed-tools: Read Write Edit Bash Glob Grep WebSearch WebFetch
---

# Claude Skill Builder

Build Claude Code skills following Anthropic's official methodology — from planning through
distribution.

**PRIMARY SOURCE**: "The Complete Guide to Building Skills for Claude" (Anthropic, January 2026)
- PDF: https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf
- Local copy: `./claude-skill-builder-guide.pdf`

---

## Quick Start

To create a skill from scratch, follow the 4-phase process below.
To improve an existing skill, read `references/refining-skills.md`.
To validate a skill's structure, run `scripts/audit-skill.sh`.

**Invoke with:** `/claude-skill-builder` or ask about creating, improving, or auditing a skill.

---

## How It Works

Four-phase methodology from the Anthropic guide:

| Phase | Activity | Time |
|-------|----------|------|
| 1: Planning & Design | Define use cases, category, success criteria | 15-30 min |
| 2: Implementation | Create folder, write SKILL.md, add resources | 30-60 min |
| 3: Testing | Triggering, functional, performance tests | 20-40 min |
| 4: Distribution | Package, document, publish to GitHub | 10-20 min |

**Total**: ~75-150 minutes for a complete, tested skill

Phase 1 covers Steps 1–2 below; Phases 2–4 correspond to Steps 3–5.

---

## Skill Creation Workflow

### Step 1: Discover Requirements

**Research the domain first** — before writing instructions, verify current best practices
for the skill's subject. Use `WebSearch` and `WebFetch` to check official docs, community
standards, and authoritative examples. Outdated or incorrect guidance in a skill is worse
than no guidance: Claude will follow it confidently.

**Retain all sources**: every URL consulted must be recorded in the skill with its full
link and a note of what it confirmed. Without sources, guidance cannot be verified or
updated when the domain changes.

For research strategies, source quality standards, and the required Sources section
format: `references/research.md`

1. Identify the problem and target users
2. Define 2-3 concrete use cases
3. Set measurable success criteria (time saved, errors reduced, quality improved)
4. Choose a skill category:

| Category | INPUT → OUTPUT | Examples |
|----------|---------------|---------|
| **1: Document & Asset Creation** | Data/specs → document, code, report | API test generator, meeting notes summarizer |
| **2: Workflow Automation** | Task params → completed multi-step process | Deploy pipeline, code review workflow |
| **3: MCP Enhancement** | MCP tool outputs → smarter orchestration | Smart file search, BigQuery assistant |

For in-depth category guidance: `references/categories.md`
For interactive discovery questions: `references/discovery.md`

### Step 2: Design Structure

Design using progressive disclosure — 3 loading levels:

| Level | When loaded | Target length | Content |
|-------|------------|---------------|---------|
| 1: Metadata | Always (~100 words) | name + description | Trigger conditions |
| 2: SKILL.md body | When skill triggers | under 5,000 words (ideally under 2,000) | Core workflow + pointers |
| 3: references/ files | As needed | Unlimited | Deep detail, schemas, examples |

For progressive disclosure writing tips and success metrics: `references/best-practices.md`

### Step 3: Implement

**Critical Rules:**
- ✅ File MUST be named `SKILL.md` (not README.md)
- ✅ Folder name MUST be **kebab-case** — no spaces, no capitals (`my-skill` not `My Skill`)
- ✅ YAML frontmatter MUST include `name`, `description`, and `version` fields
- ✅ Description MUST include specific trigger phrases — what users SAY to activate the skill
- ✅ Description must be **under 1024 characters** (hard limit — longer descriptions are truncated)
- ✅ No XML angle brackets (`<` or `>`) in any frontmatter field
- ❌ NO README.md inside the skill folder — all docs go in SKILL.md or references/
  (Exception: a README.md at the GitHub repo ROOT, outside the skill folder, is fine for GitHub.)
- ❌ NO spaces or underscores in folder names (`my_skill` → `my-skill`)

**Frontmatter: required fields**:
```yaml
---
name: your-skill-name          # kebab-case only; no spaces, capitals, or underscores
description: What it does. Use when user asks to "specific phrase", "another phrase".
             # MUST include: what it does + when to use it (trigger conditions)
             # Under 1024 characters. No XML angle brackets.
             # Do NOT start with "claude" or "anthropic" (reserved namespaces).
version: 0.1.0                 # Required; use semantic versioning
---
```

**Frontmatter: all optional fields**:
```yaml
---
name: your-skill-name
description: What it does and when. Use when user says "trigger phrase 1", "trigger phrase 2".
license: MIT                   # Optional: open-source license (MIT, Apache-2.0, etc.)
allowed-tools: "Bash(python:*) WebFetch"  # Optional: restrict which tools the skill can use
compatibility: Claude Code     # Optional: 1-500 chars; environment requirements
metadata:                      # Optional: custom key-value pairs
  author: Your Name
  version: 1.0.0               # Version inside metadata (Anthropic's spec); also accepted at top level
  mcp-server: your-server      # If skill requires a specific MCP server
  category: productivity
  tags: [automation, workflow]
  documentation: https://example.com/docs
---
```

**Positioning language** (outcome-focused: "generate tests 87% faster") belongs in README.md or
GitHub landing page — NOT in the description field. See `references/best-practices.md`.

**Folder structure (standalone skills at `~/.claude/skills/`):**
```
~/.claude/skills/your-skill-name/
├── SKILL.md                         # Required — loaded when skill triggers (<5k words)
├── references/                      # Docs Claude loads into context as needed
│   ├── detailed-guide.md            #   schemas, API docs, policies, detailed workflows
│   └── examples/                    #   working code users copy (subdirectory of references/)
│       └── working-example.sh
├── scripts/                         # Executables (run without loading into context)
│   └── validate.sh
└── assets/                          # Files used IN skill output (not loaded to context)
    └── template.html
```

| Directory | Load into context? | Use for |
|-----------|-------------------|---------|
| `references/` | Yes, as needed | Schemas, API docs, policies, workflow guides |
| `references/examples/` | As needed | Working code users copy and adapt |
| `scripts/` | No (run directly) | Validators, scaffolders, utilities |
| `assets/` | No (used in output) | Images, fonts, HTML templates the skill pastes into output |

Note: Plugin skills (in `plugin-name/skills/`) may place `examples/` at the top level — that is
plugin-dev convention. For standalone `~/.claude/skills/` skills, put examples inside `references/`.

To scaffold a new skill: `bash scripts/scaffold-skill.sh my-skill-name`
To start from template: copy `references/examples/SKILL-template.md`

### Step 4: Test

Three testing approaches (run in order):

1. **Triggering tests** — verify Claude activates on expected phrases; does NOT activate on unrelated requests
2. **Functional tests** — validate the skill's core workflow produces correct output for known inputs
3. **Performance tests** — measure improvement over baseline (time saved, error reduction, consistency)

**Debugging trigger issues**:
```
Ask Claude: "When would you use the [skill name] skill?"
```
Claude will quote its description back at you. Adjust based on what's missing or too vague.

**Fixing undertriggering**: Add more specific trigger phrases and relevant technical terms.

**Fixing overtriggering**: Add negative triggers to the description:
```yaml
description: Processes PDF legal documents for contract review. Use for "review this contract",
  "analyze legal document", "extract contract clauses". Do NOT use for general PDF viewing,
  image extraction, or non-legal documents (use doc-converter skill instead).
```

To validate skill structure, naming, and frontmatter:
```bash
bash ~/.claude/skills/claude-skill-builder/scripts/audit-skill.sh ~/.claude/skills/YOUR-SKILL
```

For automated quality review, use the built-in `skill-creator` skill:
```
"Use the skill-creator skill to review this skill and suggest improvements"
```
Also available: the `skill-reviewer` agent from the plugin-dev plugin checks description quality.

For detailed test case templates and the Testing Triangle methodology: `references/testing.md`

### Step 5: Distribute

**Three distribution channels** (choose one or all):

**A. Claude.ai / Claude Code (individual install)**
```bash
# Clone into Claude Code skills directory:
cd ~/.claude/skills && git clone https://github.com/username/your-skill-name
# Or: download ZIP → upload in Claude.ai Settings > Capabilities > Skills
```

**B. Organization-wide deployment** (admins only, shipped Dec 2025)
Admins can deploy skills workspace-wide via Claude.ai admin console — automatic updates,
centralized management. Users get the skill without any install step.

**C. Programmatic / API**
Add skills to Messages API requests via `container.skills` parameter. Use the `/v1/skills`
endpoint to manage skills. Works with the Claude Agent SDK for building custom agents.

**GitHub setup for public distribution:**
1. Create a public repo — the skill folder IS the repo (or is nested inside it)
2. Add `README.md` at the repo root (OUTSIDE the skill folder) with installation instructions
   and outcome-focused positioning: "Generate tests 87% faster" (GitHub marketing, not SKILL.md)
3. Share in Claude Discord or communities

For full distribution guidance, GitHub templates, and community strategies: `references/distribution.md`

---

## Common Pitfalls

| Pitfall | ❌ Wrong | ✅ Correct |
|---------|---------|---------|
| File naming | `my_skill/README.md` | `my-skill/SKILL.md` |
| Description field | Outcome-focused: `"generates tests 87% faster"` | Trigger phrases: `"create a skill", "improve my skill"` |
| README positioning | Trigger phrases in GitHub README | Outcome-focused: `"generate tests 87% faster"` |
| No progressive disclosure | Monolithic wall of text | 3-level: hook (50-100w) → workflow (200-400w) → detail |
| No testing | Write → publish immediately | Triggering + functional + performance tests |
| Missing success criteria | "Build a skill that helps with APIs" | "Reduce API test writing time by 75%" |
| Feature-focused description | "Uses OpenAPI parser and Jinja2 templates" | Trigger phrases + concise capability summary |

---

## Refining Existing Skills

Signs a skill needs refinement:
- File named README.md or folder has underscores/capitals (P0 — Claude cannot find it)
- Missing YAML frontmatter (P0 — Claude cannot auto-activate it)
- Description is outcome-focused instead of trigger-phrase format (P1)
- SKILL.md is over 5,000 words (P0 — hard limit; Claude reports degraded quality above this)
- SKILL.md is over 2,000 words with no references/ files (P1 — detail belongs in references/)
- Wall of text with no progressive disclosure structure (P1)

For the complete 5-step refinement process (audit → prioritize → fix → validate → document),
migration scenarios, before/after examples, and performance tracking:
`references/refining-skills.md`

---

## Additional Resources

### Reference Files (loaded as needed by Claude)
- **`references/research.md`** — Research strategies before writing skill instructions:
  how to find authoritative sources, evaluate quality, and translate knowledge into skill content
- **`references/best-practices.md`** — Progressive disclosure writing tips, success metrics
  framework, Testing Triangle, common anti-patterns
- **`references/refining-skills.md`** — Complete 5-step refinement process with migration
  scenarios, before/after examples, and continuous improvement framework
- **`references/sources.md`** — Anthropic PDF guide URL, MCP docs, community links, full citations
- **`references/categories.md`** — In-depth guide to all 3 skill categories
  with characteristics, examples, and best practices for each
- **`references/discovery.md`** — Interactive 20-question guided Q&A for discovering skill
  requirements, design choices, and implementation plan
- **`references/testing.md`** — Detailed test case templates for triggering, functional, and
  performance testing with concrete examples
- **`references/distribution.md`** — GitHub setup guide, installation instructions template,
  positioning language, community sharing strategies
- **`references/patterns.md`** — 5 advanced patterns (sequential orchestration,
  multi-MCP coordination, iterative refinement, context-aware selection, domain intelligence)
- **`references/troubleshooting.md`** — Fix guide: skill doesn't trigger, triggers too often,
  instructions not followed, context overload
- **`references/changelog.md`** — Version history and improvement notes
- **`notes/2026_03_reliable_skill_usage_and_design.md`** — Community research on skill activation rates (250 sandboxed evals): keyword matching vs semantic, naming conventions, forced-eval hooks, description template patterns

### Scripts (run directly — do not load into context)
- **`scripts/audit-skill.sh`** — Skill structure smoke test with scored output (0-100%)
  ```bash
  bash ~/.claude/skills/claude-skill-builder/scripts/audit-skill.sh ~/.claude/skills/YOUR-SKILL
  ```
- **`scripts/scaffold-skill.sh`** — Create a new skill directory with correct structure
  ```bash
  bash ~/.claude/skills/claude-skill-builder/scripts/scaffold-skill.sh my-skill-name
  ```

---

## Version History

**v1.1.0** - 2026-03-05
- Added YAML frontmatter (enables Claude auto-detection)
- Rewrote body to imperative form throughout
- Integrated IMPROVEMENTS.md self-critique (moved to references/changelog.md)
- Corrected description templates: trigger-phrase format for SKILL.md, outcome-focused for README
- Trimmed SKILL.md from 932 → ~350 lines; moved detail to references/
- Corrected directory taxonomy: references/examples/ for standalone skills (Anthropic's recommended structure)
- Corrected README.md rule: enforce "no README inside skill folder" with distribution exception
- Added description field constraints: 1024-char hard limit, no angle brackets, kebab-case names
- Added Additional Resources section linking all references/ files and scripts/
- Created references/patterns.md with 5 advanced patterns + troubleshooting from Anthropic's guide
- Confirmed skill categories are from Anthropic's official guide — no "unofficial" label

**v1.0.0** - Initial release based on Anthropic's Complete Guide
- Complete 4-phase methodology
- Progressive disclosure templates
- Testing framework
- Distribution strategies
- Common pitfalls guide
