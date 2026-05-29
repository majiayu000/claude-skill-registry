---
name: rad
description: Response-Aware Development (RAD) - Systematic verification of code assumptions using multi-model AI analysis. Auto-activates on keywords assumption, verify assumptions, list assumptions, RAD, response-aware, assumption tags, critical assumptions, assumption verification. Routes to verification, listing, and testing workflows.
allowed-tools: Read, Bash(git:*, find:*, grep:*), Grep, mcp__zen-core__chat, mcp__zen-core__dynamic_model_selector, Task
---

# Response-Aware Development (RAD) Skill

Systematic approach to identifying and verifying implicit assumptions in code using multi-model AI analysis. Prevents production failures by catching assumptions before they reach deployment.

## When This Skill Activates

This skill automatically activates when user mentions:
- "assumption" or "assumptions"
- "verify assumptions" or "check assumptions"
- "list assumptions" or "find assumptions"
- "RAD" or "response-aware"
- "assumption tags" or "assumption verification"
- "critical assumptions" or "assumption analysis"

## What This Skill Does

The RAD methodology identifies implicit assumptions that could cause production failures and routes them to appropriate AI models for verification based on risk level:

- **#CRITICAL**: Production-critical assumptions (payments, security, concurrency) → Premium models
- **#ASSUME**: Standard assumptions (state management, APIs, validation) → Dynamic free models
- **#EDGE**: Edge cases (browser compatibility, performance) → Fast free models

## User Intent Detection and Routing

### Assumption Verification
**Triggers**: "verify assumptions", "check my assumptions", "validate code assumptions", "run RAD verification"

**Route to**: [/rad/verify](workflows/verify.md) workflow

**Examples**:
- "verify all assumptions in my code"
- "check critical assumptions only"
- "run assumption verification on changed files"

### Assumption Listing
**Triggers**: "list assumptions", "find assumptions", "show all assumptions", "assumption inventory"

**Route to**: [/rad/list](workflows/list.md) workflow

**Examples**:
- "list all assumptions in the project"
- "show me critical assumptions"
- "find unverified assumptions"

### RAD Testing
**Triggers**: "test RAD", "RAD demo", "test assumption system", "sample assumptions"

**Route to**: [/rad/test](workflows/test.md) workflow

**Examples**:
- "test the RAD system"
- "show me how RAD works"
- "create sample assumptions"

### General RAD Questions
**Triggers**: "how does RAD work", "what is response-aware development", "assumption tagging guide"

**Action**: Load [methodology context](context/methodology.md) and explain RAD concepts

**Examples**:
- "explain the RAD methodology"
- "how do I tag assumptions?"
- "what are the assumption categories?"

## Quick Command Reference

```bash
# Verify assumptions (tiered strategy, changed files only)
/rad/verify --strategy=tiered --scope=changed-files

# Verify only critical assumptions
/rad/verify --strategy=critical-only

# List all assumptions in project
/rad/list

# List assumptions in specific directory
/rad/list src/

# Test RAD system with samples
/rad/test

# Test with specific scenario
/rad/test advanced
```

## RAD Methodology Overview

### Assumption Tagging Standards

Tag assumptions during development to enable systematic verification:

```javascript
// #CRITICAL: [category]: [assumption that could cause outages/data loss]
// #VERIFY: [defensive code required]
// Example: Payment processing, auth flows, concurrent writes

// #ASSUME: [category]: [assumption that could cause bugs]
// #VERIFY: [validation needed]
// Example: UI state, form validation, API responses

// #EDGE: [category]: [assumption about uncommon scenarios]
// #VERIFY: [optional improvement]
// Example: Browser compatibility, slow networks
```

### Critical Assumption Categories (Mandatory Tagging)

- **Timing Dependencies**: State updates, async operations, race conditions
- **External Resources**: API availability, file existence, network connectivity
- **Data Integrity**: Type safety at boundaries, null/undefined handling
- **Concurrency**: Shared state, transaction isolation, deadlock potential
- **Security**: Authentication, authorization, input validation
- **Payment/Financial**: Transaction integrity, retry logic, rollback handling

### Verification Workflow

1. **Tag Assumptions**: Claude tags during development, or manual tagging during review
2. **Auto-Detection**: Pre-commit hooks or explicit command trigger scan
3. **Model Routing**: Assumptions routed to appropriate models by risk level
4. **Analysis**: Fresh context prevents confirmation bias in verification
5. **Fix Generation**: Defensive code patterns generated automatically
6. **Review & Apply**: Developer reviews and applies fixes selectively

## Integration with Other Skills

### Pre-Commit Validation
Works seamlessly with [quality skill](../quality/SKILL.md):
```bash
/quality/precommit  # Includes RAD assumption verification
```

### Security Auditing
Complements [security skill](../security/SKILL.md):
```bash
/security/scan     # Static security analysis
/rad/verify        # Dynamic assumption verification
```

### Agent Integration

For complex assumption analysis, this skill coordinates with specialized agents:

- **Analysis Agent** (`mcp__zen-core__chat`): Deep assumption pattern analysis
- **Model Selector** (`mcp__zen-core__dynamic_model_selector`): Optimal model selection
- **Code Review Agent** (via Task tool): Integration with code review workflows

## Common Workflows

### Before Committing Code
```bash
# 1. Quick check of changed files
/rad/verify --scope=changed-files

# 2. If critical assumptions found, verify with premium models
/rad/verify --strategy=critical-only --budget=premium

# 3. Review and apply fixes
git diff  # Review proposed changes
git add -p  # Selectively stage fixes
```

### During Code Review
```bash
# 1. Get assumption inventory for PR
/rad/list

# 2. Verify all assumptions found
/rad/verify --strategy=tiered

# 3. Ensure no blocking issues
grep "❌ BLOCKING" assumption-report.md
```

### Technical Debt Assessment
```bash
# 1. Full project scan
/rad/list .

# 2. Identify hotspots (files with high assumption density)
# 3. Prioritize verification by risk level
# 4. Schedule verification sprints
```

## Success Metrics

- **Detection Rate**: Assumptions tagged per 1000 lines of code
- **Fix Rate**: Percentage of assumptions requiring defensive code
- **Cost Efficiency**: >90% of verifications using free models
- **Production Impact**: Reduction in assumption-related incidents

## Resources

- **Complete Methodology**: See [context/methodology.md](context/methodology.md)
- **Tagging Standards**: See [context/tagging-standards.md](context/tagging-standards.md)
- **Verification Workflow**: See [workflows/verify.md](workflows/verify.md)
- **Global Standards**: See `CLAUDE.md > Response-Aware Development`

---

*Consolidated from verify-assumptions-smart, list-assumptions, and test-rad commands.*
