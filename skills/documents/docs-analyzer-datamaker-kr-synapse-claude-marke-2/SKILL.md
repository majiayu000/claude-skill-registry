---
name: docs-analyzer
description: Analyzes code changes and identifies documentation gaps. Scans git history, catalogs existing docs, and generates comprehensive analysis reports.
allowed-tools: Read, Grep, Glob, Bash
user-invocable: true
---

# Documentation Analyzer Skill

## Purpose

This skill specializes in analyzing codebases to identify documentation gaps and assess the impact of code changes on existing documentation. It provides structured reports to guide documentation updates.

## When to Activate

Use this skill when:
- Starting documentation review for a project
- Analyzing impact of recent code changes
- Auditing documentation completeness
- Preparing for documentation updates
- User requests documentation analysis

## Core Workflow

### Step 1: Catalog Existing Documentation

Scan and catalog all documentation files in the repository:

**Documentation Files to Find**:
- `README.md` (root and subdirectories)
- `docs/` directory contents
- `CONTRIBUTING.md`
- `CHANGELOG.md`
- `*.md` files throughout the codebase
- API documentation (OpenAPI/Swagger specs)
- Architecture diagrams and documentation

**Use Glob and Read tools**:
```bash
# Find all markdown files
Glob: "**/*.md"

# Find documentation directories
Glob: "**/docs/**/*"

# Find API specs
Glob: "**/*.{yaml,yml,json}" (for OpenAPI specs)
```

**Catalog Output**:
- List of all documentation files found
- Brief description of each file's purpose
- Last modified date (from git)
- Current state assessment (complete, outdated, missing sections)

### Step 2: Analyze Git History

Use Bash tool to analyze recent code changes and identify affected components.

**Git Commands to Run**:
```bash
# Get recent commits (last 10-50 depending on activity)
git log --oneline -20

# Get detailed diff for recent changes
git diff HEAD~10..HEAD --stat

# Identify changed files by type
git diff HEAD~10..HEAD --name-only

# Get commit messages for context
git log HEAD~10..HEAD --pretty=format:"%h - %s"
```

**Analyze**:
- Files modified (by extension and directory)
- Commit messages (feature, fix, refactor indicators)
- Areas of codebase affected (frontend, backend, infrastructure, etc.)

### Step 3: Identify Affected Components

Based on file changes, determine which components were modified:

**Backend Projects** (Django, FastAPI, Express, etc.):
- API endpoints (routes, views, controllers)
- Data models (ORM models, schemas)
- Database migrations
- Background tasks
- Services and business logic
- Authentication/authorization
- Middleware

**Frontend Projects** (React, Vue, Angular, etc.):
- Components
- State management
- Routing
- API integrations
- UI/styling
- Build configuration

**Infrastructure** (Terraform, Kubernetes, etc.):
- Resource definitions
- Configuration changes
- Deployment scripts
- CI/CD pipelines

**Use Grep to Search**:
```bash
# Find API endpoint definitions
Grep: pattern="@app\\.(get|post|put|delete)" (FastAPI)
Grep: pattern="class.*ViewSet|class.*APIView" (Django)
Grep: pattern="router\\.(get|post)" (Express)

# Find model definitions
Grep: pattern="class.*\\(models\\.Model\\)" (Django)
Grep: pattern="class.*\\(BaseModel\\)" (Pydantic/FastAPI)

# Find component definitions
Grep: pattern="function.*Component|const.*Component" (React)
Grep: pattern="export default.*defineComponent" (Vue)
```

### Step 4: Detect Documentation Gaps

Compare code changes against existing documentation to identify gaps.

**Gap Categories**:

1. **Missing Documentation**:
   - New features without README updates
   - New API endpoints not documented
   - New models/schemas without descriptions
   - New components without usage examples

2. **Outdated Documentation**:
   - API docs referencing removed endpoints
   - Installation instructions outdated
   - Configuration examples missing new options
   - Architecture diagrams not reflecting current structure

3. **Incomplete Documentation**:
   - API docs missing request/response examples
   - README missing setup instructions
   - No architecture overview
   - Missing deployment guide
   - Absence of Mermaid diagrams for complex flows

