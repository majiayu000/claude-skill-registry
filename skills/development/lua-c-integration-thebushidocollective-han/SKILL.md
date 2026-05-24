---
name: Lua C Integration
description: Use when lua C API for extending Lua with native code including stack operations, calling C from Lua, calling Lua from C, creating C modules, userdata types, metatables in C, and performance optimization techniques.
allowed-tools: []
---

# Lua C Integration

## Introduction

Lua's C API enables seamless integration with C code, allowing developers to
extend Lua with high-performance native functionality or embed Lua as a scripting
engine within C applications. This bidirectional integration makes Lua ideal for
performance-critical applications requiring scripting capabilities.

The C API operates through a virtual stack for passing values between Lua and C,
with functions for manipulating Lua values, calling functions, and managing
memory. Understanding stack operations and Lua's data model is essential for
safe, efficient C integration.

This skill covers the Lua stack, calling C from Lua, calling Lua from C,
creating C modules, userdata and metatables, error handling, memory management,
and performance optimization patterns.

## Lua Stack Fundamentals

The Lua-C API uses a virtual stack for all value exchange between Lua and C,
requiring understanding of push/pop operations.

```c
#include <lua.h>
#include <lauxlib.h>
#include <lualib.h>

// Basic stack operations
void demonstrate_stack(lua_State *L) {
    // Push values onto stack
    lua_pushinteger(L, 42);           // Stack: 42
    lua_pushnumber(L, 3.14);          // Stack: 42 | 3.14
    lua_pushstring(L, "hello");       // Stack: 42 | 3.14 | "hello"
    lua_pushboolean(L, 1);            // Stack: 42 | 3.14 | "hello" | true
    lua_pushnil(L);                   // Stack: 42 | 3.14 | "hello" | true | nil

    // Get stack size
    int top = lua_gettop(L);          // Returns 5

    // Access values by index (1-based)
    lua_Integer i = lua_tointeger(L, 1);      // 42 (index from bottom)
    lua_Number n = lua_tonumber(L, 2);        // 3.14
    const char *s = lua_tostring(L, 3);       // "hello"
    int b = lua_toboolean(L, 4);              // 1 (true)

    // Negative indices (from top)
    lua_Number n2 = lua_tonumber(L, -4);      // 3.14 (4th from top)
    const char *s2 = lua_tostring(L, -3);     // "hello" (3rd from top)

    // Type checking
    if (lua_isnumber(L, 1)) {
        // Handle number
    }
    if (lua_isstring(L, 3)) {
        // Handle string
    }

    // Remove elements
    lua_pop(L, 1);                    // Remove top element (nil)
    lua_remove(L, 2);                 // Remove element at index 2 (3.14)

    // Replace element
    lua_pushstring(L, "world");
    lua_replace(L, 3);                // Replace index 3 with "world"

    // Clear stack
    lua_settop(L, 0);                 // Empty the stack
}

// Stack manipulation patterns
void stack_patterns(lua_State *L) {
    // Insert at specific position
    lua_pushstring(L, "new value");
    lua_insert(L, 1);                 // Insert at bottom

    // Copy element
    lua_pushvalue(L, 1);              // Duplicate element at index 1

    // Rotate elements
    lua_rotate(L, 1, 2);              // Rotate 2 elements starting from index 1

    // Check stack space
    if (!lua_checkstack(L, 100)) {
        // Failed to allocate stack space
    }

    // Absolute index (doesn't change with stack modifications)
    int abs_idx = lua_absindex(L, -1);
}

// Type checking helper
int check_arguments(lua_State *L) {
    int argc = lua_gettop(L);

    if (argc < 2) {
        return luaL_error(L, "Expected at least 2 arguments");
    }

    if (!lua_isnumber(L, 1)) {
        return luaL_error(L, "Argument 1 must be a number");
    }

    if (!lua_isstring(L, 2)) {
        return luaL_error(L, "Argument 2 must be a string");
    }

    return 0;
}

// Table operations
void table_operations(lua_State *L) {
    // Create table
    lua_newtable(L);                  // Stack: {}

    // Set field: table["key"] = "value"
    lua_pushstring(L, "value");
    lua_setfield(L, -2, "key");

    // Get field: value = table["key"]
    lua_getfield(L, -1, "key");
    const char *value = lua_tostring(L, -1);
    lua_pop(L, 1);

    // Set with arbitrary key
    lua_pushstring(L, "key2");
    lua_pushinteger(L, 42);
    lua_settable(L, -3);              // table[key2] = 42

    // Array-style: table[1] = "first"
    lua_pushinteger(L, 1);
    lua_pushstring(L, "first");
    lua_settable(L, -3);

    // Rawset/rawget (bypass metamethods)
    lua_pushstring(L, "rawkey");
    lua_pushstring(L, "rawvalue");
    lua_rawset(L, -3);

    // Table length
    lua_len(L, -1);
    lua_Integer len = lua_tointeger(L, -1);
    lua_pop(L, 1);
}

// Global variables
void global_operations(lua_State *L) {
    // Set global: my_global = 42
    lua_pushinteger(L, 42);
    lua_setglobal(L, "my_global");

    // Get global: value = my_global
    lua_getglobal(L, "my_global");
    lua_Integer value = lua_tointeger(L, -1);
    lua_pop(L, 1);
}
```

