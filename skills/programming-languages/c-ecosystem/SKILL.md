---
name: C Ecosystem
description: This skill should be used when working with C projects, "C11", "C17", "C23", "Makefile", "gcc", "clang", "valgrind", "getopt", or C language patterns. Provides comprehensive Modern C (C11-C23) patterns, memory management, and CLI development best practices.
---

<purpose>
Provide comprehensive patterns for Modern C language (C11/C17/C23), memory management, toolchain configuration, and CLI tool development.
</purpose>

<c_language>
  <standards_evolution>
    <standard name="C11">
      <description>ISO/IEC 9899:2011 - Major modernization with threading and type-generic features</description>
      <features>
        <feature name="_Generic">Type-generic selection for polymorphic macros</feature>
        <feature name="_Atomic">Atomic types and operations for lock-free programming</feature>
        <feature name="_Thread_local">Thread-local storage duration</feature>
        <feature name="_Static_assert">Compile-time assertions</feature>
        <feature name="_Alignas">Alignment specifier for variables and types</feature>
        <feature name="_Alignof">Query alignment requirements</feature>
        <feature name="_Noreturn">Function that does not return</feature>
        <feature name="anonymous_structs_unions">Unnamed struct/union members</feature>
      </features>
    </standard>

    <standard name="C17">
      <description>ISO/IEC 9899:2018 - Bug fix release with no new features</description>
      <changes>
        <change>__STDC_VERSION__ updated to 201710L</change>
        <change>Defect reports resolved</change>
        <change>ATOMIC_VAR_INIT deprecated</change>
      </changes>
    </standard>

    <standard name="C23">
      <description>ISO/IEC 9899:2024 - Significant modernization with C++ alignment</description>
      <features>
        <feature name="nullptr">Null pointer constant with nullptr_t type</feature>
        <feature name="typeof">Type inference operator</feature>
        <feature name="constexpr">Compile-time constant objects</feature>
        <feature name="auto">Type inference for variables</feature>
        <feature name="binary_literals">0b prefix for binary literals</feature>
        <feature name="digit_separators">Single quote separator in numeric literals</feature>
        <feature name="attributes">[[nodiscard]], [[maybe_unused]], [[deprecated]], [[fallthrough]], [[noreturn]]</feature>
        <feature name="bool_true_false">bool, true, false as keywords</feature>
        <feature name="embed">embed directive for binary resource inclusion</feature>
        <feature name="static_assert">Single argument form</feature>
      </features>
    </standard>
  </standards_evolution>

  <type_system>
    <concept name="integer_types">
      <description>Fixed-width integer types from stdint.h</description>
      <types>
        <type name="int8_t, int16_t, int32_t, int64_t">Exact-width signed integers</type>
        <type name="uint8_t, uint16_t, uint32_t, uint64_t">Exact-width unsigned integers</type>
        <type name="intptr_t, uintptr_t">Pointer-sized integers</type>
        <type name="size_t">Unsigned size type for memory operations</type>
        <type name="ptrdiff_t">Signed pointer difference type</type>
      </types>
      <example>
#include &lt;stdint.h&gt;
#include &lt;stddef.h&gt;

uint32_t compute_hash(const uint8_t \*data, size_t len);
      </example>
    </concept>

    <concept name="type_generic_selection">
      <description>_Generic for type-based dispatch (C11)</description>
      <example>
#define print_value(x) _Generic((x), \
int: print_int, \
double: print_double, \
char *: print_string, \
default: print_unknown \
)(x)
      </example>
      <use_case>Implement type-safe generic interfaces without void pointers</use_case>
    </concept>

    <concept name="compound_literals">
      <description>Anonymous compound literals for in-place struct/array creation</description>
      <example>
struct point { int x, y; };
void draw(struct point p);

draw((struct point){.x = 10, .y = 20});

int \*arr = (int[]){1, 2, 3, 4, 5};
      </example>
    </concept>

    <concept name="designated_initializers">
      <description>Named field initialization for structs and arrays</description>
      <example>
