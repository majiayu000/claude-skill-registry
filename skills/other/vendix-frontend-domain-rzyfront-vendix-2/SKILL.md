---
name: vendix-frontend-domain
description: Domain configuration.
metadata:
  scope: [root]
  auto_invoke: "Working on frontend domains"
---
# Vendix Frontend Domain Detection

> **Domain Configuration** - Detección automática de dominios, configuración de branding y routing dinámico.

## 🌐 Domain Types & App Types

**Files:**
- `core/models/environment.enum.ts` - Enum definitions
- `core/models/domain-config.interface.ts` - Config interfaces

### App Type Enum (PRIMARY)

```typescript
// NUEVO ESTÁNDAR UNIFICADO - Única fuente de verdad para el tipo de app
export enum AppType {
  VENDIX_LANDING = 'VENDIX_LANDING',   // Landing principal de Vendix
  VENDIX_ADMIN = 'VENDIX_ADMIN',       // Admin super usuario de Vendix
  ORG_LANDING = 'ORG_LANDING',         // Landing de organización
  ORG_ADMIN = 'ORG_ADMIN',             // Admin de organización
  STORE_LANDING = 'STORE_LANDING',     // Landing de tienda
  STORE_ADMIN = 'STORE_ADMIN',         // Admin de tienda
  STORE_ECOMMERCE = 'STORE_ECOMMERCE', // Ecommerce de tienda
}

// Alias para compatibilidad
export type AppEnvironment = AppType;
export const AppEnvironment = AppType;
```

### Domain Type Enum (LEGACY)

```typescript
// Legacy - para compatibilidad con domain_type_enum del backend
export enum DomainType {
  VENDIX_CORE = 'vendix_core',
  ORGANIZATION = 'organization',
  STORE = 'store',
  ECOMMERCE = 'ecommerce',
}
```

### Domain Config Interface

```typescript
export interface DomainConfig {
  // Primary: App type determines which app loads
  environment: AppType;      // AppType enum value
  domainType: string;        // DomainType enum value (legacy)

  organization_slug?: string;
  store_slug?: string;
  organization_id?: number;
  store_id?: number;
  customConfig?: DomainCustomConfig;
  isVendixDomain: boolean;
  hostname: string;
}
```

---

## 🔍 Domain Detection Service

**File:** `core/services/app-config.service.ts` (formerly `domain-config.service.ts`)

```typescript
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject, of } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { DomainConfig, AppType, AppEnvironment } from '../models/domain-config.interface';

@Injectable({
  providedIn: 'root',
})
export class AppConfigService {
  private http = inject(HttpClient);

  private domain_config$$ = new BehaviorSubject<DomainConfig>({
    environment: AppType.VENDIX_LANDING,
    domainType: 'vendix_core',
  });
  domain_config$ = this.domain_config$$.asObservable();

  constructor() {
    this.loadDomainConfig();
  }

  loadDomainConfig(): Observable<DomainConfig> {
    const host = window.location.host;
    const subdomain = this.extractSubdomain(host);

    return this.http.get<DomainResolution>('/api/domains/resolve', {
      params: { domain: subdomain },
    }).pipe(
      map(response => {
        // Use 'app' from backend response (app_type from domain_settings)
        const config: DomainConfig = {
          environment: response.app as AppType,
          domainType: response.domain_type,
          organization_slug: response.organization_slug,
          store_slug: response.store_slug,
          organization_id: response.organization_id,
          store_id: response.store_id,
          customConfig: {
            branding: response.branding,
            fonts: response.fonts,
            ecommerce: response.ecommerce,
            publication: response.publication,
          },
          isVendixDomain: response.raw_domain_type === 'vendix_core',
          hostname: response.hostname,
        };
        this.domain_config$$.next(config);
        return config;
      }),
      catchError(() => {
        // Default to vendix core on error
        const default_config: DomainConfig = {
          environment: AppType.VENDIX_LANDING,
          domainType: 'vendix_core',
          isVendixDomain: true,
          hostname: window.location.host,
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

  // App Type getters (PRIMARY)
  get appType(): AppType {
    return this.domain_config$$.value.environment;
  }

  isVendixLanding(): boolean {
    return this.appType === AppType.VENDIX_LANDING;
  }

  isVendixAdmin(): boolean {
    return this.appType === AppType.VENDIX_ADMIN;
  }

  isOrgLanding(): boolean {
    return this.appType === AppType.ORG_LANDING;
  }

  isOrgAdmin(): boolean {
    return this.appType === AppType.ORG_ADMIN;
  }

  isStoreLanding(): boolean {
    return this.appType === AppType.STORE_LANDING;
  }

  isStoreAdmin(): boolean {
    return this.appType === AppType.STORE_ADMIN;
  }

  isStoreEcommerce(): boolean {
    return this.appType === AppType.STORE_ECOMMERCE;
  }

  // Domain Type getters (LEGACY)
  get domainType(): string {
    return this.domain_config$$.value.domainType;
  }

  // Branding getters
  get branding(): BrandingConfig | undefined {
    return this.domain_config$$.value.customConfig?.branding;
  }

  get organizationId(): number | undefined {
    return this.domain_config$$.value.organization_id;
  }

  get storeId(): number | undefined {
    return this.domain_config$$.value.store_id;
  }
}
```

