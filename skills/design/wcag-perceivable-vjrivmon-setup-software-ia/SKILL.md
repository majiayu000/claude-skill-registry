---
name: wcag-perceivable
description:
  Principio 1 de WCAG - contenido perceptible por todos los usuarios. Use cuando
  diseñe contenido multimedia, imágenes, o cualquier información visual o
  auditiva.
metadata:
  author: ux-ui-skills
  version: "1.0"
  category: accessibility
---

# WCAG: Perceptible

## Resumen

El primer principio de WCAG establece que la información y los componentes de la
interfaz deben ser presentados de manera que los usuarios puedan percibirlos. No
puede ser invisible a todos sus sentidos.

## Origen

- **Organización**: W3C (World Wide Web Consortium)
- **Documento**: Web Content Accessibility Guidelines
- **Versión actual**: WCAG 2.1 / 2.2
- **Niveles**: A (mínimo), AA (recomendado), AAA (óptimo)

## Directrices

### 1.1 Alternativas de Texto

- Todas las imágenes deben tener alt text
- Imágenes decorativas: alt=""
- Imágenes informativas: descripción del contenido
- Imágenes complejas: descripción extendida

```html
<!-- Informativa -->
<img src="chart.png" alt="Ventas Q1 2024: $1.2M, +15% vs Q1 2023" />

<!-- Decorativa -->
<img src="divider.png" alt="" role="presentation" />

<!-- Compleja -->
<img src="diagram.png" alt="Diagrama de flujo" aria-describedby="desc" />
<div id="desc">Descripción completa del diagrama...</div>
```

### 1.2 Medios Basados en Tiempo

- Video: captions y transcripciones
- Audio: transcripciones
- Video en vivo: captions en tiempo real
- Audio descripción para ciegos

### 1.3 Adaptable

- Contenido debe poder presentarse de diferentes formas
- Estructura semántica correcta (headings, lists, tables)
- Secuencia de lectura significativa
- No depender solo de características sensoriales

```html
<!-- Malo -->
<div class="big-text">Título</div>

<!-- Bueno -->
<h1>Título</h1>
```

### 1.4 Distinguible

- Contraste de color suficiente
- No usar solo color para transmitir información
- Audio controlable por el usuario
- Texto redimensionable
- Texto como texto, no imágenes

## Criterios de Éxito Clave

### Contraste de Color

- **AA**: 4.5:1 para texto normal, 3:1 para texto grande
- **AAA**: 7:1 para texto normal, 4.5:1 para texto grande
- Texto grande: ≥18pt o ≥14pt bold

### Herramientas de Verificación

- WebAIM Contrast Checker
- axe DevTools
- WAVE
- Lighthouse

## Aplicación Práctica

### Imágenes

- Alt text descriptivo y conciso
- Describir función, no apariencia
- "Botón de búsqueda" no "Lupa azul"
- Evitar "imagen de..."

### Video

- Captions sincronizados
- Transcripción completa
- Audio descripción cuando necesario
- Controles accesibles

### Formularios

- Labels asociados a inputs
- Errores no solo por color
- Instrucciones claras
- Mensajes de error descriptivos

### Color

- Indicadores adicionales (iconos, texto)
- Patrones además de colores en gráficos
- No "haga click en el botón rojo"

## Ejemplos

- **YouTube**: Captions automáticos y manuales
- **GitHub**: Alt text requerido en issues
- **Stripe Docs**: Excelente contraste y estructura
- **Gov.uk**: Modelo de accesibilidad

## Anti-patterns

- ❌ Imágenes de texto
- ❌ Videos sin captions
- ❌ Solo color para indicar estado
- ❌ Contraste insuficiente
- ❌ Alt text genérico ("imagen" o vacío incorrecto)

## Métricas

- **Automated Audit Score**: Lighthouse, axe
- **Manual Review**: Checklist WCAG
- **Contrast Ratio**: Todas las combinaciones de color
- **Screen Reader Testing**: Navegación con NVDA/VoiceOver

## Principios Relacionados

- [[wcag-operable]] - Siguiente principio WCAG
- [[universal-design]] - Diseño para todos
- [[inclusive-design]] - Considerar diversidad

## Referencias

- W3C. "Web Content Accessibility Guidelines (WCAG) 2.1"
- https://www.w3.org/WAI/WCAG21/Understanding/
- WebAIM. "WCAG 2 Checklist"
