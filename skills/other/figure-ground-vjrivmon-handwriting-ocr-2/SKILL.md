---
name: figure-ground
description:
  El cerebro separa elementos en primer plano y fondo. Use cuando diseñe
  modales, overlays, focus states, o jerarquía visual de capas.
metadata:
  author: ux-ui-skills
  version: "1.0"
  category: gestalt
---

# Principio de Figura-Fondo

## Resumen

El sistema perceptual organiza elementos visuales en figuras (objetos de
atención) y fondo (contexto). Los elementos se perciben como uno u otro, no
ambos simultáneamente.

## Origen

- **Escuela**: Psicología de la Gestalt
- **Año**: ~1920s
- **Autor principal**: Edgar Rubin (jarrón de Rubin)

## Fundamento Psicológico

El cerebro necesita separar objetos de su contexto para procesarlos. La relación
figura-fondo es inestable cuando ambos son igualmente prominentes (como en
ilusiones ópticas), causando confusión visual. En diseño, debemos hacer clara
esta distinción.

## Aplicación en Diseño

### Modales y Overlays

- Background oscurecido (scrim) detrás de modal
- Modal con shadow prominente
- Elevación visual clara
- Focus trap en el elemento frontal

### Jerarquía de Capas

- Z-index consistente para tipos de elementos
- Shadows que indican elevación
- Blur en elementos de fondo
- Contraste entre capas

### Focus y Selección

- Elementos seleccionados destacados del fondo
- Estados hover con elevación sutil
- Active states con mayor prominencia
- Disabled states fundidos con fondo

### Texto y Contenido

- Contraste suficiente texto/fondo (4.5:1 mínimo)
- Backgrounds que no compiten con contenido
- Imágenes con overlays para texto
- Cards elevadas sobre el fondo de página

## Ejemplos

- **iOS Modals**: Fondo desenfocado, modal nítido
- **Google Material**: Elevation system con shadows
- **Lightboxes**: Imagen destacada, fondo oscurecido
- **Dropdown menus**: Elevados sobre contenido
- **Toast notifications**: Flotando sobre la UI

## Anti-patterns

- ❌ Modales sin scrim que se pierden en el fondo
- ❌ Texto sobre imágenes sin overlay
- ❌ Elementos superpuestos sin jerarquía clara
- ❌ Backgrounds con patrones que compiten
- ❌ Niveles de elevación inconsistentes

## Métricas

- **Contrast Ratio**: Cumplimiento de WCAG (4.5:1, 3:1)
- **Layer Hierarchy Test**: Usuarios identifican qué está "encima"
- **Modal Visibility**: Reconocimiento inmediato de overlays
- **Visual Noise Score**: Competencia figura/fondo medida

## Principios Relacionados

- [[closure]] - Completar figuras reconocibles
- [[nielsen-minimalist-design]] - Reducir ruido de fondo
- [[common-region]] - Delimitar figuras claramente

## Referencias

- Rubin, E. (1915). "Synsoplevede Figurer"
- Palmer, S.E. (1999). "Vision Science: Photons to Phenomenology"
- https://www.nngroup.com/articles/gestalt-figure-ground/
