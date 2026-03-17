---
name: lang-c-library-dev
description: C library development patterns covering API design, header organization, memory management for libraries, ABI stability, build system integration, documentation with Doxygen, testing frameworks, and packaging. Use when creating C libraries, designing public APIs, managing build systems (CMake, Make, Meson), or distributing C packages. Extends lang-c-dev with library-specific tooling and patterns.
---

# C Library Development

C-specific patterns for library development. This skill extends `lang-c-dev` with library design patterns, build systems, ABI stability, and packaging practices.

## This Skill Extends

- `lang-c-dev` - Foundational C programming (type system, memory, pointers, preprocessor)

For general concepts like type system, pointers, memory management basics, and preprocessor directives, see the foundational skill first.

## This Skill Adds

- **Library design**: API design patterns, header organization, ABI stability
- **Build systems**: CMake, Make, Meson, Autotools, pkg-config
- **Documentation**: Doxygen, man pages, API documentation
- **Testing**: Unity, Check, CUnit, Criterion testing frameworks
- **Packaging**: Static/shared libraries, versioning, distribution

## This Skill Does NOT Cover

- General C programming - see `lang-c-dev`
- Advanced memory engineering - see `lang-c-memory-eng`
- POSIX APIs and system calls - see `lang-c-posix-dev`
- Systems programming patterns - see `lang-c-systems-eng`
- Embedded programming - see `lang-c-embedded-dev`

---

## Quick Reference

| Task | Command/Pattern |
|------|-----------------|
| Create static library | `ar rcs libname.a obj1.o obj2.o` |
| Create shared library | `gcc -shared -o libname.so obj1.o obj2.o` |
| Install library | `make install` or `cmake --install` |
| Generate docs | `doxygen Doxyfile` |
| Run tests | `make test` or `ctest` |
| Check ABI | `abidiff lib-v1.so lib-v2.so` |
| Package config | `pkg-config --cflags --libs mylib` |

---

## Library Design Patterns

### Opaque Pointer Pattern (PIMPL)

**Purpose**: Hide implementation details, maintain ABI stability

```c
// mylib.h (public API)
#ifndef MYLIB_H
#define MYLIB_H

#include <stddef.h>

// Opaque pointer - users cannot see internal structure
typedef struct mylib_context mylib_context_t;

// Constructor/destructor
mylib_context_t* mylib_create(void);
void mylib_destroy(mylib_context_t* ctx);

// Operations
int mylib_process(mylib_context_t* ctx, const char* input, char* output, size_t output_size);
int mylib_set_option(mylib_context_t* ctx, const char* key, const char* value);

#endif // MYLIB_H
```

```c
// mylib.c (implementation)
#include "mylib.h"
#include <stdlib.h>
#include <string.h>

// Full structure definition hidden from users
struct mylib_context {
    char* buffer;
    size_t buffer_size;
    int flags;
    void* internal_state;
};

mylib_context_t* mylib_create(void) {
    mylib_context_t* ctx = calloc(1, sizeof(*ctx));
    if (!ctx) return NULL;

    ctx->buffer_size = 4096;
    ctx->buffer = malloc(ctx->buffer_size);
    if (!ctx->buffer) {
        free(ctx);
        return NULL;
    }

    return ctx;
}

void mylib_destroy(mylib_context_t* ctx) {
    if (ctx) {
        free(ctx->buffer);
        free(ctx);
    }
}

int mylib_process(mylib_context_t* ctx, const char* input, char* output, size_t output_size) {
    if (!ctx || !input || !output) return -1;
    // Implementation...
    return 0;
}
```

### Error Handling Patterns

**Return codes with error context:**

