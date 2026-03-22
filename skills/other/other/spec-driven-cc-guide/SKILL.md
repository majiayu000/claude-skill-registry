---
name: spec-driven-cc-guide
description: >
  Expert knowledge base for Claude Code Terminal — the CLI tool itself, not coding tasks.
  Implements 4 knowledge-retrieval phases with structural anti-skip enforcement using the
  Execute-Verify-Gate pattern at every step. Designed to prevent token optimization bias
  that causes reference file skipping by making every reference load mandatory and verifiable.
  MUST use this skill whenever the user asks about Claude Code features, configuration,
  setup, or troubleshooting. This includes: keyboard shortcuts not working (Option key,
  Alt+P, Shift+Enter, Ctrl+B), creating or configuring subagents/skills/commands/plugins,
  setting up hooks (PreToolUse, PostToolUse, HTTP hooks), installing or debugging MCP
  servers, GitHub Actions or GitLab CI/CD integration for PR reviews, switching models
  mid-conversation, undoing or rewinding Claude's changes, proxy/network configuration,
  permission modes, memory and CLAUDE.md setup, the /batch /simplify /debug bundled skills,
  git worktrees, agent teams, remote control, headless mode, or ANY question where the user
  is asking about how Claude Code works rather than asking Claude Code to do coding work.
  When in doubt about whether a question is about Claude Code itself vs. a coding task,
  prefer triggering this skill — it will not interfere with coding-focused responses.
allowed-tools:
  - Read
  - Grep
  - Glob
  - WebFetch
  - WebSearch
model: sonnet
effort: Medium
---

# Spec-Driven CC Guide

Authoritative Claude Code Terminal knowledge base with 4-phase Execute-Verify-Gate enforcement for knowledge retrieval. Prevents token optimization bias that causes reference file skipping.

---

## Execution Model

This skill expands inline. After invocation, execute Phase 00 Initialization immediately. Do not wait passively, ask permission, or offer execution options.

**Self-Check (if ANY box is true = VIOLATION):**

- [ ] Stopping to ask about token budget
- [ ] Stopping to offer execution options
- [ ] Waiting passively for results
- [ ] Asking "should I execute this?"
- [ ] Skipping a phase because it "seems simple"
- [ ] Combining multiple phases into one
- [ ] Summarizing instead of loading a reference file
- [ ] Answering from memory instead of loading the reference file first

**IF any box checked:** EXECUTION MODEL VIOLATION. Go directly to Phase 00 Initialization now.

---

## Anti-Skip Enforcement Contract

This skill enforces 3 independent anti-skip layers. ALL THREE must fail for a step to be skipped:

1. **Per-phase mandatory reference loading** — Every phase specifies which reference files to Read(). Skipping a Read() is a violation. The answer MUST come from loaded reference content, not from general knowledge or SKILL.md summaries.
2. **Artifact verification** — Each Read() is verified to return non-empty content before proceeding.
3. **Step registry** — `devforgeai-validate phase-record` tracks completion (graceful degradation if CLI unavailable).

**Execute-Verify-Gate Pattern:** Every mandatory step has three parts:
- **EXECUTE:** The exact action to perform
- **VERIFY:** How to confirm the action happened
- **RECORD:** CLI command to record completion (`devforgeai-validate phase-record`)

**Token Optimization Bias is PROHIBITED.** Do not skip, compress, or shortcut any step. The entire purpose of this skill's migration from `claude-code-terminal-expert` was to prevent reference file skipping. If you answer without loading the reference file first, you have defeated the skill's purpose.

---

## When to Use This Skill

**Feature Discovery:** "Can Claude Code do...?", "How do I use [feature]?", "What features are available?"

**Component Creation:** Creating subagents, skills, slash commands, plugins, hooks

**Configuration:** Settings, models, permissions, MCP servers, CI/CD, network/proxy

**Troubleshooting:** Installation issues, errors, performance problems

**Integration:** GitHub Actions, GitLab CI/CD, headless mode, DevContainers, hooks

