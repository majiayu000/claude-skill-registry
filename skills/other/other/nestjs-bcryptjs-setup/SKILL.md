---
name: nestjs-bcryptjs-setup
description: Install, repair, and verify bcryptjs hashing in NestJS with ConfigModule-based SALT_ROUNDS validation, a reusable hash/verify EncryptionService, and a global EncryptionModule export. Use when users ask to add or fix password hashing, credential verification, auth secret hashing, login compare flow, or reusable bcrypt utilities.
---

# NestJS bcryptjs Setup

Use this workflow to add reusable one-way secret hashing with bcryptjs.

## Prerequisites

- NestJS backend with `AppModule` and `src`
- Node.js 20+ for modern Nest projects
- `@nestjs/config` available so `SALT_ROUNDS` can be read from environment

## Preflight checks

1. Confirm target is a NestJS backend root containing `package.json`, `src/main.ts`, and `src/app.module.ts`.
2. Confirm package manager from lockfile:
   - `package-lock.json` -> use `npm`
   - `pnpm-lock.yaml` -> use `pnpm`
   - `yarn.lock` -> use `yarn`
3. If required files are missing, stop and report the exact missing path before editing.

## Install dependencies

If `@nestjs/config` is missing, install it first.

```bash
npm install @nestjs/config
```

Install bcrypt packages from project root:

```bash
npm install bcryptjs
npm install -D @types/bcryptjs
```

Equivalent commands may be used for `pnpm` or `yarn`, but keep dependency intent identical.

## Configure `SALT_ROUNDS`

Add `SALT_ROUNDS` to `.env`:

- Production: `10-12`
- Tests/local fast feedback: `4-8`

Example:

```env
SALT_ROUNDS=10
```

If not already present, wire global config in `AppModule`:

```ts
ConfigModule.forRoot({ isGlobal: true })
```

If `ConfigModule.forRoot({ isGlobal: true })` already exists, do not duplicate it.

## Add `EncryptionService`

Implement `EncryptionService` from [reference.md](reference.md) with these rules:

1. Inject `ConfigService`.
2. Parse and validate `SALT_ROUNDS` once in the constructor.
3. Expose `hash(plain: string): Promise<string>`.
4. Expose `verify(plain: string, hashed: string): Promise<boolean>`.
5. Use only one-way terms (`hash` and `verify`), not encrypt/decrypt names.
6. Throw clear startup errors when `SALT_ROUNDS` is missing or out of accepted range.

## Add `EncryptionModule`

Create a global module from [reference.md](reference.md) that:

- imports `ConfigModule`
- provides `EncryptionService`
- exports `EncryptionService`

Register `EncryptionModule` in `AppModule.imports`.

## Optional env helper

Use `addEncryptionEnvVariables` from [reference.md](reference.md) if the project generates `.env` or `.env.example` files programmatically.

## Suggested file layout

- `src/libs/encryption/encryption.service.ts`
- `src/libs/encryption/encryption.module.ts`
- `src/libs/encryption/encryption.utils.ts` (optional)
- `src/libs/encryption/index.ts`

## Verification

1. Run backend checks from project root:

```bash
npm run build
npm run test
```

2. Verify hashing flow:
   - `verify(plain, await hash(plain))` returns `true`.
   - `verify('wrong', await hash('correct'))` returns `false`.
3. Verify config guardrails:
   - App boots with valid `SALT_ROUNDS`.
   - Missing or invalid `SALT_ROUNDS` fails fast with a clear startup error.
4. If any check fails, report exact failing command or assertion and stop before claiming completion.

## Checklist

- [ ] Confirm NestJS project root and package manager
- [ ] Install `bcryptjs` and `@types/bcryptjs`
- [ ] Ensure `ConfigModule.forRoot({ isGlobal: true })` is configured
- [ ] Add `SALT_ROUNDS` to `.env`
- [ ] Add `EncryptionService` and `EncryptionModule` from [reference.md](reference.md)
- [ ] Import `EncryptionModule` in `AppModule`
- [ ] Run build and tests, then verify hash/compare flow end to end

## Additional resources

- Full code snippets: [reference.md](reference.md)
