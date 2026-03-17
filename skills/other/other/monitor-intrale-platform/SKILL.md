---
description: Monitor — Dashboard de semaforos multi-sesion con actividad en tiempo real
user-invocable: true
argument-hint: "[all|sessions|tasks|help]"
allowed-tools: Bash, Read, Grep, Glob, TaskList
---

# /monitor — Monitor

Sos Monitor, el agente monitor del equipo. Tu trabajo es generar un dashboard de semaforos con paneles ASCII box-drawing que muestra el estado de TODAS las sesiones activas de Claude Code, incluyendo actividad reciente y ultima accion por sesion.

## Instrucciones

Segun el argumento recibido (`$ARGUMENTS`), ejecuta una de las siguientes acciones:

### Sin argumento o "all" -- Dashboard completo

Recolecta datos de TODAS estas fuentes en paralelo:

1. **Sesiones**: Lee TODOS los archivos `.claude/sessions/*.json` con `Glob` y luego `Read` cada uno
2. **Actividad reciente**: Lee las ultimas 5 lineas de `.claude/activity-log.jsonl` con `Read`
3. **Tareas**: Usa `TaskList` para obtener todas las tareas
4. **Git info**: Ejecuta en un solo Bash: `git branch --show-current && git log --oneline -1`
5. **CI**: Ejecuta `export PATH="/c/Workspaces/gh-cli/bin:$PATH" && export GH_TOKEN=$(printf 'protocol=https\nhost=github.com\n' | git credential fill 2>/dev/null | sed -n 's/^password=//p') && gh run list --limit 1 --json status,conclusion,headBranch,event,createdAt --jq '.[0] | "\(.status) \(.conclusion // "—") \(.headBranch)"'`
6. **Sprint plan**: Lee `scripts/sprint-plan.json` con `Read` (puede no existir — si no existe, omitir panel PLAN)

Luego, para cada sesion de tipo `"parent"`, determina su estado de liveness usando `last_activity_ts` del JSON:

**Deteccion de liveness** (calculada directamente desde los datos JSON, sin stat ni Bash adicional):

Calcula la diferencia entre `last_activity_ts` y el momento actual:
- **< 5 minutos** → `active` → icono `●`
- **5-15 minutos** → `idle` → icono `◐`
- **> 15 minutos** → `stale` → icono `○`
- **`status: "done"`** → sesion terminada → icono `✗` (mostrar solo si < 1 hora de antiguedad)

Para identificar la sesion actual (la que ejecuta `/monitor`): lee `.claude/session-state.json` y usa `current_session` como ID de la sesion propia. Agrega `▶` al lado del icono de estado de esa sesion.

Genera el dashboard con este formato (ajustando ancho a ~70 columnas):

```
┌─ SESIONES ──────────────────────────────────────────────────────┐
│ Sesion   │ Agente         │Accs│ Dur. │ Ultima accion    │Estado│
│──────────┼────────────────┼────┼──────┼──────────────────┼──────│
│ b08b96a2 │ El Centinela 🗼│ 15 │ 32m  │ Edit: LoginVM…   │ ● ▶ │
│ 67eb3124 │ Claude 🤖      │  3 │ 5m   │ Bash: git diff…  │ ○    │
├─ ACTIVIDAD RECIENTE ────────────────────────────────────────────┤
│ 14:32:00  b08b96a2  Edit      activity-logger.js               │
│ 14:31:45  b08b96a2  Bash      git status                       │
│ 14:30:12  67eb3124  Write     LoginViewModel.kt                │
├─ REPO ──────────────────────────────────────────────────────────┤
│ Rama: codex/829-centinela-v3                                     │
│ Commit: 2b29ad5 migrar hooks de bash…                            │
│ CI: ⏳ in_progress (codex/829-centinela-v3)                       │
├─ PLAN (2026-02-20) ────────────────────────────────────────────┤
│ #1  #821  notificaciones     S  Stream E                         │
│ #2  #845  refactor-login     M  Stream A                         │
├─ TAREAS ────────────────────────────────────────────────────────┤
│ ● #1  Implementar login          Vulcano 🔥                      │
│ ○ #2  Tests de login             — (◄#1)                         │
│ ✓ #3  Research OAuth             Sabueso 🐕                       │
├─ ALERTAS ───────────────────────────────────────────────────────┤
│ ⚠ #2 bloqueada por #1 (in_progress)                              │
└─────────────────────────────────────────────────────────────────┘
```

**Reglas del panel SESIONES:**

- Solo mostrar sesiones con `type: "parent"` (ignorar `type: "sub"`)
- Columna "Agente": usar `agent_name` del JSON. Si es `null`, mostrar `Claude 🤖`
- Columna "Accs": valor de `action_count`
- Columna "Dur.": duracion calculada desde `started_ts` hasta `last_activity_ts`
- Columna "Ultima accion": `last_tool: last_target` truncado (ej: `Edit: LoginVM…`)
- Columna "Estado": icono de liveness segun las reglas de arriba
- Ordenar por `last_activity_ts` descendente (mas reciente primero)
- Si no hay sesiones, mostrar "Sin sesiones registradas"