Master stack operations for efficient C-Lua value exchange and avoid stack
overflow through proper cleanup.

## Calling C Functions from Lua

C functions follow specific signatures and conventions to be callable from Lua
scripts.

```c
#include <lua.h>
#include <lauxlib.h>
#include <lualib.h>

// Basic C function callable from Lua
// int my_function(lua_State *L)
// Returns number of return values pushed onto stack
static int add(lua_State *L) {
    // Get arguments
    lua_Number a = luaL_checknumber(L, 1);
    lua_Number b = luaL_checknumber(L, 2);

    // Compute result
    lua_Number result = a + b;

    // Push result
    lua_pushnumber(L, result);

    // Return number of results
    return 1;
}

// Multiple return values
static int divide_with_remainder(lua_State *L) {
    lua_Integer a = luaL_checkinteger(L, 1);
    lua_Integer b = luaL_checkinteger(L, 2);

    if (b == 0) {
        return luaL_error(L, "Division by zero");
    }

    lua_pushinteger(L, a / b);        // Quotient
    lua_pushinteger(L, a % b);        // Remainder

    return 2;  // Return 2 values
}

// Optional arguments with defaults
static int greet(lua_State *L) {
    const char *name = luaL_optstring(L, 1, "World");
    lua_pushfstring(L, "Hello, %s!", name);
    return 1;
}

// Table as argument
static int sum_table(lua_State *L) {
    luaL_checktype(L, 1, LUA_TTABLE);

    lua_Number sum = 0;
    lua_Integer len = luaL_len(L, 1);

    for (lua_Integer i = 1; i <= len; i++) {
        lua_geti(L, 1, i);  // Get table[i]
        sum += lua_tonumber(L, -1);
        lua_pop(L, 1);
    }

    lua_pushnumber(L, sum);
    return 1;
}

// Returning a table
static int create_point(lua_State *L) {
    lua_Number x = luaL_checknumber(L, 1);
    lua_Number y = luaL_checknumber(L, 2);

    lua_newtable(L);

    lua_pushnumber(L, x);
    lua_setfield(L, -2, "x");

    lua_pushnumber(L, y);
    lua_setfield(L, -2, "y");

    return 1;
}

// Variadic arguments
static int print_all(lua_State *L) {
    int n = lua_gettop(L);  // Number of arguments

    for (int i = 1; i <= n; i++) {
        const char *str = luaL_tolstring(L, i, NULL);
        printf("%s\n", str);
        lua_pop(L, 1);  // Pop string from luaL_tolstring
    }

    return 0;
}

// Function with callback
static int each(lua_State *L) {
    luaL_checktype(L, 1, LUA_TTABLE);
    luaL_checktype(L, 2, LUA_TFUNCTION);

    lua_Integer len = luaL_len(L, 1);

    for (lua_Integer i = 1; i <= len; i++) {
        lua_pushvalue(L, 2);      // Push function
        lua_geti(L, 1, i);        // Push table[i]
        lua_pushinteger(L, i);    // Push index

        // Call function with 2 arguments
        if (lua_pcall(L, 2, 0, 0) != LUA_OK) {
            return lua_error(L);
        }
    }

    return 0;
}

// Register functions
static const luaL_Reg mylib[] = {
    {"add", add},
    {"divide_with_remainder", divide_with_remainder},
    {"greet", greet},
    {"sum_table", sum_table},
    {"create_point", create_point},
    {"print_all", print_all},
    {"each", each},
    {NULL, NULL}  // Sentinel
};

// Library initialization
int luaopen_mylib(lua_State *L) {
    luaL_newlib(L, mylib);
    return 1;
}

// Alternative registration
void register_functions(lua_State *L) {
    lua_register(L, "add", add);
    lua_register(L, "greet", greet);
}
```

