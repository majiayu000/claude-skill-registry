---
name: weber-fechner-law
description:
  La percepción de cambio es proporcional al estímulo original. Use cuando
  diseñe feedback de progreso, sistemas de pricing, o cambios visuales
  graduales.
metadata:
  author: ux-ui-skills
  version: "1.0"
  category: perception
---

# Ley de Weber-Fechner

## Resumen

La percepción de cambio en un estímulo es proporcional a la magnitud del
estímulo original. Un cambio pequeño se nota más en valores pequeños que en
valores grandes.

## Origen

- **Autores**: Ernst Weber (1834), Gustav Fechner (1860)
- **Campo**: Psicofísica
- **Fórmula**: ΔS/S = k (donde ΔS es cambio perceptible, S es estímulo, k es
  constante)

## Fundamento Psicológico

### Just Noticeable Difference (JND)

- Mínimo cambio perceptible
- Proporcional al valor base
- ~1-2% para brillo
- ~2-3% para peso
- Variable por modalidad sensorial

### Implicaciones

- $1 de descuento importa más en $5 que en $500
- 100ms delay se nota más en 200ms que en 2s
- 5px de cambio se nota más en 20px que en 200px

## Aplicación en Diseño

### Pricing y Descuentos

- Porcentajes para precios altos
- Valores absolutos para precios bajos
- "$50 off" vs "10% off" según contexto
- Anclas que maximicen percepción de ahorro

### Progress Indicators

- Inicio: Incrementos pequeños se sienten
- Final: Necesita incrementos más grandes
- Logarítmica más satisfactoria que lineal
- Gamification: Niveles cada vez más largos

### Visual Design

- Cambios de tamaño proporcionales
- Escalas tipográficas con ratios (1.2, 1.618)
- Spacing systems con multiplicadores
- Color: Pasos perceptualmente uniformes (LAB)

### Performance

- 100ms → 200ms: Muy notable
- 1s → 1.1s: Apenas perceptible
- Optimizar donde más se siente
- Budget de latencia proporcional

## Ejemplos

- **Uber Surge**: 1.5x vs $10 extra según base
- **Steam Sales**: -75% impacta más visualmente
- **XP Systems**: Niveles exponencialmente más largos
- **Type Scales**: 16, 20, 24, 32 (ratio 1.25)
- **Spotify Volume**: Curva logarítmica

## Anti-patterns

- ❌ Escala lineal para progress bars largos
- ❌ Mismo descuento absoluto para todos los precios
- ❌ Incrementos de tamaño aritméticos
- ❌ Esperar que 50ms se note igual en 100ms y 1000ms
- ❌ Escalas de color con pasos RGB iguales

## Métricas

- **JND Testing**: Mínimo cambio detectable
- **Perception Surveys**: Percepción de diferencias
- **A/B Tests**: Diferentes escalas
- **Price Sensitivity**: Por rango de precio

## Principios Relacionados

- [[fitts-law]] - Tamaño y distancia
- [[millers-law]] - Límites de procesamiento
- [[cognitive-load]] - Esfuerzo de percepción

## Referencias

- Fechner, G.T. (1860). "Elemente der Psychophysik"
- Stevens, S.S. (1957). "On the Psychophysical Law"
- https://www.interaction-design.org/literature/article/weber-s-law
