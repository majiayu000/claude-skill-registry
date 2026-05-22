---
name: refactoring-detection
description: リファクタリング候補検出のast-grepパターン、推定工数算出、言語別設定を定義
---

# リファクタリング検出スキル

`/find-refactoring`コマンドで使用する検出ロジック・パターンを定義。

---

## 前提ツール

| ツール | 必須/任意 | 用途 | インストール |
|--------|---------|------|-------------|
| `ast-grep (sg)` | **必須** | AST解析 | `cargo install ast-grep` / `brew install ast-grep` |
| `jscpd` | 任意 | 重複検出 | `npm install -g jscpd` |
| `jq` | **必須** | JSON処理 | `brew install jq` |
| `wc`, `grep` | **必須** | 基本検出 | 標準コマンド |

### ツール確認

```bash
check_required_tools() {
    local missing=()
    command -v sg &>/dev/null || missing+=("ast-grep (sg): cargo install ast-grep")
    command -v jq &>/dev/null || missing+=("jq: brew install jq")
    
    if [[ ${#missing[@]} -gt 0 ]]; then
        echo "Error: Missing required tools:"
        printf '  - %s\n' "${missing[@]}"
        return 1
    fi
    return 0
}

check_optional_tools() {
    if command -v jscpd &>/dev/null || command -v npx &>/dev/null; then
        echo "jscpd: available"
    else
        echo "jscpd: not available (duplicate detection skipped)"
    fi
}
```

---

## 言語検出

```bash
detect_language() {
    if [[ -f "package.json" ]]; then
        echo "typescript"
    elif [[ -f "Cargo.toml" ]]; then
        echo "rust"
    elif [[ -f "go.mod" ]]; then
        echo "go"
    elif [[ -f "pyproject.toml" ]] || [[ -f "requirements.txt" ]]; then
        echo "python"
    else
        echo "typescript"
    fi
}
```

### 言語別設定

| 言語 | 拡張子 | ast-grep lang | ファイル上限 | 関数上限 |
|------|--------|---------------|-------------|---------|
| TypeScript | `*.ts,*.tsx` | `typescript`/`tsx` | 500行 | 80行 |
| Rust | `*.rs` | `rust` | 500行 | 80行 |
| Go | `*.go` | `go` | 400行 | 60行 |
| Python | `*.py` | `python` | 400行 | 60行 |

---

## 検出パターン（TypeScript）

> **注意**: ast-grep出力は0-indexed。表示時に+1する。

### サイズ系

```bash
# 500行超過ファイル
find_large_files() {
    local target="$1"
    find "$target" -type f \( -name "*.ts" -o -name "*.tsx" \) \
        ! -path "*/node_modules/*" ! -path "*/.git/*" \
        -exec wc -l {} + 2>/dev/null | \
        awk '$1 > 500 && !/total$/ {printf "%s:%d:file_split\n", $2, $1}'
}

# 80行超過関数（function宣言）
find_large_functions_ts() {
    local target="$1"
    sg run --pattern 'function $NAME($$$) { $$$ }' --lang typescript "$target" --json 2>/dev/null | \
        jq -r '.[] | select(.range.end.line - .range.start.line > 80) | 
            "\(.file):\(.range.start.line + 1):\(.range.end.line - .range.start.line):func_split:\(.metaVariables.single.NAME.text // "anonymous")"'
}

# 80行超過アロー関数
find_large_arrow_functions() {
    local target="$1"
    sg run --pattern 'const $NAME = ($$$) => { $$$ }' --lang typescript "$target" --json 2>/dev/null | \
        jq -r '.[] | select(.range.end.line - .range.start.line > 80) | 
            "\(.file):\(.range.start.line + 1):\(.range.end.line - .range.start.line):func_split:\(.metaVariables.single.NAME.text)"'
}

# 6引数超関数
find_many_params() {
    local target="$1"
    sg run --pattern 'function $NAME($A, $B, $C, $D, $E, $F, $G, $$$) { $$$ }' \
        --lang typescript "$target" --json 2>/dev/null | \
        jq -r '.[] | "\(.file):\(.range.start.line + 1):7:many_params"'
}
```

### 型安全系

```bash
# any型使用（grep - ast-grepでは型注釈のマッチが困難）
find_any_types() {
    local target="$1"
    grep -rn --include="*.ts" --include="*.tsx" -E ':\s*any\b' "$target" 2>/dev/null | \
        grep -v node_modules | \
        while IFS=: read -r file line _; do
            echo "$file:$line:1:any_type"
        done
}

# @ts-ignore / @ts-expect-error
find_ts_ignore() {
    local target="$1"
    grep -rn --include="*.ts" --include="*.tsx" -E '@ts-ignore|@ts-expect-error' "$target" 2>/dev/null | \
        grep -v node_modules | \
        while IFS=: read -r file line _; do
            echo "$file:$line:1:ts_ignore"
        done
}
```