C functions must follow Lua's calling convention and properly manage the stack
for reliable integration.

## Calling Lua from C

C code can load Lua scripts, call Lua functions, and access Lua global variables.

```c
#include <lua.h>
#include <lauxlib.h>
#include <lualib.h>
#include <stdio.h>

// Execute Lua script
void execute_script(const char *filename) {
    lua_State *L = luaL_newstate();
    luaL_openlibs(L);

    if (luaL_dofile(L, filename) != LUA_OK) {
        fprintf(stderr, "Error: %s\n", lua_tostring(L, -1));
        lua_close(L);
        return;
    }

    lua_close(L);
}

// Execute Lua string
void execute_string(const char *code) {
    lua_State *L = luaL_newstate();
    luaL_openlibs(L);

    if (luaL_dostring(L, code) != LUA_OK) {
        fprintf(stderr, "Error: %s\n", lua_tostring(L, -1));
    }

    lua_close(L);
}

// Call Lua function
void call_lua_function(lua_State *L, const char *func_name, int arg) {
    lua_getglobal(L, func_name);  // Get function

    if (!lua_isfunction(L, -1)) {
        fprintf(stderr, "%s is not a function\n", func_name);
        lua_pop(L, 1);
        return;
    }

    lua_pushinteger(L, arg);      // Push argument

    if (lua_pcall(L, 1, 1, 0) != LUA_OK) {
        fprintf(stderr, "Error calling %s: %s\n",
                func_name, lua_tostring(L, -1));
        lua_pop(L, 1);
        return;
    }

    // Get result
    lua_Integer result = lua_tointeger(L, -1);
    printf("Result: %lld\n", result);
    lua_pop(L, 1);
}

// Call with multiple arguments and returns
void call_with_multiple(lua_State *L) {
    lua_getglobal(L, "divide");

    lua_pushinteger(L, 10);
    lua_pushinteger(L, 3);

    // Call with 2 arguments, 2 returns
    if (lua_pcall(L, 2, 2, 0) != LUA_OK) {
        fprintf(stderr, "Error: %s\n", lua_tostring(L, -1));
        return;
    }

    lua_Integer quotient = lua_tointeger(L, -2);
    lua_Integer remainder = lua_tointeger(L, -1);
    lua_pop(L, 2);

    printf("Quotient: %lld, Remainder: %lld\n", quotient, remainder);
}

// Protected call with error handler
int error_handler(lua_State *L) {
    const char *msg = lua_tostring(L, -1);
    luaL_traceback(L, L, msg, 1);
    return 1;
}

void safe_call(lua_State *L, const char *func_name) {
    lua_pushcfunction(L, error_handler);
    int errfunc_idx = lua_gettop(L);

    lua_getglobal(L, func_name);
    lua_pushinteger(L, 42);

    if (lua_pcall(L, 1, 1, errfunc_idx) != LUA_OK) {
        fprintf(stderr, "Error: %s\n", lua_tostring(L, -1));
        lua_pop(L, 1);
    } else {
        // Handle result
        lua_pop(L, 1);
    }

    lua_pop(L, 1);  // Remove error handler
}

// Access Lua table from C
void access_lua_table(lua_State *L) {
    lua_getglobal(L, "config");

    if (!lua_istable(L, -1)) {
        fprintf(stderr, "config is not a table\n");
        lua_pop(L, 1);
        return;
    }

    // Get field
    lua_getfield(L, -1, "timeout");
    lua_Integer timeout = lua_tointeger(L, -1);
    lua_pop(L, 1);

    // Iterate table
    lua_pushnil(L);  // First key
    while (lua_next(L, -2) != 0) {
        // Key at -2, value at -1
        const char *key = lua_tostring(L, -2);
        const char *value = lua_tostring(L, -1);
        printf("%s = %s\n", key, value);
        lua_pop(L, 1);  // Remove value, keep key for next
    }

    lua_pop(L, 1);  // Remove table
}

// Set Lua global from C
void set_lua_global(lua_State *L, const char *name, lua_Integer value) {
    lua_pushinteger(L, value);
    lua_setglobal(L, name);
}

// Load Lua chunk without executing
void load_chunk(lua_State *L, const char *code) {
    if (luaL_loadstring(L, code) != LUA_OK) {
        fprintf(stderr, "Load error: %s\n", lua_tostring(L, -1));
        lua_pop(L, 1);
        return;
    }

    // Chunk is on stack as function
    // Call it when ready
    if (lua_pcall(L, 0, 0, 0) != LUA_OK) {
        fprintf(stderr, "Execution error: %s\n", lua_tostring(L, -1));
        lua_pop(L, 1);
    }
}
```

