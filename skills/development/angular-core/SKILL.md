---
name: angular-core
description: Guía esencial de Angular 17+ (Standalone, Signals, Inject).
trigger: angular OR frontend OR spa OR typescript OR component
scope: global
---

# Angular Core (Modern Practices)

Esta skill documenta el estándar moderno de Angular (v17+), enfocándose en eliminar boilerplate y mejorar reactividad.

## 1. Standalone Components (Default)

Ya no usamos `NgModules` para cada cosa. Los componentes son `standalone: true`.

```typescript
@Component({
  standalone: true,
  selector: "app-user-profile",
  imports: [CommonModule, UserAvatarComponent], // Importar dependencias directas
  template: `...`,
})
export class UserProfileComponent {}
```

## 2. Signals (State Management)

Reemplaza `BehaviorSubject` para estado local y derivado.

```typescript
export class CounterComponent {
  // Estado Reactivo
  count = signal(0);

  // Estado Derivado (Computed)
  double = computed(() => this.count() * 2);

  increment() {
    this.count.update((n) => n + 1);
  }
}
```

## 3. Dependency Injection (`inject`)

Preferimos `inject()` sobre inyección en constructor para mayor flexibilidad y tipado.

```typescript
export class UserParams {
  // Antes: constructor(private route: ActivatedRoute) {}
  private route = inject(ActivatedRoute);

  id = this.route.snapshot.params["id"];
}
```

## 4. Control Flow (Nuevo Web Syntax)

Adiós `*ngIf`, hola `@if`.

```html
@if (isLoggedIn()) {
<user-dashboard />
} @else {
<login-page />
} @for (item of items(); track item.id) {
<item-card [data]="item" />
}
```

## Referencia

- Generado con Context7 / Angular.dev
