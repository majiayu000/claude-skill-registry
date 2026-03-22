---
name: C
slug: c
version: 1.0.1
description: Write safe C avoiding memory corruption, buffer overflows, and undefined behavior traps.
metadata: {"clawdbot":{"emoji":"⚙️","requires":{"bins":["gcc","clang"]},"os":["linux","darwin","win32"]}}
---

## Quick Reference

| Topic | File |
|-------|------|
| malloc/free, leaks, double free | `memory.md` |
| Null, dangling, pointer arithmetic | `pointers.md` |
| Null terminator, buffer overflow | `strings.md` |
| Integer overflow, signed/unsigned | `types.md` |
| Macro traps, include guards | `preprocessor.md` |
| Common undefined behavior | `undefined.md` |

## Critical Rules

- `malloc` returns `void*` — cast required in C++, optional in C but check for NULL
- `free(ptr); ptr = NULL;` — always null after free to prevent double-free
- `sizeof(array)` in function gives pointer size, not array size — pass length separately
- `char str[5] = "hello";` — no room for null terminator, UB when used as string
- `strcpy` doesn't check bounds — use `strncpy` and manually null-terminate
- Signed overflow is UB — compiler can optimize assuming it never happens
- `i++ + i++` is UB — no sequence point between modifications
- Returning pointer to local variable — dangling pointer, UB on use
- `#define SQUARE(x) x*x` — `SQUARE(1+2)` = `1+2*1+2` = 5, not 9
- `memcpy` with overlapping regions — use `memmove` instead
- Uninitialized variables — contain garbage, UB if used
- Array out of bounds — no runtime check, silent corruption or crash
