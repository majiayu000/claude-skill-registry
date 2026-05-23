---
name: affordances
description:
  Los objetos deben sugerir cómo se usan. Use cuando diseñe botones, controles
  interactivos, o cualquier elemento que invite a la acción.
metadata:
  author: ux-ui-skills
  version: "1.0"
  category: design-principles
---

# Affordances (Prestaciones)

## Resumen

Las affordances son propiedades de un objeto que sugieren cómo puede ser usado.
Un botón que parece presionable tiene buena affordance. Los usuarios deberían
saber qué hacer sin instrucciones.

## Origen

- **Autor**: James J. Gibson (original), Don Norman (aplicación al diseño)
- **Año**: 1966 (Gibson), 1988 (Norman)
- **Fuente**: "The Design of Everyday Things" - Don Norman

## Tipos de Affordances

### Affordances Físicas (Gibson)

- Propiedades reales del objeto
- Una silla "afford" sentarse
- Relación entre actor y objeto

### Affordances Percibidas (Norman)

- Lo que el usuario _cree_ que puede hacer
- Más relevante para UI digital
- Señales visuales que sugieren uso

### Signifiers

- Señales explícitas de cómo usar algo
- Labels, iconos, instrucciones
- Complementan affordances implícitas

## Aplicación en Diseño

### Botones

- Aspecto 3D o sombreado sugiere "presionable"
- Estados hover que invitan al click
- Tamaño táctil adecuado
- Color que indica interactividad

### Links

- Subrayado o color distintivo
- Cursor que cambia a pointer
- Estados visited diferenciados
- Texto que sugiere acción

### Formularios

- Campos con borde que invita a escribir
- Placeholders que muestran formato esperado
- Labels claros de qué introducir
- Checkboxes que parecen marcables

### Controles

- Sliders con affordance de arrastrar
- Toggle switches que invitan a cambiar
- Dropdowns con flecha indicativa
- Drag handles visibles

## Ejemplos

- **iOS**: Botones con esquinas redondeadas y color
- **Material Design**: Elevation para elementos interactivos
- **Scrollbars**: Affordance de arrastre
- **Input fields**: Borde que invita a escribir
- **Door handles**: Push plates vs pull handles

## Anti-patterns

- ❌ Links que no parecen links
- ❌ Botones planos sin estado hover
- ❌ Áreas clickeables sin señales visuales
- ❌ Texto interactivo sin diferenciación
- ❌ Controles que no sugieren su función

## Métricas

- **Discoverability Score**: % de usuarios que encuentran funciones
- **First Click Accuracy**: Clicks correctos sin ayuda
- **Error Rate**: Clicks en áreas no interactivas
- **Time to First Interaction**: Tiempo para primera acción

## Principios Relacionados

- [[feedback-principle]] - Confirmar que la affordance funcionó
- [[nielsen-visibility]] - Hacer visible lo que es posible
- [[constraints-principle]] - Limitar acciones a las válidas

## Referencias

- Gibson, J.J. (1966). "The Senses Considered as Perceptual Systems"
- Norman, D. (2013). "The Design of Everyday Things"
- https://www.nngroup.com/articles/affordance/
