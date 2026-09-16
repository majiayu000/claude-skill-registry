---
name: naturalizacion-texto-ia
description: Naturaliza texto en español generado por IA aplicando 11 técnicas lingüísticas y detectando marcas técnicas/tipográficas (caracteres invisibles, watermarking, tipografía atípica) para mejorar la calidad editorial y naturalidad comunicativa. Produce el texto reescrito y un informe con diagnóstico cuantitativo.
triggers:
  phrases:
    - "naturalizar"
    - "humanizar"
    - "hacer más humano"
    - "quitar el estilo IA"
    - "suena a IA"
    - "suena a ChatGPT"
    - "suena a Claude"
    - "reescribir"
    - "mejorar texto"
  fileTypes:
    - ".txt"
    - ".md"
    - ".docx"
---

# Skill: Naturalizar Texto IA en Español

## Propósito

Transforma texto en español generado por IA para que suene auténtico, fluido y natural, mejorando su calidad comunicativa y editorial. **No tiene como objetivo evadir detectores de IA**, sino producir texto de mayor calidad para lectores humanos.

## Cuándo activarse

Esta skill se activa cuando el usuario:
- Proporciona texto en español generado por IA (pegado directamente o en archivo `.txt`, `.md`, `.docx`)
- Usa palabras clave como "naturalizar", "humanizar", "hacer más humano", "quitar el estilo IA", "reescribir"
- Menciona que el texto "suena a ChatGPT / Claude / IA"
- Pide mejorar la naturalidad o fluidez de un texto

---

## Lista negra de marcas IA

Estas palabras y patrones deben identificarse y tratarse en el Paso 2 y eliminarse en el Paso 3.

### Tier 1 — Conectores formulaicos (sustituir siempre)
- "En resumen", "En conclusión", "Es importante destacar que", "Por otro lado"
- "Como se puede ver", "Es evidente que", "Cabe mencionar", "Sin embargo" (al inicio de párrafo)
- "En definitiva", "Cabe destacar que", "Hoy en día", "Vale la pena señalar que"
- "Permíteme explicarte", "Del lado positivo", "Por lo tanto", "En consecuencia"
- "Además" (inicio de párrafo), "También" (inicio de párrafo)
- "A la hora de" + infinitivo (muletilla de apertura muy frecuente en texto generado)
- "No obstante" (al inicio de párrafo)

### Tier 2 — Vocabulario predecible IA (limitar a 1 ocurrencia o sustituir)
- "Transformar", "fomentar", "explorar", "cautivar", "profundo", "vital", "fundamental", "integral"
- "Implementación", "metodología", "utilización", "aprovechar", "optimizar", "facilitar"
- "Invaluable" (no existe en español estándar), "requerimiento" (usar "requisito")
- "Robusto" aplicado a procesos/sistemas de forma genérica (usar "sólido", "consistente", "bien planteado")
- "Panorama" como metáfora genérica ("el panorama actual") → "el momento actual", "la situación", o suprimir
- Cadenas de adverbios en "-mente" (más de 2 consecutivos)

### Tier 3 — Patrones estructurales (romper)
- Agrupamiento sistemático en tríos: "rápido, confiable y eficiente"
- "poder + infinitivo" repetido: "podría ser", "puede ayudar", "puede resultar" (más de 3 en un párrafo)
- Estructura predecible: "definición → importancia → tipos → conclusión"
- Párrafos todos de longitud similar (±2 oraciones de diferencia)

### Tier 4 — Guiones largos (eliminar siempre)
Los guiones largos (—) son una señal tipográfica característica del texto generado por IA en español. **Deben eliminarse siempre** y reemplazarse según el contexto:
- Si introduce un inciso o aclaración → usar paréntesis: `(aclaración)`
- Si introduce una conclusión o consecuencia → usar coma: `,`
- Si separa elementos de una enumeración → reformular como oración o usar coma

### Tier 5 — Marcas técnicas y tipográficas de IA (detectar y neutralizar siempre)

Estas marcas no son errores de estilo sino señales técnicas o tipográficas que delatan generación por IA de forma más directa que el vocabulario. Como modelo leyendo texto plano, no es posible escanear bytes crudos, pero sí es posible reconocer visualmente caracteres atípicos cuando se indican patrones concretos, y garantizar no producir esos caracteres en el Output A. Si el input es un archivo, usar el tool `Read` (y opcionalmente `Grep` con patrones de rango Unicode) para inspeccionar el contenido literal, ya que el render habitual del chat puede ocultar estos caracteres.

