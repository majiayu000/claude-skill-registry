---
name: vendix-frontend-domain
description: Domain configuration.
metadata:
  scope: [root]
  auto_invoke: "Working on frontend domains"
---
# Vendix Frontend Domain Detection

> **Domain Configuration** - Detección automática de dominios, configuración de branding y routing dinámico.

## 🌐 Domain Types

**File:** `core/models/domain-config.interface.ts`

```typescript
export enum DomainType {
  VENDIX_CORE = 'vendix_core',
  ORGANIZATION = 'organization',
  STORE = 'store',
  ECOMMERCE = 'ecommerce',
}

export interface DomainConfig {
  domain_type: DomainType;
  organization_id?: number;
  store_id?: number;
  organization_name?: string;
  store_name?: string;
  logo_url?: string;
  theme_config?: ThemeConfig;
}

export interface ThemeConfig {
  primary_color?: string;
  secondary_color?: string;
  font_family?: string;
  custom_css?: string;
}
```

---

## 🔍 Domain Detection Service

**File:** `core/services/domain-config.service.ts`

```typescript
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject, of } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { DomainConfig, DomainType } from '../models/domain-config.interface';

@Injectable({
  providedIn: 'root',
})
export class DomainConfigService {
  private http = inject(HttpClient);

  private domain_config$$ = new BehaviorSubject<DomainConfig>({
    domain_type: DomainType.VENDIX_CORE,
  });
  domain_config$ = this.domain_config$$.asObservable();

  constructor() {
    this.loadDomainConfig();
  }

  loadDomainConfig(): Observable<DomainConfig> {
    const host = window.location.host;
    const subdomain = this.extractSubdomain(host);

    return this.http.get<DomainConfig>('/api/domains/resolve', {
      params: { domain: subdomain },
    }).pipe(
      map(config => {
        this.domain_config$$.next(config);
        return config;
      }),
      catchError(() => {
        // Default to vendix core on error
        const default_config: DomainConfig = {
          domain_type: DomainType.VENDIX_CORE,
        };
        this.domain_config$$.next(default_config);
        return of(default_config);
      }),
    );
  }

  private extractSubdomain(host: string): string {
    const parts = host.split('.');
    return parts[0];
  }

  get domainType(): DomainType {
    return this.domain_config$$.value.domain_type;
  }

  get organizationId(): number | undefined {
    return this.domain_config$$.value.organization_id;
  }

  get storeId(): number | undefined {
    return this.domain_config$$.value.store_id;
  }

  get organizationName(): string | undefined {
    return this.domain_config$$.value.organization_name;
  }

  get storeName(): string | undefined {
    return this.domain_config$$.value.store_name;
  }

  get logoUrl(): string | undefined {
    return this.domain_config$$.value.logo_url;
  }

  get themeConfig(): ThemeConfig | undefined {
    return this.domain_config$$.value.theme_config;
  }

  isVendixCore(): boolean {
    return this.domainType === DomainType.VENDIX_CORE;
  }

  isOrganization(): boolean {
    return this.domainType === DomainType.ORGANIZATION;
  }

  isStore(): boolean {
    return this.domainType === DomainType.STORE;
  }

  isEcommerce(): boolean {
    return this.domainType === DomainType.ECOMMERCE;
  }
}
```

---

## 🎨 Branding Configuration

### Applying Theme

**File:** `app/app.component.ts`

```typescript
import { Component, OnInit, OnDestroy } from '@angular/core';
import { DomainConfigService } from '@/app/core/services/domain-config.service';

@Component({
  selector: 'app-root',
  template: '<router-outlet />',
})
export class AppComponent implements OnInit {
  constructor(private domain_config_service: DomainConfigService) {}

  ngOnInit() {
    this.domain_config_service.domain_config$.subscribe(config => {
      this.applyTheme(config.theme_config);
    });
  }

  private applyTheme(theme?: ThemeConfig) {
    if (!theme) return;

    const root = document.documentElement;

    if (theme.primary_color) {
      root.style.setProperty('--primary-color', theme.primary_color);
    }

    if (theme.secondary_color) {
      root.style.setProperty('--secondary-color', theme.secondary_color);
    }

    if (theme.font_family) {
      root.style.setProperty('--font-family', theme.font_family);
    }

    if (theme.custom_css) {
      // Apply custom CSS
      const style_element = document.createElement('style');
      style_element.textContent = theme.custom_css;
      document.head.appendChild(style_element);
    }
  }
}
```

---

## 🏪 Store Landing Component

