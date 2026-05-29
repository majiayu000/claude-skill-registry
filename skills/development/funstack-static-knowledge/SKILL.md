---
name: funstack-static-knowledge
description: Use this skill when you need information about `@funstack/static` (the React framework your app is built with). What it is even about, API references, best practices, etc.
---

# FUNSTACK Static Knowledge

**FUNSTACK Static** (`@funstack/static`) is a React framework designed to build SPA application that can be deployed as static files to any static hosting service. Its prominent features is support for React Server Components (RSC) which allows optimizing the performance of the application by rendering parts of the UI at build time.

Note that FUNSTACK Static never runs on the server at runtime (except during development). Server Components are rendered at build time into RSC payloads which are then shipped to the client. The client React runtime can then seamlessly render both Client and Server Components into the DOM.

## FUNSTACK Static Entrypoint

FUNSTACk Static is served as a Vite plugin. See your app's `vite.config.ts` file for the current configuration. A typical configuration looks like this:

```ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { funstackStatic } from "@funstack/static";

export default defineConfig({
  plugins: [
    react(),
    funstackStatic({
      root: "./src/Root.tsx",
      app: "./src/App.tsx",
    }),
  ],
});
```

**Entrypoint.** Here, the `root` option points to the Root component of your application which is responsible for the HTML shell of your application. The `app` option points to the main App component which is the entrypoint for your application's UI.

**Server and Client Components.** The entrypoint components (Root and App) are **server components**. FUNSTACK Static follows React's conventions for Server and Client Components; the entrypoint is executed as a Server module. Modules marked with the `"use client"` directive are executed as Client modules. Server modules can import both Server and Client modules, while Client modules can only import other Client modules.

**Server Actions.** Note that Server Actions (`"use server"`) are **NOT** supported in FUNSTACK Static, as there is no server runtime deployed.

## FUNSTACK Static Docs

More detailed documentation about FUNSTACK Static (including API references and best practices) can be found inside `node_modules` at:

```
node_modules/@funstack/static/dist/docs/index.md
```