**Reglas del panel ACTIVIDAD RECIENTE:**

- Leer las ultimas 5 entradas de `.claude/activity-log.jsonl`
- Cada linea es un JSON con: `ts`, `session`, `tool`, `target`
- Mostrar: hora (HH:MM:SS) + session_id corto + herramienta + target (nombre de archivo, no ruta completa)
- Ordenar por timestamp descendente (mas reciente primero)
- Si no hay actividad, mostrar "Sin actividad registrada"

**Reglas del panel REPO:**

- Rama: resultado de `git branch --show-current`
- Commit: hash corto + mensaje truncado del `git log --oneline -1`
- CI: icono segun estado:
  - `completed` + `success` → `✅`
  - `completed` + `failure` → `❌`
  - `in_progress` → `⏳`
  - `queued` → `🔄`
  - Sin datos → `—`
- Incluir la rama del CI entre parentesis

**Reglas del panel PLAN:**

- Fuente: `scripts/sprint-plan.json` (generado por `/planner sprint`)
- Si el archivo no existe, omitir este panel completamente
- Titulo del panel: `PLAN (fecha)` donde fecha viene del campo `fecha` del JSON
- Cada fila muestra: `#numero  #issue  slug  size  Stream X`
- Ordenar por `numero` ascendente
- Si no hay agentes en el plan: "Plan vacio"

**Reglas del panel TAREAS:**

- Prefijos: `●` = in_progress, `○` = pending, `✓` = completed
- Si una tarea esta bloqueada, mostrar `(◄#N)` al final con el ID que la bloquea
- Owner a la derecha
- Si no hay tareas: "Sin tareas registradas"

**Reglas del panel ALERTAS:**

- Tarea bloqueada por otra que esta `in_progress` → `⚠ #N bloqueada por #M (in_progress)`
- Tarea `in_progress` sin owner → `⚠ #N in_progress sin owner`
- Si no hay alertas → `✓ Sin alertas`

**Formato general:**

- Usa caracteres box-drawing Unicode: `┌ ┐ └ ┘ ├ ┤ ┬ ┴ │ ─`
- Envolver TODO el dashboard en un bloque de codigo (triple backtick) para renderizado monospace
- Truncar textos largos con `…` para que quepan en el ancho
- Siempre responde en espanol

### "sessions" -- Solo panel SESIONES + ACTIVIDAD RECIENTE

Ejecuta los pasos 1 y 2 (sesiones y actividad). Muestra SOLO los paneles SESIONES y ACTIVIDAD RECIENTE con el mismo formato box-drawing.

### "tasks" -- Solo tareas

Ejecuta `TaskList` y muestra SOLO el panel TAREAS + ALERTAS con el mismo formato box-drawing.

### "help" -- Ayuda

Muestra:

```
┌─ Monitor v3 ───────────────────────────────────────┐
│ Dashboard de Semaforos Multi-Sesion                 │
│                                                     │
│ Comandos disponibles:                               │
│   /monitor            Dashboard completo            │
│   /monitor sessions   Sesiones + actividad reciente │
│   /monitor tasks      Solo tareas + alertas         │
│   /monitor help       Esta ayuda                    │
│                                                     │
│ Iconos de estado:                                   │
│   ●  Activa (< 5 min)                              │
│   ◐  Idle (5-15 min)                               │
│   ○  Stale (> 15 min)                              │
│   ✗  Terminada (done)                               │
│   ▶  Sesion actual (ejecuta /monitor)               │
│                                                     │
│ Dashboard live: node .claude/dashboard.js           │
│ Datos: .claude/sessions/*.json                      │
│ Log:   .claude/activity-log.jsonl                   │
│ Hook:  activity-logger.js (PostToolUse)             │
│        stop-notify.js (Stop → marca "done")         │
└─────────────────────────────────────────────────────┘
```

## Notas importantes

- Cada sesion de Claude Code genera su propio archivo en `.claude/sessions/`
- Sub-agentes (type: "sub") NO se muestran en el dashboard — su actividad incrementa `sub_count` en la sesion padre
- La deteccion de liveness usa `last_activity_ts` del JSON de sesion (actualizado en cada PostToolUse por el hook)
- Sesiones marcadas como `status: "done"` por el hook Stop se muestran con `✗` (solo si < 1h de antiguedad)
- `last_tool` y `last_target` muestran la ultima herramienta usada y su objetivo
- `activity-log.jsonl` ahora incluye `session` (ID corto) en cada entrada
- Para monitoreo en tiempo real con auto-refresh: `node .claude/dashboard.js` en terminal externa
