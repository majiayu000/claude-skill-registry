---
name: meson
description: 'Use when setting up a Meson project, meson setup/compile/test, wrap dependencies, cross-file cross-compiling, meson.build, or migrating from CMake/Autotools to Meson.'
---

# Meson

Meson project setup, build options, the wrap dependency system, and cross-compilation. Grounded against Meson 1.12.0; Meson drives Ninja as its backend.

## Contract

| Field | Bound contract |
|---|---|
| Trigger | The task sets up a Meson project, writes `meson.build` or `meson.options`, manages wrap dependencies, configures build options, cross-compiles with a cross file, or migrates from CMake or Autotools. |
| Authority | Reversible local: writes only `meson.build`, `meson.options`/`meson_options.txt`, cross and native files, `subprojects/`, and the build directory; rollback is version control plus deleting the build directory. No remote mutation. |
| Side effect | `meson compile` and `meson test` write local build outputs; `meson wrap install` downloads wrap files into `subprojects/`. |
| Done | `meson setup`, `meson compile`, and `meson test` run clean on the configured build directory, or the failing command is reported. |

## Inputs

- Project layout (required): sources and the root `meson.build` location.
- Meson version (required if not inferrable): run `meson --version`. `meson.options` needs Meson 1.1 or newer; older trees use `meson_options.txt`.
- Dependencies (optional): system libraries or wrap names from WrapDB.
- Cross target (optional): a cross file describing the host machine.

## Procedure

1. Configure the build directory. Done when: `meson setup builddir` succeeds.

```bash
meson setup builddir
meson setup builddir \
    --buildtype=release \
    --prefix=/usr/local \
    -Db_lto=true \
    -Db_sanitize=address

meson configure builddir -Dbuildtype=debug   # reconfigure in place
meson configure builddir                     # list all options
```

| `--buildtype` | Flags added |
|---|---|
| `debug` (default) | `-O0 -g` |
| `debugoptimized` | `-O2 -g` |
| `release` | `-O3 -DNDEBUG` |
| `minsize` | `-Os -DNDEBUG` |
| `plain` | none |
| `custom` | user-supplied flags only |

2. Build, test, and install. Done when: compile and test pass in the build directory.

```bash
meson compile -C builddir
meson test -C builddir
meson test -C builddir --verbose
meson test -C builddir -t 5            # 5x timeout multiplier
meson test -C builddir --suite unit    # one suite only
meson install -C builddir
meson install -C builddir --dry-run
```

3. Write `meson.build`. Done when: every target declares its sources, includes, and dependencies.

```python
project('myapp', 'c', 'cpp',
  version : '1.0.0',
  default_options : [
    'c_std=c23',
    'cpp_std=c++23',
    'warning_level=2',
  ]
)

glib_dep = dependency('glib-2.0', version : '>=2.68')
threads_dep = dependency('threads')
inc = include_directories('include')

mylib = static_library('mylib',
  sources : ['src/lib.c', 'src/util.c'],
  include_directories : inc,
)

executable('myapp',
  sources : ['src/main.c'],
  include_directories : inc,
  link_with : mylib,
  dependencies : [glib_dep, threads_dep],
  install : true,
)

test('basic', executable('test_basic',
  sources : ['tests/test_basic.c'],
  link_with : mylib,
))
```

4. Manage dependencies with wrap. Done when: `dependency()` resolves from the system or falls back to the wrap.

```bash
meson wrap search zlib
meson wrap install zlib
meson wrap list
meson wrap update
```

```python
# System first, wrap as fallback
zlib_dep = dependency('zlib', fallback : ['zlib', 'zlib_dep'])

# Force the wrap for reproducible builds
zlib_dep = dependency('zlib',
  fallback : ['zlib', 'zlib_dep'],
  default_options : ['default_library=static'],
)
```

5. Define project options in `meson.options` (Meson 1.1+) or `meson_options.txt`. Done when: `meson configure` lists the option and `get_option` reads it.

```python
option('with_tests', type : 'boolean', value : true,
  description : 'Build unit tests')

option('backend', type : 'combo',
  choices : ['opengl', 'vulkan', 'software'],
  value : 'opengl')

option('max_connections', type : 'integer',
  min : 1, max : 1024, value : 64)
```

```python
if get_option('with_tests')
  subdir('tests')
endif
```

6. Cross-compile with a cross file. Use `pkg-config` as the key name; `pkgconfig` is deprecated. Done when: `meson setup --cross-file` configures for the host machine.

```ini
# cross/arm-linux.ini
[binaries]
c = 'arm-linux-gnueabihf-gcc'
cpp = 'arm-linux-gnueabihf-g++'
ar = 'arm-linux-gnueabihf-ar'
strip = 'arm-linux-gnueabihf-strip'
pkg-config = 'arm-linux-gnueabihf-pkg-config'

[properties]
sys_root = '/path/to/sysroot'

[host_machine]
system = 'linux'
cpu_family = 'arm'
cpu = 'cortex-a9'
endian = 'little'
```

```bash
meson setup builddir-arm --cross-file cross/arm-linux.ini
meson compile -C builddir-arm
```

7. Migrate from CMake with this mapping. Done when: each CMake construct has its Meson equivalent.

| CMake | Meson |
|---|---|
| `add_executable` | `executable()` |
| `add_library` | `library()`, `static_library()`, `shared_library()` |
| `target_include_directories` | `include_directories` kwarg |
| `target_link_libraries` | `dependencies` and `link_with` kwargs |
| `find_package` | `dependency()` |
| `option()` | `option()` in `meson.options` |
| `add_subdirectory` | `subdir()` |
| `install(TARGETS ...)` | `install : true` kwarg |

For wrap file types, subproject patching, and compiler checks see `references/meson-wrap.md`.

## Failure and recovery

- `dependency()` fails and no wrap exists: run `meson wrap search <name>`; if WrapDB lacks it, vendor the source under `subprojects/` with its own `meson.build`.
- `meson setup` rejects an option: the option lives in `meson.options` or is a built-in `-D` name; run `meson configure builddir` to list valid names.
- Cross build picks up host libraries: the cross file needs `sys_root` under `[properties]` and correct `pkg-config` under `[binaries]`.
- Wrap download fails offline: pre-seed `subprojects/packagecache/` with the archive named in the wrap's `source_url`.
- Reconfigure does not take: some options are read once at setup; wipe the build directory with `meson setup --wipe builddir` or delete it and reconfigure.

## Output

A working `meson.build` with declared targets and dependencies, a configured build directory that compiles and tests clean, and for cross tasks a cross file verified by `meson setup --cross-file`.
