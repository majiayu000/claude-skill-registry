---
name: millers-law
description:
  Limita información a 7±2 (o 4±1) chunks para memoria de trabajo. Use cuando
  organice navegación, formularios, dashboards, o cualquier lista de elementos.
metadata:
  author: ux-ui-skills
  version: "1.0"
  category: cognitive-laws
---

# Ley de Miller

## Resumen

La persona promedio puede mantener solo 7±2 (revisado a 4±1) elementos en la
memoria de trabajo simultáneamente. La información debe organizarse en chunks
manejables.

## Origen

- **Autor**: George A. Miller
- **Año**: 1956
- **Fuente**: "The Magical Number Seven, Plus or Minus Two" - Psychological
  Review

## Actualización Moderna

Investigaciones posteriores (Cowan, 2001) sugieren que el límite real es más
cercano a **4±1 chunks**, especialmente para información no familiar o sin
relaciones previas.

## Fundamento Psicológico

La memoria de trabajo tiene capacidad limitada para procesar información nueva.
El **chunking** (agrupación de información en unidades significativas) permite
superar este límite al tratar grupos como unidades individuales. Por ejemplo,
"FBI-CIA-NASA" son 3 chunks, no 9 letras.

## Aplicación en Diseño

### Navegación

- Máximo 5-7 items en menú principal
- Submenús para opciones adicionales
- Mega-menús con categorías claras
- Breadcrumbs limitados a niveles visibles

### Formularios

- Agrupar campos relacionados (secciones)
- Máximo 5-7 campos visibles por sección
- Multi-step forms para formularios largos
- Progress indicators para orientación

### Contenido

- Listas con 5-7 bullets máximo
- Párrafos cortos (3-4 líneas)
- Chunks visuales con whitespace
- Títulos y subtítulos para secciones

### Datos y Dashboards

- Agrupar métricas relacionadas
- KPIs principales: 4-6 máximo
- Tarjetas que encapsulan información
- Visualizaciones que resumen datos

## Ejemplos

- **Teléfonos**: Números agrupados (XXX) XXX-XXXX
- **Tarjetas de crédito**: 4 grupos de 4 dígitos
- **GitHub**: Tabs limitados en repositorios
- **Slack**: Canales organizados por categorías
- **iPhone Home**: 4 apps en dock, apps en carpetas

## Anti-patterns

- ❌ Menús con más de 9 opciones sin agrupación
- ❌ Formularios de 20 campos en una sola vista
- ❌ Dashboards con 15+ métricas sin jerarquía
- ❌ Listas sin categorización ni agrupación
- ❌ Instrucciones con más de 7 pasos sin división

## Métricas

- **Recall Accuracy**: % de items recordados correctamente
- **Time to Process**: Tiempo para procesar y actuar
- **Error Rate**: Errores por sobrecarga de información
- **Chunk Size Effectiveness**: Rendimiento por tamaño de grupo

## Principios Relacionados

- [[hicks-law]] - Más opciones, más tiempo de decisión
- [[cognitive-load]] - Gestión de carga cognitiva total
- [[progressive-disclosure]] - Revelar información en chunks

## Referencias

- Miller, G.A. (1956). "The Magical Number Seven, Plus or Minus Two"
- Cowan, N. (2001). "The magical number 4 in short-term memory"
- https://lawsofux.com/millers-law/
