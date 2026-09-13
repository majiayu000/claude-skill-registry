---
name: hare-lang
description: 'Use when building or evaluating a Hare program: hare build, run, or test, tagged-union error handling, or calling C through bodyless fn declarations and -l. Not for Zig or C: use zig-cinterop or gcc.'
disable-model-invocation: true
---

# Hare

Hare is a small compiled systems language with a C-like execution model, tagged unions for errors, and a standard library that ships with the compiler. Current release 0.26.0.1 (point release of 0.26.0, 2026-02-13); there is no 1.0 and the project states it has not reached its planned 1.0 freeze. Supported targets: x86_64, aarch64, riscv64 on Linux, FreeBSD, OpenBSD, NetBSD, and DragonFlyBSD. No generics, no macros, no package manager.

## Contract

| Field | Bound contract |
|---|---|
| Trigger | The user writes, builds, tests, or evaluates Hare code, needs the C FFI pattern, or asks whether Hare fits a utility, daemon, or tool compared with C or Zig. |
| Authority | Reversible local: writes only Hare source files, build outputs named by `-o`, and the toolchain install under the prefix the user chose; rollback is deleting those files or `make uninstall` in the toolchain clone. No remote mutation. |
| Side effect | Source and binary files in the project directory. A toolchain bootstrap compiles `qbe`, `harec`, and `hare` and installs them under `/usr/local` by default. |
| Done | The program builds with `hare build`, its tests pass under `hare test`, every error path is propagated with `?` or handled in a `match`, and any C boundary is declared with the bodyless-prototype form and linked with `-l`. |

## Inputs

- Source directory: a Hare module is a directory holding one or more `.ha` files. Dependencies resolve by scanning `use` directives, first in the working directory and then along `HAREPATH` (a colon-separated list; `hare version -v` prints the default). There is no manifest file.
- Toolchain: `qbe` (backend), `harec` (compiler), `hare` (build driver and standard library). A C11 compiler and `scdoc` (for man pages, optional) are the bootstrap dependencies.
- Build tags when a file is platform- or mode-specific: `+linux`, `+test`, `+libc` in the file name or via `-T`.
- For C interop: the C library name for `-l` and, when the header lives off the default path, `-L`.

## Procedure

1. Install or confirm the toolchain. Check with `hare version`. To bootstrap: clone and `make` then `make install` `harec` from `https://git.sr.ht/~sircmpwn/harec`, then the same for `hare` from `https://git.sr.ht/~sircmpwn/hare` (`make check` runs its test suite first). Install `qbe` from `https://c9x.me/compile/` before `harec`. Root is needed only because the default prefix is `/usr/local`. Done when: `hare version` prints a version.
2. Lay out the module. Create a directory and a `main.ha`:

   ```hare
   use fmt;

   export fn main() void = {
   	fmt::println("Hello, Hare!")!;
   };
   ```

   Build with `hare build -o mytool` and run with `./mytool`, or `hare run .` to do both. Done when: the binary prints the greeting.
3. Handle errors as values. A fallible function returns a tagged union of its result and its error types. `?` propagates an error to the caller; `!` asserts success and aborts on error; `match` handles each case.

   ```hare
   use fmt;
   use fs;
   use io;
   use os;
   use strings;
   use encoding::utf8;

   fn read_file(path: str) (str | fs::error | io::error | utf8::invalid) = {
   	const file = os::open(path)?;
   	defer io::close(file)!;
   	const buf = io::drain(file)?;
   	return strings::fromutf8(buf)?;
   };

   export fn main() void = {
   	match (read_file("config.txt")) {
   	case let s: str =>
   		fmt::println(s)!;
   	case let err: fs::error =>
   		fmt::fatalf("error: {}", fs::strerror(err));
   	case let err: io::error =>
   		fmt::fatalf("error: {}", io::strerror(err));
   	case utf8::invalid =>
   		fmt::fatal("config.txt is not UTF-8");
   	};
   };
   ```

   `os::open` returns `(io::file | fs::error)`; `os` defines no error type of its own. `io::drain` allocates and reads to end of file; `io::readall` fills a caller-supplied buffer instead. `strings::fromutf8` returns `(str | utf8::invalid)`, never a bare `str`. Done when: the compiler accepts the function and every union member has a `case`.
