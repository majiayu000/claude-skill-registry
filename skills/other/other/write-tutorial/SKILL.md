---
name: write-tutorial
description: Create a Tutorial class with interactive steps, track assignment, and registration for Datagrok
---

# Write Tutorial

Help the user create an interactive tutorial that educates users about Datagrok platform features.

## Usage
```
/write-tutorial [tutorial-name] [--package <package-name>] [--track <track-name>]
```

## Instructions

### 1. Install the tutorials library

The package must depend on `@datagrok-libraries/tutorials`:

```shell
npm install @datagrok-libraries/tutorials
```

### 2. Create the Tutorial subclass

Create a TypeScript file (e.g., `src/tutorials/custom-tutorial.ts`) with a class extending `Tutorial`:

```typescript
import {Tutorial} from '@datagrok-libraries/tutorials';

export class CustomTutorial extends Tutorial {
  get name(): string { return 'Custom Tutorial'; }
  get description(): string { return 'Teaches users about a feature'; }

  protected async _run(): Promise<void> {
    // Define steps using this.action() and helper methods
    // Steps are event-based and can include interactive hints
  }
}
```

Key points:
- Override `name` and `description` getters.
- Implement the `_run` method with a sequence of steps.
- Steps use the `action` method or helper methods that call it internally.
- Steps can include interactive hints and detailed descriptions.

### 3. Register the tutorial in package.ts

Add a registration function with metadata annotations:

```typescript
import {CustomTutorial} from './tutorials/custom-tutorial';

//tags: tutorial
//meta.icon: images/custom-tutorial.png
//meta.name: Custom Tutorial
//meta.track: Test Track
//description: This tutorial illustrates a new feature
//output: object
export function registerTutorial() {
  return new CustomTutorial();
}
```

#### Required annotations

| Annotation  | Description                                                       |
|-------------|-------------------------------------------------------------------|
| `tags`      | Must include `tutorial`                                           |
| `meta.name` | Display name of the tutorial                                      |
| `output`    | Must be `object` (returns a Tutorial instance)                    |

#### Optional annotations

| Annotation    | Description                                                     |
|---------------|-----------------------------------------------------------------|
| `meta.track`  | Track name this tutorial belongs to. If omitted, a new track is created for the package. If an existing track name is used, the tutorial is added to that track (even from another package). |
| `meta.icon`   | Path to icon relative to package root. Default icon used if absent. |
| `description` | Displayed in the tutorial UI. Empty description if absent.       |

### 4. Register a track (optional)

To define a custom track that groups tutorials:

```typescript
import {Track} from '@datagrok-libraries/tutorials';

//tags: track
//help-url: https://datagrok.ai/help
//output: object
//meta.name: Test Track
export function registerTrack() {
  return new Track('Test Track', [], 'https://datagrok.ai/help');
}
```

Track registration annotations:
- `tags: track` (required)
- `meta.name` (required): track display name
- `help-url` (required): link to documentation
- `output: object` (required)

### 5. Control visibility of standard tutorials

The `Tutorials` package provides default tracks (e.g., Exploratory Data Analysis, Data Access). Their visibility can be controlled at the user group level via package settings.

### 6. Build and publish

```shell
webpack
grok publish dev
```

## Behavior

- Ask the user for the tutorial name, description, target package, and which track it should belong to.
- Ask what interactive steps the tutorial should include.
- Generate the Tutorial subclass with `_run` implementation.
- Add the registration function to `package.ts` with correct annotations.
- If the user wants a new track, also generate the track registration function.
- Ensure the `@datagrok-libraries/tutorials` dependency is present in `package.json`.
- Remind the user that without `meta.track`, tutorials get their own package-specific track.
- Follow project coding conventions: no excessive comments, no curly brackets for one-line if/for, catch/else if on new lines.
