---
name: vikunja
description: Manage tasks and projects on a self-hosted Vikunja instance (PERSONAL/WORK). Use when the user wants to create, view, complete, or manage tasks, check what's due or overdue, list projects, or get notifications. Always register user-requested tasks in Vikunja for tracking and follow-up.
---

# Vikunja Task Manager (PERSONAL / WORK)

Gestiona tareas y proyectos en una instancia self-hosted de Vikunja mediante REST API.

## Skill Files

| File | Description |
|------|-------------|
| **SKILL.md** (this file) | Command reference and API documentation |
| **REGISTER.md** | Initial setup and configuration |
| **HEARTBEAT.md** | Periodic routine to enforce task tracking |

**Install locally:**
```bash
mkdir -p ~/.nimworker/skills
curl -s https://hiveagilectl.sh/skill.md > ~/.nimworker/skills/SKILL.md
curl -s https://hiveagilectl.sh/register.md > ~/.nimworker/skills/REGISTER.md
curl -s https://hiveagilectl.sh/heartbeat.md > ~/.nimworker/skills/HEARTBEAT.md
```

Or copy from local repo:
```bash
mkdir -p ~/.nimworker/skills
cp ~/work/taskworker/skill/SKILL.md ~/.nimworker/skills/
cp ~/work/taskworker/REGISTER.md ~/.nimworker/skills/
cp ~/work/taskworker/HEARTBEAT.md ~/.nimworker/skills/
```

---

## Complete Command Reference (28 commands)

| Category | Command | Description |
|----------|---------|-------------|
| **Tasks** | `tasks` | List tasks with filters (project, assignee, search, etc.) |
| | `search` | Search tasks across all projects by keyword |
| | `task` | Get detailed task information |
| | `create-task` | Create new task with description, priority, due date |
| | `edit-task` | Edit task title, description, priority, due date |
| | `delete-task` | Delete a task |
| | `complete` | Mark task as done |
| | `move-task` | Move task to different stage/bucket |
| | `assign-task` | Assign task to user (supports multiple assignees) |
| | `overdue` | Show overdue tasks |
| | `due` | Show tasks due soon (default 24h) |
| **Labels** | `labels` | List all labels |
| | `add-label` | Add label to task (auto-creates if needed) |
| | `remove-label` | Remove label from task |
| **Comments** | `comments` | List comments on a task |
| | `add-comment` | Add comment to task |
| **Projects** | `projects` | List all projects |
| | `create-project` | Create new project (auto-creates 5 Kanban stages) |
| | `buckets` / `stages` | List Kanban stages in project |
| | `create-bucket` / `create-stage` | Create new Kanban stage |
| **Teams** | `teams` | List all teams with members |
| | `create-team` | Create new team |
| | `share-project` | Share project with team |
| | `project-teams` | List teams in a project |
| **Users** | `users` | List users in a project |
| | `invite-user` | Invite user to project (read/write/admin) |
| **Other** | `notifications` | Show notifications |

**Key Features:**
- ✅ **Filter by assignee:** `--assign "username"` to see only tasks assigned to specific user
- ✅ **Auto-stage creation:** New projects get 5 default Kanban stages (Backlog, To Do, In Progress, Review, Done)
- ✅ **Multiple assignees:** Tasks can be assigned to multiple users
- ✅ **Auto-label creation:** Adding non-existent labels creates them automatically
- ✅ **Rich output:** Shows project names, stage names with emojis, assignees, due dates, priorities
- ✅ **Team collaboration:** Share projects with teams, manage user permissions

---

## Register First

Before using Vikunja, you must configure it. See **REGISTER.md** for full setup.

Quick start:
```bash
export VIKUNJA_URL="https://your-vikunja-instance.com"
export VIKUNJA_TOKEN="your-api-token"
export VIKUNJA_TZ="Europe/Rome"
export VIKUNJA_BOT_USERNAME="Jarvis"  # Tu username en Vikunja

# Bootstrap default projects
~/.nimworker/vikunja.py ensure-default-projects
```

**IMPORTANTE:** Configura `VIKUNJA_BOT_USERNAME` con tu nombre de usuario en Vikunja. Este username se usa para:
- Asignar tareas al bot
- Filtrar tareas del bot (`--assign "Jarvis"`)
- Ejecución autónoma de tareas (ver HEARTBEAT.md)

---

## Set Up Your Heartbeat 💓

