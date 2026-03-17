---
name: occams-razor
description:
  La solución más simple suele ser la mejor. Use cuando evalúe complejidad de
  diseño, tome decisiones de features, o simplifique interfaces.
metadata:
  author: ux-ui-skills
  version: "1.0"
  category: design-principles
---

# Navaja de Occam

## Resumen

Entre soluciones competidoras, se debe preferir la más simple. No multiplicar
entidades sin necesidad. En diseño: eliminar elementos hasta que quitar más
empeoraría el resultado.

## Origen

- **Autor**: William of Ockham
- **Año**: ~1320
- **Principio original**: "Entia non sunt multiplicanda praeter necessitatem"

## En Diseño

La versión de diseño, atribuida a veces a Antoine de Saint-Exupéry:

> "La perfección se alcanza, no cuando no hay nada más que añadir, sino cuando
> no hay nada más que quitar."

## Fundamento

La complejidad tiene costos:

- Mayor carga cognitiva
- Más puntos de fallo
- Mantenimiento más difícil
- Aprendizaje más lento
- Más código, más bugs

## Aplicación en Diseño

### UI Simplification

- Eliminar elementos decorativos
- Reducir opciones a las esenciales
- Consolidar acciones similares
- Remover pasos innecesarios

### Feature Decisions

- MVP antes de feature creep
- Validar necesidad antes de construir
- "Will it hurt to remove this?"
- 80/20: focus en lo que más importa

### Visual Design

- Whitespace > decoración
- Iconos simples > elaborados
- Tipografía limitada
- Paleta de colores restringida

### Code/Architecture

- Abstracciones solo cuando necesarias
- Código simple > clever
- Dependencias mínimas
- Single responsibility

## Ejemplos

- **Google Homepage**: Solo barra de búsqueda
- **Apple Products**: Mínimos botones/puertos
- **Medium**: Diseño centrado en lectura
- **Notion**: Blocks simples, gran flexibilidad
- **Linear**: Features curadas, no todas posibles

## Anti-patterns

- ❌ Features "por si acaso"
- ❌ Opciones que nadie usa
- ❌ UI elements decorativos
- ❌ Múltiples formas de hacer lo mismo sin razón
- ❌ Abstracción prematura

## Límites del Principio

- Simplicidad ≠ fácil de usar
- A veces la complejidad es necesaria
- "Simple as possible, but no simpler" (Einstein)
- Balance entre poder y simplicidad

## Métricas

- **Feature Usage Rate**: % de features realmente usadas
- **UI Element Count**: Elementos por pantalla
- **Task Steps**: Pasos para completar tareas
- **Cognitive Load Score**: Complejidad percibida

## Principios Relacionados

- [[kiss-principle]] - Keep It Simple
- [[pragnanz]] - Gestalt: preferencia por simplicidad
- [[nielsen-minimalist-design]] - Eliminar lo irrelevante

## Referencias

- Occam, W. (~1320). Principio de parsimonia
- Lidwell, W. et al. (2010). "Universal Principles of Design"
- Maeda, J. (2006). "The Laws of Simplicity"
