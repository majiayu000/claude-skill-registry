---
name: enhance-project
description: Enhance existing projects with Claude Code agents, skills, and quality improvements. Analyzes your codebase and adds best-practice tooling.
hooks:
  SubagentStart:
    - hooks:
        - type: command
          command: |
            echo ""
            echo "┌─────────────────────────────────────┐"
            case "$AGENT_TYPE" in
              "codebase-explorer") echo "│ 🔍 Exploring codebase structure" ;;
              "dependency-analyzer") echo "│ 📦 Analyzing dependencies" ;;
              "pattern-finder") echo "│ 🎯 Finding code patterns" ;;
              "test-writer") echo "│ 🧪 Generating tests" ;;
              "refactor-planner") echo "│ 🔧 Planning refactoring" ;;
              "debugger") echo "│ 🐛 Debugging issues" ;;
              "feature-planner") echo "│ 📋 Planning improvements" ;;
              *) echo "│ 🤖 Agent: $AGENT_TYPE" ;;
            esac
            echo "└─────────────────────────────────────┘"
  SubagentStop:
    - hooks:
        - type: command
          command: "echo '   ✓ $AGENT_TYPE complete'"
  Stop:
    - hooks:
        - type: prompt
          prompt: |
            Verify that /enhance-project completed properly:

            1. Was the target project validated?
            2. Was the project type and tech stack detected?
            3. Were existing Claude Code resources checked?
            4. Did the selected enhancement phases complete?
            5. Was the enhancement report generated?

            Context: $ARGUMENTS

            Return {"ok": true} if the enhancement completed successfully.
            Return {"ok": false, "reason": "specific issue"} if incomplete.
          timeout: 30
---

# Enhance Existing Project

## Instructions

**IMPORTANT: Execute immediately. Do NOT explore the codebase first or propose a plan. Start Step 1 right now.**

Default mode is **Full Enhancement** (resources + analysis + improvements). If the user passed an argument, select the matching mode:
- `resources` → Steps 1-7 only (add agents, skills, CLAUDE.md - no code changes)
- `analysis` → Steps 1-4, 8 only (report only, no changes)
- `improvements` → Steps 1-4, 9-10 only (fix issues, refactor, add tests)
- `claudemd` → Steps 1-4, 7 only (review/improve CLAUDE.md only)
- No argument or `full` → Full Enhancement (all steps)

---

### Step 1: Validate Target Project

```bash
TARGET_DIR="${1:-.}"
TARGET_DIR=$(cd "$TARGET_DIR" && pwd)

if [ ! -d "$TARGET_DIR" ]; then
  echo "❌ Directory does not exist: $TARGET_DIR"
  exit 1
fi

if [ ! -f "$TARGET_DIR/package.json" ] && \
   [ ! -f "$TARGET_DIR/Cargo.toml" ] && \
   [ ! -f "$TARGET_DIR/pyproject.toml" ] && \
   [ ! -f "$TARGET_DIR/go.mod" ] && \
   [ ! -f "$TARGET_DIR/pom.xml" ] && \
   [ ! -f "$TARGET_DIR/build.gradle" ]; then
  echo "⚠️  No recognized project manifest found"
fi

cd "$TARGET_DIR" || exit 1
PROJECT_NAME=$(basename "$TARGET_DIR")

echo ""
echo "🔧 Enhancing project: $PROJECT_NAME"
echo "📁 Location: $TARGET_DIR"
echo ""
```

---

### Step 2: Detect Project Type and Tech Stack

Use Glob to find manifest files and Read the main ones (package.json, etc.) to detect:
- Primary language (TypeScript, JavaScript, Python, Go, Rust, Java)
- Framework (Next.js, Express, React, FastAPI, etc.)
- Build tools (npm, yarn, pnpm, cargo, pip, go)
- Testing framework (Jest, Vitest, Pytest, etc.)
- Database (if present)

Do this with direct Glob + Read calls, NOT an Explore agent. Keep it under 30 seconds.

---

### Step 3: Check Existing Claude Code Resources

```bash
echo "🔍 Checking existing Claude Code resources..."

if [ -d ".claude/agents" ]; then
  AGENT_COUNT=$(find .claude/agents -name "*.md" 2>/dev/null | wc -l)
  echo "   ✓ Agents directory exists ($AGENT_COUNT agents)"
else
  echo "   ○ No agents directory"
fi

if [ -d ".claude/skills" ]; then
  SKILL_COUNT=$(find .claude/skills -maxdepth 2 -name "SKILL.md" 2>/dev/null | wc -l)
  echo "   ✓ Skills directory exists ($SKILL_COUNT skills)"
else
  echo "   ○ No skills directory"
fi

if [ -f "CLAUDE.md" ]; then
  echo "   ✓ CLAUDE.md exists"
else
  echo "   ○ No CLAUDE.md"
fi

if [ -d "plans" ]; then
  echo "   ✓ Plans directory exists"
else
  echo "   ○ No plans directory"
fi
```

---

### Step 4: Assess Existing CLAUDE.md Quality

If CLAUDE.md exists, Read it and score against these criteria (0-100):

- **Completeness (25 pts)**: Has Overview, Tech Stack, Project Structure, Commands, Key Files sections
- **Accuracy (25 pts)**: Tech stack matches manifests, file paths exist, commands work
- **Specificity (20 pts)**: Contains project-specific patterns, not generic boilerplate
- **Code Examples (15 pts)**: Has actual code examples from this project
- **Maintenance (15 pts)**: Versions match current dependencies, no stale info

