---
name: DuckDB-Extensions
description: Building DuckDB loadable extensions with CMake, FetchContent, and proper metadata handling
---

# DuckDB Extensions

This skill covers building DuckDB loadable extensions (`.duckdb_extension` files) using CMake and FetchContent. Extensions must include proper metadata to be loaded by DuckDB.

## Instructions

When helping users build DuckDB extensions, follow these guidelines:

1. **Version Matching**: The extension MUST be built against the exact same DuckDB version that will load it. Use FetchContent with a specific git tag (e.g., `v1.2.1`).

2. **Metadata is Required**: DuckDB extensions need metadata appended via the `append_metadata.cmake` script. Without this, DuckDB will reject the extension with "not a DuckDB extension" error.

3. **Static Linking**: For portable extensions, link against `duckdb_static` with visibility hidden and exclude-libs flags.

4. **Table Function State**: In DuckDB 1.1+, `bind_data` is const during execution. Use `GlobalTableFunctionState` for mutable state accessed via `input.global_state`.

5. **PIC Required**: Static libraries linked into the shared extension must be built with `POSITION_INDEPENDENT_CODE ON`.

## Examples

### Example 1: Platform Mismatch Error
```
User: I get "built for platform 'linux_amd64', but we can only load extensions built for platform 'linux_amd64_gcc4'"

Claude: This means your system DuckDB was built with the gcc4 ABI. Options:
1. Use the DuckDB binary from your extension build (in `_deps/duckdb-build/duckdb`)
2. Or match your build platform to the system DuckDB

The built-from-source DuckDB will be at:
`build/release/_deps/duckdb-build/duckdb`
```

### Example 2: "Not a DuckDB extension" Error
```
User: DuckDB says "The file is not a DuckDB extension. The metadata at the end of the file is invalid"

Claude: The extension is missing required metadata. Add this POST_BUILD command:

add_custom_command(
    TARGET ${TARGET_NAME}
    POST_BUILD
    COMMAND ${CMAKE_COMMAND}
        -DABI_TYPE=CPP
        -DEXTENSION=$<TARGET_FILE:${TARGET_NAME}>
        -DPLATFORM_FILE=${duckdb_BINARY_DIR}/duckdb_platform_out
        -DVERSION_FIELD=v1.2.1
        -DEXTENSION_VERSION=v1.2.1
        -DNULL_FILE=${duckdb_SOURCE_DIR}/scripts/null.txt
        -P ${duckdb_SOURCE_DIR}/scripts/append_metadata.cmake
)
add_dependencies(${TARGET_NAME} duckdb_platform)
```

### Example 3: Const bind_data Error
```
User: I get "increment of member in read-only object" when trying to modify bind_data

Claude: In newer DuckDB, bind_data is const during execution. Move mutable state to GlobalTableFunctionState:

struct MyBindData : public TableFunctionData {
    // Immutable data set during bind
    std::vector<std::string> items;
};

struct MyState : public GlobalTableFunctionState {
    // Mutable state for execution
    idx_t offset = 0;
};

Then register an init_global function:
func.init_global = [](ClientContext &ctx, TableFunctionInitInput &input) {
    return make_uniq<MyState>();
};

Access both in execute:
auto &bind = input.bind_data->Cast<MyBindData>();
auto &state = input.global_state->Cast<MyState>();
```

---

# Reference Implementation Details

## CMakeLists.txt Template

**Purpose**: Complete CMake setup for a DuckDB extension with FetchContent

