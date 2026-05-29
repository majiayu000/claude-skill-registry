---
name: code-standards-analyzer
description: Generate and maintain coding standards documentation from existing codebase patterns. Use when creating STANDARDS.md files, onboarding new developers, or documenting team conventions. Evidence-based approach - standards reflect reality, not aspirations.
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
---

# Code Standards Analyzer

**Purpose**: Discover, document, and maintain coding standards from existing codebases using evidence-based analysis.

**Philosophy**: Standards should reflect REALITY (what the code actually does) not ASPIRATIONS (what we wish it did). Measure, then document.

---

## When to Use

### Primary Use Cases:
1. **Brownfield Onboarding** - "What are this project's coding conventions?"
2. **Standards Audit** - "Are we following our declared standards?"
3. **New Contributor Onboarding** - "Teach me the project patterns"
4. **Living Documentation** - "Keep standards in sync with codebase"
5. **Greenfield Setup** - "Initialize standards from best practices"

### Activation Triggers

**Keywords**: analyze coding standards, discover conventions, code style, detect patterns, coding guidelines, what are the standards, naming conventions, best practices, code quality, standards audit, anti-patterns

**User Requests**:
- "What are the coding standards for this project?"
- "Analyze the codebase and document our conventions"
- "Check if we're following our declared standards"
- "Find anti-patterns in the code"
- "Generate coding standards documentation"
- "What naming conventions does this project use?"

---

## Capabilities

### 1. **Explicit Standards Discovery** (Fast - 5 seconds)
- ✅ Detect existing `.specweave/docs/internal/governance/coding-standards.md`
- ✅ Parse ESLint configuration (`.eslintrc.json`, `.eslintrc.js`)
- ✅ Parse Prettier configuration (`.prettierrc`, `.prettierrc.json`)
- ✅ Parse TypeScript configuration (`tsconfig.json`)
- ✅ Parse EditorConfig (`.editorconfig`)
- ✅ Extract standards from `CLAUDE.md`, `CONTRIBUTING.md`

### 2. **Implicit Standards Detection** (Medium - 30 seconds)
- ✅ Naming convention analysis (variables, functions, classes, constants)
- ✅ Import pattern detection (extensions, ordering, aliasing)
- ✅ Function characteristics (avg length, max length, arrow vs regular)
- ✅ Type safety analysis (`any` usage, interface vs type preference)
- ✅ Error handling patterns (try/catch usage, custom errors)
- ✅ Comment style analysis
- ✅ File organization patterns

### 3. **Anti-Pattern Detection** (Fast - 15 seconds)
- 🚨 `console.*` usage in production code
- 🚨 Hardcoded secrets (API keys, passwords)
- 🚨 `any` type overuse
- 🚨 Large files (>500 lines)
- 🚨 Long functions (>100 lines)
- 🚨 Missing error handling
- 🚨 N+1 query patterns
- 🚨 Security vulnerabilities

### 4. **Documentation Generation** (Fast - 10 seconds)
- ✅ Generate standards document with examples
- ✅ Include statistical confidence levels
- ✅ Extract real code examples from codebase
- ✅ Highlight inconsistencies and conflicts
- ✅ Provide actionable recommendations
- ✅ Link to violating files

---

## Analysis Process

### Phase 1: Explicit Standards (5 seconds)

**Sources Checked**:
1. `.specweave/docs/internal/governance/coding-standards.md` (HIGH confidence)
2. `CLAUDE.md` (HIGH confidence - AI instructions)
3. `.eslintrc.json` (ENFORCED by tooling)
4. `.prettierrc` (ENFORCED by tooling)
5. `tsconfig.json` (ENFORCED by compiler)
6. `.editorconfig` (ENFORCED by editor)
7. `CONTRIBUTING.md` (MEDIUM confidence - may be outdated)

