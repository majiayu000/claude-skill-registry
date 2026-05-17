# humanizar-texto-es

Una skill para Claude Code que reescribe texto en español generado por IA para que suene naturalmente humano.

## Qué hace

Toma un archivo de texto en español producido por IA (ChatGPT, Claude, Gemini, etc.) y lo reescribe aplicando 11 técnicas lingüísticas simultáneas que aumentan su perplejidad y burstiness, haciéndolo indistinguible de escritura humana natural.

Siempre genera dos archivos de salida:
- **`{nombre}_humanizado.{ext}`** — el texto reescrito, listo para usar
- **`{nombre}_analisis.md`** — informe de investigación con puntuación de humanidad, patrones detectados y cambios aplicados

## Para qué sirve

Está pensada para investigación sobre técnicas de evasión de detectores de IA. No es una herramienta de engaño: el objetivo es estudiar cómo los modelos de lenguaje producen patrones reconocibles y qué transformaciones los eliminan.

## Formatos de entrada soportados

`.pdf` · `.docx` · `.md` · `.txt`

> Los PDF se convierten a DOCX en la salida.

## Las 11 técnicas aplicadas

| # | Técnica | Descripción |
|---|---|---|
| 1 | Reformulación sintáctica | Varía la estructura de las oraciones mezclando simples y compuestas |
| 2 | Control de burstiness | Alterna frases muy cortas (3-6 palabras) con frases largas (25-35 palabras) |
| 3 | Control de perplejidad | Usa palabras menos esperadas y giros creativos pero naturales |
| 4 | Marcadores discursivos españoles | Inserta expresiones como *eso sí*, *la verdad es que*, *al fin y al cabo*, *vamos*, *mira* |
| 5 | Regla 70/30 de vocabulario | Mantiene coherencia en el 70-80% del vocabulario y varía el 20-30% restante |
| 6 | Variación de registro | Alterna tono formal académico con momentos más conversacionales |
| 7 | Elementos emocionales y subjetivos | Añade opiniones, juicios de valor y pequeñas reacciones |
| 8 | Referencias concretas y específicas | Sustituye ejemplos genéricos por referencias hipotéticas concretas |
| 9 | Eliminación de listas paralelas | Convierte bullet points y enumeraciones en prosa integrada |
| 10 | Imprecisiones humanas naturales | Añade hedges: *más o menos*, *en cierta medida*, *no del todo* |
| 11 | Errores tipográficos controlados | Introduce 1-2 inconsistencias menores de puntuación o estilo |

## Puntuación de humanidad

La skill evalúa el resultado con una puntuación de 0 a 100 basada en 5 criterios:

| Criterio | Puntos |
|---|---|
| Variación de longitud de frases (burstiness) | 25 |
| Uso de marcadores discursivos españoles | 20 |
| Variación de vocabulario (regla 70/30) | 20 |
| Elementos emocionales y subjetivos | 20 |
| Ausencia de listas y estructuras paralelas | 15 |

## Instalación

Requiere [Claude Code](https://claude.ai/code) con soporte de skills.

```bash
# Clona el repositorio en tu carpeta de skills de Claude Code
git clone https://github.com/ToniPerea/humanizar-texto-es ~/.claude/skills/humanizar-texto-es
```

Una vez instalada, Claude Code la detecta automáticamente. Se activa cuando proporcionas un archivo de texto en español generado por IA.

## Uso

Simplemente abre Claude Code y proporciona la ruta a tu archivo:

```
humaniza este archivo: mi_texto.pdf
```

o

```
/humanizar-texto-es mi_ensayo.docx
```

Claude detectará que la skill aplica y ejecutará el proceso completo.

## Limitaciones

- Solo funciona con texto en **español**
- El texto debe tener al menos **100 palabras**
- No está diseñada para texto ya humanizado manualmente

## Estructura del repositorio

```
humanizar-texto-es/
├── SKILL.md      # Definición completa de la skill (instrucciones para Claude)
└── README.md     # Este archivo
```

## Licencia

MIT
