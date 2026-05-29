---
name: brownfield-analyzer
description: Analyzes existing brownfield projects to map documentation structure to SpecWeave's PRD/HLD/Spec/Runbook pattern. Scans folders, classifies documents, detects external tools (Jira, ADO, GitHub), and creates project context map for just-in-time migration. Activates for brownfield, existing project, migrate, analyze structure, legacy documentation.
---

# Brownfield Analyzer

**Self-contained brownfield project analysis for ANY existing codebase.**

---

## Purpose

Analyze existing projects and create migration plan to SpecWeave structure. Two paths supported: Quick Start (incremental) or Comprehensive (upfront).

---

## Two Migration Paths

### Path 1: Quick Start (Recommended for Large Projects)

**Best for**: 50k+ LOC, fast iteration, small teams

**Process**:
1. Initial scan: Document core architecture (1-3 hours)
2. Start working immediately
3. Per increment: Document → Modify → Update docs
4. Documentation grows with changes

**Benefits**:
- Start in days, not weeks
- Focus where it matters
- No analysis paralysis

### Path 2: Comprehensive Upfront

**Best for**: <50k LOC, teams, regulated industries

**Process**:
1. Full analysis (1-4 weeks)
2. Document all modules, business rules
3. Create baseline tests
4. Then start increments

**Benefits**:
- Complete context upfront
- Full regression coverage
- Team coordination
- Compliance ready

### Automatic Recommendation

| Project Size | LOC | Upfront Effort | Recommended |
|--------------|-----|----------------|-------------|
| Small | <10k | 4-8 hours | Comprehensive |
| Medium | 10k-50k | 1-2 weeks | User Choice |
| Large | 50k-200k | 2-4 weeks | Quick Start |
| Very Large | 200k+ | 1-3 months | Quick Start (Mandatory) |

---

## Analysis Workflow

### Step 1: Project Assessment

```bash
# Scan project
find . -type f -name "*.ts" -o -name "*.js" -o -name "*.py" | wc -l
find . -type f \( -name "*.ts" -o -name "*.js" \) -exec wc -l {} + | awk '{sum+=$1} END {print sum}'
```

**Calculate**:
- Total files
- Total LOC
- Module count
- Test coverage (if exists)

**Output**:
```
📊 Project Analysis
   Files: 1,245
   LOC: 45,678
   Modules: 23
   Tests: 45% coverage

💡 Recommendation: Medium project → User choice (Quick Start or Comprehensive)
```

### Step 2: Document Classification

Scan for documentation:

**PRD Candidates** (Product Requirements):
- `requirements.md`, `PRD.md`, `product-spec.md`
- `docs/product/`, `specs/requirements/`

**HLD Candidates** (High-Level Design):
- `architecture.md`, `design.md`, `ARCHITECTURE.md`
- `docs/architecture/`, `docs/design/`

**ADR Candidates** (Architecture Decision Records):
- `adr/`, `decisions/`, `docs/decisions/`
- Files with "ADR-" prefix or "decision" in name

**Spec Candidates** (Technical Specs):
- `spec.md`, `technical-spec.md`
- `docs/specs/`, `docs/technical/`

**Runbook Candidates** (Operations):
- `runbook.md`, `operations.md`, `deployment.md`
- `docs/ops/`, `docs/runbooks/`

**Diagrams**:
- `*.png`, `*.svg`, `*.drawio`, `*.mmd`
- `diagrams/`, `docs/diagrams/`

### Step 3: External Tool Detection

**Jira Integration**:
```bash
# Search for Jira references
grep -r "JIRA" . --include="*.md" --include="*.txt"
grep -r "jira.atlassian" . --include="*.md"
```

**Azure DevOps**:
```bash
grep -r "dev.azure.com" . --include="*.md"
grep -r "visualstudio.com" . --include="*.md"
```

**GitHub Issues**:
```bash
grep -r "github.com/.*/issues" . --include="*.md"
```

### Step 4: Coding Standards Discovery

**Auto-detect**:
- ESLint config (`.eslintrc`, `eslint.config.js`)
- Prettier config (`.prettierrc`)
- TypeScript config (`tsconfig.json`)
- Test config (`vitest.config`, `jest.config`)

**Analyze patterns**:
```bash
# Naming conventions
grep -rh "^export function" src/ | head -20
grep -rh "^export class" src/ | head -20

# Import patterns
grep -rh "^import" src/ | sort | uniq -c | sort -rn | head -10
```

### Step 5: Generate Migration Plan

**Quick Start Plan**:
```markdown
# Migration Plan: Quick Start Path

## Phase 1: Initial Setup (1-2 hours)
- [ ] Run `specweave init`
- [ ] Document core architecture only
- [ ] Create 1-2 ADRs for critical decisions

## Phase 2: First Increment (1-3 days)
- [ ] Select first feature to modify
- [ ] Document module before touching
- [ ] Create increment with /sw:increment
- [ ] Implement changes
- [ ] Update docs

## Phase 3: Iterate
- [ ] Repeat per feature
- [ ] Documentation grows organically
```