**Output**:
```markdown
## Explicit Standards Found

✅ .eslintrc.json (ENFORCED - ESLint active)
✅ .prettierrc (ENFORCED - Prettier active)
✅ tsconfig.json (ENFORCED - TypeScript compiler)
✅ CLAUDE.md (HIGH - AI development rules)
⚠️  CONTRIBUTING.md (MEDIUM - human guidelines)
❌ No .specweave/docs/internal/governance/coding-standards.md
```

### Phase 2: Implicit Standards (30 seconds)

**Analysis Performed**:
- Scan `src/**/*.{ts,js,tsx,jsx}` files
- Parse Abstract Syntax Trees (AST)
- Calculate statistical patterns
- Identify dominant conventions

**Example Output**:
```markdown
## Detected Patterns

### Naming Conventions (Confidence: 95%)
- Variables: camelCase (1,234 samples, 98% compliance)
- Functions: camelCase (567 samples, 100% compliance)
- Classes: PascalCase (89 samples, 100% compliance)
- Constants: UPPER_SNAKE_CASE (234 samples, 92% compliance)
  ⚠️ 8% use camelCase (inconsistency detected)

### Import Patterns (Confidence: 100%)
- Extensions: .js suffix required (100% compliance)
- Order: external → internal → types (87% compliance)

### Function Characteristics
- Average length: 35 lines
- Max length: 156 lines (src/core/analyzer.ts:45)
- Style: Arrow functions (78%), Regular (22%)

### Type Safety (Confidence: 85%)
- any usage: 12 instances (REVIEW NEEDED)
- Preference: Interfaces (89%) over Types (11%)
```

### Phase 3: Anti-Pattern Detection (15 seconds)

**Checks Performed**:
- Security: Hardcoded secrets, SQL injection risks
- Maintainability: Large files, complex functions
- Performance: N+1 queries, missing caching
- Robustness: Missing error handling

**Example Output**:
```markdown
## Issues Found

### 🔴 CRITICAL (2 issues)
- Hardcoded Secrets: 2 instances
  - src/config/api.ts:12
  - src/utils/auth.ts:45
  Fix: Use process.env variables

### 🟠 HIGH (5 issues)
- console.* Usage: 5 instances in src/
  - src/core/analyzer.ts:67
  Fix: Use logger abstraction

### 🟡 MEDIUM (12 issues)
- Large Files: 3 files > 500 lines
  - src/core/orchestrator.ts (678 lines)
  Fix: Split into modules
```

### Phase 4: Documentation Generation (10 seconds)

**Merge Strategy**:
1. Explicit standards = source of truth
2. Implicit standards = fill gaps
3. Anti-patterns = warnings + recommendations

**Output**: `.specweave/docs/internal/governance/coding-standards-analysis.md`

---

## Integration Points

### 1. Brownfield Analyzer Integration

**Automatic**: Runs as part of brownfield analysis

```
User: "Analyze this brownfield project"

Workflow:
1. Scan project structure
2. Classify documents
3. Detect external tools
4. → RUN code-standards-detective agent
5. → GENERATE coding-standards.md
6. Generate migration plan
```

### 2. Increment Planning

**Reference**: Standards included in technical constraints

```markdown
## Technical Constraints

Coding Standards: .specweave/docs/internal/governance/coding-standards.md
- Naming: camelCase (vars), PascalCase (classes)
- Functions: < 50 lines target
- No console.* - use logger
```

### 3. Increment Completion

**Optional**: Re-analyze on increment done

```bash
/sw:done 0046 --update-standards
```

---

## Usage Examples

### Example 1: First-Time Analysis

```
User: "What are the coding standards for this project?"

Skill: code-standards-analyzer

Actions:
1. Check for existing standards (none found)
2. Parse .eslintrc.json, .prettierrc
3. Analyze 1,234 TypeScript files
4. Detect patterns with 95% confidence
5. Generate standards document

Output:
"✅ Analysis complete! Generated coding standards at:
.specweave/docs/internal/governance/coding-standards-analysis.md

Key findings:
- Naming: 98% camelCase compliance
- Imports: 100% use .js extensions
- Issues: 5 console.* usages, 2 hardcoded secrets
- Recommendation: Formalize detected patterns as official standards"
```

