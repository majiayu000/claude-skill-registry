---
name: angular-vitest-setup
description: Migrate Angular workspaces from Karma/Jasmine to Vitest with deterministic preflight checks, test-target builder updates, dependency cleanup, and build/test verification. Use when users ask to add Vitest, switch test runners, repair broken Vitest wiring, or standardize Angular 20 unit-test configuration.
---

# Angular 20 Vitest Setup

Use this workflow for existing Angular 20 apps that need Vitest as the unit test runner.

## Workflow

1. Run deterministic preflight checks from the Angular workspace root.

- Confirm `angular.json` exists.
- Confirm `package.json` exists.
- Confirm the target project is identified:
  - If the user names a project, use that project.
  - Otherwise, if exactly one project exists, use it.
  - Otherwise, stop and ask which project to migrate.
- Confirm the target project has a `test` target under either `architect.test` or `targets.test`.
- If any check fails, stop and report the exact missing prerequisite.

2. Validate Angular compatibility before changing config.

- Ensure the workspace uses Angular tooling compatible with `@angular/build:unit-test` (Angular 20 workflow target).
- If incompatible, stop and report the detected version/tooling mismatch.

3. Install Vitest dependencies.

```bash
npm install --save-dev vitest jsdom
```

- If dependencies are already present, do not reinstall unnecessarily.

4. Configure the project test target to use the Angular unit-test builder.

- Set `projects.<project-name>.architect.test.builder` to `@angular/build:unit-test` when `architect` is used.
- Set `projects.<project-name>.targets.test.builder` to `@angular/build:unit-test` when `targets` is used.
- Keep `test.options.tsConfig` as-is when valid; otherwise set it to `tsconfig.spec.json`.
- Remove Karma-specific test options when present (for example `karmaConfig`, browser launcher options, or Karma-only polyfills such as `zone.js/testing`).
- Preserve unrelated test options.

Reference configuration:

```json
"test": {
  "builder": "@angular/build:unit-test",
  "options": {
    "tsConfig": "tsconfig.spec.json"
  }
}
```

5. Remove Karma/Jasmine dependencies safely.

```bash
npm uninstall karma karma-chrome-launcher karma-coverage karma-jasmine karma-jasmine-html-reporter jasmine-core @types/jasmine
```

- In multi-project workspaces, remove shared dependencies only when no remaining project still requires Karma/Jasmine.
- If shared usage is uncertain, report the constraint and skip destructive removal.

6. Update spec files only when they still use Jasmine-only APIs.

- Replace Jasmine globals/matchers with Vitest-compatible APIs.
- Keep test behavior unchanged while refactoring assertions/spies.
- If no Jasmine-only usage remains, skip spec edits.

## Verification

Run from workspace root:

```bash
npm run build
npm run test -- --watch=false
```

When possible, prefer scoped verification for the target project (for example Angular CLI project flags) to avoid unrelated failures.

Then verify all of the following:

- Target project test builder is `@angular/build:unit-test` in `angular.json`.
- `vitest` and `jsdom` exist in `devDependencies`.
- Karma/Jasmine packages are removed or explicitly documented as intentionally retained for other projects.
- Tests execute without Jasmine global references like `jasmine.`.

## Failure Handling

- If preflight fails, stop before installs/config edits and report exact blockers.
- If build/test fails after migration, report failing command, key error lines, and whether rollback was avoided.
- Do not modify unrelated projects unless explicitly requested.

## Assistant Portability Rules

- Resolve and mutate only the targeted Angular project path in `angular.json`.
- Keep dependency cleanup conservative in multi-project workspaces; skip destructive removals when shared usage is unclear.
- Prefer deterministic command output in reports: exact command, exact path changed, exact blocker when stopped.

## Output Requirements

When completing this skill, report:

1. Target project and exact `angular.json` test-target path changed.
2. Dependencies added, removed, and intentionally retained (if any).
3. Verification commands run and their outcomes.
4. Remaining migration blockers and next required action.

## References

[1]: https://angular.dev/guide/testing/unit-tests
[2]: https://angular.dev/cli/test
[3]: https://vitest.dev/guide/
[4]: https://docs.npmjs.com/cli/v10/commands/npm-uninstall
