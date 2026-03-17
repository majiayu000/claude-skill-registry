---
name: vendix-frontend-routing
description: Routing configuration.
metadata:
  scope: [root]
  auto_invoke: "Managing Routes"
---
# Vendix Frontend Routing Pattern

> **Public vs Private Routing** - Sistema de enrutamiento con guards, lazy loading y detección de dominios.

## 🗂️ Routing Structure

```
apps/frontend/src/app/routes/
├── public/                             # Public routes (no auth required)
│   ├── store_ecommerce.public.routes.ts
│   ├── store_landing.public.routes.ts
│   └── org_landing.public.routes.ts
│
└── private/                            # Private routes (auth required)
    ├── super_admin.routes.ts
    ├── admin.routes.ts
    ├── store_admin.routes.ts
    └── user.routes.ts
```

---
metadata:
  scope: [root]
  auto_invoke: "Managing Routes"

## 🚪 Public Routes

### Store E-commerce Routes

**File:** `routes/public/store_ecommerce.public.routes.ts`

```typescript
import { Routes } from '@angular/router';

export const STORE_ECOMMERCE_ROUTES: Routes = [
  {
    path: '',
    loadComponent: () =>
      import('@/app/public/dynamic-landing/components/store-landing/store-landing.component')
        .then(m => m.StoreLandingComponent),
  },
  {
    path: 'home',
    loadComponent: () =>
      import('@/app/private/modules/ecommerce/pages/home/home.component')
        .then(m => m.HomeComponent),
  },
  {
    path: 'catalog',
    loadComponent: () =>
      import('@/app/private/modules/ecommerce/pages/catalog/catalog.component')
        .then(m => m.CatalogComponent),
  },
  {
    path: 'product/:id',
    loadComponent: () =>
      import('@/app/private/modules/ecommerce/pages/product-detail/product-detail.component')
        .then(m => m.ProductDetailComponent),
  },
  {
    path: 'cart',
    loadComponent: () =>
      import('@/app/private/modules/ecommerce/pages/cart/cart.component')
        .then(m => m.CartComponent),
  },
  {
    path: 'checkout',
    loadComponent: () =>
      import('@/app/private/modules/ecommerce/pages/checkout/checkout.component')
        .then(m => m.CheckoutComponent),
  },
  {
    path: 'account',
    loadComponent: () =>
      import('@/app/private/modules/ecommerce/pages/account/account.component')
        .then(m => m.AccountComponent),
  },
  {
    path: 'wishlist',
    loadComponent: () =>
      import('@/app/private/modules/ecommerce/pages/wishlist/wishlist.component')
        .then(m => m.WishlistComponent),
  },
];
```

**Key Points:**
- NO `canActivate` - accessible without authentication
- Lazy loading with `loadComponent()`
- Store-facing e-commerce routes

---

## 🔒 Private Routes

### Super Admin Routes

**File:** `routes/private/super_admin.routes.ts`

```typescript
import { Routes } from '@angular/router';
import { AuthGuard } from '@/app/core/guards/auth.guard';
import { RolesGuard } from '@/app/core/guards/roles.guard';

export const SUPER_ADMIN_ROUTES: Routes = [
  {
    path: '',
    redirectTo: '/superadmin/dashboard',
    pathMatch: 'full',
  },
  {
    path: 'dashboard',
    loadComponent: () =>
      import('@/app/private/modules/superadmin/pages/dashboard/dashboard.component')
        .then(m => m.DashboardComponent),
    canActivate: [AuthGuard, RolesGuard],
    data: { roles: ['super_admin'] },
  },
  {
    path: 'organizations',
    loadComponent: () =>
      import('@/app/private/modules/superadmin/pages/organizations/organizations.component')
        .then(m => m.OrganizationsComponent),
    canActivate: [AuthGuard, RolesGuard],
    data: { roles: ['super_admin'] },
  },
  {
    path: 'system-settings',
    loadComponent: () =>
      import('@/app/private/modules/superadmin/pages/system-settings/system-settings.component')
        .then(m => m.SystemSettingsComponent),
    canActivate: [AuthGuard, RolesGuard],
    data: { roles: ['super_admin'] },
  },
];
```

**Key Points:**
- `canActivate` with guards
- `data.roles` specifies required roles
- Only accessible by super_admin

---

### Organization Admin Routes

**File:** `routes/private/admin.routes.ts`

```typescript
import { Routes } from '@angular/router';
import { AuthGuard } from '@/app/core/guards/auth.guard';

export const ADMIN_ROUTES: Routes = [
  {
    path: '',
    redirectTo: '/admin/dashboard',
    pathMatch: 'full',
  },
  {
    path: 'dashboard',
    loadComponent: () =>
      import('@/app/private/modules/organization/pages/dashboard/dashboard.component')
        .then(m => m.DashboardComponent),
    canActivate: [AuthGuard],
  },
  {
    path: 'users',
    loadComponent: () =>
      import('@/app/private/modules/organization/pages/users/users.component')
        .then(m => m.UsersComponent),
    canActivate: [AuthGuard],
  },
  {
    path: 'stores',
    loadComponent: () =>
      import('@/app/private/modules/organization/pages/stores/stores.component')
        .then(m) => m.StoresComponent),
    canActivate: [AuthGuard],
  },
];
```

