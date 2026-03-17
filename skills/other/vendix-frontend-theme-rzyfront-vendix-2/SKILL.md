---
name: vendix-frontend-theme
description: Theme and branding patterns.
metadata:
  scope: [root]
  auto_invoke: "Styling and Theming"
---
# Vendix Frontend Theme & Branding

> **ThemeService, Branding Configuration & Visual Styling** - Gestión de temas, branding y variables CSS para multi-tenancia.

## 🎯 Theme Management

**Vendix usa un sistema centralizado de branding:**
- **ThemeService** - Transforma y aplica configuración visual
- **Variables CSS** - Aplicadas dinámicamente por dominio
- **BrandingGeneratorHelper** (Backend) - Genera branding estándar
- **Formato snake_case → camelCase** - Transformación automática

---

## 📋 Formato Estándar de Branding

### Backend (snake_case)

```typescript
// Retornado por /public/domains/resolve/:hostname
{
  name: "Mi Tienda",
  theme: "light",
  logo_url: "https://...",
  favicon_url: "https://...",
  primary_color: "#7ED7A5",
  secondary_color: "#2F6F4E",
  accent_color: "#FFFFFF",
  background_color: "#F4F4F4",
  surface_color: "#FFFFFF",
  text_color: "#222222",
  border_color: "#E5E7EB",
  text_secondary_color: "#555555",
  text_muted_color: "#AAAAAA"
}
```

### Frontend (camelCase)

```typescript
// BrandingConfig - usado internamente
{
  colors: {
    primary: "#7ED7A5",
    secondary: "#2F6F4E",
    accent: "#FFFFFF",
    background: "#F4F4F4",
    surface: "#FFFFFF",
    text: {
      primary: "#222222",
      secondary: "#555555",
      muted: "#AAAAAA"
    }
  },
  fonts: {
    primary: "Inter, sans-serif",
    secondary: string,
    headings: string
  },
  logo: {
    url: "https://...",
    alt: "Mi Tienda"
  },
  favicon: "https://...",
  customCSS: string
}
```

---

## 🎨 ThemeService

### Location
`apps/frontend/src/app/core/services/theme.service.ts`

### Core Methods

```typescript
import { Injectable } from '@angular/core';
import { BrandingConfig } from '../models/tenant-config.interface';

@Injectable({ providedIn: 'root' })
export class ThemeService {
  // Aplica configuración completa de branding
  async applyAppConfiguration(appConfig: AppConfig): Promise<void>

  // Aplica solo branding
  async applyBranding(brandingConfig: BrandingConfig): Promise<void>

  // Transforma formato backend → frontend (CRÍTICO)
  transformBrandingFromApi(apiBranding: any): BrandingConfig

  // Carga fuentes externas
  async loadFont(fontFamily: string): Promise<void>

  // Inyecta CSS personalizado
  injectCustomCSS(css: string, id: string): void

  // Actualiza favicon
  updateFavicon(faviconUrl: string): void

  // Resetea todo al default
  resetTheme(): void
}
```

### CSS Variables Aplicadas

```css
:root {
  /* Colores */
  --color-primary: #7ED7A5;
  --color-secondary: #2F6F4E;
  --color-accent: #FFFFFF;
  --color-background: #F4F4F4;
  --color-surface: #FFFFFF;
  --color-text-primary: #222222;
  --color-text-secondary: #555555;
  --color-text-muted: #AAAAAA;

  /* Fuentes */
  --font-primary: "Inter, sans-serif";
  --font-secondary: string;
  --font-headings: string;
}
```

---

## 🔄 Flujo de Branding

```
1. Backend: BrandingGeneratorHelper.generateBranding()
   → Genera config en snake_case

2. Domain Settings (DB)
   → Almacena config.branding

3. API: /public/domains/resolve/:hostname
   → Retorna domain_resolution con config

4. AppConfigService.setupConfig()
   → Obtiene domain_config

5. ThemeService.transformBrandingFromApi()
   → Transforma snake_case → camelCase

6. ThemeService.applyBranding()
   → Aplica CSS variables a :root

7. Componentes
   → Usan var(--color-primary)
```

---

## 💡 Uso en Componentes

### ✅ CORRECTO - Usando CSS Variables

```scss
// component.scss
.my-button {
  background-color: var(--color-primary, #7ED7A5);
  color: var(--color-text-primary, #222222);
  border: 1px solid var(--color-border, #E5E7EB);
}

.my-card {
  background: var(--color-surface, #FFFFFF);
  border-radius: var(--border-radius, 8px);
}
```