```c
// error.h
#ifndef MYLIB_ERROR_H
#define MYLIB_ERROR_H

// Error codes
typedef enum {
    MYLIB_OK = 0,
    MYLIB_ERR_INVALID_ARGUMENT = -1,
    MYLIB_ERR_OUT_OF_MEMORY = -2,
    MYLIB_ERR_IO = -3,
    MYLIB_ERR_PARSE = -4,
} mylib_error_t;

// Get human-readable error message
const char* mylib_strerror(mylib_error_t error);

// Get last error for a context (thread-safe)
mylib_error_t mylib_last_error(mylib_context_t* ctx);
void mylib_clear_error(mylib_context_t* ctx);

#endif
```

```c
// error.c
#include "error.h"

const char* mylib_strerror(mylib_error_t error) {
    switch (error) {
        case MYLIB_OK: return "Success";
        case MYLIB_ERR_INVALID_ARGUMENT: return "Invalid argument";
        case MYLIB_ERR_OUT_OF_MEMORY: return "Out of memory";
        case MYLIB_ERR_IO: return "I/O error";
        case MYLIB_ERR_PARSE: return "Parse error";
        default: return "Unknown error";
    }
}
```

### Memory Management for Libraries

**Rule 1: Who allocates, who frees**

```c
// Pattern 1: Library allocates and frees
typedef struct mylib_result mylib_result_t;

mylib_result_t* mylib_compute(const char* input);
void mylib_result_free(mylib_result_t* result);

// Pattern 2: Caller allocates, library fills
int mylib_compute_inplace(const char* input, char* output, size_t* output_size);

// Pattern 3: Callback for custom allocation
typedef void* (*mylib_alloc_fn)(size_t size);
typedef void (*mylib_free_fn)(void* ptr);

void mylib_set_allocator(mylib_alloc_fn alloc, mylib_free_fn free);
```

**Pattern 2 example:**

```c
int mylib_get_info(mylib_context_t* ctx, char* buffer, size_t* buffer_size) {
    if (!ctx || !buffer_size) return MYLIB_ERR_INVALID_ARGUMENT;

    // Get required size
    size_t required = calculate_info_size(ctx);

    // If buffer is NULL or too small, return required size
    if (!buffer || *buffer_size < required) {
        *buffer_size = required;
        return MYLIB_ERR_INVALID_ARGUMENT;
    }

    // Fill buffer
    fill_info(ctx, buffer, *buffer_size);
    *buffer_size = required;
    return MYLIB_OK;
}
```

### Namespace Prefixing

**All public symbols must be prefixed:**

```c
// Good: All symbols prefixed with mylib_
mylib_context_t* mylib_create(void);
typedef enum { MYLIB_OK, MYLIB_ERR } mylib_error_t;
#define MYLIB_VERSION "1.0.0"

// Bad: Pollutes global namespace
context_t* create(void);
typedef enum { OK, ERR } error_t;
#define VERSION "1.0.0"
```

---

## Header File Organization

### Public vs Private Headers

```
include/
├── mylib/              # Public API
│   ├── mylib.h         # Main header
│   ├── error.h         # Error types
│   └── types.h         # Public types
src/
├── internal.h          # Private API
├── mylib.c
├── error.c
└── internal.c
```

### Header Best Practices

```c
// mylib.h
#ifndef MYLIB_H
#define MYLIB_H

// Include guards always (or #pragma once)

// System headers first
#include <stddef.h>
#include <stdint.h>

// Library version
#define MYLIB_VERSION_MAJOR 1
#define MYLIB_VERSION_MINOR 2
#define MYLIB_VERSION_PATCH 3

// Visibility macros
#ifdef _WIN32
    #ifdef MYLIB_BUILDING
        #define MYLIB_API __declspec(dllexport)
    #else
        #define MYLIB_API __declspec(dllimport)
    #endif
#else
    #define MYLIB_API __attribute__((visibility("default")))
#endif

// C++ compatibility
#ifdef __cplusplus
extern "C" {
#endif

// Forward declarations
typedef struct mylib_context mylib_context_t;

// API declarations
MYLIB_API mylib_context_t* mylib_create(void);
MYLIB_API void mylib_destroy(mylib_context_t* ctx);

#ifdef __cplusplus
}
#endif

#endif // MYLIB_H
```