---

## 🛡️ Guards

### AuthGuard

**File:** `core/guards/auth.guard.ts`

```typescript
import { Injectable } from '@angular/core';
import {
  CanActivate,
  Router,
  ActivatedRouteSnapshot,
  RouterStateSnapshot,
} from '@angular/router';
import { AuthService } from '@/app/core/services/auth.service';

@Injectable({
  providedIn: 'root',
})
export class AuthGuard implements CanActivate {
  constructor(
    private auth_service: AuthService,
    private router: Router,
  ) {}

  canActivate(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot,
  ): boolean {
    if (this.auth_service.isAuthenticated()) {
      return true;
    }

    // Store attempted URL for redirect after login
    this.auth_service.setRedirectUrl(state.url);

    this.router.navigate(['/auth/login']);
    return false;
  }
}
```

### RolesGuard

**File:** `core/guards/roles.guard.ts`

```typescript
import { Injectable } from '@angular/core';
import {
  CanActivate,
  ActivatedRouteSnapshot,
  RouterStateSnapshot,
  Router,
} from '@angular/router';
import { AuthService } from '@/app/core/services/auth.service';

@Injectable({
  providedIn: 'root',
})
export class RolesGuard implements CanActivate {
  constructor(
    private auth_service: AuthService,
    private router: Router,
  ) {}

  canActivate(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot,
  ): boolean {
    const required_roles = route.data['roles'] as string[];

    if (!required_roles || required_roles.length === 0) {
      return true;
    }

    const user_roles = this.auth_service.getUserRoles();

    const has_role = required_roles.some(role =>
      user_roles.includes(role)
    );

    if (has_role) {
      return true;
    }

    this.router.navigate(['/unauthorized']);
    return false;
  }
}
```

---

## 🌐 Domain-Based Routing

### Entry Point Component

**File:** `app/app.component.ts`

```typescript
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { DomainConfigService } from '@/app/core/services/domain-config.service';
import { DomainType } from '@/app/core/models/domain-config.interface';

@Component({
  selector: 'app-root',
  template: '<router-outlet />',
})
export class AppComponent implements OnInit {
  constructor(
    private domain_config_service: DomainConfigService,
    private router: Router,
  ) {}

  ngOnInit() {
    this.domain_config_service.loadDomainConfig().subscribe({
      next: (config) => {
        this.setupRoutes(config.domain_type);
      },
    });
  }

  private setupRoutes(domain_type: DomainType) {
    switch (domain_type) {
      case DomainType.VENDIX_CORE:
        this.router.navigateByUrl('/superadmin');
        break;

      case DomainType.ORGANIZATION:
        this.router.navigateByUrl('/admin');
        break;

      case DomainType.STORE:
      case DomainType.ECOMMERCE:
        this.router.navigateByUrl('/home');
        break;

      default:
        this.router.navigateByUrl('/landing');
    }
  }
}
```

---

## 🔀 Lazy Loading

### Route Configuration

```typescript
const routes: Routes = [
  {
    path: 'products',
    loadComponent: () =>
      import('./pages/products/products.component')
        .then(m => m.ProductsComponent),
  },
  {
    path: 'orders',
    loadComponent: () =>
      import('./pages/orders/orders.component')
        .then(m => m.OrdersComponent),
  },
];
```

---

## 📊 Route Data

### Passing Data to Routes

```typescript
// Defining route with data
{
  path: 'users/:id',
  loadComponent: () => import('./user-detail/user-detail.component')
    .then(m => m.UserDetailComponent),
  data: {
    title: 'User Details',
    breadcrumb: 'Users',
  },
}

// Accessing data in component
constructor(private route: ActivatedRoute) {}

ngOnInit() {
  const title = this.route.snapshot.data['title'];
  const id = this.route.snapshot.paramMap.get('id');
}
```

---

## 🔗 Navigation

### Router Navigation

```typescript
// Navigate to route
this.router.navigate(['/products']);

// Navigate with parameters
this.router.navigate(['/product', product_id]);

// Navigate with query parameters
this.router.navigate(['/products'], {
  queryParams: { page: 2, limit: 10 },
});

// Navigate with fragment
this.router.navigate(['/products'], {
  fragment: 'reviews',
});
```

### Relative Navigation

```typescript
// Navigate relative to current route
this.router.navigate(['../'], { relativeTo: this.route });

// Navigate to child route
this.router.navigate(['details'], { relativeTo: this.route });
```

---

## 🔍 Key Files Reference

| File | Purpose |
|------|---------|
| `routes/public/*.public.routes.ts` | Public route definitions |
| `routes/private/*.routes.ts` | Private route definitions |
| `core/guards/auth.guard.ts` | Authentication guard |
| `core/guards/roles.guard.ts` | Role-based guard |
| `core/services/domain-config.service.ts` | Domain configuration |

---

## Related Skills

- `vendix-frontend-domain` - Domain detection and config
- `vendix-frontend-module` - Module structure
- `vendix-frontend-component` - Component structure (CRITICAL)