struct config {
int timeout;
bool verbose;
const char *name;
};

struct config cfg = {
.name = "myapp",
.timeout = 30,
.verbose = true,
};
      </example>
    </concept>
  </type_system>

  <concurrency>
    <decision_tree name="when_to_use">
      <question>Do you need thread-safe operations?</question>
      <if_yes>Use _Atomic for simple counters, pthreads for complex synchronization</if_yes>
      <if_no>Single-threaded sequential execution</if_no>
    </decision_tree>

    <concept name="atomics">
      <description>Lock-free atomic operations (C11)</description>
      <example>
#include &lt;stdatomic.h&gt;

\_Atomic int counter = 0;

void increment(void) {
atomic_fetch_add(&amp;counter, 1);
}

int get_count(void) {
return atomic_load(&amp;counter);
}
      </example>
    </concept>

    <concept name="thread_local">
      <description>Thread-local storage (C11)</description>
      <example>
#include &lt;threads.h&gt;

\_Thread_local int errno_local;
      </example>
    </concept>
  </concurrency>

  <undefined_behavior>
    <description>Common undefined behavior to avoid in C</description>
    <categories>
      <category name="memory">Null pointer dereference, use-after-free, buffer overflow, double-free</category>
      <category name="arithmetic">Signed integer overflow, division by zero, shift beyond type width</category>
      <category name="aliasing">Strict aliasing violations, type punning without union</category>
      <category name="sequence">Modifying variable twice between sequence points</category>
    </categories>
    <mitigation>Use sanitizers (ASan, UBSan) during development to detect UB</mitigation>
  </undefined_behavior>

  <anti_patterns>
    <avoid name="void_pointer_abuse">
      <description>Overusing void\* for generic programming</description>
      <instead>Use \_Generic macros or code generation</instead>
    </avoid>

    <avoid name="magic_numbers">
      <description>Hardcoded numeric values without explanation</description>
      <instead>Use named constants with define or enum</instead>
    </avoid>

    <avoid name="strcpy_strcat">
      <description>Using unbounded string functions</description>
      <instead>Use snprintf for strings. Note: strncpy does NOT null-terminate if source exceeds size</instead>
    </avoid>

    <avoid name="sprintf">
      <description>Using sprintf without bounds checking</description>
      <instead>Use snprintf with explicit buffer size</instead>
    </avoid>

    <avoid name="gets">
      <description>Using gets() which has no bounds checking</description>
      <instead>Use fgets() with explicit buffer size</instead>
    </avoid>

    <avoid name="scanf_unbounded">
      <description>Using scanf with unbounded %s format</description>
      <instead>Use %Ns with explicit width or fgets followed by sscanf</instead>
    </avoid>

    <avoid name="unchecked_malloc">
      <description>Not checking malloc return value</description>
      <instead>Always check for NULL after allocation</instead>
    </avoid>

    <avoid name="format_string_vuln">
      <description>Using user input as format string (printf(user_input))</description>
      <instead>Always use printf("%s", user_input) or puts()</instead>
    </avoid>
  </anti_patterns>
</c_language>

<memory_management>
  <decision_tree name="allocation_strategy">
    <question>What is the lifetime and access pattern of the memory?</question>
    <branch condition="Short-lived, function-scoped">Use stack allocation or VLA (with size limit)</branch>
    <branch condition="Long-lived, single owner">Use malloc/free with clear ownership</branch>
    <branch condition="Many small allocations">Use arena allocator</branch>
    <branch condition="Fixed-size objects">Use pool allocator</branch>
  </decision_tree>

  <pattern name="basic_allocation">
    <description>Standard malloc/calloc/realloc/free patterns</description>
    <example>
#include &lt;stdlib.h&gt;
#include &lt;string.h&gt;

