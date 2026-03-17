---
name: ecosystem-patterns
description: "Use this when creating new projects, generating documentation, cleaning/organizing a repo, suggesting architecture, deploying containers and services, naming files/folders, or when the user references 'ecosystem', 'patterns', or 'containers'. This skill outlines naming conventions, stack preferences, project organization (iMi worktrees), Docker patterns, and PRD structures from past conversations."
---

# Preferred Patterns

## Overview

## Universal Paths

**Environment Variables:**

- $IMI_SYSTEM_PATH = $CODE = `~/code/` - All repositories
- `$VAULT` = `~/code/DeLoDocs` - Obsidian vault
- `$STACKS` = `~/docker/trunk-main/stacks` - Domain-based service stacks
  - $AI` = `$STACKS/ai` - AI/ML services
  - `$MONITORING` = `$STACKS/monitoring` - Monitoring services
  - etc.
- `$ZC` = `~/.config/zshyzsh` - Shell configuration

> [!IMPORTANT] **Critical Pattern:**
> Every repo in `$CODE` (ideally) has a matching folder in `$VAULT/Projects/` for non-tracked brainstorming and iteration documents.
> There is a `helper.zsh` script function `syncDocs` that ensures this relationship is maintained.

> [!IMPORTANT] **Critical Convention**
> `exported` paths are ALWAYS in caps.
> `aliases` and `functions` are ALWAYS lowercase.

- For every exported path, there is an alias to navigate to it quickly.
  - `alias zv='cd $ZV'` to go to the vault.

- This convention is reused and applied to LLM model and Agent invocations of that model.
  - `export KK='openrouter/moonshotai/kimi-k2'`
  - `alias kk='gptme --model $KK'`

## Pattern Categories

### 0. Universal Code Hygiene Rules

> [!CRITICAL] **The No-Script-Disease Rule**
> NEVER create versioned script variants (`-improved`, `-new`, `-v2`, `-old`, `.bak`). This creates runaway technical debt through:
>
> 1. **Ambiguity** - Which version is canonical? Which runs in production?
> 2. **Dead Code** - Old versions linger because "what if we need to roll back?"
> 3. **Discovery Friction** - New developers don't know which script to read/modify
> 4. **Merge Conflicts** - Multiple versions diverge, reconciliation becomes painful
>
> **Correct Pattern:**
> - Replace files in-place
> - Use git history for rollback capability
> - Use feature branches for experimental variants, NEVER file suffixes
> - If you must keep old versions for reference, move to archive directory with date stamp, not inline suffixes
>
> **Examples:**
> ```bash
> # ❌ WRONG - Creates script disease
> scripts/build.sh
> scripts/build-improved.sh
> scripts/build-new.sh
> scripts/build-old.sh
> scripts/build.sh.bak
>
> # ✅ CORRECT - Single canonical version
> scripts/build.sh  # Current version, git history for rollback
>
> # ✅ ACCEPTABLE - If archival needed
> scripts/build.sh
> archive/build-20251106.sh  # Explicit date, separate archive directory
> ```

> [!CRITICAL] **Port Selection Rule (avoid obvious/common ports)**
> When starting local servers (Vite dev/preview, FastAPI, etc) that will be proxied or accessed across your LAN/WAN, **do not grab the obvious/default ports** (especially `3000`). They are collision magnets.
>
> **Correct pattern:**
> - Pick a random port in **8000-19000**
> - If it collides, pick another random port
> - Update Traefik (or whatever proxy) upstream to match
>
> **Quick collision check:**
> ```bash
> ss -ltn | rg ":${PORT} " || echo "free"
> ```

### 1. Local Repo Worktree File Structure (iMi Worktrees)

I made a custom Rust CLI tool called iMi (sticking with my Bon Iver inspired project names) to manage git worktrees for all my projects. Its strict rules allow us to leverage convention over configuration. When working with AI, this is an easy way to reduce complexity and tokens by trading some agency for deterministic behavior. The rules are as follows:

- Every `iMi` project lives in the $IMI_SYSTEM_PATH (`~/code/`) directory.
- The project's top-level directory contains zero or more git worktrees for different branches and purposes.
- The top-level directory MUST contain a copy of the repo's remote `trunk`
- Each feature, PR, review, experiment, or fix gets its own worktree named according to a strict convention.
  - Branches are name by `type/descriptive-name` (e.g., `feat/add-auth`, `fix/login-bug`)
  - Worktrees are named by `type-descriptive-name` (e.g., `pr-42`, `fix-login-bug`)
  - The main trunk worktree is always named `trunk-[branch-name]` (e.g., `trunk-main`, `trunk-master`, `trunk-develop`)
  - Theses conventions can be customized per host machine via `iMi` config file (`~/.config/iMi/config.toml`)
- All worktrees are siblings with the trunk in the top-level project directory.
- The top-level project directory is referred to as the `iMi Sandbox` and contains no code itself. Instead, it contains:
  - An `.iMi/` directory for iMi's internal config and metadata.
  - A `dotfiles` directory that manages user-level and project-level, non-tracked dotfiles via symlinks.
  - `iMi` handles manages these symlinks automatically when creating worktrees.
- Before working with a new repo, it needs to be initialized:
  - If it already exists locally, run `imi init` from within the repo directory.
  - If it does not exist locally, run `imi clone {repo-url}` and it will be cloned and initialized automatically and placed in `$CODE/`
  - After initialization, the repo exists as a project in the `iMi Database` and can be managed via `imi` commands.
- When outside a project directory, list all projects with `imi list` (or `imi ls` for short).
- From within a project directory, list all worktrees with `imi list` (or `imi ls -p` to override and list all projects).
- Each worktree at any one time can be assigned either
  - one developer
    - e.g. If you manually edit files, you are implicitly assigned to that worktree.
  - one agent
    - If the worktree is created as part of a task picked up by an agent, that agent is assigned to the worktree.
  - one developer and one agent
    - If you are working in an interactive shell or REPL, it is considered pair programming and you are assigned to that worktree with the paired agent.
- iMi is loosely coupled to Agents as far as linking through foreign key. `iMi` does not manage agent spawning, lifecycle, business logic.
- iMi is tied to the 33GOD Agent Framework via generous publishing of key events to the Bloodbank Event Bus.
  - e.g., When a worktree is created, an event is published to the bus that agents registered with the Flume task service can listen for and pick up tasks depending on their expertise and stage of the task lifecycle.

**Location:** `$CODE/{project-name}/`

```bash
$CODE/repo-name/
├── .iMi/              # Main repository branch
├── trunk-main/              # Main repository branch
├── feature-{name}/          # Feature branches
├── pr-{number}-{name}/      # PR worktrees
├── pr-review-{number}/      # Review worktrees
├── experiment-{name}/       # Experimental branches
└── fix-{name}/              # Bug fixes
```

**Vault Documentation:** `$VAULT/Projects/{project-name}/`

```bash
$VAULT/Projects/repo-name/
├── markdown/                # Docs sync'd from repo
├──── PRD.md                  # Product requirements
├──── Architecture.md         # Technical architecture
├── Brainstorming.md         # non-tracked Ideas and iterations
├── Meeting-Notes.md         # Discussion notes
└── Research/                # Background research
```

**Critical Pattern:** Every project in `$CODE` has corresponding documentation in `$VAULT/Projects/` for non-tracked brainstorming and iteration.

### 2. Shell Configuration Patterns (zshyzsh)

**Theme**: Dark (Catppuccin Mocha or Gruvbox Material Dark)
**Terminal**: Alacritty
**Editor**: neovim (Lazyvim flavor, aliased to vi)
**IDE**: None. Never. I only work in a zellij multiplexed terminal with floating neovim instances.

**Key Patterns:**

- Modular zsh config in $ZSH_CUSTOM == $ZC == `~/.config/zshyzsh/`
- Zellij terminal multiplexing
- Custom aliases and functions
- Terminal logging system [WIP]
- Settings in ~/.config are moved to home/delorenj/.config/zshyzsh and symlinked back to ~/.config

**Structure:**

```
~/.config/zshyzsh/
├── aliases.zsh            # Custom aliases (ALL aliases go here!)
├── secrets.zsh            # Secrets (ALL api keys go here!)
├── [functions].zsh        # Autoloaded Shell functions
├── zellij/                # Multiplexer configs
├── alacritty/             # Multiplexer configs
```

**Preferred Coding Agents**:

- Claude Flow
- Claude Code
- AmazonQ (aliased as `qq`)
- Crush
- Gemini
- Auggie
- Codex
- Copilot
- Kimi
- GptMe (aliased as `gptme`, `kk` kimi-k2, `ds` deepseek, `dsr` ds reasoner, `zai` GLM4.6)

**CRITICAL PACKAGE & TOOL MANAGEMENT PATTERN:**

- EVERY Python project uses UV for package management.
- EVERY Rust project uses Cargo.
- EVERY JavaScript/TypeScript project uses either Node.js (with npm or Bun)
- EVERY React project uses Vite (Next.js only if explicitly requested).
- EVERY React component library uses ShadCN/UI and Tailwind CSS for styling.
- EVERY PostgreSQL database (even docker services) use my natively installed Postgres server unless explicitly requested otherwise.
- EVERY Redis database (even docker services) use my natively installed Redis server unless explicitly requested otherwise.
- EVERY Vector DB (Pinecone, Weaviate, etc.) uses my natively installed Qdrant server unless explicitly requested otherwise.
- EVERY package and tool version is installed and managed with Mise.
- All task runners, and script encapsulation/orchestration is done with Mise Tasks
- When writing scripts, ALWAYS prefer Python (with UV) or Rust (with Cargo) over Bash unless explicitly requested otherwise.
- When developing CLIs, use typer (Python) or clap (Rust).
- When developing APIs, use FastAPI (Python) or Actix (Rust).
- When developing APIs, start with a CLI.
- When developing MCP tool servers, use FastMCP (Python) (and start with an API, which starts with a CLI).
- Utilize the Command Pattern for all CLIs and APIs for maximum extensibility.
- Follow modular organization pattern

### 4. Tech Stack Preferences

**Backend:**

- FastAPI (Python) for APIs
- PostgreSQL for databases
- FastMCP for Model Context Protocol servers
- Redis for caching and message queues
- UV for Python package management
- Mise for tool version management

**Frontend:**

- React with Vite
- Tailwind CSS for styling
- ShadCN/UI for components
- TypeScript for type safety
- Mise for tool version management

**Runtime:**

- Node.js or Bun for JavaScript
- Python 3.12+ managed with UV

**DevOps:**

- Docker Compose v2 for orchestration
- Mise for tool version management
- n8n for workflow automation

**AI/Agentic:**

- Agno agents (or Pydantic Agents, Smolagents, Atomic Agents, Llamaindex Agents as alternatives)
- FastMCP for tool integration
- Custom agent frameworks (33GOD, AgentForge)
- Multi-agent coordination patterns

**Application:**

- Default to these technologies unless explicitly requested otherwise
- Reference integration patterns between these tools
- Suggest configurations that match existing setups
- Never assume Supabase/Next.js unless explicitly mentioned

### 5.4. Shell Context Independence & LLM Execution Abstraction (jelmore)

**Core Principle:** Scripts used in automation (n8n workflows, cron jobs, systemd services) must not depend on interactive shell configuration.

**Critical Pattern**: Shell aliases and functions don't propagate to subprocess environments. All automation scripts must be self-contained.

#### jelmore CLI: Convention-Based LLM Execution

**jelmore** is the low-level execution primitive for LLM invocations in the 33GOD ecosystem. It wraps various LLM clients (Claude Code, gptme, claude-flow) with a unified CLI that applies shell context independence patterns.

**Location**: `/home/delorenj/code/jelmore`

**Core Features**:
- Convention over configuration (auto-infer client, MCP servers, model tier)
- Detached Zellij sessions with immediate return
- iMi worktree integration
- Config file support for reusable workflows
- n8n Execute Command integration

**When to Use jelmore**:
- ✅ n8n workflow automation (Execute Command nodes)
- ✅ Subprocess environments (cron, systemd, containerized)
- ✅ Convention-based tasks (prompt content determines client/config)
- ✅ Non-blocking execution with deferred observability
- ✅ Manual CLI invocation with simple prompts

**When jelmore Shines**:
- **Shell-context-free**: No reliance on aliases, functions, or interactive shell config
- **Immediate return**: Returns session handle instantly, perfect for workflow continuation
- **Smart defaults**: Infers client/model/MCP servers from prompt keywords
- **Worktree-aware**: Integrates seamlessly with iMi for repository context
- **Event-driven**: Publishes lifecycle events to Bloodbank for coordination

**Usage Patterns**:

```bash
# 1. Explicit mode (all options specified)
jelmore execute --client claude --file task.md --path /repo/root