**Critical:** Without the heartbeat, tasks won't be tracked consistently.

See **HEARTBEAT.md** for the full routine. The heartbeat ensures:
- ✅ Every task request is registered in Vikunja
- ✅ Overdue tasks are checked regularly
- ✅ No tasks are forgotten

---

## Principios de uso (obligatorios)

1) **Fuente de verdad:** si el usuario pide una "tarea", **se crea en Vikunja** (siempre).
2) **Sólo dos proyectos base:** **PERSONAL** y **WORK**.
3) **Seguimiento:** cualquier consulta de "qué queda / vencimientos / atrasos / cómo voy" se responde consultando Vikunja (`overdue`, `due`, `tasks`).
4) **Cierre:** cuando el usuario diga "hecho / completado / listo", se completa la tarea correspondiente en Vikunja.

---

## Setup

Configura variables de entorno:

```bash
export VIKUNJA_URL="https://your-vikunja-instance.com"
export VIKUNJA_TOKEN="your-api-token"

# Timezone para filtros (recomendado)
export VIKUNJA_TZ="Europe/Rome"

# Proyectos base (siempre estos dos)
export VIKUNJA_PROJECT_PERSONAL="PERSONAL"
export VIKUNJA_PROJECT_WORK="WORK"

# IMPORTANTE: Nombre de usuario del bot en Vikunja (para asignación de tareas)
export VIKUNJA_BOT_USERNAME="Jarvis"  # Cambia esto por tu username en Vikunja
```

**Configuración del usuario/bot:**
1. **Token:** Vikunja → Settings → API Tokens → Create token
2. **Username:** El nombre de usuario que usas en Vikunja (ej: "Jarvis", "Aitor", "Bot")
   - Este username se usa para asignar tareas al bot
   - El bot ejecutará automáticamente tareas asignadas a este usuario
   - Configúralo en `VIKUNJA_BOT_USERNAME`

> Recomendación: ejecutar una vez `ensure-default-projects` para crear PERSONAL/WORK si faltan.

---

## Enrutado de tareas a PERSONAL / WORK (sin preguntar)

Si el usuario no especifica proyecto explícito, se asigna así:

* **WORK** si aparecen señales de trabajo: `cliente`, `reunión`, `entrega`, `deploy`, `factura`, `empresa`, `proyecto`, `ticket`, `incidencia`, `call`, `oferta`, `presupuesto`.
* **PERSONAL** si aparecen señales personales: `casa`, `compra`, `familia`, `salud`, `viaje`, `médico`, `gym`, `pago personal`.
* Si no está claro: **PERSONAL** por defecto.

> El usuario puede forzar: "en WORK …" / "en PERSONAL …".

---

## Metodología recomendada (ligera)

* **Daily (2 min):** `overdue` + `due 24h` para WORK y PERSONAL.
* **Weekly (10 min):** revisar lista por prioridad y limpiar/ajustar.

---

## Commands

> Base: `~/.nimworker/vikunja.py` (Python wrapper) o `~/.nimworker/scripts/vikunja.sh` (Bash script)

### Bootstrap: asegurar proyectos base

```bash
~/.nimworker/vikunja.py ensure-default-projects
```

### List tasks

```bash
~/.nimworker/vikunja.py tasks --count 10
~/.nimworker/vikunja.py tasks --project "WORK" --count 20
~/.nimworker/vikunja.py tasks --project "PERSONAL" --count 20
~/.nimworker/vikunja.py tasks --search "groceries"
~/.nimworker/vikunja.py tasks --sort priority --order desc
```

**Output includes:**
- ✅ Project name (WORK, PERSONAL)
- ✅ Stage/Bucket name (📋 Backlog, 📝 To Do, 🔄 In Progress, 👀 Review, ✅ Done)
- ✅ Assigned users (if any)
- ✅ Due date and priority

### Filter by assignee (NEW! ✨)

```bash
# Show only tasks assigned to specific user
~/.nimworker/vikunja.py tasks --assign "Aitor"
~/.nimworker/vikunja.py tasks --assign "Jarvis" --count 20

# Combine with project filter
~/.nimworker/vikunja.py tasks --project "WORK" --assign "Aitor"

# Combine with other filters
~/.nimworker/vikunja.py tasks --assign "Aitor" --sort priority --order desc
```

### Filtrado avanzado (Vikunja filters)

