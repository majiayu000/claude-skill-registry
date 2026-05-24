---
name: Nim C Interop
description: Use when nim-C interoperability including calling C from Nim, wrapping C libraries, importc/exportc pragmas, header generation, FFI patterns, and building high-performance systems code integrating Nim with existing C codebases.
allowed-tools: []
---

# Nim C Interop

## Introduction

Nim compiles to C, enabling seamless interoperability with C code and libraries.
This bi-directional integration allows Nim developers to leverage decades of C
libraries while exposing Nim code to C applications. Understanding C interop is
essential for systems programming and library wrapping.

The interop mechanism uses pragmas like importc, exportc, and header to declare
foreign functions and types. Nim's type system maps naturally to C, with explicit
control over memory layout and calling conventions. This enables zero-overhead
abstraction while maintaining C ABI compatibility.

This skill covers importing C functions and types, wrapping C libraries, header
file generation, memory layout control, callback handling, and patterns for safe
type-safe C interop in systems programming.

## Importing C Functions

Import C functions using pragmas to make them callable from Nim code.

```nim
# Basic C function import
proc printf(format: cstring): cint {.importc, varargs, header: "<stdio.h>".}

proc main() =
  printf("Hello from C!\n")
  printf("Number: %d\n", 42)

# C function with explicit name
proc c_sqrt(x: cdouble): cdouble {.importc: "sqrt", header: "<math.h>".}

proc useSqrt() =
  let result = c_sqrt(16.0)
  echo result  # 4.0

# Multiple headers
proc malloc(size: csize_t): pointer {.importc, header: "<stdlib.h>".}
proc free(p: pointer) {.importc, header: "<stdlib.h>".}

proc manualAlloc() =
  var p = malloc(100)
  # Use memory
  free(p)

# C types mapping
proc strlen(s: cstring): csize_t {.importc, header: "<string.h>".}
proc strcpy(dest, src: cstring): cstring {.importc, header: "<string.h>".}

# Variadic C functions
proc snprintf(buf: cstring, size: csize_t, format: cstring): cint
  {.importc, varargs, header: "<stdio.h>".}

proc formatString(): string =
  var buffer: array[256, char]
  discard snprintf(cstring(addr buffer), 256, "Value: %d", 42)
  result = $cstring(addr buffer)

# C macros as inline procs
proc EXIT_SUCCESS(): cint {.importc: "EXIT_SUCCESS", header: "<stdlib.h>".}
proc EXIT_FAILURE(): cint {.importc: "EXIT_FAILURE", header: "<stdlib.h>".}

# Function pointers
type
  CompareFunc = proc (a, b: pointer): cint {.cdecl.}

proc qsort(base: pointer, nmemb, size: csize_t, compar: CompareFunc)
  {.importc, header: "<stdlib.h>".}

proc compareInts(a, b: pointer): cint {.cdecl.} =
  let x = cast[ptr cint](a)[]
  let y = cast[ptr cint](b)[]
  return x - y

proc sortArray() =
  var arr = [5, 2, 8, 1, 9]
  qsort(addr arr[0], arr.len, sizeof(cint), compareInts)

# C struct access
type
  TimeSpec {.importc: "struct timespec", header: "<time.h>".} = object
    tv_sec: int
    tv_nsec: int

proc clock_gettime(clk_id: cint, tp: ptr TimeSpec): cint
  {.importc, header: "<time.h>".}

# Calling conventions
proc win_api_func(): cint {.stdcall, importc, dynlib: "kernel32.dll".}

# C++ name mangling
proc cpp_function(x: cint): cint
  {.importcpp, header: "<myheader.hpp>".}

# C library linking
{.passL: "-lm".}  # Link math library
proc cos(x: cdouble): cdouble {.importc, header: "<math.h>".}
```

Import pragmas enable calling C code with full type safety from Nim.

## Wrapping C Libraries

Create type-safe Nim wrappers around C libraries for idiomatic usage.

