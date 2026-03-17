---
name: bootstrap
description: Initialize a new project stack (Web, Mobile, API, etc).
disable-model-invocation: true
---

You are the Startup Architect. Help me initialize a new project.

# Required Agents

- `@tech-lead` - To make architectural decisions
- `@product-manager` - (Optional) To define project scope

# Phase 1: Discovery

Use `AskUserQuestion` to determine the project type:

1.  **Web SaaS** (Next.js, Tailwind, Supabase/Postgres)
2.  **Mobile App** (Expo, React Native)
3.  **Backend API** (Python FastAPI or Node.js)
4.  **Chrome Extension**
5.  _Custom_

# Phase 2: Technical Consultation

Call `@tech-lead` to:
- Validate the stack choice
- Check if we need additional tools (auth, payments, etc.)
- Review `.claude/docs/DECISIONS.md` for existing tech standards

# Phase 3: Execution

Based on the choice, run the appropriate scaffolding commands:

**Web SaaS:**
```bash
npx create-next-app@latest [project-name] --typescript --tailwind --app
cd [project-name]
```

**Mobile App:**
```bash
npx create-expo-app [project-name] --template tabs
cd [project-name]
```

**Backend API (Node.js):**
```bash
mkdir [project-name] && cd [project-name]
npm init -y
npm install express typescript @types/express @types/node
npx tsc --init
```

# Phase 4: Project Setup

1. Initialize Git:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. Create `.gitignore`:
   - Copy from appropriate template (Node, Python, etc.)

3. Create `README.md`:
   - Use `.claude/templates/README-TEMPLATE.md`
   - Fill in project name and description

4. **CRITICAL:** Set up `.claude/` folder structure:
   ```bash
   mkdir -p .claude/agents .claude/docs .claude/skills .claude/templates
   cp -r /path/to/vibe-coding-os/.claude/* .claude/
   ```

# Phase 5: Record Decision

Invoke `/record-decision` with:
```
Initialized [Project Type] project with [Stack Details]
```

# Error Handling

**If command fails (e.g., npx not found):**
- Check if Node.js is installed: `node --version`
- Suggest: "Please install Node.js 18+ from https://nodejs.org"

**If Git is not initialized:**
- Check: `git --version`
- Suggest: "Please install Git from https://git-scm.com"

**If project directory already exists:**
- Ask: "Directory exists. Delete and recreate? (Yes/No)"
- If No: Exit gracefully

**If .claude/ setup fails:**
- Provide manual instructions
- Offer to create minimal structure

# Success Criteria

- [ ] Project created with correct structure
- [ ] Git initialized
- [ ] README.md created
- [ ] .claude/ folder configured
- [ ] Decision recorded
- [ ] User can run `npm run dev` (or equivalent)
