---
name: setup-project
description: Explore a target project and generate tailored recipes and config through an interactive workflow. Use when user wants to onboard a new project to AutoSkillit, says "setup project", or wants a starting point config.
hooks:
  PreToolUse:
    - matcher: "*"
      hooks:
        - type: command
          command: "echo '[SKILL: setup-project] Exploring target project...'"
          once: true
---

# Setup Project Skill

Explore a target project and generate tailored recipes and AutoSkillit config through an interactive, workflow-first UX.

## When to Use

- User wants to onboard a new project to AutoSkillit
- User passes a project path and wants ready-to-use recipes
- User has no `.autoskillit/config.yaml` and wants a starting point

## Arguments

```
/autoskillit:setup-project {project_dir}
```

- `project_dir` — Absolute path to the target project to onboard

## Critical Constraints

**NEVER:**
- Modify any files in the target project without user confirmation at the summary gate
- Run commands that change the target project
- Create files outside `temp/setup-project/` directory (until the summary gate)
- Assume test framework — detect it from evidence
- Use Makefile or `make` in generated examples — use Taskfile/`task` if a task runner is needed
- Suggest `reset_guard_marker` config — that's a workspace concern, not project setup
- Include install instructions or "Getting Started" sections — user is already running the skill
- Hardcode `base_branch = main` — detect the current branch

**ALWAYS:**
- Read the target project using Glob, Read, and Grep — no shell commands against target
- Use `model: "sonnet"` when spawning all subagents via the Task tool
- Detect language, test framework, build system, and CI from actual files
- Present candidate workflows one by one for user approval before generating scripts
- Show a summary confirmation gate before writing anything to disk
- Use the two-directory model (project_dir + work_dir) in generated recipes

## Workflow

### Step 0: Parse Arguments and Prompt

Extract `project_dir` from the prompt. Invocation: `/autoskillit:setup-project {project_dir}`. If missing, abort: "Usage: `/autoskillit:setup-project /absolute/path/to/project`". Resolve to absolute path. Verify the directory exists.

**Validate project_dir before exploring:** Confirm `{project_dir}` exists and is a git
repository before launching subagents:

```bash
ls "{project_dir}"
git -C "{project_dir}" rev-parse --is-inside-work-tree
```

If the directory does not exist or is not a git repo, stop immediately and report the error to
the user. Do not assume any internal paths (`src/`, `tests/`, etc.) exist until the directory
structure has been verified in Step 1.

Then prompt the user:

> "Would you like me to also scan your Claude Code conversation history for this project to identify recurring patterns that could become recipes?"

Store the answer for Step 1.

### Step 1: Explore Target Project (Parallel Subagents)

Launch parallel Explore subagents against `project_dir`. If the user opted into history mining, include Subagent E in the same parallel launch:

**Subagent A — Language & Build System:**
- Read `pyproject.toml`, `setup.py`, `package.json`, `go.mod`, `Cargo.toml`, `build.gradle`, `pom.xml`
- Check for `Taskfile.yml`, `justfile`
- Detect primary language(s) and package manager
- Detect worktree setup command: if `Taskfile.yml` has `install-worktree` task use `["task", "install-worktree"]`; for Python+uv use `["uv", "venv", ".venv", "&&", "uv", "pip", "install", "-e", ".[dev]", "--python", ".venv/bin/python"]`; for Python+pip use `["python", "-m", "venv", ".venv", "&&", ".venv/bin/pip", "install", "-e", ".[dev]"]`; for Node npm use `["npm", "install"]`; for Node pnpm use `["pnpm", "install"]`; for Rust use `["cargo", "fetch"]`; for Go use `["go", "mod", "download"]`

**Subagent B — Test Framework:**
- Python: `pytest.ini`, `pyproject.toml [tool.pytest]`, `conftest.py`, `tests/`
- JS/TS: `jest.config.*`, `vitest.config.*`, `.mocharc.*`
- Go: `*_test.go` files
- Rust: `#[test]` in source files
- Determine the exact test command

