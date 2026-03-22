---
name: initialize-project
description: |
  Project initialization and setup workflow. Use when starting a new project,
  setting up AI-assisted development environment, or bootstrapping an existing codebase
  with Samuel framework structure.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: workflow
---

# Project Initialization

Set up new projects or adopt CLAUDE.md system in existing projects.

---

## Overview

This skill handles two scenarios:
1. **New Projects**: Bootstrap from scratch with tech stack selection and configuration
2. **Existing Projects**: Analyze codebase and adopt Samuel framework

Both paths result in a fully configured `.claude/` directory with project-specific context.

---

## For New Projects

### Discovery Process

Ask user these questions to configure the project:

**1. Tech Stack**
- Language: TypeScript, Python, Go, Rust, other?
- Framework: React, Django, Express, Axum, other?
- Versions: Which versions should we target?

**2. Architecture**
- Monolith (single deployable)
- Microservices (multiple services)
- Serverless (functions/lambdas)
- Jamstack (static + APIs)

**3. Testing**
- Unit test framework?
- Integration tests needed?
- E2E tests (Playwright, Cypress)?
- Coverage targets?

**4. Deployment**
- Cloud: AWS, GCP, Azure, Vercel, Railway?
- On-premise servers?
- Container platform: Docker, Kubernetes?

**5. Database**
- PostgreSQL, MySQL, MongoDB, SQLite?
- ORM/Query builder preferences?
- Migrations approach?

**6. Additional Requirements**
- Authentication needed?
- API type: REST, GraphQL, gRPC?
- Real-time features (WebSockets)?
- Background jobs?

### Created Artifacts

**1. `CLAUDE.md`**
Document all tech stack decisions and architecture.

**2. Directory Structure**
Create language-appropriate structure (see references/process.md for templates).

**3. Configuration Files**
Generate:
- Language config (tsconfig.json, pyproject.toml, go.mod, Cargo.toml)
- Linter config (ESLint, Ruff, golangci-lint, Clippy)
- Formatter config (Prettier, Black, gofmt, rustfmt)

**4. Essential Files**
- `.gitignore` (language-specific)
- `.env.example` (with secure defaults)
- `README.md` (setup instructions)

---

## For Existing Projects

### Analysis Process

Automatically scan and analyze:

**1. Tech Stack Detection**
```bash
# Check package managers
ls package.json requirements.txt go.mod Cargo.toml

# Identify language
find . -name "*.ts" -o -name "*.py" -o -name "*.go" -o -name "*.rs"
```

**2. Directory Structure Examination**
- Frontend? (src/, components/, pages/)
- Backend? (api/, routes/, controllers/)
- Monorepo? (packages/, apps/)
- Testing setup? (tests/, __tests__, *_test.go)

**3. Code Pattern Analysis**
```bash
# Naming conventions
grep -r "function\|class\|interface" src/

# Testing patterns
head -20 tests/*.test.ts

# Database usage
grep -r "SELECT\|INSERT\|UPDATE" src/
```

**4. Git History Review**
```bash
# Commit message style
git log --pretty=format:"%s" -10

# Branching strategy
git branch -a
```

**5. Existing Tooling Check**
- Linters: ESLint, Ruff, golangci-lint, Clippy?
- Formatters: Prettier, Black, gofmt, rustfmt?
- CI/CD: GitHub Actions, GitLab CI, CircleCI?
- Testing: Jest, pytest, Go testing, cargo test?

### Created Artifacts

**1. `CLAUDE.md`**
Document discovered tech stack and observed patterns.

Example:
```markdown
# Project: ExistingApp

## Discovered Tech Stack
- **Language**: TypeScript 5.1
- **Framework**: Next.js 14 (App Router)
- **Database**: PostgreSQL with Prisma ORM
- **Testing**: Jest + React Testing Library
- **Styling**: Tailwind CSS
- **Deployment**: Vercel

## Observed Patterns
- API routes in `app/api/`
- Components use `use client` directive
- Server actions for mutations
- Zod for API validation
- Conventional commits (mostly followed)

## Gaps Identified
- Test coverage: 45% (target: >60%)
- No pre-commit hooks
- ESLint config basic (missing recommended rules)
- Some files exceed 300 lines (needs refactoring)
- Missing .env.example
```

**2. `CLAUDE.md`**
Extract coding patterns from existing codebase.