**Comprehensive Plan**:
```markdown
# Migration Plan: Comprehensive Path

## Phase 1: Documentation Baseline (1-2 weeks)
- [ ] Map all modules to .specweave/docs/internal/modules/
- [ ] Create ADRs for major architectural decisions
- [ ] Document business rules
- [ ] Identify technical debt

## Phase 2: Test Baseline (1 week)
- [ ] Add baseline tests for core functionality
- [ ] Target 60-70% coverage
- [ ] Document test strategy

## Phase 3: Structure Migration (2-3 days)
- [ ] Run `specweave init`
- [ ] Migrate existing docs
- [ ] Organize by SpecWeave structure

## Phase 4: Ready for Increments
- [ ] Start feature work with full context
```

---

## Migration Checklist

### Before SpecWeave Init

- [ ] Assess project size (LOC, files)
- [ ] Choose path (Quick Start or Comprehensive)
- [ ] Backup existing docs
- [ ] Identify external tool integrations
- [ ] Check coding standards exist

### During Migration

**Quick Start**:
- [ ] Document core architecture only
- [ ] Create 1-2 critical ADRs
- [ ] Set up external tool sync (optional)
- [ ] Start first increment immediately

**Comprehensive**:
- [ ] Scan all documentation
- [ ] Classify and organize docs
- [ ] Create complete module docs
- [ ] Document all business rules
- [ ] Create ADRs for decisions
- [ ] Add baseline tests
- [ ] Set up external tool sync

### After Migration

- [ ] Verify `.specweave/` structure exists
- [ ] Test increment workflow
- [ ] Train team on SpecWeave
- [ ] Document migration decisions

---

## Document Mapping

**Map existing docs to SpecWeave structure**:

```
Existing Structure          SpecWeave Structure
─────────────────          ───────────────────
docs/product/              .specweave/docs/internal/strategy/
docs/architecture/         .specweave/docs/internal/architecture/
docs/decisions/            .specweave/docs/internal/architecture/adr/
docs/specs/                .specweave/docs/internal/specs/
docs/runbooks/             .specweave/docs/public/runbooks/
docs/api/                  .specweave/docs/public/api-docs/
README.md                  .specweave/docs/public/README.md
CONTRIBUTING.md            .specweave/docs/public/CONTRIBUTING.md
```

---

## External Tool Migration

### Jira → SpecWeave

**1. Detect Jira usage**:
```bash
grep -r "jira" . --include="*.md" | head -5
```

**2. Map Jira structure**:
- Epic → Feature (FS-XXX)
- Story → User Story (US-XXX)
- Task → Task (T-XXX)

**3. Sync strategy**:
```bash
# Option 1: Import existing Jira items
/sw-jira:sync --import

# Option 2: Start fresh, sync new work only
# (Use SpecWeave as source of truth)
```

### Azure DevOps → SpecWeave

**Map work items**:
- Feature → Feature (FS-XXX)
- User Story → User Story (US-XXX)
- Task → Task (T-XXX)

**Sync**:
```bash
/sw-ado:sync --import
```

### GitHub Issues → SpecWeave

**Map issues**:
- Milestone → Feature (FS-XXX)
- Issue → User Story (US-XXX)
- Task list → Tasks (T-XXX)

**Sync**:
```bash
/sw-github:sync --import
```

---

## Best Practices

**✅ DO**:
- Choose appropriate path (Quick Start for large projects)
- Document before modifying code
- Migrate incrementally (don't big-bang)
- Preserve existing docs (don't delete)
- Use external tool sync for existing items
- Train team on SpecWeave workflow

**❌ DON'T**:
- Force Comprehensive for 100k+ LOC projects
- Delete existing documentation
- Migrate all features upfront (Quick Start)
- Skip coding standards discovery
- Ignore external tool integrations
- Over-analyze in Quick Start mode

---

## Example: Large Project Migration

**Scenario**: 85k LOC Node.js backend, Jira, 15% test coverage

**Recommended**: Quick Start

**Plan**:
```
Week 1: Setup (2 hours)
- Run specweave init
- Document core architecture (5 modules)
- Create 2 ADRs (database, API design)
- Configure Jira sync

Week 1-2: First Increment
- Select first feature: "Add rate limiting"
- Document rate-limiting module
- Create increment with /sw:increment
- Implement with TDD
- Update docs

Week 3+: Iterate
- Repeat per feature
- Documentation grows to 40% over 3 months
- Eventually covers critical paths
```

**Result**: Started working in 2 hours, documentation grows naturally.

---

## Example: Small Project Migration

**Scenario**: 8k LOC Python app, GitHub Issues, 60% test coverage

**Recommended**: Comprehensive Upfront

**Plan**:
```
Week 1: Full Documentation (8 hours)
- Document all 5 modules
- Create 8 ADRs
- Map business rules
- Document API contracts

Week 1: Test Baseline (4 hours)
- Add missing unit tests (80% coverage)
- Document test strategy

Week 1: Structure Migration (2 hours)
- Run specweave init
- Migrate existing docs
- Configure GitHub sync

Week 2+: Start Increments
- Full context available
- High confidence changes
```

**Result**: 2 weeks to full documentation, then smooth increment workflow.

---

## Troubleshooting

**Issue**: Can't find existing documentation
**Solution**: Check common locations: `docs/`, `wiki/`, `.github/`, Notion exports

**Issue**: Too many documents to classify
**Solution**: Focus on architecture docs first, skip implementation details

**Issue**: Conflicting documentation
**Solution**: Use git history to find latest/canonical version

**Issue**: External tool API limits
**Solution**: Use throttled sync, batch imports

---

**This skill is self-contained and works for ANY brownfield project.**
