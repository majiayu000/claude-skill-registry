---
name: vendix-development-rules
description: General development rules.
metadata:
  scope: [root]
  auto_invoke: "General Development"
---
# Vendix Development Rules

> **CRITICAL SKILL - ALWAYS ACTIVE** - Estas reglas son MANDATORIAS para toda interacción con el código base.

## 🚨 MANDATORY REQUIREMENTS

### Rule 1: ALWAYS Use Task Tools

**YOU MUST USE Task tools for:**
- Complex, multi-step operations
- Codebase exploration and research
- Architectural decisions and planning
- Any task affecting multiple files

**NEVER attempt complex operations without proper task management.**

```bash
# ✅ CORRECTO: Usar Task tool para explorar
Task tool → Explore agent → "Find all payment-related files"

# ❌ INCORRECTO: Usar Grep/Glob directamente para tareas complejas
Grep tool → Search "payment" (para análisis complejo)
```

**When to use each agent:**
- **Explore agent**: Fast codebase exploration, finding files by patterns
- **Plan agent**: Design implementation strategies before coding
- **general-purpose agent**: Complex multi-step tasks requiring multiple tools
- **Bash**: Simple terminal operations only (git, npm, docker)

---
metadata:
  scope: [root]
  auto_invoke: "Complex Tasks"

## Rule 2: Consistency Over Preferences

**ALWAYS prioritize:**
1. **Established patterns** in the codebase
2. **Existing conventions** over personal preferences
3. **Code consistency** across the project

**NEVER:**
- Suggest "better" ways that differ from established patterns
- Introduce new conventions without justification
- Change working patterns for marginal improvements

**Principle**: If it works in the codebase, follow that pattern.

---

## Rule 3: Code Quality Standards

**YOU MUST MAINTAIN:**
- **Strong typing**: Use TypeScript interfaces, NEVER `any`
- **Modularity**: Keep code modular and reusable
- **Multi-tenancy**: Always consider tenant isolation
- **Error handling**: Implement proper error handling at all layers
- **Documentation**: Add comments only when logic isn't self-evident

**AVOID:**
- Over-engineering simple solutions
- Premature abstractions
- Adding features "just in case"
- Changing code that already works

---

## Rule 4: Technology Constraints

**BACKEND:**
- **NEVER suggest JavaScript** - Always TypeScript
- **NEVER bypass Prisma** - Always use generated clients
- **NEVER hardcode tenant IDs** - Use RequestContext (multi-tenant is automatic)

**FRONTEND:**
- **NEVER use promises for HTTP** - Always RxJS Observables
- **NEVER create isolated state** - Use global state when appropriate
- **NEVER hardcode branding** - Resolve from domain config
- **NEVER use alert()** - Use ToastService

**Note:** Backend uses global JWT authentication via `APP_GUARD`. Use `@Public()` decorator for public routes. See `vendix-backend-auth` for authentication patterns.

---

## Rule 5: Before Making Changes

**YOU MUST:**
1. **Read existing code** before suggesting changes
2. **Understand the pattern** before implementing
3. **Follow existing structures** unless explicitly requested to change
4. **Test builds** after any code change

**NEVER:**
- Propose changes without reading the file first
- Assume patterns without verification
- Skip build verification

---

## Rule 6: File Organization

**BACKEND DOMAINS:**
```
apps/backend/src/domains/{domain}/
├── {domain}.module.ts
├── {domain}.controller.ts
├── {domain}.service.ts
├── dto/
└── entities/
```

**FRONTEND MODULES:**
```
apps/frontend/src/app/private/modules/{module}/
├── {module}.component.ts
├── {module}.component.html
├── {module}.component.scss
├── components/
│   └── index.ts
├── services/
│   └── {module}.service.ts
└── interfaces/
    └── {module}.interface.ts
```

**ALL COMPONENTS:**
- **MUST be in folders** - Even if standalone, even if small
- **MUST have index.ts** - For clean exports
- **MUST follow naming** - kebab-case for folders, PascalCase for classes

---

## Rule 7: Verification Workflow

**BEFORE completing ANY task:**

1. ✅ Check Docker logs for ALL modified components
2. ✅ Verify ZERO errors exist
3. ✅ Use appropriate commands:
   - Backend: `docker logs --tail 40 vendix_backend`
   - Frontend: `docker logs --tail 40 vendix_frontend`
   - Database: `docker logs --tail 40 vendix_postgres`
4. ✅ Re-check after fixes
5. ✅ Only then mark task complete

**NO EXCEPTIONS** - A task is NEVER complete with build errors.

---

## 🎯 Quick Reference

| Task | Tool/Approach |
|------|---------------|
| Explore codebase | Task → Explore agent |
| Plan implementation | Task → Plan agent |
| Complex multi-step | Task → general-purpose agent |
| Simple commands | Bash tool directly |
| Find file by name | Glob tool |
| Search content | Grep tool |
| Read file | Read tool |

---

## 📋 Decision Tree

```
Start Task
    │
    ├─→ Is it complex/multi-step?
    │   └─→ YES: Use Task tool
    │   └─→ NO: Can I do it with one tool?
    │       └─→ YES: Use that tool
    │       └─→ NO: Use Task tool
    │
    ├─→ Does it involve code changes?
    │   └─→ YES: Read file first
    │   └─→ Follow existing patterns
    │   └─→ Verify build after
    │
    └─→ Is it a new feature/module?
        └─→ YES: Use Plan agent first
        └─→ Get user approval
        └─→ Then implement
```

---

## 🔴 CRITICAL REMINDERS

1. **NEVER skip Task tools** for complex operations
2. **NEVER compromise naming conventions** (see `vendix-naming-conventions`)
3. **NEVER skip build verification** (see `vendix-build-verification`)
4. **ALWAYS read existing code** before changing
5. **ALWAYS follow established patterns**

---

## Related Skills

- `vendix-naming-conventions` - ABSOLUTE PRIORITY for naming
- `vendix-build-verification` - MANDATORY build checks
- `vendix-backend-domain` - Backend domain patterns
- `vendix-frontend-component` - Frontend component patterns
