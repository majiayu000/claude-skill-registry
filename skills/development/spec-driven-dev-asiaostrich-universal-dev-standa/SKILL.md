---
name: spec
scope: universal
description: |
  Guide Spec-Driven Development (SDD) workflow for planning changes before implementation.
  Use when: creating specs, proposals, planning features, using OpenSpec or similar tools.
  Keywords: spec, specification, SDD, proposal, openspec, design doc, 規格, 提案, 設計文件.
---

# Spec-Driven Development Guide

> **Language**: English | [繁體中文](../../locales/zh-TW/skills/spec-driven-dev/SKILL.md)

**Version**: 1.1.0
**Last Updated**: 2026-01-26
**Applicability**: Claude Code Skills

---

## Purpose

This skill guides you through Spec-Driven Development (SDD), ensuring changes are planned, documented, and approved before implementation.

## Quick Reference

### SDD Workflow

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Proposal   │───▶│    Review    │───▶│Implementation│
└──────────────┘    └──────────────┘    └──────────────┘
                                               │
                                               ▼
                    ┌──────────────┐    ┌──────────────┐
                    │   Archive    │◀───│ Verification │
                    └──────────────┘    └──────────────┘
```

### Workflow Stages

| Stage | Description | Output |
|-------|-------------|--------|
| **Proposal** | Define what to change and why | `proposal.md` |
| **Review** | Stakeholder approval | Approval record |
| **Implementation** | Execute approved spec | Code, tests, docs |
| **Verification** | Confirm implementation matches spec | Test results |
| **Archive** | Close and archive | Archived spec with links |

### Core Principles

| Principle | Description |
|-----------|-------------|
| **Evaluate First** | Assess scope and sync needs before creating spec |
| **Spec First** | No functional changes without approved spec |
| **Tool Priority** | Use SDD tool commands when available |
| **Methodology > Tooling** | SDD works with any tool or manual process |
| **Bidirectional Sync** | Changes propagate to all related artifacts |

### Pre-Spec Evaluation

Before creating a specification, answer these questions:

| Question | Options | Result |
|----------|---------|--------|
| **Scope?** | Project-specific / Universal | Determines if Core Standard needed |
| **Interactive?** | Yes / No | Determines if Skill needed |
| **User-triggered?** | Yes / No | Determines if Command needed |

### Exceptions to "Spec First"

- Critical hotfixes (restore service immediately, document later)
- Trivial changes (typos, comments, formatting)

## Proposal Template

```markdown
# [SPEC-ID] Feature Title

## Summary
Brief description of the proposed change.

## Motivation
Why is this change needed? What problem does it solve?

## Detailed Design
Technical approach, affected components, data flow.

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Dependencies
List any dependencies on other specs or external systems.

## Risks
Potential risks and mitigation strategies.
```

## Detailed Guidelines

For complete standards, see:
- [Spec-Driven Development Standards](../../core/spec-driven-development.md)

### AI-Optimized Format (Token-Efficient)

For AI assistants, use the YAML format files for reduced token usage:
- Base standard: `ai/standards/spec-driven-development.ai.yaml`

## Integration with Other Standards

### With Commit Messages

Reference spec ID in commit messages:

```
feat(auth): implement login feature

Implements SPEC-001 login functionality with OAuth2 support.

Refs: SPEC-001
```

### With Check-in Standards

Before checking in code for a spec:

- [ ] Spec is approved
- [ ] Implementation matches spec
- [ ] Tests cover acceptance criteria
- [ ] Spec ID referenced in PR

### With Code Review

Reviewers should verify:

- [ ] Change matches approved spec
- [ ] No scope creep beyond spec
- [ ] Spec acceptance criteria met

## Examples

### ✅ Good Practices

```markdown
# SPEC-001 Add OAuth2 Login

## Summary
Add Google OAuth2 login to allow users to sign in with their Google accounts.

## Motivation
- Reduce friction for new users
- Improve security by not storing passwords

## Acceptance Criteria
- [ ] Users can click "Sign in with Google" button
- [ ] New users are automatically registered
- [ ] Existing users are linked to Google account
```

### ❌ Bad Practices

```markdown
# Add login

Adding login.
```
- Missing spec ID
- No motivation
- No acceptance criteria

## Common SDD Tools

| Tool | Description | Command Examples |
|------|-------------|------------------|
| **OpenSpec** | Specification management | `/openspec proposal`, `/openspec approve` |
| **Spec Kit** | Lightweight spec tracking | `/spec create`, `/spec close` |
| **Manual** | No tool, file-based | Create `specs/SPEC-XXX.md` manually |

## Sync Verification

After completing a spec, verify synchronization:

### Sync Checklist

```markdown
## Sync Status

### Scope: [Universal|Project|Utility]

- [ ] Core Standard: [Created|Updated|N/A]
- [ ] Skill: [Created|Updated|N/A]
- [ ] Command: [Created|Updated|N/A]
- [ ] Translations: [Synced|Pending|N/A]
```

### Sync Matrix

| Change Origin | Sync To |
|---------------|---------|
| Core Standard | → Skills, Commands, Translations |
| Skill | → Core Standard, Commands, Translations |
| Command | → Skill, Translations |

## Best Practices

### Do's

- ✅ Evaluate scope before creating spec
- ✅ Keep specs focused and atomic (one change per spec)
- ✅ Include clear acceptance criteria
- ✅ Link specs to implementation PRs
- ✅ Archive specs after completion
- ✅ Verify sync status before closing

### Don'ts

- ❌ Start coding before spec approval
- ❌ Skip scope evaluation
- ❌ Modify scope during implementation without updating spec
- ❌ Leave specs in limbo (always close or archive)
- ❌ Skip verification step
- ❌ Forget to sync related artifacts

---

## Configuration Detection

This skill supports project-specific configuration.

### Detection Order

1. Check for SDD tool in workspace (OpenSpec, Spec Kit, etc.)
2. Check `CONTRIBUTING.md` for spec workflow documentation
3. If not found, **default to manual file-based workflow**

### First-Time Setup

If no configuration found:

1. Ask the user: "This project hasn't configured SDD. Would you like to set up a specs directory?"
2. Suggest documenting in `CONTRIBUTING.md`:

```markdown
## Spec-Driven Development

We use Spec-Driven Development for all non-trivial changes.

### Process
1. Create proposal in `specs/` directory
2. Get approval from team lead
3. Implement and reference spec in PR
4. Archive spec after merge

### Spec Template
See `specs/TEMPLATE.md`
```

---

## Related Standards

- [Spec-Driven Development Standards](../../core/spec-driven-development.md)
- [Commit Message Guide](../../core/commit-message-guide.md)
- [Code Review Checklist](../../core/code-review-checklist.md)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.1.0 | 2026-01-26 | Added: Pre-Spec Evaluation, Sync Verification, Sync Matrix, enhanced best practices |
| 1.0.0 | 2025-12-30 | Initial release |

---

## License

This skill is released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

**Source**: [universal-dev-standards](https://github.com/AsiaOstrich/universal-dev-standards)