**Subagent C — Project Structure & Critical Paths:**
- Glob source directories (`src/`, `lib/`, `pkg/`, `app/`, `internal/`)
- Identify schema definitions, migrations, core config, API routes
- These become candidates for `classify_fix.path_prefixes`
- Detect monorepo workspaces: `pnpm-workspace.yaml`, `Cargo.toml [workspace]`, `go.work`, Nx `project.json`, Lerna `lerna.json`
- Read README.md (first 100 lines) for project description

**Subagent D — Existing AutoSkillit Config:**
- Check for `.autoskillit/config.yaml` — read if present
- Check for `.autoskillit/recipes/` — list any recipes
- Check for `CLAUDE.md` — extract project constraints
- Check for `.autoskillit/workflows/` — list any custom workflows

**Subagent E — Current Git Branch:**
- Run `git -C {project_dir} branch --show-current`
- This becomes the default `base_branch` in generated scripts

**Subagent F+ — Conversation History Mining (only if user opted in):**

Claude Code stores conversation history at `~/.claude/projects/<encoded-path>/` as JSONL files (one per session). The path encoding replaces `/` and `_` with `-` (e.g., `/home/user/my_project` -> `-home-user-my-project`).

1. Compute the encoded directory name from `project_dir`
2. List all `.jsonl` files in `~/.claude/projects/<encoded-name>/`, including subagent files in `<session-uuid>/subagents/agent-*.jsonl`
3. Sort by modification time (newest first)
4. Divide into batches of ~20-30 files per subagent — launch multiple parallel subagents if needed

Each history-mining subagent:
- Reads JSONL files line by line and extracts:
  - **Skill invocations**: `type: "user"` messages where `content` contains `<command-name>/skill-name</command-name>`. Extract skill name and args.
  - **Tool call sequences**: `type: "assistant"` messages -> `message.content[]` items with `type: "tool_use"`. Extract `name` and `input`. Build ordered tool-call sequences per session.
  - **Repeated multi-step patterns**: Same tool sequence appearing across multiple sessions (e.g., always `Bash(git checkout) -> Edit -> Edit -> Bash(pytest) -> Bash(git commit)`).
  - **Common skill chains**: Skill invocations that follow a consistent order (e.g., `/autoskillit:investigate` -> `/autoskillit:rectify` -> `/autoskillit:implement-worktree`).
  - **Repeated `run_cmd` commands**: Exact shell commands run frequently via Bash tool.
- Returns structured findings: frequency-ranked tool sequences (min 3 occurrences), skill chains, and notable single-tool patterns

### Step 2: Synthesize Project Profile

Consolidate subagent findings into a structured profile:
- Language + package manager
- Test command (exact list form, e.g. `["pytest", "-v"]`)
- Build/lint tools
- Critical paths (for classify_fix)
- Whether a reset mechanism exists (Taskfile `clean` target, npm script, etc.)
- Worktree setup command (command to run after `git worktree add`)
- Existing config state (none / partial / complete)
- Current git branch (for `base_branch` default)
- Discovered workflow patterns from conversation history (if opted in) — recurring tool sequences and skill chains, ranked by frequency, with candidate recipe drafts

### Step 3: Write Analysis to temp/ (relative to the current working directory)

Before presenting anything interactively, write the full analysis (project profile, workflow patterns, candidate workflows, shell command patterns) to:

```
temp/setup-project/analysis_{project_name}_{YYYY-MM-DD_HHMMSS}.md
```

Tell the user: "Full analysis saved to {path} for your review."

### Step 4: Present Candidate Workflows

Interactive flow. For each candidate workflow discovered:

**CRITICAL:** Do NOT output any prose status text between workflow iterations.
After completing one workflow's presentation and user response, immediately
begin presenting the next workflow.

1. **Always offer the standard implementation pipeline first** (plan → dry-walkthrough → implement → test → merge), even if not discovered in history. This is the core AutoSkillit workflow.