**Prompt Engineering:** Writing effective prompts, system prompts, using XML tags, chain-of-thought

**Skills Specification:** Agent Skills spec, SKILL.md format, frontmatter fields, skill packaging

---

## Core Features Overview

### 1. Subagents

Specialized AI workers with isolated context windows for domain-specific tasks.

- Custom system prompts and tool restrictions
- Project-level (`.claude/agents/`) or user-level (`~/.claude/agents/`)
- Built-in types: **Explore** (read-only, Haiku), **Plan** (research), **general-purpose** (full tools)
- **`isolation: worktree`** — run in isolated git worktree with auto-cleanup
- **`background: true`** — always run as background task
- **`memory: user|project|local`** — persistent cross-session learning
- **`skills`** field — preload skill content into subagent context
- **`permissionMode`** — `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, `plan`
- **`hooks`** — lifecycle hooks scoped to subagent execution
- **`maxTurns`** — limit agentic turns
- Cannot spawn other subagents (no nesting)

**Quick start:** `/agents` command or create `.claude/agents/my-agent.md`

**Details:** `references/core-features.md` (Section 1)

---

### 2. Skills

Modular capabilities Claude automatically uses based on context, following the [Agent Skills](https://agentskills.io) open standard.

- YAML frontmatter + Markdown instructions in `SKILL.md`
- Progressive disclosure: metadata (always) -> instructions (on trigger) -> resources (on demand)
- **`context: fork`** — run in isolated subagent context
- **`agent`** field — specify which subagent type executes the skill
- **`disable-model-invocation: true`** — user-only invocation (prevents auto-trigger)
- **`user-invocable: false`** — model-only invocation (hidden from `/` menu)
- **`${CLAUDE_SKILL_DIR}`** — reference files relative to skill directory
- **`allowed-tools`** — restrict tool access during skill execution
- **`hooks`** — lifecycle hooks scoped to skill
- **`!`command`** syntax** — inject dynamic shell output into skill content
- Arguments via `$ARGUMENTS`, `$ARGUMENTS[N]`, or `$N` shorthand

**Quick start:** Create `.claude/skills/my-skill/SKILL.md` with frontmatter

**Details:** `references/core-features.md` (Section 2)

---

### 3. Slash Commands & Bundled Skills

User-invoked workflows via `/command` syntax. Commands and skills are now unified — `.claude/commands/` files still work but skills are recommended.

**Built-in commands (50+):** `/help`, `/clear`, `/compact`, `/config`, `/model`, `/agents`, `/mcp`, `/hooks`, `/plugin`, `/memory`, `/rewind`, `/rename`, `/resume`, `/stats`, `/cost`, `/usage`, `/copy`, `/diff`, `/doctor`, `/export`, `/fork`, `/fast`, `/context`, `/desktop`, `/review`, `/security-review`, `/pr-comments`, `/insights`, `/keybindings`, `/vim`, `/theme`, `/permissions`, `/plan`, `/skills`, `/tasks`, `/terminal-setup`, `/remote-control`, `/statusline`, `/sandbox`, and more.

**Bundled skills:**
- **`/simplify`** — reviews changed files for reuse/quality/efficiency, spawns 3 parallel review agents
- **`/batch <instruction>`** — orchestrates large-scale parallel changes across codebase using git worktrees
- **`/debug [description]`** — troubleshoots session issues by reading debug logs
- **`/claude-api`** — loads Claude API reference for your project's language

**Details:** `references/core-features.md` (Section 3)

---

### 4. Plugins

Bundled extensions containing commands, agents, skills, hooks, and MCP servers.

- Marketplace-based distribution
- Team-wide installation via `settings.json`
- **`git-subdir`** source type for subdirectories within git repos
- Custom npm registries and version pinning
- **`/reload-plugins`** — activate changes without restart
- Plugins can ship default `settings.json`

**Details:** `references/core-features.md` (Section 4)

---

### 5. MCP Servers

