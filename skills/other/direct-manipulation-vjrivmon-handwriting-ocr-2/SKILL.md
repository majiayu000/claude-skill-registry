---
name: direct-manipulation
description:
  Los usuarios interactúan directamente con objetos en lugar de comandos
  abstractos. Use cuando diseñe editores, interfaces drag-and-drop, o sistemas
  de manipulación visual.
metadata:
  author: ux-ui-skills
  version: "1.0"
  category: design-principles
---

# Manipulación Directa

## Resumen

Los usuarios interactúan directamente con objetos en pantalla, viendo el
resultado inmediato de sus acciones. Es más intuitivo que ingresar comandos o
navegar menús.

## Origen

- **Autor**: Ben Shneiderman
- **Año**: 1983
- **Fuente**: "Direct Manipulation: A Step Beyond Programming Languages"

## Características

### Visibilidad de Objetos

- Objetos de interés siempre visibles
- Estado actual representado visualmente
- Opciones disponibles perceptibles
- Sin comandos abstractos

### Acciones Incrementales

- Operaciones pequeñas y reversibles
- Feedback inmediato
- Cambios visibles en tiempo real
- Exploración sin riesgo

### Reversibilidad

- Cada acción se puede deshacer
- Estados anteriores accesibles
- Errores fácilmente corregibles
- Experimentación segura

## Aplicación en Diseño

### Drag and Drop

- Mover archivos arrastrando
- Reordenar listas
- Organizar layouts
- Conexiones visuales (diagramas)

### Resize y Transform

- Handles para redimensionar
- Rotate con gestos
- Crop con marquee
- Scale con pinch

### Editores Visuales

- WYSIWYG text editors
- Design tools (Figma, Sketch)
- Video editors (timeline)
- Code editors (live preview)

### Controles Interactivos

- Sliders en lugar de inputs numéricos
- Color pickers visuales
- Maps con pan/zoom
- Charts interactivos

## Ejemplos

- **Figma**: Diseño completamente visual
- **Trello**: Cards que se arrastran entre columnas
- **Google Maps**: Pan, zoom, street view
- **iOS Photos**: Gestos para editar
- **Notion**: Bloques arrastrables

## Anti-patterns

- ❌ Comandos de texto para acciones visuales
- ❌ Formularios para lo que podría ser visual
- ❌ Sin feedback durante la manipulación
- ❌ Acciones no reversibles
- ❌ Manipulación sin mostrar resultado

## Beneficios

- Menor curva de aprendizaje
- Mayor sensación de control
- Exploración más natural
- Errores más fáciles de detectar
- Más engagement

## Métricas

- **Task Completion Time**: Más rápido con manipulación directa
- **Error Rate**: Errores detectados durante acción
- **Learning Time**: Tiempo para dominar
- **User Satisfaction**: Preferencia por interfaces directas

## Principios Relacionados

- [[affordances]] - Objetos que invitan a manipulación
- [[feedback-principle]] - Resultado inmediato visible
- [[nielsen-user-control]] - Control directo del usuario

## Referencias

- Shneiderman, B. (1983). "Direct Manipulation: A Step Beyond Programming
  Languages"
- Hutchins, E. et al. (1985). "Direct Manipulation Interfaces"
- https://www.interaction-design.org/literature/article/direct-manipulation