Example:
```markdown
# Patterns

## API Error Handling
All API routes use this pattern:
\`\`\`typescript
try {
  const data = await validateInput(req.body);
  const result = await service.process(data);
  return NextResponse.json(result);
} catch (error) {
  return handleAPIError(error);
}
\`\`\`

## Database Queries
Always use Prisma with error handling:
\`\`\`typescript
const user = await prisma.user.findUnique({
  where: { id }
}).catch(handlePrismaError);
\`\`\`
```

**3. Gap Analysis & Recommendations**

Propose improvements:
- Add missing configuration files
- Improve test coverage (identify untested modules)
- Refactor oversized files (list files >300 lines)
- Add pre-commit hooks (husky + lint-staged)
- Update dependencies (security patches)
- Improve documentation

### Adoption Checklist

Confirm with user:
- [ ] Tech stack correctly identified?
- [ ] Architecture pattern accurate?
- [ ] Code conventions match observations?
- [ ] Testing approach correct?
- [ ] Any custom patterns AI should know?
- [ ] Any legacy code to avoid modifying?
- [ ] Any protected files/directories?

Then proceed to:
- [ ] Apply guardrails to new code (don't refactor existing immediately)
- [ ] Suggest incremental improvements
- [ ] Document conventions in `.claude/`
- [ ] Set up recommended tooling (optional)

---

## Post-Initialization

### Verify Setup

**New Projects:**
```bash
# Install dependencies
npm install  # or pip install -r requirements.txt

# Run tests (should pass even if empty)
npm test

# Start dev server
npm run dev

# Check linting
npm run lint
```

**Existing Projects:**
```bash
# Verify .claude/ structure created
ls .claude/

# Read project documentation
cat CLAUDE.md

# Review proposed improvements
cat CLAUDE.md
```

### Next Steps

1. **Review `CLAUDE.md`**
   - Confirm tech stack accurate
   - Add any missing context

2. **Review `CLAUDE.md`** (if existing project)
   - Confirm patterns are correct
   - Add any unobserved patterns

3. **Prioritize Improvements** (if existing project)
   - Security issues: Fix immediately
   - Test coverage: Incremental improvement
   - Refactoring: Gradual (as you touch files)
   - Tooling: Set up recommended tools

4. **Start Development**
   - AI will now follow guardrails
   - AI will load language guide automatically
   - AI will reference patterns from `.claude/`

---

## Common Issues

### Dependencies Won't Install

**Node.js:**
```bash
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

**Python:**
```bash
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

**Go:**
```bash
go clean -modcache
go mod download
```

**Rust:**
```bash
cargo clean
cargo build
```

### Wrong Version

Use version managers:
```bash
# Node.js
nvm install 20 && nvm use 20

# Python
pyenv install 3.11 && pyenv local 3.11

# Go
gvm install go1.21 && gvm use go1.21

# Rust
rustup update stable
```

### AI Not Detecting Tech Stack

Manually specify in `CLAUDE.md`:
```markdown
# Project: MyApp

**Tech Stack**: TypeScript + React + Express
**Database**: PostgreSQL
**Testing**: Jest
```

Then: `"I've updated project.md. Please load the appropriate language guide."`

---

## Customization

### Modify Initial Structure

Edit `.claude/skills/initialize-project/SKILL.md` to customize:
- Default directory structure
- Configuration file templates
- Questions AI asks
- Files AI creates

### Add Company Standards

Create `.claude/company-standards.md`:
```markdown
# Company Standards

## Required Tools
- ESLint with company config
- Prettier with company config
- Husky for pre-commit hooks

## Required Files
- SECURITY.md
- CONTRIBUTING.md
- LICENSE (MIT)

## Deployment
- All projects deploy to AWS
- Use Terraform for infrastructure
- CI/CD via GitHub Actions
```

AI will reference this during initialization.

---

## Success Criteria

- [ ] `CLAUDE.md` created with accurate tech stack
- [ ] `CLAUDE.md` created (if existing project)
- [ ] Directory structure appropriate for language
- [ ] Configuration files generated
- [ ] `.gitignore` includes language-specific entries
- [ ] `.env.example` created with secure defaults
- [ ] README.md has setup instructions
- [ ] Dependencies install successfully
- [ ] Tests run (even if empty)
- [ ] Dev server starts

---

## References

For detailed templates and examples, see:
- `references/process.md` - Full directory structures and configuration templates
- CLAUDE.md - Core guardrails and methodology
- `.claude/skills/{language}-guide/SKILL.md` - Language-specific patterns

---

**Remember**: Initialization is a one-time setup. The `.claude/` directory grows organically as the project evolves. Don't over-document upfront - let patterns emerge naturally.
