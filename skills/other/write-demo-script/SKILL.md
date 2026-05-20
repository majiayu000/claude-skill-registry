---
name: write-demo-script
description: Create a DemoScript with steps, registration, and demoPath for the Datagrok demo application
---

# Write Demo Script

Help the user create a demo script that demonstrates step-by-step functionality in the Datagrok demo application.

## Usage
```
/write-demo-script [script-name] [--package <package-name>]
```

## Instructions

### 1. Install the tutorials library

The package must depend on `@datagrok-libraries/tutorials`:

```shell
npm install @datagrok-libraries/tutorials
```

### 2. Create the DemoScript class

Create a TypeScript file (e.g., `src/demo-app/demo-script.ts`) with a function that initializes and runs the demo:

```typescript
import {DemoScript} from '@datagrok-libraries/tutorials';

export function demo() {
  const demoScript = new DemoScript(
    'Script Name',        // name (required)
    'Script description', // description (required)
    true,                 // isAutomatic: true = auto-advance, false = manual
    {
      autoStartFirstStep: true,  // optional: auto-start first step in manual mode
      path: 'Category/Demo'      // optional: breadcrumb path in the view
    }
  );

  demoScript
    .step('Step 1', async () => {
      grok.shell.addTableView(grok.data.demo.demog());
    }, {description: 'Opens the demographics dataset.', delay: 2000})
    .step('Step 2', async () => {
      grok.shell.addTableView(grok.data.testData('biosensor'));
    }, {description: 'Opens the biosensor dataset.', delay: 2000})
    .step('Final step', async () => console.log('Finished'));

  return demoScript.start();
}
```

#### Step parameters

Each `.step()` call takes:
- `name` (string, required): step display name
- `func` (async function, required): the action to perform
- Options object (optional):
  - `description` (string): text shown to the user during this step
  - `delay` (number): milliseconds to wait before advancing (for automatic scripts)

### 3. Register the demo script in package.ts

Add a function with the required metadata annotations to `package.ts`:

```typescript
import {demo} from './demo-app/demo-script';

//name: Demo script
//description: Illustrates the work of the demo script
//meta.demoPath: Category | Subcategory | Script Name
//meta.isDemoScript: True
export function demoScript() {
  return new demo();
}
```

#### Required annotations

| Annotation         | Description                                                  |
|--------------------|--------------------------------------------------------------|
| `meta.demoPath`    | Path in the demo app, separated by ` \| `. Without this, the script will NOT appear in the demo application. |
| `meta.isDemoScript`| Must be `True`. Without this, the script won't render as a demo script with a dedicated view. |

#### Optional annotations

| Annotation    | Description                                          |
|---------------|------------------------------------------------------|
| `description` | Tooltip text shown in the demo application UI        |

### 4. Build and publish

```shell
webpack
grok publish dev
```

## Behavior

- Ask the user for the demo script name, description, and which package it belongs to.
- Ask what steps the demo should include and whether it should be automatic or manual.
- Generate the DemoScript file with properly structured steps.
- Add the registration function to `package.ts` with the correct `meta.demoPath` and `meta.isDemoScript` annotations.
- Use the pipe separator ` | ` in `meta.demoPath` (e.g., `Viewers | Charts | My Demo`).
- Ensure the `@datagrok-libraries/tutorials` dependency is present in `package.json`.
- Follow project coding conventions: no excessive comments, no curly brackets for one-line if/for, catch/else if on new lines.
