---
name: doc-to-app
description: Convierte un documento (PDF/texto) en una mini-app web interactiva lista para abrir en preview. Úsalo cuando quieras pasar de "contenido" a "producto usable".
---

# Doc-to-App (Documento a Mini-App)

Skill especializado en transformar documentos (PDF, texto, notas) en mini-aplicaciones web interactivas con buscador, filtros y navegación por secciones. Genera archivos listos para preview sin dependencias externas.

## Cuándo usar este skill

- Cuando tengas información en un PDF, texto o notas y quieras transformarla en una mini web navegable
- Cuando necesites crear una guía, catálogo, checklist o itinerario interactivo
- Cuando el usuario diga "convertí este documento en algo usable"
- Cuando quieras pasar de "contenido estático" a "producto compartible"
- Antes de compartir información compleja de forma más accesible

## Inputs necesarios

> **Regla**: Si falta alguno de estos inputs, PREGUNTAR antes de generar.

| Input               | Descripción                                      | Obligatorio |
| ------------------- | ------------------------------------------------ | ----------- |
| **Fuente**          | PDF o texto pegado con el contenido              | ✅ Sí       |
| **Tipo de app**     | Guía, catálogo, checklist, itinerario, FAQ, etc. | ✅ Sí       |
| **Prioridad**       | "Más visual" o "más práctica"                    | ✅ Sí       |
| **Idioma y estilo** | Ej: español, claro, sin jerga                    | Opcional    |

### Tipos de app soportados

| Tipo           | Estructura esperada    | Funcionalidades clave         |
| -------------- | ---------------------- | ----------------------------- |
| **Guía**       | Secciones + pasos      | Navegación, expandir/contraer |
| **Catálogo**   | Items con categorías   | Filtros, búsqueda, cards      |
| **Checklist**  | Lista de tareas        | Marcar como hecho, progreso   |
| **Itinerario** | Eventos por tiempo     | Timeline, filtros por día     |
| **FAQ**        | Preguntas y respuestas | Búsqueda, acordeón            |
| **Referencia** | Datos estructurados    | Búsqueda, filtros, copiar     |

## Reglas obligatorias

| Regla                   | Razón                             |
| ----------------------- | --------------------------------- |
| No devolver solo texto  | El output es una app funcional    |
| No sobrescribir nada    | Cada ejecución crea carpeta nueva |
| Mobile first            | Debe funcionar bien en móvil      |
| Sin frameworks externos | Solo HTML, CSS, JS vanilla        |
| Datos en JSON separado  | Facilita edición y mantenimiento  |

## Estructura de salida (crear siempre)

```
miniapp_<tema>_<YYYYMMDD_HHMM>/
├── index.html      # La app completa (HTML + CSS + JS inline)
├── data.json       # Datos estructurados del documento
└── README.txt      # Instrucciones de uso
```

### Convención de nombres

- **Tema**: slug del contenido (ej: `guia_viaje_paris`, `catalogo_productos`)
- **Fecha**: formato `YYYYMMDD_HHMM` (ej: `20260129_1626`)
- **Ejemplo completo**: `miniapp_guia_viaje_paris_20260129_1626/`

## Funcionalidades mínimas de la app

| #   | Funcionalidad         | Obligatoria  | Notas                                       |
| --- | --------------------- | ------------ | ------------------------------------------- |
| 1   | **Buscador**          | ✅ Sí        | Filtrar por texto en tiempo real            |
| 2   | **Filtros**           | ⚠️ Si aplica | Por categorías, etiquetas o tipo            |
| 3   | **Navegación**        | ✅ Sí        | Índice arriba o sidebar                     |
| 4   | **Responsive**        | ✅ Sí        | Mobile first, legible en cualquier pantalla |
| 5   | **Botón copiar**      | ⚠️ Si aplica | Para items que se copian frecuentemente     |
| 6   | **Marcar hecho**      | ⚠️ Si aplica | Para checklists, con localStorage           |
| 7   | **Expandir/contraer** | ⚠️ Si aplica | Para contenido largo o FAQs                 |

## Workflow (orden fijo)

### Paso 1: Analizar documento

1. Leer el documento completo
2. Identificar estructura: secciones, listas, tablas, puntos clave
3. Determinar tipo de app más adecuado
4. Definir categorías/etiquetas si aplica

### Paso 2: Estructurar datos

