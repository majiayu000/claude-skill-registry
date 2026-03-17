---
name: shell-scripting
description: Bash Shell 脚本编写
version: 1.0.0
author: terminal-skills
tags: [linux, bash, shell, scripting, automation]
---

# Shell 脚本编写

## 概述
Bash 脚本编写、调试、最佳实践等技能。

## 基础语法

### 脚本结构
```bash
#!/bin/bash
# 脚本描述
# Author: name
# Date: 2024-01-01

set -euo pipefail                   # 严格模式

# 变量定义
VAR="value"
readonly CONST="constant"

# 主逻辑
main() {
    echo "Hello, World!"
}

main "$@"
```

### 变量
```bash
# 定义变量
name="value"
name='literal value'                # 不解析变量

# 使用变量
echo $name
echo ${name}
echo "${name}_suffix"

# 默认值
${var:-default}                     # 未设置时使用默认值
${var:=default}                     # 未设置时赋值并使用
${var:+value}                       # 已设置时使用 value
${var:?error message}               # 未设置时报错

# 字符串操作
${#var}                             # 长度
${var:0:5}                          # 子串
${var#pattern}                      # 删除前缀
${var%pattern}                      # 删除后缀
${var/old/new}                      # 替换
```

### 数组
```bash
# 定义数组
arr=(a b c d)
arr[0]="first"

# 访问数组
${arr[0]}                           # 第一个元素
${arr[@]}                           # 所有元素
${#arr[@]}                          # 数组长度
${!arr[@]}                          # 所有索引

# 遍历数组
for item in "${arr[@]}"; do
    echo "$item"
done
```

## 流程控制

### 条件判断
```bash
# if 语句
if [[ condition ]]; then
    commands
elif [[ condition ]]; then
    commands
else
    commands
fi

# 条件表达式
[[ -f file ]]                       # 文件存在
[[ -d dir ]]                        # 目录存在
[[ -z "$var" ]]                     # 变量为空
[[ -n "$var" ]]                     # 变量非空
[[ "$a" == "$b" ]]                  # 字符串相等
[[ "$a" != "$b" ]]                  # 字符串不等
[[ $a -eq $b ]]                     # 数字相等
[[ $a -lt $b ]]                     # 小于
[[ $a -gt $b ]]                     # 大于

# 逻辑运算
[[ cond1 && cond2 ]]                # 与
[[ cond1 || cond2 ]]                # 或
[[ ! cond ]]                        # 非
```

### 循环
```bash
# for 循环
for i in 1 2 3 4 5; do
    echo $i
done

for i in {1..10}; do
    echo $i
done

for ((i=0; i<10; i++)); do
    echo $i
done

for file in *.txt; do
    echo "$file"
done

# while 循环
while [[ condition ]]; do
    commands
done

# 读取文件
while IFS= read -r line; do
    echo "$line"
done < file.txt

# until 循环
until [[ condition ]]; do
    commands
done
```

### case 语句
```bash
case "$var" in
    pattern1)
        commands
        ;;
    pattern2|pattern3)
        commands
        ;;
    *)
        default commands
        ;;
esac
```

## 函数

### 定义函数
```bash
# 方式1
function_name() {
    local var="local variable"
    echo "Arguments: $@"
    echo "First arg: $1"
    echo "Arg count: $#"
    return 0
}

# 方式2
function function_name {
    commands
}

# 调用函数
function_name arg1 arg2

# 获取返回值
result=$(function_name)
```

### 常用函数模板
```bash
# 日志函数
log() {
    local level=$1
    shift
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $*"
}

log INFO "This is info message"
log ERROR "This is error message"

# 错误处理
die() {
    echo "ERROR: $*" >&2
    exit 1
}

# 确认函数
confirm() {
    read -p "$1 [y/N] " response
    [[ "$response" =~ ^[Yy]$ ]]
}

if confirm "Continue?"; then
    echo "Proceeding..."
fi
```

## 输入输出

### 读取输入
```bash
# 读取用户输入
read -p "Enter name: " name
read -sp "Enter password: " password   # 隐藏输入
read -t 10 -p "Quick! " answer          # 超时

# 读取文件
while IFS= read -r line; do
    echo "$line"
done < file.txt
```

### 重定向
```bash
# 输出重定向
command > file                      # 覆盖
command >> file                     # 追加
command 2> error.log                # 错误输出
command > file 2>&1                 # 合并输出
command &> file                     # 同上

# 输入重定向
command < file

# Here Document
cat << EOF
多行文本
变量: $var
EOF

cat << 'EOF'                        # 不解析变量
原始文本
EOF
```

## 调试技巧

### 调试选项
```bash
# 启用调试
set -x                              # 打印执行的命令
set -v                              # 打印读取的行
set -e                              # 出错即退出
set -u                              # 未定义变量报错
set -o pipefail                     # 管道错误传递

# 组合使用
set -euxo pipefail

# 调试特定部分
set -x
# 调试代码
set +x
```

### 调试工具
```bash
# 语法检查
bash -n script.sh

# 调试运行
bash -x script.sh

# shellcheck 静态分析
shellcheck script.sh
```

## 最佳实践

### 脚本模板
```bash
#!/bin/bash
#
# Script: script_name.sh
# Description: Brief description
# Author: Your Name
# Date: 2024-01-01
#

set -euo pipefail

# Constants
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly SCRIPT_NAME="$(basename "$0")"

# Logging
log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }
error() { echo "[ERROR] $*" >&2; }
die() { error "$*"; exit 1; }

# Usage
usage() {
    cat << EOF
Usage: $SCRIPT_NAME [options] <arguments>

Options:
    -h, --help      Show this help message
    -v, --verbose   Enable verbose mode

Examples:
    $SCRIPT_NAME -v input.txt
EOF
}

# Parse arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                usage
                exit 0
                ;;
            -v|--verbose)
                VERBOSE=true
                shift
                ;;
            *)
                ARGS+=("$1")
                shift
                ;;
        esac
    done
}

# Main
main() {
    parse_args "$@"
    
    # Your logic here
    log "Starting $SCRIPT_NAME"
}

main "$@"
```

## 故障排查

| 问题 | 解决方法 |
|------|----------|
| 语法错误 | `bash -n script.sh` 检查 |
| 变量未定义 | 使用 `set -u` 或 `${var:-}` |
| 空格问题 | 变量加引号 `"$var"` |
| 管道错误被忽略 | 使用 `set -o pipefail` |
| 调试困难 | 使用 `set -x` 或 `shellcheck` |
