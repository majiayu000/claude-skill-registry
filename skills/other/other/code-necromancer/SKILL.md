---
name: code-necromancer
description: Systematic framework for resurrecting and modernizing legacy codebases through archaeology, resurrection, and rejuvenation phases. Activate on "legacy code", "inherited codebase", "no documentation", "technical debt", "resurrect", "modernize". NOT for greenfield projects or well-documented active codebases.
allowed-tools: Read,Write,Edit,Bash,WebFetch,Grep,Glob
category: Code Quality & Testing
tags:
  - legacy
  - modernization
  - technical-debt
  - archaeology
  - refactoring
pairs-with:
  - skill: refactoring-surgeon
    reason: Clean up discovered legacy code
  - skill: technical-writer
    reason: Document resurrected codebases
---

# Code Necromancer

**Tagline**: Raise dead codebases from the grave

Systematic framework for understanding, resurrecting, and modernizing legacy codebases.

## When to Activate

✅ **Use when:**
- Inheriting a codebase with 5+ repos and no documentation
- Resurrecting a product dormant for 2+ years
- Joining a company with significant technical debt and tribal knowledge loss
- Performing due diligence on acquired codebases
- Modernizing legacy systems without breaking existing functionality

❌ **NOT for:**
- Greenfield projects (start fresh instead)
- Well-documented active codebases
- Simple bug fixes in maintained systems

## The Three Phases

### Phase 1: ARCHAEOLOGY
**Objective**: Create a complete map before touching anything.

| Output | Description |
|--------|-------------|
| `repo-inventory.json` | All repos with metadata, languages, activity |
| `dependency-graph.mmd` | Inter-repo and external dependencies |
| `architecture-diagram.mmd` | Visual system topology |
| `tech-stack-matrix.md` | Language/framework versions per repo |
| `maturity-assessment.md` | Code quality, test coverage, docs quality |
| `missing-pieces.md` | Gaps, orphaned repos, broken integrations |

**Process**: Inventory → Deep Scan → Cross-Reference → Visualize → Assess

→ See `references/archaeology-guide.md` for detailed techniques.

### Phase 2: RESURRECTION
**Objective**: Get the system running in development.

| Output | Description |
|--------|-------------|
| `dependency-audit.md` | Outdated packages, vulnerabilities, breaking changes |
| `environment-variables.md` | All required env vars with defaults |
| `secrets-needed.md` | API keys, certs, OAuth credentials |
| `infrastructure-status.md` | Cloud resources, what exists vs deleted |
| `resurrection-blockers.md` | Critical issues preventing launch |
| `integration-tests/` | Tests verifying components work and communicate |

**Process**: Audit Dependencies → Map Environment → Check Infrastructure → Write Tests → Document Blockers

→ See `references/integration-test-patterns.md` for resurrection test patterns.

### Phase 3: REJUVENATION
**Objective**: Modernize while maintaining feature parity.

| Output | Description |
|--------|-------------|
| `security-recommendations.md` | Vulnerability fixes, compliance |
| `modernization-roadmap.md` | Prioritized upgrades with effort estimates |
| `architecture-improvements.md` | Scalability, performance, maintainability |

**Process**: Security First → Infrastructure (containerize, CI/CD) → Code Quality → Architecture

## Key Commands

```bash
# List all repos in org
gh repo list ORG --limit 1000 --json name,primaryLanguage,pushedAt

# Dependency analysis
npm audit && npm outdated      # Node.js
pip list --outdated && safety check  # Python
go mod graph                    # Go

# Find env vars in code
grep -rn 'process\.env\|os\.environ' --include="*.js" --include="*.py"
```

→ See `references/framework-detection.md` for framework/stack identification.
→ See `references/infrastructure-mapping.md` for cloud resource discovery.
→ See `references/dependency-patterns.md` for dependency detection.

## Anti-Patterns to Avoid

### 1. Premature Resurrection
**What it looks like**: Running `npm install` before reading any code
**Why it's wrong**: You'll fix the same bug 5 times; dependencies have changed
**Fix**: Complete archaeology first; understand before touching

### 2. Scope Creep
**What it looks like**: "Let's also refactor while we're here"
**Why it's wrong**: Scope explosion; never actually resurrect
**Fix**: Strict phase separation; refactoring is Phase 3

### 3. Big Bang Updates
**What it looks like**: Update all dependencies in one commit
**Why it's wrong**: Something breaks, no idea what
**Fix**: Update incrementally; test after each

### 4. Ignoring Tests
**What it looks like**: "It runs, ship it"
**Why it's wrong**: Regression city; no baseline for changes
**Fix**: Write resurrection tests as you go; they prove progress

### 5. Undocumented Changes
**What it looks like**: "I fixed it but forgot what I changed"
**Why it's wrong**: Tribal knowledge returns; next person is you in 6 months
**Fix**: Document everything you learn and change

### 6. Trusting Old Documentation
**What it looks like**: Following README from 2019
**Why it's wrong**: APIs change, services get deprecated
**Fix**: Verify every instruction; documentation lies

## Success Metrics

### Archaeology Complete When:
- [ ] All repos cataloged with metadata
- [ ] Dependency graph visualized
- [ ] Architecture diagram created
- [ ] Core vs peripheral repos identified
- [ ] Missing pieces documented

### Resurrection Complete When:
- [ ] All services start locally
- [ ] Services can communicate with each other
- [ ] Integration tests pass
- [ ] At least one full user flow works

### Rejuvenation Complete When:
- [ ] No critical security vulnerabilities
- [ ] All dependencies reasonably current
- [ ] CI/CD pipeline working
- [ ] Documentation current
- [ ] Team can develop new features

## References

→ `references/archaeology-guide.md` - Deep code archaeology techniques
→ `references/dependency-patterns.md` - Dependency detection across ecosystems
→ `references/framework-detection.md` - Framework/stack identification
→ `references/infrastructure-mapping.md` - Cloud resource discovery
→ `references/integration-test-patterns.md` - Resurrection test patterns

## Templates

→ `templates/repo-inventory.json` - Repository catalog
→ `templates/archaeology-report.md` - Phase 1 output
→ `templates/resurrection-plan.md` - Phase 2 output
→ `templates/rejuvenation-roadmap.md` - Phase 3 output
