---
name: fitts-law
description:
  Calcula el tiempo para alcanzar un objetivo basado en distancia y tamaño. Use
  cuando dimensione botones, posicione CTAs, o diseñe áreas interactivas.
metadata:
  author: ux-ui-skills
  version: "1.0"
  category: cognitive-laws
---

# Ley de Fitts

## Resumen

El tiempo para adquirir un objetivo es función de la distancia al objetivo y el
tamaño del mismo. Los objetivos más grandes y cercanos son más rápidos de
alcanzar.

## Origen

- **Autor**: Paul Fitts
- **Año**: 1954
- **Fuente**: "The Information Capacity of the Human Motor System in Controlling
  the Amplitude of Movement" - Journal of Experimental Psychology

## Fórmula

```
T = a + b × log₂(2D/W)
```

Donde:

- **T** = Tiempo de movimiento
- **D** = Distancia al centro del objetivo
- **W** = Ancho del objetivo (a lo largo del eje de movimiento)
- **a, b** = Constantes empíricas

## Fundamento Psicológico

El sistema motor humano opera como un canal de información con capacidad
limitada. Movimientos más precisos (objetivos pequeños o distantes) requieren
más correcciones motoras y por tanto más tiempo. La relación logarítmica indica
que duplicar el tamaño no duplica la velocidad, pero sí la mejora
significativamente.

## Aplicación en Diseño

### Tamaño de Elementos Interactivos

- **Mínimo táctil**: 44×44px (Apple), 48×48dp (Material)
- **Óptimo para desktop**: 40-60px para CTAs principales
- Padding generoso en links de texto
- Áreas de click más grandes que el elemento visual

### Posicionamiento Estratégico

- CTAs principales cerca del punto de atención actual
- Menús en bordes/esquinas (objetivo "infinito")
- Acciones relacionadas agrupadas
- Evitar ping-pong entre elementos distantes

### Bordes y Esquinas de Pantalla

- Los bordes actúan como objetivos de tamaño infinito
- Menús pegados a bordes son más rápidos de alcanzar
- Barra de tareas de Windows, Dock de macOS
- Scrollbars en el borde derecho

### Acciones Frecuentes vs Infrecuentes

- Mayor tamaño para acciones frecuentes
- Acciones destructivas: pequeñas pero no diminutas
- Shortcuts de teclado para bypasear movimiento

## Ejemplos

- **macOS Dock**: Magnificación aumenta tamaño al acercarse
- **Windows**: Botón Start en esquina (objetivo infinito)
- **Mobile FAB**: Floating Action Button grande y accesible
- **Ribbon de Office**: Iconos grandes para herramientas comunes
- **Teclados móviles**: Teclas más grandes para letras frecuentes

## Anti-patterns

- ❌ Botones de 20×20px en touch interfaces
- ❌ Links de texto sin padding adicional
- ❌ CTAs principales en esquinas opuestas
- ❌ Menús que requieren precisión extrema
- ❌ Targets pequeños para acciones frecuentes

## Métricas

- **Movement Time (MT)**: Tiempo desde inicio hasta click
- **Error Rate**: Clicks fuera del objetivo
- **Throughput (bits/s)**: Eficiencia del movimiento
- **Index of Difficulty (ID)**: log₂(2D/W)

## Principios Relacionados

- [[hicks-law]] - Tiempo de decisión antes del movimiento
- [[nielsen-flexibility]] - Atajos reducen necesidad de movimiento
- [[direct-manipulation]] - Interacción directa con objetos

## Referencias

- Fitts, P.M. (1954). "The Information Capacity of the Human Motor System"
- MacKenzie, I.S. (1992). "Fitts' Law as a Research and Design Tool in HCI"
- https://www.interaction-design.org/literature/article/fitts-s-law
