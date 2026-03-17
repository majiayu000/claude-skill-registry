---
name: nielsen-recognition-recall
description:
  Minimiza la carga de memoria mostrando opciones visibles en lugar de requerir
  que usuarios recuerden información. Use cuando diseñe navegación, formularios,
  o interfaces donde el usuario debe tomar decisiones.
metadata:
  author: ux-ui-skills
  version: "1.0"
  category: heuristics
---

# Reconocimiento sobre Recuerdo

## Resumen

Minimizar la carga de memoria del usuario haciendo visibles objetos, acciones y
opciones. El usuario no debería tener que recordar información de una parte del
diálogo a otra. Las instrucciones de uso deben ser visibles o fácilmente
recuperables.

## Origen

- **Autor**: Jakob Nielsen
- **Año**: 1994 (refinado 2020)
- **Fuente**: Nielsen Norman Group - "10 Usability Heuristics for User Interface
  Design"

## Fundamento Psicológico

El reconocimiento es cognitivamente más fácil que el recuerdo porque activa
directamente la memoria (matching pattern) en lugar de requerir búsqueda activa.
Según Miller (1956), la memoria de trabajo tiene capacidad limitada (~4 items).
Las interfaces basadas en reconocimiento aprovechan la memoria a largo plazo,
que tiene capacidad prácticamente ilimitada.

## Aplicación en Diseño

### Elementos Siempre Visibles

- Menús desplegables con todas las opciones
- Toolbars con iconos y labels
- Navegación persistente
- Estado actual visible (breadcrumbs, indicadores)

### Historial y Sugerencias

- Búsquedas recientes
- Documentos abiertos recientemente
- Autocompletado basado en historial
- "Continuar donde lo dejaste"

### Ayuda Contextual

- Tooltips con información adicional
- Placeholders descriptivos en campos
- Labels claros en todos los inputs
- Iconos con texto cuando el espacio lo permite

### Reducción de Inputs Manuales

- Selectores en lugar de campos de texto libre
- Date pickers en lugar de escribir fechas
- Dropdowns con opciones predefinidas
- Auto-fill de formularios

## Ejemplos

- **Google**: Sugerencias de búsqueda mientras escribes
- **Amazon**: "Productos vistos recientemente"
- **Spotify**: "Escuchado recientemente" en home
- **VS Code**: Command Palette con búsqueda fuzzy
- **Netflix**: "Continuar viendo" prominente

## Anti-patterns

- ❌ Interfaces de línea de comandos sin autocompletado
- ❌ Formularios sin labels persistentes (solo placeholders)
- ❌ Navegación que desaparece al hacer scroll
- ❌ Códigos o IDs que el usuario debe memorizar
- ❌ Mensajes que desaparecen sin poder recuperarlos

## Métricas

- **Time to Find**: Tiempo para localizar una función
- **Error Rate**: Errores por confusión de opciones similares
- **Memory Load Score**: Evaluación heurística de carga cognitiva
- **Help Usage Rate**: Frecuencia de consulta a documentación

## Principios Relacionados

- [[millers-law]] - Límite de memoria de trabajo
- [[cognitive-load]] - Teoría de carga cognitiva
- [[progressive-disclosure]] - Revelar información gradualmente

## Referencias

- Nielsen, J. (1994). "Usability Engineering". Morgan Kaufmann
- Miller, G.A. (1956). "The Magical Number Seven". Psychological Review
- https://www.nngroup.com/articles/recognition-and-recall/
