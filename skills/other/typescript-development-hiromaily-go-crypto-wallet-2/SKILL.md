---
name: typescript-development
description: TypeScript/JavaScript development workflow for apps/ directory. Use when modifying TypeScript code in xrpl-grpc-server or JavaScript in erc20-token.
---

# TypeScript/JavaScript Development Workflow

Workflow for TypeScript/JavaScript code changes in `apps/` directory.

## Prerequisites

- **Use `git-workflow` Skill** for branch management, commit conventions, and PR creation.
- **Refer to `.claude/rules/typescript.md`** for detailed verification commands (SSOT).

## Applicable Directories

| App | Language | Runtime | Path | Status |
|-----|----------|---------|------|--------|
| xrpl-grpc-server | TypeScript | **Bun** | `apps/xrpl-grpc-server/` | **Active** |
| erc20-token | JavaScript | Node.js | `apps/erc20-token/` | Active |
| ripple-lib-server | TypeScript | Node.js | `apps/ripple-lib-server/` | **Deprecated (READ-ONLY)** |

> **Important**: `ripple-lib-server` is deprecated. All XRP server work should be done in `xrpl-grpc-server`.

## Workflow

### 1. Make Changes

Edit TypeScript/JavaScript files following the rules in `.claude/rules/typescript.md`.

### 2. Verify (from rules/typescript.md)

```bash
# xrpl-grpc-server (Bun)
cd apps/xrpl-grpc-server && bun run lint && bun run typecheck

# erc20-token (Node.js/npm)
cd apps/erc20-token && npm run lint-js && npm run fmt
```

### 3. Self-Review Checklist

- [ ] No TypeScript errors
- [ ] No `any` types (unless documented reason)
- [ ] Async errors properly handled
- [ ] Auto-generated files not edited

## Command Summary

| App | Lint | Format | Type Check |
|-----|------|--------|------------|
| xrpl-grpc-server | `bun run lint` | `bun run format` | `bun run typecheck` |
| erc20-token | `npm run lint-js` | `npm run fmt` | - |

## Related

- `.claude/rules/typescript.md` - TypeScript rules (SSOT)
- `git-workflow` - Branch, commit, PR workflow
- `solidity-development` - For Solidity contracts in erc20-token
