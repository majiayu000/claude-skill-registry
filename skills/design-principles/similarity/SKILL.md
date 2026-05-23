---
name: similarity
description:
  Elementos visualmente similares se perciben como relacionados. Use cuando
  diseñe sistemas de iconos, estados, categorías, o elementos que deben verse
  como grupo.
metadata:
  author: ux-ui-skills
  version: "1.0"
  category: gestalt
---

# Principio de Similitud

## Resumen

Los elementos que comparten características visuales (color, forma, tamaño,
orientación) se perciben como relacionados o pertenecientes al mismo grupo.

## Origen

- **Escuela**: Psicología de la Gestalt
- **Año**: ~1920s
- **Autores principales**: Max Wertheimer, Kurt Koffka, Wolfgang Köhler

## Fundamento Psicológico

El cerebro usa similitud visual como heurística para categorizar información
rápidamente. Este proceso automático permite identificar patrones y estructuras
sin análisis consciente, reduciendo la carga cognitiva.

## Aplicación en Diseño

### Color como Agrupador

- Links del mismo color en toda la app
- Estados de error siempre en rojo
- Acciones primarias con color consistente
- Categorías diferenciadas por color

### Forma y Estilo

- Iconos con estilo visual consistente
- Botones primarios vs secundarios (filled vs outlined)
- Cards con mismo border-radius y shadow
- Badges con forma consistente

### Tamaño y Peso

- Headlines del mismo nivel, mismo tamaño
- Botones de igual importancia, igual tamaño
- Iconos en toolbar de tamaño uniforme
- Texto de ayuda siempre más pequeño

### Tipografía

- Misma fuente para mismo tipo de contenido
- Bold para términos clave consistentemente
- Monospace para código en toda la app
- Itálicas para citas siempre

## Ejemplos

- **Gmail**: Emails no leídos en bold, leídos en normal
- **GitHub**: Labels de colores para categorizar issues
- **Spotify**: Cards de albums/playlists con estilo uniforme
- **iOS**: Iconos de apps con rounded squares consistentes
- **Material Design**: FABs siempre circulares

## Anti-patterns

- ❌ Links de diferentes colores en la misma página
- ❌ Botones primarios con estilos inconsistentes
- ❌ Iconos mezclando estilos (filled, outlined, etc.)
- ❌ Estados similares con colores diferentes
- ❌ Elementos relacionados con apariencia distinta

## Métricas

- **Visual Consistency Score**: Adherencia a design system
- **Pattern Recognition**: Tiempo para identificar categorías
- **Error Rate**: Confusión por elementos similares mal usados
- **Design Audit**: Número de inconsistencias visuales

## Principios Relacionados

- [[proximity]] - Proximidad también agrupa
- [[nielsen-consistency]] - Consistencia de patrones
- [[uniform-connectedness]] - Conexiones visuales

## Referencias

- Wertheimer, M. (1923). "Laws of Organization in Perceptual Forms"
- Lidwell, W. et al. (2010). "Universal Principles of Design"
- https://www.interaction-design.org/literature/article/the-law-of-similarity
