---
name: coding-standard-java
description: Enforce Java coding standards including camelCase variables, PascalCase classes, and PascalCase filenames matching class names.
---

# Java Coding Standards

When reviewing or generating Java code, follow these rules:

## File Naming
- **Source files:** PascalCase matching the public class name (e.g., `UserService.java`)
- **One public class per file:** File name must match the public class name exactly
- **Test files:** Class name with `Test` suffix (e.g., `UserServiceTest.java`)
- **Interface files:** PascalCase (e.g., `Comparable.java`, `UserRepository.java`)

## Package Naming
- **Packages:** All lowercase, dot-separated (e.g., `com.example.service`, `org.project.utils`)
- **No underscores or hyphens** in package names
- Follow reverse domain name convention

## Variable Naming
- **Local variables:** camelCase (e.g., `userName`, `isActive`, `totalCount`)
- **Instance variables:** camelCase (e.g., `userId`, `createdAt`)
- **Constants:** UPPER_SNAKE_CASE with `static final` (e.g., `MAX_RETRIES`, `DEFAULT_TIMEOUT`)
- **Boolean variables:** Prefix with `is`, `has`, `can`, `should` (e.g., `isEnabled`, `hasPermission`)

## Method Naming
- **Methods:** camelCase, verb or verb phrase (e.g., `calculateTotal()`, `getUserById()`)
- **Getters:** `get` prefix (e.g., `getName()`, `getId()`)
- **Setters:** `set` prefix (e.g., `setName()`, `setId()`)
- **Boolean getters:** `is` or `has` prefix (e.g., `isActive()`, `hasChildren()`)
- **Factory methods:** `create`, `of`, `from`, `valueOf` (e.g., `createInstance()`, `of()`)

## Class/Interface Naming
- **Classes:** PascalCase, noun or noun phrase (e.g., `UserService`, `OrderProcessor`)
- **Interfaces:** PascalCase, adjective or noun (e.g., `Comparable`, `UserRepository`)
- **Abstract classes:** PascalCase, optionally prefix with `Abstract` (e.g., `AbstractHandler`)
- **Exception classes:** PascalCase with `Exception` suffix (e.g., `InvalidInputException`)
- **Enums:** PascalCase for type, UPPER_SNAKE_CASE for values

## Generics
- **Type parameters:** Single uppercase letter (e.g., `T`, `E`, `K`, `V`)
- **Meaningful names:** When clarity needed (e.g., `<Key, Value>`)

## Organization
- Package statement first
- Import statements (java.*, javax.*, third-party, project imports)
- Class declaration with fields, constructors, methods
- Public methods before private methods
