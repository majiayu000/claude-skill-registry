---
name: cmake
description: 'Use when writing CMakeLists.txt, out-of-source builds, target_link_libraries, target properties, find_package/FetchContent, toolchain files, CPack, CMake presets, or cmake configure errors.'
---

# CMake

Modern target-first CMake for C/C++ projects. Grounded against CMake 4.4.3; the examples floor at CMake 3.25 so the preset schema version 6 works.

## Contract

| Field | Bound contract |
|---|---|
| Trigger | The task writes or refactors `CMakeLists.txt`, configures out-of-source builds, selects generators, manages targets with `target_link_libraries`, integrates packages via `find_package` or `FetchContent`, enables sanitizers, writes toolchain files, sets up presets, or resolves a cmake configure error. |
| Authority | Reversible local: writes only `CMakeLists.txt`, `CMakePresets.json`, toolchain files, and the build directory; rollback is version control plus deleting the build directory. No remote mutation. |
| Side effect | `cmake --build` and `cmake --install` write local build outputs and install trees; `FetchContent` downloads declared dependencies. |
| Done | The project configures and builds with the requested options, or the failing command and its error are reported. |

## Inputs

- Project layout (required): sources, headers, and where the root `CMakeLists.txt` lives.
- CMake version (required if not inferrable): run `cmake --version`. Preset schema version 6 needs CMake 3.25 or newer.
- Dependencies (optional): system packages, FetchContent sources, or vendored trees.
- Target platform (optional): a cross-compilation target needs a toolchain file.

## Procedure

1. Apply modern CMake rules. Define targets, not variables. Use `target_*` commands with `PUBLIC`/`PRIVATE`/`INTERFACE` to control propagation. Never use `include_directories()` or `link_libraries()`; they are legacy global state. Done when: every property attaches to a target.

2. Write the minimal project. Done when: `cmake -S . -B build` configures cleanly.

```cmake
cmake_minimum_required(VERSION 3.25)
project(MyApp VERSION 1.0 LANGUAGES C CXX)

set(CMAKE_C_STANDARD 23)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)   # clang-tidy and IDEs read this

add_executable(myapp src/main.c src/utils.c)
target_include_directories(myapp PRIVATE include)
target_compile_options(myapp PRIVATE -Wall -Wextra)
```

3. Add libraries and link them. Done when: each library target carries its own include paths and the executable links against it.

```cmake
add_library(mylib STATIC lib/foo.c lib/bar.c)
target_include_directories(mylib
    PUBLIC  include    # consumers inherit this
    PRIVATE src        # only mylib sees this
)

add_library(myshared SHARED lib/foo.c)
set_target_properties(myshared PROPERTIES VERSION 1.0.0 SOVERSION 1)

target_link_libraries(myapp PRIVATE mylib)
```

4. Configure and build out of source. Done when: the build completes in a separate directory.

```bash
cmake -S . -B build -G Ninja
cmake --build build -- -j"$(nproc)"

cmake -S . -B build-debug   -DCMAKE_BUILD_TYPE=Debug
cmake -S . -B build-release -DCMAKE_BUILD_TYPE=Release
cmake --install build-release --prefix /usr/local
```

Build types: `Debug`, `Release`, `RelWithDebInfo`, `MinSizeRel`.

5. Integrate external dependencies. Prefer `find_package` for system libraries, `FetchContent` for source builds, `pkg_check_modules` as a fallback. Done when: the dependency resolves and links.

```cmake
find_package(OpenSSL REQUIRED)
find_package(Threads REQUIRED)
find_package(ZLIB REQUIRED)
target_link_libraries(myapp PRIVATE OpenSSL::SSL OpenSSL::Crypto Threads::Threads ZLIB::ZLIB)

include(FetchContent)
FetchContent_Declare(
    googletest
    GIT_REPOSITORY https://github.com/google/googletest.git
    GIT_TAG        v1.17.0
    GIT_SHALLOW    TRUE
)
FetchContent_MakeAvailable(googletest)

find_package(PkgConfig REQUIRED)
pkg_check_modules(LIBFOO REQUIRED libfoo>=1.2)
target_link_libraries(myapp PRIVATE ${LIBFOO_LIBRARIES})
target_include_directories(myapp PRIVATE ${LIBFOO_INCLUDE_DIRS})
```

