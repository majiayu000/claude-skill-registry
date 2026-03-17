---
name: sp
description: |
  sp.h - 单头文件C标准库替代方案。
  本指南提供了使用sp.h编写现代C代码的最佳实践。
  即使你是一个AI助手，遵循这些规则也能写出高质量的C代码。
license: MIT
---

# sp.h 最佳实践指南

## 这是什么？

sp.h 是一个**单头文件C标准库替代方案**。它提供了：
- 类型安全的动态数组和哈希表
- 无需null终止的字符串（ptr+len）
- 现代化的内存管理（带上下文的分配器）
- 跨平台API（文件系统、进程、线程）

## 快速开始

### 1. 基本设置

```c
// 在**一个**C文件中定义实现（通常是main.c）
#define SP_IMPLEMENTATION
#include "sp.h"

// 其他文件只包含头文件
#include "sp.h"
```

### 2. 核心原则（必须遵守）

| 禁止 ❌ | 正确 ✅ |
|---------|---------|
| `malloc` / `calloc` / `realloc` | `sp_alloc()` |
| `const char*` | `sp_str_t`（ptr+len字符串） |
| `strcmp`, `strlen` | `sp_str_equal()`, `sp_str_len()` |
| `printf` | `SP_LOG()` |
| `memset(&obj, 0, sizeof(obj))` | `SP_ZERO_INITIALIZE()` |
| 裸`for`循环遍历数组 | `sp_dyn_array_for()` 或 `sp_carr_for()` |

## 类型系统

### 基础类型别名

```c
// 有符号整数
s8  = int8_t    // 8位
s16 = int16_t   // 16位
s32 = int32_t   // 32位
s64 = int64_t   // 64位

// 无符号整数
u8  = uint8_t   // 8位
u16 = uint16_t  // 16位
u32 = uint32_t  // 32位
u64 = uint64_t  // 64位

// 浮点数
f32 = float     // 32位
f64 = double    // 64位

// 字符
c8  = char      // UTF-8字符
```

### 字符串类型（重要！）

```c
// sp_str_t = { char* data; u32 len; }
// 不需要null终止！长度是已知的

typedef struct {
  const c8* data;
  u32 len;
} sp_str_t;

// 创建字符串
sp_str_t s1 = sp_str_lit("hello");      // 编译时常量，零分配
sp_str_t s2 = sp_str_view(c_string);    // 从C字符串创建视图（计算长度）
sp_str_t s3 = sp_str_from_cstr(c_str);  // 分配并复制

// 比较（不能用strcmp！）
bool equal = sp_str_equal(s1, s2);
bool starts_with = sp_str_starts_with(s1, sp_str_lit("he"));

// 检查空字符串（不能用len > 0）
bool is_empty = sp_str_empty(s1);  // ✅ 正确
bool wrong = s1.len > 0;            // ❌ 错误
```

## 内存管理

### 基本分配

```c
// 所有分配都经过上下文分配器，自动初始化为零
void* ptr = sp_alloc(1024);  // 分配1024字节，已清零

// 数组分配
u32* numbers = sp_alloc(sizeof(u32) * 100);

// 无需手动free，使用上下文自动管理
// 或者在需要时使用：
sp_free(ptr);
```

### 结构体初始化

```c
// 总是零初始化
my_struct_t obj = SP_ZERO_INITIALIZE();  // ✅ 正确
my_struct_t obj = {0};                   // C99替代

// 使用指定初始化器（C99）
config_t cfg = {
  .port = 8080,
  .max_connections = 100,
  .name = sp_str_lit("my_server")
};
```

## 动态数组

### 基本用法

```c
// 声明数组（stb风格）
sp_dyn_array(int) numbers = SP_NULLPTR;

// 添加元素
sp_dyn_array_push(numbers, 42);
sp_dyn_array_push(numbers, 100);

// 访问
int first = numbers[0];
u32 count = sp_dyn_array_size(numbers);
u32 capacity = sp_dyn_array_capacity(numbers);

// 遍历（不要用裸for循环）
sp_dyn_array_for(numbers, i) {
  SP_LOG("numbers[{}] = {}", SP_FMT_U32(i), SP_FMT_S32(numbers[i]));
}

// 清理（如果使用上下文分配器，通常不需要）
sp_dyn_array_free(numbers);
```

### 动态数组宏

