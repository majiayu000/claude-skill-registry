---
name: mcp-doc-add-tool
description: >
  Create a custom MCP tool for the documentation manifest. Guides the user
  through defining the tool's purpose, generating an action script with
  embedded data, computing the hash, and adding it to the manifest.
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion
argument-hint: ""
---

# MCP Doc Add Tool

Guide the user through creating a custom MCP tool for their documentation manifest. Custom tools filter, query, or present documentation in ways specific to the user's project. The generated action script embeds index data and is added to `.mcp/manifest.yml` with a computed SHA-256 hash.

Custom tools are preserved during `/mcp-doc-sync` — they are never overwritten or removed by sync operations.

## Step 1: Load Manifest

Read `.mcp/manifest.yml` from the project root.

If the file does not exist, tell the user:

```
No manifest found at .mcp/manifest.yml.
Run /mcp-doc-init to initialize the documentation manifest first.
```

Stop here if no manifest exists.

Parse the manifest and extract:
- All resource entries (to know what documentation is available for the tool to query)
- All existing tool entries (to detect name collisions and show what already exists)

List the existing tools for context:

```
Existing tools in manifest:
  - search_docs (default)
  - get_applicable_docs (default)
  - get_doc_tree (default)
  - {any custom tools already created}
```

## Step 2: Gather Requirements

Ask the user a series of questions via AskUserQuestion to define the custom tool.

### 2a: Tool name

Ask: "What should the tool be called? Use snake_case (e.g., `get_coding_standards`, `get_team_api_docs`, `list_adrs`)."

Validate:
- Must be snake_case (lowercase letters, digits, underscores only)
- Must not collide with existing tool names in the manifest
- Must not use reserved names: `search_docs`, `get_applicable_docs`, `get_doc_tree`

If the name collides, tell the user and ask for a different name.

### 2b: Tool description

Ask: "Describe what this tool does. Include:
- A one-sentence summary of the tool's purpose
- USE THIS WHEN: when should the AI use this tool? (2-3 bullet points)
- DO NOT USE WHEN: when should the AI use a different tool instead? (1-2 bullet points)"

Example:
```yaml
description: |
  Returns all coding standards and conventions for this project.

  USE THIS WHEN:
  - The user asks about coding standards, conventions, or style rules
  - You need to check project conventions before writing code

  DO NOT USE WHEN:
  - The user asks about a specific file or module (use get_applicable_docs)
```

### 2c: Tool purpose

Ask: "What should this tool return? Choose one or describe your own:"

