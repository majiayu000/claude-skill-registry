---
name: coding-standard-cpp
description: Enforce C++ coding standards including camelCase or snake_case variables, PascalCase classes, and consistent file naming.
---

# C++ Coding Standards

When reviewing or generating C++ code, follow these rules:

## File Naming
- **Source files:** snake_case or PascalCase with `.cpp` extension (e.g., `user_service.cpp` or `UserService.cpp`)
- **Header files:** Same base name with `.h`, `.hpp`, or `.hxx` extension
- **Template files:** `.tpp` or `.inl` for template implementations
- **Be consistent** within a project

## Header Guards / Pragma
- **Prefer `#pragma once`** for modern compilers
- **Or use traditional guards:** UPPER_SNAKE_CASE with `_HPP` suffix
```cpp
#pragma once
// or
#ifndef USER_SERVICE_HPP
#define USER_SERVICE_HPP
#endif
```

## Namespace Naming
- **Namespaces:** all_lowercase or snake_case (e.g., `myproject`, `data_processing`)
- **Nested namespaces:** Use C++17 syntax when possible (e.g., `namespace project::utils {}`)
- **Avoid `using namespace` in headers**

## Variable Naming
- **Local variables:** snake_case or camelCase (e.g., `user_count` or `userCount`)
- **Member variables:** Prefix with `m_` or suffix with `_` (e.g., `m_data` or `data_`)
- **Static members:** Prefix with `s_` (e.g., `s_instance`)
- **Constants:** UPPER_SNAKE_CASE or kPascalCase (e.g., `MAX_SIZE` or `kMaxSize`)
- **Global variables:** Prefix with `g_` (e.g., `g_config`)

## Function/Method Naming
- **Free functions:** snake_case or camelCase (e.g., `calculate_total()` or `calculateTotal()`)
- **Member functions:** camelCase or PascalCase (e.g., `getUserId()` or `GetUserId()`)
- **Getters/Setters:** `get`/`set` prefix or just property name (e.g., `getName()` or `name()`)
- **Factory functions:** `Create`, `Make`, or `Build` prefix (e.g., `CreateUser()`)

## Class/Type Naming
- **Classes:** PascalCase (e.g., `UserService`, `DataProcessor`)
- **Structs:** PascalCase (e.g., `Point`, `Rectangle`)
- **Interfaces:** PascalCase with `I` prefix optional (e.g., `ISerializable` or `Serializable`)
- **Template parameters:** Single letter or PascalCase (e.g., `T`, `Container`, `KeyType`)
- **Enums:** PascalCase for type, UPPER_SNAKE_CASE or PascalCase for values
- **Type aliases:** PascalCase (e.g., `using StringList = std::vector<std::string>;`)

## Smart Pointers
- Use `std::unique_ptr` for single ownership
- Use `std::shared_ptr` for shared ownership
- Avoid raw `new`/`delete`

## Organization
- Include guards / pragma once
- System includes (alphabetical)
- Project includes (alphabetical)
- Forward declarations
- Namespace opening
- Class declarations
- Inline/template implementations
