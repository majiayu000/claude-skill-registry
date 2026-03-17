---
name: nielsen-visibility
description:
  Garantiza que el sistema informe constantemente al usuario sobre su estado.
  Use cuando diseñe feedback visual, loaders, estados de progreso o cualquier
  interacción que requiera confirmación.
metadata:
  author: ux-ui-skills
  version: "1.0"
  category: heuristics
---

# Visibilidad del Estado del Sistema

## Resumen

El sistema debe mantener a los usuarios informados sobre lo que está sucediendo
mediante feedback apropiado y oportuno. Los usuarios nunca deben preguntarse si
su acción fue registrada o qué está haciendo el sistema.

## Origen

- **Autor**: Jakob Nielsen
- **Año**: 1994 (refinado 2020)
- **Fuente**: Nielsen Norman Group - "10 Usability Heuristics for User Interface
  Design"

## Fundamento Psicológico

La incertidumbre genera ansiedad y frustración. Cuando los usuarios no reciben
confirmación de sus acciones, experimentan **disonancia cognitiva** y pueden
repetir acciones innecesariamente. El feedback inmediato activa el sistema de
recompensa del cerebro, reforzando la sensación de control y competencia (Teoría
de la Autodeterminación de Deci & Ryan).

## Aplicación en Diseño

### Feedback Inmediato

- Cambios de estado visual en botones al hacer hover/click
- Animaciones de confirmación (checkmarks, colores)
- Sonidos o vibraciones hapticas en móvil
- Tiempo de respuesta: **<100ms** para sensación instantánea

### Indicadores de Progreso

- **Progress bars** para operaciones >1 segundo
- **Skeleton screens** durante carga de contenido
- **Spinners** solo para operaciones breves (<4 segundos)
- Porcentajes o tiempo estimado para operaciones largas

### Estados del Sistema

- Indicadores de conexión online/offline
- Estado de sincronización (guardado, guardando, error)
- Badges de notificaciones pendientes
- Breadcrumbs para ubicación en navegación

### Confirmaciones Explícitas

- Mensajes de éxito después de acciones (toast notifications)
- Confirmación visual de items agregados al carrito
- Recibos o confirmaciones de transacciones

## Ejemplos

- **Gmail**: Muestra "Enviando...", luego "Mensaje enviado" con opción de
  deshacer
- **Slack**: Indicador de "escribiendo..." cuando otro usuario redacta mensaje
- **Uber**: Mapa en tiempo real con ubicación del conductor y ETA actualizado
- **GitHub**: Progress bar durante push/pull con detalles de archivos
  transferidos
- **macOS**: Animación de "genie" al minimizar ventanas confirma la acción

## Anti-patterns

- ❌ Botones que no cambian de estado al hacer click
- ❌ Formularios que se envían sin confirmación visual
- ❌ Operaciones largas sin indicador de progreso
- ❌ Spinners infinitos sin timeout ni mensaje de error
- ❌ Cambios de estado silenciosos que el usuario no percibe

## Métricas

- **Time to First Feedback**: <100ms después de interacción
- **Perceived Wait Time**: Reducido con skeleton screens vs spinners
- **Error Discovery Time**: Tiempo hasta que usuario nota un problema
- **Repeat Action Rate**: Acciones duplicadas por falta de feedback (debe ser
  ~0%)

## Principios Relacionados

- [[doherty-threshold]] - Tiempos de respuesta óptimos
- [[feedback-principle]] - Principio general de retroalimentación
- [[nielsen-error-recovery]] - Comunicar errores claramente

## Referencias

- Nielsen, J. (1994). "Usability Engineering". Morgan Kaufmann
- Nielsen Norman Group (2020). "10 Usability Heuristics for User Interface
  Design"
- https://www.nngroup.com/articles/visibility-system-status/