Model Context Protocol servers connecting Claude to external services (GitHub, Jira, Figma, Stripe, etc.).

- HTTP, SSE, or stdio transports
- OAuth authentication with step-up auth and discovery caching
- Project, user, or local scope
- **`oauth.authServerMetadataUrl`** config option
- Binary content handling (PDFs, Office docs, audio)

**Quick start:** `claude mcp add --transport http <name> <url>`

**Details:** `references/core-features.md` (Section 5)

---

### 6. Hooks

Shell commands, HTTP endpoints, or LLM prompts executed at lifecycle events.

**Event types (11):** `PreToolUse`, `PostToolUse`, `Stop`, `SessionStart`, `SessionEnd`, `SubagentStart`, `SubagentStop`, `WorktreeCreate`, `WorktreeRemove`, `Notification`, `lastAssistantMessage`

- **HTTP hooks** — POST JSON to URLs instead of running shell commands
- **Prompt hooks** — LLM-evaluated hooks for complex decisions
- **MCP tool hooks** — hooks on MCP tool calls
- Command-based hooks with matcher patterns
- Exit code 2 blocks operations
- Hooks in skills and agents via frontmatter

**Quick start:** `/hooks` command

**Details:** `references/integration-patterns.md` (Section 3)

---

### 7. Configuration & Memory

Multi-level settings hierarchy: enterprise -> CLI -> local -> project -> user.

- **Auto-memory** — Claude automatically saves useful context (manage with `/memory`)
- 5-level memory hierarchy (Enterprise -> Project -> Rules -> User -> Local)
- `.claude/rules/` for modular, conditional rules with `paths:` frontmatter
- Import syntax `@path/to/file` (max 5 hops)
- Managed settings via macOS plist or Windows Registry
- `settings.json` at multiple scopes

**Details:** `references/configuration-guide.md`

---

### 8. CI/CD Integration

Automated Claude Code in GitHub Actions and GitLab CI/CD.

- **GitHub Actions:** `@claude` mentions in PRs/issues, `/install-github-app`
- **GitLab CI/CD:** Automated MR creation and reviews
- AWS Bedrock and Google Vertex support
- Headless mode (`claude -p`) for automation

**Details:** `references/integration-patterns.md`

---

### 9. Background Tasks & Worktrees

- `Ctrl+B` — move running command to background (Tmux: press twice)
- `Ctrl+F` — kill all background agents (two-press confirm)
- `!` prefix — bash mode (run commands without Claude interpretation)
- **`--worktree` (`-w`)** flag — isolated git worktree sessions
- `TaskOutput` tool to retrieve background results
- Auto-cleanup on session exit

---

### 10. Checkpoints & Rewind

- Auto-saves code state before each edit
- `Esc Esc` — rewind/summarize menu
- `/rewind` — restore code and/or conversation
- 30-day retention, persists across sessions
- Does NOT track bash/external changes

---

### 11. Sessions & History

- `/rename` — name sessions; `/resume` — resume by name/ID
- `/stats` — usage stats, streaks, model preferences
- `/fork` — fork conversation at current point
- `Ctrl+R` — reverse search command history
- History stored per working directory
- History-based autocomplete for `!` bash commands

---

### 12. Model Selection

- `Alt+P` / `Option+P` — quick model switch mid-prompt
- Aliases: `opus`, `sonnet`, `haiku`, `default`
- `/fast` — toggle fast mode
- Extended context: `[1m]` suffix for 1M token window
- Effort level display and adjustment via `/model`
- `Alt+T` / `Option+T` — toggle extended thinking

---

### 13. Agent Teams

For sustained parallelism across separate sessions (beyond subagents).

- Multiple agents working in parallel with independent contexts
- Communication across separate sessions
- Use when work exceeds single context window

**Details:** See `references/core-features.md` (Section 6)

---

### 14. Remote Control

