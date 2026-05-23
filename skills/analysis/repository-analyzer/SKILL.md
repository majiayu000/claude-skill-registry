---
name: repository-analyzer
description: Analyzes codebases to generate comprehensive documentation including structure, languages, frameworks, dependencies, design patterns, and technical debt. Use when user says "analyze repository", "understand codebase", "document project", or when exploring unfamiliar code.
priority: MEDIUM
conflicts_with: [Task tool with Explore agent]
use_when:
  - User wants COMPREHENSIVE DOCUMENTATION (saved markdown file)
  - User wants to ONBOARD to unfamiliar project
  - User wants WRITTEN ANALYSIS to reference later
  - User says "document", "analyze repository", "generate docs"
avoid_when:
  - User wants to FIND specific code (use Explore agent)
  - User wants QUICK ANSWERS without documentation
  - User wants to SEARCH for patterns (use Grep)
---

# Repository Analyzer

## Purpose

Quickly understand unfamiliar codebases by automatically scanning structure, detecting technologies, mapping dependencies, and generating comprehensive documentation.

**For SDAM users**: Creates external documentation of codebase structure you can reference later.
**For ADHD users**: Instant overview without manual exploration - saves hours of context-switching.
**For all users**: Onboard to new projects in minutes instead of days.

## Activation Triggers

- User says: "analyze repository", "understand codebase", "document project"
- Requests for: "what's in this repo", "how does this work", "codebase overview"
- New project onboarding scenarios
- Technical debt assessment requests

## Core Workflow

### 1. Scan Repository Structure

**Step 1: Get directory structure**
```bash
# Use filesystem tools to map structure
tree -L 3 -I 'node_modules|.git|dist|build'
```

**Step 2: Count files by type**
```bash
# Identify languages used
find . -type f -name "*.js" | wc -l
find . -type f -name "*.py" | wc -l
find . -type f -name "*.go" | wc -l
# etc...
```

**Step 3: Measure codebase size**
```bash
# Count lines of code
cloc . --exclude-dir=node_modules,.git,dist,build
```

### 2. Detect Technologies

**Languages**: JavaScript, TypeScript, Python, Go, Rust, Java, etc.

**Frameworks**:
- **Frontend**: React, Vue, Angular, Svelte
- **Backend**: Express, FastAPI, Django, Rails
- **Mobile**: React Native, Flutter
- **Desktop**: Electron, Tauri

**Detection methods**:
```javascript
const detectFramework = async () => {
  // Check package.json
  const packageJson = await readFile('package.json');
  const dependencies = packageJson.dependencies || {};

  if ('react' in dependencies) return 'React';
  if ('vue' in dependencies) return 'Vue';
  if ('express' in dependencies) return 'Express';

  // Check requirements.txt
  const requirements = await readFile('requirements.txt');
  if (requirements.includes('fastapi')) return 'FastAPI';
  if (requirements.includes('django')) return 'Django';

  // Check go.mod
  const goMod = await readFile('go.mod');
  if (goMod.includes('gin-gonic')) return 'Gin';

  return 'Unknown';
};
```

### 3. Map Dependencies

**For Node.js**:
```bash
# Read package.json
cat package.json | jq '.dependencies'
cat package.json | jq '.devDependencies'

# Check for outdated packages
npm outdated
```

**For Python**:
```bash
# Read requirements.txt or pyproject.toml
cat requirements.txt

# Check for outdated packages
pip list --outdated
```

**For Go**:
```bash
# Read go.mod
cat go.mod

# Check for outdated modules
go list -u -m all
```

### 4. Identify Architecture Patterns

**Common patterns to detect**:

- **MVC** (Model-View-Controller): `models/`, `views/`, `controllers/`
- **Layered**: `api/`, `services/`, `repositories/`
- **Feature-based**: `features/auth/`, `features/users/`
- **Domain-driven**: `domain/`, `application/`, `infrastructure/`
- **Microservices**: Multiple services in `services/` directory
- **Monorepo**: Workspaces or packages structure

**Detection logic**:
```javascript
const detectArchitecture = (structure) => {
  if (structure.includes('models') && structure.includes('views') && structure.includes('controllers')) {
    return 'MVC Pattern';
  }
  if (structure.includes('features')) {
    return 'Feature-based Architecture';
  }
  if (structure.includes('domain') && structure.includes('application')) {
    return 'Domain-Driven Design';
  }
  if (structure.includes('services') && structure.includes('api-gateway')) {
    return 'Microservices Architecture';
  }
  return 'Custom Architecture';
};
```

