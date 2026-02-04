---
name: laravel-auth
description: Use when implementing user authentication, API tokens, social login, or authorization. Covers Sanctum, Passport, Socialite, Fortify, policies, and gates for Laravel 12.
versions:
  laravel: "12.x"
  sanctum: "4.0"
  php: "8.4"
user-invocable: true
references: references/authentication.md, references/authorization.md, references/sanctum.md, references/passport.md, references/fortify.md, references/socialite.md, references/starter-kits.md, references/verification.md, references/passwords.md, references/session.md, references/csrf.md, references/encryption.md, references/hashing.md, references/templates/LoginController.php.md, references/templates/GatesAndPolicies.php.md, references/templates/PostPolicy.php.md, references/templates/sanctum-setup.md, references/templates/PassportSetup.php.md, references/templates/FortifySetup.php.md, references/templates/SocialiteController.php.md, references/templates/PasswordResetController.php.md
related-skills: laravel-api, laravel-permission, fusecore
---

# Laravel Authentication & Authorization

## Agent Workflow (MANDATORY)

Before ANY implementation, launch in parallel:

1. **fuse-ai-pilot:explore-codebase** - Check existing auth setup, guards, policies
2. **fuse-ai-pilot:research-expert** - Verify latest Laravel 12 auth docs via Context7
3. **mcp__context7__query-docs** - Query specific patterns (Sanctum, Passport, etc.)

After implementation, run **fuse-ai-pilot:sniper** for validation.

---

## Overview

Laravel provides a complete authentication and authorization ecosystem. Choose based on your needs:

| Package | Best For | Complexity |
|---------|----------|------------|
| **Starter Kits** | New projects, quick setup | Low |
| **Sanctum** | API tokens, SPA auth | Low |
| **Fortify** | Custom UI, headless backend | Medium |
| **Passport** | OAuth2 server, third-party access | High |
| **Socialite** | Social login (Google, GitHub) | Low |

---

## Critical Rules

1. **Use policies for model authorization** - Not inline `if` checks
2. **Always hash passwords** - `Hash::make()` or `'hashed'` cast
3. **Regenerate session after login** - Prevents fixation attacks
4. **Use HTTPS in production** - Required for secure cookies
5. **Define token abilities** - Principle of least privilege

---

## Architecture

```
app/
├── Http/
│   ├── Controllers/
│   │   └── Auth/              ← Auth controllers (if manual)
│   └── Middleware/
│       └── Authenticate.php   ← Redirects unauthenticated
├── Models/
│   └── User.php               ← HasApiTokens trait (Sanctum)
├── Policies/                  ← Authorization policies
│   └── PostPolicy.php
├── Providers/
│   └── AppServiceProvider.php ← Gate definitions
└── Actions/
    └── Fortify/               ← Fortify actions (if used)
        ├── CreateNewUser.php
        └── ResetUserPassword.php

config/
├── auth.php                   ← Guards & providers
├── sanctum.php                ← API token config
└── fortify.php                ← Fortify features
```

---

## FuseCore Integration

When working in a **FuseCore project**, authentication follows the modular structure:

```
FuseCore/
├── Core/                      # Infrastructure (priority 0)
│   └── App/Contracts/
│       └── AuthServiceInterface.php  ← Auth contract
│
├── User/                      # Auth module (existing)
│   ├── App/
│   │   ├── Models/User.php    ← HasApiTokens trait
│   │   ├── Http/
│   │   │   ├── Controllers/
│   │   │   │   ├── AuthController.php
│   │   │   │   └── TokenController.php
│   │   │   ├── Requests/
│   │   │   │   ├── LoginRequest.php
│   │   │   │   └── RegisterRequest.php
│   │   │   └── Resources/UserResource.php
│   │   ├── Policies/UserPolicy.php
│   │   └── Services/AuthService.php
│   ├── Config/
│   │   └── sanctum.php        ← Sanctum config (module-level)
│   ├── Database/Migrations/
│   ├── Routes/api.php         ← Auth routes
│   └── module.json            # dependencies: []
│
└── {YourModule}/              # Depends on User module
    ├── App/Policies/          ← Module-specific policies
    └── module.json            # dependencies: ["User"]
```

### FuseCore Auth Checklist

- [ ] Auth code in `/FuseCore/User/` module
- [ ] Policies in module's `/App/Policies/`
- [ ] Auth routes in `/FuseCore/User/Routes/api.php`
- [ ] Sanctum config in `/FuseCore/User/Config/sanctum.php`
- [ ] Declare `"User"` dependency in other modules' `module.json`
- [ ] Use `auth:sanctum` middleware in module routes

