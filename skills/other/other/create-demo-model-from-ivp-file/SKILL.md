---
name: create-demo-model-from-ivp-file
description: Create a Diff Studio demo model TS file and register it in the package, using equations from an IVP file
argument-hint: <ivp-file path> [png-file path]
---

# Create Demo Model from IVP File

Create a Diff Studio demo model using equations extracted from the IVP file, and register it in the package.

## Naming Conventions

Throughout this skill, the model name extracted from the IVP file is transformed into three forms:

| Form | Example | Usage |
|---|---|---|
| Original (as in IVP) | `Acid Base` | Decorator `name` |
| `kebab-case` | `acid-base` | File name, import path |
| `camelCase` | `acidBase` | Method name, decorator `name` |
| `UPPER_SNAKE_CASE` | `ACID_BASE` | Constant prefixes |

## Instructions

1. **Parse input**: extract:
   - **First argument** (required): path to the IVP file. Verify the file exists and has an `.ivp` extension.
   - **Second argument** (optional): path to a PNG file (icon). Verify the file exists and has a `.png` extension if provided.

2. **Read the IVP file**:
   - Extract the model name from the `#name:` block (e.g., `#name: Acid Base` → `Acid Base`).
   - Extract the model description from the `#description:` block, if present.
   - Read the entire file content as a raw string (it will be used as the equations constant).

3. **Generate TS file**: create `src/demos/<kebab-case>.ts` with the following content:
   ```ts
   import {LINK} from '../ui-constants';
   import {ModelInfo} from '../model';

   export const <UPPER_SNAKE_CASE>_MODEL = `<entire IVP file content>`;

   const UI_OPTS = {
     inputsTabDockRatio: 0.17,
     graphsDockRatio: 0.85,
   };

   const INFO = `# Model
   <model-description or remove this line if not available>
   # Try
   Interactive results based on input changes.
   # Performance
   Nonlinear systems of differential equations are solved within milliseconds.
   # No-code
   [Diff Studio](${LINK.DIF_STUDIO})
   enables the creation of complex models without writing code.
   # Learn more
   * [Sensitivity analysis](${LINK.SENS_AN})
   * [Parameter optimization](${LINK.FITTING})`;

   export const <UPPER_SNAKE_CASE>_MODEL_INFO: ModelInfo = {
     equations: <UPPER_SNAKE_CASE>_MODEL,
     uiOptions: UI_OPTS,
     info: INFO,
   };
   ```

   > **Note**: when embedding the IVP file content inside a template literal, escape any backticks (`` ` ``) and `${` sequences found in the file.

4. **Update the package file** `src/package.ts`:

   a. **Add import** for use in the class method:
   ```ts
   import {<UPPER_SNAKE_CASE>_MODEL_INFO} from './demo/<kebab-case>';
   ```

   b. **Add method** to the `PackageFunctions` class (in alphabetical order among existing model methods):
   ```ts
   @grok.decorators.model({
     name: '<Original model name from IVP>',
     description: '<model-description>',
     icon: '<path-to-png-file>',
   })
   static async <camelCase>(): Promise<void> {
     const model = new Model(<UPPER_SNAKE_CASE>_MODEL_INFO);
     await model.run();
   }
   ```

   - Omit `description` from the decorator if no description was found in the IVP file.
   - Omit `icon` from the decorator if no PNG file was provided.

## Example

Given: `src/ivp/acid-base.ivp` with content:
```
#name: Acid Base
#description: Acid-base equilibrium model
...
```

And optional PNG: `images/acid-base.png`

**Generated file** `src/demo/acid-base.ts`:
```ts
import {LINK} from '../ui-constants';
import {ModelInfo} from '../model';

export const ACID_BASE_MODEL = `#name: Acid Base
#description: Acid-base equilibrium model
...`;

// ... UI_OPTS, INFO, and ACID_BASE_MODEL_INFO as described above
```

**In `src/package.ts`**:
```ts
import {ACID_BASE_MODEL_INFO} from './demo/acid-base';

// Inside PackageFunctions:
@grok.decorators.model({
  name: 'Acid Base',
  description: 'Acid-base equilibrium model',
  icon: 'images/acid-base.png',
})
static async acidBase(): Promise<void> {
  const model = new Model(ACID_BASE_MODEL_INFO);
  await model.run();
}
```