2. For each candidate workflow (including the standard one):
   Do NOT output any prose status text between workflows — immediately begin the
   next workflow's presentation after the user responds.
   - Present the workflow chain and explain what it automates
   - Ask the user: "Would you like me to generate a recipe for this workflow?"
   - Before generating, resolve skill references in the workflow:
     - For each skill in the detected chain (no prose between skills), check if it exists both locally
       (`.claude/skills/<name>/SKILL.md`) and as a bundled autoskillit skill
     - If any skill exists in both, present the conflicts to the user as a batch:
       > "These skills exist in both your project and AutoSkillit's bundled set:
       > - `<name>` → local (bare `/<name>`) or bundled (`/autoskillit:<name>`)?
       > Local versions are recommended. Should I use local for all, or do you want
       > to pick individually?"
       List each conflicting skill name on its own line in the prompt.
     - Record the user's preferences and pass them as context to write-recipe
   - If yes: LOAD `/autoskillit:write-recipe` using the Skill tool to generate the script. The agent already has full context from the exploration phases (workflow name, detected variables like project_dir/work_dir/base_branch, tool call sequence, routing logic) — no explicit parameter passing is needed. write-recipe uses that context directly to produce a clean script.
   - Explain what a recipe is (discovered via `list_recipes` MCP tool, loaded via `load_recipe`, the agent interprets the YAML and executes the steps), show the generated script content
   - Track the user's approval — do NOT write to disk yet
   - Move to the next candidate workflow

Fill in detected values: test command, base branch, project-specific notes, any detected quirks. Use the two-directory model (project_dir + work_dir) in generated scripts. If `work_dir` equals `project_dir`, note that `add_dir` is not needed.

### Step 5: Config Updates

Interactive config suggestion flow:

1. Show the current config vs. suggested config diff
2. For each suggested change, ask the user if they want to apply it
3. Track approvals — do NOT write to disk yet
4. Do NOT suggest `reset_guard_marker` — that's a workspace concern, not project setup
5. Ask the user for their preferred default base branch:
   > "What is your default base branch? (e.g., 'integration' for the 3-tier model, 'main' for the classic model)"
   > Default: `integration`
   If the user selects a value different from the package default (`integration`), add it to the config diff as:
   ```yaml
   branching:
     default_base_branch: {user_choice}
   ```

If no config exists, present the suggested config in full. If config exists, only highlight missing or suboptimal settings.

Suggested config template:
```yaml
test_check:
  command: {detected test command as list}
  # timeout: 600

# classify_fix:
#   path_prefixes:
#     - {detected critical paths}

# reset_workspace:
#   command: {detected reset command}
#   preserve_dirs: []

# worktree_setup:
#   command: {detected worktree setup command}
```

### Step 6: Summary Confirmation Gate

Following the Terraform plan→apply pattern, show a summary of everything approved before touching disk:

1. For each approved recipe, save to `.autoskillit/recipes/{name}.yaml`
2. List all approved recipes with their save paths
3. List all approved config changes
4. Ask one final question: "Write all of the above?"
5. If confirmed:
   - Create target directories as needed
   - Write all approved recipes to their chosen paths
   - Apply all approved config changes
6. If declined: abort without writing anything

This prevents incremental approval fatigue and gives the user a single clear decision point.

### Step 7: Output Summary

Write a concise summary to terminal:
- Which scripts were saved and where
- Which config changes were applied
- Any notes or warnings (e.g., test timeout may need adjustment, critical paths are inferred)

Do NOT include:
- Install instructions (user is already running the skill)
- "Getting Started" sections
- Repeated content from earlier steps

## Output

Artifacts created:
- `temp/setup-project/analysis_{project_name}_{YYYY-MM-DD_HHMMSS}.md` — full analysis (always)
- `.autoskillit/recipes/{name}.yaml` — approved recipes
- `.autoskillit/config.yaml` — updated config (if changes approved)

After the summary confirmation gate completes (Step 7), emit the following structured
output tokens as the very last lines of your text output:

```
analysis_path = {absolute_path_to_analysis_file}
config_path = {absolute_path_to_config_file}
```

Emit `config_path` only if `.autoskillit/config.yaml` was written in this session.
If no config changes were applied, omit the `config_path=` line.