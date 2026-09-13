---
# machine-translated to es from skills/okr-builder/SKILL.md — review: pending. Native fixes welcome via PR.
name: okr-builder
description: "Crea OKRs bien estructurados (Objetivos y Resultados Clave) para equipos de producto, startups e individuos. Úsalo cuando te pidan escribir OKRs, establecer objetivos trimestrales, definir resultados clave o revisar OKRs existentes. Produce un conjunto completo de OKRs con objetivos, resultados clave medibles, líneas de base y una guía de puntuación."
---

# Skill OKR Builder

Escribe OKRs ambiciosos y medibles que conecten el trabajo de producto con la estrategia empresarial. Evita métricas de vanidad, resultados clave orientados a output y objetivos que suenen como listas de tareas.

## Lee / Escribe en el Brain

Si existe un [`professional-brain`](../professional-brain/SKILL.md) (`brain/`), apóyate en él en lugar de volver a preguntar lo que ya sabes:

- **Lee primero:** `context.md` (definiciones de métricas), `knowledge/strategy.md` (hacia dónde va el producto) y cualquier `hypotheses/` abierta. Ejecuta `python3 ../professional-brain/scripts/brain_query.py ./brain "<tema del objetivo>"` y lleva la etiqueta de procedencia de cada hecho — no fijes un resultado clave basado en un `[hunch]` como si fuera `[data]`.
- **📥 Propón al Brain:** después de producir, propón registrar los objetivos elegidos + targets de KR como registro en `decisions/` (la apuesta del período) y cualquier nueva definición de métrica en `knowledge/`, cada una etiquetada por procedencia. Muéstralas, obtén un sí y luego escribe con `../professional-brain/scripts/brain_write.py … --commit` (append-only, dry-run por defecto).

## Trabajo a partir de un brief

A menudo recibirás un brief corto sin todos los detalles (sin líneas de base, sin números exactos). **Siempre entrega un conjunto OKR completo y específico** — no te detengas para hacer preguntas ni dejes placeholders entre corchetes como `[target]`. Cuando falte una línea de base o número, infiere un valor realista a partir del brief y el dominio, y márcalo *(asumido — confirma)*. Una línea de base claramente etiquetada (p. ej. "activación 40% *(asumido)* → 60%") siempre es mejor que un espacio en blanco o una cifra inventada como hecho.

## Materiales más profundos

- **`references/bad-okr-gallery.md`** — seis OKRs malos realistas con diagnóstico y reescritura (hoja de ruta disfrazada, objetivo no falsable, sandbagging, KR incontrolable, zoo de métricas, guardrail faltante), terminando en un diagnóstico de 5 preguntas. Úsalo cuando *revises* OKRs existentes — compara contra la galería antes de escribir feedback.
- **`templates/okr-worksheet.md`** — una hoja de trabajo para rellenar cuyas columnas refuerzan las puertas de calidad (fuente de línea de base, test de drift, test de control, guardrail) más una rúbrica de puntuación pre-comprometida de fin de trimestre. Ofrécela cuando un equipo quiera redactar OKRs por sí mismo.

## Fundamentos de OKR

**Objetivo:** Cualitativo, inspirador, limitado en tiempo. Responde "¿hacia dónde vamos?"
**Resultado Clave:** Cuantitativo, específico, medible. Responde "¿cómo sabremos que hemos llegado?"

### La Prueba de un Buen KR
- ¿Puede puntuarse 0.0–1.0 al final del período?
- ¿Mide resultado, no output? ("Los ingresos de nuevos clientes aumentaron un 30%" no "Lanzar 3 features")
- ¿Es ambicioso pero alcanzable? (Apunta a 70% de cumplimiento como el estándar de oro)
- ¿Está bajo el control del equipo?

## Anti-Patrones Comunes de OKR a Señalar y Corregir

