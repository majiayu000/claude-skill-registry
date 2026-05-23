---
name: create-script-handler
description: Create a custom script handler for an unsupported scripting language in Datagrok
---

# Create Script Handler

Help the user register a custom script handler so Datagrok can run scripts in a language not natively supported.

## Usage
```
/create-script-handler [language-name] [--package <package-name>]
```

## Instructions

### 1. Define the handler function

Create a TypeScript function that accepts a `DG.FuncCall` and executes the script, setting output parameters on completion:

```typescript
export async function myLanguageHandler(call: DG.FuncCall): Promise<void> {
  // Read input parameters from call.inputs
  // Execute the script (e.g., via WebAssembly or a Docker container)
  // Set output parameters on call.outputs
}
```

The implementation can use any execution strategy: WebAssembly, a Docker container, a remote API, etc.

### 2. Add mandatory annotations

Place these multi-line comments above the function declaration:

```typescript
//tags: scriptHandler
//meta.scriptHandler.language: clojure
//meta.scriptHandler.extensions: clj,cljs,cljr
//meta.scriptHandler.commentStart: ;
//input: funccall scriptCall
export async function clojureScriptHandler(call: DG.FuncCall): Promise<void> {
  // implement handler
}
```

#### Mandatory annotations

| Annotation                        | Description                                              |
|-----------------------------------|----------------------------------------------------------|
| `tags: scriptHandler`             | Marks the function as a script handler for registration  |
| `meta.scriptHandler.language`     | Language name (shown in UI when creating scripts)        |
| `meta.scriptHandler.extensions`   | Comma-separated file extensions (e.g., `py`, `js`, `clj,cljs,cljr`) |
| `input: funccall scriptCall`      | The handler must accept exactly one input of type `funccall` |

#### Optional annotations

| Annotation                              | Description                                                    |
|-----------------------------------------|----------------------------------------------------------------|
| `meta.scriptHandler.templateScript`     | Template code added to newly created scripts in this language  |
| `meta.scriptHandler.codeEditorMode`     | CodeMirror editor mode for syntax highlighting ([available modes](https://codemirror.net/5/mode/)) |
| `meta.icon`                             | Path to icon inside package files, used in UI for all scripts of this language |
| `meta.scriptHandler.vectorizationFunction` | Function in form `<namespace>:<function name>` for vectorizing `DG.Script`. Accepts `DG.Script`, returns string with vectorized code. |
| `meta.scriptHandler.commentStart`       | Comment character(s) for the language (e.g., `;` for Clojure, `#` for Python) |

### 3. Publish the package

Build and publish the package:

```shell
webpack
grok publish dev
```

After publishing, the language appears in the script creation UI. The platform recognizes scripts with a matching `language` annotation and routes them to this handler.

### Complete example

```typescript
import * as DG from 'datagrok-api/dg';

//tags: scriptHandler
//meta.scriptHandler.language: clojure
//meta.scriptHandler.extensions: clj,cljs,cljr
//meta.scriptHandler.commentStart: ;
//meta.scriptHandler.codeEditorMode: clojure
//meta.scriptHandler.templateScript: (println "Hello, World!")
//meta.icon: images/clojure-icon.png
//input: funccall scriptCall
export async function clojureScriptHandler(call: DG.FuncCall): Promise<void> {
  const script = call.inputs['scriptCall'];
  // Execute the Clojure code
  // Set outputs: call.setParamValue('result', value);
}
```

## Behavior

- Ask the user which programming language they want to support.
- Ask for the file extensions associated with that language.
- Determine the execution strategy (WebAssembly, Docker container, remote service, etc.).
- Generate the handler function with all mandatory annotations.
- Add optional annotations (template, icon, editor mode) if the user provides them.
- If Docker execution is needed, suggest also using the `/create-docker-container` skill.
- Ensure the function signature has exactly one `funccall` input parameter.
- Follow project coding conventions: no excessive comments, no curly brackets for one-line if/for, catch/else if on new lines.
