---
name: build-app
description: Create a Datagrok application with routing, views, and data access
---

# Build a Datagrok Application

Help the user create a full Datagrok application inside a package, with entry points, views, routing, and data access.

## Usage
```
/build-app [app-name] [--in-package <package-name>]
```

## Instructions

### 1. Create or use an existing package

If no package exists yet:
```shell
grok create <PackageName>
cd <PackageName>
npm install
```

Add an app to the package:
```shell
grok add app <AppName>
```

### 2. Define the app entry point

Modern Datagrok apps use the `@grok.decorators.app` decorator on a static method:

```typescript
import * as grok from 'datagrok-api/grok';
import * as ui from 'datagrok-api/ui';
import * as DG from 'datagrok-api/dg';

export const _package = new DG.Package();

export class PackageFunctions {
  @grok.decorators.app({
    name: 'MyApp',
    description: 'Description of the app',
    icon: 'images/icons/app-icon.png',
  })
  static myApp(
    @grok.decorators.param({options: {'meta.url': true, 'optional': true}}) path?: string
  ): void {
    // App initialization logic
  }
}
```

The `meta.url` parameter captures the URL path after the app name, enabling routing.

### 3. Add navigation with AppTreeBrowser

For apps with multiple views, define a tree browser linked to the app:

```typescript
@grok.decorators.appTreeBrowser({app: 'MyApp'})
static async myAppTreeBrowser(treeNode: DG.TreeViewGroup): Promise<void> {
  treeNode.item('Home').onSelected.subscribe((_) => { /* show home view */ });
  const dataGroup = treeNode.group('Data');
  dataGroup.item('View 1').onSelected.subscribe((_) => { /* show view 1 */ });
  dataGroup.item('View 2').onSelected.subscribe((_) => { /* show view 2 */ });
}
```

### 4. Build the main view

Most apps start with a custom view or a table view:

```typescript
// Custom view
const view = DG.View.create();
view.name = 'My App';
view.root.appendChild(ui.divV([
  ui.h1('Welcome'),
  ui.divText('App content here')
]));
grok.shell.addView(view);

// Table view with data
const df = await grok.data.demo.demog(100);
const tv = grok.shell.addTableView(df);
tv.addViewer('Scatter plot');
```

Use `ui.splitH` / `ui.splitV` for layout composition.

### 5. App URLs and launching

- Single app in package: `https://<host>/apps/<APP_NAME>`
- Multiple apps in package: `https://<host>/apps/<PACKAGE_NAME>/<APP_NAME>`
- Users find apps in `Functions | Apps` in the sidebar.

### 6. Data access patterns

**Database queries:**
```typescript
const result = await grok.data.query('PackageName:QueryName', {param1: 'value'});
```

**REST endpoints (with CORS proxy):**
```typescript
const response = await grok.dapi.fetchProxy('https://api.example.com/data');
```

**User data storage (persist settings):**
```typescript
await grok.dapi.userDataStorage.postValue('storeName', 'key', 'value');
const val = await grok.dapi.userDataStorage.getValue('storeName', 'key');
```

### 7. Build and publish

```shell
npm run build
grok publish dev
```

## Behavior

- Ask for the app name and purpose if not clear from the request.
- Default to TypeScript with decorator-based entry points.
- When the user asks about routing, explain the `meta.url` parameter pattern.
- When the user needs data access, guide them to the appropriate pattern (database query, REST proxy, file share).
- Follow Datagrok coding conventions: no excessive comments, no curly brackets for one-line if/for, catch/else-if on new line.
- Suggest `AppTreeBrowser` for apps that need multi-view navigation.
- Remind the user to configure server keys via `grok config` if they haven't published before.
