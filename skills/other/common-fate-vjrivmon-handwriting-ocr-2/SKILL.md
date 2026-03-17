---
name: common-fate
description:
  Elementos que se mueven juntos se perciben como grupo. Use cuando diseñe
  animaciones, transiciones, drag-and-drop, o elementos que reaccionan en
  conjunto.
metadata:
  author: ux-ui-skills
  version: "1.0"
  category: gestalt
---

# Principio de Destino Común

## Resumen

Los elementos que se mueven en la misma dirección y velocidad se perciben como
relacionados o parte del mismo grupo, incluso si tienen otras características
diferentes.

## Origen

- **Escuela**: Psicología de la Gestalt
- **Año**: ~1920s
- **Autores principales**: Max Wertheimer, Kurt Koffka, Wolfgang Köhler

## Fundamento Psicológico

El sistema visual evolucionó para detectar objetos en movimiento (depredadores,
presas). Elementos que comparten movimiento se interpretan como una unidad
porque en la naturaleza, partes del mismo objeto se mueven juntas.

## Aplicación en Diseño

### Animaciones de Grupo

- Cards que se reorganizan juntas al filtrar
- Elementos que entran en escena coordinadamente
- Collapse/expand de secciones como unidad
- Parallax con capas que se mueven a diferentes velocidades

### Drag and Drop

- Múltiples items seleccionados se mueven juntos
- Ghost preview muestra todos los elementos
- Drop zones que se expanden juntas
- Elementos que "hacen espacio" al mismo tiempo

### Transiciones de Estado

- Loading states que afectan grupos
- Hover effects que propagan a relacionados
- Selection que destaca grupo completo
- Ripple effects coordinados

### Scroll Behaviors

- Sticky headers que se mueven con scroll
- Elementos que aparecen/desaparecen en sync
- Carousels con movimiento coordinado
- Parallax que agrupa por velocidad

## Ejemplos

- **Trello**: Mover card mueve todos sus elementos
- **macOS Mission Control**: Ventanas de misma app agrupadas
- **Figma**: Selección múltiple se mueve como unidad
- **iOS Folders**: Apps dentro se mueven juntas
- **Google Photos**: Grid items que se reorganizan

## Anti-patterns

- ❌ Elementos relacionados que se animan independientemente
- ❌ Transiciones desincronizadas en grupos
- ❌ Drag que no muestra todos los items seleccionados
- ❌ Scroll con elementos relacionados a diferentes velocidades
- ❌ Hover effects que no propagan a elementos asociados

## Métricas

- **Animation Sync Score**: Coordinación de movimientos
- **Group Recognition**: Usuarios identifican grupos por movimiento
- **Interaction Cohesion**: Consistencia en comportamientos de grupo
- **Motion Hierarchy**: Claridad en relaciones por movimiento

## Principios Relacionados

- [[proximity]] - Cercanía espacial también agrupa
- [[similarity]] - Similitud visual agrupa
- [[continuity]] - Movimiento en trayectorias continuas

## Referencias

- Wertheimer, M. (1923). "Laws of Organization in Perceptual Forms"
- Chang, D. & Nesbitt, K. (2006). "Developing Gestalt-based design guidelines
  for multi-sensory displays"
- https://www.interaction-design.org/literature/article/the-law-of-common-fate