# 2. Convention mode (auto-infer everything)
jelmore execute -p "Create a react dashboard" --auto

# 3. Config-based mode (reusable workflows)
jelmore execute --config pr-review.json
```

**Convention Engine Intelligence**:

| Prompt Pattern | Inferred Client | MCP Servers |
|---------------|----------------|-------------|
| `react`, `typescript` | `claude` (Claude Code) | - |
| `python`, `api` | `gptme` | - |
| `review`, `refactor` | `claude-flow` (swarm) | - |
| `github`, `pr` | (current) | `github-mcp` |
| `docs`, `documentation` | (current) | `obsidian-mcp` |
| All prompts | (current) | `bloodbank-mcp` |

**n8n Integration Pattern**:

Execute Command node returns immediately with session handle:
```javascript
{
  "command": "uv run jelmore execute -f task.md --worktree pr-{{ $json.pr_number }} --auto --json",
  "timeout": 5000
}
```

Returns JSON for workflow continuation:
```json
{
  "execution_id": "abc123",
  "session_name": "jelmore-pr-458-20251103-143022",
  "client": "claude-flow",
  "log_path": "/tmp/jelmore-abc123.log",
  "started_at": "2025-11-03T14:30:22"
}
```

Attach later to observe:
```bash
zellij attach jelmore-pr-458-20251103-143022
```

**Config File Examples**:

Profiles stored in `~/.config/jelmore/profiles/`:
- `pr-review-auto.json` - Auto-inference PR review workflow
- `feature-planning.json` - Multi-phase feature development
- `refactor-session.json` - Systematic refactoring
- `bug-triage.json` - Deep reasoning for bug investigation
- `api-implementation.json` - End-to-end API development
- `n8n-integration-template.json` - Template for n8n workflows

**Architecture Position**:

```
┌─────────────────────────────────────────────┐
│  n8n Workflows / Manual CLI                 │
│  (triggers, user input)                     │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│  jelmore CLI (Execution Primitive)          │
│  - Convention engine                        │
│  - Detached Zellij sessions                 │
│  - Shell-context independence               │
│  - Immediate return with handle             │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│  LLM Clients (claude, gptme, claude-flow)   │
│  - Actual execution                         │
│  - MCP server integration                   │
│  - iMi worktree context                     │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│  Bloodbank Event Bus                        │
│  - Lifecycle events                         │
│  - Coordination signals                     │
└─────────────────────────────────────────────┘
```

**Related Components**:
- **Flume**: High-level task orchestration layer (future)
- **Bloodbank**: Event bus for cross-service communication
- **iMi**: Git worktree management and context resolution

**Key Implementation**:
- Scripts in `~/.local/bin/` with explicit PATH exports
- No reliance on `.zshrc`, `.bashrc`, or shell aliases
- Detached Zellij sessions for long-running operations with immediate return
- Unique session identifiers for observability and attachment

**Architecture Benefits**:
1. **Portability**: Works in any execution context (interactive, automated, containerized)
2. **Observability**: Full terminal output available via session attachment
3. **Non-blocking**: Automation gets immediate response with connection info
4. **Debuggable**: Can attach to live session to watch real-time progress
5. **Persistent**: Sessions survive caller termination
6. **Convention-driven**: Reduces configuration overhead via smart inference

**Documentation**:
- Full CLI reference: `/home/delorenj/code/jelmore/CLI.md`
- Quick start guide: `/home/delorenj/code/jelmore/CLI-QUICKSTART.md`
- Config examples: `/home/delorenj/code/jelmore/examples/configs/`
- User profiles: `~/.config/jelmore/profiles/`

**See Also**:
- `references/shell-context-independence.md` - Complete pattern documentation
- `/home/delorenj/code/jelmore/` - Source code and implementation
- `bloodbank-n8n-event-driven-workflows` skill - Event-driven integration patterns

### 5.5. Composable Git Operations

**Core Principle:** Git operations in tooling should be atomic, side-effect-free primitives that compose cleanly.

**Anti-Pattern: High-Level Convenience Commands**

```bash
# DON'T: gh pr checkout has hidden side effects
gh pr checkout 123 -b pr-123

