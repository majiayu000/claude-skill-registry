---
name: weekly-newsletter
description: "Genera la newsletter semanal de DevExpert recopilando contenido de X, YouTube, PostFlow y bookmarks. Crea borrador en Listmonk para revisión."
---

# Weekly Newsletter DevExpert

Genera la newsletter semanal recopilando todo el contenido publicado y programado de la semana.

## Cuándo se usa

- Una vez por semana, en el día/hora que defina el cron activo.
- Rangos de contenido (agnóstico del día):
  - **X (tweets propios + bookmarks), PostFlow y YouTube**: últimos 7 días hasta el momento de ejecución.
  - Si hay una fecha/hora de corte indicada por el usuario, usar esa en lugar de la ventana de 7 días.

## Flujo de trabajo

### Dependencia de Listmonk (importante)

Para cualquier operación de Listmonk (listas, suscriptores, campañas, schedule, archive), usar como referencia principal la skill [listmonk-cli](../listmonk-cli/SKILL.md).

Esta skill (`weekly-newsletter`) define el flujo editorial y el contenido; `listmonk-cli` es la referencia operativa del CLI.

### 1. Recopilar contenido de todas las fuentes

**X/Twitter** (bird CLI):
```bash
bird user-tweets antonioleivag -n 50 --json
```
Filtrar por fechas del rango.

**PostFlow** (posts programados):
```bash
postflow --json schedule list --from YYYY-MM-DDTHH:MM:SSZ --to YYYY-MM-DDTHH:MM:SSZ
```

**YouTube** (vídeos publicados o programados):
```bash
python list_videos.py --limit 10 --json
```
Usa el script `list_videos.py` incluido en la skill `youtube-publish` (carpeta `scripts/`).

El flag `--json` devuelve título, descripción, fecha, estado y URL. La descripción indica quién ha grabado el vídeo (Antonio o Nino) y de qué trata exactamente.

**Bookmarks de X** (lecturas recomendadas):
```bash
bird bookmarks -n 100
```
Usar 100 bookmarks para asegurar cobertura del rango completo. Filtrar por fechas.

### 2. Proponer lista de temas al usuario

Primero, analizar si hay un **tema dominante** en la semana:
- ¿Hay un tema que aparece en múltiples posts propios, bookmarks y conversaciones?
- ¿Se ha hablado de lo mismo desde varios ángulos (artículo, podcast, reflexiones)?
- Si la respuesta es sí, usar la estructura con "El tema de la semana"

Presentar el contenido en DOS bloques:

**BLOQUE 1: Contenido recomendado para la newsletter**
Organizado por secciones (ver estructura más abajo):
- **El tema de la semana** (si hay tema dominante) - agrupa contenido propio y de terceros sobre ese tema
- Vídeo de la semana
- Lo que ha pasado (contenido propio que no entre en el tema de la semana)
- Lecturas recomendadas (bookmarks de terceros que no entren en el tema de la semana)
- Reflexión de la semana (si hay)
- Novedades de modelos (si hay - buscar en bookmarks lanzamientos de modelos)

**BLOQUE 2: Lo que queda fuera**
Listar el contenido dentro del rango que no se ha incluido en el bloque 1, para que el usuario pueda decidir si añadir algo.

El usuario revisa y ajusta antes de generar el borrador.

### 3. Crear borrador en Listmonk

Antes de ejecutar comandos de Listmonk, consultar [listmonk-cli](../listmonk-cli/SKILL.md) si hay dudas de flags, formatos o troubleshooting.

Escribir el contenido en un archivo temporal:
```
/tmp/newsletter-YYYY-MM-DD.md
```

Crear la campaña:
```bash
listmonk campaigns create \
  --name "Newsletter semanal - DD mes YYYY" \
  --subject "<subject atractivo>" \
  --lists 3 \
  --template-id 1 \
  --content-type markdown \
  --body-file /tmp/newsletter-YYYY-MM-DD.md
```

