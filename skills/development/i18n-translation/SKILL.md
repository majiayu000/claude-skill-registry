---
name: i18n-translation
description: "Ensure all user-facing text is translatable via ngx-translate. Use when adding text to UI components, checking for hardcoded strings, or when the user asks about translations."
version: "1.0.0"
author: "@Frontend"

# Auto-invocation configuration
auto_invoke:
  event: "component-creation"
  condition: "file contains hardcoded user-facing strings"

# Required inputs
inputs:
  - component_file: "Path to the component with text"
  - locale: "Target locale (es, en)"

# Skill output
output: "Updated component + translation keys"
---

# I18n Translation Skill

> **Purpose:** Ensure all user-facing text uses translation keys, never hardcoded strings.

## When to Invoke

- Creating new components with visible text
- Adding labels, buttons, messages to templates
- Reviewing components for i18n compliance

## Translation Setup

**Library:** `@ngx-translate/core` + `@ngx-translate/http-loader`

**Files:**

- `apps/web/public_override/assets/i18n/es.json` - Spanish (primary)
- `apps/web/public_override/assets/i18n/en.json` - English

## Key Naming Convention

```
MODULE.SECTION.KEY_NAME
```

**Examples:**

```json
{
  "COMMON": {
    "BUTTONS": {
      "SAVE": "Guardar",
      "CANCEL": "Cancelar",
      "DELETE": "Eliminar",
      "CONFIRM": "Confirmar",
      "CLOSE": "Cerrar",
      "LOADING": "Cargando..."
    },
    "LABELS": {
      "SEARCH": "Buscar",
      "FILTER": "Filtrar",
      "ACTIONS": "Acciones"
    },
    "MESSAGES": {
      "SUCCESS": "Operación exitosa",
      "ERROR": "Ha ocurrido un error",
      "CONFIRM_DELETE": "¿Estás seguro de eliminar?"
    }
  },
  "COMPONENTS": {
    "DATA_TABLE": {
      "NO_DATA": "No hay datos disponibles",
      "LOADING": "Cargando datos...",
      "ROWS_PER_PAGE": "Filas por página",
      "OF": "de"
    },
    "MODAL": {
      "CLOSE": "Cerrar",
      "CONFIRM": "Confirmar",
      "CANCEL": "Cancelar"
    }
  }
}
```

## Component Pattern

### Import TranslateModule

```typescript
import { TranslateModule } from "@ngx-translate/core";

@Component({
  selector: "ui-example",
  imports: [TranslateModule],
  template: ` <button>{{ "COMMON.BUTTONS.SAVE" | translate }}</button> `,
})
export class ExampleComponent {}
```

### Dynamic Values with Parameters

```html
<!-- Translation with parameter -->
<p>{{ 'COMMON.MESSAGES.WELCOME' | translate:{ name: userName() } }}</p>

<!-- In JSON: "WELCOME": "Bienvenido, {{name}}" -->
```

### Pluralization

```json
{
  "ITEMS": {
    "COUNT_0": "Sin elementos",
    "COUNT_1": "1 elemento",
    "COUNT_OTHER": "{{count}} elementos"
  }
}
```

### Async Pipe Alternative

```typescript
import { TranslateService } from "@ngx-translate/core";

export class ExampleComponent {
  private translate = inject(TranslateService);

  // For complex scenarios
  message = computed(() => this.translate.instant("COMMON.MESSAGES.SUCCESS"));
}
```

## Component Checklist

When creating/reviewing components:

- [ ] All visible text uses `| translate` pipe
- [ ] All aria-labels are translatable
- [ ] All placeholder text uses translations
- [ ] All tooltip content is translatable
- [ ] All error messages use translation keys
- [ ] Translation keys are added to ALL locale files

## Prohibited Patterns

```html
<!-- ❌ DON'T: Hardcoded text -->
<button>Save</button>
<button>Guardar</button>

<!-- ❌ DON'T: Mixed languages -->
<p>Click here to {{ 'ACTION' | translate }}</p>

<!-- ✅ DO: Full translation -->
<button>{{ 'COMMON.BUTTONS.SAVE' | translate }}</button>
```

## Shared Component Translations

All shared components should use `COMPONENTS.` prefix:

```json
{
  "COMPONENTS": {
    "BUTTON": {
      "LOADING": "Cargando..."
    },
    "INPUT": {
      "REQUIRED": "Este campo es requerido",
      "INVALID_EMAIL": "Email inválido"
    },
    "EMPTY_STATE": {
      "DEFAULT_TITLE": "Sin datos",
      "DEFAULT_MESSAGE": "No hay información disponible"
    },
    "DATA_TABLE": {
      "NO_RESULTS": "No se encontraron resultados",
      "LOADING": "Cargando...",
      "SELECT_ALL": "Seleccionar todo",
      "ROWS_PER_PAGE": "Filas por página",
      "PAGE_OF": "Página {{current}} de {{total}}"
    },
    "TOAST": {
      "CLOSE": "Cerrar"
    }
  }
}
```

## Validation

After adding translations:

1. Check all locale files have the same keys
2. Verify no hardcoded text in templates
3. Test with different locales
4. Verify placeholders render correctly