### Feature Detection Headers

```c
// config.h (generated by build system)
#ifndef MYLIB_CONFIG_H
#define MYLIB_CONFIG_H

// Feature detection
#define MYLIB_HAVE_THREADS 1
#define MYLIB_HAVE_ZLIB 1
// #undef MYLIB_HAVE_OPENSSL

// Platform detection
#ifdef _WIN32
    #define MYLIB_PLATFORM_WINDOWS
#elif defined(__APPLE__)
    #define MYLIB_PLATFORM_MACOS
#elif defined(__linux__)
    #define MYLIB_PLATFORM_LINUX
#endif

#endif
```

---

## ABI Stability

### Versioning Strategy

**Semantic Versioning for ABI:**
- Major: Breaking ABI changes
- Minor: New features, ABI compatible
- Patch: Bug fixes, ABI compatible

### ABI-Safe Changes

**Safe (ABI compatible):**
- Adding new functions
- Adding new struct members at the end (if opaque)
- Adding new enum values (if used with non_exhaustive pattern)
- Increasing struct size (if opaque)

**Unsafe (ABI breaking):**
- Removing functions
- Changing function signatures
- Reordering struct members
- Changing struct sizes (if exposed)
- Changing enum underlying type

### Symbol Versioning

```c
// Use symbol versioning for evolving APIs
__asm__(".symver mylib_open_v1, mylib_open@MYLIB_1.0");
__asm__(".symver mylib_open_v2, mylib_open@@MYLIB_2.0");

// Old version
int mylib_open_v1(const char* path);

// New version (default)
int mylib_open_v2(const char* path, int flags);
```

### Version Script (Linux)

```
# mylib.map
MYLIB_1.0 {
    global:
        mylib_create;
        mylib_destroy;
        mylib_process;
    local:
        *;
};

MYLIB_2.0 {
    global:
        mylib_process_v2;
} MYLIB_1.0;
```

```bash
# Link with version script
gcc -shared -Wl,--version-script=mylib.map -o libmylib.so *.o
```

---

## Build Systems

### CMake (Modern Approach)

```cmake
# CMakeLists.txt
cmake_minimum_required(VERSION 3.15)
project(mylib VERSION 1.2.3 LANGUAGES C)

# Options
option(BUILD_SHARED_LIBS "Build shared libraries" ON)
option(MYLIB_BUILD_TESTS "Build tests" ON)
option(MYLIB_BUILD_DOCS "Build documentation" OFF)

# Library target
add_library(mylib
    src/mylib.c
    src/error.c
    src/internal.c
)

# Include directories
target_include_directories(mylib
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        $<INSTALL_INTERFACE:include>
    PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/src
)

# Compiler features
target_compile_features(mylib PRIVATE c_std_99)
target_compile_options(mylib PRIVATE
    $<$<C_COMPILER_ID:GNU,Clang>:-Wall -Wextra -pedantic>
    $<$<C_COMPILER_ID:MSVC>:/W4>
)

# Symbol visibility
set_target_properties(mylib PROPERTIES
    C_VISIBILITY_PRESET hidden
    VERSION ${PROJECT_VERSION}
    SOVERSION ${PROJECT_VERSION_MAJOR}
)

# Dependencies
find_package(ZLIB)
if(ZLIB_FOUND)
    target_link_libraries(mylib PRIVATE ZLIB::ZLIB)
    target_compile_definitions(mylib PRIVATE MYLIB_HAVE_ZLIB)
endif()

# Installation
include(GNUInstallDirs)
install(TARGETS mylib
    EXPORT mylibTargets
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)

install(DIRECTORY include/mylib
    DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
)

# Export targets
install(EXPORT mylibTargets
    FILE mylibTargets.cmake
    NAMESPACE mylib::
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/mylib
)

# Generate config files
include(CMakePackageConfigHelpers)
write_basic_package_version_file(
    "${CMAKE_CURRENT_BINARY_DIR}/mylibConfigVersion.cmake"
    VERSION ${PROJECT_VERSION}
    COMPATIBILITY SameMajorVersion
)

configure_package_config_file(
    "${CMAKE_CURRENT_SOURCE_DIR}/cmake/mylibConfig.cmake.in"
    "${CMAKE_CURRENT_BINARY_DIR}/mylibConfig.cmake"
    INSTALL_DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/mylib
)

install(FILES
    "${CMAKE_CURRENT_BINARY_DIR}/mylibConfig.cmake"
    "${CMAKE_CURRENT_BINARY_DIR}/mylibConfigVersion.cmake"
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/mylib
)

# Testing
if(MYLIB_BUILD_TESTS)
    enable_testing()
    add_subdirectory(tests)
endif()
```

