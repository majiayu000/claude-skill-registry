---
name: copycat
description: Inventory a Next.js app's marketing and dashboard views by authenticated vs unauthenticated roles, confirm view names with the user, and plan a shadcn-based clean platform scaffold in a separate App Router folder using user-confirmed naming and route segments. Use when auditing role-based views, planning shadcn UI recreation, or splitting auth vs public routes.
---

# Next.js Auth View Discovery + Clean Platform Scaffold

## Quick start
1) Identify router type and entry points.
2) Inventory routes, auth boundaries, and roles.
3) Run a route naming audit (librarian pass).
4) Confirm the view list and new names with the user.
5) Derive the platform name and route segment from existing copy.
6) Scaffold `app/<platform-segment>` public/app layouts.
7) Add the landing header dropdown link.
8) Smoke-test public and auth routes.

## Scope
Does:
- Inventory public vs authenticated routes and role gates.
- Confirm view naming and scope before scaffold.
- Create a clean App Router subtree for the new platform.
- Keep legacy routes intact and isolated.

Does not:
- Migrate every legacy screen.
- Change auth logic or delete old code.

## Required inputs
Derive before scaffolding (do not ask the user):
- `platformName`
- `platformRouteSegment`
- `platformFolderName` (default: `platformRouteSegment`)
- `landingDropdownLabel` (default: `platformName`)
- `landingDropdownItemLabel` (default: `platformName`)

## Rule categories by priority
| Priority | Category | Rules |
| --- | --- | --- |
| 1 | Discovery & confirmation | `rules/discovery-auth-views`, `rules/route-naming-audit`, `rules/confirm-view-names`, `rules/platform-naming-derive` |
| 2 | Platform scaffold & boilerplate | `rules/routing-platform-scaffold`, `rules/boilerplate-first` |
| 3 | Coexistence & entry | `rules/coexistence-legacy`, `rules/landing-header-dropdown` |
| 4 | Naming & testing | `rules/naming-clean`, `rules/test-auth-flows` |

## Output: view inventory template
```
UserRole: <role name>
Public views (unauthenticated):
- <View Title> -> <route> (source: <file>)

Authenticated views:
- <View Title> -> <route> (source: <file>)

Role-specific views:
- <View Title> -> <route> (role gate: <where>)

Status:
- Recreate in new platform: YES / NO
- Rename required: YES / NO
- New name (if renamed): <confirmed title>
 - Active in UI navigation: YES / NO
 - Evidence of activity: <nav link | redirect | deep link | comment>
```

## Rules (must follow)
- Boilerplate-first: only scaffold confirmed views.
- Confirmation-first: do not scaffold before view list + naming is confirmed.
- Clean naming: no `New*`, `*V2`, `Temp*`, legacy prefixes.
- Legacy isolation: do not import legacy CSS into new platform layouts.
- Shadcn-first: use shadcn components via CLI or MCP.
- Shadcn install: use MCP to add all components upfront, then reuse.
- Shadcn blocks: prefer `sidebar-16`/`sidebar-01`, `dashboard-01`, `login-04`, `signup-02`.
- Global CSS baseline: use shadcn create preset (nova/zinc/orange).
- No legacy UI kits: do not use Ant/Chakra/etc in new routes.
- Auth parity: align new auth routes with historical provider and users.
- No legacy CSS: enforce new baseline styles only.
- Keep new routes under `app/<platform-segment>`.

## Platform structure
```
app/
  <platform-segment>/
    layout.tsx
    (public)/
      layout.tsx
      page.tsx
      <public-views>/
    (app)/
      layout.tsx
      <auth-views>/
```

## Verification
- Public routes load unauthenticated.
- Authenticated routes redirect when unauthenticated.
- Role-gated routes block unauthorized roles.
- Landing dropdown navigates to `/<platform-segment>`.
- No console errors on load.

## Version policy
Use the latest stable versions of `next`, `react`, `tailwindcss`, and `shadcn/ui`.

## Additional resources
- Scans, mapping tips, and gotchas: `reference.md`
- Example inventories and scaffolds: `examples.md`
- Rule index:
  - Priority 1: `rules/discovery-auth-views`, `rules/route-naming-audit`, `rules/confirm-view-names`, `rules/platform-naming-derive`
  - Priority 2: `rules/routing-platform-scaffold`, `rules/boilerplate-first`
  - Priority 3: `rules/coexistence-legacy`, `rules/landing-header-dropdown`
  - Priority 4: `rules/naming-clean`, `rules/test-auth-flows`
