---
name: PIX Validation Expert
description: Validates PIX key requirements for MutuaPIX platform, ensuring email used for login matches PIX key email for payment processing
version: 1.0.0
allowed-tools: [Read, Grep, Bash]
---

# PIX Validation Expert Skill

## Overview

This skill ensures compliance with MutuaPIX's critical business rule: **the user's login email MUST match their PIX key email** for payment processing to work correctly.

## Critical Business Rule

**⚠️ EMAIL MATCHING REQUIREMENT:**
- User's login email (`users.email`) MUST be identical to PIX key email
- PIX key type must be `email`
- This is enforced for payment redemptions and donations

**Why:** PIX payment system uses email as unique identifier. Mismatched emails cause payment failures and user confusion.

## Database Schema

### Users Table (`users`)

```sql
-- Relevant columns
email VARCHAR(255) NOT NULL UNIQUE  -- Login email
pix_key VARCHAR(255) NULLABLE       -- PIX key value
pix_key_type ENUM('cpf', 'cnpj', 'email', 'phone', 'random') NULLABLE
```

**Location:** `backend/database/migrations/2024_04_14_000001_add_pix_fields_to_users_table.php`

## Validation Logic

### Backend Middleware: `CheckPixKey`

**File:** `backend/app/Http/Middleware/CheckPixKey.php`

```php
public function handle(Request $request, Closure $next)
{
    $user = $request->user();

    if (!$user->pix_key || !$user->pix_key_type) {
        return response()->json([
            'success' => false,
            'message' => 'É necessário cadastrar uma chave Pix antes de realizar resgates.',
        ], 422);
    }

    return $next($request);
}
```

**⚠️ MISSING VALIDATION:** Current middleware only checks if PIX key exists, but **does NOT validate email match!**

### Required Validation (Not Implemented Yet)

```php
public function handle(Request $request, Closure $next)
{
    $user = $request->user();

    // 1. Check PIX key exists
    if (!$user->pix_key || !$user->pix_key_type) {
        return response()->json([
            'success' => false,
            'message' => 'É necessário cadastrar uma chave Pix antes de realizar resgates.',
        ], 422);
    }

    // 2. NEW: Validate email match if PIX key type is email
    if ($user->pix_key_type === 'email' && $user->pix_key !== $user->email) {
        return response()->json([
            'success' => false,
            'message' => 'A chave PIX email deve ser igual ao email de login da conta.',
            'details' => [
                'login_email' => $user->email,
                'pix_key_email' => $user->pix_key,
            ]
        ], 422);
    }

    return $next($request);
}
```

## Routes Using PIX Validation

**File:** `backend/routes/api/mutuapix.php`

Routes that should enforce email matching:
- `/api/v1/redemptions` - Point redemptions (requires PIX)
- `/api/v1/pix/*` - PIX payment operations
- `/api/v1/donations` - Donation creation

## Frontend Validation

### Registration Flow

**Recommendation:** During user registration, automatically set PIX key to match email:

```typescript
// frontend/src/components/auth/RegisterForm.tsx
const handleRegister = async (data: RegisterFormData) => {
  const payload = {
    name: data.name,
    email: data.email,
    password: data.password,
    // AUTO-SET PIX key to match email
    pix_key: data.email,
    pix_key_type: 'email',
  };

  await authService.register(payload);
};
```

### Profile Settings

**Recommendation:** Show warning if user tries to change PIX email to different value:

```typescript
// frontend/src/components/user/PixSettings.tsx
const validatePixEmail = (pixEmail: string, loginEmail: string) => {
  if (pixEmail !== loginEmail) {
    return {
      valid: false,
      message: '⚠️ Atenção: Para garantir que você receba seus pagamentos, recomendamos usar o mesmo email da sua conta.',
      suggestion: `Use: ${loginEmail}`
    };
  }
  return { valid: true };
};
```

## Testing Scenarios

### Test Case 1: User Registration with Auto-PIX
```bash
# Expected: PIX key automatically set to email
POST /api/v1/register
{
  "name": "João Silva",
  "email": "joao@example.com",
  "password": "senha123"
}

# Backend should auto-create:
{
  "email": "joao@example.com",
  "pix_key": "joao@example.com",
  "pix_key_type": "email"
}
```

### Test Case 2: Mismatched PIX Email
```bash
# Expected: Validation error
User: {
  "email": "joao@example.com",
  "pix_key": "joao.silva@gmail.com",
  "pix_key_type": "email"
}

POST /api/v1/redemptions
# Should return 422 with message about email mismatch
```

### Test Case 3: CPF PIX Key (No Validation Needed)
```bash
# Expected: Success (CPF doesn't need email matching)
User: {
  "email": "joao@example.com",
  "pix_key": "123.456.789-00",
  "pix_key_type": "cpf"
}

POST /api/v1/redemptions
# Should proceed normally
```

## Implementation Checklist

When working with PIX validation:

- [ ] Check if user has PIX key configured
- [ ] Validate PIX key type is one of: cpf, cnpj, email, phone, random
- [ ] If PIX key type is `email`, verify it matches `users.email`
- [ ] Show clear error messages when validation fails
- [ ] Auto-populate PIX key with email during registration
- [ ] Warn users in profile settings if changing to different email

## Related Files

**Backend:**
- `app/Http/Middleware/CheckPixKey.php` - PIX validation middleware
- `app/Models/User.php` - User model with PIX fields
- `app/Services/PixPaymentService.php` - PIX payment processing
- `database/migrations/2024_04_14_000001_add_pix_fields_to_users_table.php`

**Frontend:**
- `src/services/pix-help.ts` - PIX help service
- `src/hooks/usePixHelp.ts` - PIX help hook
- `src/stores/helpPixStore.ts` - PIX state management

## Common Errors

**Error:** "Payment failed - email mismatch"
- **Cause:** User's login email differs from PIX key email
- **Fix:** Update PIX key to match login email or vice versa

**Error:** "É necessário cadastrar uma chave Pix"
- **Cause:** User hasn't configured PIX key
- **Fix:** Guide user to profile settings to add PIX key

## Best Practices

1. **Auto-populate:** Set PIX key = email during registration
2. **Validate early:** Check email match before payment processing starts
3. **Clear messaging:** Tell user exactly what email should be used
4. **Allow override:** Let user use CPF/phone if they prefer (no matching needed)
5. **Audit trail:** Log when PIX keys are changed

## Version History

- **1.0.0** (2025-10-16): Initial skill creation
  - Documented email matching requirement
  - Identified missing validation in middleware
  - Provided implementation examples
