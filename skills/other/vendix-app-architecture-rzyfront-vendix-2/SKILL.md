---
name: vendix-app-architecture
description: >
  Explains the Vendix Public and Private App architecture, Domain Types, and App Environments.
  Trigger: When asking about different apps, environments (ORG_ADMIN, STORE_ADMIN), or domain logic.
license: Apache-2.0
metadata:
  author: vendix-arch
  version: "1.0"
  scope: [root]
  auto_invoke: "Understanding Public/Private Apps and Domains"
---

## When to Use

Use this skill when:

- Understanding the difference between Public and Private apps.
- Configuring domains or environments.
- Debugging routing issues related to domain resolution.
- Setting up new user roles and their corresponding environments.

## 🏗️ Core Architecture: One Codebase, Multiple Apps

Vendix is a **multi-tenant monorepo** where a single frontend application (`apps/frontend`) dynamically behaves as different "Apps" based on the **Domain** and **User Context**.

### 🌍 App Environments

The system defines specific "Environments" that determine the UI and features available.

| Environment           | Type    | Target User           | Description                                             |
| :-------------------- | :------ | :-------------------- | :------------------------------------------------------ |
| **`VENDIX_ADMIN`**    | Private | Super Admin           | Platform administration (SaaS owners).                  |
| **`ORG_ADMIN`**       | Private | Org Owner / Admin     | Manages the Organization, Billing, and global settings. |
| **`STORE_ADMIN`**     | Private | Store Manager / Staff | Manages a specific Store (POS, Inventory, Orders).      |
| **`STORE_ECOMMERCE`** | Public  | Customers             | Public online store for shopping.                       |
| **`VENDIX_LANDING`**  | Public  | Visitors              | Public landing page for the Vendix SaaS platform.       |
| **`ORG_LANDING`**     | Public  | Visitors              | Public landing page for an Organization (optional).     |

---

## 🔍 Domain Resolution Logic

The frontend determines which "App" to load based on the **Host Resolution** provided by the backend. This is handled by `AppConfigService`.

**CRITICAL:** The decision of which app to load is **NOT** inferred solely from the URL pattern. It is explicitly returned by the backend in the `app` property (from `domain_settings.app_type`).

### Resolution Response Structure

When the frontend calls `/api/domains/resolve`, the backend returns a configuration object. The `app` key is the **Source of Truth** (synchronized with `app_type_enum`).

```json
{
  "success": true,
  "data": {
    "hostname": "vendix.com",
    "app": "VENDIX_LANDING",  // <--- THIS DETERMINES THE APP (from domain_settings.app_type)
    "branding": { ... },      // Branding from store_settings
    "fonts": { ... },         // Fonts from store_settings
    "ecommerce": { ... },     // Ecommerce config from store_settings
    "publication": { ... },   // Publication config from store_settings
    "domain_type": "vendix_core",
    "config": {               // Legacy - kept for backward compatibility
      "app": "VENDIX_LANDING"
    }
  }
}
```

### App Type Enum (Backend + Frontend)

Both backend and frontend use the **same enum values** for `app_type`:

```typescript
// Frontend: apps/frontend/src/app/core/models/environment.enum.ts
// Backend: Prisma schema - app_type_enum
export enum AppType {
  VENDIX_LANDING = 'VENDIX_LANDING',   // Public: Vendix SaaS landing
  VENDIX_ADMIN = 'VENDIX_ADMIN',       // Private: Super admin panel
  ORG_LANDING = 'ORG_LANDING',         // Public: Organization landing
  ORG_ADMIN = 'ORG_ADMIN',             // Private: Organization admin
  STORE_LANDING = 'STORE_LANDING',     // Public: Store landing
  STORE_ADMIN = 'STORE_ADMIN',         // Private: Store admin panel
  STORE_ECOMMERCE = 'STORE_ECOMMERCE', // Public: Store e-commerce
}
```

### Database Schema

```prisma
// Prisma schema
enum app_type_enum {
  VENDIX_LANDING
  VENDIX_ADMIN
  ORG_LANDING
  ORG_ADMIN
  STORE_LANDING
  STORE_ADMIN
  STORE_ECOMMERCE
}

model domain_settings {
  app_type  app_type_enum  @default(VENDIX_LANDING) // <--- Source of Truth
  config    Json?                                      // Now nullable (legacy)
  // ...
}

model user_settings {
  app_type  app_type_enum  @default(STORE_ADMIN) // Override post-login
  // ...
}
```

### Domain Types vs App Types

**IMPORTANT:** There are TWO related but distinct concepts:

1. **`app_type`** (`AppType` enum) - **Primary Source of Truth**
   - Determines which App/Environment loads
   - Stored in `domain_settings.app_type`
   - Can be overridden by `user_settings.app_type` after login
   - Directly controls UI/UX and available features

