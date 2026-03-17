---
name: mapping-principle
description:
  Los controles deben corresponder naturalmente a sus efectos. Use cuando diseñe
  controles de UI, layouts de controles, o cualquier relación causa-efecto.
metadata:
  author: ux-ui-skills
  version: "1.0"
  category: design-principles
---

# Principio de Mapping (Correspondencia)

## Resumen

La relación entre controles y sus efectos debe ser obvia y natural. Un buen
mapping aprovecha analogías físicas y espaciales para que el uso sea intuitivo.

## Origen

- **Autor**: Don Norman
- **Año**: 1988
- **Fuente**: "The Design of Everyday Things"

## Tipos de Mapping

### Mapping Espacial

- Control ubicado cerca de lo que controla
- Botón izquierdo controla elemento izquierdo
- Slider vertical para control vertical
- Layout que refleja relación física

### Mapping Conceptual

- Analogías con el mundo real
- Volumen: más = más fuerte
- Brillo: más = más claro
- Temperatura: derecha = más caliente

### Mapping Cultural

- Convenciones aprendidas
- Scroll down = contenido sube (controversial)
- Verde = continuar, rojo = parar
- X = cerrar

## Aplicación en Diseño

### Controles de UI

- Sliders horizontales para valores horizontales
- Toggles que van de izquierda (off) a derecha (on)
- Volume que sube al mover hacia arriba
- Zoom con pinch natural

### Layouts

- Controles de texto cerca del text area
- Settings de elemento junto al elemento
- Preview al lado de controles que lo modifican
- Navegación que refleja estructura de contenido

### Formularios

- Labels directamente sobre o junto a campos
- Botones de acción al final del flujo
- Grupos que reflejan categorías de datos
- Progress que va de izquierda a derecha

### Interfaces Espaciales

- Mapas con controles de zoom intuitivos
- Editores gráficos con paletas contextuales
- Dashboards con métricas relacionadas agrupadas
- Timelines con controles temporales lógicos

## Ejemplos

- **Stovetop controls**: Disposición que coincide con hornillas
- **Car mirrors**: Controles ubicados en el espejo
- **iOS volume**: Botones físicos arriba/abajo
- **Figma**: Properties panel junto a objeto seleccionado
- **Google Maps**: Zoom con + arriba, - abajo

## Anti-patterns

- ❌ Controles alejados de lo que controlan
- ❌ Sliders verticales para valores horizontales
- ❌ Botones en orden no lógico
- ❌ Settings globales mezclados con locales
- ❌ Mappings que contradicen convenciones

## Métricas

- **Mapping Intuitiveness Score**: Evaluación de naturalidad
- **Control Discovery Time**: Tiempo para encontrar control
- **Error Rate by Mapping**: Errores por mapping pobre
- **Learning Time**: Tiempo para dominar controles

## Principios Relacionados

- [[affordances]] - Controles que sugieren su uso
- [[proximity]] - Gestalt: cercanía indica relación
- [[nielsen-match-real-world]] - Coincidencia con mundo real

## Referencias

- Norman, D. (2013). "The Design of Everyday Things"
- Lidwell, W. et al. (2010). "Universal Principles of Design"
- https://www.interaction-design.org/literature/article/mapping-in-design