Calling Lua from C enables using Lua as a configuration or scripting layer
within C applications.

## Creating C Modules

C modules package related functions and constants for use in Lua programs.

```c
#include <lua.h>
#include <lauxlib.h>
#include <math.h>

// Module functions
static int vector_new(lua_State *L) {
    lua_Number x = luaL_checknumber(L, 1);
    lua_Number y = luaL_checknumber(L, 2);

    lua_newtable(L);

    lua_pushnumber(L, x);
    lua_setfield(L, -2, "x");

    lua_pushnumber(L, y);
    lua_setfield(L, -2, "y");

    return 1;
}

static int vector_add(lua_State *L) {
    luaL_checktype(L, 1, LUA_TTABLE);
    luaL_checktype(L, 2, LUA_TTABLE);

    lua_getfield(L, 1, "x");
    lua_Number x1 = lua_tonumber(L, -1);
    lua_pop(L, 1);

    lua_getfield(L, 1, "y");
    lua_Number y1 = lua_tonumber(L, -1);
    lua_pop(L, 1);

    lua_getfield(L, 2, "x");
    lua_Number x2 = lua_tonumber(L, -1);
    lua_pop(L, 1);

    lua_getfield(L, 2, "y");
    lua_Number y2 = lua_tonumber(L, -1);
    lua_pop(L, 1);

    lua_newtable(L);
    lua_pushnumber(L, x1 + x2);
    lua_setfield(L, -2, "x");
    lua_pushnumber(L, y1 + y2);
    lua_setfield(L, -2, "y");

    return 1;
}

static int vector_magnitude(lua_State *L) {
    luaL_checktype(L, 1, LUA_TTABLE);

    lua_getfield(L, 1, "x");
    lua_Number x = lua_tonumber(L, -1);
    lua_pop(L, 1);

    lua_getfield(L, 1, "y");
    lua_Number y = lua_tonumber(L, -1);
    lua_pop(L, 1);

    lua_pushnumber(L, sqrt(x*x + y*y));
    return 1;
}

// Module table
static const luaL_Reg vector_funcs[] = {
    {"new", vector_new},
    {"add", vector_add},
    {"magnitude", vector_magnitude},
    {NULL, NULL}
};

// Module initialization
int luaopen_vector(lua_State *L) {
    luaL_newlib(L, vector_funcs);

    // Add constants
    lua_pushnumber(L, M_PI);
    lua_setfield(L, -2, "PI");

    lua_pushnumber(L, M_E);
    lua_setfield(L, -2, "E");

    return 1;
}

// Submodules pattern
static const luaL_Reg math_basic[] = {
    {"add", add},
    {"subtract", subtract},
    {NULL, NULL}
};

static const luaL_Reg math_trig[] = {
    {"sin", trig_sin},
    {"cos", trig_cos},
    {NULL, NULL}
};

int luaopen_mathlib(lua_State *L) {
    lua_newtable(L);

    // Basic submodule
    luaL_newlib(L, math_basic);
    lua_setfield(L, -2, "basic");

    // Trig submodule
    luaL_newlib(L, math_trig);
    lua_setfield(L, -2, "trig");

    return 1;
}

// Module with state
typedef struct {
    int counter;
    char name[64];
} ModuleState;

static int get_counter(lua_State *L) {
    ModuleState *state = (ModuleState *)lua_touserdata(L, lua_upvalueindex(1));
    lua_pushinteger(L, state->counter);
    return 1;
}

static int increment_counter(lua_State *L) {
    ModuleState *state = (ModuleState *)lua_touserdata(L, lua_upvalueindex(1));
    state->counter++;
    return 0;
}

int luaopen_stateful(lua_State *L) {
    ModuleState *state = (ModuleState *)lua_newuserdata(L, sizeof(ModuleState));
    state->counter = 0;
    strncpy(state->name, "default", sizeof(state->name));

    // Functions with state as upvalue
    lua_newtable(L);

    lua_pushvalue(L, -2);  // Push state
    lua_pushcclosure(L, get_counter, 1);
    lua_setfield(L, -2, "get_counter");

    lua_pushvalue(L, -2);  // Push state
    lua_pushcclosure(L, increment_counter, 1);
    lua_setfield(L, -2, "increment");

    return 1;
}
```