char *duplicate_string(const char *src) {
if (!src) return NULL;

size_t len = strlen(src) + 1;
char *dst = malloc(len);
if (!dst) return NULL;

memcpy(dst, src, len);
return dst;

}
    </example>
    <rules priority="critical">
      <rule>Always check malloc/calloc/realloc return value for NULL</rule>
      <rule>Use calloc for zero-initialized memory</rule>
      <rule>After realloc, use the returned pointer (original may be invalid)</rule>
      <rule>Set pointer to NULL after free to prevent use-after-free</rule>
    </rules>
  </pattern>

  <pattern name="arena_allocator">
    <description>Bulk allocation with single-point deallocation</description>
    <example>
typedef struct {
char *base;
size_t size;
size_t offset;
} Arena;

Arena arena_create(size_t size) {
Arena a = {0};
a.base = malloc(size);
if (a.base) a.size = size;
return a;
}

void *arena_alloc(Arena *a, size_t bytes) {
size_t aligned = (bytes + 7) &amp; ~7; // 8-byte alignment
if (a-&gt;offset + aligned &gt; a-&gt;size) return NULL;
void \*ptr = a-&gt;base + a-&gt;offset;
a-&gt;offset += aligned;
return ptr;
}

void arena_reset(Arena \*a) {
a-&gt;offset = 0;
}

void arena_destroy(Arena *a) {
free(a-&gt;base);
*a = (Arena){0};
}
    </example>
    <use_case>Parsing, compilers, request handling - many allocations freed together</use_case>
  </pattern>

  <pattern name="pool_allocator">
    <description>Fixed-size object allocation with O(1) alloc/free</description>
    <example>
typedef struct PoolBlock {
struct PoolBlock *next;
} PoolBlock;

typedef struct {
PoolBlock *free_list;
char *memory;
size_t object_size;
size_t capacity;
} Pool;

Pool pool_create(size_t object_size, size_t count) {
Pool p = {0};
size_t size = object_size &gt; sizeof(PoolBlock) ? object_size : sizeof(PoolBlock);
p.memory = malloc(size \* count);
if (!p.memory) return p;

p.object_size = size;
p.capacity = count;

// Build free list
for (size_t i = 0; i &lt; count; i++) {
PoolBlock *block = (PoolBlock *)(p.memory + i * size);
block-&gt;next = p.free_list;
p.free_list = block;
}
return p;

}

void *pool_alloc(Pool *p) {
if (!p-&gt;free_list) return NULL;
PoolBlock \*block = p-&gt;free_list;
p-&gt;free_list = block-&gt;next;
return block;
}

void pool_free(Pool *p, void *ptr) {
PoolBlock \*block = ptr;
block-&gt;next = p-&gt;free_list;
p-&gt;free_list = block;
}

void pool_destroy(Pool *p) {
free(p-&gt;memory);
*p = (Pool){0};
}
    </example>
    <use_case>Game entities, network connections, fixed-size records</use_case>
  </pattern>

  <pattern name="goto_cleanup">
    <description>Resource cleanup with goto for error handling</description>
    <example>
int process_file(const char *path) {
int result = -1;
FILE *fp = NULL;
char *buffer = NULL;

fp = fopen(path, "r");
if (!fp) goto cleanup;

buffer = malloc(BUFFER_SIZE);
if (!buffer) goto cleanup;

// ... process file ...

result = 0;  // Success

cleanup:
free(buffer);
if (fp) fclose(fp);
return result;
}
    </example>
    <note>Single cleanup point prevents resource leaks on error paths</note>
  </pattern>

  <anti_patterns>
    <avoid name="memory_leak">
      <description>Forgetting to free allocated memory</description>
      <instead>Use Valgrind/ASan, establish clear ownership rules</instead>
    </avoid>

    <avoid name="double_free">
      <description>Freeing the same pointer twice</description>
      <instead>Set pointer to NULL after free, use ownership tracking</instead>
    </avoid>

    <avoid name="use_after_free">
      <description>Accessing memory after it has been freed</description>
      <instead>Clear pointers after free, use ASan for detection</instead>
    </avoid>

    <avoid name="buffer_overflow">
      <description>Writing beyond allocated buffer bounds</description>
      <instead>Always track buffer sizes, use bounded functions</instead>
    </avoid>
  </anti_patterns>
