---
name: modern-bash
description: Modern Bash scripting with a functional programming mindset. Bash is essentially "string Lisp" - a language where everything is string manipulation, commands are functions, and pipelines are composition. Use when writing, refactoring, or analyzing Bash scripts with emphasis on static/dynamic semantics, functional patterns, and modern best practices.
---

# Modern Bash - The String Lisp

## Core Philosophy: Bash = String Lisp

Bash的本质是**字符串Lisp**:
- **一切都是字符串** - 变量、输出、参数都是字符串
- **命令即函数** - 每个命令都是纯函数 (stdin → stdout)
- **管道即组合** - `|` 是函数组合操作符
- **命令替换即求值** - `$(...)` 是表达式求值
- **重定向即副作用** - 显式管理副作用

```bash
# Lisp思维: (compose (map f) (filter g) xs)
# Bash表达:
seq 1 100 | xargs -n1 | while read n; do echo $((n * 2)); done

# 函数组合: (f (g x))
result=$(echo "$input" | grep pattern | wc -l)
```

## Agent Workflow

1. **静态语义检查** - 分析语法结构、作用域、变量绑定
2. **动态语义分析** - 理解执行流程、状态转换、副作用
3. **函数式重构** - 减少副作用，增加可组合性
4. **严格求值验证** - 确认参数展开、命令替换顺序
5. **边界处理** - 空值、空格、特殊字符的防御性处理

## Essential Patterns

### 1. 纯函数式命令 (Pure Functions)

```bash
# ✅ 纯函数: 相同输入→相同输出，无副作用
add() {
    echo $(( $1 + $2 ))
}
result=$(add 3 5)  # result = "8"

# ❌ 不纯函数: 有副作用
global_var=0
impure_add() {
    global_var=$(( global_var + $1 ))  # 修改外部状态
}
```

### 2. 字符串作为数据结构

```bash
# 列表表示 (字符串分割)
files="file1.txt file2.txt file3.txt"
for f in $files; do
    echo "Processing: $f"
done

# 关联数组 (Bash 4+)
declare -A config=(
    [host]="localhost"
    [port]="8080"
)
echo "${config[host]}:${config[port]}"
```

### 3. 管道组合 (Function Composition)

```bash
# 读取 → 过滤 → 转换 → 聚合
cat data.txt \
    | grep "ERROR" \
    | cut -d' ' -f3 \
    | sort \
    | uniq -c \
    | sort -rn

# 等同于 Lisp: (->> data (filter error?) (map extract) sort frequencies)
```

### 4. 命令替换作为表达式求值

```bash
# 严格求值: 先求值 $(seq 1 3)，再绑定到 for
for i in $(seq 1 3); do
    echo $i
done

# 惰性序列模拟 (进程替换)
while read line; do
    echo "Processing: $line"
done < <(generate_infinite_stream)
```

### 5. 词法作用域模拟

```bash
# 使用 local 创建词法作用域
process_file() {
    local filepath="$1"
    local filename=$(basename "$filepath")
    local temp_dir=$(mktemp -d)

    # 作用域内的私有变量
    local content
    content=$(cat "$filepath")

    # 清理 (类似 RAII)
    trap "rm -rf '$temp_dir'" EXIT

    # 处理逻辑...
}
```

## Static Semantics (静态语义)

### 词法分析

```bash
# Token 类别识别
KEYWORD: function, if, for, while, do, done, then, fi
IDENTIFIER: [a-zA-Z_][a-zA-Z0-9_]*
VARIABLE: $[0-9], $*, $@, $#, $?, $$, $!, $_, ${name}
SYMBOL: |, &, ;, (, ), {, }, <, >
```

### 作用域分析

```bash
# 全局作用域污染 (危险)
for i in $(seq 1 10); do
    : # i 泄漏到全局
    done

# ✅ 局部作用域
local_scope_demo() {
    local i           # 显式局部声明
    local count="${1:-10}"  # 默认参数

    for i in $(seq 1 "$count"); do
        echo $i
    done
}
```