# Problem: This command:
# 1. Fetches PR ref ✓
# 2. Checks out branch in CURRENT directory ✗ (side effect)
# 3. Creates local tracking branch ✓
```

**Pattern: Atomic Operations**

```bash
# DO: Separate fetch from checkout
# Step 1: Get PR metadata (no side effects)
PR_REF=$(gh pr view 123 --json headRefName -q .headRefName)

# Step 2: Fetch ref without checkout (no side effects)
git fetch origin $PR_REF:pr-123

# Step 3: Create worktree from fetched ref (explicit side effect)
git worktree add /path/to/pr-123 pr-123
```

**Architectural Benefits:**

1. **Predictability:** Each operation has single, clear responsibility
2. **Composability:** Operations can be reordered or skipped independently
3. **Testability:** Each step can be tested in isolation
4. **Debuggability:** Failures occur at precise operation boundaries
5. **Reversibility:** Each step can be rolled back independently

**Implementation Pattern (Rust Example):**

```rust
// Anti-pattern: Monolithic operation
pub fn checkout_pr(&self, pr_number: u32) -> Result<PathBuf> {
    // This modifies trunk directory as side effect!
    Command::new("gh")
        .args(&["pr", "checkout", &pr_number.to_string()])
        .output()?;

    // Then tries to create worktree from checked-out branch
    self.create_worktree(...)?;  // FAILS: branch already checked out
}

