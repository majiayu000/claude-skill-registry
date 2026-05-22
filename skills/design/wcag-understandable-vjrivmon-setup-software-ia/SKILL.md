---
name: wcag-understandable
description:
  Principio 3 de WCAG - contenido comprensible para todos. Use cuando escriba
  contenido, diseñe flujos, o implemente comportamientos predecibles.
metadata:
  author: ux-ui-skills
  version: "1.0"
  category: accessibility
---

# WCAG: Comprensible

## Resumen

El tercer principio de WCAG establece que la información y la operación de la
interfaz deben ser comprensibles. Los usuarios deben poder entender tanto el
contenido como cómo operar la interfaz.

## Directrices

### 3.1 Legible

- Idioma de la página especificado
- Idioma de partes especificado cuando difiere
- Palabras inusuales explicadas
- Abreviaturas expandidas
- Nivel de lectura apropiado

```html
<!-- Idioma de página -->
<html lang="es">
  <!-- Cambio de idioma en parte -->
  <p>
    La palabra <span lang="en">accessibility</span> significa accesibilidad.
  </p>
</html>
```

#### Nivel de Lectura

- Apuntar a nivel de secundaria (8vo-9no grado)
- Oraciones cortas
- Vocabulario común
- Explicar términos técnicos
- Alternativas simplificadas disponibles

### 3.2 Predecible

- Navegación consistente
- Identificación consistente
- Sin cambios de contexto inesperados
- Interacciones predecibles

#### Consistencia

- Menús en la misma posición
- Mismos iconos para mismas acciones
- Comportamientos uniformes
- Patrones repetidos

```html
<!-- Malo: cambio de contexto en focus -->
<select onchange="window.location=this.value">
  <option>Seleccionar...</option>
  <option value="/page1">Página 1</option>
</select>

<!-- Bueno: requiere acción explícita -->
<select id="pages">
  <option>Seleccionar...</option>
  <option value="/page1">Página 1</option>
</select>
<button onclick="goToPage()">Ir</button>
```

### 3.3 Asistencia de Input

- Identificación de errores
- Labels e instrucciones
- Sugerencias de error
- Prevención de errores

#### Errores

- Identificar qué campo tiene error
- Describir el error en texto
- Sugerir cómo corregirlo
- Permitir revisar antes de submit final

```html
<!-- Error message asociado -->
<label for="email">Email</label>
<input id="email" type="email" aria-describedby="email-error" />
<div id="email-error" class="error">
  Ingresa un email válido, por ejemplo: nombre@ejemplo.com
</div>
```

## Criterios de Éxito Clave

### Formularios Accesibles

- Labels visibles y asociados
- Instrucciones antes del input
- Errores específicos y constructivos
- Formato esperado indicado

```html
<label for="phone">
  Teléfono
  <span class="hint">(formato: 555-123-4567)</span>
</label>
<input
  id="phone"
  type="tel"
  pattern="[0-9]{3}-[0-9]{3}-[0-9]{4}"
  aria-describedby="phone-hint"
/>
<div id="phone-hint" class="visually-hidden">
  Ingresa 10 dígitos separados por guiones
</div>
```

### Prevención de Errores

- Confirmación antes de acciones irreversibles
- Revisión de datos antes de submit
- Capacidad de corregir
- Reversibilidad cuando posible

## Aplicación Práctica

### Contenido

- Plain language
- Estructura clara con headings
- Párrafos cortos
- Listas para múltiples items
- Definiciones de términos técnicos

### Navegación

- Misma estructura en todas las páginas
- Breadcrumbs consistentes
- Búsqueda disponible
- Mapa del sitio

### Formularios

- Un concepto por pregunta
- Progreso visible en forms largos
- Autoguardado de drafts
- Resumen antes de submit

### Errores

- En línea con el campo
- Color + icono + texto
- Lenguaje no técnico
- Solución sugerida

## Ejemplos

- **Gov.uk**: Lenguaje claro, guías de estilo
- **Mailchimp**: Mensajes de error amigables
- **Stripe**: Validación en tiempo real con ayuda
- **TurboTax**: Guía paso a paso comprensible

## Anti-patterns

- ❌ Jerga técnica sin explicación
- ❌ "Error 500" sin contexto
- ❌ Navegación que cambia entre páginas
- ❌ Submit sin confirmación en acciones críticas
- ❌ Campos sin labels visibles

## Métricas

- **Readability Score**: Flesch-Kincaid, SMOG
- **Error Recovery Rate**: Usuarios que corrigen errores
- **Task Completion**: Sin consultar ayuda
- **Consistency Audit**: Variaciones en UI

## Principios Relacionados

- [[wcag-operable]] - Principio anterior
- [[wcag-robust]] - Siguiente principio
- [[nielsen-error-recovery]] - Recuperación de errores

## Referencias

- W3C. "WCAG 2.1 Guideline 3: Understandable"
- Plain Language Association International
- https://www.nngroup.com/articles/plain-language-experts/