Habilitar el archivo público de la campaña:
```bash
listmonk campaigns archive <id> --enable
```

Tras crear el borrador, **abrir la campaña en el navegador** con:
```
open "<LISTMONK_BASE_URL>/admin/campaigns/<id>"
```
La URL base de Listmonk está en `~/.config/skills/config.json` bajo `listmonk.base_url`.

Para actualizar tras cambios:
```bash
listmonk campaigns update <id> \
  --body-file /tmp/newsletter-YYYY-MM-DD.md \
  --lists 3
```

### 4. Programar envío (solo con confirmación explícita)

**Regla:** No programar nunca sin confirmación explícita del usuario.

Por defecto, programar según el horario que indique el usuario. Si no indica hora, usar una propuesta explícita y pedir confirmación.

```bash
listmonk campaigns schedule <id> \
  --send-at "YYYY-MM-DDTHH:MM:SS+01:00"
```

## Estructura de la newsletter

### Estructura A: Con tema dominante de la semana

Usar cuando hay un tema claro que ha dominado la semana. El bloque "El tema de la semana" se escribe de forma **narrativa**, con los enlaces integrados en el texto (no al final de cada párrafo).

```markdown
¡Hola DevExpert!

[Intro 2-3 líneas contextualizando la semana y adelantando el tema principal]

**TL;DR de esta semana:**
- **Vídeo:** [Título del vídeo](URL) - Descripción corta
- **Tema de la semana:** Título del tema - Resumen en una línea
- **Nuevos modelos:** [Modelo 1](enlace) (qué hace) · [Modelo 2](enlace)

---

## El tema de la semana: [Título del tema]

[Texto narrativo que va contando la historia del tema, integrando enlaces en el propio texto. Por ejemplo:]

[Herramienta X](enlace) ha revolucionado la forma de trabajar esta semana. La idea es simple: [explicación].

El hype ha sido brutal. [Fulano contaba](enlace) cómo logró X. [Otro usuario](enlace) hizo Y.

Por mi parte, escribí [un artículo sobre Z](enlace). En [el podcast de esta semana](enlace) profundizamos en todo esto.

[El texto fluye como una narrativa, no como una lista de items separados]

---

## El vídeo de la semana: [Título]

[Descripción breve del vídeo principal]

[Ver el vídeo en YouTube](URL)

---

## Novedades de modelos (opcional)

**[Modelo 1](enlace)** - [Descripción breve]

**[Modelo 2](enlace)** - [Descripción breve]

---

## Próxima edición de AI Expert

[CTA fijo hacia devexpert.io]

[Toda la información aquí](https://devexpert.io/cursos/expert/ai)

---

Un abrazo,

Antonio.
```

### Estructura B: Sin tema dominante (semana variada)

Usar cuando no hay un tema claro y el contenido es variado.

```markdown
¡Hola DevExpert!

[Intro 2-3 líneas contextualizando la semana]

**TL;DR de esta semana:**
- **Vídeo:** [Título del vídeo](URL) - Descripción corta
- **Destacado:** Tema principal - Resumen en una línea
- **Nuevos modelos:** [Modelo 1](enlace) (qué hace) · [Modelo 2](enlace)

---

## El vídeo de la semana: [Título]

[Descripción breve del vídeo principal]

[Ver el vídeo en YouTube](URL)

---

## Lo que ha pasado esta semana

**[Tema 1]**

[Descripción + opinión]

[Enlace]

**[Tema 2]**

[...]

---

## Lecturas recomendadas

**[Título de tercero 1]**

[Por qué es interesante, puntos clave]

[Enlace]

**[Título de tercero 2]**

[...]

---

## Reflexión de la semana: [Título] (opcional)

[Reflexión personal más extensa]

[Enlace]

---

## Novedades de modelos (opcional)

**[Modelo 1](enlace)** - [Descripción breve]

**[Modelo 2](enlace)** - [...]

---

## Próxima edición de AI Expert

[CTA fijo hacia devexpert.io]

[Toda la información aquí](https://devexpert.io/cursos/expert/ai)

---

Un abrazo,

Antonio.
```

