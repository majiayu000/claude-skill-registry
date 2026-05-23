---
name: vendix-naming-conventions
description: Project naming conventions.
metadata:
  scope: [root]
  auto_invoke: "Writing Code (Naming)"
---
# Vendix Naming Conventions

> **CRITICAL SKILL - ALWAYS ACTIVE** - Las convenciones de nombres son la PRIORIDAD ABSOLUTA. CUALQUIER violación es un BUG CRÍTICO.

## 🚨 CRITICAL RULE - ZERO TOLERANCE

**YOU MUST ENFORCE THESE NAMING CONVENTIONS WITHOUT EXCEPTION:**

| Type | Convention | Example | ❌ WRONG |
|------|------------|---------|---------|
| **Variables** | `snake_case` | `user_name`, `order_total`, `is_active` | `userName`, `order-total` |
| **Functions** | `CamelCase` | `getUserData()`, `calculateOrderTotal()` | `get_user_data()`, `GetUserData()` |
| **Classes** | `PascalCase` | `UserService`, `OrderService` | `userService`, `user_service` |
| **Interfaces** | `PascalCase` | `UserProfile`, `ApiResponse` | `userProfile`, `api_response` |
| **Constants** | `SCREAMING_SNAKE_CASE` | `MAX_RETRIES`, `DEFAULT_TIMEOUT` | `maxRetries`, `default_timeout` |
| **Enums** | `PascalCase` | `UserRole`, `OrderStatus` | `userRole`, `order_status` |
| **Enum Values** | `snake_case` | `ADMIN`, `PENDING` | `Admin`, `Pending` |
| **Files** | `kebab-case` | `user.service.ts`, `order.controller.ts` | `userService.ts`, `Order.service.ts` |
| **Folders** | `kebab-case` | `user-management/`, `order-processing/` | `userManagement/`, `order_processing/` |

---
metadata:
  scope: [root]
  auto_invoke: "Any Code Change"

## 📋 Detailed Rules

### 1. Variables - `snake_case` (MANDATORY)

**✅ CORRECT:**
```typescript
const user_name = 'John';
const order_total = 99.99;
const is_active = true;
const client_info = { ip_address: '192.168.1.1' };
const product_list = [];
```

**❌ WRONG:**
```typescript
const userName = 'John';           // ❌ camelCase
const orderTotal = 99.99;          // ❌ camelCase
const isActive = true;             // ❌ camelCase
const clientInfo = { ... };        // ❌ camelCase
```

**WHY:** Readability, team collaboration, automated tools, type inference.

---

### 2. Functions - `CamelCase` (MANDATORY)

**✅ CORRECT:**
```typescript
function getUserData() { }
function calculateOrderTotal() { }
function validateStoreAccess(user_store_id?: number) { }
function generateSlug(text: string) { }
async function registerOwner(registerOwnerDto: RegisterOwnerDto) { }
```

**❌ WRONG:**
```typescript
function get_user_data() { }        // ❌ snake_case
function CalculateOrderTotal() { }  // ❌ PascalCase
function ValidateStoreAccess() { }  // ❌ PascalCase
```

---

### 3. Classes - `PascalCase` (MANDATORY)

**✅ CORRECT:**
```typescript
export class UserService { }
export class OrderService { }
export class RequestContextService { }
export class AuthGuard implements CanActivate { }
export class ProductListComponent { }
```

**❌ WRONG:**
```typescript
export class userService { }       // ❌ camelCase
export class order_service { }     // ❌ snake_case
export class AUTH_GUARD { }        // ❌ SCREAMING_SNAKE_CASE
```

---

### 4. Interfaces - `PascalCase` (MANDATORY)

**✅ CORRECT:**
```typescript
export interface UserProfile { }
export interface ApiResponse<T> { }
export interface AuthenticatedRequest extends Request { }
export interface CreateUserDto { }
```

**❌ WRONG:**
```typescript
export interface userProfile { }     // ❌ camelCase
export interface API_response { }    // ❌ snake_case
export interface ICreateUserDto { }  // ❌ No 'I' prefix needed
```

---

### 5. Constants - `SCREAMING_SNAKE_CASE` (MANDATORY)

**✅ CORRECT:**
```typescript
const MAX_RETRIES = 3;
const DEFAULT_TIMEOUT = 5000;
const API_BASE_URL = 'https://api.vendix.com';
const DB_CONNECTION_POOL_SIZE = 10;
```