#### 5a. Caracteres invisibles y watermarking estadístico
- **Espacio de ancho cero** (zero-width space, U+200B) y caracteres de control invisibles relacionados: U+200C (ZWNJ), U+200D (ZWJ), U+FEFF (BOM/zero-width no-break space) aparecidos en medio de palabras o entre oraciones.
- **Selectores de variación Unicode** fuera de su uso legítimo con emoji: rango U+FE00–U+FE0F y el rango extendido U+E0100–U+E01EF. Su presencia en texto puramente alfabético en español es anómala.
- **Homoglifos**: letras que parecen latinas pero pertenecen a otro bloque Unicode (ejemplo: "а" cirílica U+0430 en vez de "a" latina; "е" cirílica U+0435 en vez de "e"; "і" ucraniana U+0456 en vez de "i"; "о" cirílica U+043E en vez de "o"; "р" cirílica U+0440 en vez de "p"; "с" cirílica U+0441 en vez de "c"). Sospechar cuando una palabra común no coincide con los patrones ortográficos esperados.
- **Watermarking estadístico de token** (esquemas tipo SynthID u otros que sesgan la elección de tokens): opera a nivel de logits del modelo generador y **no es detectable leyendo el texto como caracteres**. No existe una secuencia visible que buscar; la mitigación real ocurre al reescribir con variación léxica y rítmica propia (Técnicas 1, 2 y 4), que con alta probabilidad destruye cualquier patrón estadístico del texto original. Documentar esto en el Output B como advertencia, no como detección positiva/negativa.

**Tratamiento:** eliminar sin dejar rastro cualquier carácter de los rangos anteriores. Si un homoglifo forma parte de una palabra reconocible, sustituirlo por su equivalente latino y conservar la palabra. El Output A nunca debe contener caracteres de estos rangos ni homoglifos.

#### 5b. Tipografía sospechosa visible (más allá del guion largo, ya cubierto en Tier 4)
- **Comillas tipográficas curvas** " " (U+201C/U+201D) o ' ' (U+2018/U+2019) en vez de comillas españolas «» o comillas rectas "". Sustituir por «» (preferido en texto editorial/formal) o por "" rectas según el estilo ya usado en el documento.
- **Puntos suspensivos como carácter único** "…" (U+2026) en vez de tres puntos escritos "...". Reemplazar siempre por tres puntos.
- **Espacio de no separación atípico** (non-breaking space, U+00A0) fuera de los usos legítimos (unidades de medida, "20 °C", cifras con separador). Sustituir por espacio normal salvo en esos casos.
- **Guion corto (en-dash, –, U+2013)** usado donde correspondería un guion largo o una coma: aplicar la misma regla contextual de Tier 4. Reservar el en-dash solo para rangos numéricos ("2020-2024"), su uso legítimo en español.

**Tratamiento:** ninguno de estos caracteres debe sobrevivir al Output A salvo los usos legítimos señalados (NBSP en unidades, en-dash en rangos numéricos).

---

## Proceso (un solo pase)

### Paso 1 — Leer el input

- **Archivo**: usar el tool `Read` para leer el contenido del archivo indicado
- **Texto en el chat**: tomarlo directamente del mensaje del usuario

### Paso 2 — Análisis interno de patrones IA

Antes de reescribir, identificar y anotar internamente los patrones presentes:

| Patrón | Señal |
|---|---|
| Baja burstiness | Oraciones de longitud uniforme, sin variación rítmica |
| Baja perplexity | Vocabulario predecible, siempre la palabra más obvia |
| Conectores Tier 1 | Ver lista negra arriba |
| Vocabulario Tier 2 | Ver lista negra arriba |
| Guiones largos (—) | Presencia de em-dash tipográfico |
| Caracteres invisibles / watermarking | Zero-width space (U+200B), variation selectors (U+FE00-FE0F, U+E0100-E01EF), homoglifos cirílicos/latinos |
| Tipografía sospechosa visible | Comillas curvas " " ' ', puntos suspensivos "…" (U+2026), NBSP atípico (U+00A0), en-dash (–) mal usado |
| Agrupamiento en tríos | Ver Tier 3 |
| Ausencia de voz autoral | Sin posicionamiento, sin matices, sin perspectiva |
| Prosa enumerativa | Bullets y listas donde debería haber párrafos |
| Falta de marcadores españoles | Sin "eso sí", "la verdad es que", "dicho esto", "a fin de cuentas" |
| Ausencia de hedges | Sin imprecisiones naturales ni matices de incertidumbre |
| Sujeto siempre explícito | IA tiende a no aprovechar el pro-drop del español |