### Example 2: Standards Audit

```
User: "Check if we're following our declared standards"

Skill: code-standards-analyzer

Actions:
1. Read existing coding-standards.md
2. Analyze current codebase
3. Compare declared vs actual
4. Report violations

Output:
"📊 Standards Compliance: 87%

✅ Passing:
- Naming conventions: 98% compliant
- Import patterns: 100% compliant

⚠️ Violations:
- console.* usage: 12 instances (should be 0)
- Large files: 3 files > 500 lines (should be 0)

Recommendation: Fix violations or update standards to reflect reality"
```

### Example 3: New Contributor Onboarding

```
User: "I'm new to this codebase. What conventions should I follow?"

Skill: code-standards-analyzer

Actions:
1. Load existing coding-standards.md
2. Extract key rules with examples
3. Highlight SpecWeave-specific patterns

Output:
"📚 Coding Standards Summary

1. Naming:
   - Variables: camelCase (e.g., `userId`, `isActive`)
   - Functions: camelCase (e.g., `getUserById()`)
   - Classes: PascalCase (e.g., `UserService`)

2. Imports:
   - Always use .js extensions
   - Example: import { foo } from './bar.js'

3. Error Handling:
   - Use custom error types
   - Example: throw new UserNotFoundError(id)

4. Logging:
   - NEVER use console.*
   - Use logger abstraction instead

Full standards: .specweave/docs/internal/governance/coding-standards.md"
```

---

## Commands

### Manual Analysis

```bash
# Full analysis
/sw:analyze-standards

# Drift detection only
/sw:analyze-standards --drift

# Update existing standards
/sw:analyze-standards --update
```

---

## Output Files

### 1. `coding-standards-analysis.md` (Auto-Generated)

**Location**: `.specweave/docs/internal/governance/coding-standards-analysis.md`

**Purpose**: Latest analysis report (gitignored, temporary)

**Contents**:
- Detected patterns with confidence levels
- Real code examples
- Statistical evidence
- Violation warnings
- Recommendations

### 2. `coding-standards.md` (Source of Truth)

**Location**: `.specweave/docs/internal/governance/coding-standards.md`

**Purpose**: Official coding standards (git-tracked, manual + auto)

**Contents**:
- Naming conventions
- Import patterns
- Function guidelines
- Type safety rules
- Error handling
- Security practices
- Performance guidelines

### 3. `coding-standards-history.md` (Change Log)

**Location**: `.specweave/docs/internal/governance/coding-standards-history.md`

**Purpose**: Track standard evolution over time

**Contents**:
- Timestamp of each analysis
- Changes detected
- Migration guides
- Rationale for updates

---

## Best Practices

### 1. Run During Onboarding
- Analyze standards as part of brownfield analysis
- Generate baseline documentation
- Establish project context

### 2. Periodic Re-Analysis
- Quarterly reviews
- After major refactors
- On team onboarding

### 3. Team Review Required
- Don't auto-commit changes
- Review generated standards
- Discuss inconsistencies
- Formalize decisions

### 4. Living Documentation
- Keep standards in sync with code
- Update when patterns change
- Track evolution in history

### 5. Enforcement Through Tooling
- Most standards → ESLint/Prettier
- This skill → document what tools can't catch
- Focus on SpecWeave-specific patterns

---

## Related Documentation

- [Coding Standards](.specweave/docs/internal/governance/coding-standards.md) - Official standards
- [Code Review Standards](.specweave/docs/internal/delivery/core/code-review-standards.md) - Review process
- [Brownfield Analyzer](../brownfield-analyzer/SKILL.md) - Project analysis

---

## Technical Details

