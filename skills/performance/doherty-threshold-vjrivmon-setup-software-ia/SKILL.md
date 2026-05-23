---
name: doherty-threshold
description:
  Mantén tiempos de respuesta bajo 400ms para mantener la atención del usuario.
  Use cuando optimice performance, diseñe feedback de carga, o evalúe latencia
  percibida.
metadata:
  author: ux-ui-skills
  version: "1.0"
  category: cognitive-laws
---

# Umbral de Doherty

## Resumen

La productividad se dispara cuando una computadora y sus usuarios interactúan a
un ritmo que asegura que ninguno tiene que esperar por el otro. El umbral óptimo
es <400ms.

## Origen

- **Autores**: Walter J. Doherty y Ahrvind J. Thadani (IBM)
- **Año**: 1982
- **Fuente**: "The Economic Value of Rapid Response Time" - IBM Systems Journal

## Umbrales de Respuesta

| Tiempo     | Percepción     | Acción Recomendada             |
| ---------- | -------------- | ------------------------------ |
| <100ms     | Instantáneo    | Feedback directo               |
| 100-300ms  | Inmediato      | Transiciones suaves            |
| 300-1000ms | Espera notable | Indicador de actividad         |
| 1-10s      | Espera larga   | Progress bar + mensaje         |
| >10s       | Interrupción   | Background task + notificación |

## Fundamento Psicológico

La atención humana opera en ciclos. Respuestas bajo 400ms mantienen al usuario
en estado de "flujo" donde la tarea se siente continua. Sobre este umbral, el
usuario experimenta una "interrupción" cognitiva que rompe la concentración y
requiere re-engagement.

## Aplicación en Diseño

### Optimización de Performance

- Code splitting para cargas iniciales rápidas
- Lazy loading de contenido no visible
- Caching agresivo de recursos estáticos
- CDN para reducir latencia geográfica

### Percepción de Velocidad

- Skeleton screens en lugar de spinners
- Optimistic UI (asumir éxito)
- Animaciones que "distraen" durante cargas
- Progressive rendering de contenido

### Feedback Inmediato

- Estados hover/active instantáneos
- Animaciones de confirmación
- Progress indicators apropiados al tiempo
- Mensajes de estado durante operaciones

### Operaciones Largas

- Background processing con notificaciones
- Estimaciones de tiempo restante
- Permitir otras acciones durante espera
- Confirmación clara al completar

## Ejemplos

- **Facebook**: Optimistic UI al dar like
- **Google**: Resultados mientras escribes (<200ms)
- **Slack**: Mensajes aparecen instantáneamente (local-first)
- **GitHub**: Skeleton loading en feeds
- **Stripe Dashboard**: Real-time updates sin refresh

## Anti-patterns

- ❌ Spinners para operaciones <1 segundo
- ❌ Bloquear UI durante requests
- ❌ Páginas que tardan >3s en cargar
- ❌ Formularios que no responden al submit
- ❌ Sin feedback durante operaciones largas

## Métricas

- **Time to First Byte (TTFB)**: <200ms ideal
- **First Contentful Paint (FCP)**: <1.8s
- **Largest Contentful Paint (LCP)**: <2.5s
- **Time to Interactive (TTI)**: <3.8s
- **Total Blocking Time (TBT)**: <300ms

## Principios Relacionados

- [[nielsen-visibility]] - Feedback del estado del sistema
- [[cognitive-load]] - Esperas aumentan carga cognitiva
- [[feedback-principle]] - Respuesta a acciones del usuario

## Referencias

- Doherty, W.J. & Thadani, A.J. (1982). "The Economic Value of Rapid Response
  Time"
- Nielsen, J. (1993). "Response Times: The 3 Important Limits"
- https://lawsofux.com/doherty-threshold/