```bash
~/.nimworker/vikunja.py tasks --filter 'done = false && priority >= 3'
~/.nimworker/vikunja.py tasks --project "WORK" --filter 'priority >= 4'
```

### Overdue tasks

```bash
~/.nimworker/vikunja.py overdue
~/.nimworker/vikunja.py overdue --project "WORK"
~/.nimworker/vikunja.py overdue --project "PERSONAL"
```

### Tasks due soon (next N hours)

```bash
~/.nimworker/vikunja.py due --hours 24
~/.nimworker/vikunja.py due --hours 24 --project "WORK"
~/.nimworker/vikunja.py due --hours 48 --project "PERSONAL"
```

### Create a task

**Basic task:**
```bash
~/.nimworker/vikunja.py create-task --project "WORK" --title "Llamar a cliente X" --due "2026-02-01" --priority 4
~/.nimworker/vikunja.py create-task --project "PERSONAL" --title "Comprar leche" --due "2026-02-01" --priority 2
```

**Task with detailed description:**
```bash
~/.nimworker/vikunja.py create-task \
  --project "WORK" \
  --title "Implementar autenticación OAuth" \
  --description "Integrar OAuth 2.0 con Google y GitHub. Requisitos: tokens JWT, refresh tokens, manejo de errores. Ver documentación en /docs/auth.md" \
  --due "2026-02-15" \
  --priority 5 \
  --bucket "To Do"
```

**Task with multiline description:**
```bash
~/.nimworker/vikunja.py create-task \
  --project "PERSONAL" \
  --title "Planificar viaje a Barcelona" \
  --description "Tareas:
- Reservar vuelos (Vueling o Ryanair)
- Hotel cerca de Las Ramblas
- Entradas Sagrada Familia
- Restaurantes recomendados: El Xampanyet, Can Culleretes
Presupuesto: 800€" \
  --due "2026-03-01" \
  --priority 3
```

**Assign to a specific Kanban stage:**
```bash
~/.nimworker/vikunja.py create-task --project "WORK" --title "Fix bug #123" --bucket "In Progress" --priority 5
~/.nimworker/vikunja.py create-task --project "WORK" --title "New feature" --stage "To Do" --priority 3
```

**Parameters:**
* `--title`: Task title (required)
* `--project`: Project name (required)
* `--description`: Detailed description (optional, supports multiline)
* `--due`: Due date in **YYYY-MM-DD** format
* `--priority`: **1 (low)** to **5 (urgent)**
* `--bucket` / `--stage`: Kanban stage (partial match, e.g., "todo", "progress", "done")

### Complete a task

```bash
~/.nimworker/vikunja.py complete --id 123
```

### Get task details

```bash
~/.nimworker/vikunja.py task --id 123
```

### List projects

```bash
~/.nimworker/vikunja.py projects
```

### Create a project (extra)

> Nota: El flujo principal usa PERSONAL y WORK. Crear proyectos adicionales sólo si el usuario lo pide explícitamente.

```bash
~/.nimworker/vikunja.py create-project --title "New Project" --description "Optional description"
```

**Automatic Kanban stages:** When creating a project, 5 default stages are automatically created:
- 📋 **Backlog** - Ideas and future tasks
- 📝 **To Do** - Ready to start
- 🔄 **In Progress** - Currently working on
- 👀 **Review** - Waiting for review/approval
- ✅ **Done** - Completed tasks

To skip automatic stage creation, use `--no-stages`:
```bash
~/.nimworker/vikunja.py create-project --title "New Project" --no-stages
```

### Get notifications

```bash
~/.nimworker/vikunja.py notifications
```

### Assign tasks to users

```bash
# Assign task to a user
~/.nimworker/vikunja.py assign-task --id 123 --user "Aitor"
~/.nimworker/vikunja.py assign-task --id 456 --user "Jarvis"

# Note: Users must be in project teams or directly invited to the project
# Tasks can have multiple assignees
```

### Move tasks between stages

```bash
# Move task to different Kanban stage
~/.nimworker/vikunja.py move-task --id 123 --stage "In Progress"
~/.nimworker/vikunja.py move-task --id 456 --bucket "Done"
~/.nimworker/vikunja.py move-task --id 789 --stage "Review" --project "WORK"
```

### Edit tasks

```bash
# Edit task details
~/.nimworker/vikunja.py edit-task --id 123 --title "New title"
~/.nimworker/vikunja.py edit-task --id 123 --priority 5 --due "2026-03-01"
~/.nimworker/vikunja.py edit-task --id 123 --description "Updated description"
```

