---
name: hicks-law
description:
  Predice el tiempo de decisión basado en número de opciones. Use cuando diseñe
  menús, navegación, formularios con múltiples opciones, o simplifique
  interfaces.
metadata:
  author: ux-ui-skills
  version: "1.0"
  category: cognitive-laws
---

# Ley de Hick-Hyman

## Resumen

El tiempo para tomar una decisión aumenta logarítmicamente con el número y
complejidad de las opciones disponibles. Más opciones = más tiempo de decisión.

## Origen

- **Autores**: William Edmund Hick y Ray Hyman
- **Año**: 1952
- **Fuente**: "On the Rate of Gain of Information" - Quarterly Journal of
  Experimental Psychology

## Fórmula

```
T = a + b × log₂(n + 1)
```

Donde:

- **T** = Tiempo de reacción
- **n** = Número de opciones equiprobables
- **a, b** = Constantes empíricas
- **+1** = Cuenta la opción de "no elegir"

## Fundamento Psicológico

El cerebro procesa opciones como información. Cada duplicación de opciones añade
una "decisión binaria" al proceso cognitivo. La relación logarítmica significa
que agregar opciones tiene rendimientos decrecientes en complejidad percibida,
pero aún así aumenta el tiempo de decisión.

## Aplicación en Diseño

### Reducción de Opciones

- **Regla de 3-5**: Menús principales con 3-5 items
- Agrupar opciones relacionadas en submenús
- Mostrar opciones más usadas, ocultar el resto
- Defaults inteligentes que reducen decisiones

### Categorización Efectiva

- Chunks de información relacionada
- Jerarquías claras (navegación multinivel)
- Filtros para reducir set de opciones
- Búsqueda como alternativa a navegación

### Progressive Disclosure

- Revelar opciones gradualmente
- Wizards paso a paso
- Menús contextuales según estado
- Personalización que reduce opciones irrelevantes

### Casos Especiales

- Usuarios expertos: más opciones pueden ser aceptables
- Listas conocidas (alfabéticas): búsqueda más rápida
- Selección serial (teclado numérico): no aplica igual

## Ejemplos

- **Amazon**: Mega-menús categorizados vs lista plana
- **iPhone**: Settings agrupados en secciones lógicas
- **Spotify**: Búsqueda + browse + personalización reduce decisiones
- **Google**: Una sola caja de búsqueda vs Yahoo 2000
- **Netflix**: Categorías + recomendaciones personalizadas

## Anti-patterns

- ❌ Menús con 15+ opciones al mismo nivel
- ❌ Dropdowns con cientos de opciones sin búsqueda
- ❌ Dashboards con todas las acciones visibles simultáneamente
- ❌ Formularios que muestran todos los campos desde el inicio
- ❌ Landing pages con múltiples CTAs compitiendo

## Métricas

- **Decision Time**: Tiempo desde ver opciones hasta elegir
- **Choice Overload Rate**: % usuarios que abandonan por exceso
- **Conversion by Options**: Tasa de conversión vs número de opciones
- **Cognitive Load Score**: Evaluación subjetiva de complejidad

## Principios Relacionados

- [[millers-law]] - Límite de items en memoria de trabajo
- [[paradox-of-choice]] - Más opciones pueden reducir satisfacción
- [[progressive-disclosure]] - Revelar complejidad gradualmente

## Referencias

- Hick, W.E. (1952). "On the Rate of Gain of Information"
- Schwartz, B. (2004). "The Paradox of Choice"
- https://lawsofux.com/hicks-law/
