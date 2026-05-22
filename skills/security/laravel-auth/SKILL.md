---
name: laravel-auth
description: Implement authentication with Sanctum, Passport, Socialite, Fortify, policies, and gates. Use when setting up user authentication, API tokens, social login, or authorization.
user-invocable: false
---

# Laravel Authentication & Authorization

## Documentation

### Authentication
- [authentication.md](docs/authentication.md) - Authentication basics
- [sanctum.md](docs/sanctum.md) - API token authentication
- [passport.md](docs/passport.md) - OAuth2 server
- [fortify.md](docs/fortify.md) - Authentication backend
- [socialite.md](docs/socialite.md) - Social authentication
- [starter-kits.md](docs/starter-kits.md) - Breeze & Jetstream

### Authorization
- [authorization.md](docs/authorization.md) - Gates & Policies

### Security
- [verification.md](docs/verification.md) - Email verification
- [passwords.md](docs/passwords.md) - Password reset
- [encryption.md](docs/encryption.md) - Encryption
- [hashing.md](docs/hashing.md) - Hashing
- [csrf.md](docs/csrf.md) - CSRF protection
- [session.md](docs/session.md) - Session management

## Sanctum Setup

```php
use Laravel\Sanctum\HasApiTokens;

class User extends Authenticatable
{
    use HasApiTokens, HasFactory, Notifiable;
}
```

## Policy

```php
<?php

declare(strict_types=1);

namespace App\Policies;

final class PostPolicy
{
    public function update(User $user, Post $post): bool
    {
        return $user->id === $post->user_id;
    }

    public function delete(User $user, Post $post): bool
    {
        return $user->id === $post->user_id || $user->isAdmin();
    }
}
```

## Gates

```php
Gate::define('admin', fn (User $user) => $user->role === UserRole::Admin);

// Usage
if (Gate::allows('admin')) { }
```
