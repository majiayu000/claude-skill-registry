---
name: mocking
description: Mocking skill for the ikigai project
---

# Mocking

## Description
MOCKABLE wrapper patterns for testing external dependencies.

## Philosophy

**Mock external dependencies, never our own code.** External means: libraries (talloc, yyjson, curl), system calls (open, read, write, stat), and vendor inline functions.

## The MOCKABLE Pattern

`wrapper.h` provides zero-overhead mocking via weak symbols:

```c
// wrapper.h
#ifdef NDEBUG
    #define MOCKABLE static inline  // Release: zero overhead
#else
    #define MOCKABLE __attribute__((weak))  // Debug: overridable
#endif

MOCKABLE int posix_write_(int fd, const void *buf, size_t count);
```

## Using Mocks in Tests

Override the weak symbol in your test file:

```c
// test_file.c
#include "wrapper.h"

// Override - this replaces the weak symbol
int posix_write_(int fd, const void *buf, size_t count) {
    return -1;  // Simulate write failure
}

void test_write_error_handling(void) {
    // Now any code calling posix_write_() gets our mock
    res_t r = save_file("test.txt", "content");
    assert(IS_ERR(r));
}
```

## Available Wrappers

### POSIX System Calls
| Wrapper | Wraps |
|---------|-------|
| `posix_open_()` | `open()` |
| `posix_close_()` | `close()` |
| `posix_read_()` | `read()` |
| `posix_write_()` | `write()` |
| `posix_stat_()` | `stat()` |
| `posix_mkdir_()` | `mkdir()` |
| `posix_access_()` | `access()` |
| `posix_rename_()` | `rename()` |
| `posix_getcwd_()` | `getcwd()` |
| `posix_pipe_()` | `pipe()` |
| `posix_fcntl_()` | `fcntl()` |
| `posix_select_()` | `select()` |
| `posix_sigaction_()` | `sigaction()` |
| `posix_ioctl_()` | `ioctl()` |
| `posix_tcgetattr_()` | `tcgetattr()` |
| `posix_tcsetattr_()` | `tcsetattr()` |
| `posix_tcflush_()` | `tcflush()` |

### POSIX stdio
| Wrapper | Wraps |
|---------|-------|
| `fopen_()` | `fopen()` |
| `fclose_()` | `fclose()` |
| `fread_()` | `fread()` |
| `fwrite_()` | `fwrite()` |
| `fseek_()` | `fseek()` |
| `ftell_()` | `ftell()` |
| `posix_fdopen_()` | `fdopen()` |
| `popen_()` | `popen()` |
| `pclose_()` | `pclose()` |
| `opendir_()` | `opendir()` |

### C Standard Library
| Wrapper | Wraps |
|---------|-------|
| `snprintf_()` | `snprintf()` |
| `vsnprintf_()` | `vsnprintf()` |
| `gmtime_()` | `gmtime()` |
| `strftime_()` | `strftime()` |

### talloc
| Wrapper | Wraps |
|---------|-------|
| `talloc_zero_()` | `talloc_zero_size()` |
| `talloc_strdup_()` | `talloc_strdup()` |
| `talloc_array_()` | `talloc_zero_size()` |
| `talloc_realloc_()` | `talloc_realloc_size()` |
| `talloc_asprintf_()` | `talloc_vasprintf()` |

### yyjson
| Wrapper | Wraps |
|---------|-------|
| `yyjson_read_file_()` | `yyjson_read_file()` |
| `yyjson_mut_write_file_()` | `yyjson_mut_write_file()` |
| `yyjson_read_()` | `yyjson_read()` |
| `yyjson_doc_get_root_()` | `yyjson_doc_get_root()` |
| `yyjson_obj_get_()` | `yyjson_obj_get()` |
| `yyjson_get_sint_()` | `yyjson_get_sint()` |
| `yyjson_get_str_()` | `yyjson_get_str()` |
| `yyjson_mut_obj_add_str_()` | `yyjson_mut_obj_add_str()` |
| `yyjson_mut_obj_add_int_()` | `yyjson_mut_obj_add_int()` |
| `yyjson_mut_obj_add_uint_()` | `yyjson_mut_obj_add_uint()` |
| `yyjson_mut_obj_()` | `yyjson_mut_obj()` |
| `yyjson_mut_arr_()` | `yyjson_mut_arr()` |
| `yyjson_mut_obj_add_val_()` | `yyjson_mut_obj_add_val()` |
| `yyjson_mut_arr_add_val_()` | `yyjson_mut_arr_add_val()` |
| `yyjson_mut_obj_add_bool_()` | `yyjson_mut_obj_add_bool()` |
| `yyjson_val_mut_copy_()` | `yyjson_val_mut_copy()` |