**❌ WRONG:**
```typescript
const maxRetries = 3;           // ❌ camelCase
const default_timeout = 5000;   // ❌ snake_case
const apiBaseUrl = '...';       // ❌ camelCase
```

---

### 6. Enums - `PascalCase` (values: `snake_case`)

**✅ CORRECT:**
```typescript
enum UserRole {
  ADMIN = 'admin',
  USER = 'user',
  SUPER_ADMIN = 'super_admin',
}

enum OrderStatus {
  PENDING = 'pending',
  PROCESSING = 'processing',
  COMPLETED = 'completed',
}
```

**❌ WRONG:**
```typescript
enum userRole { }              // ❌ camelCase
enum user_role { }             // ❌ snake_case
enum UserRole {
  Admin = 'admin',             // ❌ PascalCase values
  SuperAdmin = 'super_admin',  // ❌ Inconsistent
}
```

---

### 7. Files - `kebab-case` (MANDATORY)

**✅ CORRECT:**
```
user.service.ts
order.controller.ts
auth.guard.ts
product-list.component.ts
request-context.service.ts
domain-resolver.middleware.ts
```

**❌ WRONG:**
```
userService.ts           // ❌ camelCase
order.service.ts         // ❌ Mixed case
Auth.Guard.ts            // ❌ PascalCase
productList.component.ts // ❌ camelCase
```

---

### 8. Folders - `kebab-case` (MANDATORY)

**✅ CORRECT:**
```
user-management/
order-processing/
auth-module/
product-list/
shared-components/
domain-resolver/
```

**❌ WRONG:**
```
userManagement/       // ❌ camelCase
order_processing/     // ❌ snake_case
AuthModule/           // ❌ PascalCase
sharedComponents/     // ❌ camelCase
```

---

## 🔍 Special Cases

### Database Tables - `snake_case`

```prisma
model users { }                    // ✅ CORRECTO
model product_variants { }         // ✅ CORRECTO
model sales_order_items { }        // ✅ CORRECTO
```

```prisma
model Users { }                    // ❌ WRONG
model ProductVariants { }          // ❌ WRONG
model salesOrderItems { }          // ❌ WRONG
```

### Database Columns - `snake_case`

```prisma
model users {
  id               Int       // ✅ CORRECTO
  organization_id  Int       // ✅ CORRECTO
  main_store_id    Int?      // ✅ CORRECTO
  created_at       DateTime  // ✅ CORRECTO
}
```

### API Endpoints - `kebab-case`

```typescript
// ✅ CORRECTO
@Controller('user-management')
@Get('user-profile')
@Post('create-order')

// ❌ WRONG
@Controller('userManagement')  // ❌ camelCase
@Get('userProfile')            // ❌ camelCase
```

### Component Selectors - `kebab-case` with `app-` prefix

```typescript
// ✅ CORRECTO
@Component({
  selector: 'app-user-profile',
  selector: 'app-product-list',
  selector: 'app-order-summary',
})

// ❌ WRONG
selector: 'userProfile'         // ❌ camelCase
selector: 'appUserProfile'      // ❌ camelCase without hyphen
selector: 'user-profile'        // ❌ Missing app- prefix
```

---

## 🎯 Quick Checklist

Before committing code, verify:

- [ ] All variables use `snake_case`
- [ ] All functions use `CamelCase`
- [ ] All classes use `PascalCase`
- [ ] All interfaces use `PascalCase`
- [ ] All constants use `SCREAMING_SNAKE_CASE`
- [ ] All files use `kebab-case`
- [ ] All folders use `kebab-case`
- [ ] All enum values use `snake_case`
- [ ] All DB tables use `snake_case`
- [ ] All DB columns use `snake_case`
- [ ] All component selectors use `app-kebab-case`

---

## 🔴 YOUR RESPONSIBILITY

**YOU MUST:**
1. ✅ **Double-check variable names** BEFORE writing code
2. ✅ **Immediately fix** ANY naming violation you encounter
3. ✅ **Flag violations as CRITICAL bugs**
4. ✅ **Reinforce conventions** in every interaction
5. ✅ **NEVER compromise** naming conventions for ANY reason

**TREAT NAMING VIOLATIONS AS CRITICAL BUGS THAT REQUIRE IMMEDIATE ATTENTION**

---

## Related Skills

- `vendix-development-rules` - General development rules
- `buildcheck-dev` - Build verification workflow
- `vendix-backend-domain` - Backend naming patterns
- `vendix-frontend-component` - Frontend component patterns