### Cross-Module Authorization

```php
// In FuseCore/{Module}/Routes/api.php
Route::middleware(['api', 'auth:sanctum'])->group(function () {
    Route::apiResource('posts', PostController::class);
});

// In FuseCore/{Module}/App/Http/Controllers/PostController.php
public function update(UpdatePostRequest $request, Post $post)
{
    $this->authorize('update', $post);  // Uses PostPolicy
    // ...
}
```

→ See [fusecore skill](../fusecore/SKILL.md) for complete module patterns.

---

## Decision Guide

### Authentication Method

```
Need auth scaffolding? → Starter Kit
├── Yes → Use React/Vue/Livewire starter kit
└── No → Building custom frontend?
    ├── Yes → Use Fortify (headless)
    └── No → API only?
        ├── Yes → Sanctum (tokens)
        └── No → Session-based
```

### Token Type

```
Third-party apps need access? → Passport (OAuth2)
├── No → Mobile app?
│   ├── Yes → Sanctum API tokens
│   └── No → SPA on same domain?
│       ├── Yes → Sanctum SPA auth (cookies)
│       └── No → Sanctum API tokens
```

---

## Key Concepts

| Concept | Description | Reference |
|---------|-------------|-----------|
| **Guards** | Define HOW users authenticate (session, token) | [authentication.md](references/authentication.md) |
| **Providers** | Define WHERE users are retrieved from (database) | [authentication.md](references/authentication.md) |
| **Gates** | Closure-based authorization for simple checks | [authorization.md](references/authorization.md) |
| **Policies** | Class-based authorization tied to models | [authorization.md](references/authorization.md) |
| **Abilities** | Token permissions (Sanctum/Passport scopes) | [sanctum.md](references/sanctum.md) |

---

## Reference Guide

### Concepts (WHY & Architecture)

| Topic | Reference | When to Consult |
|-------|-----------|-----------------|
| **Authentication** | [authentication.md](references/authentication.md) | Guards, providers, login flow |
| **Authorization** | [authorization.md](references/authorization.md) | Gates vs policies, access control |
| **Sanctum** | [sanctum.md](references/sanctum.md) | API tokens, SPA authentication |
| **Passport** | [passport.md](references/passport.md) | OAuth2 server, third-party access |
| **Fortify** | [fortify.md](references/fortify.md) | Headless auth, 2FA |
| **Socialite** | [socialite.md](references/socialite.md) | Social login providers |
| **Starter Kits** | [starter-kits.md](references/starter-kits.md) | Auth scaffolding |
| **Email Verification** | [verification.md](references/verification.md) | MustVerifyEmail, verified middleware |
| **Password Reset** | [passwords.md](references/passwords.md) | Forgot password flow |
| **Session** | [session.md](references/session.md) | Session drivers, flash data |
| **CSRF** | [csrf.md](references/csrf.md) | Form protection, AJAX tokens |
| **Encryption** | [encryption.md](references/encryption.md) | Data encryption (not passwords) |
| **Hashing** | [hashing.md](references/hashing.md) | Password hashing |

### Templates (Complete Code)

| Template | When to Use |
|----------|-------------|
| [LoginController.php.md](references/templates/LoginController.php.md) | Manual authentication controllers |
| [GatesAndPolicies.php.md](references/templates/GatesAndPolicies.php.md) | Gates and policy examples |
| [PostPolicy.php.md](references/templates/PostPolicy.php.md) | Complete policy class with before filter |
| [sanctum-setup.md](references/templates/sanctum-setup.md) | Sanctum configuration + testing |
| [PassportSetup.php.md](references/templates/PassportSetup.php.md) | OAuth2 server setup |
| [FortifySetup.php.md](references/templates/FortifySetup.php.md) | Fortify configuration + 2FA |
| [SocialiteController.php.md](references/templates/SocialiteController.php.md) | Social login + testing |
| [PasswordResetController.php.md](references/templates/PasswordResetController.php.md) | Password reset flow |

---

## Best Practices

### DO
- Use starter kits for new projects
- Define policies for all models
- Set token expiration
- Rate limit login attempts
- Use `verified` middleware for sensitive actions
- Prune expired tokens regularly

### DON'T
- Store plain text passwords
- Skip session regeneration on login
- Use Passport when Sanctum suffices
- Forget to prune expired tokens
- Ignore HTTPS in production
- Put authorization logic in controllers
