---
name: coding-standard-c
description: Enforce C coding standards including snake_case variables and functions, UPPER_SNAKE_CASE macros, and snake_case filenames.
---

# C Coding Standards

When reviewing or generating C code, follow these rules:

## File Naming
- **Source files:** snake_case with `.c` extension (e.g., `user_service.c`, `data_parser.c`)
- **Header files:** snake_case with `.h` extension (e.g., `user_service.h`, `data_parser.h`)
- **Keep names short** but descriptive (max ~20 characters)

## Header Guards
- **Format:** UPPER_SNAKE_CASE with `_H` suffix
- **Include path in guard:** (e.g., `PROJECT_MODULE_FILE_H`)
```c
#ifndef USER_SERVICE_H
#define USER_SERVICE_H
// content
#endif /* USER_SERVICE_H */
```

## Variable Naming
- **Local variables:** snake_case (e.g., `user_count`, `buffer_size`, `is_valid`)
- **Global variables:** snake_case with `g_` prefix (e.g., `g_config`, `g_instance_count`)
- **Static variables:** snake_case with `s_` prefix (e.g., `s_initialized`, `s_cache`)
- **Pointers:** Include `p` or `ptr` suffix when helpful (e.g., `user_ptr`, `buffer_p`)

## Constant/Macro Naming
- **Macros:** UPPER_SNAKE_CASE (e.g., `MAX_BUFFER_SIZE`, `DEFAULT_TIMEOUT`)
- **Enum values:** UPPER_SNAKE_CASE (e.g., `STATUS_OK`, `ERROR_INVALID_INPUT`)
- **Compile-time constants:** UPPER_SNAKE_CASE with `#define`

## Function Naming
- **Functions:** snake_case (e.g., `calculate_total()`, `parse_input()`)
- **Module prefix:** Use module name prefix (e.g., `user_create()`, `user_destroy()`)
- **Static functions:** snake_case, no prefix needed (internal to file)
- **Init/cleanup pairs:** Use `_init()` and `_cleanup()` or `_create()` and `_destroy()`

## Type Naming
- **Structs:** snake_case with `_t` suffix or PascalCase (e.g., `user_data_t` or `UserData`)
- **Typedefs:** snake_case with `_t` suffix (e.g., `user_id_t`, `callback_fn_t`)
- **Enums:** snake_case with `_e` suffix for type (e.g., `status_e`)

## Organization
- Header includes at top (system headers, then project headers)
- Macro definitions after includes
- Type definitions (structs, enums, typedefs)
- Function prototypes
- Global/static variable declarations
- Function implementations
