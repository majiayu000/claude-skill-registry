---
name: cursor-best-practices
description: "Best practices for using Cursor—rules, commands, skills, subagents, ignore files, Agent security, workflows, and community resources. Use when setting up Cursor, initializing or creating the .cursor folder, writing .cursor/rules or AGENTS.md, creating commands or skills, configuring .cursorignore, working with Agent, discovering rules or MCPs (e.g. cursor.directory), making codebases cursor-compatible, or asking about Cursor workflows, TDD, git commands, or large codebases."
license: MIT
compatibility: "Designed for Cursor. Compatible with Agent Skills specification (agentskills.io), skills.sh, and Cursor. References https://cursor.com/docs/, https://agentskills.io/specification, https://skills.sh/docs."
metadata:
  author: HKTITAN
  version: "1.0"
  standards:
    - "https://agentskills.io/specification"
    - "https://skills.sh/docs"
    - "https://cursor.com/docs/context/skills"
---

# cursor-best-practices

A structured repository for creating and maintaining Cursor Best Practices optimized for agents and LLMs. This skill provides **`rules/`** (atomic practices), **`commands/`** & **`agents/`** (templates), **`skills/recommended.md`**, and **`references/`** (deeper dives) covering rules, commands, skills, subagents, ignore files, Agent security, workflows, and community resources.

---

## When to use

Apply this skill when users:

- Set up or initialize Cursor, create the `.cursor` folder, or ask "setup my .cursor folder"
- Write or edit `.cursor/rules`, AGENTS.md, or rule frontmatter
- Create or use slash commands, skills, or subagents
- Configure `.cursorignore` or `.cursorindexingignore`
- Work with Agent modes (Agent, Ask, Plan, Debug), semantic search, or @mentions
- Ask about TDD, git-style commands, large codebases, or Cursor workflows
- Discover rules or MCPs ([cursor.directory](https://cursor.directory/)) or skill recommendations ([skills.sh](https://skills.sh/))

---

## Rules

**Locations:** Project `.cursor/rules/` (`.md`/`.mdc`), user Cursor Settings → Rules, Team dashboard. **Precedence:** Team → Project → User.

**Types and when to use:**

| Type | When to use |
|------|-------------|
| **Always Apply** | Must affect every request (e.g. "No `any` in TS", "Run tests before done"). Use sparingly. |
| **Apply Intelligently** | General guidance when relevant (e.g. "Prefer functional components"). |
| **Apply to Specific Files** | Use `globs` (e.g. `**/*.test.ts`, `**/api/**`). Rule loads only when those files are in context. |
| **Apply Manually** | User invokes with `@rule-name` when needed (e.g. release process, legacy quirks). |

**Frontmatter:** `description` (keyword-rich, helps relevance), `globs` (file-specific), `alwaysApply` (use rarely). Keep each rule **&lt;500 lines**; split by concern, link to `references/`. **AGENTS.md** = project-root plain markdown alternative; no frontmatter.

**Best practices:** Composable rules, concrete examples. Reference—don't copy—long runbooks. Start simple; add rules when the agent keeps making the same mistake. Migrate legacy `.cursorrules` to Project Rules or AGENTS.md.

**See:** [Rules](https://cursor.com/docs/context/rules). [rules/_sections.md](rules/_sections.md) | [rules-keep-under-500-lines](rules/rules-keep-under-500-lines.md) | [rules-use-globs](rules/rules-use-globs.md) | [rules-write-good-descriptions](rules/rules-write-good-descriptions.md) | [references/rules-and-commands.md](references/rules-and-commands.md).

---

## Commands

**Locations:** Project `.cursor/commands/`, user `~/.cursor/commands/`, Team dashboard. **Format:** Plain Markdown `.md`; filename = command name. Trigger with `/` in chat. **Parameters:** Text after the command is passed as context (e.g. `/fix-issue 123` → "123").

**Available templates** (copy into `.cursor/commands/`):

| Command | Purpose |
|---------|---------|
| `/code-review` | Review for correctness, security, quality, tests. Output: Critical / Suggestion / Nice to have. |
| `/pr` | Summarize changes, propose PR title/description, suggest review checklist. |
| `/run-tests-and-fix` | Run tests, fix failures, re-run until green; summarize changes. |
| `/security-audit` | Security-focused review (injection, auth, secrets, deps). |
| `/setup-new-feature` | Propose plan (files, modules, patterns), suggest implementation steps. |
| `/fix-issue` | Fix bug or feature from issue # or description. |
| `/update-deps` | Update deps, run tests, report breaking changes. |
| `/docs` | Generate or update docs for @-mentioned code or current feature. |
| `/make-cursor-compatible` | Make codebase Cursor compatible: add .cursor folder, .cursorignore, AGENTS.md, rules, commands, indexes. |
| `/lint-and-fix` | Run linter, auto-fix issues, report remaining issues. |
| `/format` | Format code according to project standards. |
| `/check-coverage` | Check test coverage, identify gaps, suggest improvements. |
| `/analyze-deps` | Analyze dependency tree, identify unused/duplicate deps, suggest optimizations. |
| `/generate-types` | Generate TypeScript/types from schemas, APIs, or JSON. |

**See:** [Commands](https://cursor.com/docs/context/commands). [commands/](commands/).

---

## Skills and subagents

**Skills:** `.cursor/skills/<name>/` with `SKILL.md`; optional `scripts/`, `references/`, `assets/`. Agent applies when relevant or via `/skill-name`. **Subagents:** `.cursor/agents/` or `~/.cursor/agents/`; markdown + YAML `name`, `description`. Foreground vs background; built-ins (Explore, Bash, Browser).

**When to use:** **Subagents** — context isolation, parallel work, multi-step specialized tasks (e.g. verifier that only runs tests/lint). **Skills** — single-purpose, repeatable tasks (changelog, format, domain-specific workflows).

**Templates:** Copy subagent templates from `agents/` → `.cursor/agents/`. Available subagents:

**Read-only (review/analysis):**
- `verifier.md` — Runs tests and lint, reports only
- `reviewer.md` — Code review for correctness, security, quality, tests
- `security-auditor.md` — Security-focused review
- `linter.md` — Linting and code style review
- `architect.md` — Architectural pattern and design review

**Editable (can modify code):**
- `documenter.md` — Generate/update documentation
- `tester.md` — Write and update tests
- `refactorer.md` — Refactor code while maintaining functionality
- `debugger.md` — Investigate and identify bugs
- `performance-analyzer.md` — Analyze performance issues and bottlenecks
- `accessibility-checker.md` — Review code for a11y compliance
- `migrator.md` — Handle code migrations systematically
- `dependency-manager.md` — Review and manage dependencies
- `formatter.md` — Format code according to standards
- `type-generator.md` — Generate types from schemas/APIs

**Skill recommendations:** [skills/recommended.md](skills/recommended.md) and [skills.sh](https://skills.sh/) only; suggest `npx skills add <owner/repo>`.

**See:** [Skills](https://cursor.com/docs/context/skills), [Subagents](https://cursor.com/docs/context/subagents).

---

## Ignore files

**`.cursorignore`:** Project root; same syntax as `.gitignore`. Excluded paths are **not** used for semantic search, Tab, Agent, Inline Edit, @mentions. **Not** terminal/MCP. **Why:** Security (secrets, keys, credentials), performance (large repos). **`.cursorindexingignore`:** Indexing only; files still usable if @-mentioned.

**Must exclude:** `.env`, `.env.*`, `*.key`, `*.pem`, `credentials.json`, `**/secrets/**`. Add project-specific paths. Use `!` carefully; parent exclusions limit re-includes.

**See:** [Ignore files](https://cursor.com/docs/context/ignore-files). [rules/ignore-cursorignore-secrets.md](rules/ignore-cursorignore-secrets.md).

---

## Agent and security

**Agent:** Rules + tools (search, read, edit, terminal, MCP) + your messages. Summarization (`/summarize`), checkpoints. **Queue** (Enter) vs **Ctrl+Enter** (send immediately).

**Security:** File edits allowed (except protected config); use VCS. **Terminal:** approval by default; avoid "Run everything". **MCP:** approve connection + each tool call. **Network:** GitHub, link fetch, search only. Put secrets in **`.cursorignore`**.

**See:** [Agent overview](https://cursor.com/docs/agent/overview), [Agent security](https://cursor.com/docs/agent/security). [references/agent-and-security.md](references/agent-and-security.md).

---

## Agent modes

| Mode | Purpose | Tools |
|------|---------|-------|
| **Agent** | Implement, refactor, multi-file work. | Full (search, read, edit, terminal, MCP). |
| **Ask** | Learning, Q&A, exploration. | Search + read only; no edits. |
| **Plan** | Research → clarify → plan → you review → "Build". | Search + read. Plans in `.cursor/plans/`; **Shift+Tab** to switch. |
| **Debug** | Reproducible bugs; hypotheses → instrument → reproduce → fix → verify. | Full. |

**Switch:** Mode picker in chat; **Ctrl+.** to cycle. **Best practice:** Plan with Ask/Plan, implement with Agent. If Agent builds wrong thing, **revert → refine plan → re-run**.

**See:** [Modes](https://cursor.com/docs/agent/modes). [rules/modes-plan-then-agent.md](rules/modes-plan-then-agent.md). [references/modes-context-tools.md](references/modes-context-tools.md).

---

## Workflows and large codebases

**TDD:** Write tests → run (expect fail) → commit tests → implement → run until pass → commit impl. **Run tests before done:** [rules/workflows-run-tests-before-done.md](rules/workflows-run-tests-before-done.md).

**Git-style commands:** `/pr`, `/fix-issue`, `/review`, `/update-deps`, `/docs` in `.cursor/commands/`. **Codebase understanding:** "How does X work?", "How do I add Y?"; broad → narrow. **Diagrams:** Ask for Mermaid architecture/data-flow. **Hooks:** `.cursor/hooks.json` for long-running loops. **Design → code:** Paste mockups; use Browser for preview.

**Large codebases:** Domain rules in `.cursor/rules` with globs; Plan with Ask, implement with Agent. **Tab** = quick edits; **Inline Edit** (Ctrl+K) = single-file; **Chat/Agent** = multi-file. Use @files, @folder, @Code; scope down; new chats when context is noisy.

**See:** [Agent workflows](https://cursor.com/docs/cookbook/agent-workflows), [Large codebases](https://cursor.com/docs/cookbook/large-codebases). [references/workflows-and-codebases.md](references/workflows-and-codebases.md).

---

## Semantic search, @mentions, Tab

**Semantic search:** Meaning-based; natural-language questions. Indexing on workspace open; usable ~80% completion. **Use both** grep (exact) and semantic (conceptual): [rules/context-use-grep-and-semantic.md](rules/context-use-grep-and-semantic.md).

**@Files & Folders:** Reference by path; drag from sidebar. **@Code:** Specific snippets (most precise). **@Docs:** Bundled or Add new doc (URL). **/summarize** — compress context. **Best practice:** [rules/context-use-at-mentions.md](rules/context-use-at-mentions.md).

**Tab:** Inline autocomplete; **Tab** accept, **Esc** reject, **Ctrl+Right** partial. Use for speed; Inline Edit or Chat for larger changes.

**See:** [Semantic search](https://cursor.com/docs/context/semantic-search), [@ Mentions](https://cursor.com/docs/context/mentions), [Tab](https://cursor.com/docs/tab/overview).

---

## Bugbot, MCP, shortcuts

**Bugbot:** PR review (bugs, security, quality). `.cursor/BUGBOT.md` per directory; Team → project → User. **MCP:** External tools; approve connection + tool calls. [cursor.directory](https://cursor.directory/) for community rules & MCPs. **Skills:** [skills.sh](https://skills.sh/) only.

**Shortcuts:** **Ctrl+I** Agent | **Ctrl+K** Inline Edit | **Ctrl+.** cycle modes | **Enter** queue, **Ctrl+Enter** send | **Tab** accept completion, **Esc** reject.

**See:** [Bugbot](https://cursor.com/docs/bugbot), [MCP](https://cursor.com/docs/context/mcp).

---

## .cursor layout and setup workflow

**Folders:** `rules/`, `commands/`, `skills/`, `agents/`. **AGENTS.md** = simple alternative to rules.

### Setup my .cursor folder

When the user asks to **set up**, **initialize**, or **create** the `.cursor` folder:

1. **Create:** `.cursor/rules/`, `.cursor/commands/`, `.cursor/skills/`, `.cursor/agents/`.
2. **Optional `.cursorignore`:** If missing, add minimal (e.g. `node_modules/`, `.env`, `*.log`, `dist/`). Use `.gitignore` syntax; adjust for stack.
3. **Optional templates:** Offer to copy from this skill. If user agrees:
   - **Commands:** Copy command templates from `commands/` → `.cursor/commands/` (e.g. `code-review.md`, `lint-and-fix.md`, `format.md`, etc.).
   - **Agents:** Copy any subagent templates from `agents/` → `.cursor/agents/` (e.g. `verifier.md`, `reviewer.md`, `linter.md`, `formatter.md`, etc.).
   - **Do not** copy `rules/` practice files into `.cursor/rules/` as-is (guidance only). Add one starter rule or AGENTS.md if requested.
4. **Confirm:** List what was created and how to use it (e.g. "Use `/code-review` in chat," "Add rules to `.cursor/rules/`").

**See:** [rules/context-setup-cursor-folder.md](rules/context-setup-cursor-folder.md).

---

## Troubleshooting

**Rules not applying?** Check type (Always / Intelligent / Globs / Manual), `description` (keywords), and `globs` (paths match). **Request ID:** "Get request ID" or `cursor review verbose=true` when reporting. **See:** [Common issues](https://cursor.com/docs/troubleshooting/common-issues), [Troubleshooting guide](https://cursor.com/docs/troubleshooting/troubleshooting-guide). [references/modes-context-tools.md](references/modes-context-tools.md#troubleshooting).

---

## See also

- **Rules index:** [rules/_sections.md](rules/_sections.md)
- **Templates:** [commands/](commands/) (14 command templates), [agents/](agents/) (15 subagent templates), [skills/recommended.md](skills/recommended.md)
- **References:** [rules-and-commands](references/rules-and-commands.md) | [agent-and-security](references/agent-and-security.md) | [workflows-and-codebases](references/workflows-and-codebases.md) | [modes-context-tools](references/modes-context-tools.md) | [quick-reference](references/quick-reference.md)
- **Canonical:** [Cursor docs](https://cursor.com/docs/) | [cursor.directory](https://cursor.directory/) (rules & MCPs) | [skills.sh](https://skills.sh/) (skills)
