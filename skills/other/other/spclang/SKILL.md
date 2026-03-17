---
name: sp
description: Guide for sp.h, a single-header C standard library replacement. You must use this guide when using or discussing sp.h in any capacity.
license: MIT
---

# sp.h Overview
- sp.h is a single-header C standard library replacement
- You MUST annotate references to functions from sp.h with verbatim function headers
- When providing references to code from `sp.h`, you MUST provide a matching declaration from `references/index.md`. Function names without the full declaration are COMPLETELY useless, and WILL NOT be tolerated.
<example>
user: How do I use the asset registry from sp.h?
assistant: [Reads the index, uses the Task tool to search through sources bundled with skill (sp.h, spn.c), includes "sp_str_t sp_str_sub(sp_str_t str, s32 index, s32 len)" in answer]
</example>
<example>
user: Write a function that reads a file and logs its contends
assistant: [Searches through bundled source code with Task tool to find relevant APIs and writes function]
</example>
- NEVER, EVER MODIFY THE REFERENCE CODE

## Usage
- Search `references/index.md` before trying to search through the codebase. Do not guess; refer to `references/index.md` to find a precise search term.
<example>
user: How do I read a file in sp.h?
assistant: [Reads index.md, searches through sp.h and spn.c with Task tool, provides concise, annotated answer]
</example>
- Search through `references/sp.h` judiciously as needed; do not guess symbol names, function signatures, or implementation details. Read the source code.
- Function signatures are prefixed with `SP_API`
- Types are prefixed with `sp_` and suffixed with `_t`

## Rules
- Never use `malloc`, `calloc`, or `realloc`; use `sp_alloc` (which zero initializes)
- Unless explicitly interfacing with an existing C API, never use `const char*`; use `sp_str_t` (pointer + length)
- Never use `strcmp`, `strlen`, or any `string.h` functions with `sp_str_t`; use `sp_str_*`
- Never use `strcmp`, `strlen`, or any `string.h` functions with `const char*`; use `sp_cstr_*`
- Always use `SP_ZERO_INITIALIZE()`. When you need a type, use `SP_ZERO_STRUCT(T)`
- Always use `sp_da(T)` and `sp_ht(T)` for dynamic arrays and hash maps (`sp_dyn_array_*` and `sp_ht_*`)
- Always use `sp_dyn_array_for(arr, it)` and `sp_ht_for(ht, it)` to iterate sp_da and sp_ht
- Never check `str.len > 0`; always use `!sp_str_empty(str)`
- Always use C99 designated initializers for struct literals when possible
- Always use short literal types (`s32`, `u8`, `c8`, `const c8*`)
- Never use `printf` family; always use `SP_LOG()`
- Always use `sp_carr_for()` when iterating a C array
- Always explicitly handle all enum cases in a switch statement. Fallthroughs are OK, `default` is not.

## Namespaces
Use these when searching through `references/index.md`, `references/sp.h`, or `references/spn.c`
- Memory: `sp_alloc`, `sp_context`, `sp_allocator`, `sp_os`
- Strings: `sp_str`, `sp_str_builder`, `sp_cstr`
- Containers: `sp_dyn_array` / `sp_da`, `sp_ht`, `sp_rb`
- IO: `sp_io`
- Process: `sp_ps`
- Filesystem: `sp_os`
- Platform: `sp_os`
- Time: `sp_tm`
- Concurrency: `sp_thread`, `sp_mutex`, `sp_semaphore`, `sp_atomic`, `sp_spin_lock`
- Logging: `sp_format`, `SP_LOG`, `SP_FMT_*`

## Common Patterns
### Initialization
```c
// Always zero-initialize structs
sp_str_builder_t builder = SP_ZERO_INITIALIZE();
sp_dynamic_array_t arr = SP_ZERO_INITIALIZE();
```

### String Handling
```c
// Create strings
sp_str_t literal = sp_str_lit("hello");     // Compile-time string literal
sp_str_t view = sp_str_view(some_char_ptr); // Runtime C string (calculates length)
sp_str_t copy = sp_str_from_cstr("hello");  // Allocates and copies
const char* cstr = sp_str_to_cstr(str);
```

### Dynamic Arrays (stb-style)
```c
sp_dyn_array(int) numbers = SP_NULLPTR;
sp_dyn_array_push(numbers, 42);
sp_dyn_array_push(numbers, 100);

sp_dyn_array_for(numbers, i) {
  SP_LOG("numbers[{}] = {}", SP_FMT_U32(i), SP_FMT_S32(numbers[i]));
}

u32 count = sp_dyn_array_size(numbers);
u32 capacity = sp_dyn_array_capacity(numbers);

// Cleanup happens automatically via allocator
```

### Hash Tables (stb-style)
```c
sp_ht(s32, s32) hta = SP_NULLPTR;
sp_ht(sp_str_t, s32) htb = SP_NULLPTR;
sp_ht_set_fns(hta, sp_ht_on_hash_str_key, sp_ht_on_compare_str_key);

sp_ht_insert(htb, SP_LIT("answer"), 42);

s32* value_ptr = sp_ht_getp(htb, SP_LIT("answer"));

sp_ht_key_exists(htb, SP_LIT("answer"));

sp_ht_for(htb, it) {
  sp_str_t* key = sp_ht_it_getkp(map, it);
  s32* val = sp_ht_it_getp(map, it);
}

// Cleanup happens automatically via allocator
```

### Formatting and Logging
```c
// Type-safe formatting with color support
SP_LOG(
  "Processing {:fg cyan} with {} {}",
  SP_FMT_STR(name),
  SP_FMT_U32(count),
  SP_FMT_CSTR("items")
);

sp_str_t msg = sp_format("Result: {}", SP_FMT_S32(42));

// Colors: :fg, :bg, :color
// Colors: black, red, green, yellow, blue, magenta, cyan, white
// Add 'bright' prefix for bright variants
```

### Switch Statements
```c
// Always use braces, always handle all cases
switch (state) {
  case STATE_IDLE: {
    break;
  }
  case STATE_RUNNING: {
    break;
  }
  default: {
    SP_UNREACHABLE_CASE();
  }
}
```

### Error Handling
```c
// Return an enum for recoverable errors (consumer app may have their own error type)
sp_err_t load_config(sp_str_t path, config_t* config) {
  if (!sp_os_does_path_exist(path)) {
    SP_LOG("Config not found: {}", SP_FMT_STR(path));
    return SP_ERR_WHATEVER;
  }

  return SP_ERR_OK;
}

// Prefer to SP_ASSERT when possible
void process_array(int* arr, u32 size) {
  SP_ASSERT(arr);
  SP_ASSERT(size > 0);
}

// SP_FATAL is SP_LOG + SP_ASSERT(false)
if (critical_failure) {
  SP_FATAL("Cannot continue: {:fg red}", SP_FMT_STR(reason));
}
```
