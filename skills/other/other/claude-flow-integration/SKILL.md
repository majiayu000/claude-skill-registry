---
name: claude-flow-integration
description: "Hybrid Claude-Flow V3 integration architecture: hook execution order, system roles, background workers, production features (DDD/ADR/security), and integration rules. Use when working with Claude-Flow hooks, workers, or production features."
---

# Claude-Flow Integration

This project uses a **hybrid architecture** combining Claude Code's native agent teams with Claude-Flow V3 features. Both systems MUST work together — neither is optional.

## Architecture Philosophy

- **Priority:** Stability and integrity over speed optimization
- **Context:** Production-quality work, not just internal tooling
- **Enforcement:** 100% accuracy required for all workflow rules

## System Roles

### Our Custom System (Blocking Enforcement)

- **Agent Teams:** TeamCreate + native experimental teams (visible tmux panes, mandatory)
- **Hooks:** `.claude/hooks/*.sh` scripts enforce workflow rules (blocking, fail-fast)
- **Memory:** `claude-mem` stores human decisions, architectural choices, preferences
- **Agent Specs:** `.claude/agents/*.md` define agent capabilities (authoritative for model routing)
- **Linear Integration:** Single source of truth for requirements, status, tickets

### Claude-Flow V3 (Learning & Advisory)

- **Hooks:** Claude-Flow hooks run AFTER our enforcement hooks (non-blocking, continueOnError: true)
- **Background Workers:** 10 daemon workers (map, audit, optimize, consolidate, testgaps, ultralearn, deepdive, document, refactor, benchmark)
- **Memory:** Claude-Flow HNSW memory stores agent patterns, coding learnings, optimization history
- **Model Routing:** Claude-Flow routing provides suggestions; agent specs are the final authority
- **Task Management:** Claude-Flow task orchestration supplements native TaskCreate/TaskUpdate
- **Production Features:** DDD domain tracking, ADR generation, security scanning (CVE, threat modeling)

### Serena MCP (Semantic Code Intelligence)

- **Symbol Navigation:** `find_symbol`, `get_symbols_overview` for token-efficient code reading (50-75% savings vs reading full files)
- **Impact Analysis:** `find_referencing_symbols` to find all callers/users of any symbol
- **Precise Edits:** `replace_symbol_body`, `insert_before/after_symbol` for symbol-level code modifications
- **Rename Refactoring:** `rename_symbol` with automatic reference updates across codebase
- **Pattern Search:** `search_for_pattern` for regex search across project files
- **Project Memory:** `read_memory`, `write_memory` for project-specific code structure and conventions

## Hook Execution Order (CRITICAL)

Hooks run in this exact order to ensure enforcement before learning:

**Write/Edit/MultiEdit:**
1. `.claude/hooks/protect-hooks.sh` (ask — prompts user before hook modifications)
2. `.claude/hooks/enforce-orchestrator-delegation-v2.sh` (blocking — ensures orchestrator delegates to agents; auto-allows subagents)
3. `.claude/hooks/enforce-plan-files.sh` (blocking — protects plan/ directory)
4. `.claude/hooks/check-unwrap.sh` (advisory — warns about `.unwrap()` in library code)
5. `.claude/hooks/scan-secrets.sh` (advisory — detects potential secrets/credentials in code)
6. Claude-Flow `pre-edit` hook (non-blocking — learns patterns, advisory only)

**Bash commands:**
1. `.claude/hooks/protect-hooks.sh` (ask — prompts user before hook modifications)
2. `.claude/hooks/enforce-orchestrator-delegation-v2.sh` (blocking — catches sed/awk/perl bypasses; auto-allows subagents)
3. `.claude/hooks/protect-main.sh` (blocking — prevents direct main commits)
4. `.claude/hooks/enforce-branch-naming.sh` (blocking — validates branch format)
5. `.claude/hooks/enforce-review-gate.sh` (blocking — requires git-review completion)
6. Claude-Flow `pre-command` hook (non-blocking — learns patterns, advisory only)

**Task (agent spawning):**
1. `.claude/hooks/enforce-visible-agents.sh` (blocking — requires team_name for agent visibility)
2. Claude-Flow task hook (non-blocking — advisory only)

**Read/Grep/Bash (source files):**
1. `.claude/hooks/enforce-serena-usage.sh` (advisory — suggests Serena for code navigation)

**Stop (session end):**
1. `.claude/hooks/enforce-memory.sh` (advisory — reminds to save to claude-mem)
2. `.claude/hooks/check-claude-flow-memory.sh` (advisory — reminds to save patterns)

