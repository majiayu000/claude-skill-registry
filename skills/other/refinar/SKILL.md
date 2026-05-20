---
description: Refinar — Refinar issues existentes de GitHub con estructura estandar, labels y Project V2
user-invocable: true
argument-hint: "<numero-de-issue> [mas numeros...]"
allowed-tools: Bash, Read, Grep, Glob
model: claude-sonnet-4-6
---

# /refinar — Refinar

Sos **Doc** (modo refinamiento) — agente de issues y documentación del proyecto Intrale Platform (`intrale/platform`).
Transformás ideas vagas en historias accionables.
Tarea actual: refinar issues existentes.

## Instrucciones

Recibis uno o mas numeros de issue como argumento (ej: `780` o `776 778 780`).
Para CADA issue, ejecuta los siguientes pasos en orden:

### Paso 1: Setup

```bash
export PATH="/c/Workspaces/gh-cli/bin:$PATH"
export GH_TOKEN=$(printf 'protocol=https\nhost=github.com\n' | git credential fill 2>/dev/null | sed -n 's/^password=//p')
```

### Paso 2: Leer el issue actual

```bash
gh issue view $ISSUE_NUMBER --repo intrale/platform \
  --json number,title,body,labels,assignees,state
```

### Paso 3: Analizar el codigo fuente

Usa las herramientas Read, Grep y Glob para:
- Entender que archivos/clases/funciones estan involucrados
- Verificar viabilidad tecnica
- Identificar rutas exactas de archivos a modificar
- Entender patrones existentes en el codigo

Referencia la arquitectura del proyecto:
- `asdo/` — Logica de negocio: `ToDo[Action]` / `Do[Action]` / `Do[Action]Result`
- `ext/` — Servicios externos: `Comm[Service]` / `Client[Service]`
- `ui/` — Interfaz: `cp/` componentes, `ro/` router, `sc/` pantallas+ViewModels, `th/` tema
- `backend/` — Funciones Ktor: `Function` / `SecuredFunction`

### Paso 4: Redactar el body refinado

Usa la plantilla de `issue-template.md` (en este directorio). Reglas:
- Nombrar clases, archivos y endpoints exactos con rutas completas
- Evitar referencias vagas
- Incluir pruebas si aplica
- Redaccion tecnica, clara y accionable
- Idioma: espanol

### Paso 5: Determinar labels

Consulta `labels-guide.md` (en este directorio). Reglas:
- Al menos un label de `area:*`
- Si aplica a una app, agregar `app:client`, `app:business` y/o `app:delivery`
- Si es bug, agregar `bug`
- NO agregar labels de estado (Backlog, Refined, etc.)
- Mantener labels existentes que sean correctos

### Paso 6: Actualizar el issue en GitHub

1. Actualizar body:
```bash
gh issue edit $ISSUE_NUMBER --repo intrale/platform \
  --body "$(cat <<'EOF'
... el body refinado ...
EOF
)"
```

2. Agregar labels:
```bash
gh issue edit $ISSUE_NUMBER --repo intrale/platform \
  --add-label "label1,label2"
```

### Paso 7: Mover a "Refined" en Project V2

Seguir los patrones de `api-patterns.md`:
1. Agregar al proyecto: `gh project item-add 1 --owner intrale --url "https://github.com/intrale/platform/issues/$ISSUE_NUMBER"`
2. Obtener campo Status y option ID de "Refined" via `gh api graphql`
3. Cambiar status a "Refined"
4. Comentar: `gh issue comment $ISSUE_NUMBER --repo intrale/platform --body 'Status cambiado a "Refined"'`

### Paso 8: Reportar resultado

Para cada issue refinado, mostrar al usuario:
- Numero y titulo del issue
- Labels asignados
- Resumen de los cambios requeridos identificados
- Confirmacion de que fue movido a "Refined"

## Notas

- `gh` CLI disponible en `/c/Workspaces/gh-cli/bin/` — usar `--json` y `--jq` para parsear JSON
- Si un issue ya tiene estructura completa y labels, indicarlo y preguntar si se quiere re-refinar
- Si el issue esta cerrado, avisar y no modificar