**File:** `public/dynamic-landing/components/store-landing/store-landing.component.ts`

```typescript
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DomainConfigService } from '@/app/core/services/domain-config.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-store-landing',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './store-landing.component.html',
  styleUrls: ['./store-landing.component.scss'],
})
export class StoreLandingComponent implements OnInit {
  store_name = '';
  logo_url = '';
  isLoading = true;

  constructor(
    private domain_config_service: DomainConfigService,
    private router: Router,
  ) {}

  ngOnInit() {
    this.domain_config_service.domain_config$.subscribe(config => {
      this.store_name = config.store_name || '';
      this.logo_url = config.logo_url || '';
      this.isLoading = false;

      // If authenticated, redirect to home
      if (this.domain_config_service.isStore()) {
        this.router.navigate(['/home']);
      }
    });
  }

  goToCatalog() {
    this.router.navigate(['/catalog']);
  }

  goToLogin() {
    this.router.navigate(['/auth/login']);
  }
}
```

---

## 🏢 Organization Landing Component

**File:** `public/dynamic-landing/components/org-landing/org-landing.component.ts`

```typescript
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DomainConfigService } from '@/app/core/services/domain-config.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-org-landing',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './org-landing.component.html',
  styleUrls: ['./org-landing.component.scss'],
})
export class OrgLandingComponent implements OnInit {
  organization_name = '';
  isLoading = true;

  constructor(
    private domain_config_service: DomainConfigService,
    private router: Router,
  ) {}

  ngOnInit() {
    this.domain_config_service.domain_config$.subscribe(config => {
      this.organization_name = config.organization_name || '';
      this.isLoading = false;

      // If authenticated, redirect based on role
      if (this.domain_config_service.isOrganization()) {
        this.router.navigate(['/admin']);
      }
    });
  }

  goToAdmin() {
    this.router.navigate(['/auth/login']);
  }

  goToStoreSelection() {
    this.router.navigate(['/stores']);
  }
}
```

---

## 🎯 Domain-Specific Guards

### DomainTypeGuard

**File:** `core/guards/domain-type.guard.ts`

```typescript
import { Injectable } from '@angular/core';
import {
  CanActivate,
  ActivatedRouteSnapshot,
  RouterStateSnapshot,
  Router,
} from '@angular/router';
import { DomainConfigService, DomainType } from '@/app/core/services/domain-config.service';

@Injectable({
  providedIn: 'root',
})
export class DomainTypeGuard implements CanActivate {
  constructor(
    private domain_config_service: DomainConfigService,
    private router: Router,
  ) {}

  canActivate(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot,
  ): boolean {
    const required_domain_type = route.data['requiredDomainType'] as DomainType;
    const current_domain_type = this.domain_config_service.domainType;

    if (current_domain_type === required_domain_type) {
      return true;
    }

    // Redirect based on current domain type
    switch (current_domain_type) {
      case DomainType.STORE:
      case DomainType.ECOMMERCE:
        this.router.navigate(['/home']);
        break;

      case DomainType.ORGANIZATION:
        this.router.navigate(['/admin']);
        break;

      case DomainType.VENDIX_CORE:
        this.router.navigate(['/superadmin']);
        break;

      default:
        this.router.navigate(['/landing']);
    }

    return false;
  }
}
```

---

## 🔗 Usage in Routes

### Domain-Based Routes

```typescript
const routes: Routes = [
  {
    path: 'superadmin',
    canActivate: [DomainTypeGuard],
    data: { requiredDomainType: DomainType.VENDIX_CORE },
    children: SUPER_ADMIN_ROUTES,
  },
  {
    path: 'admin',
    canActivate: [DomainTypeGuard],
    data: { requiredDomainType: DomainType.ORGANIZATION },
    children: ADMIN_ROUTES,
  },
  {
    path: 'home',
    canActivate: [DomainTypeGuard],
    data: { requiredDomainType: DomainType.STORE },
    children: STORE_ROUTES,
  },
];
```

---

## 🔍 Key Files Reference

| File | Purpose |
|------|---------|
| `core/models/domain-config.interface.ts` | Domain type definitions |
| `core/services/domain-config.service.ts` | Domain detection and config |
| `public/dynamic-landing/components/*/` | Landing pages |
| `core/guards/domain-type.guard.ts` | Domain type guard |

---

## Related Skills

- `vendix-frontend-routing` - Routing patterns
- `vendix-frontend-module` - Module structure
- `vendix-naming-conventions` - Naming conventions (CRITICAL)