If score < 80, note improvements needed. Present the score to the user.

---

### Step 5: Copy Agents

```bash
mkdir -p .claude/agents

# Based on detected tech stack, select appropriate agents:
# - All projects: codebase-explorer, pattern-finder, debugger
# - Web projects: add ui-ux-designer, component-builder, api-developer
# - API projects: add api-developer, test-writer, architecture-planner
# - Libraries: add test-writer, pattern-finder, dependency-analyzer
```

Copy agents from the global `~/.claude/agents/` directory into the project's `.claude/agents/`. Create subdirectories (explore/, plan/, implement/, design/) as needed.

---

### Step 6: Copy Skills

```bash
mkdir -p .claude/skills

# Core workflow skills (all projects)
CORE_SKILLS="ship verify-work organize-commits track-progress"

# Development skills
DEV_SKILLS="create-plan plan-status generate-tests performance-check"

# Git workflow skills
GIT_SKILLS="worktree-create worktree-sync worktree-cleanup"
```

Copy skills from the global `~/.claude/skills/` directory into the project's `.claude/skills/`.

---

### Step 7: Create/Update CLAUDE.md

If no CLAUDE.md exists, or if the quality score from Step 4 is < 80:

1. Select the appropriate template from `templates/claude-md/` based on detected tech stack:
   - Next.js → `nextjs-app.md`
   - Express/Fastify/NestJS → `api-service.md`
   - CLI tool → `cli-tool.md`
   - React library → `node-library.md`
   - Python project → `python-app.md`
   - Game → `game-browser.md`
   - Unknown → `minimal.md`

2. If creating new: Generate from template, replacing placeholders with actual values
3. If improving existing: Preserve custom content, fix low-scoring sections only
4. Validate the result meets quality standards

---

### Step 8: Run Codebase Analysis

**Invoke three agents in parallel** using the Task tool in a single message:

1. **codebase-explorer** - "Analyze this project and report: primary language/version, frameworks, project structure pattern, key directories, build/test configuration"

2. **dependency-analyzer** - "Analyze dependencies: security vulnerabilities, outdated packages, unused dependencies, circular dependencies, license compatibility"

3. **pattern-finder** - "Identify code patterns: style/formatting conventions, naming conventions, import patterns, error handling, testing patterns, documentation patterns"

**Wait for all three to complete**, then synthesize findings into a report for the user.

---

### Step 9: Generate Tests

1. Identify untested code by comparing source files to test files
2. **Invoke `/generate-tests`** using the Skill tool to create missing test files
3. Report what was generated

---

### Step 10: Apply Code Improvements

**IMPORTANT:** This step makes actual code changes. Confirm with the user before proceeding.

1. **Invoke both in parallel** using the Skill tool in a single message:
   - `/verify-work` - security, best practices, standards
   - `/performance-check` - performance anti-patterns

2. Present findings to the user and get approval to fix

3. Apply fixes for approved issues:
   - Security vulnerabilities (blocking)
   - Performance bottlenecks
   - Code standard violations

---

### Step 11: Create Development Plan

1. **Invoke `/create-plan`** using the Skill tool with name "improvements"
2. This creates `plans/active/improvements/plan.md` with prioritized tasks based on analysis

---

### Step 12: Organize Commits (if changes were made)

1. **Invoke `/organize-commits`** using the Skill tool to create logical commits:
   - `feat: add Claude Code agents and skills`
   - `refactor: improve code structure` (if improvements applied)
   - `fix: resolve security issues` (if security fixes applied)
   - `test: add comprehensive test coverage` (if tests generated)
   - `docs: add CLAUDE.md and improve documentation`

2. **Invoke `/track-progress`** using the Skill tool to record enhancements

---

### Step 13: Generate Enhancement Report

Present a summary:

```markdown
## Enhancement Complete: [PROJECT_NAME]

### Resources Added
- Agents: [count] agents in .claude/agents/
- Skills: [count] skills in .claude/skills/
- CLAUDE.md: [created/improved] (quality score: [X]/100)

### Analysis Results
- [Summary from codebase-explorer]
- [Summary from dependency-analyzer]
- [Summary from pattern-finder]

### Code Improvements
- Security issues fixed: [count]
- Performance issues fixed: [count]
- Tests generated: [count] files

### Next Steps
1. Review CLAUDE.md for accuracy
2. Check plans/active/improvements/plan.md for suggested tasks
3. Use /plan-status to track improvements
4. Use /ship at the end of each session
```

---

## Reference

### Enhancement vs Starter Project

| Aspect | `/starter-project` | `/enhance-project` |
|--------|-------------------|-------------------|
| **Target** | New projects | Existing projects |
| **Creates files** | Yes (scaffold) | Minimal (resources only) |
| **Analyzes code** | No existing code | Yes, deeply |
| **Generates tests** | For new code | For existing code |
| **Creates plan** | Getting-started | Improvements |
| **Respects existing** | N/A | Yes, non-destructive |

### Tips

- **Backup first**: Consider committing before enhancing
- **Review CLAUDE.md**: Generated conventions may need adjustment
- **Check the plan**: Improvement plan prioritizes based on analysis
- **Re-run analysis**: Use `analysis` mode after making changes