4. **Inconsistent Documentation**:
   - README contradicts code
   - API docs show wrong endpoint paths
   - Environment variables documented differently than used

### Step 5: Assess Documentation Impact

For each gap, determine severity and priority:

**Severity Levels**:
- 🔴 **Critical**: Blocks users from using the project (missing setup, wrong install commands)
- 🟡 **High**: Significantly impacts understanding (missing API docs, outdated architecture)
- 🟢 **Medium**: Helpful but not blocking (missing examples, incomplete guides)
- 🔵 **Low**: Nice-to-have (additional diagrams, expanded explanations)

**Priority Factors**:
- User impact (external users vs internal team)
- Feature visibility (public API vs internal utility)
- Change magnitude (major refactor vs minor fix)
- Documentation type (critical README vs supplementary guide)

### Step 6: Generate Analysis Report

Create a structured report with findings:

**Report Format**:

```markdown
# Documentation Analysis Report

## Summary
- Total documentation files: X
- Files analyzed: Y
- Gaps identified: Z
- Last commit analyzed: [commit hash]

## Existing Documentation
### Complete ✅
- [file path]: [brief description]

### Outdated ⚠️
- [file path]: [what's outdated]

### Missing ❌
- [expected file]: [why it's needed]

## Code Changes Detected
### Modified Components
- [component type]: [list of components]

### Impact Areas
- [area]: [description of changes]

## Documentation Gaps

### Critical 🔴
1. **[Gap Title]**
   - **Affected File**: [file path or "Not exists"]
   - **Issue**: [description]
   - **Code Reference**: [file:line or component]
   - **Recommendation**: [what to add/update]

### High Priority 🟡
[same format as above]

### Medium Priority 🟢
[same format as above]

### Low Priority 🔵
[same format as above]

## Recommendations

### Immediate Actions
1. [action item]
2. [action item]

### Suggested Updates
- **[file path]**: [specific section to update]
- **New files**: [files to create]

### Diagrams Needed
- [diagram type]: [what it should show]
- [diagram type]: [what it should show]

## Next Steps
1. Review this report
2. Prioritize gap remediation
3. Invoke docs-bootstrapper for missing structure (if needed)
4. Update documentation with approved changes
```

## Output Specification

The report should be:
- **Actionable**: Clear recommendations for each gap
- **Prioritized**: Ordered by severity
- **Specific**: Reference exact files, lines, components
- **Comprehensive**: Cover all gap categories
- **Structured**: Easy to scan and understand

## Integration with Other Skills

This skill is designed to work with:
- **docs-manager**: Invoked by docs-manager to get analysis before updates
- **docs-bootstrapper**: Identifies when bootstrapping is needed
- **mermaid-expert**: Identifies where diagrams are needed

## Example Usage

**Scenario**: User made changes to authentication system

**docs-analyzer actions**:
1. Catalogs existing docs: README.md, docs/api.md, docs/auth.md
2. Analyzes git history: Finds changes in auth/ directory
3. Identifies affected components: AuthService, LoginEndpoint, User model
4. Detects gaps:
   - README missing new OAuth setup
   - API docs show old token format
   - No sequence diagram for auth flow
5. Generates report with priorities
6. Returns structured report to caller

## Guidelines

### Do:
- ✅ Analyze git history comprehensively
- ✅ Catalog all documentation files
- ✅ Provide specific file/line references
- ✅ Prioritize gaps by user impact
- ✅ Generate actionable recommendations
- ✅ Return structured, parseable reports

### Don't:
- ❌ Make assumptions about what documentation should contain
- ❌ Skip cataloging existing docs
- ❌ Generate vague recommendations
- ❌ Ignore commit messages and git context
- ❌ Overwhelm with low-priority items
- ❌ Make documentation changes (read-only analysis)

## Standalone Usage

While designed for orchestration, this skill can be invoked directly:

```
User: /docs-analyzer

Skill: Analyzes codebase and generates comprehensive documentation gap report
```

This allows developers to audit documentation health independently from the update workflow.