### Makefile (Traditional Approach)

```makefile
# Makefile
PREFIX ?= /usr/local
LIBDIR ?= $(PREFIX)/lib
INCLUDEDIR ?= $(PREFIX)/include

CC = gcc
CFLAGS = -Wall -Wextra -std=c99 -O2 -fPIC
LDFLAGS = -shared

# Library name and version
LIB_NAME = mylib
LIB_VERSION = 1.2.3
LIB_SOVERSION = 1

# Source files
SRCS = src/mylib.c src/error.c src/internal.c
OBJS = $(SRCS:.c=.o)
HEADERS = include/mylib/mylib.h include/mylib/error.h

# Targets
STATIC_LIB = lib$(LIB_NAME).a
SHARED_LIB = lib$(LIB_NAME).so.$(LIB_VERSION)
SHARED_LIB_LINK = lib$(LIB_NAME).so
SHARED_LIB_SONAME = lib$(LIB_NAME).so.$(LIB_SOVERSION)

.PHONY: all clean install uninstall test

all: $(STATIC_LIB) $(SHARED_LIB)

# Static library
$(STATIC_LIB): $(OBJS)
	ar rcs $@ $^

# Shared library
$(SHARED_LIB): $(OBJS)
	$(CC) $(LDFLAGS) -Wl,-soname,$(SHARED_LIB_SONAME) -o $@ $^
	ln -sf $(SHARED_LIB) $(SHARED_LIB_SONAME)
	ln -sf $(SHARED_LIB_SONAME) $(SHARED_LIB_LINK)

# Object files
%.o: %.c
	$(CC) $(CFLAGS) -Iinclude -c -o $@ $<

# Install
install: all
	install -d $(DESTDIR)$(LIBDIR)
	install -m 644 $(STATIC_LIB) $(DESTDIR)$(LIBDIR)/
	install -m 755 $(SHARED_LIB) $(DESTDIR)$(LIBDIR)/
	ln -sf $(SHARED_LIB) $(DESTDIR)$(LIBDIR)/$(SHARED_LIB_SONAME)
	ln -sf $(SHARED_LIB_SONAME) $(DESTDIR)$(LIBDIR)/$(SHARED_LIB_LINK)
	install -d $(DESTDIR)$(INCLUDEDIR)/mylib
	install -m 644 $(HEADERS) $(DESTDIR)$(INCLUDEDIR)/mylib/
	ldconfig -n $(DESTDIR)$(LIBDIR)

# Uninstall
uninstall:
	rm -f $(DESTDIR)$(LIBDIR)/$(STATIC_LIB)
	rm -f $(DESTDIR)$(LIBDIR)/$(SHARED_LIB)*
	rm -rf $(DESTDIR)$(INCLUDEDIR)/mylib

# Clean
clean:
	rm -f $(OBJS) $(STATIC_LIB) $(SHARED_LIB)*

# Tests
test:
	$(MAKE) -C tests
```

### Meson (Modern Alternative)