```nim
# Simple wrapper
type
  FileHandle = distinct cint

proc c_open(path: cstring, flags: cint): cint
  {.importc: "open", header: "<fcntl.h>".}

proc c_close(fd: cint): cint
  {.importc: "close", header: "<unistd.h>".}

proc openFile(path: string): FileHandle =
  let fd = c_open(cstring(path), 0)
  if fd < 0:
    raise newException(IOError, "Failed to open file")
  FileHandle(fd)

proc close(fh: FileHandle) =
  discard c_close(cint(fh))

# Wrapping libcurl
type
  Curl = distinct pointer

const CURLE_OK = 0

proc curl_easy_init(): Curl {.importc, header: "<curl/curl.h>".}
proc curl_easy_cleanup(curl: Curl) {.importc, header: "<curl/curl.h>".}
proc curl_easy_setopt(curl: Curl, option: cint, parameter: pointer): cint
  {.importc, varargs, header: "<curl/curl.h>".}

type
  CurlHandle = object
    handle: Curl

proc newCurl(): CurlHandle =
  result.handle = curl_easy_init()
  if result.handle.pointer == nil:
    raise newException(Exception, "Failed to initialize curl")

proc close(curl: CurlHandle) =
  curl_easy_cleanup(curl.handle)

proc setUrl(curl: CurlHandle, url: string) =
  discard curl_easy_setopt(curl.handle, 10002, cstring(url))

# RAII wrapper with destructor
type
  CurlSession = object
    curl: Curl

proc `=destroy`(session: var CurlSession) =
  if session.curl.pointer != nil:
    curl_easy_cleanup(session.curl)
    session.curl = Curl(nil)

proc newSession(): CurlSession =
  result.curl = curl_easy_init()

# Wrapping complex C API
type
  SqliteDb = distinct pointer
  SqliteStmt = distinct pointer

proc sqlite3_open(filename: cstring, db: ptr SqliteDb): cint
  {.importc, header: "<sqlite3.h>".}

proc sqlite3_close(db: SqliteDb): cint
  {.importc, header: "<sqlite3.h>".}

proc sqlite3_prepare_v2(
  db: SqliteDb, sql: cstring, nbyte: cint,
  stmt: ptr SqliteStmt, tail: ptr cstring
): cint {.importc, header: "<sqlite3.h>".}

type
  Database = object
    handle: SqliteDb

proc openDatabase(filename: string): Database =
  var db: SqliteDb
  let rc = sqlite3_open(cstring(filename), addr db)
  if rc != 0:
    raise newException(IOError, "Cannot open database")
  result.handle = db

proc `=destroy`(db: var Database) =
  if db.handle.pointer != nil:
    discard sqlite3_close(db.handle)

# C callback wrapping
type
  EventCallback = proc (data: pointer) {.cdecl.}

proc c_register_callback(cb: EventCallback, data: pointer)
  {.importc: "register_callback", header: "events.h".}

proc nimCallback(data: pointer) {.cdecl.} =
  echo "Callback triggered"

proc registerEvent() =
  c_register_callback(nimCallback, nil)
```

Wrappers provide Nim-idiomatic interfaces while preserving C library functionality.

## Exporting to C

Export Nim functions to C using exportc pragma for library creation.

```nim
# Basic export
proc add(a, b: cint): cint {.exportc.} =
  a + b

# Export with specific name
proc multiply(a, b: cint): cint {.exportc: "nim_multiply".} =
  a * b

# Export with dynlib
proc divide(a, b: cint): cint {.exportc, dynlib.} =
  if b == 0: return 0
  a div b

# Export complex types
type
  Point {.exportc.} = object
    x: cint
    y: cint

proc createPoint(x, y: cint): Point {.exportc.} =
  Point(x: x, y: y)

proc pointDistance(p1, p2: Point): cdouble {.exportc.} =
  let dx = (p2.x - p1.x).float
  let dy = (p2.y - p1.y).float
  sqrt(dx * dx + dy * dy)

# Export string operations
proc processString(input: cstring): cstring {.exportc.} =
  let s = $input
  result = cstring(s.toUpperAscii())

# Generating header file
{.emit: """/*TYPESECTION*/
typedef struct {
  int x;
  int y;
} Point;
""".}

proc generateHeader() {.exportc: "lib_init".} =
  echo "Library initialized"

# Export callbacks
type
  Callback = proc (value: cint) {.cdecl.}

proc registerCallback(cb: Callback) {.exportc.} =
  cb(42)

# Building shared library
# Compile with: nim c --app:lib --noMain mylib.nim

# Library initialization
proc NimMain() {.importc.}

proc libInit() {.exportc: "lib_init".} =
  NimMain()
  echo "Nim library initialized"

# Export with error handling
proc safeOperation(value: cint): cint {.exportc.} =
  try:
    if value < 0:
      raise newException(ValueError, "Negative value")
    result = value * 2
  except:
    result = -1
```

Exportc enables creating C-compatible libraries from Nim code.

## Memory Layout and Alignment

Control memory layout for C struct compatibility and performance.