### Paso 3 — Aplicar las 11 técnicas de naturalización

Aplicar **simultáneamente** en un único pase de reescritura:

#### 1. Variación rítmica (burstiness)
Alternar deliberadamente frases cortas con largas. Romper la cadencia uniforme con cortes inesperados. Una frase corta. Después, una más extensa que desarrolle la idea con detalle y establezca conexiones que el lector puede seguir sin esfuerzo.

#### 2. Variación de surprisal léxico
Intercalar vocabulario de alta frecuencia (palabras función, términos simples) con palabras más precisas o inesperadas, creando picos y valles de densidad léxica a lo largo del texto. No mantener complejidad léxica uniforme: un párrafo puede ser más llano, el siguiente más elaborado. Evitar que cada oración tenga exactamente el mismo peso informativo.

#### 3. Marcadores discursivos del español real
Introducir expresiones propias del español escrito natural:
- "eso sí", "la verdad es que", "dicho esto"
- "claro que", "hay que decirlo", "a fin de cuentas"
- "en el fondo", "sin ir más lejos", "ahí está la clave"
- "por cierto", "en mi experiencia", "y no es un detalle menor"

#### 4. Regla 70/30 de vocabulario
- **70%** del vocabulario original se mantiene para preservar el significado
- **30%** se sustituye por sinónimos más precisos, coloquiales o inesperados según el tono

#### 5. Prosa integrada sobre listas
Convertir bullets y enumeraciones en párrafos continuos con conectores variados y no formulaicos. Evitar que la transición se note forzada.

#### 6. Hedges y matices naturales
Añadir imprecisiones propias del texto humano donde corresponda:
- "en general", "en la mayoría de los casos"
- "tiende a", "puede que", "no siempre es así"
- "al menos en principio", "salvo excepciones"

#### 7. Posicionamiento autoral
Introducir pequeñas marcas de voz que den perspectiva:
- "lo que resulta llamativo es"
- "vale la pena detenerse aquí"
- "esto es relevante porque"
- "y no es un detalle menor"

#### 8. Eliminación de conectores IA y marcas tipográficas/técnicas
- "Además" (párrafo) → integrar sin conector, o "y también", "sumado a esto"
- "Por otro lado" → "ahora bien", "dicho esto", o simplemente un punto y aparte
- "En conclusión" → "en definitiva", "a fin de cuentas", o reformular sin anunciarlo
- "Es importante destacar" → integrar la importancia directamente en la oración
- **Guiones largos (—) → siempre paréntesis o coma** (ver Tier 4 de la lista negra)
- **Caracteres invisibles y watermarking (Tier 5a)** → eliminar sin dejar rastro; si el carácter rompe una palabra reconocible, reconstruir la palabra
- **Homoglifos (Tier 5a)** → sustituir por el carácter latino equivalente
- **Comillas curvas, puntos suspensivos únicos, NBSP atípico, en-dash mal usado (Tier 5b)** → normalizar según las reglas de la Tier 5b de la lista negra

#### 9. Morfosintaxis específica del español
Aprovechar rasgos propios del español que la IA aplana:
- **Pro-drop**: omitir el sujeto cuando el contexto lo permite ("Llegué tarde" vs. "Yo llegué tarde")
- **Clíticos pronominales**: usar "me", "te", "le", "nos" naturalmente en verbos que los admiten
- **Orden flexible**: invertir ocasionalmente el orden SVO ("A ese problema le damos solución")
- **Subjuntivo**: usarlo en contextos de duda, deseo o condición donde la IA pone indicativo
- **Posición postnominal de adjetivos**: evitar el exceso de adjetivos prenominales (calco del inglés)

#### 10. Irregularidades estilísticas controladas
Introducir elementos que el texto IA raramente produce de forma espontánea:
- Preguntas retóricas puntuales
- Fragmentos breves (oraciones sin verbo cuando el contexto lo permite)
- Pequeñas digresiones o incisos explicativos
- Arranques de frase no convencionales (adverbio, participio, pregunta)
- Transiciones imperfectas: "por cierto", "volviendo al tema", "aunque esto es otro asunto"