### libcurl (Easy API)
| Wrapper | Wraps |
|---------|-------|
| `curl_easy_init_()` | `curl_easy_init()` |
| `curl_easy_cleanup_()` | `curl_easy_cleanup()` |
| `curl_easy_perform_()` | `curl_easy_perform()` |
| `curl_easy_setopt_()` | `curl_easy_setopt()` |
| `curl_easy_getinfo_()` | `curl_easy_getinfo()` |
| `curl_easy_strerror_()` | `curl_easy_strerror()` |
| `curl_slist_append_()` | `curl_slist_append()` |
| `curl_slist_free_all_()` | `curl_slist_free_all()` |

### libcurl (Multi API)
| Wrapper | Wraps |
|---------|-------|
| `curl_multi_init_()` | `curl_multi_init()` |
| `curl_multi_cleanup_()` | `curl_multi_cleanup()` |
| `curl_multi_add_handle_()` | `curl_multi_add_handle()` |
| `curl_multi_remove_handle_()` | `curl_multi_remove_handle()` |
| `curl_multi_perform_()` | `curl_multi_perform()` |
| `curl_multi_fdset_()` | `curl_multi_fdset()` |
| `curl_multi_timeout_()` | `curl_multi_timeout()` |
| `curl_multi_info_read_()` | `curl_multi_info_read()` |
| `curl_multi_strerror_()` | `curl_multi_strerror()` |

### libpq (PostgreSQL)
| Wrapper | Wraps |
|---------|-------|
| `PQgetvalue_()` | `PQgetvalue()` |
| `pq_exec_()` | `PQexec()` |
| `pq_exec_params_()` | `PQexecParams()` |
| `PQresultStatus_()` | `PQresultStatus()` |

### pthread
| Wrapper | Wraps |
|---------|-------|
| `pthread_mutex_init_()` | `pthread_mutex_init()` |
| `pthread_mutex_destroy_()` | `pthread_mutex_destroy()` |
| `pthread_mutex_lock_()` | `pthread_mutex_lock()` |
| `pthread_mutex_unlock_()` | `pthread_mutex_unlock()` |
| `pthread_create_()` | `pthread_create()` |
| `pthread_join_()` | `pthread_join()` |

### Internal ikigai Functions
| Wrapper | Wraps |
|---------|-------|
| `ik_db_init_()` | `ik_db_init()` |
| `ik_db_message_insert_()` | `ik_db_message_insert()` |
| `ik_scrollback_append_line_()` | `ik_scrollback_append_line()` |
| `ik_repl_render_frame_()` | `ik_repl_render_frame()` |
| `ik_agent_get_provider_()` | `ik_agent_get_provider()` |
| `ik_request_build_from_conversation_()` | `ik_request_build_from_conversation()` |
| `ik_http_multi_create_()` | `ik_http_multi_create()` |
| `ik_http_multi_info_read_()` | `ik_http_multi_info_read()` |
| `ik_agent_start_tool_execution_()` | `ik_agent_start_tool_execution()` |
| `ik_agent_should_continue_tool_loop_()` | `ik_agent_should_continue_tool_loop()` |
| `ik_repl_submit_tool_loop_continuation_()` | `ik_repl_submit_tool_loop_continuation()` |
| `ik_agent_add_message_()` | `ik_agent_add_message()` |
| `ik_agent_transition_to_idle_()` | `ik_agent_transition_to_idle()` |

## Adding New Wrappers

When you need to mock a new external dependency:

1. Add declaration to `wrapper.h`:
```c
MOCKABLE return_type function_name_(args);
```

2. Add implementation to `wrapper.c`:
```c
return_type function_name_(args) {
    return original_function(args);
}
```

3. Replace direct calls in production code with the wrapper

4. Override in tests to inject failures

## Wrapping Vendor Inline Functions

Problem: Inline functions like `yyjson_doc_get_root()` expand at every call site, creating untestable branches.

Solution: Wrap once, use wrapper everywhere:

```c
// sse_parser.h
yyjson_val *yyjson_doc_get_root_wrapper(yyjson_doc *doc);

// sse_parser.c
yyjson_val *yyjson_doc_get_root_wrapper(yyjson_doc *doc) {
    return yyjson_doc_get_root(doc);  // Inline expands here only
}

// Test both branches once
void test_wrapper_null(void) {
    assert(yyjson_doc_get_root_wrapper(NULL) == NULL);
}
void test_wrapper_valid(void) {
    yyjson_doc *doc = create_test_doc();
    assert(yyjson_doc_get_root_wrapper(doc) != NULL);
}
```

## What NOT to Mock

- Our own code (refactor instead)
- Pure functions (test directly)
- Simple data structures

## References

- `src/wrapper.h` - MOCKABLE declarations
- `src/wrapper.c` - Wrapper implementations
- `src/openai/sse_parser.h` - Inline wrapper example
