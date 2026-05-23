---
name: create-utility-service
description: Create a utility service for cross-cutting concerns. Use when creating services for authentication, authorization, email, notifications, or other shared functionality that doesn't directly map to a domain entity.
---

# Create Utility Service

Creates a service for cross-cutting concerns or specialized functionality. Unlike resource services, utility services don't extend `BaseService` and typically don't inject repositories.

## Quick Reference

**Location**: `src/services/{service-name}.service.ts`
**Naming**: Descriptive, kebab-case (e.g., `authentication.service.ts`, `email.service.ts`)

## When to Use

Use this skill when creating services that:

- Call **external APIs** (auth service, payment gateway, email provider)
- Provide **shared functionality** used by other services
- Handle **cross-cutting concerns** (authorization, validation, notifications)
- Don't directly map to a domain entity

**Examples**: `AuthenticationService`, `AuthorizationService`, `EmailService`, `NotificationService`

## Service Categories

### 1. External API Services

Services that communicate with external systems.

```typescript
import { env } from "@/env";
import { ServiceUnavailableError, UnauthenticatedError } from "@/errors";
import { responseSchema, type ResponseType } from "@/schemas/response.schema";

export class ExternalApiService {
  private readonly baseUrl: string;

  constructor() {
    this.baseUrl = env.EXTERNAL_SERVICE_URL;

    if (!this.baseUrl) {
      throw new ServiceUnavailableError(
        "External service is not properly configured.",
      );
    }
  }

  async fetchData(token: string): Promise<ResponseType> {
    try {
      const response = await fetch(`${this.baseUrl}/endpoint`, {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        this.handleHttpError(response.status);
      }

      const rawData = await response.json();
      return this.validateResponse(rawData);
    } catch (error) {
      this.handleError(error);
    }
  }

  private handleHttpError(status: number): never {
    if (status === 401 || status === 403) {
      throw new UnauthenticatedError("Invalid authentication token");
    }
    throw new ServiceUnavailableError(`External service error: ${status}`);
  }

  private validateResponse(data: unknown): ResponseType {
    const parsed = responseSchema.safeParse(data);
    if (!parsed.success) {
      console.error("Invalid response format:", parsed.error.format());
      throw new ServiceUnavailableError("Invalid response format");
    }
    return parsed.data;
  }

  private handleError(error: unknown): never {
    // Re-throw known domain errors
    if (
      error instanceof UnauthenticatedError ||
      error instanceof ServiceUnavailableError
    ) {
      throw error;
    }

    console.error("External service error:", error);
    throw new ServiceUnavailableError("External service unavailable");
  }
}
```

**Key patterns**:

- Read config from `@/env` (never `process.env` directly)
- Validate responses with Zod schemas
- Throw domain errors from `@/errors`
- Handle and wrap unknown errors

### 2. Authorization Services

Services that provide permission logic.

```typescript
import type { AuthenticatedUserContextType } from "@/schemas/user.schemas";
import type { {Entity}Type } from "@/schemas/{entity}.schema";

export class AuthorizationService {
  isAdmin(user: AuthenticatedUserContextType): boolean {
    return user.globalRole === "admin";
  }

  // --- {Entity} Permissions ---

  async canView{Entity}(
    user: AuthenticatedUserContextType,
    {entity}: {Entity}Type,
  ): Promise<boolean> {
    if (this.isAdmin(user)) return true;
    if ({entity}.createdBy === user.userId) return true;
    return false;
  }

  async canCreate{Entity}(user: AuthenticatedUserContextType): Promise<boolean> {
    if (this.isAdmin(user)) return true;
    if (user.globalRole === "user") return true;
    return false;
  }

  async canUpdate{Entity}(
    user: AuthenticatedUserContextType,
    {entity}: {Entity}Type,
  ): Promise<boolean> {
    if (this.isAdmin(user)) return true;
    if ({entity}.createdBy === user.userId) return true;
    return false;
  }

  async canDelete{Entity}(
    user: AuthenticatedUserContextType,
    {entity}: {Entity}Type,
  ): Promise<boolean> {
    if (this.isAdmin(user)) return true;
    if ({entity}.createdBy === user.userId) return true;
    return false;
  }

  // --- Event Permissions ---

  async canReceive{Entity}Event(
    user: AuthenticatedUserContextType,
    {entity}Data: { createdBy: string; [key: string]: unknown },
  ): Promise<boolean> {
    // Apply same rules as viewing
    if (this.isAdmin(user)) return true;
    if ({entity}Data.createdBy === user.userId) return true;
    return false;
  }
}
```

**Key patterns**:

- Methods are `async` for consistency (even if currently sync)
- Return `boolean` not throw errors (let caller decide)
- Admin check is a shared helper
- Group permissions by entity with comments

### 3. Notification/Communication Services

Services that send notifications, emails, or messages.

