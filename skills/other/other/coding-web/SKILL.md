---
name: coding-web
cluster: coding
description: "Web coding meta: JS/TS/Node for full-stack development"
tags: ["web","fullstack","coding"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "web fullstack javascript typescript node coding"
---

# coding-web

## Purpose
This skill enables OpenClaw to assist with full-stack web development using JavaScript, TypeScript, and Node.js, focusing on generating, debugging, and optimizing code for web applications.

## When to Use
Use this skill when building or maintaining web projects involving frontend (e.g., React, Vue) and backend (e.g., Node.js servers), especially for tasks like scaffolding apps, fixing bugs in JS/TS code, or integrating APIs. Apply it in iterative development cycles, such as rapid prototyping or migrating legacy code to modern standards.

## Key Capabilities
- Generate boilerplate for Node.js servers: Use to create Express apps with routes, e.g., output a server.js file.
- Handle TypeScript conversions: Convert JS to TS, ensuring type safety; for example, add interfaces to existing functions.
- Optimize frontend code: Minify and bundle JS/TS assets; invoke with parameters to target specific frameworks like React.
- Debug common web errors: Identify and suggest fixes for issues like CORS in Node.js or state management in React components.
- Integrate with databases: Generate code for MongoDB or SQL connections in Node.js, using async/await patterns.
- Code snippets: For a simple React component, OpenClaw might output: `import React from 'react'; const MyComponent = () => <div>Hello</div>; export default MyComponent;`

## Usage Patterns
To invoke this skill, prefix commands with `openclaw coding-web` in your terminal or integrate via OpenClaw's API. Always specify the subcommand first (e.g., `generate`, `debug`), followed by options like `--language ts` or `--framework react`. For API calls, use POST requests to `/api/coding-web/execute` with a JSON payload containing `{ "action": "generate", "params": { "type": "component", "name": "UserForm" } }`. Set environment variables for authentication, e.g., export `$OPENCLAW_API_KEY` before running commands. Chain skills by piping outputs, like using output from a database skill as input here.

## Common Commands/API
- CLI Command: `openclaw coding-web generate --type server --framework express --port 3000` – Creates a basic Express server; add `--language ts` for TypeScript.
- CLI Command: `openclaw coding-web debug --file app.js --issue "undefined variable"` – Analyzes and patches errors in the specified file.
- API Endpoint: POST to `/api/coding-web/generate` with body `{ "codeType": "component", "language": "ts", "details": { "name": "Login", "props": ["username"] } }` – Returns generated code as JSON.
- Config Format: Use a JSON config file, e.g., `{ "defaultLanguage": "ts", "framework": "react", "apiKey": "$OPENCLAW_API_KEY" }`, placed in `.openclaw/config.json`.
- Code Snippet: For API response handling: `const response = await fetch('/api/coding-web/generate', { method: 'POST', body: JSON.stringify({ action: 'generate' }) }); const code = await response.json();`
- Authentication: Always include `$OPENCLAW_API_KEY` in headers for API calls, e.g., `headers: { 'Authorization': `Bearer ${process.env.OPENCLAW_API_KEY}` }`.

## Integration Notes
Integrate this skill with IDEs like VS Code by adding it to your extensions or using OpenClaw's plugin system; install via `npm install openclaw-vscode`. For CI/CD, embed in scripts like GitHub Actions: `run: openclaw coding-web generate --type test --file src/app.js`. Handle dependencies by specifying Node.js versions in package.json, e.g., `"engines": { "node": ">=14" }`. If using with other tools, export generated code as modules: `module.exports = generatedCode;`. Ensure your environment has Node.js installed; check with `node -v` before invoking.

## Error Handling
When errors occur, check the exit code from CLI commands (e.g., code 1 for failures) and parse JSON error responses from APIs, which include fields like `{ "error": "Invalid params", "details": "Missing --type flag" }`. For common issues, retry with corrected inputs, e.g., if a generation fails due to missing dependencies, run `npm install express` first. Use try-catch in code snippets: `try { await openclawAPI.call('coding-web', { action: 'generate' }); } catch (e) { console.error(e.message); // e.g., "API key required" }`. If authentication fails (e.g., 401 status), verify `$OPENCLAW_API_KEY` is set and not expired.

## Concrete Usage Examples
1. **Example 1: Generate a Node.js Express Server**  
   Use: `openclaw coding-web generate --type server --framework express --language js`  
   This creates a basic server file: `const express = require('express'); const app = express(); app.listen(3000, () => console.log('Server running'));`  
   Then, run it with `node server.js` to start the server on port 3000.

2. **Example 2: Debug and Fix a TypeScript React Component**  
   Use: `openclaw coding-web debug --file MyComponent.tsx --issue "Type error in props"`  
   It might output a fixed snippet: `interface Props { name: string; } const MyComponent: React.FC<Props> = ({ name }) => <div>{name}</div>;`  
   Integrate by copying the output into your project and rebuilding with `tsc`.

## Graph Relationships
- Related to: "coding-backend" (shares Node.js capabilities)
- Depends on: "tools-node" (for Node.js runtime access)
- Connected to: "web-frontend" (for frontend-specific tasks like React/Vue)
- Overlaps with: "fullstack-dev" (in cluster "coding" for broader development)
