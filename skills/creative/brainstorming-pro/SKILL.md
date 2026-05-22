---
name: brainstorming-pro
description: Genera ideas de calidad con estructura, filtros y selección final. Úsalo cuando necesites opciones creativas con criterio y una recomendación clara.
---

# Brainstorming Pro

Skill especializado en generación de ideas estructuradas con filtrado por calidad y recomendación final ejecutable.

## Cuándo usar este skill

- Cuando el usuario pida ideas, variantes, conceptos, hooks, nombres, formatos o enfoques
- Cuando haya bloqueo creativo o demasiadas opciones y haga falta ordenar
- Cuando el usuario necesite ideas "buenas para ejecutar", no solo ocurrencias
- Cuando se pida "dame opciones para X" o "necesito ideas de Y"

## Inputs necesarios

> **Regla**: Si falta alguno de estos inputs, PREGUNTAR antes de generar ideas.

1. **Objetivo exacto**: ¿Qué se quiere conseguir? (obligatorio)
2. **Público / contexto**: ¿Para quién es y dónde se usa? (obligatorio)
3. **Restricciones**: Tiempo, presupuesto, tono, formato, herramientas (obligatorio)
4. **Ejemplos de preferencia**: Lo que SÍ y lo que NO le gusta al usuario (opcional)

## Workflow

### Fase 1: Clarificar (solo si faltan datos)

1. Hacer 3–5 preguntas rápidas para completar inputs faltantes
2. Confirmar entendimiento del objetivo antes de generar

### Fase 2: Generar ideas en 4 tandas

| Tanda | Cantidad | Enfoque                         |
| ----- | -------- | ------------------------------- |
| **A** | 10 ideas | Rápidas, claras y ejecutables   |
| **B** | 5 ideas  | Ángulos diferentes, no obvios   |
| **C** | 5 ideas  | Low effort, rápidas de producir |
| **D** | 3 ideas  | High impact, más ambiciosas     |

### Fase 3: Filtrar y puntuar

3. Evaluar cada idea con escala 1–5 en:
   - **Impacto**: ¿Qué tan potente es el resultado?
   - **Claridad**: ¿Se entiende de inmediato?
   - **Novedad**: ¿Qué tan diferente es?
   - **Esfuerzo**: ¿Qué tan fácil de implementar? (5 = muy fácil)
   - **Viabilidad**: ¿Es realista con los recursos disponibles?

### Fase 4: Recomendar

4. Seleccionar TOP 5 final con:
   - Idea (1 línea)
   - Por qué funciona (2 líneas)
   - Primer paso (1 línea)

## Instrucciones

### Reglas de calidad

| Regla                   | Ejemplo malo               | Ejemplo bueno                                                           |
| ----------------------- | -------------------------- | ----------------------------------------------------------------------- |
| Nada genérico           | "Mejorar tu productividad" | "Rutina de 15 min con 3 tareas priorizadas por impacto"                 |
| Hooks con tensión       | "Cómo ser mejor"           | "El error que cometes cada mañana (y te cuesta 2 horas)"                |
| Formatos con estructura | "Hacer un video"           | "Video de 60s: hook (5s) + problema (15s) + solución (30s) + CTA (10s)" |

### Reglas adicionales

- Si el usuario pide **hooks/títulos**: que sean cortos y con tensión/curiosidad
- Si el usuario pide **formatos**: incluir estructura + ejemplo de primer minuto
- Si una idea depende de algo incierto: decirlo y ofrecer alternativa
- Nunca repetir ideas con diferente fraseo
- Cada idea debe ser **ejecutable en el contexto dado**

### Manejo de errores

- Si las ideas no encajan con el objetivo → volver a Fase 1 y reclarificar
- Si el usuario rechaza todo el TOP 5 → preguntar qué criterio falta
- Si hay ambigüedad en restricciones → preguntar antes de asumir

## Output (formato exacto)

```markdown
## 🔍 Preguntas rápidas

[Solo si faltan datos - 3 a 5 preguntas concretas]

---

## 💡 Ideas generadas

### Tanda A: Ideas rápidas y ejecutables (10)

1. [Idea]
2. [Idea]
   ...

### Tanda B: Ángulos diferentes (5)

1. [Idea]
2. [Idea]
   ...

### Tanda C: Low effort (5)

1. [Idea]
2. [Idea]
   ...

### Tanda D: High impact (3)

1. [Idea]
2. [Idea]
3. [Idea]

---

## 🏆 TOP 5 Recomendado

| #   | Idea   | Impacto | Claridad | Novedad | Esfuerzo | Viabilidad | Total |
| --- | ------ | ------- | -------- | ------- | -------- | ---------- | ----- |
| 1   | [Idea] | X/5     | X/5      | X/5     | X/5      | X/5        | XX/25 |
| 2   | [Idea] | X/5     | X/5      | X/5     | X/5      | X/5        | XX/25 |
| 3   | [Idea] | X/5     | X/5      | X/5     | X/5      | X/5        | XX/25 |
| 4   | [Idea] | X/5     | X/5      | X/5     | X/5      | X/5        | XX/25 |
| 5   | [Idea] | X/5     | X/5      | X/5     | X/5      | X/5        | XX/25 |

### Detalle del TOP 5

**#1: [Nombre de la idea]**

- 💡 Idea: [1 línea]
- ✅ Por qué funciona: [2 líneas]
- 🚀 Primer paso: [1 línea]

[Repetir para #2, #3, #4, #5]
```
