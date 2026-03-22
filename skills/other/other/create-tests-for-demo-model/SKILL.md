---
name: create-tests-for-demo-model
description: Create tests for Diff Studio demo models
argument-hint: <ts-file path>
---

# Create Tests for Diff Studio Demo Model

Create tests for a Diff Studio model defined in the TS file at the path specified in the argument.

## Instructions

1. **Parse input**: extract the path to the TS file from the argument. Verify the file exists and has a `.ts` extension.

2. **Read the TS file**: open it and locate the single exported object of type `ModelInfo`. Note:
   - The export name (e.g., `export const myModel: ModelInfo = { ... }`).
   - The `equations` field of the exported object.

3. **Extract the file name**: derive the base file name (without directory path and without the `.ts` extension) from the given path. This will be used as the test case name.

4. **Update the test file** `src/tests/demo-models-tests.ts`:

   a. **Add import**: at the top of the file (with other imports), add:
```ts
      import { <exportName> } from '<relative-path-to-ts-file>';
```
      Use the correct relative path from `src/tests/` to the target file (without the `.ts` extension in the import path).

   b. **Add test case**: inside the `'Demo models'` category block, add a call to `testTemplate` (imported from `./test-utils`):
```ts
      testTemplate('<file-name>', <exportName>.equations);
```
      - First argument: string with the TS file name (e.g., `'my-model'`).
      - Second argument: the `equations` field of the imported `ModelInfo` object.

   c. **Placement**: add the new test case in alphabetical order relative to existing test cases, or at the end of the `'Demo models'` category if ordering is not established.

## Example

Given argument: `src/demos/acid-base.ts`

If the file exports:
```ts
export const acidBase: ModelInfo = { equations: `...`, ... };
```

Then in `src/tests/demo-models-tests.ts`:
```ts
import { acidBase } from '../demos/acid-base';
// ...
testTemplate('acid-base', acidBase.equations);
```