#### 11. Coherencia tonal
Asegurar que el registro (formal, divulgativo, académico, conversacional) sea consistente de principio a fin y coherente con el tono del texto original. No mezclar registros sin justificación.

> **Nota sobre texto académico (paradoja académica):** La escritura académica bien estructurada obtiene naturalmente baja perplexity porque usa terminología estandarizada y estructuras formulaicas propias del género (esto no es un defecto: es la norma del registro). En textos académicos, la naturalización sigue esta guía operativa:
>
> **Qué SÍ tocar:**
> - Conectores formulaicos genéricos (Tier 1) que no son terminología del campo: "en conclusión", "cabe destacar", "es importante señalar" sí se sustituyen, incluso en registro académico, porque son muletillas de redacción, no términos técnicos.
> - Longitud y ritmo de oraciones dentro de un mismo párrafo (Técnica 1), sin romper la convención de oraciones más largas propia del género.
> - Guiones largos, comillas curvas, puntos suspensivos y demás Tier 4/5: se corrigen siempre, el registro académico no los legitima.
> - Estructura de párrafos (variar longitud) sin alterar la lógica argumentativa introducción→desarrollo→conclusión propia del género académico (distinto de la estructura genérica "definición→importancia→tipos→conclusión" de Tier 3, que sí se rompe).
>
> **Qué NO tocar:**
> - Terminología técnica y estandarizada del campo (no sustituir "metodología" por sinónimos informales si es el término correcto del área; Tier 2 aplica a uso genérico/inflado, no a terminología disciplinar precisa).
> - Marcadores discursivos coloquiales (Técnica 3: "eso sí", "la verdad es que") no se introducen en registro académico formal; ahí el marcador equivalente es "cabe señalar, sin que ello implique..." o similar, manteniendo formalidad.
> - Voz pasiva y estructuras impersonales convencionales del género académico (no forzar voz activa/pro-drop si el campo exige impersonalidad, p. ej. "se observó que" en vez de "observé que").
> - Subjuntivo y morfosintaxis: aplicar solo donde ya es gramaticalmente natural, no forzar.
>
> En el Output B, para texto académico, incluir una línea aclarando que un score más bajo en "variación rítmica" o "diversidad léxica" puede ser esperable y no indica fallo de naturalización, sino fidelidad al registro.

### Paso 3.5 — Verificación final antes de entregar

Antes de generar los outputs, releer el texto reescrito completo buscando específicamente:
- Guiones largos (—) residuales
- Cualquier carácter Tier 5 (comillas curvas, puntos suspensivos únicos, NBSP, en-dash, caracteres invisibles, homoglifos)
- Conectores Tier 1 que hayan quedado sin sustituir, especialmente en textos largos donde el primer párrafo se corrige con más cuidado que los últimos

Si el texto supera ~500 palabras, hacer esta verificación por bloques para no perder atención al final del documento. Esta verificación es la causa más común de que sobrevivan marcas IA en textos largos.

### Paso 4 — Generar los dos outputs

---

## Outputs

### Output A — Texto naturalizado

Presentar el texto reescrito directamente, sin prefacio ni comentarios editoriales inline. El texto debe:
- Mantener el mismo significado e información que el original
- Aplicar las 11 técnicas de forma integrada y no mecánica
- No contener guiones largos (—), ni ningún carácter de las categorías Tier 5 (caracteres invisibles, homoglifos, comillas curvas, puntos suspensivos de carácter único, NBSP atípico, en-dash mal empleado)
- Preservar la corrección ortográfica y gramatical (no introducir errores)
- Respetar el tono y registro del texto original

---

### Output B — Informe de naturalización