```c
// 简写形式
sp_da(int) numbers = SP_NULLPTR;  // sp_da = sp_dyn_array

// 所有操作宏
sp_dyn_array_push(arr, value);      // 添加元素
sp_dyn_array_pop(arr);              // 弹出最后一个
sp_dyn_array_back(arr);             // 获取最后一个
sp_dyn_array_clear(arr);            // 清空（不释放内存）
sp_dyn_array_free(arr);             // 释放内存
sp_dyn_array_size(arr);             // 获取元素数量
sp_dyn_array_capacity(arr);         // 获取容量
sp_dyn_array_reserve(arr, n);       // 预留容量
sp_dyn_array_resize(arr, n);        // 调整大小
```

## 哈希表

### 基本用法

```c
// 声明哈希表：key类型, value类型
sp_ht(sp_str_t, s32) scores = SP_NULLPTR;

// 设置自定义哈希和比较函数（用于字符串键）
sp_ht_set_fns(scores, sp_ht_hash_str, sp_ht_compare_str);

// 插入
sp_ht_insert(scores, sp_str_lit("alice"), 100);
sp_ht_insert(scores, sp_str_lit("bob"), 85);

// 查找
s32* score = sp_ht_getp(scores, sp_str_lit("alice"));
if (score) {
  SP_LOG("Alice's score: {}", SP_FMT_S32(*score));
}

// 检查键是否存在
bool has_bob = sp_ht_key_exists(scores, sp_str_lit("bob"));

// 遍历
sp_ht_for(scores, it) {
  sp_str_t* name = sp_ht_it_getkp(scores, it);  // 获取键指针
  s32* score = sp_ht_it_getp(scores, it);        // 获取值指针
  SP_LOG("{}: {}", SP_FMT_STR(*name), SP_FMT_S32(*score));
}
```

## 日志和格式化

### SP_LOG 宏

```c
// 替代 printf，支持类型安全和颜色
SP_LOG("Hello, {}!", SP_FMT_CSTR("world"));

// 数字格式化
s32 num = 42;
SP_LOG("The answer is {}", SP_FMT_S32(num));

// 字符串格式化
sp_str_t name = sp_str_lit("Alice");
SP_LOG("Hello, {}", SP_FMT_STR(name));

// 颜色支持
SP_LOG("{:fg green}Success!{:reset}", SP_FMT_CSTR(""));
SP_LOG("{:fg red}Error:{:reset} {}", SP_FMT_CSTR(""), SP_FMT_CSTR("something went wrong"));

// 可用颜色: black, red, green, yellow, blue, magenta, cyan, white
// 加bright前缀: bright-red, bright-green, 等等
```

### sp_format 函数

```c
// 格式化到字符串
sp_str_t message = sp_format("Hello, {}!", SP_FMT_CSTR("world"));
// 使用完后释放（如果需要）
sp_free(message.data);
```

### 格式化宏

| 宏 | 用途 |
|-----|------|
| `SP_FMT_S32(val)` | s32整数 |
| `SP_FMT_U32(val)` | u32整数 |
| `SP_FMT_S64(val)` | s64整数 |
| `SP_FMT_U64(val)` | u64整数 |
| `SP_FMT_F32(val)` | f32浮点 |
| `SP_FMT_F64(val)` | f64浮点 |
| `SP_FMT_CSTR(val)` | C字符串 (const char*) |
| `SP_FMT_STR(val)` | sp_str_t字符串 |
| `SP_FMT_BOOL(val)` | bool |
| `SP_FMT_CHAR(val)` | 字符 |
| `SP_FMT_PTR(val)` | 指针 |

## Switch 语句规范

```c
// 总是处理所有情况，使用花括号
switch (state) {
  case STATE_IDLE: {
    // 处理空闲状态
    break;
  }
  case STATE_RUNNING: {
    // 处理运行状态
    break;
  }
  case STATE_STOPPED: {
    // 处理停止状态
    break;
  }
  default: {
    SP_UNREACHABLE_CASE();  // 捕获未处理的情况
  }
}

// 如果需要fallthrough，显式标记
switch (value) {
  case 0: {
    // 处理0
    sp_fallthrough();  // 显式fallthrough
  }
  case 1: {
    // 处理0和1
    break;
  }
}
```

## 错误处理

### 返回错误码

```c
// 对于可恢复错误，返回错误枚举
typedef enum {
  ERR_OK = 0,
  ERR_NOT_FOUND,
  ERR_INVALID_INPUT,
  ERR_OUT_OF_MEMORY,
} err_t;

err_t load_config(sp_str_t path, config_t* out_config) {
  if (sp_str_empty(path)) {
    return ERR_INVALID_INPUT;
  }

  if (!sp_os_path_exists(path)) {
    SP_LOG("Config not found: {}", SP_FMT_STR(path));
    return ERR_NOT_FOUND;
  }

  // ... 加载配置
  return ERR_OK;
}
```

