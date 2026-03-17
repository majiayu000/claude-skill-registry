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

**🚨 CRITICAL:** Use Task tools for ANY operation involving multiple files, research, or complex analysis. NEVER attempt complex operations without proper task management.

---

## 📊 Decision Matrix: When to Use Task Tools

| Scenario | Files Affected | Use Task Tool? | Agent Type |
|----------|---------------|----------------|------------|
| Single file edit | 1 | ❌ No | N/A (Edit directly) |
| Rename across codebase | 5+ | ✅ **YES** | general-purpose |
| Find pattern in unknown locations | Unknown | ✅ **YES** | Explore |
| Understand architecture | Research | ✅ **YES** | Explore |
| Plan new feature | Design | ✅ **YES** | Plan |
| Debug complex issue | 3+ | ✅ **YES** | general-purpose |
| Add simple field to DTO | 1 | ❌ No | N/A |
| Refactor multi-file logic | 3+ | ✅ **YES** | general-purpose |
| Search how X works | Research | ✅ **YES** | Explore |

---

## 🤖 Agent Selection Guide

```
┌─────────────────────────────────────────────────────────────────┐
│                     TASK SELECTION FLOW                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Start Task                                                     │
│      │                                                          │
│      ▼                                                          │
│  ┌─────────────────┐                                           │
│  │ Need to explore  │──── YES ──→ Use Explore agent             │
│  │ or understand?  │                                           │
│  └────────┬────────┘                                           │
│           │ NO                                                  │
│           ▼                                                     │
│  ┌─────────────────┐                                           │
│  │ Planning needed │──── YES ──→ Use Plan agent                 │
│  │ for feature?    │                                           │
│  └────────┬────────┘                                           │
│           │ NO                                                  │
│           ▼                                                     │
│  ┌─────────────────┐                                           │
│  │ Affects 3+      │──── YES ──→ Use general-purpose agent     │
│  │ files?          │                                           │
│  └────────┬────────┘                                           │
│           │ NO                                                  │
│           ▼                                                     │
│     Use direct tools (Edit, Read, Grep, Glob, Bash)            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Explore Agent
**Use for:** Fast codebase exploration, finding files by patterns, understanding how things work
```
Examples:
• "Find all files related to user authentication"
• "Where are order payment methods handled?"
• "Show me the inventory adjustment flow"
• "How does multi-tenancy work in this codebase?"
```

### Plan Agent
**Use for:** Designing implementation strategies before coding
```
Examples:
• "Plan how to add product variant pricing"
• "Design the refund flow integration"
• "Plan the store settings restructure"
```

### General-Purpose Agent
**Use for:** Complex multi-step tasks requiring multiple tools
```
Examples:
• "Rename UserService to CustomerService across all files"
• "Add error handling to all inventory endpoints"
• "Refactor the cart calculation logic"
```

---

## ✅ ❌ Real Examples from Vendix

### ✅ CORRECT: Using Task Tool

```typescript
// ❌ DON'T DO THIS: Manual search across codebase
// Grep → Search "payment" → Grep → Search "stripe" → Read → Read...

// ✅ DO THIS: Use Explore agent
Task tool → Explore agent → "Find all payment processing files and explain the flow"
```

```typescript
// ❌ DON'T DO THIS: Manually finding all references
// Grep "UserService" → Edit → Edit → Edit... (10+ files)

// ✅ DO THIS: Use general-purpose agent
Task tool → general-purpose agent → "Rename UserService to CustomerService in all files"
```

```typescript
// ❌ DON'T DO THIS: Guessing architecture
// Read random files hoping to understand the pattern

// ✅ DO THIS: Use Explore agent
Task tool → Explore agent → "Explain how multi-tenant context is managed across domains"
```

### ❌ INCORRECT: Using Task Tool Unnecessarily

```typescript
// ❌ DON'T DO THIS: Overkill for simple tasks
Task tool → "Add one field to CreateUserDto"

// ✅ DO THIS: Direct Edit tool
Edit tool → Add field directly
```

```typescript
// ❌ DON'T DO THIS: Task for single command
Task tool → "Run docker compose restart"

// ✅ DO THIS: Direct Bash tool
Bash tool → docker compose restart
```

---

## 🎯 Quick Reference Table

| Need | Use | Pattern |
|------|-----|---------|
| Find where X is defined | Explore | "Find where {interface/class} is defined" |
| Understand flow | Explore | "Explain the {feature} flow from start to end" |
| Plan implementation | Plan | "Plan how to implement {feature} with {constraints}" |
| Multi-file refactor | general-purpose | "Refactor {pattern} across all {domain} files" |
| Find bug across files | general-purpose | "Find why {symptom} happens in {context}" |
| Single file change | Direct tools | Edit tool directly |
| Run command | Direct tools | Bash tool directly |
| Read specific file | Direct tools | Read tool directly |

---

## ⚠️ Common Mistakes to Avoid

| Mistake | Why It's Wrong | Correct Approach |
|---------|----------------|------------------|
| Using Grep to find all usages | Slow, error-prone, incomplete | `Task → Explore agent` |
| Manually editing 10+ files | Time-consuming, easy to miss one | `Task → general-purpose agent` |
| Reading random files to understand | Inefficient, misses context | `Task → Explore agent` |
| Starting coding without planning | Creates wrong patterns | `Task → Plan agent` first |

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
3. **NEVER skip build verification** (see `buildcheck-dev`)
4. **ALWAYS read existing code** before changing
5. **ALWAYS follow established patterns**

---

## Related Skills

- `vendix-naming-conventions` - ABSOLUTE PRIORITY for naming
- `buildcheck-dev` - MANDATORY build checks
- `vendix-backend-domain` - Backend domain patterns
- `vendix-frontend-component` - Frontend component patterns