Present options:
1. **Filter docs by tags** — return only docs matching specific tags (e.g., only docs tagged `standards`, `api`, or `adr`)
2. **Filter docs by scope** — return only docs under a specific directory subtree (e.g., only docs under `packages/auth`)
3. **Custom query with input parameters** — tool accepts input parameters and filters/transforms docs based on them (e.g., accept a `team` parameter and return that team's docs)
4. **Static curated list** — return a fixed set of docs chosen by the user (e.g., a "getting started" reading list)
5. **Other** — let the user describe the behavior

Based on the chosen purpose, determine:
- Which docs from the manifest to embed in the action (the "data subset")
- What input parameters the tool needs
- What filtering/display logic the action script should implement

### 2d: Input parameters

Based on the chosen purpose:

- **Filter by tags (option 1):** No input parameters needed (the tag filter is baked in). Ask the user which tags to filter on.
- **Filter by scope (option 2):** No input parameters needed (the scope is baked in). Ask the user which scope/path to filter on.
- **Custom query (option 3):** Ask the user to define each input parameter:
  - Parameter name (snake_case)
  - Type (string, number, boolean)
  - Description (shown to AI)
  - Required or optional
- **Static list (option 4):** No input parameters. Ask the user to select which docs to include.
- **Other (option 5):** Work with the user to define parameters based on their description.

## Step 3: Generate Action Script

Create the action file at `.mcp/actions/{tool-name}.js` (convert tool name from snake_case to kebab-case for the filename: `get_coding_standards` becomes `get-coding-standards.js`).

The action script must:
- Embed the relevant data subset as a const array
- Export a default async function matching the git-doc-mcp action signature: `export default async function(input, ctx)`
- Return `{ content: [{ type: "text", text: "..." }] }`
- Be marked as editable (unlike default tools)

### Template by purpose type

#### Filter by tags

```js
// Custom tool: {tool_name}
// Created by mcp-doc-add-tool — editable
const DOCS = [
  { name: "docs_coding-standards", path: "docs/coding-standards.md", title: "Coding Standards", description: "Project coding conventions and style guide" },
  { name: "docs_naming-conventions", path: "docs/naming.md", title: "Naming Conventions", description: "Variable, function, and file naming rules" },
  // ... filtered subset of docs matching the chosen tags
];

export default async function(input, ctx) {
  const text = DOCS.map(d =>
    `- **${d.title}** (${d.path})\n  ${d.description}`
  ).join("\n\n");

  return {
    content: [{
      type: "text",
      text: `${DOCS.length} document(s) found:\n\n${text}`
    }]
  };
}
```

#### Filter by scope

```js
// Custom tool: {tool_name}
// Created by mcp-doc-add-tool — editable
const DOCS = [
  { name: "packages_auth_readme", path: "packages/auth/README.md", title: "Auth Package", description: "Authentication and authorization module" },
  { name: "packages_auth_docs_guide", path: "packages/auth/docs/guide.md", title: "Auth Guide", description: "Setup and integration guide for auth" },
  // ... docs scoped to the chosen subtree
];

export default async function(input, ctx) {
  const text = DOCS.map(d =>
    `- **${d.title}** (${d.path})\n  ${d.description}`
  ).join("\n\n");

  return {
    content: [{
      type: "text",
      text: `${DOCS.length} document(s) in scope:\n\n${text}`
    }]
  };
}
```

#### Custom query with input parameters

```js
// Custom tool: {tool_name}
// Created by mcp-doc-add-tool — editable
const DOCS = [
  // ... relevant docs with team/tag/scope metadata
  { name: "packages_auth_readme", path: "packages/auth/README.md", title: "Auth Package", description: "...", team: "platform" },
  { name: "packages_billing_readme", path: "packages/billing/README.md", title: "Billing Package", description: "...", team: "payments" },
];

export default async function(input, ctx) {
  const team = (input.team || "").toLowerCase();
  if (!team) {
    return { content: [{ type: "text", text: "Please provide a team name." }] };
  }

  const filtered = DOCS.filter(d => d.team === team);
  if (filtered.length === 0) {
    return { content: [{ type: "text", text: `No documentation found for team "${team}".` }] };
  }

  const text = filtered.map(d =>
    `- **${d.title}** (${d.path})\n  ${d.description}`
  ).join("\n\n");

  return {
    content: [{
      type: "text",
      text: `${filtered.length} document(s) for team "${team}":\n\n${text}`
    }]
  };
}
```

#### Static curated list

```js
// Custom tool: {tool_name}
// Created by mcp-doc-add-tool — editable
const DOCS = [
  { name: "root_readme", path: "README.md", title: "Project Overview", description: "Start here for project overview and setup" },
  { name: "docs_architecture", path: "docs/architecture.md", title: "Architecture", description: "System architecture and design decisions" },
  { name: "docs_contributing", path: "CONTRIBUTING.md", title: "Contributing Guide", description: "How to contribute to this project" },
  // ... user-selected docs in their preferred order
];

export default async function(input, ctx) {
  const text = DOCS.map((d, i) =>
    `${i + 1}. **${d.title}** (${d.path})\n   ${d.description}`
  ).join("\n\n");

  return {
    content: [{
      type: "text",
      text: `Recommended reading order:\n\n${text}`
    }]
  };
}
```

Adapt the template to the user's specific requirements. The examples above are starting points — the actual embedded data and logic should match what the user described.

## Step 4: Compute Hash

After writing the action file, compute its SHA-256 hash:

```bash
sha256sum .mcp/actions/{tool-name}.js | awk '{print "sha256:" $1}'
```

Store the computed hash for use in the manifest entry.

## Step 5: Update Manifest

Add the tool entry to `.mcp/manifest.yml`. Insert it after the existing tool entries.

```yaml
  - name: {tool_name}
    title: "{short human-readable title}"
    description: "{user-provided description with USE THIS WHEN / DO NOT USE WHEN}"
    inputSchema:
      type: object
      properties:
        {param_name}:
          type: {param_type}
          description: "{param_description}"
      required: [{required_params}]
    action: ./actions/{tool-name}.js
    actionHash: sha256:{computed-hash}
    annotations:
      readOnlyHint: true
```

If the tool has no input parameters (filter by tags, filter by scope, static list), use an empty properties object:

```yaml
    inputSchema:
      type: object
      properties: {}
```

## Step 6: Custom Tool Preservation

Custom tools are identified by name. The three default tools are:
- `search_docs`
- `get_applicable_docs`
- `get_doc_tree`

Any tool with a different name is considered custom. The `/mcp-doc-sync` skill will:
- **NOT** overwrite custom tool action files
- **NOT** modify custom tool manifest entries
- **NOT** remove custom tools from the manifest
- **NOT** recalculate custom tool hashes

If the user needs to update a custom tool's embedded data after docs change, they should either:
- Edit the action file manually (it is marked "editable")
- Run `/mcp-doc-add-tool` again to recreate it
- Delete the old tool entry from the manifest and action file, then recreate

## Step 7: Report

Present what was created:

```
Custom tool created: {tool_name}

Action file: .mcp/actions/{tool-name}.js
Manifest:    .mcp/manifest.yml (tool entry added)
Hash:        sha256:{hash}

The tool is now available via the {project-name}-docs MCP server.

To test: restart the MCP server and invoke the tool.

To edit: modify .mcp/actions/{tool-name}.js directly.
         The file is marked "editable" — it will not be overwritten by /mcp-doc-sync.
         After editing, recompute the hash:
           sha256sum .mcp/actions/{tool-name}.js | awk '{print "sha256:" $1}'
         Then update the actionHash in .mcp/manifest.yml.

To delete: remove the tool entry from .mcp/manifest.yml and delete .mcp/actions/{tool-name}.js.
```
