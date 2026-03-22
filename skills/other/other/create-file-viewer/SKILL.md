---
name: create-file-viewer
description: Create a custom file viewer for Datagrok file share browser
argument-hint: "[extensions] [package-path]"
---

# Create File Viewer

Create a custom file viewer that is used by the Datagrok file share browser to display files with specific extensions.

## Usage

```
/create-file-viewer [extensions] [package-path]
```

## Instructions

When this skill is invoked, help the user create a custom file viewer for one or more file extensions.

### Step 1: Create the viewer function

Add a function to `package.ts` (or a separate file imported by it) with the correct annotations. The function must:

- Accept a single `file` input
- Return a `view`
- Have the `fileViewer` tag plus a `fileViewer-<ext>` tag for each supported extension

```ts
//name: myFileViewer
//tags: fileViewer, fileViewer-xyz, fileViewer-abc
//input: file file
//output: view v
export function myFileViewer(file: DG.FileInfo) {
  let view = DG.View.create();

  // Read file content and render it
  file.readAsString().then((content) => {
    let host = ui.div([]);
    // Process and display content
    host.innerText = content;
    view.append(host);
  });

  return view;
}
```

### Step 2: Handle file content

Choose the appropriate method to read file content:

- `file.readAsString()` - for text-based files (returns `Promise<string>`)
- `file.readAsBytes()` - for binary files (returns `Promise<Uint8Array>`)

Example for binary files:

```ts
//tags: fileViewer, fileViewer-mol, fileViewer-sdf, fileViewer-cif
//input: file file
//output: view v
export function structureViewer(file: DG.FileInfo) {
  let view = DG.View.create();
  let host = ui.div([], 'd4-ngl-viewer');

  file
    .readAsBytes()
    .then(bytes => {
      // Process binary content
      let blob = new Blob([bytes]);
      // Render blob...
    });

  view.append(host);
  return view;
}
```

### Step 3: Build and publish

```bash
npm run build
grok publish
```

Once the package is published, Datagrok automatically uses the viewer when a user selects a file with a matching extension in the file share browser.

### Key points

- Each supported extension needs its own tag: `fileViewer-mol`, `fileViewer-sdf`, etc.
- The function runs when a user clicks on a file with a matching extension in the file share browser
- The view is displayed in the file preview panel
- Return the view synchronously; load file content asynchronously inside it
- Multiple extensions can be handled by a single function with multiple `fileViewer-<ext>` tags

## Behavior

1. Ask the user which file extension(s) they want to support if not specified
2. Determine whether the file is text-based or binary to choose `readAsString` vs `readAsBytes`
3. Create the viewer function with correct tags for all specified extensions
4. Add rendering logic appropriate for the file type
5. Ensure imports are correct (`import * as DG from 'datagrok-api/dg'`, `import * as ui from 'datagrok-api/ui'`)
