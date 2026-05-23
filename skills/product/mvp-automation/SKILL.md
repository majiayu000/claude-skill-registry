---
name: mvp-automation
description: |
  Orquesta el flujo completo de MVP automatizado: SPEC → Historias → Tareas → Skills.
  Genera skills especializadas para cada tarea para que los agentes paralelos
  tengan conocimiento contextual específico.
metadata:
  author: vicente-rivas
  version: "2.0"
  category: orchestration
---

# MVP Automation - Flujo Completo Automatizado

## Resumen

Este skill orquesta la creación automatizada de un MVP completo, generando no
solo la especificación, sino también:

1. **Historias de Usuario** desde el SPEC
2. **Tareas paralelas** desde cada historia
3. **Skills especializadas** para cada tarea

## Flujo Automatizado

```
┌─────────────────────────────────────────────────────────────────┐
│                    MVP AUTOMATION FLOW                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  /project:interview <nombre>                                    │
│           │                                                     │
│           ▼                                                     │
│     ┌─────────────┐                                             │
│     │   SPEC.md   │  ← Entrevista profunda                      │
│     └──────┬──────┘                                             │
│            │                                                    │
│            ▼ [Usuario confirma]                                 │
│                                                                 │
│  /mvp:auto-generate                                             │
│           │                                                     │
│           ├──────────────────────────────────────┐              │
│           ▼                                      ▼              │
│     ┌─────────────┐                       ┌─────────────┐       │
│     │  H001.md    │                       │  H002.md    │  ...  │
│     │  Historia 1 │                       │  Historia 2 │       │
│     └──────┬──────┘                       └──────┬──────┘       │
│            │                                     │              │
│            ▼                                     ▼              │
│     ┌─────────────┐                       ┌─────────────┐       │
│     │  T001.md    │                       │  T003.md    │       │
│     │  T002.md    │                       │  T004.md    │       │
│     └──────┬──────┘                       └──────┬──────┘       │
│            │                                     │              │
│            ▼                                     ▼              │
│     ┌─────────────┐                       ┌─────────────┐       │
│     │ SKILL-T001  │                       │ SKILL-T003  │       │
│     │ SKILL-T002  │                       │ SKILL-T004  │       │
│     └─────────────┘                       └─────────────┘       │
│                                                                 │
│            │ [Skills generadas]                                 │
│            ▼                                                    │
│                                                                 │
│  /swarm:launch N   ← Agentes con skills especializadas          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Comandos

### `/project:interview <nombre>`

Inicia entrevista profunda para generar SPEC.md (ya existente).

### `/mvp:auto-generate`

**Nuevo comando** que tras confirmar el SPEC:

1. Genera historias de usuario automáticamente
2. Divide cada historia en tareas paralelas
3. Crea una skill especializada para cada tarea
4. Prepara el entorno para `/swarm:launch`

### `/skill:generate <task-id>`

Genera una skill especializada para una tarea específica.

### `/skill:batch <story-id>`

Genera skills para todas las tareas de una historia.

## Estructura de Archivos Generados

```
.claude/
├── specs/
│   └── PROYECTO-SPEC.md
├── stories/
│   ├── H001-feature-name.md
│   ├── H002-another-feature.md
│   └── STORIES-INDEX.md
├── tasks/
│   ├── T001-task-name.md
│   ├── T002-task-name.md
│   └── TASKS-INDEX.md
└── skills/
    └── generated/
        └── PROYECTO/
            ├── T001-skill/
            │   └── SKILL.md
            ├── T002-skill/
            │   └── SKILL.md
            └── INDEX.md
```

## Generación de Skills

Cada skill generada incluye:

### 1. Conocimiento Contextual

- Resumen de la historia padre
- Criterios de aceptación específicos
- Dependencias con otras tareas

### 2. Patrones Recomendados

- Patrones de código específicos del stack
- Mejores prácticas para el tipo de tarea
- Ejemplos de implementación similares

### 3. Anti-patterns

- Errores comunes a evitar
- Trampas específicas del dominio

### 4. Checklist de Completitud

- Criterios verificables para "done"
- Tests requeridos
- Integración esperada

## Ejemplo de Skill Generada

````markdown
---
name: T001-supabase-auth
description: |
  Implementa autenticación con Supabase SSR para Next.js 14.
  Incluye middleware de protección de rutas y providers de contexto.
metadata:
  author: mvp-automation
  version: "1.0"
  category: auth
  story_id: H001
  task_id: T001
---

# T001: Configurar Autenticación Supabase

## Contexto

**Historia**: H001 - Sistema de Autenticación **Tarea**: Configurar cliente
Supabase con SSR

## Conocimiento Especializado

### Supabase SSR en Next.js 14

- Usar `@supabase/ssr` en lugar de `@supabase/auth-helpers-nextjs`
- Crear cliente separado para browser y server
- Middleware para refresh de tokens

### Patrones Recomendados

```typescript
// lib/supabase/server.ts
import { createServerClient } from "@supabase/ssr";
import { cookies } from "next/headers";

export async function createClient() {
  const cookieStore = await cookies();
  return createServerClient(url, key, {
    cookies: {
      getAll: () => cookieStore.getAll(),
      setAll: (cookiesToSet) => {
        cookiesToSet.forEach(({ name, value, options }) =>
          cookieStore.set(name, value, options),
        );
      },
    },
  });
}
```
````

## Anti-patterns

- ❌ No usar `createBrowserClient` en Server Components
- ❌ No almacenar tokens en localStorage
- ❌ No olvidar el middleware para refresh

## Checklist

- [ ] Cliente browser en `lib/supabase/client.ts`
- [ ] Cliente server en `lib/supabase/server.ts`
- [ ] Middleware en `middleware.ts`
- [ ] AuthProvider con contexto
- [ ] Rutas protegidas funcionando

````

## Integración con Agentes Paralelos

Cuando se lanza `/swarm:launch`:

1. Cada agente recibe su tarea asignada
2. El agente carga automáticamente la skill correspondiente
3. La skill proporciona contexto y guía específica
4. El agente ejecuta con conocimiento especializado

## Configuración del Worktree

```bash
# En cada worktree, el archivo .claude/PROMPT.md incluye:
# 1. La tarea específica
# 2. Referencia a la skill generada
# 3. Contexto de la historia

cat trees/T001/.claude/PROMPT.md
# ---
# Tarea: T001 - Configurar Autenticación Supabase
# Skill: .claude/skills/generated/PROYECTO/T001-skill/SKILL.md
# Historia: H001 - Sistema de Autenticación
# ---
# [Contenido de la tarea]
````

## Beneficios

1. **Agentes más inteligentes**: Cada agente tiene conocimiento específico
2. **Menos errores**: Anti-patterns documentados previenen problemas
3. **Consistencia**: Patrones estandarizados en todo el proyecto
4. **Trazabilidad**: Cada skill vinculada a su tarea e historia
5. **Reutilización**: Skills pueden servir para proyectos similares

## Próximos Pasos

Tras ejecutar `/mvp:auto-generate`:

1. Revisar skills generadas (ajustar si necesario)
2. Ejecutar `/swarm:launch N` con el número de agentes
3. Monitorear con `/swarm:status`
4. Integrar con `/swarm:integrate`
