---
name: common-region
description:
  Elementos dentro de un área delimitada se perciben como grupo. Use cuando
  diseñe cards, secciones, formularios agrupados, o contenedores visuales.
metadata:
  author: ux-ui-skills
  version: "1.0"
  category: gestalt
---

# Principio de Región Común

## Resumen

Los elementos que comparten un área cerrada o delimitada se perciben como
pertenecientes al mismo grupo, incluso si no comparten otras características.

## Origen

- **Autor**: Stephen Palmer
- **Año**: 1992
- **Fuente**: "Common Region: A New Principle of Perceptual Grouping"

## Fundamento Psicológico

Los límites visuales crean containers perceptuales que el cerebro interpreta
como agrupadores. Es un principio más reciente, agregado a la Gestalt clásica,
pero extremadamente relevante para interfaces digitales donde cards y containers
son ubicuos.

## Aplicación en Diseño

### Cards y Containers

- Cards con border o background diferenciado
- Secciones con fondos alternos
- Fieldsets con border visible
- Well components para contenido agrupado

### Formularios

- Grupos de campos relacionados en sections
- Fieldsets para datos de contacto, envío, pago
- Inline grouping para campos relacionados
- Step containers en wizards

### Dashboards

- Widgets en cards separadas
- Métricas agrupadas por categoría
- Paneles con bordes definidos
- Data visualization containers

### Listas y Tablas

- Rows con alternating backgrounds
- Headers en región separada
- Footers delimitados
- Grupos de filas relacionadas

## Ejemplos

- **Material Design Cards**: Elevated containers para contenido
- **Bootstrap Wells**: Áreas con fondo diferenciado
- **Form Fieldsets**: Grupos de campos con legend
- **Dashboard Widgets**: Cada métrica en su card
- **Stripe Checkout**: Secciones claramente delimitadas

## Anti-patterns

- ❌ Contenido relacionado sin container visual
- ❌ Cards con bordes tan sutiles que no delimitan
- ❌ Secciones sin separación clara
- ❌ Formularios sin agrupación de campos
- ❌ Demasiados niveles de nesting confusos

## Métricas

- **Group Association Accuracy**: Usuarios asocian contenido correctamente
- **Visual Boundary Clarity**: Claridad de delimitaciones
- **Container Hierarchy**: Niveles de anidamiento comprensibles
- **Scan Pattern Efficiency**: Eye-tracking respeta regiones

## Principios Relacionados

- [[proximity]] - Cercanía dentro de región refuerza grupo
- [[figure-ground]] - Región como figura sobre fondo
- [[similarity]] - Styling de containers consistente

## Referencias

- Palmer, S.E. (1992). "Common Region: A New Principle of Perceptual Grouping"
- Lidwell, W. et al. (2010). "Universal Principles of Design"
- https://uxdesign.cc/gestalt-principles-in-ux-design-6-common-region-26ab9d57c8a7
