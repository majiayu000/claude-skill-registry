---
name: coding-standard-javascript
description: Enforce JavaScript/ES6+ and TypeScript coding standards including camelCase variables, PascalCase classes, and kebab-case filenames.
---

# JavaScript/TypeScript Coding Standards

When reviewing or generating JavaScript/TypeScript code, follow these rules:

## File Naming
- **Source files:** Use kebab-case (e.g., `user-service.js`, `api-client.ts`)
- **Component files:** Use kebab-case (e.g., `user-profile.js`, `data-table.tsx`)
- **Test files:** Use `.test.js` or `.spec.js` suffix (e.g., `user-service.test.js`)
- **Type definition files:** Use `.d.ts` suffix (e.g., `api-types.d.ts`)

## Variable Naming
- **Variables:** camelCase (e.g., `userName`, `isActive`, `totalCount`)
- **Constants:** UPPER_SNAKE_CASE for true constants (e.g., `MAX_RETRIES`, `API_BASE_URL`)
- **Boolean variables:** Prefix with `is`, `has`, `can`, `should` (e.g., `isLoading`, `hasError`)

## Function Naming
- **Functions:** camelCase (e.g., `calculateTotal()`, `fetchUserData()`)
- **Async functions:** Consider prefixing with action verb (e.g., `loadUsers()`, `saveDocument()`)
- **Event handlers:** Prefix with `handle` or `on` (e.g., `handleClick`, `onSubmit`)
- **Factory functions:** Prefix with `create` (e.g., `createUser()`, `createConnection()`)

## Class/Constructor Naming
- **Classes:** PascalCase (e.g., `UserService`, `DataProcessor`, `ApiClient`)
- **Interfaces (TS):** PascalCase, optionally prefix with `I` (e.g., `IUserService` or `UserService`)
- **Type aliases (TS):** PascalCase (e.g., `UserResponse`, `ConfigOptions`)
- **Enums (TS):** PascalCase for enum name, UPPER_SNAKE_CASE for values

## Private Members
- **Private fields:** Prefix with underscore (e.g., `_privateData`, `_internalState`)
- **Private methods:** Prefix with underscore (e.g., `_validateInput()`, `_processData()`)

## Module Organization
- Group imports: external packages first, then internal modules
- Export public API at the bottom of the file
- One class/component per file when possible