**TaskCompleted (task marked done):**
1. `.claude/hooks/enforce-task-quality.sh` (blocking — runs `cargo test` + `cargo clippy` before task completion; skips non-code tasks)

**TeammateIdle (agent going idle):**
1. `.claude/hooks/enforce-idle-quality.sh` (blocking — runs `cargo test` + `cargo clippy` before idle; skips if no source changes)

**UserPromptSubmit (every prompt):**
1. `.claude/hooks/enforce-ticket.sh` (blocking — requires branch with ticket ID)
2. Claude-Flow routing hook (non-blocking)
3. `.claude/hooks/workflow-reminder.sh` (advisory)

## Memory Separation

- **claude-mem:** User preferences, architectural decisions, debugging insights, cross-session learnings (human-driven)
- **Claude-Flow memory:** Agent coordination patterns, code optimization history, model performance data (agent-driven)
- **Serena memory:** Project code structure, conventions, build commands (code-driven, auto-discovered via onboarding)
- **Linear:** Ticket requirements, acceptance criteria, status tracking (project management)
- **No overlap:** Each memory system serves a distinct purpose; never duplicate content

## Tool Routing (Serena vs Native Tools)

- **Reading code structure**: Use Serena `get_symbols_overview` → only read bodies you need (saves 50-75% tokens)
- **Finding definitions**: Use Serena `find_symbol` instead of Grep for symbol definitions
- **Finding callers**: Use Serena `find_referencing_symbols` instead of Grep for who-calls-what
- **Replacing functions**: Use Serena `replace_symbol_body` for entire function replacement (vs Edit for line-level)
- **Non-code files**: Use Read/Edit/Grep (Serena only works with LSP-supported languages)
- **Config/markdown/TOML**: Use Read/Edit (Serena has limited support for non-code)

## Model Routing

- **Agent specs** (`.claude/agents/*.md`) define the authoritative model for each agent type
- **Claude-Flow routing** provides suggestions based on task complexity and past performance
- **In case of conflict:** Agent spec always wins (manual configuration > automated suggestion)
- **Model tiers:** Opus (3: planner, red-teamer, senior-coder), Sonnet (7: requirements-interviewer, explorer, architect, coder, tech-lead, reviewer, qa), Haiku (4: junior-coder, documentation, explainer, optimizer)
- **Example:** `coder` uses Sonnet (per spec), even if Claude-Flow suggests Opus for a task

## Background Workers (Always Enabled)

All 10 Claude-Flow daemon workers run continuously:
- **map**: Codebase structure analysis
- **audit**: Code quality and security auditing
- **optimize**: Performance optimization suggestions
- **consolidate**: Memory and pattern consolidation
- **testgaps**: Test coverage gap detection
- **ultralearn**: Advanced pattern learning from agent interactions
- **deepdive**: Deep analysis of complex code changes
- **document**: Automatic documentation generation (ADR, DDD docs)
- **refactor**: Refactoring opportunity detection
- **benchmark**: Performance benchmarking and regression detection

## Production Features (Always Enabled)

- **DDD (Domain-Driven Design):** Track bounded contexts, validate domain boundaries, maintain `/docs/ddd`
- **ADR (Architecture Decision Records):** Auto-generate decision records, maintain `/docs/adr`, use MADR template
- **Security Scanning:** Auto-scan on edit, CVE vulnerability checking, threat modeling, security pattern detection

## Integration Rules

1. **Both systems required:** Claude-Flow features supplement native teams; never replace them
2. **Hook order matters:** Our blocking hooks run first; Claude-Flow hooks learn second
3. **Memory separation:** Never duplicate data across claude-mem, Claude-Flow memory, and Linear
4. **Model authority:** Agent specs define models; Claude-Flow routing is advisory only
5. **Stability first:** All Claude-Flow hooks have `continueOnError: true` to prevent workflow blockage
6. **100% enforcement:** Our custom hooks must maintain perfect accuracy; no false positives

## Why This Architecture?

- **Complementary systems:** Native teams handle coordination; Claude-Flow handles learning
- **Fail-safe design:** Blocking enforcement prevents mistakes; non-blocking learning improves over time
- **Production-ready:** DDD, ADR, security features support large-scale professional work
- **Clear boundaries:** Each system owns specific responsibilities with no overlap
- **Observable behavior:** tmux panes show agent activity; background workers run invisibly
- **Token efficiency:** Serena's LSP-powered navigation reads only what's needed (50-75% savings over full-file reads)