### 5. Extract Technical Debt

**Search for indicators**:
```bash
# Find TODOs
grep -r "TODO" --include="*.js" --include="*.py" --include="*.go"

# Find FIXMEs
grep -r "FIXME" --include="*.js" --include="*.py" --include="*.go"

# Find HACKs
grep -r "HACK" --include="*.js" --include="*.py" --include="*.go"

# Find deprecated code
grep -r "@deprecated" --include="*.js" --include="*.ts"
```

**Complexity analysis**:
```javascript
// Identify long functions (potential refactor targets)
const analyzeFunctions = () => {
  // Functions > 50 lines = high complexity
  // Functions > 100 lines = very high complexity
  // Cyclomatic complexity > 10 = needs refactoring
};
```

### 6. Generate Documentation

**Output format**:
```markdown
# {Project Name} - Repository Analysis

**Generated:** {timestamp}
**Analyzed by:** Claude Code Repository Analyzer

---

## 📊 Overview

**Primary Language:** {language}
**Framework:** {framework}
**Architecture:** {architecture pattern}
**Total Files:** {count}
**Lines of Code:** {LOC}
**Last Updated:** {git log date}

---

## 📁 Directory Structure

```
project/
├── src/
│   ├── components/
│   ├── services/
│   └── utils/
├── tests/
└── docs/
```

---

## 🛠 Technologies

### Frontend
- React 18.2.0
- TypeScript 5.0
- Tailwind CSS 3.3

### Backend
- Node.js 18
- Express 4.18
- PostgreSQL 15

### DevOps
- Docker
- GitHub Actions
- Jest for testing

---

## 📦 Dependencies

### Production (12 packages)
- express: 4.18.2
- pg: 8.11.0
- jsonwebtoken: 9.0.0
- ...

### Development (8 packages)
- typescript: 5.0.4
- jest: 29.5.0
- eslint: 8.40.0
- ...

### ⚠️ Outdated (3 packages)
- express: 4.18.2 → 4.19.0 (minor update available)
- jest: 29.5.0 → 29.7.0 (patch updates available)

---

## 🏗 Architecture

**Pattern:** Layered Architecture

**Layers:**
1. **API Layer** (`src/api/`): REST endpoints, request validation
2. **Service Layer** (`src/services/`): Business logic
3. **Repository Layer** (`src/repositories/`): Database access
4. **Models** (`src/models/`): Data structures

**Data Flow:**
```
Client → API → Service → Repository → Database
```

---

## 🔍 Code Quality

**Metrics:**
- Average function length: 25 lines
- Cyclomatic complexity: 3.2 (low)
- Test coverage: 78%
- TypeScript strict mode: ✅ Enabled

**Strengths:**
- ✅ Well-structured codebase
- ✅ Good test coverage
- ✅ Type-safe with TypeScript

**Areas for Improvement:**
- ⚠️ 12 TODOs found (see Technical Debt section)
- ⚠️ 3 outdated dependencies
- ⚠️ Missing documentation in `/utils`

---

## 🐛 Technical Debt

### High Priority (3)
- **FIXME** in `src/services/auth.js:42`: JWT refresh token rotation not implemented
- **TODO** in `src/api/users.js:78`: Add rate limiting
- **HACK** in `src/utils/cache.js:23`: Using setTimeout instead of proper cache expiry

### Medium Priority (5)
- **TODO** in `src/components/Dashboard.jsx:15`: Optimize re-renders
- **TODO** in `tests/integration/api.test.js:100`: Add more edge cases
- ...

### Low Priority (4)
- **TODO** in `README.md:50`: Update installation instructions
- ...

---

## 🚀 Entry Points

**Main Application:**
- `src/index.js` - Server entry point
- `src/client/index.jsx` - Client entry point

**Development:**
- `npm run dev` - Start dev server
- `npm test` - Run tests
- `npm run build` - Production build

**Configuration:**
- `.env.example` - Environment variables
- `tsconfig.json` - TypeScript config
- `jest.config.js` - Test configuration

---

## 📋 Common Tasks

**Adding a new feature:**
1. Create component in `src/components/`
2. Add service logic in `src/services/`
3. Create API endpoint in `src/api/`
4. Write tests in `tests/`

**Database changes:**
1. Create migration in `migrations/`
2. Update models in `src/models/`
3. Run `npm run migrate`

---

## 🔗 Integration Points

**External Services:**
- PostgreSQL database (port 5432)
- Redis cache (port 6379)
- SendGrid API (email)
- Stripe API (payments)

**API Endpoints:**
- `GET /api/users` - List users
- `POST /api/auth/login` - Authentication
- `GET /api/dashboard` - Dashboard data

---

## 📚 Additional Resources

- [Architecture Diagram](./docs/architecture.png)
- [API Documentation](./docs/api.md)
- [Development Guide](./docs/development.md)

---

**Next Steps:**
1. Address high-priority technical debt
2. Update outdated dependencies
3. Increase test coverage to 85%+
4. Document utility functions
```