| Anti-Patrón | Ejemplo | Versión Mejorada |
|---|---|---|
| Tarea disfrazada de KR | "Lanzar rediseño de onboarding" | "La tasa de activación de nuevos usuarios aumenta del 42% al 65%" |
| Métrica de vanidad | "Obtener 10,000 descargas de app" | "La retención a 30 días para nuevos usuarios alcanza el 40%" |
| KR binario | "Enviar API v2" | "API v2 adoptada por el 80% de las integraciones activas" |
| Demasiados KRs | 6+ por objetivo | Máximo 3–4 KRs por objetivo |
| Sin línea de base | "Mejorar NPS" | "NPS aumenta de 32 a 50" |

Siempre señala anti-patrones y ofrece una reescritura.

## Formato de Salida

### OKRs [Trimestre] — [Equipo/Área de Producto]

---

**Objetivo 1: [Afirmación cualitativa inspiradora]**

*Por qué importa:* [Contexto estratégico de 1–2 oraciones]

| # | Resultado Clave | Línea de Base | Target | Método de Medición |
|---|---|---|---|---|
| KR1 | [Resultado medible] | [Estado actual] | [Target] | [Cómo se mide] |
| KR2 | [Resultado medible] | [Estado actual] | [Target] | [Cómo se mide] |
| KR3 | [Resultado medible] | [Estado actual] | [Target] | [Cómo se mide] |

*Propietario:* [Nombre/Rol]
*Cadencia de check-in:* Semanal

---

Repite para cada objetivo. Recomendamos 2–4 objetivos por equipo por trimestre.

## Guía de Puntuación a Incluir

Al final del trimestre, puntúa cada KR:
- 0.7–1.0 = Excelente (0.7 es el "punto dulce" — si todos los KRs puntúan 1.0, no eran lo suficientemente ambiciosos)
- 0.4–0.6 = Hizo progreso pero falló
- 0.0–0.3 = Falló — requiere discusión retrospectiva

## Inputs (infiere los que no se proporcionen — etiqueta las suposiciones)

- **Equipo o individuo** para los que son los OKRs
- **Trimestre y año**
- **Métrica North Star de la empresa o producto** (los OKRs deben conectar con esto — si no se da, infiere una plausible y etiquétala *(asumido)*)
- **Top 3 prioridades u objetivos para este trimestre** (notas aproximadas está bien)
- **Cualquier OKR existente a revisar o mejorar** (opcional)

## Directrices

- Conecta OKRs con el North Star de la empresa/producto; si no se da, infiere uno plausible y etiquétalo *(asumido)* en lugar de preguntar
- Recomienda no más de 3 objetivos por equipo por trimestre
- Si el usuario proporciona objetivos basados en output, siempre reenmarca como resultados
- Incluye una sección "health check" señalando qué KRs no tienen datos de línea de base actual
- Recuerda al usuario: los OKRs no son evaluaciones de desempeño — deben ser lo suficientemente ambiciosos para que fallar esté bien

## Controles de Calidad

- [ ] Cada KR es medible con una línea de base y target
- [ ] Sin KRs basados en output (sin "lanzar X" o "completar Y")
- [ ] Máximo 4 KRs por objetivo
- [ ] Los OKRs se conectan con el North Star de la empresa o producto
- [ ] Lo suficientemente ambiciosos para que 0.7 de cumplimiento sea la puntuación esperada

## Anti-Patrones

- [ ] No aceptes resultados clave basados en output — cualquier KR redactado como "lanzar X" o "completar Y" debe ser reescrito como un resultado con una línea de base y target
- [ ] No escribas OKRs sin preguntar por el North Star de la empresa o producto — los OKRs desconectados del contexto estratégico son solo un ejercicio de fijación de objetivos
- [ ] No escribas más de 4 KRs por objetivo — demasiados KRs diluyen el enfoque y hacen la puntuación ambigua al final del trimestre
- [ ] No uses KRs binarios (enviar/no enviar) — cada KR debe ser puntuable en una escala 0.0–1.0 basada en el grado de logro
- [ ] No omitas la sección de health check sobre líneas de base — los OKRs sin líneas de base actuales no pueden puntuarse objetivamente al final del trimestre