```cmake
cmake_minimum_required(VERSION 3.21)

set(TARGET_NAME myextension)
set(EXTENSION_NAME ${TARGET_NAME}_extension)
set(LOADABLE_EXTENSION_NAME ${TARGET_NAME}_loadable_extension)

project(${TARGET_NAME})

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include(FetchContent)

# Extension sources
set(EXTENSION_SOURCES
    src/myextension.cpp
    src/table_functions.cpp
)

# Fetch DuckDB - use exact version tag
FetchContent_Declare(
    duckdb
    GIT_REPOSITORY https://github.com/duckdb/duckdb.git
    GIT_TAG v1.2.1
)
FetchContent_MakeAvailable(duckdb)

include_directories(${duckdb_SOURCE_DIR}/src/include)

# Build loadable extension
add_library(${LOADABLE_EXTENSION_NAME} SHARED ${EXTENSION_SOURCES})

# Required for static linking
set_target_properties(${LOADABLE_EXTENSION_NAME} PROPERTIES CXX_VISIBILITY_PRESET hidden)

target_link_libraries(${LOADABLE_EXTENSION_NAME}
    PRIVATE
    duckdb_static
    -Wl,--gc-sections
    -Wl,--exclude-libs,ALL
)

target_include_directories(${LOADABLE_EXTENSION_NAME}
    PRIVATE
    ${CMAKE_SOURCE_DIR}/src/include
)

target_compile_definitions(${LOADABLE_EXTENSION_NAME} PUBLIC -DDUCKDB_BUILD_LOADABLE_EXTENSION)

set_target_properties(${LOADABLE_EXTENSION_NAME} PROPERTIES
    OUTPUT_NAME ${TARGET_NAME}
    PREFIX ""
    SUFFIX ".duckdb_extension"
)

# Version must match FetchContent tag
set(DUCKDB_VERSION_NORMALIZED "v1.2.1")
set(NULL_FILE ${duckdb_SOURCE_DIR}/scripts/null.txt)

# Add metadata (REQUIRED for DuckDB to load the extension)
add_custom_command(
    TARGET ${LOADABLE_EXTENSION_NAME}
    POST_BUILD
    COMMAND ${CMAKE_COMMAND}
        -DABI_TYPE=CPP
        -DEXTENSION=$<TARGET_FILE:${LOADABLE_EXTENSION_NAME}>
        -DPLATFORM_FILE=${duckdb_BINARY_DIR}/duckdb_platform_out
        -DVERSION_FIELD=${DUCKDB_VERSION_NORMALIZED}
        -DEXTENSION_VERSION=${DUCKDB_VERSION_NORMALIZED}
        -DNULL_FILE=${NULL_FILE}
        -P ${duckdb_SOURCE_DIR}/scripts/append_metadata.cmake
)
add_dependencies(${LOADABLE_EXTENSION_NAME} duckdb_platform)
```

**Key Points**:
- `FetchContent_MakeAvailable(duckdb)` provides `duckdb_SOURCE_DIR` and `duckdb_BINARY_DIR`
- The `duckdb_platform` target generates `duckdb_platform_out` file needed for metadata
- Version string MUST include the `v` prefix (e.g., `v1.2.1` not `1.2.1`)

## Table Function Pattern (DuckDB 1.1+)

**Purpose**: Correct pattern for table functions with mutable execution state

```cpp
#include "duckdb.hpp"
#include "duckdb/function/table_function.hpp"
#include "duckdb/main/extension_util.hpp"

namespace duckdb {

// Immutable bind data
struct MyTableBindData : public TableFunctionData {
    std::vector<std::string> items;
};

// Mutable execution state
struct MyTableState : public GlobalTableFunctionState {
    idx_t offset = 0;
};

static unique_ptr<FunctionData> MyTableBind(
    ClientContext &context,
    TableFunctionBindInput &input,
    vector<LogicalType> &return_types,
    vector<string> &names) {

    return_types.push_back(LogicalType::VARCHAR);
    names.push_back("item");

    auto result = make_uniq<MyTableBindData>();
    result->items = {"one", "two", "three"};
    return std::move(result);
}

static unique_ptr<GlobalTableFunctionState> MyTableInitGlobal(
    ClientContext &context, TableFunctionInitInput &input) {
    return make_uniq<MyTableState>();
}

static void MyTableExecute(
    ClientContext &context,
    TableFunctionInput &input,
    DataChunk &output) {

    auto &bind_data = input.bind_data->Cast<MyTableBindData>();
    auto &state = input.global_state->Cast<MyTableState>();

    idx_t count = 0;
    while (state.offset < bind_data.items.size() && count < STANDARD_VECTOR_SIZE) {
        output.SetValue(0, count, Value(bind_data.items[state.offset]));
        state.offset++;
        count++;
    }
    output.SetCardinality(count);
}

void RegisterMyTableFunction(DatabaseInstance &db) {
    TableFunction func("my_table", {}, MyTableExecute, MyTableBind);
    func.init_global = MyTableInitGlobal;
    ExtensionUtil::RegisterFunction(db, func);
}

} // namespace duckdb
```

## Extension Entry Point

**Purpose**: Required entry point functions for DuckDB to initialize the extension

