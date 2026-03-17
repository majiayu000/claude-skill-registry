---
name: NestJS Configuration
description: Environment variables validation and ConfigModule setup.
metadata:
  labels: [nestjs, config, env]
  triggers:
    files: ['.env', 'app.module.ts', '**/config.ts']
    keywords: [ConfigModule, Joi, env]
---

# NestJS Configuration Standards

## **Priority: P1 (OPERATIONAL)**

Environment configuration and validation patterns for NestJS applications.

## Setup

1. **Library**: Use `@nestjs/config`.
2. **Initialization**: Import `ConfigModule.forRoot({ isGlobal: true })` in `AppModule`.

## Validation

- **Mandatory**: Validate environment variables at startup.
- **Tool**: Use `joi` or a custom validation class.
- **Effect**: The app **must crash** immediately if a required env var (e.g., `DB_URL`) is missing.

```typescript
// app.module.ts
ConfigModule.forRoot({
  validationSchema: Joi.object({
    NODE_ENV: Joi.string()
      .valid('development', 'production')
      .default('development'),
    PORT: Joi.number().default(3000),
    DATABASE_URL: Joi.string().required(),
  }),
});
```

## Usage

- **Injection**: Inject `ConfigService` to access values.
- **Typing**: Avoid magic strings. Use a type-safe getter helper or a dedicated configuration object/interface.
- **Secrets**: Never commit `.env` files. Add `.env*` to `.gitignore`.