### ❌ WRONG - Colores hardcoded

```scss
// NO hacer esto
.my-button {
  background-color: #7ED7A5;  // ❌ Hardcoded
  color: #222222;              // ❌ No dinámico
}
```

---

## 🔧 Integración con AppConfigService

### En app-config.service.ts

```typescript
import { ThemeService } from './theme.service';

@Injectable({ providedIn: 'root' })
export class AppConfigService {
  private http = inject(HttpClient);
  private themeService = inject(ThemeService);

  private buildAppConfig(domainConfig: DomainConfig): AppConfig {
    return {
      environment: domainConfig.environment,
      domainConfig,
      routes: this.resolveRoutes(domainConfig),
      layouts: [],
      // ✅ Usa ThemeService para transformación
      branding: this.themeService.transformBrandingFromApi(
        domainConfig.customConfig?.branding || {}
      ),
    };
  }
}
```

### En config.effects.ts

```typescript
import { ThemeService } from '../../services/theme.service';

@Injectable()
export class ConfigEffects {
  private themeService = inject(ThemeService);

  initializeAppSuccess$ = createEffect(
    () =>
      this.actions$.pipe(
        ofType(ConfigActions.initializeAppSuccess),
        tap(({ config }) => {
          // ✅ Aplica branding al cargar config
          this.themeService.applyAppConfiguration(config);
        }),
      ),
    { dispatch: false },
  );
}
```

---

## 🎯 Backend: BrandingGeneratorHelper

### Location
`apps/backend/src/common/helpers/branding-generator.helper.ts`

### Uso en Servicios

```typescript
import { BrandingGeneratorHelper } from '@common/helpers/branding-generator.helper';

@Injectable()
export class OnboardingWizardService {
  private brandingGeneratorHelper = inject(BrandingGeneratorHelper);

  async setupAppConfig(dto: SetupAppConfigDto) {
    // ✅ Genera branding estándar
    const branding = this.brandingGeneratorHelper.generateBranding({
      name: 'Mi Tienda',
      primaryColor: '#7ED7A5',
      secondaryColor: '#2F6F4E',
      theme: 'light',
    });

    // Guarda en DB con formato snake_case
    await this.prisma.domain_settings.create({
      data: {
        hostname: 'mitienda-org.vendix.com',
        config: {
          app: 'ORG_LANDING',
          branding: branding, // ✅ Formato estándar
        },
      },
    });
  }
}
```

---

## 🚨 Reglas Críticas

### ✅ SIEMPRE HACER

1. **Usar ThemeService.transformBrandingFromApi()** - Single source of truth
2. **Usar variables CSS en componentes** - Con fallback values
3. **Usar BrandingGeneratorHelper en backend** - Para generar branding
4. **Proporcionar fallbacks** - `var(--color-primary, #7ED7A5)`
5. **Formatear colores como hex** - `#RRGGBB` o `#RGB`

### ❌ NUNCA HACER

1. **NO duplicar lógica de transformación** - Usar ThemeService
2. **NO hardcodear colores** - Usar var(--color-*)
3. **NO crear formatos custom** - Usar el estándar
4. **NO omitir fallbacks** - Siempre dar valor default
5. **NO transformar manualmente** - Dejar que ThemeService lo haga

---

## 🔍 Archivos Clave

| Archivo | Propósito |
|---------|-----------|
| `core/services/theme.service.ts` | Servicio de temas |
| `core/services/app-config.service.ts` | Configuración de app |
| `core/store/config/config.effects.ts` | Aplica branding |
| `core/models/tenant-config.interface.ts` | BrandingConfig |
| Backend: `common/helpers/branding-generator.helper.ts` | Genera branding |

---

## 🧪 Testing

### Verificar Variables CSS

```typescript
// En consola del navegador
getComputedStyle(document.documentElement)
  .getPropertyValue('--color-primary')
// → "#7ED7A5"
```

### Verificar Transformación

```typescript
// theme.service.ts
const apiBranding = {
  primary_color: "#7ED7A5",
  secondary_color: "#2F6F4E",
};

const transformed = this.transformBrandingFromApi(apiBranding);

console.log(transformed.colors.primary);
// → "#7ED7A5" ✅
```

---

## 📚 Related Skills

- `vendix-frontend-domain` - Domain resolution y config
- `vendix-frontend-state` - State management
- `vendix-frontend-component` - Component structure
- `vendix-naming-conventions` - Naming conventions (CRITICAL)