### Delete tasks

```bash
~/.nimworker/vikunja.py delete-task --id 123
```

### Labels

```bash
# List all labels
~/.nimworker/vikunja.py labels

# Add label to task (creates label if it doesn't exist)
~/.nimworker/vikunja.py add-label --id 123 --label "urgent"
~/.nimworker/vikunja.py add-label --id 123 --label "bug"

# Remove label from task
~/.nimworker/vikunja.py remove-label --id 123 --label "urgent"
```

### Comments

```bash
# List comments on a task
~/.nimworker/vikunja.py comments --id 123

# Add comment to task
~/.nimworker/vikunja.py add-comment --id 123 --comment "Working on this now"
~/.nimworker/vikunja.py add-comment --id 456 --comment "Blocked by task #123"
```

### Team Management

```bash
# List all teams
~/.nimworker/vikunja.py teams

# Create a new team
~/.nimworker/vikunja.py create-team --name "Development Team" --description "Core dev team"

# Share project with team
~/.nimworker/vikunja.py share-project --project "WORK" --team "Development Team" --rights write

# List teams in a project
~/.nimworker/vikunja.py project-teams --project "WORK"
```

### User Management

```bash
# List users in a project
~/.nimworker/vikunja.py users --project "WORK"

# Invite user to project
~/.nimworker/vikunja.py invite-user --project "WORK" --user "maria@example.com" --rights write
~/.nimworker/vikunja.py invite-user --project "PERSONAL" --user "john" --rights read
```

**Rights levels:**
- `read` - Can view tasks
- `write` - Can create and edit tasks
- `admin` - Full project administration

### Kanban Stages (Buckets)

```bash
# List stages in a project
~/.nimworker/vikunja.py buckets --project "WORK"
~/.nimworker/vikunja.py stages --project "PERSONAL"  # alias

# Create a new stage
~/.nimworker/vikunja.py create-bucket --project "WORK" --title "🔥 Urgent" --position 0
~/.nimworker/vikunja.py create-stage --project "WORK" --title "🧪 Testing"  # alias
```

### Search across all projects

```bash
# Search by keyword in title or description
~/.nimworker/vikunja.py search --query "bug"
~/.nimworker/vikunja.py search --query "cliente"
~/.nimworker/vikunja.py search --query "payment"
```

**Search output includes:**
- Project name
- Stage name
- Due date and priority
- Task ID

---

## Rutinas listas para copiar

### Daily (mañana)

```bash
# Check overdue and upcoming tasks
~/.nimworker/vikunja.py overdue --project "WORK"
~/.nimworker/vikunja.py due --hours 24 --project "WORK"
~/.nimworker/vikunja.py overdue --project "PERSONAL"
~/.nimworker/vikunja.py due --hours 24 --project "PERSONAL"

# Check your assigned tasks
~/.nimworker/vikunja.py tasks --assign "YourUsername" --count 10
```

### Weekly (revisión)

```bash
# Review all tasks by priority
~/.nimworker/vikunja.py tasks --project "WORK" --sort priority --order desc --count 50
~/.nimworker/vikunja.py tasks --project "PERSONAL" --sort priority --order desc --count 50

# Review team assignments
~/.nimworker/vikunja.py tasks --project "WORK" --assign "Aitor"
~/.nimworker/vikunja.py tasks --project "WORK" --assign "Jarvis"
```

---

## Due Date Monitoring (cron genérico)

Ejemplo simple (sin acoplar a bots):

```bash
# Cada día a las 09:00
0 9 * * * ~/work/taskworker/vikunja overdue && ~/work/taskworker/vikunja due --hours 24
```

Si querés notificaciones, integralo con tu sistema (Telegram, email, etc.) según tu stack.

---

## Notes

* Los nombres de proyecto en `--project` son case-insensitive.
* Filters siguen la sintaxis de filtros de Vikunja.
* Timezone para filtros se controla con `VIKUNJA_TZ` (por defecto recomendado: Europe/Rome).

---

## Examples

### Work Tasks