Organize related functionality into modules for clean API design and namespace
management.

## Userdata and Metatables

Userdata wraps C structures for use in Lua with custom behavior through
metatables.

```c
#include <lua.h>
#include <lauxlib.h>
#include <stdlib.h>

// C structure
typedef struct {
    double x;
    double y;
} Point;

#define POINT_METATABLE "Point"

// Constructor
static int point_new(lua_State *L) {
    double x = luaL_checknumber(L, 1);
    double y = luaL_checknumber(L, 2);

    Point *p = (Point *)lua_newuserdata(L, sizeof(Point));
    p->x = x;
    p->y = y;

    luaL_getmetatable(L, POINT_METATABLE);
    lua_setmetatable(L, -2);

    return 1;
}

// Get userdata from stack
static Point *check_point(lua_State *L, int index) {
    return (Point *)luaL_checkudata(L, index, POINT_METATABLE);
}

// Methods
static int point_distance(lua_State *L) {
    Point *p1 = check_point(L, 1);
    Point *p2 = check_point(L, 2);

    double dx = p2->x - p1->x;
    double dy = p2->y - p1->y;
    double dist = sqrt(dx*dx + dy*dy);

    lua_pushnumber(L, dist);
    return 1;
}

static int point_tostring(lua_State *L) {
    Point *p = check_point(L, 1);
    lua_pushfstring(L, "Point(%f, %f)", p->x, p->y);
    return 1;
}

static int point_add(lua_State *L) {
    Point *p1 = check_point(L, 1);
    Point *p2 = check_point(L, 2);

    Point *result = (Point *)lua_newuserdata(L, sizeof(Point));
    result->x = p1->x + p2->x;
    result->y = p1->y + p2->y;

    luaL_getmetatable(L, POINT_METATABLE);
    lua_setmetatable(L, -2);

    return 1;
}

static int point_eq(lua_State *L) {
    Point *p1 = check_point(L, 1);
    Point *p2 = check_point(L, 2);

    lua_pushboolean(L, p1->x == p2->x && p1->y == p2->y);
    return 1;
}

static int point_index(lua_State *L) {
    Point *p = check_point(L, 1);
    const char *key = luaL_checkstring(L, 2);

    if (strcmp(key, "x") == 0) {
        lua_pushnumber(L, p->x);
        return 1;
    } else if (strcmp(key, "y") == 0) {
        lua_pushnumber(L, p->y);
        return 1;
    }

    return 0;
}

static int point_newindex(lua_State *L) {
    Point *p = check_point(L, 1);
    const char *key = luaL_checkstring(L, 2);
    double value = luaL_checknumber(L, 3);

    if (strcmp(key, "x") == 0) {
        p->x = value;
    } else if (strcmp(key, "y") == 0) {
        p->y = value;
    }

    return 0;
}

// Garbage collection
static int point_gc(lua_State *L) {
    Point *p = check_point(L, 1);
    // Cleanup if needed (e.g., free allocated memory)
    return 0;
}

// Metatable methods
static const luaL_Reg point_metamethods[] = {
    {"__tostring", point_tostring},
    {"__add", point_add},
    {"__eq", point_eq},
    {"__index", point_index},
    {"__newindex", point_newindex},
    {"__gc", point_gc},
    {NULL, NULL}
};

// Module initialization
int luaopen_point(lua_State *L) {
    // Create metatable
    luaL_newmetatable(L, POINT_METATABLE);
    luaL_setfuncs(L, point_metamethods, 0);

    // Create module table
    lua_newtable(L);
    lua_pushcfunction(L, point_new);
    lua_setfield(L, -2, "new");

    lua_pushcfunction(L, point_distance);
    lua_setfield(L, -2, "distance");

    return 1;
}

// Light userdata (pointer without GC)
static int create_light_userdata(lua_State *L) {
    Point *p = (Point *)malloc(sizeof(Point));
    p->x = 10;
    p->y = 20;

    lua_pushlightuserdata(L, p);
    return 1;
}
```