- `claude remote-control` / `/remote-control` (`/rc`)
- Control terminal session from claude.ai
- Optional `--name` argument for custom session titles
- `/remote-env` — configure default remote environment

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+C` | Cancel input/generation |
| `Ctrl+B` | Background running task (Tmux: press twice) |
| `Ctrl+F` | Kill all background agents (press twice) |
| `Ctrl+T` | Toggle task list |
| `Ctrl+G` | Open prompt in text editor |
| `Ctrl+R` | Reverse search history |
| `Ctrl+O` | Toggle verbose output |
| `Ctrl+L` | Clear terminal screen |
| `Ctrl+V` | Paste image from clipboard |
| `Esc Esc` | Rewind/summarize menu |
| `Alt+P` / `Option+P` | Switch model |
| `Alt+T` / `Option+T` | Toggle extended thinking |
| `Shift+Tab` / `Alt+M` | Cycle permission modes |
| `Tab` | Accept prompt suggestion |
| `@` | File path autocomplete |
| `!` | Bash mode prefix |
| `/` | Command/skill prefix |
| `\` + `Enter` | Multiline input |
| `?` | Show available shortcuts |

---

## Phase 00: Initialization [INLINE]

Extract the user's question from conversation context and prepare for phase execution.

```
$QUESTION = Extract the user's question or request about Claude Code from conversation context
$SESSION_ID = "CCG-" + date_string + "-" + sequence_number (e.g., CCG-2026-03-19-001)
```

Proceed immediately to Phase 01.

---

## Phase Orchestration Loop

```
FOR phase_num in [01, 02, 03, 04]:
    phase_id = phase_num

    1. ENTRY GATE: devforgeai-validate phase-check ${SESSION_ID} --workflow=cc-guide --from={prev} --to={phase_id} --project-root=.
       IF exit 0: proceed | IF exit 1: HALT | IF exit 127: continue without enforcement

    2. LOAD: Read(file_path=".claude/skills/spec-driven-cc-guide/phases/{phase_files[phase_id]}")
       Load FRESH - do NOT rely on memory of previous reads

    3. EXECUTE: Follow every step in the phase file (EXECUTE-VERIFY-RECORD triplets)

    4. RECORD: devforgeai-validate phase-record ${SESSION_ID} --workflow=cc-guide --phase={phase_id} --project-root=.

    5. EXIT GATE: devforgeai-validate phase-complete ${SESSION_ID} --workflow=cc-guide --phase={phase_id} --checkpoint-passed --project-root=.
       IF exit 0: proceed | IF exit 1: HALT | IF exit 127: continue