**Development task with details:**
```bash
~/work/taskworker/vikunja.py \
  --project "WORK" \
  --title "Implementar API de pagos" \
  --description "OBJETIVO: Integrar Stripe para pagos recurrentes

REQUISITOS:
- Webhook para eventos de pago
- Manejo de errores y reintentos
- Tests unitarios y de integración
- Documentación en Swagger

REFERENCIAS:
- Docs Stripe: https://stripe.com/docs/api
- Ticket Jira: PROJ-123

ESTIMACIÓN: 40 horas" \
  --due "2026-02-20" \
  --priority 5 \
  --bucket "To Do"
```

**Bug fix:**
```bash
~/work/taskworker/vikunja.py \
  --project "WORK" \
  --title "Fix: Login timeout en producción" \
  --description "PROBLEMA: Usuarios reportan timeout al hacer login después de 5 minutos

PASOS PARA REPRODUCIR:
1. Login en app
2. Esperar 5+ minutos sin actividad
3. Intentar hacer cualquier acción
4. Error: 401 Unauthorized

CAUSA POSIBLE: JWT expira pero refresh token no se usa correctamente

LOGS: /var/log/app/auth-errors.log
REPORTADO POR: 3 usuarios (tickets #456, #457, #458)" \
  --due "2026-02-05" \
  --priority 5 \
  --bucket "In Progress"
```

**Client communication:**
```bash
~/work/taskworker/vikunja.py \
  --project "WORK" \
  --title "Enviar propuesta a cliente Acme Corp" \
  --description "SOLICITUD: Cotización para desarrollo app móvil

ALCANCE:
- App móvil iOS/Android
- Backend API REST
- Panel admin web
- Integración con su ERP

ESTIMACIÓN: 3 meses, 2 devs full-time
PRESUPUESTO: 45.000€

CONTACTO: Juan Pérez (juan@acmecorp.com)
TEMPLATE: /templates/propuesta-desarrollo.docx" \
  --due "2026-02-10" \
  --priority 4 \
  --bucket "To Do"
```

### Personal Tasks

**Shopping list:**
```bash
~/work/taskworker/vikunja.py \
  --project "PERSONAL" \
  --title "Compra semanal supermercado" \
  --description "LISTA DE COMPRAS:

FRESCOS:
- Leche (2L)
- Pan integral
- Frutas: manzanas, plátanos, naranjas
- Verduras: lechuga, tomates, pepino

DESPENSA:
- Pasta (500g)
- Arroz (1kg)
- Aceite de oliva
- Conservas: atún, tomate

LIMPIEZA:
- Detergente lavadora
- Papel higiénico

PRESUPUESTO: ~60€
SUPERMERCADO: Mercadona o Carrefour" \
  --due "2026-02-02" \
  --priority 3 \
  --bucket "To Do"
```

**Travel planning:**
```bash
~/work/taskworker/vikunja.py \
  --project "PERSONAL" \
  --title "Organizar viaje a Japón (abril)" \
  --description "VIAJE: 15-30 abril (15 días)

PENDIENTE:
- Vuelos Madrid-Tokyo (Skyscanner)
- JR Pass (7 días, ~280€)
- Hoteles: Tokyo (5n), Kyoto (4n), Osaka (3n)
- Pocket WiFi o SIM card
- Seguro de viaje

LUGARES A VISITAR:
- Senso-ji, Fushimi Inari, Dotonbori, Nara

PRESUPUESTO: ~2.500€/persona
COMPAÑEROS: Ana y Carlos

GUÍAS: japan-guide.com, /r/JapanTravel" \
  --due "2026-03-01" \
  --priority 2 \
  --bucket "Backlog"
```

**Health appointment:**
```bash
~/work/taskworker/vikunja.py \
  --project "PERSONAL" \
  --title "Cita médico: revisión anual" \
  --description "CITA: 12 febrero, 10:30
LUGAR: Centro Médico Salud, C/ Mayor 45, 3º
TELÉFONO: 91-234-5678

LLEVAR:
- Tarjeta sanitaria
- Resultados análisis sangre
- Lista medicación actual

TEMAS A CONSULTAR:
- Dolor espalda recurrente
- Renovar receta medicación presión arterial
- Vacuna gripe

RECORDATORIO: Llegar 10 min antes" \
  --due "2026-02-12" \
  --priority 4 \
  --bucket "To Do"
```

---

## Next Steps

1. **Setup:** Read `REGISTER.md` for initial configuration
2. **Heartbeat:** Read `HEARTBEAT.md` to set up periodic checks
3. **Start using:** Create your first task and test the workflow

**Remember:** Vikunja is your source of truth. If a task isn't in Vikunja, it doesn't exist. 📋
