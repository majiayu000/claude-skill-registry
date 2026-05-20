---
name: starter-project
description: Generate starter projects pre-configured with Claude Code agents and skills. Choose from SaaS app, API service, component library, CLI tool, e-commerce, or browser game templates.
---

# Starter Project Generator

## Instructions

**IMPORTANT: Execute immediately. If the user provided a category argument, start building. If not, ask the user to choose a template using AskUserQuestion - do NOT print a menu and wait.**

Parse arguments:
- `$1` = category: `saas`, `api`, `components`, `cli`, `ecommerce`, `game`
- `$2` = project name (if not provided, ask the user)

If no category was provided, use AskUserQuestion to ask which template they want:
- **SaaS Web App** - Full-stack Next.js with auth and dashboard
- **API Service** - Node.js REST API with testing
- **Component Library** - React components with Storybook
- **CLI Tool** - Command-line application
- **E-Commerce Store** - Next.js store with Stripe integration
- **Browser Game** - Canvas/Phaser game

Once you have category and name, proceed immediately to Step 1.

---

### Step 1: Set Up Template Configuration

Based on the category, determine tech stack and which agents to copy:

| Category | Tech Stack | Agents |
|----------|-----------|--------|
| saas | Next.js 14, TypeScript, Tailwind, NextAuth, Drizzle | All |
| api | Node.js, Express, TypeScript, Vitest | explore/*, plan/architecture-planner, implement/api-developer, implement/test-writer, implement/debugger |
| components | React, TypeScript, Storybook, Vitest, CSS Modules | explore/pattern-finder, plan/feature-planner, implement/component-builder, implement/test-writer, design/ui-ux-designer |
| cli | Node.js, TypeScript, Commander.js, Vitest | explore/pattern-finder, implement/test-writer, implement/debugger |
| ecommerce | Next.js 14, TypeScript, Stripe, Drizzle | All |
| game | TypeScript, Phaser.js, Vite | explore/codebase-explorer, implement/component-builder, implement/debugger, design/ui-ux-designer |

---

### Step 2: Select CLAUDE.md Template

Map category to template file:
- saas/ecommerce → `templates/claude-md/nextjs-app.md`
- api → `templates/claude-md/api-service.md`
- components → `templates/claude-md/node-library.md`
- cli → `templates/claude-md/cli-tool.md`
- game → `templates/claude-md/game-browser.md`

---

### Step 3: Create Project Directory

```bash
PROJECT_NAME=$(echo "$PROJECT_NAME" | tr '[:upper:]' '[:lower:]' | tr '_' '-' | tr ' ' '-')
TARGET_DIR="../$PROJECT_NAME"

if [ -d "$TARGET_DIR" ]; then
  echo "❌ Directory already exists: $TARGET_DIR"
  exit 1
fi

mkdir -p "$TARGET_DIR"
cd "$TARGET_DIR" || exit 1
git init -q
echo "✓ Created project directory and initialized git"
```

---

### Step 4: Copy Agents and Skills

Copy agents from `~/.claude/agents/` to `.claude/agents/` based on the agent list for this category (from Step 1).

Copy these workflow skills from `~/.claude/skills/` to `.claude/skills/`:
- Core: `ship`, `verify-work`, `organize-commits`, `track-progress`
- Development: `create-plan`, `plan-status`, `generate-tests`, `performance-check`
- Git: `worktree-create`, `worktree-sync`, `worktree-cleanup`

---

### Step 5: Phase 1 - Setup & Planning

1. Create `plans/active` directory

2. **Invoke `/create-plan`** using the Skill tool with name "getting-started" and template "guide"

3. Use the Task tool to invoke **architecture-planner** agent: "Design a [TEMPLATE_NAME] project called [PROJECT_NAME] with tech stack: [TECH_STACK]. Include: project structure, data models (if applicable), API endpoints, component hierarchy"

---

### Step 6: Phase 2 - Design

**Invoke both agents in parallel** using the Task tool in a single message:

1. **ui-ux-designer** - "Create a design system for [PROJECT_NAME] ([TEMPLATE_NAME]) with: professional color palette (not AI-generic), typography scale, spacing system, component designs for Button/Input/Card, layout structure appropriate for [TEMPLATE_NAME]"

2. **feature-planner** - "Plan the initial features for [PROJECT_NAME] ([TEMPLATE_NAME]). Break down into small tasks for the getting-started plan. Map each task to the appropriate agent"

---

### Step 7: Phase 3 - Implementation

1. Generate base configuration files (package.json, tsconfig.json, etc.) based on the category

2. Create CLAUDE.md from the template selected in Step 2:
   - Copy template, replace placeholders ([Project Name], etc.) with actual values
   - Fill in tech stack, update project structure, add category-specific patterns
   - Follow quality standards from `docs/best-practices/claude-md-authoring.md`

3. Use the Task tool to invoke **api-developer** agent: "Create initial API endpoints for [PROJECT_NAME]: health check at /api/health, auth endpoints (if applicable), one CRUD resource, include Zod validation and error handling"

4. Use the Task tool to invoke **component-builder** agent: "Build UI components for [PROJECT_NAME]: apply the design system, include TypeScript props, add accessibility features, create loading/error states, build Button/Input/Card and layout components"

---

### Step 8: Phase 4 - Testing & Quality

1. Use the Task tool to invoke **test-writer** agent: "Create comprehensive tests for [PROJECT_NAME]: API endpoint tests, UI component tests, utility tests"

2. **Invoke `/generate-tests`** using the Skill tool to fill any remaining coverage gaps

3. **Invoke both in parallel** using the Skill tool in a single message:
   - `/verify-work` - validate code quality and security
   - `/performance-check` - identify performance issues

Fix any blocking issues found.

---

### Step 9: Phase 5 - Verification

**Invoke three agents in parallel** using the Task tool in a single message:

1. **codebase-explorer** - verify project structure matches the architecture design
2. **dependency-analyzer** - validate all dependencies are correct
3. **pattern-finder** - ensure code patterns are consistent

---

### Step 10: Phase 6 - Ship

1. **Invoke `/organize-commits`** using the Skill tool to create logical commit history:
   - `chore: initial project setup`
   - `feat(db): add database schema` (if applicable)
   - `feat(api): add API endpoints`
   - `feat(ui): add design system and components`
   - `test: add comprehensive test coverage`
   - `docs: add CLAUDE.md and README`

2. **Invoke `/track-progress`** using the Skill tool to record the generation

---

### Step 11: Display Results

```bash
echo "================================================================"
echo "✅ Successfully created [TEMPLATE_NAME]: [PROJECT_NAME]"
echo "================================================================"
echo ""
echo "📁 Location: $TARGET_DIR"
echo "📋 Getting-started plan: plans/active/getting-started/plan.md"
echo ""
echo "🎯 Agents used: architecture-planner, ui-ux-designer, api-developer,"
echo "   component-builder, test-writer, codebase-explorer, dependency-analyzer,"
echo "   pattern-finder, feature-planner"
echo ""
echo "Next steps:"
echo "  1. cd ../$PROJECT_NAME"
echo "  2. npm install"
echo "  3. npm run dev"
echo ""
echo "💡 Commands:"
echo "   /plan-status    - View your getting-started plan"
echo "   /worktree-create - Parallel feature development"
echo "   /ship           - End-of-session workflow"
```

---

## Template Reference

| Category | Template | Tech Stack |
|----------|----------|-----------|
| saas | SaaS Web App | Next.js 14, TypeScript, Tailwind, NextAuth, Drizzle |
| api | API Service | Node.js, Express, TypeScript, Vitest |
| components | Component Library | React, TypeScript, Storybook, Vitest, CSS Modules |
| cli | CLI Tool | Node.js, TypeScript, Commander.js, Vitest |
| ecommerce | E-Commerce Store | Next.js 14, TypeScript, Stripe, Drizzle |
| game | Browser Game | TypeScript, Phaser.js, Vite |

## What Gets Created

All projects include:
- **CLAUDE.md** - Generated from template following best practices
- **.claude/agents/** - Relevant agents for the project type
- **.claude/skills/** - Development workflow skills
- **plans/active/getting-started/** - Initial development plan
- **README.md** - Setup and development instructions
- **Git repository** - Initialized with logical commit history

## Tips

- **Choose the right template**: Match your project type to get relevant agents
- **Review the plan**: Each template includes suggested first features
- **Explore the agents**: Check `.claude/agents/` to see what's available
- **Use the skills**: Workflow skills help maintain code quality
- **Customize freely**: The generated project is yours to modify
