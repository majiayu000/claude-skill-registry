---
name: create-odoo-pwa
description: Generate an offline-first Progressive Web App with Odoo Studio backend integration. Use when user wants to create new Odoo-backed application, mentions "PWA with Odoo", "offline Odoo app", "Odoo Studio PWA", or similar terms. Supports SvelteKit, React, and Vue frameworks.
allowed-tools: Read, Write, Glob, Bash
---

# Create Odoo PWA Application

Generate a production-ready Progressive Web App with Odoo Studio backend, featuring offline-first architecture, smart caching, and automatic synchronization.

## Before You Start

This skill generates a complete PWA project following proven architectural patterns:
- **Three-layer data flow**: Component → Cache Store → API Client → Server Route → Odoo
- **Offline-first**: IndexedDB/localStorage with background sync
- **Smart caching**: Incremental fetch, stale detection, optimistic updates
- **PWA-ready**: Service workers, manifest, installable

## Required User Input

Ask the user for the following information before generating:

1. **Project name** (required)
   - Format: kebab-case (e.g., "inventory-tracker", "expense-manager")
   - Used for directory name and package.json

2. **Framework** (required)
   - Options: `sveltekit` (recommended), `react`, `vue`
   - Default: sveltekit if not specified

3. **Primary Odoo model** (required)
   - The main custom model name WITHOUT the `x_` prefix
   - Example: If Odoo model is `x_inventory`, user provides: `inventory`
   - Will automatically add `x_` prefix in code

4. **Model display name** (required)
   - Human-readable singular name (e.g., "Inventory Item", "Expense")

5. **Deployment target** (optional)
   - Options: `vercel`, `github-pages`, `cloudflare`, `netlify`
   - Default: vercel if not specified

## Generation Steps

### Step 1: Project Initialization

Create the project directory and initialize the structure:

```bash
mkdir {{PROJECT_NAME}}
cd {{PROJECT_NAME}}
```

Generate the appropriate structure based on framework:
- **SvelteKit**: Use SvelteKit 2.x structure with `src/` directory
- **React**: Use Vite + React structure
- **Vue**: Use Vite + Vue structure

### Step 2: Base Configuration Files

Generate these files using templates from `skills/create-odoo-pwa/templates/{{FRAMEWORK}}/base/`:

#### For SvelteKit:
- `package.json` - Dependencies including @sveltejs/kit, @vite-pwa/sveltekit, @sveltejs/adapter-static
- `svelte.config.js` - SvelteKit configuration with adapter-static
- `vite.config.js` - Vite + PWA plugin configuration
- `jsconfig.json` or `tsconfig.json` - Path aliases and compiler options

#### For React:
- `package.json` - Dependencies including React 18, Vite, vite-plugin-pwa
- `vite.config.js` - React + PWA plugin configuration
- `tsconfig.json` - TypeScript configuration

#### For Vue:
- `package.json` - Dependencies including Vue 3, Vite, vite-plugin-pwa
- `vite.config.js` - Vue + PWA plugin configuration
- `tsconfig.json` - TypeScript configuration

### Step 3: Environment and Git Configuration

Create `.env.example`:
```env
# Odoo Instance Configuration
ODOO_URL=https://your-instance.odoo.com
ODOO_DB=your-database-name
ODOO_USERNAME=your-username
ODOO_API_KEY=your-api-key

# Primary Model (use x_ prefix)
ODOO_PRIMARY_MODEL=x_{{MODEL_NAME}}

# Optional: For static hosting (GitHub Pages, etc.)
PUBLIC_API_URL=
```

Create `.gitignore`:
```
node_modules/
.env
dist/
build/
.svelte-kit/
.vercel/
.DS_Store
*.log
```

### Step 4: Core Library Files

Generate these essential files from templates:

