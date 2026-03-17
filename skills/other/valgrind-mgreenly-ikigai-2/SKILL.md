---
name: valgrind
description: Valgrind skill for the ikigai project
---

# Valgrind

## Description
Interpreting Valgrind memcheck output for memory debugging.

## Running Valgrind

```bash
# Via Makefile
make check-valgrind

# Direct invocation
valgrind --leak-check=full --track-origins=yes ./ikigai
```

## Error Types

### Invalid Read/Write
```
==12345== Invalid read of size 4
==12345==    at 0x... function_name (file.c:42)
==12345==  Address 0x... is 0 bytes after a block of size 100 alloc'd
```
**Meaning:** Reading/writing past buffer bounds or freed memory.
**Fix:** Check array indices, buffer sizes, use-after-free.

### Use of Uninitialized Value
```
==12345== Conditional jump or move depends on uninitialised value(s)
==12345==    at 0x... function_name (file.c:42)
==12345==  Uninitialised value was created by a heap allocation
==12345==    at 0x... malloc (...)
```
**Meaning:** Using memory before setting it.
**Fix:** Initialize variables, use `memset`, check all code paths.

### Invalid Free
```
==12345== Invalid free() / delete / delete[]
==12345==    at 0x... free (...)
==12345==  Address 0x... is 0 bytes inside a block of size 100 free'd
```
**Meaning:** Double-free or freeing invalid pointer.
**Fix:** Track ownership, use talloc's hierarchical free.

### Memory Leaks
```
==12345== LEAK SUMMARY:
==12345==    definitely lost: 100 bytes in 1 blocks
==12345==    indirectly lost: 200 bytes in 2 blocks
==12345==    possibly lost: 0 bytes in 0 blocks
==12345==    still reachable: 500 bytes in 5 blocks
```
- **definitely lost** - Memory with no pointer to it (real leak)
- **indirectly lost** - Memory reachable only through definitely lost
- **possibly lost** - Interior pointer exists (may be intentional)
- **still reachable** - Memory still accessible at exit (often acceptable)

## Common Options

```bash
--leak-check=full          # Detailed leak info
--track-origins=yes        # Where uninitialized values came from
--show-reachable=yes       # Show still-reachable blocks
--suppressions=file.supp   # Ignore known issues
--gen-suppressions=all     # Generate suppression entries
```

## Reading Stack Traces

```
==12345== Invalid read of size 4
==12345==    at 0x401234: parse_json (parser.c:142)
==12345==    by 0x401567: load_config (config.c:89)
==12345==    by 0x401890: main (main.c:23)
```
Read bottom-up: `main` called `load_config` called `parse_json` where error occurred.

## Helgrind (Thread Debugging)

```bash
valgrind --tool=helgrind ./ikigai
```

Detects:
- Data races
- Lock order violations
- Misuse of POSIX threading API

## References

- Valgrind manual: https://valgrind.org/docs/manual/
- See `gdbserver.md` for live debugging
- See `coredump.md` for crash analysis
