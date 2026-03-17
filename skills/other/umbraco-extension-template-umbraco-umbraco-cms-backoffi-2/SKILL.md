---
name: umbraco-extension-template
description: Create new Umbraco backoffice extensions using the official dotnet template
version: 1.0.0
location: managed
allowed-tools: Read, Write, Edit, WebFetch, Bash
---

# Umbraco Extension Template

## What is it?
The Umbraco Extension Template is the official .NET template for creating backoffice extensions. It provides a pre-configured project structure with TypeScript/Vite tooling, proper folder structure, and all essential files needed for extension development. Every Umbraco backoffice extension should start with this template.

## Documentation
Always fetch the latest docs before implementing:

- **Main docs**: https://docs.umbraco.com/umbraco-cms/customizing/development-flow/umbraco-extension-template
- **Development Flow**: https://docs.umbraco.com/umbraco-cms/customizing/development-flow
- **Foundation**: https://docs.umbraco.com/umbraco-cms/customizing/foundation

## Prerequisites

- .NET SDK 9.0 or later
- Node.js 22 or later

## Workflow

1. **Install template** (one-time): `dotnet new install Umbraco.Templates`
2. **Create extension**: `dotnet new umbraco-extension -n MyExtension`
3. **Install dependencies**: `cd MyExtension/Client && npm install`
4. **Start development**: `npm run watch`
5. **Build for production**: `npm run build`

## Commands

### Install the Template
```bash
dotnet new install Umbraco.Templates
```

### Create New Extension (Basic)
```bash
dotnet new umbraco-extension -n MyExtension
```

### Create New Extension (With Examples)
```bash
dotnet new umbraco-extension -n MyExtension -ex
```
The `-ex` flag adds example code including:
- Sample API controller
- Swagger API registration
- Example dashboard component
- Generated API client

## Project Structure

### Basic Template
```
MyExtension/
├── MyExtension.csproj        # .NET project file
├── Constants.cs              # Extension constants
├── README.md                 # Setup instructions
└── Client/                   # TypeScript source
    ├── package.json
    ├── tsconfig.json
    ├── vite.config.ts
    └── src/
        └── ...               # Your extension code
```

### With Examples (-ex flag)
```
MyExtension/
├── MyExtension.csproj
├── Constants.cs
├── README.md
├── Composers/                # C# composers
│   └── SwaggerComposer.cs    # API documentation setup
├── Controllers/              # C# API controllers
│   └── MyExtensionController.cs
└── Client/
    ├── package.json
    ├── tsconfig.json
    ├── vite.config.ts
    └── src/
        ├── api/              # Generated API client
        ├── dashboards/       # Example dashboard
        └── entrypoints/      # Extension entry point
```

## Development Commands

```bash
# Navigate to Client folder
cd MyExtension/Client

# Install dependencies
npm install

# Development with hot reload
npm run watch

# Production build
npm run build

# Type checking
npm run check
```

## Build and Deploy

### Publish the Extension
```bash
dotnet publish --configuration Release
```

### Create NuGet Package
```bash
dotnet pack --configuration Release
```

## Minimal Example

After running the template, add your first manifest in `Client/src/`:

### manifest.ts
```typescript
export const manifests: Array<UmbExtensionManifest> = [
  {
    name: "My Extension Entrypoint",
    alias: "MyExtension.Entrypoint",
    type: "backofficeEntryPoint",
    js: () => import("./entrypoint.js"),
  },
];
```

### entrypoint.ts
```typescript
import type { UmbEntryPointOnInit } from "@umbraco-cms/backoffice/extension-api";

export const onInit: UmbEntryPointOnInit = (_host, _extensionRegistry) => {
  console.log("Extension loaded!");
};
```

## IMPORTANT: Add Extension to Umbraco Instance

After creating a new extension, you **MUST** add it as a project reference to the main Umbraco instance. Without this step, the extension will not load.

**Reference skill: `umbraco-add-extension-reference`**

This skill explains how to add the new extension's `.csproj` file as a `<ProjectReference>` in the main Umbraco project (e.g., `Umbraco-CMS.Skills.csproj`).

## Related Skills

After creating your extension, use these skills to add functionality:

- **Sections**: Reference skill: `umbraco-sections`
- **Dashboards**: Reference skill: `umbraco-dashboard`
- **Menus**: Reference skill: `umbraco-menu`
- **Workspaces**: Reference skill: `umbraco-workspace`
- **Trees**: Reference skill: `umbraco-tree`

For complete extension blueprints with working examples:
- Reference skill: `umbraco-backoffice`

That's it! Always fetch fresh docs, use the template to scaffold, add the project reference, then add extension types as needed.
