---
description: Documentation view expert for Docusaurus integration. Launches interactive server for SpecWeave living documentation with hot reload, auto-generated sidebar, and Mermaid diagrams. Works in ANY SpecWeave project with auto-setup. Supports both internal (port 3015) and public (port 3016) docs. Activates for preview docs, view documentation, Docusaurus server, docs UI, documentation website, local docs server, hot reload docs, static site build.
---

# Documentation View Skill

Expert in launching and managing Docusaurus documentation server for SpecWeave projects.

## What I Do

I help you view your SpecWeave living documentation with Docusaurus:

### Key Features
- **Zero-config setup** - Works in any SpecWeave project automatically
- **Internal & Public docs** - Internal on port 3015, public on port 3016
- **Cached installation** - Docusaurus cached in `.specweave/cache/docs-site/` (gitignored)
- **Hot reload** - Edit markdown, see changes instantly
- **Mermaid diagrams** - Architecture diagrams render beautifully
- **Auto sidebar** - Generated from folder structure
- **Bypasses private registries** - Uses public npm to avoid Azure DevOps/corporate issues

## How It Works

1. **First run (~30 seconds)**:
   - Creates Docusaurus in `.specweave/cache/docs-site/` (internal) or `.specweave/cache/docs-site-public/` (public)
   - Installs dependencies from public npm registry
   - Configures to read from `.specweave/docs/internal/` or `.specweave/docs/public/`

2. **Subsequent runs (instant)**:
   - Uses cached installation
   - Starts server immediately

## Available Commands

### View Internal Documentation (Default)
```bash
/sw-docs:view
```

**What it does:**
1. Checks if `.specweave/docs/internal/` exists
2. Runs pre-flight validation (auto-fixes common issues)
3. Sets up Docusaurus in cache (if first run)
4. Starts dev server on **http://localhost:3015**
5. Enables hot reload

### View Public Documentation
```bash
/sw-docs:view --public
```

**What it does:**
1. Checks if `.specweave/docs/public/` exists
2. Runs pre-flight validation (auto-fixes common issues)
3. Sets up Docusaurus in cache (if first run)
4. Starts dev server on **http://localhost:3016**
5. Enables hot reload

### Build Static Site
```bash
/sw-docs:build
```

**What it does:**
1. Builds production-ready static site
2. Outputs to `.specweave/cache/docs-site/build/`
3. Ready for deployment to any static host

## When to Use This Skill

### Activate for:
- "View my documentation"
- "Preview my docs"
- "Show me my docs in a browser"
- "Launch Docusaurus"
- "View my living documentation"
- "Start docs server"
- "I want to see my internal docs"
- "View public docs"

### Workflow

```
User: "I want to preview my docs"
You: "I'll launch the documentation view server."
     [Run: /sw-docs:view]
```

```
User: "Show me my public documentation"
You: "I'll launch the public documentation server."
     [Run: /sw-docs:view --public]
```

## Port Reference

| Docs Type | Port | Path |
|-----------|------|------|
| Internal (default) | 3015 | `.specweave/docs/internal/` |
| Public | 3016 | `.specweave/docs/public/` |

## Troubleshooting

### Port 3015 or 3016 already in use
```bash
# For internal docs
lsof -i :3015 && kill -9 $(lsof -t -i :3015)

# For public docs
lsof -i :3016 && kill -9 $(lsof -t -i :3016)
```

### Reinstall from scratch
```bash
# For internal docs
rm -rf .specweave/cache/docs-site
# Then run /sw-docs:view again

# For public docs
rm -rf .specweave/cache/docs-site-public
# Then run /sw-docs:view --public again
```

### npm registry issues
The setup explicitly uses `--registry=https://registry.npmjs.org` to bypass private/corporate registry configurations.

## See Also

- `/sw-docs:build` - Build static site for deployment
- `/sw-docs:organize` - Organize large folders with themed indexes
- `/sw-docs:health` - Documentation health report
- `/sw-docs:validate` - Validate documentation before viewing