---

## 🎨 Branding Configuration

### Branding Config Interface

```typescript
export interface BrandingConfig {
  name: string;
  primary_color: string;
  secondary_color: string;
  accent_color: string;
  background_color: string;
  surface_color: string;
  text_color: string;
  text_secondary_color: string;
  text_muted_color: string;
  logo_url?: string;
  favicon_url?: string;
  custom_css?: string;
}

export interface FontsConfig {
  primary: string;
  secondary: string;
  headings: string;
}

export interface PublicationConfig {
  store_published: boolean;
  ecommerce_enabled: boolean;
  landing_enabled: boolean;
  maintenance_mode: boolean;
  maintenance_message?: string;
  allow_public_access: boolean;
}

export interface EcommerceConfig {
  enabled: boolean;
  slider?: { enable: boolean; photos: Array<...> };
  inicio?: { titulo?: string; parrafo?: string; ... };
  catalog?: { products_per_page: number; ... };
  cart?: { allow_guest_checkout: boolean; ... };
  checkout?: { require_registration: boolean; ... };
}
```

### Applying Theme

**File:** `app/app.component.ts`

```typescript
import { Component, OnInit } from '@angular/core';
import { AppConfigService } from '@/app/core/services/app-config.service';
import { BrandingConfig } from '@/app/core/models/domain-config.interface';

@Component({
  selector: 'app-root',
  template: '<router-outlet />',
})
export class AppComponent implements OnInit {
  constructor(private app_config_service: AppConfigService) {}

  ngOnInit() {
    this.app_config_service.domain_config$.subscribe(config => {
      this.applyBranding(config.customConfig?.branding);
      this.applyFonts(config.customConfig?.fonts);
    });
  }

  private applyBranding(branding?: BrandingConfig) {
    if (!branding) return;

    const root = document.documentElement;

    root.style.setProperty('--brand-name', branding.name);
    root.style.setProperty('--primary-color', branding.primary_color);
    root.style.setProperty('--secondary-color', branding.secondary_color);
    root.style.setProperty('--accent-color', branding.accent_color);
    root.style.setProperty('--background-color', branding.background_color);
    root.style.setProperty('--surface-color', branding.surface_color);
    root.style.setProperty('--text-color', branding.text_color);
    root.style.setProperty('--text-secondary-color', branding.text_secondary_color);
    root.style.setProperty('--text-muted-color', branding.text_muted_color);

    // Apply favicon
    if (branding.favicon_url) {
      const link = document.querySelector("link[rel~='icon']") as HTMLLinkElement || document.createElement('link');
      link.rel = 'icon';
      link.href = branding.favicon_url;
      document.head.appendChild(link);
    }

    // Apply custom CSS
    if (branding.custom_css) {
      const style_element = document.createElement('style');
      style_element.textContent = branding.custom_css;
      document.head.appendChild(style_element);
    }
  }

  private applyFonts(fonts?: FontsConfig) {
    if (!fonts) return;

    const root = document.documentElement;
    root.style.setProperty('--font-primary', fonts.primary);
    root.style.setProperty('--font-secondary', fonts.secondary);
    root.style.setProperty('--font-headings', fonts.headings);
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
| `core/models/environment.enum.ts` | AppType enum (PRIMARY) |
| `core/models/domain-config.interface.ts` | Config interfaces |
| `core/services/app-config.service.ts` | App config & domain detection |
| `public/dynamic-landing/components/*/` | Landing pages |
| `core/guards/domain-type.guard.ts` | Domain/app type guard |

## 🔄 Migration Notes

### Changes from Legacy `domain_config` approach:

1. **Service renamed:** `DomainConfigService` → `AppConfigService`
2. **Primary enum:** `AppType` instead of `DomainType` for app selection
3. **Config source:** `domain_settings.app_type` instead of `config.app`
4. **Branding source:** `store_settings.branding` instead of `domain_settings.config.branding`
5. **Response format:** Backend returns `app` directly (not nested in `config.app`)

---

## Related Skills

- `vendix-frontend-routing` - Routing patterns
- `vendix-frontend-module` - Module structure
- `vendix-naming-conventions` - Naming conventions (CRITICAL)
