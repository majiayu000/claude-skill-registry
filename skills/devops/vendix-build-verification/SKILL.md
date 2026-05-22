---
name: vendix-build-verification
description: Build verification steps.
metadata:
  scope: [root]
  auto_invoke: "Verifying Build"
---
# Vendix Build Verification

> **CRITICAL SKILL - ALWAYS ACTIVE** - La verificación del build es la RESPONSABILIDAD MÁS CRÍTICA. Una tarea NUNCA está completa si hay errores de compilación.

## 🚨 THE MOST IMPORTANT RULE OF ALL

**BEFORE marking ANY task as complete, you are ABSOLUTELY REQUIRED TO:**

1. ✅ Check Docker logs for **ALL** modified components
2. ✅ Verify that **ZERO errors** exist in any component
3. ✅ Use appropriate Docker log commands
4. ✅ **DO NOT finalize** until ALL errors are completely resolved
5. ✅ Re-check logs **after** applying fixes
6. ✅ Verify **recursively** - check dependencies and related components

---
metadata:
  scope: [root]
  auto_invoke: "Verifying Build"

## 📋 Verification Workflow

### Step 1: Make Code Changes
Apply your changes to the codebase.

### Step 2: Check Docker Logs
Run the appropriate log commands based on what you modified:

```bash
# Backend changes
docker logs --tail 40 vendix_backend

# Frontend changes
docker logs --tail 40 vendix_frontend

# Database/Prisma changes
docker logs --tail 40 vendix_postgres

# Multiple components affected
docker logs --tail 40 vendix_backend
docker logs --tail 40 vendix_frontend
docker logs --tail 40 vendix_postgres
```

### Step 3: Analyze Results

**If NO errors:**
- ✅ Verify one more time
- ✅ Only then mark task complete

**If errors exist:**
- ❌ DO NOT mark task complete
- ⚠️ Fix the errors
- 🔄 Return to Step 2

### Step 4: Recursive Check
- Check not just the immediate component
- Check all dependencies
- Check all related components
- Verify the entire application builds successfully

---

## 🔍 Reading Docker Logs

### Backend Logs

```bash
docker logs --tail 40 vendix_backend
```

**Look for:**
- ❌ `ERROR` messages
- ❌ `TypeError` or `ReferenceError`
- ❌ Compilation errors
- ❌ Missing dependencies
- ❌ Type errors
- ✅ `Successfully compiled` (good)
- ✅ `Nest application successfully started` (good)

**Example of GOOD output:**
```
[Nest] INFO [NestFactory] Starting Nest application...
[Nest] INFO [InstanceLoader] modules dependencies initialized
[Nest] INFO [RouterExplorer] Mapping {/auth, POST} route
[Nest] INFO [NestApplication] Nest application successfully started
```

**Example of BAD output:**
```
[ERROR] TypeError: Cannot read property 'user_name' of undefined
[ERROR] src/domains/auth/auth.service.ts:45:20 - error TS2304
```

---

### Frontend Logs

```bash
docker logs --tail 40 vendix_frontend
```

**Look for:**
- ❌ `ERROR` messages
- ❌ `ERROR in` compilation errors
- ❌ Template parsing errors
- ❌ Module not found errors
- ❌ Type errors in `.ts` files
- ✅ `Compiled successfully` (good)
- ✅ `webpack: Compiled successfully` (good)

**Example of GOOD output:**
```
✓ Compiled successfully in 2345ms
webpack: Compiled successfully
```

**Example of BAD output:**
```
ERROR in src/app/shared/components/button/button.component.ts:12:5
TS2322: Type 'string' is not assignable to type 'ButtonVariant'
```

---

### Database Logs

```bash
docker logs --tail 40 vendix_postgres
```

**Look for:**
- ❌ `ERROR:` messages
- ❌ Connection refused
- ❌ Syntax errors in queries
- ✅ `database system is ready to accept connections` (good)

---

## 🎯 Common Build Errors and Fixes

### TypeScript Errors

**Error:**
```
TS2322: Type 'X' is not assignable to type 'Y'
```

**Fix:**
1. Check type definitions
2. Verify interface contracts
3. Ensure proper typing
4. Re-check logs after fix

---

### Module Not Found

**Error:**
```
Error: Cannot find module '@/shared/components/...'
```

**Fix:**
1. Verify import path
2. Check if file exists
3. Verify tsconfig paths
4. Re-check logs after fix

---

### Prisma Client Errors

**Error:**
```
Error: Prisma Client is not generated
```

**Fix:**
1. Run: `npx prisma generate`
2. Verify schema.prisma is valid
3. Re-check logs after fix

---

### Template Errors

**Error:**
```
NG2: Property 'user_name' does not exist on type 'Component'
```

**Fix:**
1. Check component TypeScript file
2. Verify property is defined
3. Check for proper decorators (@Input, signal)
4. Re-check logs after fix

---

## 📊 Verification Checklist

Before marking ANY task as complete:

- [ ] Code changes applied
- [ ] Docker logs checked for **ALL** affected components
- [ ] **ZERO errors** in logs
- [ ] Recursive verification complete
- [ ] Dependencies checked
- [ ] Related components checked
- [ ] Re-verified after any fixes
- [ ] Application builds successfully
- [ ] Application runs without errors

---

## 🔴 CRITICAL UNDERSTANDING

**A task is NEVER complete if there are:**
- ❌ Build errors
- ❌ Compilation errors
- ❌ Runtime errors
- ❌ Type errors
- ❌ Missing dependencies
- ❌ Template parsing errors

**You must:**
- ✅ ALWAYS verify build status recursively
- ✅ ALWAYS fix ALL issues before considering work done
- ✅ NEVER accept "it should work" - verify with logs
- ✅ ALWAYS re-check after applying fixes

**Partial completion is NOT ACCEPTABLE**

---

## 💻 Example Workflow

### Scenario: Creating a new Angular component

```bash
# 1. Create the component
ng generate component modules/user-management/user-list

# 2. Check logs IMMEDIATELY
docker logs --tail 40 vendix_frontend

# 3. If errors found:
#    - Fix them
#    - Re-check logs
#    - Repeat until ZERO errors

# 4. Only then mark task complete
```

---

## 🔧 Development vs Production

**DEVELOPMENT (Current Mode):**
- Use: `docker logs --tail 40 <container>`
- Watch mode enabled
- Hot-reload active
- Check logs after EVERY change

**PRODUCTION:**
- Use: `npm run build`
- Full compilation
- All optimizations
- Check build output

**CURRENT WORKFLOW:**
We're in development mode, so ALWAYS use Docker logs.

---

## 🎯 Quick Reference

| Component | Command |
|-----------|---------|
| Backend | `docker logs --tail 40 vendix_backend` |
| Frontend | `docker logs --tail 40 vendix_frontend` |
| Database | `docker logs --tail 40 vendix_postgres` |
| All | Run all three commands |

---

## 🔴 YOUR FINAL CHECKPOINT

**Remember: Code quality and consistency directly impact:**
- Project success
- Team productivity
- Long-term maintainability

**Build verification is your final checkpoint before delivery.**

---

## Related Skills

- `vendix-development-rules` - General development rules
- `vendix-naming-conventions` - Naming conventions (CRITICAL)
- `vendix-backend-domain` - Backend verification patterns
- `vendix-frontend-component` - Frontend verification patterns