```typescript
import { env } from "@/env";
import { ServiceUnavailableError } from "@/errors";

export interface EmailOptions {
  to: string;
  subject: string;
  body: string;
  html?: boolean;
}

export class EmailService {
  private readonly apiKey: string;
  private readonly fromAddress: string;

  constructor() {
    this.apiKey = env.EMAIL_API_KEY;
    this.fromAddress = env.EMAIL_FROM_ADDRESS;

    if (!this.apiKey || !this.fromAddress) {
      throw new ServiceUnavailableError(
        "Email service is not properly configured.",
      );
    }
  }

  async send(options: EmailOptions): Promise<boolean> {
    try {
      // External API call implementation
      return true;
    } catch (error) {
      console.error("Email service error:", error);
      throw new ServiceUnavailableError("Email service unavailable");
    }
  }
}
```

## Patterns & Rules

### No BaseService Extension

Utility services are standalone classes - don't extend `BaseService`:

```typescript
// Correct
export class AuthenticationService {
  // ...
}

// Wrong - BaseService is for resource services
export class AuthenticationService extends BaseService {
  // ...
}
```

### No Repository Injection

Utility services don't directly access data:

```typescript
// Correct - calls external API or provides logic
export class AuthenticationService {
  async authenticate(token: string) {
    return fetch(`${this.authUrl}/auth/me`, ...);
  }
}

// Wrong - use resource service for data access
export class AuthenticationService {
  constructor(private userRepository: IUserRepository) {}
}
```

### Multiple Implementations (Provider Pattern)

When you need to support multiple providers (e.g., different email services, notification channels, or payment gateways), create an interface and provide multiple implementations:

```typescript
// Interface in src/services/email.service.ts
export interface IEmailService {
  send(options: EmailOptions): Promise<EmailResult>;
  sendTemplate(to: string, templateId: string, variables: Record<string, string>): Promise<EmailResult>;
}

// SendGrid implementation in src/services/sendgrid-email.service.ts
export class SendGridEmailService implements IEmailService {
  async send(options: EmailOptions): Promise<EmailResult> {
    // SendGrid-specific implementation
  }
  async sendTemplate(...): Promise<EmailResult> {
    // SendGrid-specific implementation
  }
}

// Mailgun implementation in src/services/mailgun-email.service.ts
export class MailgunEmailService implements IEmailService {
  async send(options: EmailOptions): Promise<EmailResult> {
    // Mailgun-specific implementation
  }
  async sendTemplate(...): Promise<EmailResult> {
    // Mailgun-specific implementation
  }
}
```

Then inject the interface in dependent services:

```typescript
export class NotificationService {
  constructor(private emailService: IEmailService) {}

  async notifyUser(userId: string, message: string) {
    await this.emailService.send({
      to: userEmail,
      subject: "Notification",
      body: message,
    });
  }
}

// Usage - choose provider based on config
const emailService =
  env.EMAIL_PROVIDER === "sendgrid"
    ? new SendGridEmailService()
    : new MailgunEmailService();

const notificationService = new NotificationService(emailService);
```

**When to use this pattern**:

- Multiple email providers (SendGrid, Mailgun, SES)
- Multiple notification channels (email, SMS, push)
- Multiple payment gateways (Stripe, PayPal)
- Multiple storage backends (S3, GCS, local)

### Error Handling

Use domain errors from `@/errors`:

```typescript
import {
  ServiceUnavailableError,
  UnauthenticatedError,
  UnauthorizedError,
} from "@/errors";

// Throw appropriate domain errors
if (!response.ok) {
  throw new ServiceUnavailableError("Service unavailable");
}

// Re-throw known errors, wrap unknown ones
if (error instanceof ServiceUnavailableError) {
  throw error;
}
throw new ServiceUnavailableError("Unknown error");
```

### Configuration

Always read from validated env:

```typescript
import { env } from "@/env";

// Correct
const apiUrl = env.API_URL;

// Wrong - bypasses validation
const apiUrl = process.env.API_URL;
```

### Response Validation

Always validate external data with Zod:

```typescript
const rawData = await response.json();
const parsed = schema.safeParse(rawData);

if (!parsed.success) {
  console.error("Invalid format:", parsed.error.format());
  throw new ServiceUnavailableError("Invalid response format");
}

return parsed.data;
```

## Complete Examples

See [REFERENCE.md](REFERENCE.md) for complete examples:

- `AuthenticationService` - External API integration
- `AuthorizationService` - Permission logic

## What NOT to Do

- Do NOT extend `BaseService` (that's for resource services)
- Do NOT inject repositories (use resource services for data access)
- Do NOT use `process.env` directly (use `@/env`)
- Do NOT return HTTP status codes (use domain errors)
- Do NOT swallow errors silently (log and re-throw)

## See Also

- `create-service` - Guide for choosing service type
- `create-resource-service` - CRUD services for domain entities
- `add-env-variable` - Adding environment variables for service configuration