### 类型系统 (弱类型检查)

```bash
# 运行时类型检查
assert_number() {
    [[ "$1" =~ ^[0-9]+$ ]] || {
        echo "Error: expected number, got '$1'" >&2
        return 1
    }
}

# 使用
add_safe() {
    assert_number "$1" && assert_number "$2" || return 1
    echo $(( $1 + $2 ))
}
```

## Dynamic Semantics (动态语义)

### 执行模型

```bash
# 小步语义示例: $(seq 1 $n)
# 1. 参数展开: $n → "3"
# 2. 命令替换: fork → exec seq → 捕获 stdout
# 3. 字段分割: IFS 分割为列表 ["1", "2", "3"]
# 4. 绑定到循环变量

for i in $(seq 1 $n); do
    echo $i
done
```

### 副作用管理

```bash
# 显式副作用: cd 改变进程状态
cd_up() {
    local n="${1:-1}"
    local i

    for i in $(seq 1 "$n"); do
        cd .. || return $?  # 错误传播
    done
}

# 无副作用版本: 输出路径而非改变状态
parent_dir() {
    local n="${1:-1}"
    local path="$PWD"
    local i

    for i in $(seq 1 "$n"); do
        path=$(dirname "$path")
    done
    echo "$path"
}
```

### 求值策略

```bash
# 严格求值 (Eager Evaluation)
# 所有参数在调用前完全求值
foo $(expensive_op) $(another_op)  # 两个都求值后才调用 foo

# 惰性求值模拟 (短路求值)
[[ -f "$file" ]] && process "$file"  # 只有文件存在时才处理

# 延迟求值 (引号)
cmd="echo hello"
eval "$cmd"  # 运行时求值
```

## Common Pitfalls

### 1. 未引用的变量展开

```bash
# ❌ 危险: 单词分割 + 通配符展开
file_list=$(ls)
for f in $file_list; do echo "$f"; done  # 文件名含空格会出问题

# ✅ 安全: 使用数组
file_list=(*)
for f in "${file_list[@]}"; do echo "$f"; done
```

### 2. 作用域泄漏

```bash
# ❌ 循环变量污染全局命名空间
for i in a b c; do :; done
echo "$i"  # 输出 "c"

# ✅ 使用函数 + local
safe_loop() {
    local i
    for i in a b c; do :; done
}
```

### 3. 整数溢出/类型问题

```bash
# Bash 整数有范围限制
echo $(( 2**63 ))  # 溢出

# 大数使用外部命令
result=$(echo "2^100" | bc)
```

### 4. 命令替换的尾部换行

```bash
# ❌ 丢失尾部换行
content=$(cat file.txt)  # 所有尾部换行被移除

# ✅ 保留换行 (使用 printf %s)
content=$(cat file.txt; echo x)
content=${content%x}
```

## Functional Utilities

### Map

```bash
map() {
    local func="$1"
    local item
    while IFS= read -r item; do
        "$func" "$item"
    done
}

double() { echo $(( $1 * 2 )); }

seq 1 10 | map double
```

### Filter

```bash
filter() {
    local predicate="$1"
    local item
    while IFS= read -r item; do
        "$predicate" "$item" && echo "$item"
    done
}

is_even() { (( $1 % 2 == 0 )); }

seq 1 10 | filter is_even
```

### Reduce / Fold

```bash
reduce() {
    local func="$1"
    local acc="$2"
    local item
    while IFS= read -r item; do
        acc=$("$func" "$acc" "$item")
    done
    echo "$acc"
}

sum() { echo $(( $1 + $2 )); }

seq 1 10 | reduce sum 0  # 55
```

## References

- [Static and Dynamic Semantics](references/semantics.md) - 形式化语义分析
- [Functional Patterns](references/functional.md) - 函数式编程模式
- [String Manipulation](references/strings.md) - 字符串处理技巧
