---
name: nx-monorepo-generator
description: Use when adding Jest testing configuration to Nx projects, running `nx
  g @nx/jest:configuration`, setting up testing infrastructure, or troubleshooting
  tests that fail after running the Jest generator
---

---
name: nx-monorepo-generator
description: Use when adding Jest testing configuration to Nx projects, running `nx g @nx/jest:configuration`, setting up testing infrastructure, or troubleshooting tests that fail after running the Jest generator. Ensures proper TypeScript moduleResolution (nodenext), testing enhancement libraries (jest-dom, user-event, MSW), and monorepo pattern adherence. Triggers: "add tests", "setup Jest", "configure testing", "Jest not working", "moduleResolution error", "tests failing after generator"
---

# Nx Monorepo Generator - Jest Configuration Workflow

The Nx Jest generator produces defaults that conflict with this workspace's standards. This skill ensures all mandatory post-generation fixes are applied.

## Phase 1: Determine Project Type

Identify the project type before generating:

| Type | Examples | Testing Needs |
|------|----------|---------------|
| **UI** | web apps, mobile | Full stack: jest-dom, user-event, MSW |
| **Node** | server, APIs | jest-dom + conditional MSW |
| **Logic** | schemas, utils | Basic Jest only |

**How to identify**:
- Check `project.json` executors (React/Next.js = UI, Node = server)
- Schema/utility libraries = Logic
- When uncertain, ask the user

## Phase 2: Generate Configuration

```bash
pnpm exec nx g @nx/jest:configuration <project-name>
```

Creates: `jest.config.ts`, `tsconfig.spec.json`, updates `project.json`

**Warning**: Generated config has incorrect defaults - proceed to Phase 3.

## Phase 3: Post-Generation Fixes

Execute ALL applicable steps. See `references/post-gen-checklist.md` for full details.

| Step | UI | Node | Logic | Script |
|------|:--:|:----:|:-----:|--------|
| Install testing libs | ✅ | ✅ | ❌ | `scripts/install-testing-libs.sh` |
| Create jest.setup.ts | ✅ | ❌ | ❌ | Manual |
| Update jest.config.ts | ✅ | ❌ | ❌ | Manual |
| Fix moduleResolution | ✅ | ✅ | ✅ | `scripts/fix-tsconfig-spec.sh` |
| Verify Jest types | ✅ | ✅ | ✅ | `scripts/validate-jest-config.sh` |
| Clean production config | ✅ | ✅ | ✅ | `scripts/validate-jest-config.sh` |

### Critical Fix: TypeScript moduleResolution

In `tsconfig.spec.json`, change:
- `"module": "commonjs"` → `"module": "nodenext"`
- `"moduleResolution": "node10"` → `"moduleResolution": "nodenext"`

**Why**: Workspace uses `customConditions` requiring modern module resolution.

## Phase 4: Validation

```bash
# Automated validation
scripts/validate-jest-config.sh <project-path>

# Run tests
pnpm exec nx run <project-name>:test
```

**Success indicators**:
- ✅ Tests run without TypeScript errors
- ✅ No module resolution warnings
- ✅ Coverage reports generate correctly

## References

- `references/post-gen-checklist.md` - Step-by-step checklist with code examples
- `references/jest-config-patterns.md` - Configuration structure and rationale
- `references/testing-standards.md` - user-event, MSW, jest-dom patterns

## Scripts

- `scripts/validate-jest-config.sh <path>` - Validate configuration against standards
- `scripts/install-testing-libs.sh <type> <path>` - Install testing packages by project type
- `scripts/fix-tsconfig-spec.sh <path>` - Auto-fix moduleResolution settings

## Key Principle

**Generated code rarely matches monorepo patterns.** Post-generation fixes are MANDATORY. This skill ensures consistency and prevents pattern drift that causes mysterious failures.