See [patterns.md](patterns.md) for architecture pattern library and [examples.md](examples.md) for analysis examples.

## Advanced Analysis Features

### Git History Analysis
```bash
# Find most changed files (hotspots)
git log --pretty=format: --name-only | sort | uniq -c | sort -rg | head -10

# Find largest contributors
git shortlog -sn

# Recent activity
git log --oneline --since="30 days ago" --no-merges
```

### Code Complexity Metrics
```bash
# Using complexity tools
npx eslint src/ --format json | jq '.[] | select(.messages[].ruleId == "complexity")'

# Or manual analysis
# Functions > 50 lines = candidate for refactoring
# Files > 500 lines = candidate for splitting
```

### Dependency Security
```bash
# Check for vulnerabilities
npm audit
pip-audit  # for Python
go mod tidy && go list -m all  # for Go
```

## Integration with Other Skills

### Context Manager
Save repository overview:
```
remember: Analyzed ProjectX repository
Type: CONTEXT
Tags: repository, architecture, nodejs, react
Content: ProjectX uses React + Express, layered architecture,
         12 high-priority TODOs, 78% test coverage
```

### Error Debugger
If analysis finds common issues:
```
Invoke error-debugger for:
- Deprecated dependencies
- Security vulnerabilities
- Common antipatterns detected
```

### Browser App Creator
Generate visualization:
```
Create dependency graph visualization
→ browser-app-creator generates interactive HTML chart
```

## Quality Checklist

Before delivering documentation, verify:
- ✅ Directory structure mapped
- ✅ Languages and frameworks identified
- ✅ Dependencies listed
- ✅ Architecture pattern detected
- ✅ Technical debt catalogued
- ✅ Entry points documented
- ✅ Common tasks explained
- ✅ Markdown formatted properly

## Output Delivery

**Format**: Markdown file saved to `~/.claude-artifacts/analysis-{project}-{timestamp}.md` (Linux/macOS) or `%USERPROFILE%\.claude-artifacts\analysis-{project}-{timestamp}.md` (Windows)

**Notify user**:
```
✅ **{Project Name} Analysis** complete!

**Summary:**
- {LOC} lines of code across {file_count} files
- Primary stack: {stack}
- Architecture: {pattern}
- {todo_count} TODOs found

**Documentation saved to:** {filepath}

**Key findings:**
1. {finding_1}
2. {finding_2}
3. {finding_3}

**Recommended actions:**
- {action_1}
- {action_2}
```

## Common Analysis Scenarios

### New Project Onboarding
User joins unfamiliar project → analyzer provides complete overview in minutes

### Technical Debt Assessment
User needs to evaluate legacy code → analyzer identifies all TODOs/FIXMEs/HACKs

### Dependency Audit
User wants to check outdated packages → analyzer lists all outdated dependencies with versions

### Architecture Documentation
User needs to document existing project → analyzer generates comprehensive architecture docs

## Success Criteria

✅ Complete codebase structure mapped
✅ All technologies identified correctly
✅ Dependencies catalogued with versions
✅ Architecture pattern detected
✅ Technical debt surfaced
✅ Documentation generated in <2 minutes
✅ Markdown output saved to artifacts
✅ Actionable recommendations provided

## Additional Resources

- **[Pattern Library](patterns.md)** - Common architecture patterns
- **[Analysis Examples](examples.md)** - Real-world repository analyses

## Quick Reference

### Trigger Phrases
- "analyze repository"
- "understand codebase"
- "document project"
- "what's in this repo"
- "codebase overview"
- "technical debt report"

### Output Location
- Linux/macOS: `~/.claude-artifacts/analysis-{project}-{timestamp}.md`
- Windows: `%USERPROFILE%\.claude-artifacts\analysis-{project}-{timestamp}.md`

### Analysis Depth Options
- **Quick** (<1 min): Structure + languages only
- **Standard** (1-2 min): + dependencies + patterns
- **Deep** (3-5 min): + git history + complexity metrics + security audit