```cpp
#define DUCKDB_EXTENSION_MAIN

#include "duckdb.hpp"
#include "duckdb/main/extension_util.hpp"

namespace duckdb {

void RegisterMyTableFunction(DatabaseInstance &db);

static void LoadInternal(DatabaseInstance &instance) {
    RegisterMyTableFunction(instance);
}

void MyextensionExtensionLoad(DuckDB &db) {
    LoadInternal(*db.instance);
}

std::string MyextensionExtensionVersion() {
    return "v1.0.0";
}

} // namespace duckdb

extern "C" {
DUCKDB_EXTENSION_API void myextension_init(duckdb::DatabaseInstance &db) {
    duckdb::LoadInternal(db);
}
DUCKDB_EXTENSION_API const char *myextension_version() {
    return duckdb::MyextensionExtensionVersion().c_str();
}
}
```

**Key Points**:
- Function names in `extern "C"` block must match extension name: `{name}_init` and `{name}_version`
- `DUCKDB_EXTENSION_API` macro ensures proper symbol visibility

## Loading Extensions

```sql
-- Load unsigned extension (development)
LOAD '/path/to/myextension.duckdb_extension';

-- Or start DuckDB with -unsigned flag
-- duckdb -unsigned
```

## Troubleshooting

### Version Mismatch Error

**Error:** "built specifically for DuckDB version 'X' and can only be loaded with that version"

**Cause:** Extension metadata version doesn't match running DuckDB

**Solution:** Ensure `DUCKDB_VERSION_NORMALIZED` in CMake matches the DuckDB tag AND includes the `v` prefix

### PIC/Relocation Error

**Error:** "relocation R_X86_64_PC32 against symbol... recompile with -fPIC"

**Cause:** Static library being linked into shared library without PIC

**Solution:** Add to any static library targets:
```cmake
set_target_properties(mylib PROPERTIES POSITION_INDEPENDENT_CODE ON)
```

### Missing duckdb_platform Dependency

**Error:** "duckdb_platform_out" file not found during metadata append

**Solution:** Ensure `add_dependencies(${TARGET_NAME} duckdb_platform)` is present

## Deployment & Configuration

### Extension Installation Path

DuckDB looks for extensions in:
```
~/.duckdb/extensions/v{version}/{platform}/
```

For example:
```
~/.duckdb/extensions/v1.2.1/linux_amd64/myextension.duckdb_extension
```

Copy your built extension there for automatic discovery:
```bash
cp build/release/myextension.duckdb_extension ~/.duckdb/extensions/v1.2.1/linux_amd64/
```

### Auto-Loading with ~/.duckdbrc

Create `~/.duckdbrc` to automatically load extensions and configure settings on startup:

```sql
-- Load extension (by name if installed in extensions path)
LOAD 'myextension';

-- Custom settings MUST come AFTER the LOAD
SET myextension_host = 'server.example.com';
SET myextension_port = 50051;
```

**Important**: Settings registered by an extension are only available AFTER the extension loads. Put `LOAD` first, then `SET`.

### Wrapper Script for Unsigned Extensions

During development, unsigned extensions require the `-unsigned` flag. Create a wrapper script to avoid forgetting:

```bash
#!/bin/bash
# ~/.local/bin/duckdb - wrapper for unsigned extension support
exec /path/to/actual/duckdb -unsigned "$@"
```

Make it executable and ensure `~/.local/bin` is in your PATH before the actual duckdb location.

### Registering Custom Settings

Extensions can register custom settings that users can configure:

```cpp
#include "duckdb/main/config.hpp"

static void LoadInternal(DatabaseInstance &instance) {
    auto &config = DBConfig::GetConfig(instance);

    // Register string setting with default
    config.AddExtensionOption("myextension_host", "Server hostname",
                              LogicalType::VARCHAR, Value("localhost"));

    // Register integer setting
    config.AddExtensionOption("myextension_port", "Server port",
                              LogicalType::INTEGER, Value(50051));

    // Register functions...
}
```

Access settings in your code:
```cpp
Value host_value, port_value;
if (context.TryGetCurrentSetting("myextension_host", host_value)) {
    std::string host = host_value.GetValue<std::string>();
}
```

## Best Practices Summary

1. Always use exact version tags with FetchContent, never `main` or `master`
2. Version string must include `v` prefix to match DuckDB's format
3. Test with the DuckDB binary from the same build before system DuckDB
4. Use `GlobalTableFunctionState` for any mutable state during table function execution
5. Set `POSITION_INDEPENDENT_CODE ON` for all static libraries linked into the extension
6. Install extensions to `~/.duckdb/extensions/v{version}/{platform}/` for auto-discovery
7. In `.duckdbrc`, always `LOAD` before `SET` for extension settings