</memory_management>

<cli_development>
  <decision_tree name="argument_parsing">
    <question>What complexity of argument parsing is needed?</question>
    <branch condition="Simple flags and options">Use getopt()</branch>
    <branch condition="Long options needed">Use getopt_long()</branch>
    <branch condition="GNU-style with help generation">Use argp (GNU extension)</branch>
  </decision_tree>

  <pattern name="getopt">
    <description>POSIX standard option parsing</description>
    <example>
#include &lt;unistd.h&gt;
#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;

int main(int argc, char *argv[]) {
int verbose = 0;
const char *output = NULL;
int opt;

while ((opt = getopt(argc, argv, "vo:h")) != -1) {
switch (opt) {
case 'v':
verbose = 1;
break;
case 'o':
output = optarg;
break;
case 'h':
printf("Usage: %s [-v] [-o output] [file...]\n", argv[0]);
return 0;
default:
fprintf(stderr, "Usage: %s [-v] [-o output] [file...]\n", argv[0]);
return 1;
}
}

// Remaining arguments: argv[optind] to argv[argc-1]
for (int i = optind; i &lt; argc; i++) {
printf("Processing: %s\n", argv[i]);
}

return 0;

}
    </example>
  </pattern>

  <pattern name="getopt_long">
    <description>GNU extension for long options</description>
    <example>
#include &lt;getopt.h&gt;
#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;

static struct option long_options[] = {
{"verbose", no_argument, NULL, 'v'},
{"output", required_argument, NULL, 'o'},
{"help", no_argument, NULL, 'h'},
{NULL, 0, NULL, 0 }
};

int main(int argc, char *argv[]) {
int verbose = 0;
const char *output = NULL;
int opt;

while ((opt = getopt_long(argc, argv, "vo:h", long_options, NULL)) != -1) {
switch (opt) {
case 'v': verbose = 1; break;
case 'o': output = optarg; break;
case 'h':
printf("Usage: %s [--verbose] [--output FILE] [file...]\n", argv[0]);
return 0;
default:
return 1;
}
}

return 0;

}
    </example>
  </pattern>

  <pattern name="exit_codes">
    <description>Standard exit code conventions</description>
    <codes>
      <code value="0" name="EXIT_SUCCESS">Successful execution</code>
      <code value="1" name="EXIT_FAILURE">General error</code>
      <code value="2">Command line usage error</code>
      <code value="126">Command found but not executable</code>
      <code value="127">Command not found</code>
      <code value="128+N">Terminated by signal N</code>
    </codes>
    <example>
#include &lt;stdlib.h&gt;
#include &lt;sysexits.h&gt;  // EX_USAGE, EX_DATAERR, etc.

int main(int argc, char \*argv[]) {
if (argc &lt; 2) {
fprintf(stderr, "Usage: %s &lt;file&gt;\n", argv[0]);
return EX_USAGE; // 64
}

FILE *fp = fopen(argv[1], "r");
if (!fp) {
perror(argv[1]);
return EX_NOINPUT;  // 66
}

// ...

return EXIT_SUCCESS;

}
    </example>
  </pattern>

  <pattern name="signal_handling">
    <description>Graceful signal handling for clean shutdown</description>
    <example>
#include &lt;signal.h&gt;
#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;
#include &lt;stdatomic.h&gt;

static atomic_int running = 1;

static void handle_signal(int sig) {
(void)sig;
running = 0;
}

int main(void) {
struct sigaction sa = {0};
sa.sa_handler = handle_signal;
sigemptyset(&amp;sa.sa_mask);
sa.sa_flags = 0;

sigaction(SIGINT, &amp;sa, NULL);
sigaction(SIGTERM, &amp;sa, NULL);

while (running) {
// Main loop work
}

printf("Shutting down gracefully...\n");
return 0;

}
    </example>
    <rules priority="critical">
      <rule>Use sigaction() instead of signal() for portability</rule>
      <rule>Keep signal handlers minimal - set flag only</rule>
      <rule>Use volatile sig_atomic_t or atomic types for signal flags</rule>
    </rules>
  </pattern>

  <pattern name="error_reporting">
    <description>Consistent error message format</description>
    <example>