## Reglas de estilo

- **TL;DR**: Siempre después de la intro. El vídeo de la semana va primero. Usar anclas (#seccion) para enlaces internos
- **Tono**: Directo, sin rodeos, con criterio técnico
- **Emojis**: Mínimos (0-2 en todo el email)
- **Enlaces**: Alternar entre X y LinkedIn para distribuir tráfico
- **No incluir**: El vídeo de la semana anterior si ya salió en la newsletter previa
- **Bookmarks**: Usar para "Lecturas recomendadas" - contenido de terceros que aporta valor
- **Novedades de modelos**: Sección opcional (si hay esa semana) al final, antes del CTA. Interesa a un grupo reducido, por eso va abajo. Buscar en bookmarks lanzamientos de modelos nuevos
- **Saludo**: Siempre "¡Hola DevExpert!"

## Parámetros de Listmonk

- **Lista**: DevExpert (id: 3)
- **Template**: DevExpert (id: 1)
- **Content-type**: markdown

## Versión HTML para X Articles

Después de programar la newsletter en Listmonk, ofrece a Antonio generar una versión HTML adaptada para publicar como artículo en X.

Si acepta:
1. Toma el contenido de la newsletter ya aprobada
2. Conviértelo a HTML limpio (sin estilos inline de email, sin tablas de layout)
3. Propón un **título llamativo** para X (evitar títulos genéricos tipo "Newsletter semanal..."). Debe despertar curiosidad y dejar claro el beneficio en 1 frase.
4. Inserta ese título como `<h1>` al inicio del HTML.
5. Usa tags semánticos: `<h1>`, `<h2>`, `<p>`, `<a>`, `<strong>`, `<blockquote>`, `<hr>`
6. Para enlaces a posts de X (`x.com`), muestra la URL en texto claro dentro del contenido (no solo ancla), para poder copiar/pegar e integrar el post fácilmente en X Articles.
7. Elimina el CTA de AI Expert (de momento, para medir si el contenido funciona por sí solo)
8. Elimina el saludo "¡Hola DevExpert!" y el cierre "Un abrazo, Antonio"
9. Guarda el fichero HTML en `~/Documents/aipal/newsletter-html/YYYY-MM-DD.html`
10. Genera una imagen de portada para el artículo en formato **5:2** (por ejemplo 1500x600 o 2000x800) usando el skill nano-banana-pro, con un diseño llamativo y relacionado con el tema principal de la newsletter (que no parezca una portada genérica). Guarda la imagen en `~/Documents/aipal/newsletter-html/YYYY-MM-DD-cover.png`
11. Envía por Telegram: título sugerido + HTML como documento + imagen, para que Antonio pueda pegarlo en X Articles

## Registro en el vault (paso final obligatorio)

Al finalizar (después de crear el borrador en Listmonk), añadir una entrada al fichero `~/Documents/aipal/10-areas/contenido/learnings.md`. Si el fichero no existe, crearlo.

**Formato del bloque a añadir** (append, nunca truncar):

```markdown
## YYYY-MM-DD — Newsletter semanal

- **Tema central**: [título o descripción del tema dominante, o "variada" si no hubo uno]
- **Estructura usada**: A (con tema dominante) / B (variada)
- **Secciones incluidas**: [lista: vídeo semana, tema semana, lo que pasó, lecturas recomendadas, novedades modelos, reflexión…]
- **Contenido propio destacado**: [títulos de posts propios más relevantes de la semana]
- **Bookmarks incluidos**: [número y temáticas]
- **Campana Listmonk ID**: [id]
```

Este registro permite que futuras sesiones conozcan el historial de newsletters sin necesidad de consultarlo manualmente.

## Notas

- La newsletter se queda en estado `draft` hasta que Antonio la revise y programe
- Los enlaces a vídeos privados de YouTube funcionan una vez se publican
- Si hay vídeo programado para el jueves, incluir el enlace aunque esté privado