```nim
# Packed structures
type
  PackedStruct {.packed.} = object
    a: uint8
    b: uint32
    c: uint8

echo sizeof(PackedStruct)  # 6 bytes (no padding)

# Aligned structures
type
  AlignedStruct {.align(16).} = object
    data: array[4, float32]

echo sizeof(AlignedStruct)  # Aligned to 16 bytes

# C struct layout
type
  CStruct {.importc, header: "myheader.h".} = object
    field1: cint
    field2: cdouble
    field3: cstring

# Union types
type
  Union {.union.} = object
    intValue: cint
    floatValue: cfloat
    bytes: array[4, uint8]

proc accessUnion() =
  var u: Union
  u.intValue = 0x12345678
  echo u.bytes[0].toHex

# Bit fields (via packed)
type
  BitField {.packed.} = object
    flag1: uint8  # Use 1 byte per field
    flag2: uint8
    value: uint16

# Padding control
type
  ControlledPadding = object
    a: uint8
    pad1 {.align(4).}: array[3, uint8]
    b: uint32

# Calculating offsets
proc fieldOffset() =
  type T = object
    a: int32
    b: int64

  echo offsetOf(T, a)  # 0
  echo offsetOf(T, b)  # 8 (with padding)

# C array mapping
type
  CArray = object
    data: ptr UncheckedArray[cint]
    len: csize_t

proc accessCArray(arr: CArray) =
  for i in 0..<arr.len:
    echo arr.data[i]

# Flexible array member
type
  FlexArray = object
    length: cint
    data: UncheckedArray[cint]

proc createFlexArray(size: int): ptr FlexArray =
  let totalSize = sizeof(cint) + size * sizeof(cint)
  result = cast[ptr FlexArray](alloc(totalSize))
  result.length = cint(size)
```

Memory layout control ensures C compatibility and optimal performance.

## FFI Patterns and Safety

Common patterns for safe foreign function interface usage.

```nim
# Safe string conversion
proc safeToString(cs: cstring): string =
  if cs == nil:
    return ""
  result = $cs

# Handling C errors
type
  CError = object
    code: cint
    message: cstring

proc checkError(err: CError) =
  if err.code != 0:
    raise newException(Exception, $err.message)

# Resource management
type
  Resource = object
    handle: pointer

proc acquire(): Resource =
  result.handle = malloc(1024)

proc `=destroy`(r: var Resource) =
  if r.handle != nil:
    free(r.handle)
    r.handle = nil

# Callback with closure
type
  ClosureCallback = object
    fn: proc (data: pointer) {.cdecl.}
    data: pointer

var globalClosure: ref tuple[callback: proc()]

proc wrapCallback(callback: proc()) =
  globalClosure = new(tuple[callback: proc()])
  globalClosure.callback = callback

  proc cCallback(data: pointer) {.cdecl.} =
    globalClosure.callback()

  # Register cCallback with C library

# Opaque types
type
  OpaqueHandle {.importc, header: "lib.h".} = object

proc createHandle(): ptr OpaqueHandle
  {.importc, header: "lib.h".}

proc destroyHandle(h: ptr OpaqueHandle)
  {.importc, header: "lib.h".}

# Version checking
when sizeof(clong) == 8:
  type CLong = int64
else:
  type CLong = int32

# Platform-specific code
when defined(windows):
  proc windowsFunc() {.importc, dynlib: "kernel32.dll".}
elif defined(posix):
  proc posixFunc() {.importc, header: "<unistd.h>".}
```

Safe FFI patterns prevent common C interop errors and resource leaks.

## Best Practices

1. **Use distinct types** for C handles to prevent mixing different handle types

2. **Implement destructors** for wrapped resources to ensure cleanup

3. **Check for nil** when receiving pointers from C code

4. **Use cstring carefully** as Nim strings and C strings have different lifetimes

5. **Wrap C APIs** with Nim-idiomatic interfaces rather than exposing C directly

6. **Test interop code** thoroughly as type mismatches cause runtime errors

7. **Use const for read-only** C parameters to prevent accidental modification

8. **Generate headers** when exporting to make C integration easier

9. **Handle C errors** explicitly and convert to Nim exceptions

10. **Document memory ownership** for functions passing pointers between
    Nim and C

## Common Pitfalls

1. **Not preserving string lifetime** when passing Nim strings to C causes corruption

2. **Forgetting to link C libraries** with passL causes undefined symbol errors

3. **Mismatching calling conventions** (cdecl vs stdcall) causes stack corruption

4. **Not handling nil pointers** from C causes segmentation faults

5. **Incorrect memory layout** for C structs causes data corruption

6. **Using GC types in C callbacks** causes crashes as GC may move objects

7. **Not checking C return values** misses error conditions

8. **Mixing Nim and C memory** management causes double-free or leaks

9. **Assuming C struct padding** matches Nim without packed pragma

10. **Not testing on target platform** misses platform-specific issues

## When to Use This Skill

Apply C interop when wrapping existing C libraries for Nim projects.

Use importc to leverage battle-tested C code without reimplementation.

Export Nim functions to create libraries usable from C applications.

Integrate with system APIs only available through C interfaces.

Optimize hot paths by calling optimized C implementations.

Build upon C ecosystems while writing higher-level Nim code.

## Resources

- [Nim C Interop](<https://nim-lang.org/docs/manual.html#foreign-function-interface>)
- [Nim FFI Guide](<https://nim-lang.org/docs/backends.html#c-ffi>)
- [wrapping C libraries](<https://nim-by-example.github.io/ffi/>)
- [Nim C Integration](<https://nim-lang.org/docs/lib.html#c-interface>)
- [Nim Compiler Backend](<https://nim-lang.org/docs/nimc.html#c-code-generation>)
