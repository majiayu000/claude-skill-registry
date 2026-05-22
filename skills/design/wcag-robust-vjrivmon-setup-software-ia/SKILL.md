---
name: wcag-robust
description:
  Principio 4 de WCAG - compatibilidad con tecnologías actuales y futuras. Use
  cuando implemente HTML, ARIA, o componentes custom para asegurar
  compatibilidad.
metadata:
  author: ux-ui-skills
  version: "1.0"
  category: accessibility
---

# WCAG: Robusto

## Resumen

El cuarto principio de WCAG establece que el contenido debe ser lo
suficientemente robusto para ser interpretado por una amplia variedad de user
agents, incluyendo tecnologías asistivas.

## Directrices

### 4.1 Compatible

- HTML válido y bien formado
- Nombres, roles, valores determinables
- Mensajes de estado programáticamente determinables

## Criterios de Éxito Clave

### 4.1.1 Parsing (Obsoleto en WCAG 2.2)

- IDs únicos en la página
- Elementos anidados correctamente
- Atributos no duplicados
- Tags cerrados apropiadamente

```html
<!-- Malo: ID duplicado -->
<div id="menu">...</div>
<div id="menu">...</div>

<!-- Bueno: IDs únicos -->
<div id="main-menu">...</div>
<div id="footer-menu">...</div>
```

### 4.1.2 Nombre, Rol, Valor

Todo componente de UI debe tener:

- **Nombre**: Label accesible
- **Rol**: Qué tipo de componente es
- **Estado/Valor**: Estado actual

```html
<!-- Nativo: automáticamente accesible -->
<button>Guardar</button>
<input type="checkbox" checked />

<!-- Custom: necesita ARIA -->
<div role="button" aria-label="Guardar" tabindex="0">💾</div>

<div role="checkbox" aria-checked="true" tabindex="0">✓</div>
```

### 4.1.3 Mensajes de Estado

Los mensajes que informan al usuario deben ser anunciados por screen readers sin
recibir focus.

```html
<!-- Live region para mensajes -->
<div role="status" aria-live="polite">Guardado exitosamente</div>

<div role="alert" aria-live="assertive">Error: No se pudo guardar</div>
```

## ARIA (Accessible Rich Internet Applications)

### Primera Regla de ARIA

> Si puedes usar un elemento HTML nativo con la semántica requerida, úsalo.

### Roles Comunes

```html
<!-- Landmarks -->
<nav role="navigation">
  <!-- o simplemente <nav> -->
  <main role="main">
    <!-- o simplemente <main> -->
    <aside role="complementary">
      <!-- o simplemente <aside> -->

      <!-- Widgets -->
      <div role="button">
        <!-- mejor usar <button> -->
        <div role="tablist">
          <div role="dialog">
            <div role="alert"></div>
          </div>
        </div>
      </div>
    </aside>
  </main>
</nav>
```

### Estados y Propiedades

```html
<!-- Estados -->
aria-expanded="true|false" aria-selected="true|false" aria-hidden="true|false"
aria-disabled="true|false"

<!-- Propiedades -->
aria-label="Descripción" aria-labelledby="id-del-label"
aria-describedby="id-de-descripcion" aria-controls="id-del-elemento-controlado"
```

## Aplicación Práctica

### Componentes Custom

```html
<!-- Tabs accesibles -->
<div role="tablist">
  <button role="tab" aria-selected="true" aria-controls="panel-1" id="tab-1">
    Tab 1
  </button>
  <button role="tab" aria-selected="false" aria-controls="panel-2" id="tab-2">
    Tab 2
  </button>
</div>
<div role="tabpanel" id="panel-1" aria-labelledby="tab-1">Contenido Tab 1</div>
```

### Modales

```html
<div role="dialog" aria-modal="true" aria-labelledby="modal-title">
  <h2 id="modal-title">Confirmar acción</h2>
  <p>¿Estás seguro?</p>
  <button>Confirmar</button>
  <button>Cancelar</button>
</div>
```

### Actualizaciones Dinámicas

```html
<!-- Contador de items -->
<div aria-live="polite" aria-atomic="true">3 items en el carrito</div>

<!-- Notificaciones -->
<div role="status">Mensaje enviado</div>
```

## Testing de Robustez

### Herramientas

- **axe DevTools**: Auditoría automática
- **WAVE**: Evaluación visual
- **Lighthouse**: Accessibility score
- **NVDA/VoiceOver**: Testing manual con screen reader

### Checklist

1. ¿HTML es válido?
2. ¿Todos los elementos tienen roles apropiados?
3. ¿Los estados se actualizan correctamente?
4. ¿Las actualizaciones se anuncian?
5. ¿Funciona con screen readers?

## Ejemplos

- **React Aria**: Librería de Adobe para componentes accesibles
- **Headless UI**: Componentes accesibles sin estilos
- **Radix UI**: Primitivos accesibles para React
- **Gov.uk Components**: Referencia de implementación

## Anti-patterns

- ❌ Divs y spans para todo
- ❌ ARIA sin comportamiento correspondiente
- ❌ aria-hidden="true" en contenido importante
- ❌ IDs duplicados
- ❌ Estados que no se actualizan

## Métricas

- **Automated Accessibility Score**: axe, Lighthouse
- **Screen Reader Testing**: Tareas completadas
- **HTML Validation**: W3C Validator
- **ARIA Usage Audit**: Uso correcto de ARIA

## Principios Relacionados

- [[wcag-perceivable]] - Primer principio
- [[wcag-operable]] - Segundo principio
- [[wcag-understandable]] - Tercer principio

## Referencias

- W3C. "WCAG 2.1 Guideline 4: Robust"
- W3C. "WAI-ARIA Authoring Practices"
- https://www.w3.org/WAI/ARIA/apg/
