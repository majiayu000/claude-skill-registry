---
name: make
description: 'Use when writing or debugging Makefiles, understanding pattern rules and automatic dependency generation, managing CFLAGS/LDFLAGS, or diagnosing incremental build, phony targets, or recursive make.'
---

# GNU Make

Idiomatic Makefile patterns for C/C++ projects: phony targets, pattern rules, automatic dependency generation, and incremental-build hygiene. Grounded against GNU Make 4.4.

## Contract

| Field | Bound contract |
|---|---|
| Trigger | The task writes or debugs a Makefile, sets up pattern rules or automatic dependency generation, manages `CFLAGS`/`LDFLAGS`, converts ad-hoc compile commands into a Makefile, or diagnoses incremental build failures. |
| Authority | Reversible local: writes only `Makefile`/`*.mk` files and local build outputs; rollback is version control plus `make clean`. No remote mutation. |
| Side effect | `make` runs the compiler and writes objects and binaries into the tree or build directory. |
| Done | `make` builds the target incrementally (a second run reports nothing to do) and `make clean` removes the outputs. |

## Inputs

- Source layout (required): where `.c`/`.cpp` files and headers live.
- Compiler and flags (required if not inferrable): `CC`, `CFLAGS`, `LDFLAGS`, `LDLIBS`.
- Build variants (optional): debug/release split, install prefix.

## Procedure

1. Write the minimal correct Makefile. Recipes start with a tab, not spaces. Done when: `make` builds and `make clean` removes outputs.

```makefile
CC      := gcc
CFLAGS  := -std=c23 -Wall -Wextra -g -O2
LDFLAGS :=
LDLIBS  :=

SRCS    := $(wildcard src/*.c)
OBJS    := $(SRCS:src/%.c=build/%.o)
TARGET  := build/prog

.PHONY: all clean

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(LDFLAGS) -o $@ $^ $(LDLIBS)

build/%.o: src/%.c | build
	$(CC) $(CFLAGS) -c -o $@ $<

build:
	mkdir -p build

clean:
	rm -rf build
```

Automatic variables: `$@` is the target, `$<` the first prerequisite, `$^` all prerequisites deduplicated, `$*` the pattern stem, `$(@D)` the target's directory part.

2. Add automatic dependency generation. Without it, editing a header rebuilds nothing. `-MMD` writes a `.d` file per object; `-MP` adds phony targets for headers so deleting one does not break the build. Done when: touching a header rebuilds exactly its dependents.

```makefile
DEPFLAGS = -MMD -MP
DEPS    := $(OBJS:.o=.d)

build/%.o: src/%.c | build
	$(CC) $(CFLAGS) $(DEPFLAGS) -MF $(@:.o=.d) -c -o $@ $<

-include $(DEPS)   # leading - ignores missing .d files on first build
```

3. Use pattern rules for repeated transforms. Done when: one rule covers each source-to-output shape.

```makefile
%.o: %.c
	$(CC) $(CFLAGS) -c -o $@ $<

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c -o $@ $<

%.s: %.c
	$(CC) $(CFLAGS) -S -o $@ $<
```

4. Add build variants and quiet output. Done when: `make BUILD=debug` switches flags and `make V=1` shows full commands.

```makefile
BUILD ?= release
ifeq ($(BUILD),debug)
  CFLAGS += -g -Og -DDEBUG
else
  CFLAGS += -O2 -DNDEBUG
endif

Q := $(if $(V),,@)
build/%.o: src/%.c | build
	@echo "  CC  $<"
	$(Q)$(CC) $(CFLAGS) -c -o $@ $<
```

5. Add an install target with `DESTDIR` and `PREFIX`. Done when: `make install DESTDIR=/tmp/stage` stages the tree.

```makefile
PREFIX ?= /usr/local

install: $(TARGET)
	install -d $(DESTDIR)$(PREFIX)/bin
	install -m 0755 $(TARGET) $(DESTDIR)$(PREFIX)/bin/
```

6. Structure multi-directory projects with included `.mk` files, not recursive make. Recursive make fragments the dependency graph and breaks parallelism. Done when: one top-level Makefile sees every prerequisite.

```makefile
# Makefile
include lib/module.mk
include src/app.mk
```

```makefile
# lib/module.mk
LIB_SRCS := $(wildcard lib/*.c)
LIB_OBJS := $(LIB_SRCS:lib/%.c=build/lib_%.o)
OBJS     += $(LIB_OBJS)

build/lib_%.o: lib/%.c
	$(CC) $(CFLAGS) -c -o $@ $<
```

7. Diagnose failures against this table. Done when: the error maps to a cause and a fix.

| Error | Cause | Fix |
|---|---|---|
| `No rule to make target 'foo.o'` | Missing source or rule | Check the source path and pattern rule |
| `Nothing to be done for 'all'` | Targets up to date | Touch a source or run `make clean` |
| `Circular dependency dropped` | Target depends on itself | Trace the prerequisite chain |
| `missing separator` | Spaces where a tab belongs | Recipes need a literal tab |
| `multiple target patterns` | Bad pattern rule syntax | Check `%` placement |
| Rebuilds everything | Wrong timestamps or missing `.PHONY` | Check `date`; mark `all` and `clean` phony |
| Header edit rebuilds nothing | No dependency tracking | Add `-MMD -MP` and `-include $(DEPS)` |

Useful flags: `make -j"$(nproc)"` parallel, `make -O` synchronizes output, `make -n` dry run, `make -B` force rebuild, `make -k` keep going, `make -p` print the rule database, `make --warn-undefined-variables` catch typos.

For the full variable, function, and special-target reference see `references/cheatsheet.md`.

## Failure and recovery

- `make` does nothing after a header edit: dependency files are missing; add `-MMD -MP` and `-include $(DEPS)`.
- Parallel build races: a missing order-only prerequisite or an undeclared generated header; declare the real dependency, never serialize to hide it.
- `missing separator`: convert the recipe's leading spaces to a tab.
- Variable expands empty: `=` defers expansion to use time, `:=` expands at definition; pick `:=` unless late expansion is the point. `::=` is the POSIX immediate form, available in GNU Make 4.4 and later.
- Recursive make is already present: include the child `.mk` files from the top Makefile instead of `$(MAKE) -C`.

## Output

A Makefile that builds incrementally, tracks header dependencies, supports `clean` and `install`, and survives `make -j`. For debugging tasks, the diagnosed cause and the minimal fix.