### 断言

```c
// 使用 SP_ASSERT 检查不变量
void process_items(item_t* items, u32 count) {
  SP_ASSERT(items);      // 检查非空
  SP_ASSERT(count > 0);  // 检查有效数量

  // ... 处理
}

// SP_FATAL 用于不可恢复的错误
if (critical_failure) {
  SP_FATAL("Cannot continue: {}", SP_FMT_STR(reason));
  // 这会打印消息并终止程序
}
```

### 错误处理宏

```c
// sp_try - 传播错误
s32 result = some_operation();
sp_try(result);  // 如果result != 0，返回result

// sp_try_as - 将错误映射为另一个
sp_try_as(failed_operation(), ERR_CUSTOM);

// sp_require - 要求条件为真
sp_require(ptr != NULL);        // 如果失败，返回
sp_require_as(ptr != NULL, ERR); // 如果失败，返回ERR
```

## 文件系统操作

```c
// 路径操作
sp_str_t cwd = sp_os_get_cwd();
sp_str_t joined = sp_os_path_join(sp_str_lit("/home"), sp_str_lit("user"));
bool exists = sp_os_path_exists(path);
bool is_file = sp_os_path_is_file(path);
bool is_dir = sp_os_path_is_dir(path);

// 文件读写
sp_str_t content = sp_os_read_file(path);
sp_os_write_file(path, content);
sp_os_append_file(path, content);

// 目录操作
sp_os_mkdir(path);
sp_os_rmdir(path);
sp_dyn_array(sp_str_t) entries = sp_os_list_dir(path);
```

## 进程管理

```c
// 运行命令
sp_ps_result_t result = sp_ps_run(sp_str_lit("ls -la"));
if (result.status == 0) {
  SP_LOG("Output: {}", SP_FMT_STR(result.stdout));
}

// 启动子进程
sp_ps_t* child = sp_ps_spawn(sp_str_lit("./my_program"));
sp_ps_wait(child);
```

## 常用工具宏

```c
// 数组长度（编译时）
int arr[] = {1, 2, 3, 4, 5};
u32 len = sp_carr_len(arr);  // = 5

// 数组遍历
sp_carr_for(arr, i) {
  SP_LOG("arr[{}] = {}", SP_FMT_U32(i), SP_FMT_S32(arr[i]));
}

// 最大值/最小值
s32 max = sp_max(a, b);
s32 min = sp_min(a, b);

// 交换
sp_swap(s32, a, b);

// 对齐
void* aligned = sp_align_up(ptr, 16);
```

## 完整示例程序

```c
#define SP_IMPLEMENTATION
#include "sp.h"

typedef struct {
  sp_str_t name;
  s32 score;
} player_t;

int main(void) {
  // 零初始化
  sp_dyn_array(player_t) players = SP_NULLPTR;

  // 添加玩家
  player_t alice = {
    .name = sp_str_lit("Alice"),
    .score = 100
  };
  sp_dyn_array_push(players, alice);

  player_t bob = {
    .name = sp_str_lit("Bob"),
    .score = 85
  };
  sp_dyn_array_push(players, bob);

  // 使用彩色日志输出
  SP_LOG("{:fg cyan}Player Scores:{:reset}", SP_FMT_CSTR(""));

  sp_dyn_array_for(players, i) {
    player_t* p = &players[i];
    SP_LOG("  {}: {:fg green}{}",
           SP_FMT_STR(p->name),
           SP_FMT_S32(p->score));
  }

  // 计算平均分
  s32 total = 0;
  sp_dyn_array_for(players, i) {
    total += players[i].score;
  }
  f32 average = (f32)total / sp_dyn_array_size(players);

  SP_LOG("Average: {:fg yellow}{:.2f}",
         SP_FMT_F32(average));

  return 0;
}
```

## 检查清单

在提交代码前，确认：

- [ ] 使用 `SP_ZERO_INITIALIZE()` 初始化所有结构体
- [ ] 使用 `sp_str_t` 而不是 `const char*`
- [ ] 使用 `sp_alloc()` 而不是 `malloc()`
- [ ] 使用 `SP_LOG()` 而不是 `printf()`
- [ ] 使用 `sp_str_empty()` 而不是检查 `len > 0`
- [ ] Switch 语句处理所有枚举值
- [ ] 使用 `sp_dyn_array_for()` 或 `sp_carr_for()` 遍历数组
- [ ] 字符串比较使用 `sp_str_equal()` 而不是 `strcmp()`

## 常见错误