```meson
# meson.build
project('mylib', 'c',
  version: '1.2.3',
  default_options: ['c_std=c99', 'warning_level=3']
)

# Dependencies
zlib_dep = dependency('zlib', required: false)

# Configuration
conf_data = configuration_data()
conf_data.set('MYLIB_VERSION', meson.project_version())
conf_data.set('MYLIB_HAVE_ZLIB', zlib_dep.found())

configure_file(
  input: 'config.h.in',
  output: 'config.h',
  configuration: conf_data
)

# Library
mylib_sources = files(
  'src/mylib.c',
  'src/error.c',
  'src/internal.c'
)

mylib_inc = include_directories('include')

mylib = library('mylib',
  mylib_sources,
  include_directories: mylib_inc,
  dependencies: zlib_dep,
  version: meson.project_version(),
  soversion: '1',
  install: true
)

# Install headers
install_headers(
  'include/mylib/mylib.h',
  'include/mylib/error.h',
  subdir: 'mylib'
)

# pkg-config
pkg = import('pkgconfig')
pkg.generate(mylib,
  description: 'My awesome C library',
  subdirs: 'mylib'
)

# Testing
if get_option('build_tests')
  subdir('tests')
endif
```

### pkg-config File

```
# mylib.pc.in
prefix=@PREFIX@
exec_prefix=${prefix}
libdir=${exec_prefix}/lib
includedir=${prefix}/include

Name: mylib
Description: My awesome C library
Version: @VERSION@
Libs: -L${libdir} -lmylib
Cflags: -I${includedir}
Requires: zlib
```

---

## Documentation with Doxygen

### Doxygen Configuration

```doxyfile
# Doxyfile
PROJECT_NAME           = "mylib"
PROJECT_NUMBER         = 1.2.3
OUTPUT_DIRECTORY       = docs
GENERATE_HTML          = YES
GENERATE_LATEX         = NO
EXTRACT_ALL            = YES
EXTRACT_PRIVATE        = NO
EXTRACT_STATIC         = NO
INPUT                  = include/mylib
RECURSIVE              = YES
USE_MDFILE_AS_MAINPAGE = README.md
```

### Documentation Patterns

```c
/**
 * @file mylib.h
 * @brief Main library interface
 * @author Your Name
 */

/**
 * @brief Context object for library operations
 *
 * This is an opaque type. Users should not access its members directly.
 * Use the provided API functions to interact with it.
 */
typedef struct mylib_context mylib_context_t;

/**
 * @brief Create a new library context
 *
 * @return Pointer to new context, or NULL on allocation failure
 * @note The returned context must be freed with mylib_destroy()
 * @see mylib_destroy()
 */
MYLIB_API mylib_context_t* mylib_create(void);

/**
 * @brief Destroy a library context
 *
 * @param ctx Context to destroy (may be NULL)
 * @note Safe to call with NULL pointer
 * @warning Do not use the context after calling this function
 */
MYLIB_API void mylib_destroy(mylib_context_t* ctx);

/**
 * @brief Process input data
 *
 * @param ctx Library context
 * @param input Input string (must be null-terminated)
 * @param output Output buffer
 * @param output_size Size of output buffer
 * @return 0 on success, negative error code on failure
 * @retval MYLIB_OK Success
 * @retval MYLIB_ERR_INVALID_ARGUMENT Invalid parameter
 * @retval MYLIB_ERR_OUT_OF_MEMORY Allocation failed
 *
 * @code{.c}
 * mylib_context_t* ctx = mylib_create();
 * char output[1024];
 * int result = mylib_process(ctx, "input", output, sizeof(output));
 * if (result == MYLIB_OK) {
 *     printf("Output: %s\n", output);
 * }
 * mylib_destroy(ctx);
 * @endcode
 */
MYLIB_API int mylib_process(mylib_context_t* ctx, const char* input,
                            char* output, size_t output_size);
```

---

## Testing Frameworks

### Unity Test Framework

