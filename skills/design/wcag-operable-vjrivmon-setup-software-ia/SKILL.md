---
name: wcag-operable
description:
  Principio 2 de WCAG - interfaces operables por todos. Use cuando diseñe
  navegación, interacciones, o cualquier componente que requiera input del
  usuario.
metadata:
  author: ux-ui-skills
  version: "1.0"
  category: accessibility
---

# WCAG: Operable

## Resumen

El segundo principio de WCAG establece que los componentes de la interfaz y la
navegación deben ser operables. Los usuarios deben poder operar la interfaz
independientemente de su método de input.

## Directrices

### 2.1 Accesible por Teclado

- Toda funcionalidad disponible desde teclado
- Sin "trampas de teclado"
- Atajos de teclado configurables
- Tab order lógico

#### Teclas Estándar

- **Tab**: Navegar entre elementos
- **Enter/Space**: Activar
- **Escape**: Cerrar/cancelar
- **Flechas**: Navegar dentro de componentes
- **Home/End**: Primero/último

```html
<!-- Elemento focusable por defecto -->
<button>Click me</button>

<!-- Hacer div focusable (evitar cuando posible) -->
<div role="button" tabindex="0" onkeydown="handleKey(event)">Click me</div>
```

### 2.2 Tiempo Suficiente

- Permitir extender límites de tiempo
- Pausar contenido en movimiento
- No hay límites de tiempo a menos que sea esencial
- Interrupciones controlables

#### Implementación

- Warnings antes de timeout
- Opción de extender sesión
- Autoguardado de trabajo
- Sin carruseles automáticos no pausables

### 2.3 Convulsiones y Reacciones Físicas

- Nada parpadea más de 3 veces por segundo
- Evitar contenido que causa convulsiones
- Animaciones de movimiento desactivables

```css
/* Respetar preferencias del usuario */
@media (prefers-reduced-motion: reduce) {
  * {
    animation: none !important;
    transition: none !important;
  }
}
```

### 2.4 Navegable

- Bypass blocks (skip links)
- Títulos de página descriptivos
- Orden de foco lógico
- Propósito de links claro
- Múltiples formas de encontrar páginas

```html
<!-- Skip link -->
<a href="#main" class="skip-link">Saltar al contenido</a>

<!-- Visible on focus -->
<style>
  .skip-link:not(:focus) {
    position: absolute;
    width: 1px;
    height: 1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
  }
</style>
```

### 2.5 Modalidades de Input

- Gestos simples como alternativa a complejos
- Cancelación de pointer (no activar en down)
- Labels accesibles para controles de voz
- Activación por movimiento desactivable

## Criterios de Éxito Clave

### Focus Visible

- Focus indicator siempre visible
- Alto contraste con el fondo
- No remover outline sin alternativa

```css
/* Malo */
:focus {
  outline: none;
}

/* Bueno */
:focus {
  outline: 2px solid #005fcc;
  outline-offset: 2px;
}

/* Mejor - solo keyboard */
:focus:not(:focus-visible) {
  outline: none;
}
:focus-visible {
  outline: 2px solid #005fcc;
}
```

### Touch Targets

- Mínimo 44x44 CSS pixels (WCAG 2.2)
- Spacing adecuado entre targets
- Áreas de tap suficientes

## Aplicación Práctica

### Modales/Dialogs

- Focus trapped dentro del modal
- Escape cierra el modal
- Focus retorna al trigger al cerrar
- Aria-modal="true"

### Menús Dropdown

- Abrir con Enter/Space
- Navegar con flechas
- Cerrar con Escape
- Focus visible en opciones

### Formularios

- Tab order sigue visual order
- Labels clickeables
- Error messages asociados
- Submit con Enter

### Carruseles

- Botones de pausa
- Navegación por teclado
- No autoplay si tiene contenido importante

## Ejemplos

- **Slack**: Excelente navegación por teclado
- **GitHub**: Shortcuts de teclado comprensivos
- **Google Docs**: Accesibilidad de teclado completa
- **Notion**: Cmd+K para navegación

## Anti-patterns

- ❌ Solo funciona con mouse
- ❌ Outlines removidos sin alternativa
- ❌ Trampas de focus (no se puede salir)
- ❌ Timeouts sin warning
- ❌ Carruseles automáticos no pausables

## Métricas

- **Keyboard-Only Testing**: Completar tareas sin mouse
- **Focus Order Audit**: Tab sequence lógica
- **Touch Target Size**: Cumplimiento de 44px
- **Time-Based Function Review**: Timeouts documentados

## Principios Relacionados

- [[wcag-perceivable]] - Principio anterior
- [[wcag-understandable]] - Siguiente principio
- [[fitts-law]] - Tamaño de targets

## Referencias

- W3C. "WCAG 2.1 Guideline 2: Operable"
- https://www.w3.org/WAI/WCAG21/Understanding/operable
- WebAIM. "Keyboard Accessibility"
