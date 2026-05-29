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

The frontend determines which "App" to load based on the **Host Resolution** provided by the backend. This is handled by `DomainConfigService`.

**CRITICAL:** The decision of which app to load is **NOT** inferred solely from the URL pattern. It is explicitly returned by the backend in the `config.app` property.

### Resolution Response Structure

When the frontend calls `/api/domains/resolve`, the backend returns a configuration object. The `config.app` key is the **Source of Truth**.

```json
{
  "success": true,
  "data": {
    "hostname": "vendix.com",
    "config": {
      "app": "VENDIX_LANDING",  // <--- THIS DETERMINES THE APP
      "branding": { ... },
      "security": { ... }
    },
    "domain_type": "vendix_core"
  }
}
```

### Domain Types (`DomainType`)

Although `config.app` is the primary driver, domains are categorized into types based on the resolved entity in the database, **NOT** the URL structure itself.

1.  **`VENDIX_CORE`** (`app.vendix.com`, `vendix.com`)
    - **Apps:** `VENDIX_LANDING` (public), `VENDIX_ADMIN` (private).
2.  **`ORGANIZATION`** (Any mapped domain/subdomain)
    - _Examples:_ `my-company.vendix.com`, `corp.custom-domain.com`
    - **Apps:** `ORG_ADMIN` (private), `ORG_LANDING` (public).
3.  **`STORE`** (Any mapped domain/subdomain)
    - _Examples:_ `cool-shop.vendix.com`, `store.my-company.com`, `www.mystore.com`
    - **Note:** Subdomains are aesthetic/flexible. The backend resolves the hostname to a specific `store_id`.
    - **Apps:** `STORE_ADMIN` (private), `STORE_ECOMMERCE` (public).
4.  **`ECOMMERCE`** (Dedicated storefront domain)
    - **Apps:** `STORE_ECOMMERCE` (public).

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

### Backend: `DefaultPanelUIService`

The backend dictates which modules are active for a user via `user_settings.config.panel_ui`.

```json
// Example User Settings (ORG_ADMIN)
{
  "app": "ORG_ADMIN",
  "panel_ui": {
    "ORG_ADMIN": { "dashboard": true, "stores": true, "billing": true },
    "STORE_ADMIN": { "pos": true, "orders": true } // Optional access to store features
  }
}
```

### Frontend: Environment Switching

Users can switch between environments (e.g., from `ORG_ADMIN` to `STORE_ADMIN`) if they have permissions.

- **Service:** `EnvironmentSwitchService`.
- **Action:** Updates `user_settings.config.app` and redirects to the appropriate route.

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

- **Domain Config Interface**: `apps/frontend/src/app/core/models/domain-config.interface.ts`
- **Routing Skill**: [vendix-frontend-routing](../vendix-frontend-routing/SKILL.md)
- **Backend Defaults**: `apps/backend/src/common/services/default-panel-ui.service.ts`
