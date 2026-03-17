---
name: exploration
description: Codebase exploration techniques for rapid discovery, architecture analysis, pattern detection, and dependency mapping.
argument-hint: "[directory] [--thorough]"
context: fork
agent: fuse-ai-pilot:explore-codebase
user-invocable: false
---

**Session:** ${CLAUDE_SESSION_ID}

# Exploration Skill

## Exploration Protocol

### Phase 1: Initial Reconnaissance

```bash
# List root files
ls -la

# Find config files
find . -maxdepth 2 -name "package.json" -o -name "*.config.*" -o -name "pyproject.toml" -o -name "go.mod" -o -name "Cargo.toml" 2>/dev/null

# Check for common entry points
ls -la src/ app/ lib/ cmd/ 2>/dev/null
```

### Phase 2: Structure Mapping

```bash
# Tree view (excluding common noise)
tree -L 3 -I 'node_modules|dist|build|.git|__pycache__|.next|target|vendor' 2>/dev/null || find . -type d -maxdepth 3 | head -50

# Identify main directories
ls -la src/ lib/ app/ internal/ pkg/ 2>/dev/null
```

### Phase 3: Entry Points Detection

```bash
# JavaScript/TypeScript
grep -rn "main\|index\|app.listen\|createServer\|export default" --include="*.{js,ts,jsx,tsx}" | head -20

# Python
grep -rn "if __name__\|main()\|app.run\|uvicorn" --include="*.py" | head -20

# Go
grep -rn "func main\|http.ListenAndServe" --include="*.go" | head -20

# Rust
grep -rn "fn main" --include="*.rs" | head -10
```

### Phase 4: Dependency Analysis

```bash
# Node.js
cat package.json 2>/dev/null | head -50

# Python
cat pyproject.toml requirements.txt setup.py 2>/dev/null | head -50

# Go
cat go.mod 2>/dev/null

# Rust
cat Cargo.toml 2>/dev/null | head -50

# PHP
cat composer.json 2>/dev/null | head -50
```

### Phase 5: Pattern Detection

**Search for architectural patterns**:

```bash
# MVC patterns
ls -la controllers/ models/ views/ routes/ 2>/dev/null

# Clean/Hexagonal Architecture
ls -la domain/ application/ infrastructure/ interfaces/ adapters/ ports/ 2>/dev/null

# Feature-based
ls -la features/ modules/ 2>/dev/null

# Next.js App Router
ls -la app/ pages/ components/ 2>/dev/null
```

---

## Architecture Pattern Detection

### Pattern Indicators

| Pattern | Key Directories | Indicators |
|---------|-----------------|------------|
| **MVC** | `controllers/`, `models/`, `views/` | Rails, Laravel, Express |
| **Clean Architecture** | `domain/`, `application/`, `infrastructure/` | DDD, Use cases |
| **Hexagonal** | `adapters/`, `ports/`, `core/` | Ports & adapters |
| **Feature-based** | `features/[name]/` | All layers per feature |
| **Layered** | `presentation/`, `business/`, `data/` | Traditional 3-tier |
| **Monolith** | Single `src/` | Mixed concerns |
| **Microservices** | Multiple `services/` | Separate repos/folders |
| **Next.js App Router** | `app/`, `components/`, `lib/` | Server/Client components |
| **Modular Monolith** | `modules/[name]/` | Bounded contexts |

---

## Tech Stack Detection

### JavaScript/TypeScript

| File | Technology |
|------|------------|
| `package.json` | Dependencies, scripts |
| `tsconfig.json` | TypeScript config |
| `next.config.*` | Next.js |
| `vite.config.*` | Vite |
| `webpack.config.*` | Webpack |
| `tailwind.config.*` | Tailwind CSS |
| `.eslintrc.*` | ESLint |
| `prisma/schema.prisma` | Prisma ORM |

**Detection commands**:
```bash
# Framework detection
grep -l "next\|react\|vue\|angular\|svelte" package.json 2>/dev/null

# Database/ORM
ls prisma/ drizzle/ migrations/ 2>/dev/null

# State management
grep -E "zustand|redux|@reduxjs|jotai|recoil" package.json 2>/dev/null
```

### Python

| File | Technology |
|------|------------|
| `pyproject.toml` | Modern Python project |
| `requirements.txt` | Dependencies |
| `setup.py` | Package setup |
| `manage.py` | Django |
| `alembic.ini` | Database migrations |

