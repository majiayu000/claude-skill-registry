---
name: create-custom-view
description: Create a custom view for Datagrok by extending ViewBase
argument-hint: "[view-name] [package-path]"
---

# Create Custom View

Create a custom view for the Datagrok platform that can be opened via URL, saved in projects, and added to navigation.

## Usage

```
/create-custom-view [view-name] [package-path]
```

## Instructions

When this skill is invoked, help the user create a custom view by extending `DG.ViewBase`.

### Step 1: Create the view class

Create a new file in the package's `src/` directory (e.g., `src/my-view.ts`).

The class must extend `DG.ViewBase` and implement:

- `get type()` - view type identifier string
- `get name()` - display name
- `get path()` - URL path for the view (used for routing)
- `get helpUrl()` (optional) - link to help page
- `getIcon()` (optional) - returns an HTMLElement for the view icon
- `saveStateMap()` / `loadStateMap(stateMap)` - state serialization for project saving
- `handlePath(path)` - restore view from a URL path
- `acceptsPath(path)` - return true if this view handles the given URL path

```ts
export class MyView extends DG.ViewBase {
  private TYPE = 'MyView';
  private PATH = '/myview';

  constructor(params: any, path: string) {
    super(params, path);
    this.TYPE = 'MyView';
    this.PATH = '/myview';
  }

  get type() { return this.TYPE; }
  get helpUrl() { return '/help/path/to/help.md'; }
  get name() { return 'My View'; }
  get path() { return `${this.PATH}/${this.viewId}`; }

  getIcon(): HTMLElement {
    let img = document.createElement('img');
    img.src = '/images/entities/my-icon.png';
    img.height = 18;
    img.width = 18;
    return img;
  }

  // State serialization for project saving
  saveStateMap(): Record<string, any> { return {'viewId': this.viewId}; }
  loadStateMap(stateMap: Record<string, any>) { this.open(stateMap['viewId']); }

  // URL routing
  handlePath(path: string) {
    let id = path.replace(`${this.PATH}/`, '');
    this.open(id);
  }

  acceptsPath(path: string): boolean { return path.startsWith(this.PATH); }
}
```

### Step 2: Register the view

Add a factory function in `package.ts` with the `view` tag:

```ts
//name: My View
//description: Creates a My View
//input: map params
//input: string path
//tags: view
//output: view result
export function myView(params: any = null, path: string = '') {
  return new MyView(params, path);
}
```

The registration rules:
- Must have the `view` tag
- Must accept `params` (map) and `path` (string) inputs
- Must return output of type `view`

### Step 3: Build and populate the view

Add UI content to the view in the constructor or an `open()` method:

```ts
this.root.appendChild(ui.divText('Hello from My View!'));
this.root.appendChild(ui.button('Click me', () => grok.shell.info('Clicked')));
```

For ad-hoc views (quick prototyping without a class):

```ts
let view = grok.shell.newView('My Quick View', [ui.divText('Hi!')]);
```

### Key points

- `saveStateMap` / `loadStateMap` enable saving views as part of a project
- `handlePath` / `acceptsPath` enable URL-based routing (opening views from links)
- The `path` property should return a unique URL that can reconstruct the view state
- For real examples, see the Notebooks package: `public/packages/Notebooks/src/package.js`

## Behavior

1. Ask the user what the view should display if not specified
2. Create the view class with proper state serialization and URL routing
3. Register the view factory function in `package.ts`
4. Add appropriate UI components to the view
5. Ensure imports are correct (`import * as DG from 'datagrok-api/dg'`, `import * as grok from 'datagrok-api/grok'`, `import * as ui from 'datagrok-api/ui'`)
