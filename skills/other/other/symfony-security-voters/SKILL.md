---
description: "Symfony security voters — role hierarchy, voter pattern, access control, authorization, permissions, IsGranted attribute. Triggers on: security, voter, role, authorization, access control, permission, IsGranted, role hierarchy, RBAC"
---

# Symfony Security & Voters

You are an expert in Symfony security with Voters pattern within hexagonal architecture.

## When to Activate

- User needs authorization on endpoints
- User asks about voters or role hierarchy
- User wants access control logic
- User mentions RBAC, permissions, or security

## Core Rule: Every Endpoint Has a ROLE

**No endpoint is publicly accessible without explicit `#[IsGranted]` or Voter check.**

```php
#[Route('/api/users', methods: ['GET'])]
#[IsGranted('ROLE_USER_LIST')]  // ALWAYS required
public function list(): JsonResponse { ... }
```

## Role Hierarchy

Define roles in `security.yaml`:

```yaml
security:
    role_hierarchy:
        ROLE_ADMIN: [ROLE_USER_CREATE, ROLE_USER_EDIT, ROLE_USER_DELETE, ROLE_USER_LIST, ROLE_USER_VIEW]
        ROLE_MANAGER: [ROLE_USER_LIST, ROLE_USER_VIEW, ROLE_ORDER_MANAGE]
        ROLE_USER: [ROLE_USER_VIEW]
```

### Naming Convention
- Module-scoped: `ROLE_{MODULE}_{ACTION}`
- Examples: `ROLE_USER_CREATE`, `ROLE_ORDER_VIEW`, `ROLE_REPORT_GENERATE`

## Simple Cases: Use `#[IsGranted]`

```php
#[IsGranted('ROLE_USER_CREATE')]
public function create(): JsonResponse { ... }
```

## Complex Cases: Use Voters

When authorization depends on the resource (e.g., "can this user edit THIS order?"):

```php
namespace App\Infrastructure\{Module}\Security;

use Symfony\Component\Security\Core\Authentication\Token\TokenInterface;
use Symfony\Component\Security\Core\Authorization\Voter\Voter;

final class {Entity}Voter extends Voter
{
    public const VIEW = 'VIEW';
    public const EDIT = 'EDIT';
    public const DELETE = 'DELETE';

    protected function supports(string $attribute, mixed $subject): bool
    {
        return in_array($attribute, [self::VIEW, self::EDIT, self::DELETE])
            && $subject instanceof {Entity};
    }

    protected function voteOnAttribute(string $attribute, mixed $subject, TokenInterface $token): bool
    {
        $user = $token->getUser();
        if (!$user instanceof UserInterface) {
            return false;
        }

        return match ($attribute) {
            self::VIEW => $this->canView($subject, $user),
            self::EDIT => $this->canEdit($subject, $user),
            self::DELETE => $this->canDelete($subject, $user),
            default => false,
        };
    }

    private function canView({Entity} $entity, UserInterface $user): bool
    {
        // Owner or admin can view
        return $entity->ownerId() === $user->getId()
            || in_array('ROLE_ADMIN', $user->getRoles());
    }

    private function canEdit({Entity} $entity, UserInterface $user): bool
    {
        return $entity->ownerId() === $user->getId();
    }

    private function canDelete({Entity} $entity, UserInterface $user): bool
    {
        return in_array('ROLE_ADMIN', $user->getRoles());
    }
}
```

### Using Voter in Controller
```php
#[Route('/{id}', methods: ['PUT'])]
public function update(string $id): JsonResponse
{
    $order = $this->getOrder($id);
    $this->denyAccessUnlessGranted('EDIT', $order);
    // ... proceed
}
```

## References

See `references/` for detailed guides:
- `voter-patterns.md` — Full voter examples and testing
- `role-hierarchy.md` — Role hierarchy design patterns