### エラー処理系

```bash
# 空catchブロック（try-catch全体でマッチ）
find_empty_catch() {
    local target="$1"
    sg run --pattern 'try { $$$ } catch ($E) { }' --lang typescript "$target" --json 2>/dev/null | \
        jq -r '.[] | "\(.file):\(.range.start.line + 1):1:empty_catch"'
}
```

### 品質系

```bash
# console.log残存（テスト・設定ファイル除外）
find_console_log() {
    local target="$1"
    sg run --pattern 'console.log($$$)' --lang typescript "$target" --json 2>/dev/null | \
        jq -r '.[] | select(
            (.file | test("\\.(spec|test)\\.(ts|tsx)$") | not) and
            (.file | test("(jest|vitest|eslint|prettier)\\.config") | not)
        ) | "\(.file):\(.range.start.line + 1):1:console_log"'
}
```

---

## 検出パターン（Rust）

```bash
# 80行超過関数
find_large_functions_rust() {
    local target="$1"
    sg run --pattern 'fn $NAME($$$) { $$$ }' --lang rust "$target" --json 2>/dev/null | \
        jq -r '.[] | select(.range.end.line - .range.start.line > 80) | 
            "\(.file):\(.range.start.line + 1):\(.range.end.line - .range.start.line):func_split:\(.metaVariables.single.NAME.text)"'
}

# unwrap()多用（1ファイル5箇所超）
find_unwrap_abuse() {
    local target="$1"
    sg run --pattern '$_.unwrap()' --lang rust "$target" --json 2>/dev/null | \
        jq -r 'group_by(.file) | .[] | select(length > 5) | 
            "\(.[0].file):1:\(length):unwrap_abuse"'
}

# todo!/unimplemented!残存
find_rust_todo() {
    local target="$1"
    grep -rn --include="*.rs" -E 'todo!|unimplemented!' "$target" 2>/dev/null | \
        while IFS=: read -r file line _; do
            echo "$file:$line:1:rust_todo"
        done
}
```

---

## 検出パターン（Go）

```bash
# 60行超過関数
find_large_functions_go() {
    local target="$1"
    sg run --pattern 'func $NAME($$$) { $$$ }' --lang go "$target" --json 2>/dev/null | \
        jq -r '.[] | select(.range.end.line - .range.start.line > 60) | 
            "\(.file):\(.range.start.line + 1):\(.range.end.line - .range.start.line):func_split:\(.metaVariables.single.NAME.text)"'
}

# panic残存
find_go_panic() {
    local target="$1"
    grep -rn --include="*.go" 'panic(' "$target" 2>/dev/null | \
        grep -v '_test.go' | \
        while IFS=: read -r file line _; do
            echo "$file:$line:1:go_panic"
        done
}
```

---

## 検出パターン（Python）

```bash
# 60行超過関数
find_large_functions_python() {
    local target="$1"
    sg run --pattern 'def $NAME($$$): $$$' --lang python "$target" --json 2>/dev/null | \
        jq -r '.[] | select(.range.end.line - .range.start.line > 60) | 
            "\(.file):\(.range.start.line + 1):\(.range.end.line - .range.start.line):func_split:\(.metaVariables.single.NAME.text)"'
}

# print残存（テストファイル除外）
find_python_print() {
    local target="$1"
    grep -rn --include="*.py" 'print(' "$target" 2>/dev/null | \
        grep -v test_ | grep -v _test.py | \
        while IFS=: read -r file line _; do
            echo "$file:$line:1:python_print"
        done
}
```

---

## 重複コード検出

```bash
find_duplicates() {
    local target="$1"
    local cmd=""
    
    if command -v jscpd &>/dev/null; then
        cmd="jscpd"
    elif command -v npx &>/dev/null; then
        cmd="npx jscpd"
    else
        return 0  # スキップ
    fi
    
    $cmd "$target" --min-lines 10 --reporters json --silent 2>/dev/null | \
        jq -r '.duplicates[]? | 
            "\(.firstFile.name):\(.firstFile.start):\(.firstFile.end - .firstFile.start):duplicate:\(.secondFile.name)"' 2>/dev/null || true
}
```

---

## 統合検出関数

