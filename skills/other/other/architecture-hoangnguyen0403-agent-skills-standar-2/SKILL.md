---
name: Next.js Architecture (FSD)
description: Scalable project structure using Feature-Sliced Design (FSD).
metadata:
  labels: [nextjs, architecture, fsd, folder-structure]
  triggers:
    files: ['src/features/**', 'src/entities/**', 'src/widgets/**']
    keywords: [FSD, Feature Sliced Design, slices, segments]
---

# Architecture (Feature-Sliced Design)

## **Priority: P2 (MEDIUM)**

Adopt **Feature-Sliced Design (FSD)** for scalable applications.
**Warning**: FSD introduces boilerplate. Use it only if the project is expected to grow significantly (e.g., 20+ features). For smaller projects, a simple module-based structure is preferred.

## Strategy

1. **RSC Boundaries**: Enforce strict serialization rules for props passed from Server to Client. See [RSC Boundaries & Serialization](references/RSC_BOUNDARIES.md).
2. **App Layer is Thin**: The `app/` directory (App Router) is **only** for Routing.
   - _Rule_: `page.tsx` should only import Widgets/Features. No business logic (`useEffect`, `fetch`) directly in pages.
3. **Slices over Types**: Group code by **Business Domain** (User, Product, Cart), not by File Type (Components, Hooks, Utils).
   - _Bad_: `src/components/LoginForm.tsx`, `src/hooks/useLogin.ts`
   - _Good_: `src/features/auth/login/` containing both.
4. **Layer Hierarchy**: Code can only import from _layers below it_.
   - `App` -> `Widgets` -> `Features` -> `Entities` -> `Shared`.
5. **Avoid Excessive Entities**: Do not preemptively create Entities.
   - _Rule_: Start logic in `Features` or `Pages`. Move to `Entities` **only** when data/logic is strictly reused across multiple differing features.
   - _Rule_: Simple CRUD belongs in `shared/api`, not `entities`.
6. **Standard Segments**: Use standard segment names within slices.
   - `ui` (Components), `model` (State/actions), `api` (Data fetching), `lib` (Helpers), `config` (Constants).
   - _Avoid_: `components`, `hooks`, `services` as segment names.

## Structure Reference

For the specific directory layout and layer definitions, see the reference documentation.

- [**FSD Folder Structure**](references/fsd-structure.md)
- [**Bundling & Compatibility**](references/BUNDLING.md)
- [**Runtime Selection (Edge/Node)**](references/RUNTIME_SELECTION.md)
- [**Debug Tricks & MCP**](references/DEBUG_TRICKS.md)

## Integration with Next.js Core

- **Server Actions**: Place them in the `model/` folder of a Feature (e.g., `features/auth/model/actions.ts`).
- **Data Access (DAL)**: Place logic in the `model/` folder of an Entity (e.g., `entities/user/model/dal.ts`).
- **UI Components**: Base UI (shadcn) belongs in `shared/ui`. Feature-specific UI belongs in `features/*/ui`.