### Supported Languages
- ✅ TypeScript (primary)
- ✅ JavaScript (ES6+)
- ✅ Python (pyproject.toml, .pylintrc, ruff.toml, .flake8, mypy.ini)
- ✅ Java/Kotlin (checkstyle.xml, pmd.xml, spotbugs.xml, detekt.yml)
- ✅ Go (go.mod, .golangci.yml, staticcheck.conf)
- ✅ C#/.NET (.editorconfig, StyleCop.json, Directory.Build.props)
- ✅ Rust (rustfmt.toml, clippy.toml, Cargo.toml)
- ✅ React (package.json, ESLint plugin:react/*)
- ✅ Angular (angular.json, ESLint @angular-eslint)
- ✅ Vue (package.json, ESLint plugin:vue/*)
- ✅ Svelte (package.json, svelte.config.js)

### Detection Algorithms

**Naming Convention Detection**:
- Regex pattern matching
- Statistical frequency analysis
- AST node analysis
- Confidence scoring (samples / total)

**Anti-Pattern Detection**:
- Static analysis (grep, AST parsing)
- Rule-based checks
- Security scanning
- Complexity metrics

**Confidence Levels**:
- ENFORCED: Linter/compiler enforced (100%)
- HIGH: 90%+ compliance in codebase
- MEDIUM: 70-89% compliance
- LOW: 50-69% compliance
- CONFLICT: <50% compliance (inconsistent)

---

## Limitations

1. **Implicit Standards**: Requires representative codebase sample
2. **False Positives**: Anti-pattern detection may flag intentional code
3. **Context**: Can't understand business rationale for patterns

---

## Multi-Technology Support

**Status**: ✅ Implemented (increment 0122-multi-technology-governance)

| Technology | Config Files | Status |
|------------|--------------|--------|
| TypeScript/JavaScript | `.eslintrc.*`, `.prettierrc`, `tsconfig.json` | ✅ Implemented |
| Python | `pyproject.toml`, `.pylintrc`, `ruff.toml`, `.flake8`, `mypy.ini` | ✅ Implemented |
| Go | `go.mod`, `.golangci.yml`, `staticcheck.conf` | ✅ Implemented |
| Java/Kotlin | `checkstyle.xml`, `pmd.xml`, `spotbugs.xml`, `detekt.yml` | ✅ Implemented |
| C#/.NET | `.editorconfig`, `StyleCop.json`, `Directory.Build.props` | ✅ Implemented |
| Rust | `rustfmt.toml`, `clippy.toml`, `Cargo.toml` | ✅ Implemented |
| React | ESLint + `plugin:react/*`, `package.json` | ✅ Implemented |
| Angular | `angular.json`, `.eslintrc` | ✅ Implemented |
| Vue | ESLint + `plugin:vue/*`, `vite.config.*` | ✅ Implemented |
| Svelte | `svelte.config.js`, `package.json` | ✅ Implemented |

**Output Structure:**
```
.specweave/docs/internal/governance/
├── coding-standards.md          # Unified summary of ALL technologies
├── shared-conventions.md        # EditorConfig, Git conventions
└── standards/
    ├── typescript.md
    ├── python.md
    ├── golang.md
    ├── java.md
    ├── react.md
    ├── angular.md
    ├── vue.md
    └── svelte.md
```

**Usage**:
```typescript
import {
  detectEcosystems,
  parsePythonStandards,
  parseGoStandards,
  parseJavaStandards,
  parseFrontendStandards,
  generateStandardsMarkdown,
  generateUnifiedSummary
} from 'src/core/living-docs/governance/index.js';
```

---

## Future Enhancements

- [ ] Auto-generate ESLint rules from detected patterns
- [ ] AI-powered suggestions from top OSS projects
- [ ] Team-specific standards in multi-project mode
- [ ] Pre-commit hook integration for enforcement
- [ ] Real-time drift alerts
- [ ] Standards comparison across projects

## Project-Specific Learnings

**Before starting work, check for project-specific learnings:**

```bash
# Check if skill memory exists for this skill
cat .specweave/skill-memories/code-standards-analyzer.md 2>/dev/null || echo "No project learnings yet"
```

Project learnings are automatically captured by the reflection system when corrections or patterns are identified during development. These learnings help you understand project-specific conventions and past decisions.
