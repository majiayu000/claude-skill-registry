---
name: auditing-libraries
description: This skill should be used when the user asks to "audit libraries", "check library conventions", "validate lib structure", "find convention violations", "review library organization", or wants to verify that existing libraries follow the _.ts/__.ts namespace pattern correctly. Identifies and reports violations.
---

# Auditing Libraries

Analyze existing libraries for convention violations and report issues.

## CRITICAL

### Read Conventions Before Auditing

The authoritative convention documents are:

* `~/.claude/docs/conventions/namespace-module.md` — Core `_.ts`/`__.ts` pattern
* `~/.claude/docs/conventions/library-local.md` — Local library context (`src/lib/`)
* `~/.claude/docs/conventions/library-package.md` — Package-level context

Read these before auditing to understand the full rules.

## Operations

### Audit Single Library

Check a specific library for violations.

__Steps:__

1. Identify library type (local lib, package lib)
2. Check file structure matches expected pattern
3. Validate `_.ts` content
4. Validate `__.ts` content (if exists)
5. Check import patterns in code modules
6. Verify test file imports
7. Report all violations found

### Audit All Libraries

Scan project for all libraries and check each.

__Steps:__

1. Find all directories containing `_.ts` files
2. Categorize each (local lib at `src/lib/*`, package lib at `src/*`)
3. Audit each library individually
4. Summarize violations by category

### Fix Violations

After auditing, fix identified issues.

__Steps:__

1. Present violations to user
2. Propose fixes for each
3. Apply fixes with user approval
4. Re-audit to confirm resolution

## Violation Categories

### Structure Violations

| Violation       | Description                       | Fix                               |
| --------------- | --------------------------------- | --------------------------------- |
| Missing `_.ts`  | Library has no namespace module   | Create `_.ts` with correct export |
| Missing `__.ts` | Multiple impl files but no barrel | Create `__.ts` with re-exports    |
| Extra `__.ts`   | Single impl file with barrel      | Remove `__.ts`, update `_.ts`     |
| Wrong location  | Library not in `src/lib/`         | Move to correct location          |

### Namespace Module (`_.ts`) Violations

| Violation                | Description                       | Fix                        |
| ------------------------ | --------------------------------- | -------------------------- |
| Wrong export target      | Points to wrong file              | Fix export path            |
| Has imports              | Contains import statements        | Remove imports             |
| Wrong namespace name     | Doesn't match directory           | Fix namespace name         |
| Missing barrel reference | Has `__.ts` but exports from impl | Change to `from './__.js'` |

### Barrel Module (`__.ts`) Violations

| Violation           | Description                      | Fix                            |
| ------------------- | -------------------------------- | ------------------------------ |
| Imports from `_.ts` | Circular dependency              | Remove import                  |
| Value imports       | Has `import { x }` not re-export | Convert to `export { x } from` |
| External imports    | Imports from outside library     | Move to code module            |
| Parent imports      | Imports from `../`               | Remove or restructure          |

### Import Pattern Violations

| Violation              | Description                  | Fix                                             |
| ---------------------- | ---------------------------- | ----------------------------------------------- |
| Destructured namespace | `import { Foo } from '#lib'` | Use `import { Lib } from '#lib'` then `Lib.Foo` |
| Self namespace import  | Code imports own `_.ts`      | Use relative imports                            |
| Self barrel import     | Code imports own `__.ts`     | Use relative imports                            |
| Relative cross-lib     | `import from '../other-lib'` | Use `#other-lib`                                |

### Test Violations

| Violation                 | Description                 | Fix                       |
| ------------------------- | --------------------------- | ------------------------- |
| Wrong import              | Test imports from impl file | Import from `./_.js`      |
| Destructured              | Test destructures namespace | Use namespace directly    |
| Missing fixture namespace | Fixture doesn't export `Fx` | Add `export namespace Fx` |

## Audit Checklist

```markdown
## Library: <name>

### Structure

* [ ] Located at correct path (src/lib/<name>/ or src/<name>/)
* [ ] Has _.ts namespace module
* [ ] Has __.ts barrel (if multiple impl files)
* [ ] No __.ts (if single impl file)

### Namespace Module (_.ts)

* [ ] Correct export pattern
* [ ] Namespace name matches directory (PascalCase)
* [ ] No import statements
* [ ] Points to __.ts (if exists) or impl file

### Barrel Module (__.ts) - if exists

* [ ] Only contains re-exports
* [ ] No imports from _.ts
* [ ] No external package imports
* [ ] All exports from local files

### Code Modules

* [ ] No imports from own _.ts
* [ ] No imports from own __.ts
* [ ] Cross-lib imports use #<name>
* [ ] Sibling imports use relative paths

### Tests (_.test.ts)

* [ ] Imports from ./_.js only
* [ ] Uses namespace, no destructuring
* [ ] No top-level describe wrapping all tests

### Config

* [ ] package.json has imports entry
* [ ] tsconfig.json has paths entry
```

## Examples

### Violation Report Format

```
Library: src/lib/parser/

VIOLATIONS FOUND: 3

1. [NAMESPACE] _.ts has wrong export
   Current:  export * from './parser.js'
   Expected: export * as Parser from './__.js'
   Reason:   __.ts exists, so _.ts must export namespace from barrel

2. [IMPORT] tokenizer.ts imports from own namespace
   Line 3: import { Parser } from './_.js'
   Fix:     Use relative import: import { helper } from './helper.js'

3. [TEST] _.test.ts destructures namespace
   Line 1: import { tokenize, lex } from './_.js'
   Fix:     import { Parser } from './_.js' then use Parser.tokenize
```

## Notes

* Run `/fix-conventions` command for automated fixing
* Some violations require architectural decisions (restructuring)
* Package-level libraries have different path expectations