// Pattern: Composable primitives
pub fn fetch_pr_ref(&self, pr_number: u32) -> Result<String> {
    // Returns ref name, no side effects
    let output = Command::new("gh")
        .args(&["pr", "view", &pr_number.to_string(),
                "--json", "headRefName", "-q", ".headRefName"])
        .output()?;
    Ok(String::from_utf8(output.stdout)?.trim().to_string())
}

pub fn fetch_branch(&self, remote_ref: &str, local_name: &str) -> Result<()> {
    // Fetches branch, no checkout side effect
    self.execute_git(&["fetch", "origin",
                       &format!("{}:{}", remote_ref, local_name)])?;
    Ok(())
}

pub fn create_worktree(&self, path: &Path, branch: &str) -> Result<()> {
    // Creates worktree, explicit operation
    self.execute_git(&["worktree", "add",
                       path.to_str().unwrap(), branch])?;
    Ok(())
}

// Composition: Clear, testable, debuggable
pub fn checkout_pr(&self, pr_number: u32, worktree_path: &Path) -> Result<PathBuf> {
    let remote_ref = self.fetch_pr_ref(pr_number)?;
    let local_branch = format!("pr-{}", pr_number);

    self.fetch_branch(&remote_ref, &local_branch)?;
    self.create_worktree(worktree_path, &local_branch)?;

    Ok(worktree_path.to_path_buf())
}
```

**State Validation Pattern:**

```rust
// Validate state before and after operations
pub async fn create_pr_worktree(&self, pr_number: u32) -> Result<PathBuf> {
    // Precondition: Validate trunk is on expected branch
    let trunk_branch = self.get_current_branch(&trunk_path)?;
    if trunk_branch != self.config.default_branch {
        return Err(anyhow!("Trunk must be on {} before PR checkout",
                          self.config.default_branch));
    }

    // Operation
    let worktree_path = self.checkout_pr(pr_number, &target_path)?;

    // Postcondition: Verify trunk unchanged
    let trunk_branch_after = self.get_current_branch(&trunk_path)?;
    if trunk_branch != trunk_branch_after {
        return Err(anyhow!("Operation corrupted trunk branch state"));
    }

    Ok(worktree_path)
}
```

**Testing Strategy:**

```rust
#[cfg(test)]
mod tests {
    // Test each primitive independently
    #[test]
    fn test_fetch_pr_ref_returns_branch_name() {
        let ref_name = git.fetch_pr_ref(123)?;
        assert!(ref_name.contains("feat/"));
    }