5. Convertir contenido a `data.json` con formato estandarizado
6. Validar que no hay información perdida
7. Agregar metadatos (título, descripción, fecha)

### Paso 3: Generar app

8. Crear carpeta con nombre según convención
9. Generar `index.html` con:
   - CSS inline (diseño limpio, responsive)
   - JS inline (buscador, filtros, interacciones)
   - Carga de datos desde `data.json` o embebido
10. Crear `README.txt` con instrucciones

### Paso 4: Validar

11. Verificar que se ve bien en preview
12. Probar buscador y filtros
13. Verificar responsive (simular móvil)
14. Confirmar que no hay contenido roto

### Paso 5: Entregar

15. Informar carpeta creada
16. Indicar archivo a abrir
17. Dar resumen de contenido y funcionalidades

## Instrucciones técnicas

### Estructura de data.json

```json
{
  "meta": {
    "title": "Título de la app",
    "description": "Descripción breve",
    "type": "guia|catalogo|checklist|itinerario|faq|referencia",
    "generated": "2026-01-29T16:26:00-03:00",
    "source": "Nombre del documento original"
  },
  "categories": [{ "id": "cat1", "name": "Categoría 1", "color": "#hexcolor" }],
  "items": [
    {
      "id": "item_001",
      "title": "Título del item",
      "content": "Contenido o descripción",
      "category": "cat1",
      "tags": ["tag1", "tag2"],
      "metadata": {}
    }
  ]
}
```

### Template base de index.html

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>[Título]</title>
    <style>
      /* Reset + variables + diseño mobile first */
      * {
        box-sizing: border-box;
        margin: 0;
        padding: 0;
      }
      :root {
        --primary: #3b82f6;
        --bg: #0f172a;
        --surface: #1e293b;
        --text: #f1f5f9;
        --text-muted: #94a3b8;
      }
      body {
        font-family: "Inter", system-ui, sans-serif;
        background: var(--bg);
        color: var(--text);
      }
      /* ... más estilos según tipo de app ... */
    </style>
  </head>
  <body>
    <header><!-- Título + buscador --></header>
    <nav><!-- Navegación/filtros --></nav>
    <main><!-- Contenido dinámico --></main>
    <script>
      // Cargar datos y renderizar
      // Implementar búsqueda y filtros
      // Guardar estado en localStorage si aplica
    </script>
  </body>
</html>
```

### Requisitos de diseño

| Aspecto           | Especificación                           |
| ----------------- | ---------------------------------------- |
| **Fuente**        | Inter o system-ui como fallback          |
| **Tema**          | Dark mode por defecto (moderno, legible) |
| **Contraste**     | Mínimo 4.5:1 en textos                   |
| **Espaciado**     | Consistente, mínimo 16px en mobile       |
| **Animaciones**   | Sutiles (transiciones de 200ms)          |
| **Touch targets** | Mínimo 44x44px en botones/links          |

### Manejo de errores

- Si el documento es muy largo (>50 secciones) → dividir en páginas o usar lazy loading
- Si no hay estructura clara → preguntar al usuario cómo organizarlo
- Si hay imágenes referenciadas → avisar que no se incluyen, sugerir URLs

## Output (formato exacto)

```markdown
## ✅ Mini-App Creada

### 📁 Carpeta

`miniapp_<tema>_<YYYYMMDD_HHMM>/`

### 🚀 Cómo abrir

Abrí el archivo: `miniapp_<tema>_<YYYYMMDD_HHMM>/index.html`

### 📊 Contenido incluido

| Métrica           | Valor                          |
| ----------------- | ------------------------------ |
| **Tipo de app**   | [guía/catálogo/checklist/etc.] |
| **Secciones**     | X                              |
| **Items totales** | X                              |
| **Categorías**    | X                              |

### ⚡ Funcionalidades

- ✅ Buscador por texto
- ✅ Filtros por [categorías/tags]
- ✅ Navegación por secciones
- ✅ Diseño responsive
- ✅ [Otras funcionalidades específicas]

### 📝 Archivos creados

| Archivo      | Descripción                      |
| ------------ | -------------------------------- |
| `index.html` | App completa, abrir en navegador |
| `data.json`  | Datos estructurados (editable)   |
| `README.txt` | Instrucciones de uso             |

### 💡 Notas

[Observaciones sobre el contenido, limitaciones o sugerencias de mejora]
```
