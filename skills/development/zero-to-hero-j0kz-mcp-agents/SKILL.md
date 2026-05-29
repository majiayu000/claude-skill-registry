---
name: zero-to-hero
version: 1.0.0
type: onboarding
tags: [onboarding, codebase, exploration, learning, documentation]
compatibility: any-project
dependencies: optional
language: any
description: Go from zero knowledge to codebase expert in ANY project, ANY size, ANY language
---

# Zero to Hero - Master Any Codebase Fast

## 🎯 When to Use This Skill

Use when you need to:
- Join a new project/team
- Contribute to open source
- Debug unfamiliar code
- Review a codebase for acquisition
- Take over maintenance of a project
- Understand how a library works internally

## ⚡ The 15-Minute Quick Start

### WITH MCP Tools:
```
"Give me a complete overview of this codebase"
"Show me the architecture and main components"
```

### WITHOUT MCP - The Speed Run:

```bash
# 1. Size and scope (30 seconds)
find . -type f -name "*.js" -o -name "*.py" -o -name "*.java" | wc -l
du -sh .

# 2. Main technologies (30 seconds)
ls package.json pom.xml requirements.txt go.mod Gemfile Cargo.toml 2>/dev/null

# 3. Entry points (1 minute)
find . -name "main.*" -o -name "index.*" -o -name "app.*" | head -10

# 4. Project structure (1 minute)
tree -L 2 -d -I 'node_modules|vendor|target|dist|build'

# 5. Recent activity (30 seconds)
git log --oneline -10

# 6. Documentation (1 minute)
ls README* readme* docs/ doc/ 2>/dev/null

# 7. Tests (30 seconds)
find . -name "*test*" -o -name "*spec*" | head -5

# 8. Configuration (30 seconds)
ls .*rc .env* config/ conf/ 2>/dev/null
```

## 📚 Level 1: RECONNAISSANCE (30 minutes)

### 1. Understand the Purpose

**Read Documentation:**
```bash
# Check for docs
cat README.md | head -50
cat CONTRIBUTING.md
cat docs/getting-started.md

# No docs? Check code comments
grep -r "TODO\|FIXME\|NOTE" --include="*.js" | head -20
```

**Understand the Domain:**
```bash
# What does this project do?
# Look for domain-specific terms
grep -r "class\|interface\|struct" --include="*.java" | cut -d: -f2 | grep -o '[A-Z][a-zA-Z]*' | sort | uniq -c | sort -rn | head -20

# Find business logic keywords
grep -roh '\b[A-Z][a-z]+[A-Z][a-zA-Z]*\b' --include="*.py" | sort | uniq -c | sort -rn | head -20
```

### 2. Map the Architecture

**Identify Layers:**
```bash
# Common architectural patterns
ls -la | grep -E "controller|service|model|view|repository|handler|router|middleware"

# MVC Pattern?
find . -type d -name "*controller*" -o -name "*model*" -o -name "*view*"

# Microservices?
find . -type f -name "Dockerfile" -o -name "docker-compose*"

# Monolith?
find . -name "pom.xml" -o -name "build.gradle"
```

**Trace Data Flow:**
```javascript
// Add strategic console.logs to trace execution
console.trace('🔍 TRACE:');  // Shows call stack

// Or use debugger
debugger;  // Breakpoint when dev tools open
```

### 3. Find the Core

**The 80/20 Rule - Find the 20% that matters:**
```bash
# Most modified files (probably important)
git log --pretty=format: --name-only | sort | uniq -c | sort -rn | head -10

# Largest files (often core logic)
find . -type f -name "*.js" -exec wc -l {} + | sort -rn | head -10

# Most imported/required modules
grep -r "import\|require" --include="*.js" | cut -d'"' -f2 | sort | uniq -c | sort -rn | head -10
```

## 🔍 Level 2: EXPLORATION (2 hours)

### 1. Run the Project

**Setup Checklist:**
```bash
# 1. Install dependencies
npm install    # Node.js
pip install -r requirements.txt  # Python
bundle install  # Ruby
go mod download  # Go

# 2. Setup database
cp .env.example .env  # Configure
npm run db:migrate   # Run migrations

# 3. Start development
npm run dev
# or
python manage.py runserver
# or
./gradlew bootRun
```

**Make it Work:**
```bash
# Common issues and fixes:

# Port already in use
lsof -i :3000
kill -9 <PID>

# Missing dependencies
npm ci  # Clean install

# Database connection
psql -h localhost -U postgres  # Test connection

# Environment variables
export $(cat .env | xargs)  # Load .env file
```

### 2. Follow User Journeys

**Pick One Feature and Trace It:**
```markdown
## User Login Flow Trace

1. **Frontend**: Login form submission
   - File: `src/components/LoginForm.jsx`
   - Action: POST /api/auth/login

2. **Backend**: Authentication endpoint
   - File: `server/routes/auth.js`
   - Handler: `authController.login()`

3. **Business Logic**: Validate credentials
   - File: `server/services/authService.js`
   - Method: `validateUser()`

4. **Database**: Check user exists
   - File: `server/models/User.js`
   - Query: `findByEmail()`

5. **Response**: Return JWT token
   - File: `server/utils/jwt.js`
   - Method: `generateToken()`
```