```bash
run_all_detections() {
    local target="$1"
    local lang="$2"
    
    # 共通
    find_large_files "$target"
    
    case "$lang" in
        typescript)
            find_large_functions_ts "$target"
            find_large_arrow_functions "$target"
            find_many_params "$target"
            find_any_types "$target"
            find_ts_ignore "$target"
            find_empty_catch "$target"
            find_console_log "$target"
            ;;
        rust)
            find_large_functions_rust "$target"
            find_unwrap_abuse "$target"
            find_rust_todo "$target"
            ;;
        go)
            find_large_functions_go "$target"
            find_go_panic "$target"
            ;;
        python)
            find_large_functions_python "$target"
            find_python_print "$target"
            ;;
    esac
    
    find_duplicates "$target"
}
```

---

## 推定工数算出

| 問題タイプ | 変数 | 計算式 | 例 |
|-----------|------|--------|-----|
| file_split | 超過行数 | `(行数-500)*0.3`分 | 723行→67分 |
| func_split | 超過行数 | `(行数-80)*0.5`分 | 150行→35分 |
| any_type | 箇所数 | `箇所数*5`分 | 5箇所→25分 |
| empty_catch | 箇所数 | `箇所数*10`分 | 3箇所→30分 |
| ts_ignore | 箇所数 | `箇所数*15`分 | 2箇所→30分 |
| console_log | 箇所数 | `箇所数*2`分 | 10箇所→20分 |
| duplicate | 重複行数 | `行数*0.5`分 | 40行→20分 |
| many_params | 固定 | 20分 | - |
| unwrap_abuse | 箇所数 | `箇所数*3`分 | 10箇所→30分 |
| rust_todo | 箇所数 | `箇所数*10`分 | 3箇所→30分 |

```bash
estimate_effort() {
    local type="$1"
    local value="$2"
    local minutes=0
    
    case "$type" in
        file_split)     minutes=$(( (value - 500) * 3 / 10 )) ;;
        func_split)     minutes=$(( (value - 80) / 2 )) ;;
        any_type)       minutes=$(( value * 5 )) ;;
        empty_catch)    minutes=$(( value * 10 )) ;;
        ts_ignore)      minutes=$(( value * 15 )) ;;
        console_log)    minutes=$(( value * 2 )) ;;
        duplicate)      minutes=$(( value / 2 )) ;;
        many_params)    minutes=20 ;;
        unwrap_abuse)   minutes=$(( value * 3 )) ;;
        rust_todo|go_panic|python_print) minutes=$(( value * 10 )) ;;
        *)              minutes=30 ;;
    esac
    
    if [[ $minutes -lt 1 ]]; then minutes=5; fi
    
    if [[ $minutes -ge 60 ]]; then
        echo "$(( minutes / 60 ))h$(( minutes % 60 ))m"
    else
        echo "${minutes}m"
    fi
}
```

---

## Issue粒度チェック

```bash
estimate_work_lines() {
    local type="$1"
    local value="$2"
    
    case "$type" in
        file_split)     echo $(( (value - 500) / 3 )) ;;
        func_split)     echo $(( (value - 80) / 2 )) ;;
        any_type)       echo $(( value * 5 )) ;;
        empty_catch)    echo $(( value * 10 )) ;;
        ts_ignore)      echo $(( value * 15 )) ;;
        duplicate)      echo $(( value / 2 )) ;;
        *)              echo 50 ;;
    esac
}

needs_decompose() {
    local lines="$1"
    [[ "$lines" -gt 200 ]]
}
```

---

## 既存Issue重複チェック

```bash
get_existing_refactoring_issues() {
    gh issue list --label refactoring --state open \
        --json number,title,body --limit 100 2>/dev/null || echo "[]"
}

check_duplicate_issue() {
    local file_path="$1"
    local existing_issues="$2"
    
    echo "$existing_issues" | jq -r --arg fp "$file_path" \
        '.[] | select(.body | contains($fp)) | "#\(.number)"' | head -1
}
```

---

## 優先度判定

| 優先度 | ルール |
|--------|--------|
| Critical | `ts_ignore` |
| High | `file_split`, `func_split`, `any_type`, `empty_catch`, `rust_todo`, `go_panic` |
| Medium | `duplicate`, `many_params`, `console_log`, `unwrap_abuse`, `python_print` |
| Low | その他 |

```bash
get_priority() {
    local type="$1"
    case "$type" in
        ts_ignore)      echo "critical" ;;
        file_split|func_split|any_type|empty_catch|rust_todo|go_panic) 
                        echo "high" ;;
        duplicate|many_params|console_log|unwrap_abuse|python_print)
                        echo "medium" ;;
        *)              echo "low" ;;
    esac
}
```
