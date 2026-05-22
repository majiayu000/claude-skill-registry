---
name: nielsen-consistency
description:
  Mantiene patrones visuales y de comportamiento uniformes en toda la interfaz.
  Use cuando diseñe sistemas de diseño, defina patrones de interacción, o evalúe
  coherencia entre pantallas.
metadata:
  author: ux-ui-skills
  version: "1.0"
  category: heuristics
---

# Consistencia y Estándares

## Resumen

Los usuarios no deberían preguntarse si diferentes palabras, situaciones o
acciones significan lo mismo. Seguir convenciones de plataforma e industria, y
mantener consistencia interna en toda la aplicación.

## Origen

- **Autor**: Jakob Nielsen
- **Año**: 1994 (refinado 2020)
- **Fuente**: Nielsen Norman Group - "10 Usability Heuristics for User Interface
  Design"

## Fundamento Psicológico

La consistencia reduce la **carga cognitiva** al permitir que los usuarios
apliquen conocimiento previo. El cerebro busca patrones (Gestalt) y se frustra
cuando expectativas basadas en experiencias anteriores no se cumplen. La **Ley
de Jakob** refuerza que los usuarios pasan más tiempo en otros sitios y esperan
comportamientos similares.

## Aplicación en Diseño

### Consistencia Interna

- Mismos colores para mismas acciones (azul = links)
- Iconografía uniforme en toda la app
- Posición consistente de elementos (nav, CTAs)
- Terminología idéntica para mismos conceptos

### Consistencia Externa

- Convenciones de plataforma (iOS vs Android guidelines)
- Patrones de industria (carrito arriba-derecha en e-commerce)
- Estándares web (logo → home, links subrayados)
- Atajos de teclado estándar (Ctrl+S, Ctrl+C)

### Sistemas de Diseño

- Design tokens (colores, spacing, typography)
- Componentes reutilizables documentados
- Patrones de interacción definidos
- Guidelines de voz y tono

### Niveles de Consistencia

1. **Mismo elemento**: Botón se ve igual en todas las páginas
2. **Misma aplicación**: Patrones coherentes internamente
3. **Misma plataforma**: Respeta guidelines de iOS/Android/Web
4. **Misma industria**: Sigue convenciones del sector

## Ejemplos

- **Material Design**: Sistema completo con componentes, motion, iconografía
- **Apple HIG**: Guidelines estrictas que unifican todo el ecosistema
- **Stripe**: Consistencia en API, docs, dashboard, y checkout
- **Airbnb**: Design Language System con componentes React
- **IBM Carbon**: Design system open source para productos enterprise

## Anti-patterns

- ❌ Botones primarios de diferentes colores en distintas páginas
- ❌ Mismo icono con significados distintos
- ❌ Navegación que cambia de posición
- ❌ Terminología inconsistente ("Guardar" vs "Salvar" vs "Almacenar")
- ❌ Comportamientos diferentes para acciones similares

## Métricas

- **Heuristic Evaluation Score**: Evaluación de consistencia por expertos
- **Component Reuse Rate**: % de componentes del design system usados
- **Style Guide Compliance**: Adherencia a guidelines
- **Cross-page Task Time**: Tiempo para tareas similares en diferentes secciones

## Principios Relacionados

- [[jakobs-law]] - Expectativas basadas en otros sitios
- [[consistency-principle]] - Principio general de consistencia
- [[similarity]] - Gestalt: elementos similares se agrupan

## Referencias

- Nielsen, J. (1994). "Usability Engineering". Morgan Kaufmann
- Apple Human Interface Guidelines
- Material Design Guidelines
- https://www.nngroup.com/articles/consistency-and-standards/