#include &lt;errno.h&gt;
#include &lt;stdarg.h&gt;
#include &lt;stdio.h&gt;
#include &lt;string.h&gt;

static const char \*progname = "myapp";

void set_progname(const char *argv0) {
const char *p = strrchr(argv0, '/');
progname = p ? p + 1 : argv0;
}

void error(const char \*fmt, ...) {
fprintf(stderr, "%s: ", progname);
va_list ap;
va_start(ap, fmt);
vfprintf(stderr, fmt, ap);
va_end(ap);
fprintf(stderr, "\n");
}

void error_errno(const char \*fmt, ...) {
int saved_errno = errno;
fprintf(stderr, "%s: ", progname);
va_list ap;
va_start(ap, fmt);
vfprintf(stderr, fmt, ap);
va_end(ap);
fprintf(stderr, ": %s\n", strerror(saved_errno));
}
    </example>
  </pattern>
</cli_development>

<toolchain>
  <compilers>
    <compiler name="gcc">
      <description>GNU Compiler Collection</description>
      <flags>
        <flag name="-std=c11">Enable C11 standard (or c17, c23)</flag>
        <flag name="-Wall -Wextra -Wpedantic">Comprehensive warnings</flag>
        <flag name="-Werror">Treat warnings as errors</flag>
        <flag name="-Wshadow">Warn on variable shadowing</flag>
        <flag name="-Wconversion">Warn on implicit conversions</flag>
        <flag name="-Wstrict-prototypes">Require function prototypes</flag>
        <flag name="-fanalyzer">Static analysis (GCC 10+)</flag>
      </flags>
    </compiler>

    <compiler name="clang">
      <description>LLVM C compiler</description>
      <flags>
        <flag name="-std=c11">Enable C11 standard (or c17, c23)</flag>
        <flag name="-Wall -Wextra -Wpedantic">Comprehensive warnings</flag>
        <flag name="-Werror">Treat warnings as errors</flag>
        <flag name="-Weverything">All warnings (use selectively)</flag>
      </flags>
    </compiler>
  </compilers>

  <sanitizers>
    <sanitizer name="AddressSanitizer">
      <description>Memory error detection (buffer overflow, use-after-free)</description>
      <flags>-fsanitize=address -fno-omit-frame-pointer</flags>
      <example>
gcc -fsanitize=address -fno-omit-frame-pointer -g -o myapp myapp.c
      </example>
    </sanitizer>

    <sanitizer name="UndefinedBehaviorSanitizer">
      <description>Undefined behavior detection</description>
      <flags>-fsanitize=undefined</flags>
      <example>