    #[test]
    fn test_fetch_branch_no_checkout_side_effect() {
        let before = git.get_current_branch(&repo)?;
        git.fetch_branch("feat/new-thing", "pr-123")?;
        let after = git.get_current_branch(&repo)?;
        assert_eq!(before, after);  // No side effect
    }

    #[test]
    fn test_create_worktree_explicit_effect() {
        git.create_worktree(&path, "pr-123")?;
        assert!(path.exists());  // Expected effect
    }
}
```

**Failure Mode Recovery:**

```rust
// Each operation is reversible independently
pub async fn create_pr_worktree_safe(&self, pr_number: u32) -> Result<PathBuf> {
    let local_branch = format!("pr-{}", pr_number);

    // Step 1: Fetch
    if let Err(e) = self.fetch_pr_ref(pr_number) {
        // No cleanup needed, no state changed
        return Err(e);
    }

    // Step 2: Fetch branch
    if let Err(e) = self.fetch_branch(&remote_ref, &local_branch) {
        // Cleanup: Delete any partial refs
        let _ = self.delete_local_branch(&local_branch);
        return Err(e);
    }

    // Step 3: Create worktree
    if let Err(e) = self.create_worktree(&path, &local_branch) {
        // Cleanup: Delete fetched branch, no worktree to remove
        let _ = self.delete_local_branch(&local_branch);
        return Err(e);
    }

    Ok(path)
}
```

**Key Lessons:**

1. **Avoid convenience commands in automation** - They optimize for interactive use, not composability
2. **Prefer explicit over implicit** - Side effects should be in function names (create_*, delete_*, update_*)
3. **Validate state boundaries** - Check preconditions and postconditions explicitly
4. **Design for failure** - Each operation should leave system in valid state even if next operation fails
5. **Test isolation** - Unit test each primitive, integration test compositions

**Related Patterns:**
- **Command Pattern:** Each git operation is a command with execute/undo
- **Transaction Pattern:** Operations are atomic, all-or-nothing
- **State Machine:** Repository state transitions are explicit and validated

**See Also:**
- `git-state-recovery.md` - Recovery procedures when state is corrupted
- `layered-bug-diagnosis.md` - Debugging multi-layer operations

### 5. Documentation Patterns (Obsidian Vault)

**Key Patterns:**

- Custom data management system called Frontmatters (git@github.com:delorenj/frontmatters)
- Complexity/effort metrics instead of time estimates
- Obsidian vault at `$VAULT` (`~/code/DeLoDocs`)
- Project-based folder structure
- Daily note (One BIG Daily Activity Note per year)
- **Every repo has matching vault folder**

**Critical Relationship:**

```
$CODE/project-name/          → $VAULT/Projects/project-name/
Term: 33GOD (codename for agentic pipeline that contains many microservices)
```

## Usage Workflow

### When Creating New Projects

1. **Check for existing project patterns:**
   - Search conversations for similar projects
   - Extract naming conventions from matches
   - Reference tech stack choices

2. **Apply iMi structure:**
   - Suggest worktree organization
   - Provide setup commands
   - Reference existing worktree conventions

3. **Generate PRD using pattern:**
   - Use complexity metrics, not dates
   - Include user personas from past PRDs
   - Apply consistent structure

### When Suggesting Architecture

1. **Reference existing stack patterns:**

- Default to FastAPI + PostgreSQL + React + Vite + Tailwind + ShadCN
- Suggest Docker Compose configuration
- Apply layered abstraction principles

2. **Check for integration patterns:**
   - Look for past integrations of similar services
   - Reference existing configurations
   - Suggest tested patterns

3. **Apply naming conventions:**
   - Match file/folder structures
   - Use established branch naming
   - Follow API conventions

### When Generating Code

1. **Extract code style from history:**
   - Utilize Composition patterns
   - Leverage Event Driven patterns
   - Search for similar implementations before REINVENTING
   - Utilize Command Pattern, Factory Pattern
   - Match comment styles

2. **Reference existing utilities:**
   - Check for helper functions
   - Look for custom hooks/components
   - Find configuration patterns

3. **Apply architectural patterns:**
   - Layered abstraction (data/logic/presentation)
   - API-first design
   - Modular microservices

## Pattern Mining Process

### What to Look For in Conversations

**Project Requests:**

- What tech stacks are chosen?
- How are projects structured?
- What naming conventions emerge?

**Problem-Solving Patterns:**

- What approaches are preferred?
- Which tools are frequently mentioned?
- What trade-offs are discussed?

**Code Reviews:**

- What feedback is given repeatedly?
- What patterns are praised?
- What anti-patterns are corrected?

**Documentation Style:**

- NEVER ADD to the number of Documents
- Keep them concice and to the point
- Docs should only serve a few purposes:
  - PRD
  - Architecture overviews
  - Roadmap with milestones (NO DATES, use complexity/effort points)
  - Step-by-step Runbooks to show how to do common tasks
  - ONE SINGLE Root Level README.md per repo
  - NEVER create backups or docs or scripts - rely on GIT !!
  - NEVER put documents randomly in the root of a repo - use the vault for that
  - After each large task, prune and refactor docs to keep them minimal and useful.

> [!IMPORTANT] **Document Pruning Rule:**
> Rule of thumb: If you created 10 docs in a session, delete 9 of them and keep only the best one.

**HIGH CONFIDENCE (3+ occurrences):**

- Apply automatically
- Reference explicitly
- Use as defaults

**MEDIUM CONFIDENCE (2 occurrences):**

- Suggest as option
- Confirm before applying
- Mention alternative exists

**LOW CONFIDENCE (1 occurrence):**

- Don't apply automatically
- Ask for clarification
- Learn from response

## Critical Reminders

**Universal Paths:**

- All projects: `$CODE` = `~/code/`
- Documentation: `$VAULT` = `~/code/DeLoDocs`
- Containers: `~/docker/trunk-main/` (DeLoContainers)
- Shell config: `~/.config/zshyzsh`
- ALWAYS use absolute paths: `/home/delorenj/code/project`
- NEVER use relative paths unless explicitly requested
- Every repo in `$CODE` has matching folder in `$VAULT/Projects/`

**Stack Awareness:**

- Backend: FastAPI + PostgreSQL + Redis
- Frontend: React + Vite + Tailwind + ShadCN
- Python: UV for package management
- Runtime: Node/Bun
- AI: Agno agents, FastMCP
- MCP: FastMCP for tool servers
- Never assume Next.js or Supabase unless explicitly mentioned

**Workflow Patterns:**

- iMi worktrees for all project organization
- Mise for tool versioning
- Modular zsh configs in `~/.config/zshyzsh`
- **ALL aliases in `$ZC/aliases.zsh`, NEVER in `.zshrc`**
- Docker Compose for services in `~/docker`
- Vault docs in `$VAULT/Projects/` for every project

**Communication Style:**

- Direct, concise, technical authority
- No em dashes
- Medium-depth explanations (~200 words)
- Speak as peer and best friend that's hanging out having some beer and coding together!
- Don't be serious all the time - absurd humor is welcome!

## Resources

### scripts/

- `pattern_miner.py` - Analyzes conversation history for patterns
- `prd_extractor.py` - Extracts PRD structure patterns
- `naming_analyzer.py` - Identifies naming convention patterns

### references/

- `docker_patterns.md` - Comprehensive Docker/compose patterns
- `zshyzsh_patterns.md` - Shell configuration patterns
- `project_patterns.md` - iMi workflow and project structures
- `code_patterns.md` - Language-specific style guides
- `prd_template.md` - Standard PRD structure with examples

### assets/

- `prd_template.md` - Reusable PRD template
- `docker-compose.yml` - Standard compose file template
- `worktree_setup.sh` - iMi initialization script