2. **`domain_type`** (`DomainType` enum) - **Legacy/Categorization**
   - Categorizes the domain based on the resolved entity
   - Used for database relationships and organization
   - **NOT** the primary driver for app selection
   - Will eventually be deprecated in favor of `app_type`

#### App Type → Domain Type Mapping

| `app_type` | `domain_type` | Example Domain |
| :--- | :--- | :--- |
| `VENDIX_LANDING` | `vendix_core` | `vendix.com` |
| `VENDIX_ADMIN` | `vendix_core` | `app.vendix.com/admin` |
| `ORG_LANDING` | `organization` | `my-company.vendix.com` |
| `ORG_ADMIN` | `organization` | `my-company.vendix.com/admin` |
| `STORE_LANDING` | `store` | `store.example.com` |
| `STORE_ADMIN` | `store` | `store.example.com/admin` |
| `STORE_ECOMMERCE` | `ecommerce` | `shop.example.com` |

**NOTE:** A single domain can resolve to different `app_type` values based on:
- User authentication status
- URL path (`/admin/*` vs `/`)
- User permissions and `user_settings.app_type` override

---

## 🔐 Private vs Public Access

### Private Apps (Admin Panels)

- **Requires Auth:** Yes (JWT).
- **Guards:** `AuthGuard`, `RolesGuard`.
- **Routing Path:** `/admin/*`, `/superadmin/*`.
- **Features:** Defined by `DefaultPanelUIService` in backend.
  - _Example:_ An `ORG_ADMIN` user sees "Stores", "Billing", "Users".
  - _Example:_ A `STORE_ADMIN` user sees "POS", "Orders", "Inventory".

### Public Apps (Storefronts / Landing)

- **Requires Auth:** No (Optional for Customer Accounts).
- **Guards:** None (or `PublicGuard`).
- **Routing Path:** `/` (Root), `/catalog`, `/cart`.
- **Features:** Product catalog, Cart, Checkout.

---

## 🛠️ Configuration & Context

### Backend: Store Settings & Branding

Branding and app configuration now comes from `store_settings` rather than `domain_settings.config`:

```typescript
// Backend: StoreSettings interface
interface StoreSettings {
  branding: {
    name: string;
    primary_color: string;
    secondary_color: string;
    logo_url?: string;
    favicon_url?: string;
    custom_css?: string;
  };
  fonts: {
    primary: string;
    secondary: string;
    headings: string;
  };
  publication: {
    store_published: boolean;
    ecommerce_enabled: boolean;
    landing_enabled: boolean;
    maintenance_mode: boolean;
  };
  ecommerce: {
    enabled: boolean;
    slider?: { ... };
    catalog?: { ... };
    cart?: { ... };
    checkout?: { ... };
  };
}
```

### User Settings: App Type Override

Users can have a default `app_type` override in their settings:

```json
// user_settings
{
  "app_type": "STORE_ADMIN",  // Default app for this user
  "config": {
    "panel_ui": {
      "ORG_ADMIN": { "dashboard": true, "stores": true },
      "STORE_ADMIN": { "pos": true, "orders": true }
    }
  }
}
```

### Frontend: Environment Switching

Users can switch between environments (e.g., from `ORG_ADMIN` to `STORE_ADMIN`) if they have permissions.

- **Service:** `AppConfigService` (formerly `DomainConfigService`)
- **Action:** Updates `user_settings.app_type` and redirects to the appropriate route.

```typescript
// Frontend: App type switching
switchAppType(newAppType: AppType) {
  // Update user preference on backend
  this.userService.updateSettings({ app_type: newAppType });
  // Redirect to appropriate route
  this.router.navigate(this.getRouteForAppType(newAppType));
}
```

---

## 📝 Decision Tree: Which App is this?

```
Incoming Request Hostname
├── Is it the main SaaS domain? (vendix.com)
│   ├── Is user logged in & SuperAdmin? → VENDIX_ADMIN
│   └── Else → VENDIX_LANDING
│
├── Is it an Organization domain? (org.vendix.com)
│   ├── Is user logged in & OrgUser? → ORG_ADMIN
│   └── Else → ORG_LANDING (or redirect to Login)
│
└── Is it a Store domain? (store.org.vendix.com)
    ├── Is URL path /admin/* ?
    │   └── Is user logged in & StoreUser? → STORE_ADMIN
    └── Else → STORE_ECOMMERCE
```

## Resources

- **App Type Enum (Frontend)**: `apps/frontend/src/app/core/models/environment.enum.ts`
- **Domain Config Interface**: `apps/frontend/src/app/core/models/domain-config.interface.ts`
- **App Config Service**: `apps/frontend/src/app/core/services/app-config.service.ts`
- **Routing Skill**: [vendix-frontend-routing](../vendix-frontend-routing/SKILL.md)
- **Backend Defaults**: `apps/backend/src/domains/store/settings/defaults/default-store-settings.ts`
- **Public Domains Service**: `apps/backend/src/domains/public/domains/public-domains.service.ts`