gcc -fsanitize=undefined -g -o myapp myapp.c
      </example>
    </sanitizer>

    <sanitizer name="ThreadSanitizer">
      <description>Data race detection</description>
      <flags>-fsanitize=thread</flags>
      <note>Cannot be combined with AddressSanitizer</note>
    </sanitizer>

    <sanitizer name="MemorySanitizer">
      <description>Uninitialized memory read detection (Clang only)</description>
      <flags>-fsanitize=memory</flags>
    </sanitizer>
  </sanitizers>

  <static_analysis>
    <tool name="clang-tidy">
      <description>Clang-based linter and static analyzer</description>
      <usage>clang-tidy src/*.c -- -std=c11</usage>
      <configuration>
        <file_reference>.clang-tidy</file_reference>
Checks: > -*,
bugprone-_,
clang-analyzer-_,
misc-_,
performance-_,
readability-\*,
-readability-identifier-length

WarningsAsErrors: '\*'
      </configuration>
    </tool>

    <tool name="cppcheck">
      <description>Static analysis tool for C/C++</description>
      <usage>cppcheck --enable=all --error-exitcode=1 src/</usage>
    </tool>

    <tool name="valgrind">
      <description>Runtime memory error detection</description>
      <usage>valgrind --leak-check=full --show-leak-kinds=all ./myapp</usage>
      <tools>
        <tool name="memcheck">Memory error detection (default)</tool>
        <tool name="helgrind">Thread error detection</tool>
        <tool name="cachegrind">Cache profiling</tool>
        <tool name="callgrind">Call graph profiling</tool>
      </tools>
    </tool>
  </static_analysis>

  <testing>
    <decision_tree name="framework_selection">
      <question>What testing style do you prefer?</question>
      <branch condition="Simple, minimal dependencies">Use Check or Unity</branch>
      <branch condition="BDD-style">Use cmocka</branch>
      <branch condition="Embedded/resource-constrained">Use Unity (smallest footprint)</branch>
    </decision_tree>

    <framework name="Check">
      <description>Unit testing framework for C</description>
      <example>
#include &lt;check.h&gt;

START_TEST(test_addition) {
ck_assert_int_eq(1 + 1, 2);
}
END_TEST

Suite *math_suite(void) {
Suite *s = suite_create("Math");
TCase \*tc = tcase_create("Core");
tcase_add_test(tc, test_addition);
suite_add_tcase(s, tc);
return s;
}

int main(void) {
Suite *s = math_suite();
SRunner *sr = srunner_create(s);
srunner_run_all(sr, CK_NORMAL);
int failed = srunner_ntests_failed(sr);
srunner_free(sr);
return failed ? EXIT_FAILURE : EXIT_SUCCESS;
}
      </example>
    </framework>
  </testing>
</toolchain>

<build_systems>
  <decision_tree name="build_system_selection">
    <question>What is your project's complexity and portability needs?</question>
    <branch condition="Simple project, Unix-only">Use Make</branch>
    <branch condition="Cross-platform, dependencies">Use CMake or Meson</branch>
    <branch condition="Modern, fast builds">Use Meson</branch>
  </decision_tree>

  <make>
    <pattern name="simple_makefile">
      <description>Basic Makefile for C projects</description>
      <example>
CC := gcc
CFLAGS := -std=c11 -Wall -Wextra -Wpedantic -g
LDFLAGS :=
LDLIBS :=

SRCS := $(wildcard src/\*.c)
OBJS := $(SRCS:.c=.o)
TARGET := myapp

.PHONY: all clean

all: $(TARGET)

$(TARGET): $(OBJS)
$(CC) $(LDFLAGS) -o $@ $^ $(LDLIBS)

%.o: %.c
$(CC) $(CFLAGS) -c -o $@ $&lt;

clean:
rm -f $(OBJS) $(TARGET)
      </example>
    </pattern>
  </make>

  <cmake>
    <pattern name="modern_cmake">
      <description>Modern CMake for C projects</description>
      <example>
cmake_minimum_required(VERSION 3.20)
project(myapp VERSION 1.0.0 LANGUAGES C)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS OFF)

add_executable(myapp src/main.c src/utils.c)
target_include_directories(myapp PRIVATE include)

target_compile_options(myapp PRIVATE
$&lt;$&lt;C_COMPILER_ID:GNU,Clang&gt;:
-Wall -Wextra -Wpedantic -Werror
&gt;
)
      </example>
      <note>For detailed CMake patterns, see cplusplus-ecosystem skill</note>
    </pattern>
  </cmake>

  <meson>
    <pattern name="meson_build">
      <description>Meson build for C projects</description>
      <example>
# meson.build
project('myapp', 'c',
version: '1.0.0',
default_options: [
'c_std=c11',
'warning_level=3',
'werror=true',
]
)

src = files('src/main.c', 'src/utils.c')
inc = include_directories('include')

executable('myapp', src, include_directories: inc)
      </example>
    </pattern>
  </meson>
</build_systems>

<context7_integration>
  <description>Use Context7 MCP for up-to-date C documentation</description>

  <c_libraries>
    <library name="cppreference" id="/websites/cppreference_com" />
  </c_libraries>

  <usage_patterns>
    <pattern name="language_reference">
      <step>resolve-library-id libraryName="cppreference"</step>
      <step>get-library-docs context7CompatibleLibraryID="/websites/cppreference_com" topic="stdatomic.h"</step>
    </pattern>

    <pattern name="standard_library">
      <step>get-library-docs context7CompatibleLibraryID="/websites/cppreference_com" topic="malloc"</step>
    </pattern>
  </usage_patterns>
</context7_integration>

<best_practices>
  <practice priority="critical">Always check return values of malloc/calloc/realloc</practice>
  <practice priority="critical">Enable -Wall -Wextra -Werror for all builds</practice>
  <practice priority="critical">Run with AddressSanitizer during development</practice>
  <practice priority="critical">Use Valgrind before release</practice>
  <practice priority="high">Use fixed-width integer types from stdint.h</practice>
  <practice priority="high">Prefer snprintf over sprintf for buffer safety</practice>
  <practice priority="high">Use designated initializers for struct clarity</practice>
  <practice priority="high">Document ownership semantics in function comments</practice>
  <practice priority="medium">Use static for file-local functions and variables</practice>
  <practice priority="medium">Prefer const for read-only parameters</practice>
  <practice priority="medium">Use enum for related constants instead of define</practice>
  <practice priority="medium">Include what you use - minimize header dependencies</practice>
</best_practices>

<workflow>
  <phase name="analyze">
    <objective>Understand C code requirements</objective>
    <step>1. Check for existing code patterns and conventions</step>
    <step>2. Identify memory ownership requirements</step>
    <step>3. Review header dependencies</step>
  </phase>
  <phase name="implement">
    <objective>Write safe, portable C code</objective>
    <step>1. Use appropriate C standard (C11 minimum recommended)</step>
    <step>2. Follow memory management patterns</step>
    <step>3. Handle all error conditions</step>
  </phase>
  <phase name="validate">
    <objective>Verify C code correctness</objective>
    <step>1. Compile with warnings enabled</step>
    <step>2. Run with sanitizers</step>
    <step>3. Test with Valgrind</step>
  </phase>
</workflow>

<error_escalation>
  <level severity="low">
    <example>Compiler warning about unused variable</example>
    <action>Fix warning, maintain clean build</action>
  </level>
  <level severity="medium">
    <example>Valgrind reports minor memory leak</example>
    <action>Track down and fix leak, verify with Valgrind</action>
  </level>
  <level severity="high">
    <example>AddressSanitizer detects buffer overflow</example>
    <action>Stop, fix immediately - this is a security issue</action>
  </level>
  <level severity="critical">
    <example>Use-after-free or double-free detected</example>
    <action>Block operation, require immediate fix and review</action>
  </level>
</error_escalation>

<constraints>
  <must>Check all allocation return values</must>
  <must>Use bounded string functions (snprintf, strncpy)</must>
  <must>Enable compiler warnings</must>
  <must>Run sanitizers during development</must>
  <avoid>Using gets(), sprintf(), or other unsafe functions</avoid>
  <avoid>Raw pointer arithmetic without bounds checking</avoid>
  <avoid>Implicit type conversions that may lose data</avoid>
  <avoid>Global mutable state when possible</avoid>
</constraints>

<related_agents>
  <agent name="design">Memory architecture, data structure design</agent>
  <agent name="execute">C implementation with proper memory management</agent>
  <agent name="security">Buffer overflow detection, input validation</agent>
  <agent name="performance">Cache optimization, memory layout, profiling with Valgrind</agent>
</related_agents>

<related_skills>
  <skill name="serena-usage">Navigate C codebases and header hierarchies</skill>
  <skill name="context7-usage">C documentation via /websites/cppreference_com</skill>
  <skill name="cplusplus-ecosystem">CMake patterns and clang-tidy configuration</skill>
  <skill name="investigation-patterns">Debugging with Valgrind, GDB, and sanitizers</skill>
</related_skills>
