---
name: add-odoo-model
description: Add integration for an additional Odoo Studio model to an existing Odoo PWA project. Use when user wants to add support for another model, mentions "add new model", "integrate another Odoo model", or similar.
allowed-tools: Read, Write, Edit, Glob
---

# Add Odoo Model Integration

Add a new Odoo model integration to an existing Odoo PWA project, creating cache stores, API methods, and UI components.

## Prerequisites

- Existing Odoo PWA project (generated with create-odoo-pwa skill)
- New Odoo Studio model created with `x_` prefix
- Model name and display name from user

## Required User Input

Ask the user for:

1. **Model name** (required)
   - Format: without `x_` prefix (e.g., "inventory", "tasks")
   - Example: If Odoo model is `x_inventory`, user provides: `inventory`

2. **Model display name** (required)
   - Human-readable singular name (e.g., "Inventory Item", "Task")

3. **Create UI pages** (optional)
   - Ask if user wants to generate form and list pages
   - Default: yes

## Detection Steps

Before generating, detect the project structure:

1. **Detect framework**:
   - Check for `svelte.config.js` → SvelteKit
   - Check for `vite.config.ts` with React → React
   - Check for `nuxt.config.ts` → Vue/Nuxt

2. **Find existing files**:
   - Locate `src/lib/odoo.js` (or equivalent)
   - Find existing cache stores in `src/lib/stores/`
   - Check routes structure

3. **Verify Odoo connection**:
   - Check `.env` file has ODOO_URL and credentials

## Generation Steps

### Step 1: Create Cache Store

Generate `src/lib/stores/{{MODEL_NAME}}Cache.js`:

- Based on existing cache store pattern
- Replace model name throughout
- Update fields array with model-specific fields
- Include CRUD methods

### Step 2: Update Odoo API Client

Add model-specific methods to `src/lib/odoo.js`:

```javascript
/**
 * Fetch {{MODEL_DISPLAY_NAME}} records
 */
async fetch{{MODEL_NAME|capitalize}}s(domain = [], fields = []) {
  return await this.searchRecords('x_{{MODEL_NAME}}', domain, fields);
}

/**
 * Create {{MODEL_DISPLAY_NAME}}
 */
async create{{MODEL_NAME|capitalize}}(fields) {
  return await this.createRecord('x_{{MODEL_NAME}}', fields);
}

/**
 * Update {{MODEL_DISPLAY_NAME}}
 */
async update{{MODEL_NAME|capitalize}}(id, values) {
  return await this.updateRecord('x_{{MODEL_NAME}}', id, values);
}

/**
 * Delete {{MODEL_DISPLAY_NAME}}
 */
async delete{{MODEL_NAME|capitalize}}(id) {
  return await this.deleteRecord('x_{{MODEL_NAME}}', id);
}
```

### Step 3: Create UI Pages (if requested)

#### Add Form Page: `src/routes/{{MODEL_NAME}}/+page.svelte`

Generate form component:
- Import cache store
- Form fields for model
- Handle offline/online states
- Submit handler with validation

#### List Page: `src/routes/{{MODEL_NAME}}/list/+page.svelte`

Generate list component:
- Display records in table/card format
- Search/filter functionality
- Delete actions
- Sync status

### Step 4: Update Navigation

Update navigation in main layout or existing pages:

```svelte
<nav>
  <!-- Existing links -->
  <a href="/{{MODEL_NAME}}">{{MODEL_DISPLAY_NAME}}s</a>
</nav>
```

### Step 5: Update Environment Variables

Add to `.env.example` (if needed):
```env
# {{MODEL_DISPLAY_NAME}} Model
ODOO_{{MODEL_NAME|uppercase}}_MODEL=x_{{MODEL_NAME}}
```

## Post-Generation Instructions

Provide user with:

```
✅ {{MODEL_DISPLAY_NAME}} integration added successfully!

📋 Next Steps:

1. Verify Odoo Model Setup:
   - Model name: x_{{MODEL_NAME}}
   - Add custom fields with x_studio_ prefix in Odoo Studio

2. Update Cache Store:
   - Edit src/lib/stores/{{MODEL_NAME}}Cache.js
   - Add all model fields to the 'fields' array

3. Customize UI:
   - Edit src/routes/{{MODEL_NAME}}/+page.svelte for form
   - Edit src/routes/{{MODEL_NAME}}/list/+page.svelte for list view
   - Add model-specific fields and validation

4. Test Integration:
   npm run dev
   - Navigate to /{{MODEL_NAME}}
   - Test create, read, update, delete operations
   - Verify offline functionality

📚 Model-Specific Files Created:
- src/lib/stores/{{MODEL_NAME}}Cache.js - Cache and sync logic
- src/routes/{{MODEL_NAME}}/+page.svelte - Add form
- src/routes/{{MODEL_NAME}}/list/+page.svelte - List view

🔗 Access:
- Add: http://localhost:5173/{{MODEL_NAME}}
- List: http://localhost:5173/{{MODEL_NAME}}/list
```

## Framework-Specific Notes

### SvelteKit
- Use Svelte 5 syntax with `$state`, `$derived`, `$effect`
- Cache stores use Svelte stores pattern
- Routes in `src/routes/`

### React
- Use React hooks (useState, useEffect)
- Context API for cache
- Routes configuration depends on router (React Router, etc.)

### Vue
- Use Vue 3 Composition API
- Composables for cache logic
- Routes in `src/pages/` or as configured

## Error Handling

If generation fails:
- Verify project has Odoo PWA structure
- Check for existing odoo.js file
- Ensure proper permissions for file creation
- Provide clear error messages

## Examples

User: "Add inventory model to track items"
- Model name: inventory
- Display name: Inventory Item
- Creates: inventoryCache.js, /inventory pages, API methods

User: "Integrate task management"
- Model name: task
- Display name: Task
- Creates: taskCache.js, /task pages, API methods