4. Use the type system as written. Tagged unions: `type color = (u8 | u16 | void);`. Slices are pointer plus length: `fn sum(nums: []i32) i32` with `for (let i = 0z; i < len(nums); i += 1)`. Size literals carry the `z` suffix. There are no implicit numeric conversions; cast with `v: u16`. `abort()` and `abort("message")` end the program; `fmt::fatalf` prints and exits. Done when: no conversion is implicit and every `match` on a union is exhaustive or has a `case =>` arm.
5. Cross the C boundary with a bodyless prototype. Import `types::c` for C-compatible types and declare the foreign function without a body; add `@symbol("name")` only when the Hare identifier must differ from the linker symbol:

   ```hare
   use types::c;

   export type FILE = opaque;
   export @symbol("fopen") fn fopen(pathname: const *c::char, mode: const *c::char) nullable *FILE;
   ```

   Export a Hare function to C with the same attribute in reverse: `export @symbol("greet_user") fn greet_user(user: const *c::char) int = { ... };`. Link with `hare build -l <libname>`; any `-l` also links libc and adds the `+libc` tag. There is no `@extern` attribute. Done when: the program links and calls across the boundary.
6. Write tests next to the code in `+test.ha` files with the `@test` attribute and `assert`:

   ```hare
   @test fn sum_small() void = {
   	assert(sum([1i32, 2, 3]) == 6);
   };
   ```

   `hare test` adds the `+test` tag and runs them; a trailing glob selects tests by name. `-v` prints the compiler and linker commands, not per-test detail. Done when: `hare test` exits 0.
7. Reach for the standard library before writing code: `fmt`, `io`, `os`, `fs`, `strings`, `bufio`, `memio`, `net` (with `net::tcp`, `net::udp`, `net::dial`, `net::dns`, `net::ip`, `net::uri`), `time` (with `time::date`, `time::chrono`), `encoding` (`base32`, `base64`, `hex`, `pem`, `utf8`, `asn1`), `types::c`. JSON is not in the core library; `hare-json` is a separate extended-library repository providing `encoding::json`. Done when: no hand-written code duplicates a stdlib module.
8. Decide fit. Hare suits command-line utilities, build tools replacing shell, small network daemons, and code that must stay auditable without a runtime. Choose Zig instead when compile-time generics or metaprogramming carry the design (`zig-cinterop` covers its C boundary), and C when the project is glue over a large existing C code base (`gcc`). Done when: the recommendation names the deciding constraint.

## Failure and recovery

| Failure | Cause | Fix |
|---|---|---|
| `unknown type` or unresolved identifier | Missing `use module;` or module not on `HAREPATH` | Add the `use` line; check `hare version -v` for the search path |
| Link error on a C symbol | Library not passed | Add `-l <libname>` and, for a non-default path, `-L <dir>` |
| Compiler rejects an unhandled union member | `match` not exhaustive | Add the missing `case` or a `case =>` arm; or propagate with `?` |
| `utf8::invalid` at runtime | Bytes are not UTF-8 | Handle the `strings::fromutf8` error case instead of asserting with `!` |
| Test not run | File lacks the `+test` tag or function lacks `@test` | Rename to `name+test.ha` and add the attribute |
| No stdlib module for a platform call | Library gap | Declare the libc function as a bodyless prototype and link with `-l` |
| Code from an older tutorial fails to compile | Pre-1.0 churn; 0.26.0 replaced `@offset` with `_` padding fields | Read the release notes for the installed version |

## Output

A Hare module that builds with `hare build`, passes `hare test`, propagates or handles every error, and declares any C boundary with the bodyless-prototype form and the `-l` flags recorded; plus, when the question was fit, a recommendation naming the deciding constraint.
