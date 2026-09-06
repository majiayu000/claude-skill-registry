---
name: binutils
description: 'Use when building static archives with ar, stripping or converting binaries, mapping crash addresses with addr2line, or demangling C++ symbols. Not for ELF analysis: use elf-inspection.'
---

# GNU binutils

The GNU binutils manipulate existing binaries: static archives, symbol stripping, address to source mapping, and name demangling. Inspection of ELF structure belongs to `elf-inspection`.

## Contract

| Field | Bound contract |
|---|---|
| Trigger | The task creates or modifies a static archive, strips or converts a binary, separates debug info, maps a crash address to source, extracts printable strings, or demangles a symbol. |
| Authority | Reversible local: writes only the archive, binary, or debug files the user names, and preserves each input when producing a new output file; rollback is version control or the preserved input. No remote mutation. |
| Side effect | Local writes to archives, binaries, `.debug` files, and generated object files. Local reads of every other file. |
| Done | The named artifact exists with the requested transformation applied, verified by re-running the matching inspection command (`ar t`, `file`, `addr2line`, `nm -C`) on the output. |

## Inputs

- The target file or files: required. Name every input; the skill writes only named targets.
- The transformation: required. Create, strip, convert, debuglink, embed, map, or demangle.
- The target architecture: required for cross targets, so the tool prefix is `aarch64-linux-gnu-` or `arm-none-eabi-` instead of the host tools.

## Procedure

1. Build a static archive with `ar`. `r` inserts, `c` creates without a warning, `s` writes the symbol index. Done when: `ar t` lists the expected members and `nm libfoo.a` shows their symbols.

```bash
ar rcs libfoo.a foo.o bar.o baz.o
ar t libfoo.a            # list members
ar x libfoo.a foo.o      # extract one member
ar r libfoo.a new.o      # insert or replace
ar d libfoo.a old.o      # delete
ranlib libfoo.a          # rebuild the index after an external edit
```

LTO objects carry GIMPLE IR that plain `ar` indexes incorrectly. Use `gcc-ar` and `gcc-ranlib` for GCC, or `llvm-ar` for Clang.

2. Strip a binary. Choose the flag from what must survive. Done when: `file prog` reports `stripped` (or not) as intended, and the symbols that must remain do.

```bash
strip --strip-all prog         # smallest output, no symbols
strip --strip-debug prog       # keep the symbol table for crash reports
strip --strip-unneeded prog    # for shared libraries: keep exported symbols
strip -o prog.stripped prog    # write a copy, preserve the input
```

3. Separate debug info so a small shipped binary still debugs. Done when: GDB loads `prog.debug` through the debuglink without a manual `symbol-file`.

```bash
gcc -g -O2 -o prog main.c
objcopy --only-keep-debug prog prog.debug   # save debug info
strip --strip-debug prog                    # slim the shipped binary
objcopy --add-gnu-debuglink=prog.debug prog # GDB finds prog.debug by name
```

4. Convert and reshape binaries with `objcopy`. Done when: the output loads on the target or links into the project.

```bash
objcopy -O binary prog prog.bin    # raw binary for embedded flashing
objcopy -O ihex prog prog.hex      # Intel HEX
objcopy -O srec prog prog.srec     # Motorola S-record
objcopy --remove-section .comment prog
objcopy --rename-section .text=.boot_text prog
objcopy --compress-debug-sections prog
```

Embed a data file as linkable symbols. The `--rename-section` flags move the blob out of `.data` so it lands in read-only memory:

```bash
objcopy -I binary -O elf64-x86-64 \
    --rename-section .data=.rodata,alloc,load,readonly,data,contents \
    data.bin data_blob.o
# links as _binary_data_bin_start / _binary_data_bin_end / _binary_data_bin_size
```

5. Map a crash address to source with `addr2line`. The binary needs debug info from `-g`. For a stripped binary, point `-e` at the unstripped build or the `.debug` file. Done when: every address resolves to a file and line, with inline frames shown by `-i`.

```bash
addr2line -e prog -f -i 0x400a12
grep -o '0x[0-9a-f]*' crash.log | addr2line -e prog -f -i
```

6. Demangle C++ symbols with `c++filt`, or let `nm -C` demangle inline. Done when: the mangled name from the linker error or crash log reads as a plain signature.

```bash
c++filt _ZN3foo3barEv        # foo::bar()
nm prog | c++filt
```

7. Extract printable strings. Default minimum length is 4; raise it with `-n` to cut noise. Print offsets with `-t x` so a hit can be located in a hex dump. Done when: the searched string and its offset are reported. Scan only data sections with `-d` to skip code bytes.

```bash
strings -n 8 -t x prog
strings -d prog | grep -i version
objdump -s -j .rodata prog   # dump the section itself, no version quirks
```

8. For cross-compiled targets, prefix every tool with the target triplet; the host tools reject foreign objects. Done when: each command runs the triplet-prefixed tool.

```bash
aarch64-linux-gnu-objcopy -O binary prog prog.bin
aarch64-linux-gnu-addr2line -e prog -f 0x400a12
arm-none-eabi-nm libfirmware.a
```

## Failure and recovery

| Failure class | Behavior |
|---|---|
| `addr2line` prints `??:0` | The binary has no debug info, or the address comes from a different build. Point `-e` at the exact build, or rebuild with `-g`. |
| `x: index not found` from `ar` or link errors on an LTO archive | The archive was built with plain `ar`. Rebuild it with `gcc-ar` or `llvm-ar`. |
| Strip removed a needed symbol | Redo the strip from the preserved input with `--strip-debug` or `--strip-unneeded` instead of `--strip-all`. |
| `objcopy` rejects the format | The target architecture differs from the host tool. Switch to the triplet-prefixed tool and pass the matching `-O` format. |
| Debuglink does not resolve | GDB searches a build-id route and fixed dirs, not next to the binary by default. Verify with `readelf -n prog` that the build ID matches `prog.debug`. |

## Output

The transformed artifact plus a one-line verification per step: archive members, `file` classification of the stripped output, an `addr2line` resolution, or the demangled symbol. A reference table of the flags above is in `references/cheatsheet.md`.