**Detection commands**:
```bash
# Framework detection
grep -E "django|flask|fastapi|starlette" pyproject.toml requirements.txt 2>/dev/null

# ORM
grep -E "sqlalchemy|django|tortoise|peewee" pyproject.toml requirements.txt 2>/dev/null
```

### Go

| File | Technology |
|------|------------|
| `go.mod` | Module definition |
| `go.sum` | Dependencies lock |
| `cmd/` | Entry points |
| `internal/` | Private packages |
| `pkg/` | Public packages |

**Detection commands**:
```bash
# Framework detection
grep -E "gin|echo|fiber|chi|gorilla" go.mod 2>/dev/null

# Database
grep -E "gorm|sqlx|ent|pgx" go.mod 2>/dev/null
```

### PHP

| File | Technology |
|------|------------|
| `composer.json` | Dependencies |
| `artisan` | Laravel |
| `bin/console` | Symfony |

### Rust

| File | Technology |
|------|------------|
| `Cargo.toml` | Dependencies |
| `src/lib.rs` | Library crate |
| `src/main.rs` | Binary crate |

---

## Code Organization Assessment

### Check Interface Separation

```bash
# TypeScript/JavaScript
ls -la src/interfaces/ src/types/ types/ 2>/dev/null

# Check for interfaces in components (violation)
grep -r "interface.*Props\|type.*Props" --include="*.tsx" src/components/ 2>/dev/null | head -10
```

### Check Business Logic Location

```bash
# Hooks for business logic
ls -la src/hooks/ hooks/ 2>/dev/null

# Check for logic in components (violation)
grep -rn "useState\|useEffect\|async" --include="*.tsx" src/components/ 2>/dev/null | wc -l
```

### Check State Management

```bash
# Store files
ls -la src/stores/ stores/ src/store/ 2>/dev/null

# Store usage
grep -r "useStore\|useSelector\|create(" --include="*.{ts,tsx}" src/ 2>/dev/null | head -10
```

---

## Response Format

```markdown
## 🗺️ Codebase Exploration: [Project Name]

### Structure Overview
- **Type**: Monolith / Microservices / Library / Monorepo
- **Tech Stack**: [Languages], [Frameworks], [Tools]
- **Architecture**: [Pattern detected]
- **Entry Points**: [Main files]

### Key Directories
```
src/
├── [dir1]/    # [Purpose]
├── [dir2]/    # [Purpose]
└── [dir3]/    # [Purpose]
```

### Dependencies
- **Runtime**: [Key dependencies]
- **Dev**: [Build tools, linters]
- **Database**: [ORM, driver]

### Architecture Patterns
- [Pattern 1]: [Evidence]
- [Pattern 2]: [Evidence]

### Code Organization
- **Interfaces**: [Location or ❌ mixed with components]
- **Business Logic**: [Location or ❌ in components]
- **State**: [Store location or ❌ prop drilling]
- **File Sizes**: [Compliant or ❌ violations found]

### Potential Issues
- ⚠️ [Issue 1]
- ⚠️ [Issue 2]

### Recommendations
- 💡 [Suggestion 1]
- 💡 [Suggestion 2]
```

---

## Quick Analysis Commands

### Full Stack Assessment

```bash
# One-liner for quick assessment
echo "=== Package Manager ===" && ls package.json pyproject.toml go.mod Cargo.toml composer.json 2>/dev/null && echo "=== Framework ===" && head -20 package.json 2>/dev/null | grep -E "next|react|vue|express" && echo "=== Structure ===" && ls -la src/ app/ lib/ 2>/dev/null
```

### File Count by Type

```bash
# Count files by extension
find . -type f -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" 2>/dev/null | wc -l
find . -type f -name "*.py" 2>/dev/null | wc -l
find . -type f -name "*.go" 2>/dev/null | wc -l
```

### Large Files Detection

```bash
# Find files > 100 lines (potential violations)
find . -name "*.ts" -o -name "*.tsx" -o -name "*.py" 2>/dev/null | xargs wc -l 2>/dev/null | sort -rn | head -20
```

---

## Forbidden Behaviors

- ❌ Make assumptions without code evidence
- ❌ Ignore configuration files
- ❌ Overlook test directories
- ❌ Skip dependency analysis
- ❌ Miss entry points
- ❌ Assume architecture without verification

## Behavioral Traits

- Systematic and methodical
- Pattern-focused detection
- Context-aware analysis
- Comprehensive yet concise
- Evidence-based insights
- Quick reconnaissance before deep dive