### 3. Understand Patterns

**Identify Coding Patterns:**
```javascript
// Common patterns to look for:

// 1. Dependency Injection
constructor(userService, logger) {
  this.userService = userService;
  this.logger = logger;
}

// 2. Factory Pattern
class UserFactory {
  static create(type) {
    // ...
  }
}

// 3. Singleton
class Database {
  static instance;
  static getInstance() {
    if (!this.instance) {
      this.instance = new Database();
    }
    return this.instance;
  }
}

// 4. Observer/EventEmitter
emitter.on('user:login', handleLogin);
```

## 🚀 Level 3: CONTRIBUTION (First PR)

### 1. Find Easy Wins

```bash
# Good first issues
grep -r "TODO" --include="*.js" | grep -i "easy\|simple\|trivial"

# Typos in comments
grep -r "teh\|recieve\|occured" --include="*.md"

# Missing tests
find . -name "*.js" ! -name "*.test.js" ! -name "*.spec.js" | while read f; do
  test_file="${f%.js}.test.js"
  if [ ! -f "$test_file" ]; then
    echo "Missing test: $f"
  fi
done

# Documentation gaps
grep -r "function\|class" --include="*.js" | grep -v "//" | grep -v "/\*"
```

### 2. Make Safe Changes

**Start with Non-Breaking Changes:**
- Add tests for untested code
- Improve error messages
- Add logging/monitoring
- Update documentation
- Fix linter warnings
- Refactor test code (safer than production)

### 3. Learn Team Conventions

```bash
# Coding style
cat .eslintrc .prettierrc

# Commit conventions
git log --oneline | head -20  # See patterns

# PR process
cat .github/pull_request_template.md

# CI/CD pipeline
cat .github/workflows/*.yml
cat .gitlab-ci.yml
cat Jenkinsfile
```

## 📊 Codebase Analysis Template

```markdown
# Codebase Analysis: [Project Name]

## Overview
- **Purpose**: [What does it do?]
- **Language**: [Primary languages]
- **Framework**: [Main frameworks]
- **Size**: [LOC, number of files]
- **Age**: [First commit date]
- **Activity**: [Commits per month]

## Architecture
- **Pattern**: [MVC, Microservices, etc.]
- **Database**: [Type and version]
- **External Services**: [APIs, queues, etc.]

## Key Components
1. **[Component Name]**: [Purpose]
   - Location: `path/to/component`
   - Responsibility: [What it does]

## Entry Points
- Main: `src/index.js`
- API: `server/app.js`
- CLI: `bin/cli.js`

## Data Flow
1. User request → Router
2. Router → Controller
3. Controller → Service
4. Service → Database
5. Response → User

## Testing
- Framework: [Jest, Pytest, etc.]
- Coverage: [Percentage]
- CI/CD: [Platform]

## Quick Start
\`\`\`bash
npm install
npm run dev
\`\`\`

## Key Files to Understand
1. `src/core/App.js` - Application entry
2. `config/database.js` - DB configuration
3. `routes/index.js` - API routes

## Gotchas
- [Common issues and solutions]

## Team Conventions
- Style: [Linter configuration]
- Commits: [Convention used]
- PRs: [Review process]
```

## 💡 Pro Tips for Fast Learning

### The "Teach It" Method:
```markdown
After 1 hour of exploration, explain the codebase as if teaching someone:
1. What problem does it solve?
2. How is it organized?
3. What are the main components?
4. How do they interact?
5. What would you change?
```

### The "Break and Fix" Method:
```javascript
// Intentionally break something
throw new Error('LEARNING: What calls this?');

// See what breaks, understand dependencies
// Remember to git reset after!
```

### The "Question List" Method:
```markdown
## Questions to Answer:
- [ ] How does authentication work?
- [ ] Where is business logic?
- [ ] How is data validated?
- [ ] What can be configured?
- [ ] How are errors handled?
- [ ] Where are the tests?
- [ ] How is it deployed?
```

## 🎯 Success Metrics

You understand the codebase when you can:
- ✅ Run it locally without help
- ✅ Add a simple feature
- ✅ Fix a bug independently
- ✅ Explain the architecture to someone
- ✅ Review PRs meaningfully
- ✅ Suggest improvements
- ✅ Debug production issues

## 🚨 Common Pitfalls

### Don't:
- ❌ Refactor before understanding
- ❌ Judge code quality too quickly
- ❌ Ignore existing patterns
- ❌ Skip reading tests
- ❌ Assume anything - verify!

### Do:
- ✅ Ask questions early
- ✅ Document as you learn
- ✅ Respect existing conventions
- ✅ Read commit history for context
- ✅ Start with small changes

Remember: Every expert was once a beginner. The codebase that seems complex today will feel natural tomorrow! 🚀