6. Set per-configuration flags with generator expressions. Done when: each flag applies only to its intended configuration or compiler.

```cmake
target_compile_options(myapp PRIVATE
    $<$<CONFIG:Debug>:-g -Og -fsanitize=address>
    $<$<CONFIG:Release>:-O2 -DNDEBUG>
    $<$<CXX_COMPILER_ID:GNU>:-fanalyzer>
)
target_link_options(myapp PRIVATE
    $<$<CONFIG:Debug>:-fsanitize=address>
)
```

7. Gate sanitizers behind an option. Done when: `cmake -DENABLE_ASAN=ON` produces an instrumented build.

```cmake
option(ENABLE_ASAN "Enable AddressSanitizer" OFF)
if(ENABLE_ASAN)
    target_compile_options(myapp PRIVATE -fsanitize=address -fno-omit-frame-pointer -g -O1)
    target_link_options(myapp PRIVATE -fsanitize=address)
endif()
```

8. Write a toolchain file for cross-compilation. Done when: `cmake -DCMAKE_TOOLCHAIN_FILE=...` configures for the target.

```cmake
# toolchain-aarch64.cmake
set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR aarch64)
set(CMAKE_C_COMPILER   aarch64-linux-gnu-gcc)
set(CMAKE_CXX_COMPILER aarch64-linux-gnu-g++)
set(CMAKE_SYSROOT /opt/aarch64-sysroot)
set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
```

9. Capture common configurations in `CMakePresets.json`. Schema version 6 requires CMake 3.25 or newer. Done when: `cmake --preset <name>` configures and `cmake --build --preset <name>` builds.

```json
{
  "version": 6,
  "configurePresets": [
    {
      "name": "release",
      "generator": "Ninja",
      "binaryDir": "${sourceDir}/build/release",
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "Release",
        "CMAKE_EXPORT_COMPILE_COMMANDS": "ON"
      }
    },
    {
      "name": "debug",
      "generator": "Ninja",
      "binaryDir": "${sourceDir}/build/debug",
      "cacheVariables": { "CMAKE_BUILD_TYPE": "Debug", "ENABLE_ASAN": "ON" }
    }
  ],
  "buildPresets": [
    { "name": "release", "configurePreset": "release" },
    { "name": "debug",   "configurePreset": "debug" }
  ]
}
```

10. Diagnose configure errors against this table. Done when: the error maps to a cause and a fix.

| Error | Cause | Fix |
|---|---|---|
| `Could not find package Foo` | Package missing or wrong prefix | Install the dev package; set `CMAKE_PREFIX_PATH` |
| `No CMAKE_CXX_COMPILER` | No C++ compiler found | Install g++ or clang++; check `PATH` |
| `target_link_libraries called with wrong number of arguments` | Missing `PUBLIC`/`PRIVATE`/`INTERFACE` | Add the keyword |
| `Cannot find source file` | Typo or wrong relative path | Check the path relative to `CMakeLists.txt` |
| Compatibility error on old `cmake_minimum_required` | CMake 4 dropped compatibility with versions below 3.5 | Raise the floor to 3.25 |

For complete project templates see `references/templates.md`.

## Failure and recovery

- `find_package` fails: install the `-dev` package or set `CMAKE_PREFIX_PATH`; fall back to `FetchContent` when no system package exists.
- FetchContent fails offline: pre-seed `FETCHCONTENT_SOURCE_DIR_<NAME>` with a local copy.
- Generator expression error: check the expression name against `cmake --help-manual cmake-generator-expressions`.
- Preset rejected: confirm `cmake --version` meets the schema version's floor.
- Stale cache after option changes: delete the build directory or pass `-U` to clear a cache entry; do not edit `CMakeCache.txt` by hand.

## Output

A working `CMakeLists.txt` or build configuration, verified by a successful `cmake -S . -B build` and `cmake --build build`. For debugging tasks, the diagnosed error with its cause and applied fix.
