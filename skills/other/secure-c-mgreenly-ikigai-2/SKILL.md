---
name: security/secure-c
description: Secure C Coding security skill
---

# Secure C Coding

Avoid dangerous functions, use safe alternatives, enable compiler hardening.

## Banned Functions → Safe Alternatives

| Banned | Why | Use Instead |
|--------|-----|-------------|
| `strcpy` | No bounds | `strncpy`, `strlcpy`, `snprintf` |
| `strcat` | No bounds | `strncat`, `strlcat` |
| `sprintf` | No bounds | `snprintf` |
| `gets` | Always unsafe | `fgets` |
| `scanf("%s")` | No bounds | `scanf("%Ns")` with width |
| `mktemp` | Race condition | `mkstemp` |
| `atoi` | No error detection | `strtol` with validation |

## Compiler Hardening

```makefile
CFLAGS += -fstack-protector-strong  # Stack canaries
CFLAGS += -D_FORTIFY_SOURCE=2       # Runtime buffer checks
CFLAGS += -fPIE -pie                # ASLR for executables
LDFLAGS += -Wl,-z,relro,-z,now      # GOT protection
```

## Static Analysis

- `make lint` - clang-tidy checks
- `cppcheck --enable=all`
- Compiler warnings: `-Wall -Wextra -Werror`

**Review red flags:** Any banned function, missing bounds on string ops, `char buf[N]` with unchecked input.