```
## Informe de naturalización

### Patrones IA detectados en el original
- [listar los patrones del Paso 2, incluyendo guiones largos si los había]
- [si se detectan marcas Tier 5a (caracteres invisibles/watermarking), listar tipo y ubicación aproximada, ej. "zero-width space detectado tras la palabra 'información', párrafo 3"]

### Técnicas aplicadas y cambios destacados
- [2-4 ejemplos concretos formato: ANTES → DESPUÉS]

### Diagnóstico cuantitativo

| Métrica | Valor estimado | Umbral humano | Estado |
|---|---|---|---|
| Conectores Tier 1 | X% de párrafos | < 10% | ✓ / ✗ |
| Guiones largos (—) | X encontrados | 0 | ✓ / ✗ |
| Variación de longitud oracional | Alta / Media / Baja | Alta | ✓ / ✗ |
| Diversidad léxica (TTR estimado) | Alta / Media / Baja | > 0.50 | ✓ / ✗ |
| Voz pasiva | X% de oraciones | 10-20% | ✓ / ✗ |
| Marcadores discursivos del español | Presentes / Ausentes | Presentes | ✓ / ✗ |
| Marcas técnicas/tipográficas Tier 5 | X encontradas (detalle por tipo) | 0 | ✓ / ✗ |

### Puntuación de naturalidad

| Dimensión | Puntos (máx. 20) | Justificación breve |
|---|---|---|
| Variación rítmica y surprisal | X/20 | ... |
| Diversidad léxica | X/20 | ... |
| Marcadores discursivos del español | X/20 | ... |
| Eliminación de conectores IA y guiones | X/20 | ... |
| Coherencia tonal y morfosintaxis | X/20 | ... |
| Ausencia de marcas técnicas y tipográficas IA (Tier 5) | X/20 | ... |
| **TOTAL** | **X/120** | |
```

> Nota (texto académico): si el texto de entrada es de registro académico/formal, añadir aquí una línea aclarando que un score algo más bajo en "Variación rítmica y surprisal" o "Diversidad léxica" puede reflejar fidelidad al género, no un fallo de naturalización (ver guía operativa en la nota de paradoja académica del Paso 3).

---

## Fundamento técnico

- **Perplexity léxica** (DivEye, TMLR 2026): el texto humano varía la imprevisibilidad léxica creando picos y valles. La IA produce distribuciones uniformes.
- **Burstiness rítmica** (Xia et al., EACL 2026): la variación de longitud oracional tiene correlación de Pearson > 0.7 con la detección de texto IA.
- **Marcadores culturales**: el español tiene un repertorio de marcadores discursivos propios que los modelos omiten o reemplazan por calcos del inglés (González Ledesma, 2024).
- **Guiones largos**: patrón tipográfico estadísticamente sobrerepresentado en texto IA en español; los hablantes nativos los perciben como señal artificial.
- **Marcas técnicas y tipográficas (Tier 5)**: caracteres invisibles, homoglifos y tipografía atípica (comillas curvas, puntos suspensivos unicarácter, NBSP, en-dash) son señales técnicas adicionales a la superficie léxica; el watermarking estadístico de tokens (tipo SynthID) no deja huella textual identificable y se mitiga indirectamente mediante la reescritura léxica y rítmica, no mediante detección directa.

Esta skill **no introduce errores tipográficos ni ortográficos deliberados**. La corrección se preserva; la naturalidad se logra por vía estilística, léxica y morfosintáctica.

---

## Ejemplo de activación

**Usuario:** "Este texto suena muy a IA, ¿puedes naturalizarlo?"

**Respuesta esperada:**
1. Leer el texto proporcionado
2. Analizar patrones IA presentes (incluyendo guiones largos y marcas Tier 5)
3. Reescribir aplicando las 11 técnicas en un pase
4. Verificar el resultado (Paso 3.5) antes de entregar
5. Presentar Output A (texto naturalizado, sin guiones largos ni marcas Tier 5) seguido de Output B (informe con diagnóstico cuantitativo y puntuación sobre /120)

---

## Limitaciones

- **Preservación de significado**: no se cambia el contenido informativo, solo la forma
- **Registro**: el tono de salida debe ser coherente con el de entrada; no se convierte texto académico en coloquial sin indicación explícita
- **Texto académico**: en géneros con estructuras formulaicas propias, la naturalización se centra en variación de conectores, puntuación y marcas Tier 5, no en informalidad (ver guía operativa qué SÍ/NO tocar en el Paso 3)
- **Extensión**: textos muy largos (>2000 palabras) pueden procesarse por secciones si el usuario lo indica; en cualquier caso, el Paso 3.5 exige verificación por bloques a partir de ~500 palabras
- **Watermarking estadístico**: la skill no puede detectar ni garantizar la eliminación de watermarking a nivel de token (tipo SynthID); solo mitiga indirectamente mediante la reescritura léxica y rítmica
