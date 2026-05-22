---
name: nielsen-user-control
description:
  Proporciona a usuarios control total sobre sus acciones con opciones de
  deshacer y salir. Use cuando diseñe flujos de navegación, acciones
  destructivas, o cualquier operación que el usuario pueda querer revertir.
metadata:
  author: ux-ui-skills
  version: "1.0"
  category: heuristics
---

# Control y Libertad del Usuario

## Resumen

Los usuarios a menudo realizan acciones por error y necesitan una "salida de
emergencia" claramente marcada para abandonar el estado no deseado sin tener que
pasar por un proceso extenso. Soportar deshacer y rehacer es esencial.

## Origen

- **Autor**: Jakob Nielsen
- **Año**: 1994 (refinado 2020)
- **Fuente**: Nielsen Norman Group - "10 Usability Heuristics for User Interface
  Design"

## Fundamento Psicológico

La sensación de control es fundamental para el bienestar psicológico (Locus de
Control de Rotter). Cuando los usuarios sienten que pueden explorar sin
consecuencias irreversibles, experimentan menor ansiedad y mayor disposición a
experimentar. El **efecto de aversión a la pérdida** (Kahneman) hace que las
acciones irreversibles sean especialmente estresantes.

## Aplicación en Diseño

### Acciones Reversibles

- **Ctrl+Z / Cmd+Z** para deshacer en todas las aplicaciones
- Papelera con retención temporal antes de eliminación permanente
- Historial de versiones para documentos
- "Deshacer envío" con ventana de tiempo (Gmail: 30 segundos)

### Navegación Libre

- Botón "Atrás" funcional en todos los contextos
- Breadcrumbs para saltar a cualquier nivel
- Logo que siempre lleva a home
- Opción de "Salir" o "Cancelar" visible en modales

### Confirmación de Acciones Críticas

- Diálogos de confirmación para eliminaciones permanentes
- Re-autenticación para cambios sensibles
- Preview antes de publicar
- Período de gracia antes de ejecutar (timer countdown)

### Escape Claro

- Tecla ESC cierra modales y popups
- "X" visible para cerrar overlays
- "Cancelar" junto a "Confirmar" en formularios
- Opción de abandonar procesos multi-paso

## Ejemplos

- **Gmail**: "Deshacer" durante 30 segundos después de enviar
- **Google Docs**: Historial de versiones con restauración
- **Photoshop**: Historial de acciones con múltiples niveles de undo
- **iOS**: Shake para deshacer texto
- **GitHub**: Branch protection previene pushes accidentales a main

## Anti-patterns

- ❌ Eliminación instantánea sin confirmación ni recuperación
- ❌ Formularios que pierden datos al navegar accidentalmente
- ❌ Modales sin botón de cierre visible
- ❌ Procesos de checkout que no permiten volver atrás
- ❌ Acciones batch sin opción de rollback

## Métricas

- **Undo Usage Rate**: Frecuencia de uso de deshacer (indica exploración segura)
- **Abandonment Rate**: Usuarios que abandonan por no poder regresar
- **Recovery Success Rate**: % de usuarios que recuperan de errores
- **Time to Exit**: Tiempo para salir de estados no deseados

## Principios Relacionados

- [[poka-yoke]] - Prevención de errores por diseño
- [[nielsen-error-recovery]] - Recuperación elegante de errores
- [[constraints-principle]] - Limitar acciones peligrosas

## Referencias

- Nielsen, J. (1994). "Usability Engineering". Morgan Kaufmann
- Kahneman, D. (2011). "Thinking, Fast and Slow". Farrar, Straus and Giroux
- https://www.nngroup.com/articles/user-control-and-freedom/
