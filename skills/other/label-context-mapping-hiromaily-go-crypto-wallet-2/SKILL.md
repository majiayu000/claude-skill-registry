---
name: label-context-mapping
description: Maps GitHub labels to Skills and Context documents. Use when creating issues (github-issue-creation) or working on issues (fix-issue command).
---

# Label → Context Mapping

Central mapping from GitHub labels to Skills and Context documents.

**SSOT**: This skill defines the operational mappings. Label definitions are in [Task Classification](../../../docs/standards/task-classification.md).

## When to Use

- **Creating issues**: Determine which labels to apply
- **Working on issues**: Determine which skills and contexts to load

## Label Categories

### Type Labels → Context Documents

| Label | Context Document |
|-------|------------------|
| `bug` | `docs/task-contexts/bug-fix.md` |
| `enhancement` | `docs/task-contexts/feature-add.md` |
| `refactoring` | `docs/task-contexts/refactoring.md` |
| `documentation` | `docs/task-contexts/documentation.md` |
| `security` | `docs/task-contexts/security.md` |
| `technical-debt` | `docs/task-contexts/refactoring.md` |
| `test` | `docs/task-contexts/test.md` |

### Language Labels → Skills

| Label | Skill | Verification |
|-------|-------|--------------|
| `lang:go` | `go-development` | `make go-lint && make tidy && make check-build && make gotest` |
| `lang:typescript` | `typescript-development` | See skill for app-specific commands (Bun for xrpl-grpc-server, npm for erc20-token) |
| `lang:solidity` | `solidity-development` | `truffle compile && truffle test` |

### Scope Labels → Skills

| Label | Skill | Verification |
|-------|-------|--------------|
| `scope:docs` | `docs-update` | Markdown formatting |
| `scope:devops` | `devops` | `yamllint`, workflow test |
| `scope:scripts` | `shell-scripts` | `make shfmt` |
| `scope:makefile` | `makefile-update` | `make mk-lint` |
| `scope:db` | `db-migration` (+ `go-development`) | `make atlas-fmt && make atlas-lint && make sqlc` |
| `scope:config` | - | Syntax validation |
| `scope:proto` | - | `make proto` |

### Chain Labels → Context Documents

| Label | Context Documents |
|-------|-------------------|
| `chain:btc` | `docs/task-contexts/chain-specific.md`, `docs/task-contexts/chains/btc.md` |
| `chain:bch` | `docs/task-contexts/chain-specific.md`, `docs/task-contexts/chains/bch.md` |
| `chain:eth` | `docs/task-contexts/chain-specific.md`, `docs/task-contexts/chains/eth.md` |
| `chain:erc20` | `docs/task-contexts/chain-specific.md`, `docs/task-contexts/chains/eth.md` |
| `chain:xrp` | `docs/task-contexts/chain-specific.md`, `docs/task-contexts/chains/xrp.md` |
| `chain:all` | `docs/task-contexts/chain-specific.md` |

### Test Scope Labels → Verification

| Label | Verification |
|-------|--------------|
| `unit-test` | `make gotest` |
| `integration-test` | `make gotest-integration` |
| `e2e-test` | `make btc-e2e-*` or chain-specific E2E |

## Loading Procedure

### From Issue Labels

```
1. Parse issue labels
2. Load contexts:
   - Type label → Context document
   - Chain label → Chain context (if present)
3. Load skills:
   - Always: git-workflow
   - Lang/Scope label → Development skill
4. Apply verification commands from skill
```

### Mapping Examples

| Labels | Skills Loaded | Contexts Loaded |
|--------|---------------|-----------------|
| `bug`, `lang:go`, `chain:btc` | `git-workflow`, `go-development` | bug-fix.md, chains/btc.md |
| `enhancement`, `lang:typescript`, `chain:xrp` | `git-workflow`, `typescript-development` | feature-add.md, chains/xrp.md |
| `documentation`, `scope:docs` | `git-workflow`, `docs-update` | documentation.md |
| `refactoring`, `scope:db`, `lang:go` | `git-workflow`, `db-migration`, `go-development` | refactoring.md, db-change.md |
| `test`, `lang:go`, `unit-test` | `git-workflow`, `go-development` | test.md |
| `security`, `lang:go` | `git-workflow`, `go-development` | security.md |

## Label Selection Rules

### Required Labels

Every issue must have:
1. **One Type label** (`bug`, `enhancement`, `refactoring`, `documentation`, `security`, `technical-debt`, `test`)
2. **One Language OR Scope label** (`lang:*` or `scope:*`)

### Optional Labels

- **Chain label**: Only for cryptocurrency-specific code
- **Test Scope label**: Only when Type is `test`

## Quick Reference

```
Required: [Type] + [Language OR Scope]
Optional: [Test Scope] + [Chain]

Type label → Context document (what to do)
Lang/Scope label → Skill (how to do)
Chain label → Chain context (domain knowledge)
```

## Related

- [Task Classification SSOT](../../../docs/standards/task-classification.md) - Label definitions
- [GitHub Labels](.github/labels.yml) - Label configuration
- `github-issue-creation` - Uses this mapping for issue creation
- `fix-issue` command - Uses this mapping for issue work