#### A. Odoo API Client (`src/lib/odoo.js`)
Features:
- API URL configuration (supports PUBLIC_API_URL for static hosts)
- `callApi(action, data)` - Core API communication
- `createRecord(model, fields)` - Create records
- `searchRecords(model, domain, fields)` - Search/read records
- `updateRecord(model, id, values)` - Update records
- `deleteRecord(model, id)` - Delete records
- `formatMany2one(id)` - Format single relation fields
- `formatMany2many(ids)` - Format multi-relation fields
- Model-specific convenience methods

#### B. IndexedDB Manager (`src/lib/db.js`)
Features:
- Database initialization with versioning
- Store definitions for master data (partners, categories, config)
- CRUD operations: `add()`, `get()`, `getAll()`, `update()`, `remove()`
- Transaction helpers
- Error handling

#### C. Smart Cache Store (`src/lib/stores/{{MODEL_NAME}}Cache.js`)
Features:
- Framework-specific store pattern (Svelte store/React context/Vue composable)
- Dual storage strategy (localStorage for metadata, IndexedDB for master data)
- `initialize()` - Load cache and start background sync
- `sync(forceFullRefresh)` - Incremental sync with Odoo
- `forceRefresh()` - Clear cache and full sync
- Partner name resolution with caching
- Optimistic UI updates
- Stale detection (5-minute cache validity)
- Background sync (3-minute intervals)
- Derived stores for UI states

#### D. Utility Functions (`src/lib/{{MODEL_NAME}}Utils.js`)
Features:
- Business logic calculations
- Data normalization helpers
- Field formatters

### Step 5: Server-Side API Proxy

#### For SvelteKit: `src/routes/api/odoo/+server.js`
Features:
- JSON-RPC client for Odoo
- UID caching to reduce auth calls
- `execute(model, method, args, kwargs)` helper
- POST request handler with actions:
  - `create` - Create new record
  - `search` - Search and read records
  - `search_model` - Search any Odoo model
  - `update` - Update existing record
  - `delete` - Delete record
- Error handling with descriptive messages
- Environment variable access

#### For React/Vue: `src/api/odoo.js` (server endpoint)
Similar functionality adapted to framework conventions

### Step 6: UI Components and Routes

Generate starter components and pages:

#### SvelteKit Routes:
- `src/routes/+layout.svelte` - Root layout with navigation
- `src/routes/+layout.js` - SSR/CSR configuration (ssr: false, csr: true)
- `src/routes/+page.svelte` - Main form for creating records
- `src/routes/list/+page.svelte` - List/table view with filtering
- `src/app.html` - HTML template with PWA meta tags

#### React/Vue Pages:
Equivalent component structure adapted to framework conventions

#### Shared Components:
- `OfflineBanner` - Shows online/offline status
- `SyncStatus` - Displays sync state and last sync time
- `LoadingSpinner` - Loading indicator
- Form components with offline support

### Step 7: PWA Configuration

Generate PWA files:

#### `static/manifest.json` (or `public/manifest.json`):
```json
{
  "name": "{{PROJECT_NAME}}",
  "short_name": "{{PROJECT_NAME}}",
  "description": "{{MODEL_DISPLAY_NAME}} management app",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#667eea",
  "icons": [
    {
      "src": "/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
```

Configure service worker in `vite.config.js`:
- Auto-update strategy
- Cache all static assets
- Offline support

### Step 8: Deployment Configuration

Generate deployment files based on target:

#### Vercel (`vercel.json`):
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "build",
  "framework": "sveltekit",
  "regions": ["iad1"]
}
```

#### GitHub Pages (`.github/workflows/deploy.yml`):
```yaml
name: Deploy to GitHub Pages
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm ci
      - run: npm run build
      - uses: actions/upload-pages-artifact@v2
        with:
          path: build
