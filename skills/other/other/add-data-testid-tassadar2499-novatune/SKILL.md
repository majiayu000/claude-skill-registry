---
name: add-data-testid
description: Systematically add data-testid attributes to Vue components for UI test automation
user_invocable: true
arguments:
  - name: component
    description: Path to Vue component or feature area (e.g., auth, library, playlists, admin)
    required: true
---

# Add data-testid Attributes Skill

Add stable `data-testid` attributes to Vue components to enable reliable Selenium/Playwright test selectors.

## Steps

1. **Identify the target component(s)**. If a feature area is given (e.g., "auth"), find all relevant `.vue` files:
   ```bash
   find src/NovaTuneClient/apps -name "*.vue" -path "*/{feature}/*"
   ```

2. **Check existing attributes**. Search for existing `data-testid` in the target files:
   ```bash
   grep -n "data-testid" <file>
   ```

3. **Add attributes** following the naming conventions below. Add to:
   - **Form inputs**: Each `<input>`, `<select>`, `<textarea>` with a unique testid
   - **Submit/action buttons**: All buttons that trigger actions
   - **Error/success messages**: Conditional alert/banner divs
   - **Page headings**: Main `<h1>` or `<h2>` elements
   - **Empty states**: "No items" placeholder containers
   - **Lists/grids**: Container elements that hold dynamic content
   - **Navigation links**: Sidebar or tab navigation items
   - **Modals**: Modal containers and their form elements

4. **Verify** no lint or typecheck regressions:
   ```bash
   cd src/NovaTuneClient && pnpm lint && pnpm typecheck
   ```

## Naming Conventions

| Element Type | Pattern | Example |
|---|---|---|
| Text input | field name | `data-testid="email"` |
| Password input | `password` or field name | `data-testid="password"` |
| Confirm field | field name | `data-testid="confirmPassword"` |
| Submit button | `{action}-button` | `data-testid="login-button"` |
| Action button | `{action}-button` | `data-testid="create-playlist-button"` |
| Error message | `error-message` | `data-testid="error-message"` |
| Success message | `success-message` | `data-testid="success-message"` |
| Page heading | `{page}-heading` | `data-testid="library-heading"` |
| Empty state | `empty-state` | `data-testid="empty-state"` |
| List container | `{item}-list` | `data-testid="track-list"` |
| Modal input | `{entity}-{field}-input` | `data-testid="playlist-name-input"` |
| Modal submit | `{entity}-submit-button` | `data-testid="playlist-submit-button"` |
| Nav link | `nav-{destination}` | `data-testid="nav-dashboard"` |
| Search input | `search-input` | `data-testid="search-input"` |
| Loading spinner | `loading-spinner` | `data-testid="loading-spinner"` |

## Rules

- **Never change behavior**: Only add `data-testid` attributes. Do not modify logic, styles, or structure.
- **Attribute goes on the opening tag**: `<div ... data-testid="foo">` not as a child or text content.
- **One testid per element**: Each element gets at most one `data-testid`.
- **Unique within page**: Two elements visible at the same time should not share a `data-testid`.
- **Stable names**: Use semantic names tied to purpose, not implementation (e.g., `email` not `input-3`).
- **kebab-case for compound names**: `error-message`, `create-playlist-button`, not camelCase.
- **camelCase for field names**: Match the `v-model` binding name (e.g., `displayName`, `confirmPassword`).

## Example Diff

Before:
```html
<input id="email" v-model="email" type="email" required class="input" placeholder="you@example.com" />
```

After:
```html
<input id="email" v-model="email" type="email" required class="input" placeholder="you@example.com" data-testid="email" />
```

Before:
```html
<div v-if="error" class="p-3 bg-red-900/50 border border-red-700 rounded-lg text-red-200 text-sm">
```

After:
```html
<div v-if="error" class="p-3 bg-red-900/50 border border-red-700 rounded-lg text-red-200 text-sm" data-testid="error-message">
```

## Current Coverage

Components that already have `data-testid`:
- `apps/player/src/features/auth/LoginPage.vue` — email, password, login-button

Components that need `data-testid` (as of last check):
- `apps/player/src/features/auth/RegisterPage.vue`
- `apps/admin/src/features/auth/AdminLoginPage.vue`
- `apps/admin/src/features/auth/AdminRegisterPage.vue`
- `apps/player/src/features/library/LibraryPage.vue`
- `apps/player/src/features/playlists/PlaylistsPage.vue`
- `apps/admin/src/features/analytics/DashboardPage.vue`
