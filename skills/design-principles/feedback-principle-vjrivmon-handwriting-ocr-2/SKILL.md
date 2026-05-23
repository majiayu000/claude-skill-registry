---
name: feedback-principle
description:
  El sistema debe informar sobre resultados de acciones del usuario. Use cuando
  diseñe interacciones, estados de carga, confirmaciones, o manejo de errores.
metadata:
  author: ux-ui-skills
  version: "1.0"
  category: design-principles
---

# Principio de Feedback

## Resumen

Cada acción del usuario debe producir feedback perceptible del sistema. Los
usuarios necesitan saber que sus acciones fueron recibidas y qué resultados
produjeron.

## Origen

- **Concepto**: Principio fundamental de teoría de control y HCI
- **Documentado por**: Ben Shneiderman, Don Norman
- **Año**: ~1980s

## Tipos de Feedback

### Feedback Inmediato (<100ms)

- Cambios de estado en botones
- Animaciones de click
- Cursor changes
- Highlights de selección

### Feedback de Proceso (>100ms)

- Loading spinners
- Progress bars
- Skeleton screens
- Mensajes de estado

### Feedback de Resultado

- Confirmaciones de éxito
- Mensajes de error
- Toasts y notificaciones
- Cambios en la UI

### Feedback Pasivo

- Contadores actualizados
- Estados de conexión
- Indicadores de sincronización
- Badges de notificación

## Aplicación en Diseño

### Microinteracciones

- Hover states
- Press/active states
- Animaciones de transición
- Ripple effects

### Estados de Carga

- Spinners apropiados al tiempo
- Skeleton loaders
- Progress bars con %
- Estimaciones de tiempo

### Confirmaciones

- Toast notifications
- Modales de éxito
- Cambios visuales en UI
- Sonidos/haptics

### Errores

- Mensajes claros y accionables
- Highlight de campos con error
- Sugerencias de corrección
- Opción de retry

## Ejemplos

- **Gmail**: "Sending..." → "Sent" → "Undo"
- **Slack**: Checkmark al enviar mensaje
- **GitHub**: Confetti en primer PR
- **Stripe**: Validación de tarjeta en tiempo real
- **macOS**: Bounce en dock al completar

## Anti-patterns

- ❌ Clicks sin respuesta visual
- ❌ Formularios que envían sin confirmación
- ❌ Errores silenciosos
- ❌ Operaciones largas sin indicador
- ❌ Estados que cambian sin notificar

## Métricas

- **Feedback Latency**: Tiempo hasta feedback
- **User Confidence Score**: Certeza de que funcionó
- **Repeat Action Rate**: Acciones repetidas por duda
- **Error Recovery Time**: Tiempo para corregir errores

## Principios Relacionados

- [[nielsen-visibility]] - Visibilidad del estado
- [[doherty-threshold]] - Tiempos de respuesta
- [[affordances]] - Confirmar que la affordance funciona

## Referencias

- Norman, D. (2013). "The Design of Everyday Things"
- Shneiderman, B. (1987). "Designing the User Interface"
- https://www.nngroup.com/articles/response-times-3-important-limits/
