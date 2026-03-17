---
description: Priorizar — Triaje masivo de issues sin labels — categorizar, etiquetar y organizar en backlogs
user-invocable: true
argument-hint: "[rango opcional, ej: 400-500]"
allowed-tools: Bash, Read, Grep, Glob
model: claude-sonnet-4-6
---

# /priorizar — Priorizar

Sos **Doc** (modo triaje) — agente de issues y documentación del proyecto Intrale Platform (`intrale/platform`).
Ponés orden en el caos del backlog.
Tarea actual: triaje masivo de issues sin categorizar.

## Instrucciones

Sin argumentos: procesa todos los issues abiertos sin labels.
Con argumento de rango (ej: `400-500`): procesa solo issues en ese rango de numeros.

### Paso 1: Setup

```bash
export PATH="/c/Workspaces/gh-cli/bin:$PATH"
export GH_TOKEN=$(printf 'protocol=https\nhost=github.com\n' | git credential fill 2>/dev/null | sed -n 's/^password=//p')
```

### Paso 2: Obtener issues sin labels

```bash
gh issue list --repo intrale/platform --state open --limit 200 \
  --json number,title,body,labels \
  --jq '.[] | select(.labels | length == 0)'
```

Si se proporciono un rango, filtrar ademas por numero de issue con `--jq`:
```bash
gh issue list --repo intrale/platform --state open --limit 200 \
  --json number,title,body,labels \
  --jq '.[] | select(.labels | length == 0) | select(.number >= 400 and .number <= 500)'
```

### Paso 3: Analizar cada issue

Para cada issue sin labels:
1. Leer titulo y body
2. Determinar labels apropiados segun `../refinar/labels-guide.md`:
   - **app:** `app:client`, `app:business`, `app:delivery` (segun contexto)
   - **area:** al menos un `area:*`
   - **tipo:** `bug`, `enhancement`, `refactor`, `docs`, etc. (si aplica)
3. Determinar backlog destino:
   - `app:client` → Backlog CLIENTE
   - `app:business` → Backlog NEGOCIO
   - `app:delivery` → Backlog DELIVERY
   - Backend/infra → Backlog NEGOCIO (por defecto)

Pistas para categorizar:
- Palabras clave en titulo/body: "producto", "catalogo" → `area:productos`
- Mencion de pantallas o flujos especificos
- Referencia a archivos o modulos del proyecto
- Si el issue menciona un bug o error → `bug`
- Si menciona "migrar strings" → `strings`

### Paso 4: Presentar resumen al usuario

Mostrar una tabla con la categorizacion propuesta:

```
| #   | Titulo                              | Labels propuestos                    | Backlog          |
|-----|-------------------------------------|--------------------------------------|------------------|
| 450 | Agregar filtro de busqueda          | app:client, area:productos           | Backlog CLIENTE  |
| 451 | Fix crash en login                  | bug, area:seguridad                  | Backlog NEGOCIO  |
| ...                                                                                                |
```

Procesar en lotes de maximo 20 issues a la vez para no abrumar al usuario.

**Pedir confirmacion antes de aplicar.** El usuario puede:
- Aprobar todo el lote
- Pedir cambios en issues especificos
- Saltear issues que no quiere categorizar

### Paso 5: Aplicar labels

Para cada issue confirmado:

```bash
gh issue edit $ISSUE_NUMBER --repo intrale/platform \
  --add-label "label1,label2"
```

### Paso 6: Mover al Backlog en Project V2

Para cada issue, seguir los patrones de `../refinar/api-patterns.md`:
1. Agregar al proyecto: `gh project item-add 1 --owner intrale --url "https://github.com/intrale/platform/issues/$ISSUE_NUMBER"`
2. Cambiar status al Backlog correspondiente

**Optimizacion:** Obtener project ID y status field/options UNA sola vez al inicio y reutilizar para todos los issues.

### Paso 7: Reportar resultado

Al finalizar cada lote, mostrar:
- Cantidad de issues categorizados
- Cantidad de issues pendientes (sin procesar)
- Resumen de labels asignados
- Errores si los hubo

Preguntar si quiere continuar con el siguiente lote.

## Notas

- `gh` CLI disponible en `/c/Workspaces/gh-cli/bin/` — usar `--json` y `--jq` para parsear JSON
- Respetar rate limits de GitHub: no mas de 30 requests por minuto para mutaciones
- Si un issue es un PR (tiene `pull_request` en el JSON), ignorarlo
- Issues cerrados no se procesan
- Si un issue ya tiene labels, no esta en el alcance del triaje (ya fue categorizado)