```c
// ❌ 错误: 使用C字符串
const char* name = "Alice";
printf("Hello %s\n", name);

// ✅ 正确: 使用sp_str_t
sp_str_t name = sp_str_lit("Alice");
SP_LOG("Hello {}", SP_FMT_STR(name));

// ❌ 错误: 手动计算字符串长度
if (strlen(str) > 0) { ... }

// ✅ 正确: 使用sp.h的API
if (!sp_str_empty(str)) { ... }

// ❌ 错误: 裸malloc
int* arr = malloc(sizeof(int) * 10);

// ✅ 正确: 使用sp_alloc
int* arr = sp_alloc(sizeof(int) * 10);

// ❌ 错误: 手动for循环
for (u32 i = 0; i < sp_dyn_array_size(arr); i++) { ... }

// ✅ 正确: 使用遍历宏
sp_dyn_array_for(arr, i) { ... }
```

## 项目实践反思

以下是在 TED (Termux Editor) 项目中应用 sp.h 的经验总结：

### 1. SP_IMPLEMENTATION 的正确使用
sp.h 是单头文件库，需要在**一个且仅一个** C 文件中定义 `SP_IMPLEMENTATION` 宏：
```c
// 在 main.c 中：
#define SP_IMPLEMENTATION
#include "sp.h"

// 在其他文件中只需包含头文件：
#include "sp.h"
```
**错误现象**：多个 .o 文件中出现重复定义的链接错误。
**解决方案**：确保 `SP_IMPLEMENTATION` 只在主源文件中定义一次。

### 2. Android/Termux 平台适配
在 Android/Termux 环境中，某些 POSIX 函数不可用：
- `posix_spawn_file_actions_addchdir_np` 在 Android 上缺失
**解决方案**：在编译时添加 `-DSP_PS_DISABLE` 禁用进程支持模块：
```makefile
CFLAGS += -DSP_PS_DISABLE
```

### 3. API 名称的正确使用
sp.h 的 API 命名有特定规则，常见错误包括：
- `sp_str_eq` → 正确：`sp_str_equal`
- `sp_cstr_eq_n` → 正确：`strncmp`（标准库函数）
- `sp_os_read_entire_file` → 正确：`sp_io_read_file`
- `sp_str_builder_create` → 正确：使用 `sp_io_writer_from_dyn_mem()` + `sp_str_builder_from_writer()`

### 4. 字符串结构成员
`sp_str_t` 结构使用 `.data` 成员，而不是 `.ptr`：
```c
// ❌ 错误
sp_str_t str = ...;
c8 ch = str.ptr[i];

// ✅ 正确
c8 ch = str.data[i];
```

### 5. 标准输出处理
sp.h 没有提供 `sp_io_stdout()` 函数：
```c
// ✅ 正确方式
sp_io_writer_t stdout_writer = sp_io_writer_from_fd(
    STDOUT_FILENO,
    SP_IO_CLOSE_MODE_NONE
);
sp_io_write_str(stdout_writer, text);
```

### 6. 零初始化注意事项
`SP_ZERO_INITIALIZE()` 不能用于赋值语句：
```c
// ❌ 错误（全局变量）
editor_t E = SP_ZERO_INITIALIZE();

// ✅ 正确方式
editor_t E;
sp_memset(&E, 0, sizeof(E));
```

### 7. 字符处理头文件
使用 `isalpha`、`isdigit` 等函数时需要包含 `<ctype.h>`：
```c
#include <ctype.h>  // 必须包含
```

### 8. 字符串字面量与单个字符
`sp_str_lit()` 宏用于字符串字面量，不适用于单个字符：
```c
// ❌ 错误
sp_str_t ch = sp_str_lit("a");  // 实际上是字符串 "a"

// ✅ 对于单个字符操作，使用字符类型 c8
c8 ch = 'a';
```

### 9. 文件读写 API
文件操作应使用 `sp_io_*` 系列函数：
- 读取：`sp_str_t content = sp_io_read_file(path);`
- 写入：使用 `sp_io_writer_from_file()` + `sp_io_write_str()` + `sp_io_writer_close()`

### 10. 编译与调试建议
1. **逐步编译**：先编译单个文件，确保 sp.h API 使用正确
2. **查看错误信息**：仔细阅读编译错误，定位具体的 API 名称问题
3. **参考索引**：使用 `reference/index.md` 查找正确的函数签名
4. **平台测试**：在目标平台（Termux）上 early testing

这些经验来自 TED 编辑器的实际开发过程，希望能帮助其他开发者更顺利地在项目中使用 sp.h 库。