```c
// test_mylib.c
#include "unity.h"
#include "mylib/mylib.h"

void setUp(void) {
    // Run before each test
}

void tearDown(void) {
    // Run after each test
}

void test_create_destroy(void) {
    mylib_context_t* ctx = mylib_create();
    TEST_ASSERT_NOT_NULL(ctx);
    mylib_destroy(ctx);
}

void test_process_valid_input(void) {
    mylib_context_t* ctx = mylib_create();
    char output[1024];

    int result = mylib_process(ctx, "test input", output, sizeof(output));
    TEST_ASSERT_EQUAL(MYLIB_OK, result);
    TEST_ASSERT_EQUAL_STRING("expected output", output);

    mylib_destroy(ctx);
}

void test_process_invalid_argument(void) {
    int result = mylib_process(NULL, "input", NULL, 0);
    TEST_ASSERT_EQUAL(MYLIB_ERR_INVALID_ARGUMENT, result);
}

int main(void) {
    UNITY_BEGIN();
    RUN_TEST(test_create_destroy);
    RUN_TEST(test_process_valid_input);
    RUN_TEST(test_process_invalid_argument);
    return UNITY_END();
}
```

### Check Framework

```c
// test_check.c
#include <check.h>
#include "mylib/mylib.h"

START_TEST(test_create)
{
    mylib_context_t* ctx = mylib_create();
    ck_assert_ptr_nonnull(ctx);
    mylib_destroy(ctx);
}
END_TEST

START_TEST(test_process)
{
    mylib_context_t* ctx = mylib_create();
    char output[1024];

    int result = mylib_process(ctx, "input", output, sizeof(output));
    ck_assert_int_eq(result, MYLIB_OK);

    mylib_destroy(ctx);
}
END_TEST

Suite* mylib_suite(void) {
    Suite* s = suite_create("mylib");
    TCase* tc_core = tcase_create("Core");

    tcase_add_test(tc_core, test_create);
    tcase_add_test(tc_core, test_process);
    suite_add_tcase(s, tc_core);

    return s;
}

int main(void) {
    int number_failed;
    Suite* s = mylib_suite();
    SRunner* sr = srunner_create(s);

    srunner_run_all(sr, CK_NORMAL);
    number_failed = srunner_ntests_failed(sr);
    srunner_free(sr);

    return (number_failed == 0) ? 0 : 1;
}
```

### Criterion (Modern Framework)

```c
// test_criterion.c
#include <criterion/criterion.h>
#include "mylib/mylib.h"

Test(mylib, create_destroy) {
    mylib_context_t* ctx = mylib_create();
    cr_assert_not_null(ctx);
    mylib_destroy(ctx);
}

Test(mylib, process_valid) {
    mylib_context_t* ctx = mylib_create();
    char output[1024];

    int result = mylib_process(ctx, "input", output, sizeof(output));
    cr_assert_eq(result, MYLIB_OK);

    mylib_destroy(ctx);
}

Test(mylib, process_null_context) {
    char output[1024];
    int result = mylib_process(NULL, "input", output, sizeof(output));
    cr_assert_eq(result, MYLIB_ERR_INVALID_ARGUMENT);
}
```

---

## Packaging and Distribution

### Static vs Shared Libraries

**Static Library (.a):**
```bash
# Compile object files
gcc -c -I include src/mylib.c -o mylib.o
gcc -c -I include src/error.c -o error.o

# Create archive
ar rcs libmylib.a mylib.o error.o

# Link with static library
gcc main.c -L. -lmylib -o program
```

**Shared Library (.so / .dylib / .dll):**
```bash
# Compile with position-independent code
gcc -fPIC -c -I include src/mylib.c -o mylib.o
gcc -fPIC -c -I include src/error.c -o error.o

# Create shared library (Linux)
gcc -shared -Wl,-soname,libmylib.so.1 -o libmylib.so.1.2.3 mylib.o error.o

# Create symlinks
ln -s libmylib.so.1.2.3 libmylib.so.1
ln -s libmylib.so.1 libmylib.so

# Link with shared library
gcc main.c -L. -lmylib -o program
```

