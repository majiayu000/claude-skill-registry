---
name: string-manipulation-mastery
description: Advanced bash string manipulation including parameter expansion, pattern matching, regex, and text processing (2025)
---

## CRITICAL GUIDELINES

### Windows File Path Requirements

**MANDATORY: Always Use Backslashes on Windows for File Paths**

When using Edit or Write tools on Windows, you MUST use backslashes (`\`) in file paths, NOT forward slashes (`/`).

---

# Bash String Manipulation Mastery (2025)

## Overview

Comprehensive guide to string manipulation in bash using parameter expansion, pattern matching, regular expressions, and built-in transformations. Master these techniques to avoid spawning external processes like `sed`, `awk`, or `cut` for simple operations.

## Parameter Expansion Basics

### String Length

```bash
#!/usr/bin/env bash
set -euo pipefail

str="Hello, World!"

# Get length
echo "${#str}"  # 13

# Length of array element
arr=("short" "much longer string")
echo "${#arr[0]}"  # 5
echo "${#arr[1]}"  # 18

# Number of array elements (not string length)
echo "${#arr[@]}"  # 2
```

### Substring Extraction

```bash
#!/usr/bin/env bash
set -euo pipefail

str="Hello, World!"

# ${var:offset} - from offset to end
echo "${str:7}"     # World!

# ${var:offset:length} - from offset, length chars
echo "${str:0:5}"   # Hello
echo "${str:7:5}"   # World

# Negative offset (from end) - note the space or parentheses
echo "${str: -6}"      # World!
echo "${str:(-6)}"     # World!
echo "${str: -6:5}"    # World

# Last N characters
last_n() {
    local str="$1" n="$2"
    echo "${str: -$n}"
}
last_n "Hello" 3  # llo

# Extract between positions
between() {
    local str="$1" start="$2" end="$3"
    echo "${str:start:$((end - start))}"
}
between "0123456789" 3 7  # 3456
```

### Default Values

```bash
#!/usr/bin/env bash
set -euo pipefail

# ${var:-default} - use default if unset or empty
name="${1:-Anonymous}"
echo "Hello, $name"

# ${var:=default} - assign default if unset or empty
: "${CONFIG_FILE:=/etc/app.conf}"

# ${var:+alternate} - use alternate if var IS set
debug_flag="${DEBUG:+--verbose}"

# ${var:?error} - exit with error if unset or empty
: "${REQUIRED_VAR:?REQUIRED_VAR must be set}"

# Without colon - only checks if unset (empty is OK)
# ${var-default}, ${var=default}, ${var+alt}, ${var?err}

# Practical example: config with defaults
setup_config() {
    : "${DB_HOST:=localhost}"
    : "${DB_PORT:=5432}"
    : "${DB_NAME:=myapp}"
    : "${DB_USER:=postgres}"
}
```

### Indirect Expansion

```bash
#!/usr/bin/env bash
set -euo pipefail

# ${!var} - indirect reference
config_host="server.example.com"
config_port="8080"

key="config_host"
echo "${!key}"  # server.example.com

# Iterate over related variables
for suffix in host port; do
    var="config_$suffix"
    echo "$suffix = ${!var}"
done

# Get all variable names matching pattern
# ${!prefix@} or ${!prefix*}
for var in "${!config_@}"; do
    echo "$var = ${!var}"
done

# Array indirection
arr=(a b c d e)
idx=2
echo "${arr[$idx]}"  # c

# Indirect array reference (Bash 4.3+ nameref)
get_array_element() {
    local -n arr_ref="$1"
    local idx="$2"
    echo "${arr_ref[$idx]}"
}
get_array_element arr 3  # d
```

## Pattern Matching

### Prefix Removal

```bash
#!/usr/bin/env bash
set -euo pipefail

path="/home/user/documents/file.tar.gz"

# ${var#pattern} - remove shortest prefix match
echo "${path#*/}"     # home/user/documents/file.tar.gz

# ${var##pattern} - remove longest prefix match
echo "${path##*/}"    # file.tar.gz (basename)

# Remove extension
filename="archive.tar.gz"
echo "${filename#*.}"   # tar.gz (first . onwards)
echo "${filename##*.}"  # gz (last extension only)

# Remove prefix string
url="https://example.com/path"
echo "${url#https://}"  # example.com/path

# Practical: Get file extension
get_extension() {
    local file="$1"
    echo "${file##*.}"
}

# Practical: Strip leading zeros
strip_leading_zeros() {
    local num="$1"
    echo "${num#"${num%%[!0]*}"}"
}
strip_leading_zeros "000123"  # 123
```

### Suffix Removal

```bash
#!/usr/bin/env bash
set -euo pipefail

path="/home/user/documents/file.tar.gz"

# ${var%pattern} - remove shortest suffix match
echo "${path%/*}"     # /home/user/documents (dirname)

# ${var%%pattern} - remove longest suffix match
echo "${path%%/*}"    # (empty - removes everything)

# Remove extension
filename="archive.tar.gz"
echo "${filename%.*}"   # archive.tar
echo "${filename%%.*}"  # archive

# Practical: Get directory
dirname="${path%/*}"

# Practical: Remove file extension
basename="${path##*/}"
name_without_ext="${basename%.*}"

# Combined: Change extension
change_extension() {
    local file="$1" new_ext="$2"
    echo "${file%.*}.$new_ext"
}
change_extension "doc.txt" "md"  # doc.md
```

### Pattern Substitution

```bash
#!/usr/bin/env bash
set -euo pipefail

str="hello hello hello"

# ${var/pattern/replacement} - replace first match
echo "${str/hello/hi}"     # hi hello hello

# ${var//pattern/replacement} - replace all matches
echo "${str//hello/hi}"    # hi hi hi

# ${var/#pattern/replacement} - replace if at start
echo "${str/#hello/hi}"    # hi hello hello

# ${var/%pattern/replacement} - replace if at end
echo "${str/%hello/goodbye}"  # hello hello goodbye

# Delete pattern (empty replacement)
echo "${str//hello/}"      # "   " (just spaces)

# Practical: Sanitize filename
sanitize_filename() {
    local name="$1"
    # Replace spaces with underscores
    name="${name// /_}"
    # Remove special characters
    name="${name//[^a-zA-Z0-9._-]/}"
    echo "$name"
}
sanitize_filename "My File (2024).txt"  # My_File_2024.txt

# Practical: Path manipulation
normalize_path() {
    local path="$1"
    # Remove double slashes
    while [[ "$path" == *//* ]]; do
        path="${path//\/\//\/}"
    done
    # Remove trailing slash
    echo "${path%/}"
}
```

## Case Transformation

### Basic Case Changes

```bash
#!/usr/bin/env bash
set -euo pipefail

str="Hello World"

# Lowercase first character
echo "${str,}"      # hello World

# Lowercase all
echo "${str,,}"     # hello world

# Uppercase first character
echo "${str^}"      # Hello World (already uppercase)

str2="hello world"
echo "${str2^}"     # Hello world

# Uppercase all
echo "${str,,}"     # hello world
echo "${str2^^}"    # HELLO WORLD

# Toggle case (Bash 4.4+)
echo "${str~~}"     # hELLO wORLD
```

### Pattern-Based Case Changes

```bash
#!/usr/bin/env bash
set -euo pipefail

str="hello world"

# Uppercase only matching pattern
echo "${str^^[aeiou]}"  # hEllO wOrld

# Lowercase only matching pattern
str2="HELLO WORLD"
echo "${str2,,[AEIOU]}"  # HeLLo WoRLD

# Practical: Title case
title_case() {
    local str="$1"
    local result=""
    local capitalize=true

    for ((i=0; i<${#str}; i++)); do
        local char="${str:$i:1}"
        if [[ "$char" == " " ]]; then
            result+="$char"
            capitalize=true
        elif $capitalize; then
            result+="${char^}"
            capitalize=false
        else
            result+="${char,}"
        fi
    done

    echo "$result"
}
title_case "hello WORLD from BASH"  # Hello World From Bash
```

## Regular Expressions

### Bash Regex Matching

```bash
#!/usr/bin/env bash
set -euo pipefail

# =~ operator for regex matching
str="Hello World 123"

if [[ "$str" =~ ^Hello ]]; then
    echo "Starts with Hello"
fi

if [[ "$str" =~ [0-9]+ ]]; then
    echo "Contains numbers"
fi

# Capture groups with BASH_REMATCH
email="user@example.com"
if [[ "$email" =~ ^([^@]+)@(.+)$ ]]; then
    echo "User: ${BASH_REMATCH[1]}"    # user
    echo "Domain: ${BASH_REMATCH[2]}"  # example.com
    echo "Full match: ${BASH_REMATCH[0]}"  # user@example.com
fi

# Store regex in variable (avoids quoting issues)
pattern='^[0-9]{4}-[0-9]{2}-[0-9]{2}$'
date="2024-03-15"
if [[ "$date" =~ $pattern ]]; then
    echo "Valid date format"
fi

# Multiple capture groups
log_line='2024-03-15 10:30:45 ERROR Connection failed'
pattern='^([0-9-]+) ([0-9:]+) ([A-Z]+) (.+)$'
if [[ "$log_line" =~ $pattern ]]; then
    date="${BASH_REMATCH[1]}"
    time="${BASH_REMATCH[2]}"
    level="${BASH_REMATCH[3]}"
    message="${BASH_REMATCH[4]}"
fi
```

### Practical Regex Patterns

```bash
#!/usr/bin/env bash
set -euo pipefail

# Email validation
is_valid_email() {
    local email="$1"
    local pattern='^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    [[ "$email" =~ $pattern ]]
}

# IP address validation
is_valid_ip() {
    local ip="$1"
    local octet='(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'
    local pattern="^${octet}\.${octet}\.${octet}\.${octet}$"
    [[ "$ip" =~ $pattern ]]
}

# URL parsing
parse_url() {
    local url="$1"
    local pattern='^(https?|ftp)://([^/:]+)(:([0-9]+))?(/.*)?$'

    if [[ "$url" =~ $pattern ]]; then
        echo "Protocol: ${BASH_REMATCH[1]}"
        echo "Host: ${BASH_REMATCH[2]}"
        echo "Port: ${BASH_REMATCH[4]:-default}"
        echo "Path: ${BASH_REMATCH[5]:-/}"
    else
        echo "Invalid URL" >&2
        return 1
    fi
}

# Semantic version parsing
parse_semver() {
    local version="$1"
    local pattern='^v?([0-9]+)\.([0-9]+)\.([0-9]+)(-([a-zA-Z0-9.-]+))?(\+([a-zA-Z0-9.-]+))?$'

    if [[ "$version" =~ $pattern ]]; then
        echo "Major: ${BASH_REMATCH[1]}"
        echo "Minor: ${BASH_REMATCH[2]}"
        echo "Patch: ${BASH_REMATCH[3]}"
        echo "Prerelease: ${BASH_REMATCH[5]:-none}"
        echo "Build: ${BASH_REMATCH[7]:-none}"
    fi
}
```

## String Splitting and Joining

### Split String to Array

```bash
#!/usr/bin/env bash
set -euo pipefail

# Using IFS and read
str="one,two,three,four"

IFS=',' read -ra arr <<< "$str"
echo "${arr[0]}"  # one
echo "${arr[2]}"  # three

# Multi-character delimiter (using parameter expansion)
str="one||two||three"
arr=()
while [[ "$str" == *"||"* ]]; do
    arr+=("${str%%||*}")
    str="${str#*||}"
done
arr+=("$str")

# Using mapfile (newline-delimited)
mapfile -t lines <<< "$(echo -e "line1\nline2\nline3")"

# Split on any whitespace
str="one   two     three"
read -ra arr <<< "$str"  # IFS defaults to whitespace
```

### Join Array to String

```bash
#!/usr/bin/env bash
set -euo pipefail

arr=("one" "two" "three" "four")

# Join with delimiter using IFS
join_by() {
    local IFS="$1"
    shift
    echo "$*"
}
join_by ',' "${arr[@]}"  # one,two,three,four
join_by ' | ' "${arr[@]}"  # one | two | three | four

# Alternative using printf
join_array() {
    local delim="$1"
    shift
    local first="$1"
    shift
    printf '%s' "$first" "${@/#/$delim}"
}
join_array ',' "${arr[@]}"

# Join with custom format
printf '"%s" ' "${arr[@]}"  # "one" "two" "three" "four"
printf '%s\n' "${arr[@]}"   # One per line
```

## Text Processing Without External Commands

### Trim Whitespace

```bash
#!/usr/bin/env bash
set -euo pipefail

# Trim leading whitespace
trim_leading() {
    local str="$1"
    echo "${str#"${str%%[![:space:]]*}"}"
}

# Trim trailing whitespace
trim_trailing() {
    local str="$1"
    echo "${str%"${str##*[![:space:]]}"}"
}

# Trim both
trim() {
    local str="$1"
    str="${str#"${str%%[![:space:]]*}"}"
    str="${str%"${str##*[![:space:]]}"}"
    echo "$str"
}

# Extended pattern matching version (requires shopt -s extglob)
trim_extglob() {
    shopt -s extglob
    local str="$1"
    str="${str##+([[:space:]])}"
    str="${str%%+([[:space:]])}"
    echo "$str"
}

str="   hello world   "
trim "$str"  # "hello world"
```

### String Repetition

```bash
#!/usr/bin/env bash
set -euo pipefail

# Repeat string N times
repeat() {
    local str="$1"
    local n="$2"
    local result=""

    for ((i=0; i<n; i++)); do
        result+="$str"
    done

    echo "$result"
}

repeat "ab" 5  # ababababab

# Using printf
repeat_printf() {
    local str="$1"
    local n="$2"
    printf '%s' $(printf '%.0s'"$str" $(seq 1 "$n"))
}

# Create separator line
separator() {
    local char="${1:--}"
    local width="${2:-80}"
    printf '%*s\n' "$width" '' | tr ' ' "$char"
}

separator "=" 40  # ========================================
```

### Character Replacement

```bash
#!/usr/bin/env bash
set -euo pipefail

str="hello world"

# Using tr-like replacement via expansion
# Replace all 'l' with 'L'
echo "${str//l/L}"  # heLLo worLd

# Delete characters
echo "${str//o/}"   # hell wrld

# Translate character by character
translate() {
    local str="$1"
    local from="$2"
    local to="$3"

    for ((i=0; i<${#from}; i++)); do
        str="${str//${from:$i:1}/${to:$i:1}}"
    done

    echo "$str"
}

translate "hello" "el" "ip"  # hippo
```

### Padding and Alignment

```bash
#!/usr/bin/env bash
set -euo pipefail

# Right pad to width
pad_right() {
    local str="$1"
    local width="$2"
    local char="${3:- }"
    printf "%-${width}s" "$str" | tr ' ' "$char"
}

# Left pad to width
pad_left() {
    local str="$1"
    local width="$2"
    local char="${3:- }"
    printf "%${width}s" "$str" | tr ' ' "$char"
}

# Center align
center() {
    local str="$1"
    local width="$2"
    local len=${#str}
    local padding=$(( (width - len) / 2 ))

    printf "%*s%s%*s" $padding "" "$str" $((width - len - padding)) ""
}

# Zero-pad numbers
zero_pad() {
    local num="$1"
    local width="$2"
    printf "%0${width}d" "$num"
}

zero_pad 42 5  # 00042

# Format table
print_table_row() {
    printf "| %-20s | %10s | %-15s |\n" "$1" "$2" "$3"
}

print_table_row "Name" "Age" "City"
print_table_row "Alice" "30" "New York"
```

## Extended Globbing

### Enable and Use

```bash
#!/usr/bin/env bash
set -euo pipefail
shopt -s extglob

# Extended patterns:
# ?(pattern) - 0 or 1 occurrence
# *(pattern) - 0 or more occurrences
# +(pattern) - 1 or more occurrences
# @(pattern) - exactly 1 occurrence
# !(pattern) - anything except pattern

# Match files
ls *.@(jpg|png|gif)      # Images only
ls !(*.bak|*.tmp)        # Exclude backup/temp files
ls +([0-9]).txt          # Files starting with digits

# String manipulation
str="   hello   world   "

# Remove leading whitespace
echo "${str##+([[:space:]])}"  # "hello   world   "

# Remove all whitespace
echo "${str//+([[:space:]])/ }"  # " hello world "

# Remove multiple extensions
file="archive.tar.gz.bak"
echo "${file%.@(tar|gz|bak)*}"  # archive

# Match alternatives
case "$response" in
    @(yes|y|Y|YES))
        echo "Affirmative"
        ;;
    @(no|n|N|NO))
        echo "Negative"
        ;;
esac
```

### Practical Extended Glob Patterns

```bash
#!/usr/bin/env bash
set -euo pipefail
shopt -s extglob

# Clean backup files
rm -f *.@(bak|backup|orig|~)

# Find source files only
ls *.@(c|cpp|h|hpp|cc)

# Exclude certain patterns
for file in !(test_*|_*).py; do
    process "$file"
done

# Match complex version strings
version_pattern='+([0-9]).+([0-9]).+([0-9])?(-+([a-z0-9]))'
if [[ "$version" == $version_pattern ]]; then
    echo "Valid version"
fi

# Remove redundant characters
clean_string() {
    local str="$1"
    # Remove repeated spaces
    echo "${str//+([[:space:]])/ }"
}

# Match optional parts
file_pattern='*.@(test|spec)?.@(js|ts)'
# Matches: file.js, file.ts, file.test.js, file.spec.ts, etc.
```

## Bash 5.3+ String Features

### In-Shell Substitution for Strings

```bash
#!/usr/bin/env bash
# Requires Bash 5.3+
set -euo pipefail

# No-fork string operations
result=${ echo "${str^^}"; }  # Uppercase without subshell

# REPLY syntax for string building
build_path() {
    local parts=("$@")
    REPLY=""

    for part in "${parts[@]}"; do
        ${| REPLY+="${REPLY:+/}$part"; }
    done
}

# Efficient string accumulation
accumulate() {
    local -n result="$1"
    shift

    for item in "$@"; do
        ${| result+="$item"; }
    done
}
```

## Performance Tips

### Avoid Subshells for Simple Operations

```bash
#!/usr/bin/env bash
set -euo pipefail

str="hello world"

# ✗ SLOW - spawns external process
basename=$(basename "$path")
dirname=$(dirname "$path")
upper=$(echo "$str" | tr 'a-z' 'A-Z')
len=$(echo -n "$str" | wc -c)

# ✓ FAST - pure bash
basename="${path##*/}"
dirname="${path%/*}"
upper="${str^^}"
len="${#str}"
```

### Batch String Operations

```bash
#!/usr/bin/env bash
set -euo pipefail

# ✗ SLOW - multiple expansions
str="$input"
str="${str//  / }"
str="${str#"${str%%[![:space:]]*}"}"
str="${str%"${str##*[![:space:]]}"}"
str="${str,,}"

# ✓ BETTER - single function call
normalize_string() {
    local str="$1"
    str="${str//  / }"
    str="${str#"${str%%[![:space:]]*}"}"
    str="${str%"${str##*[![:space:]]}"}"
    echo "${str,,}"
}
result=$(normalize_string "$input")
```

## Resources

- [Bash Reference - Shell Parameter Expansion](https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html)
- [Bash Reference - Pattern Matching](https://www.gnu.org/software/bash/manual/html_node/Pattern-Matching.html)
- [BashFAQ/100 - String manipulation](https://mywiki.wooledge.org/BashFAQ/100)
- [Bash Hackers - Parameter Expansion](https://wiki.bash-hackers.org/syntax/pe)

---

**Master bash string manipulation to write efficient scripts without external dependencies.**