```

#### Cloudflare/Netlify:
Generate appropriate configuration files

### Step 9: Documentation

Generate comprehensive documentation:

#### `README.md`:
- Project overview
- Prerequisites (Node.js, Odoo account)
- Installation steps
- Odoo Studio model setup instructions
- Development commands
- Deployment guide
- Architecture overview

#### `CLAUDE.md`:
Complete architecture documentation following the expense-split-pwa pattern:
- Project overview
- Development commands
- Environment setup
- Architecture diagrams
- Key architectural patterns
- Odoo model structure
- Important development notes
- Common gotchas

#### `API.md`:
- Odoo integration patterns
- Available API methods
- Field formatting examples
- Common operations

### Step 10: Post-Generation Instructions

After generating all files, provide the user with:

```
✅ Project '{{PROJECT_NAME}}' generated successfully!

📋 Next Steps:

1. Navigate to the project:
   cd {{PROJECT_NAME}}

2. Install dependencies:
   npm install

3. Configure Odoo credentials:
   cp .env.example .env
   # Edit .env with your Odoo instance details

4. Create Odoo Studio Model:
   - Log into your Odoo instance
   - Go to Studio
   - Create a new model named: x_{{MODEL_NAME}}
   - Add custom fields with x_studio_ prefix
   - Example fields:
     * x_name (Char) - Required
     * x_studio_description (Text)
     * x_studio_value (Float)
     * x_studio_date (Date)
     * x_studio_category (Many2one → res.partner or custom)

5. Start development server:
   npm run dev

6. Generate PWA icons:
   - Create 192x192 and 512x512 PNG icons
   - Place in static/ or public/ directory
   - Name them icon-192.png and icon-512.png

7. Deploy (optional):
   - Vercel: vercel
   - GitHub Pages: Push to main branch
   - Cloudflare: wrangler deploy
   - Netlify: netlify deploy

📚 Documentation:
- README.md - Getting started guide
- CLAUDE.md - Architecture documentation
- API.md - Odoo integration patterns

🔗 Resources:
- Odoo API Docs: https://www.odoo.com/documentation/
- SvelteKit Docs: https://kit.svelte.dev/
```

## Template Variables

When generating files, replace these placeholders:

- `{{PROJECT_NAME}}` - User's project name (kebab-case)
- `{{MODEL_NAME}}` - Odoo model name without x_ prefix
- `{{MODEL_DISPLAY_NAME}}` - Human-readable model name
- `{{FRAMEWORK}}` - sveltekit/react/vue
- `{{DEPLOYMENT_TARGET}}` - vercel/github-pages/cloudflare/netlify
- `{{AUTHOR_NAME}}` - User's name (if provided)

## Common Patterns from expense-split-pwa

This skill implements proven patterns from the expense-split-pwa project:

1. **Smart Caching**: Load from cache immediately, sync in background if stale
2. **Incremental Fetch**: Only fetch records with `id > lastRecordId`
3. **Partner Resolution**: Batch-fetch and cache partner names
4. **Dual-Phase Calculation**: Process settled/unsettled records separately
5. **Optimistic Updates**: Update UI immediately, sync to server in background
6. **Error Recovery**: Graceful degradation when offline

## Error Handling

If generation fails:
- Verify all required input is provided
- Check template files exist
- Ensure proper permissions for file creation
- Provide clear error messages to user

## Framework-Specific Notes

### SvelteKit
- Use Svelte 5 runes syntax (`$state`, `$derived`, `$effect`)
- Configure adapter-static for static deployment
- Set `ssr: false` for client-side only apps
- Use `$app/paths` for base path support

### React
- Use React 18+ with hooks
- Context API for global state
- React Query for server state (optional)
- Vite for build tooling

### Vue
- Use Vue 3 Composition API
- Pinia for state management
- Composables for reusable logic
- Vite for build tooling

## Testing the Generated Project

After generation, verify:
1. `npm install` completes without errors
2. `npm run dev` starts development server
3. Form renders correctly
4. Offline banner appears when disconnecting
5. Data persists in localStorage/IndexedDB
6. Sync works when back online

## Support

For issues or questions:
- Check CLAUDE.md for architecture details
- Review generated code comments
- Consult Odoo API documentation
- Verify environment variables are set correctly