### Versioning Scheme

**Linux:**
- `libmylib.so.1.2.3` - Real file with full version
- `libmylib.so.1` - Symlink (SONAME) for ABI compatibility
- `libmylib.so` - Symlink for linker

**macOS:**
- `libmylib.1.2.3.dylib` - Real file
- `libmylib.1.dylib` - Symlink
- `libmylib.dylib` - Symlink

### Distribution Packages

**Debian/Ubuntu (.deb):**
```bash
# Structure
mylib_1.2.3/
├── debian/
│   ├── control
│   ├── rules
│   ├── changelog
│   └── copyright
├── include/
├── src/
└── CMakeLists.txt

# Build package
dpkg-buildpackage -us -uc
```

**Red Hat/Fedora (.rpm):**
```spec
# mylib.spec
Name:           mylib
Version:        1.2.3
Release:        1%{?dist}
Summary:        My awesome C library

License:        MIT
URL:            https://github.com/username/mylib
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  gcc, cmake, zlib-devel
Requires:       zlib

%description
My awesome C library for doing awesome things.

%prep
%setup -q

%build
%cmake
%cmake_build

%install
%cmake_install

%files
%license LICENSE
%doc README.md
%{_libdir}/libmylib.so.*
%{_libdir}/libmylib.a
%{_includedir}/mylib/

%changelog
* Mon Jan 01 2024 Your Name <email@example.com> - 1.2.3-1
- Initial package
```

---

## Best Practices Checklist

- [ ] All public symbols have library prefix (`mylib_`)
- [ ] Header files have include guards or `#pragma once`
- [ ] C++ compatibility with `extern "C"`
- [ ] Symbol visibility controlled (hidden by default)
- [ ] Opaque pointers for implementation hiding
- [ ] Clear memory ownership rules
- [ ] Consistent error handling pattern
- [ ] Thread-safety documented
- [ ] ABI versioning strategy
- [ ] Comprehensive API documentation
- [ ] Unit tests with good coverage
- [ ] pkg-config file provided
- [ ] CMake config files generated
- [ ] Build works on multiple platforms
- [ ] No warnings with `-Wall -Wextra -pedantic`

---

## Common Pitfalls

### 1. Exposing Internal Types

```c
// Bad: Exposes internal implementation
typedef struct {
    char* buffer;
    size_t size;
} mylib_context_t;

// Good: Opaque pointer
typedef struct mylib_context mylib_context_t;
```

### 2. No Namespace Prefixing

```c
// Bad: Pollutes global namespace
int init(void);
void cleanup(void);

// Good: Prefixed
int mylib_init(void);
void mylib_cleanup(void);
```

### 3. Unclear Memory Ownership

```c
// Bad: Who frees the result?
char* mylib_process(const char* input);

// Good: Clear ownership
char* mylib_process(const char* input);  // Caller frees
void mylib_result_free(char* result);
```

### 4. Breaking ABI

```c
// v1.0.0
int mylib_func(int a);

// v1.1.0 - WRONG! ABI break
int mylib_func(int a, int b);

// v1.1.0 - Correct: Add new function
int mylib_func(int a);
int mylib_func_ex(int a, int b);
```

---

## References

- `lang-c-dev` - Foundational C programming
- `lang-c-memory-eng` - Advanced memory patterns
- [CMake Documentation](https://cmake.org/documentation/)
- [Meson Build System](https://mesonbuild.com/)
- [Doxygen Manual](https://www.doxygen.nl/manual/)
- [Unity Test Framework](https://github.com/ThrowTheSwitch/Unity)
- [Check Framework](https://libcheck.github.io/check/)
- [Criterion](https://github.com/Snaipe/Criterion)
- [pkg-config Guide](https://people.freedesktop.org/~dbn/pkg-config-guide.html)