```

| Phase | Name | File |
|-------|------|------|
| 01 | Question Classification | `phases/phase-01-question-classification.md` |
| 02 | Mandatory Reference Loading | `phases/phase-02-reference-loading.md` |
| 03 | Answer Synthesis | `phases/phase-03-answer-synthesis.md` |
| 04 | Self-Update Check | `phases/phase-04-self-update-check.md` |

---

## Required Subagents Per Phase

| Phase | Required Subagents | Enforcement |
|-------|-------------------|-------------|
| 01 | (none) | N/A |
| 02 | (none) | N/A |
| 03 | (none) | N/A |
| 04 | (none) | N/A |

This skill requires no subagent delegation. All 4 phases are executed inline.

**Deviation Protocol:** Any phase skip requires explicit user consent via AskUserQuestion.

---

## Domain Routing Table (Summary)

See `references/domain-routing-table.md` for full routing rules.

| Domain | Keywords | Reference File(s) |
|--------|----------|-------------------|
| components | subagent, skill, command, plugin, MCP, agent teams | `references/core-features.md` |
| configuration | settings, model, config, permissions, memory, rules | `references/configuration-guide.md` |
| integration | CI/CD, hooks, GitHub Actions, GitLab, headless, automation | `references/integration-patterns.md` |
| troubleshooting | error, not working, can't, fails, broken, help | `references/troubleshooting-guide.md` |
| advanced | sandbox, network, proxy, security, monitoring, enterprise | `references/advanced-features.md` |
| best-practices | workflow, efficiency, prompt tips, optimize, patterns | `references/best-practices.md` |
| reference | shortcut, keyboard, command list, cheat sheet, comparison | `assets/quick-reference.md`, `assets/comparison-matrix.md` |
| prompt-engineering | prompt, chain of thought, XML tags, role, multishot | `references/prompt-engineering/*.md` |
| skills-spec | agent skills spec, SKILL.md format, frontmatter, packaging | `references/skills/*.md` |

**Multi-domain:** If 2+ domains match, load ALL matched references.
**Fallback:** Zero matches -> load `references/core-features.md` as default.

---

## State Persistence

This skill handles single-turn knowledge retrieval. No checkpoint persistence is required — the interaction completes within one turn. Phase state is tracked in-memory during execution.

---

## Workflow Completion Validation

```
expected_phases = 4
IF completed_count < expected_phases: HALT "WORKFLOW INCOMPLETE - {completed_count}/{expected_phases} phases"
IF completed_count == expected_phases: "All 4 phases completed - Knowledge retrieval passed"
```

---

## Success Criteria

Knowledge retrieval complete when:
- [ ] User question classified into >= 1 domain
- [ ] Reference file(s) loaded via Read() (not from memory or SKILL.md summary)
- [ ] Answer cites specific content from loaded reference files
- [ ] Self-update check performed (staleness evaluated)

---

## Reference Files Index

**Local references** (loaded per-phase on demand, NOT consolidated):

| Phase | Reference Files (load via Read from .claude/skills/spec-driven-cc-guide/) |
|-------|-------------------------------------------------------------------------|
| 01 | `references/domain-routing-table.md` |
| 02 | Files from $REFERENCE_FILES[] (determined in Phase 01) |
| 03 | (uses content loaded in Phase 02) |
| 04 | `references/documentation-urls.md` |

**Core reference files:**
- `references/core-features.md` — Subagents, Skills, Commands, Plugins, MCP, Agent Teams
- `references/configuration-guide.md` — Settings, Models, CLI, Permissions, Memory
- `references/integration-patterns.md` — CI/CD, Hooks, Automation, Headless
- `references/troubleshooting-guide.md` — Errors, Installation, Performance
- `references/advanced-features.md` — Sandboxing, Networking, Security
- `references/best-practices.md` — Workflows, Efficiency, Prompting
- `references/documentation-urls.md` — Official documentation URLs for self-updating

**Subdirectory references:**
- `references/prompt-engineering/*.md` — Prompt engineering guides (14 files)
- `references/skills/*.md` — Agent Skills specification docs (6 files)

**Assets:**
- `assets/quick-reference.md` — Full keyboard/command cheat sheet
- `assets/comparison-matrix.md` — Feature comparison table

---

## Self-Updating Mechanism

When documentation may be outdated (user reports missing feature, new release):

1. Load `references/documentation-urls.md` for canonical URLs
2. Fetch latest from official docs via WebFetch
3. Compare with current reference file
4. Update reference file with new content
5. Notify user of what was updated

---

## Version History

- v5.0 (2026-03-19): Migrated from claude-code-terminal-expert v4.0.0 to spec-driven-cc-guide. Added 4-phase Execute-Verify-Gate enforcement to prevent token optimization bias. All reference content preserved as-is.
- v4.0 (2026-03-05): Major update to v2.1.69 — added auto-memory, bundled skills, agent teams, remote control, fast mode, worktree isolation, persistent agent memory, HTTP/prompt hooks, skill `context:fork`, `${CLAUDE_SKILL_DIR}`, 20+ new commands
- v3.1 (2026-01-29): v2.1.23 update — task management, keybindings, autocomplete
- v3.0 (2026-01-18): Agent Skills Specification compliance
- v2.0 (2025-12-20): December 2025 features — background tasks, checkpoints, sessions
- v1.0 (2025-11-06): Initial creation as claude-code-terminal-expert