Userdata enables passing C structures to Lua while controlling access through
metatables.

## Best Practices

1. **Always check lua_pcall results** to catch and handle Lua errors properly

2. **Use luaL_check functions** for argument validation with clear error messages

3. **Balance push and pop operations** to prevent stack overflow and leaks

4. **Create metatables for userdata** to enable natural Lua-style access patterns

5. **Use luaL_newlib for modules** to simplify registration of function tables

6. **Handle errors with luaL_error** rather than returning error codes

7. **Avoid lua_tostring for numbers** as it modifies the stack; use lua_tonumber

8. **Use lua_absindex** when stack positions change during operations

9. **Register metamethods for userdata** cleanup to prevent memory leaks

10. **Document stack effects** in comments for complex C functions

## Common Pitfalls

1. **Stack overflow from unbalanced push/pop** causes crashes and undefined
   behavior

2. **Not checking function return types** leads to type mismatches and errors

3. **Using lua_tostring without checking** modifies stack for non-strings

4. **Calling lua_error directly** instead of luaL_error loses error context

5. **Accessing invalid stack indices** causes undefined behavior and crashes

6. **Not setting metatables on userdata** makes garbage collection unreliable

7. **Mixing absolute and relative indices** causes confusion and bugs

8. **Forgetting lua_pcall error handling** causes uncaught exceptions

9. **Not using luaL_checkudata** allows type confusion and crashes

10. **Closing lua_State prematurely** invalidates all references and causes
    crashes

## When to Use This Skill

Apply C integration when performance-critical operations exceed pure Lua
capabilities.

Use C modules to wrap existing C libraries for use in Lua applications.

Leverage userdata when managing complex C structures from Lua code.

Embed Lua as a scripting engine in C applications requiring runtime
configuration.

Create C extensions for computationally intensive algorithms unsuitable for Lua.

Implement low-level system operations or hardware interfaces through C bindings.

## Resources

- [Programming in Lua - The C API](<https://www.lua.org/pil/24.html>)
- [Lua Reference Manual - C API](<https://www.lua.org/manual/5.4/manual.html#4>)
- [Lua Users Wiki - Binding Code To Lua](<http://lua-users.org/wiki/BindingCodeToLua>)
- [LuaJIT FFI Library](<http://luajit.org/ext_ffi.html>)
- [Lua C API Tutorial](<https://www.lua.org/pil/contents.html#24>)
