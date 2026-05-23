---
description: Skill for reviewing shell scripts with shell-neutral behavior with best efforts.
name: shell-script-review
---

Currently, all the mainstream operating systems are using Bash as their default shell.
However, many programmers like Zsh for its better interactive features.

Below we list several common different behaviors between Bash and Zsh, along with
workarounds to write shell-neutral scripts that work in both shells.

## DO NOT over checking!

```bash
if [ -f XXX ] then
   ...
fi
```

Suspecting everything itself is suspicious: If the file checked is a well committed file in this repo, **DO NOT** check for it existence at all!
If you are not sure, use `git ls-files XXX` to check if it is tracked by git.

Similarly for environment variables, check `setup.sh` and `session-init.sh` to see if these variables are always set by those scripts.
If so, **DO NOT** `-z` or `-n` check them!


## Array Indexing

```bash
arr=(apple banana cherry)
echo ${arr[0]}  # apple
echo ${arr[1]}  # banana
```

```zsh
arr=(apple banana cherry)
echo ${arr[1]}  # apple
echo ${arr[2]}  # banana
```

### Shell-neutral workaround:

#### Option 1: Force ksh-style arrays in zsh
```zsh
#!/bin/bash  # or #!/bin/zsh
[ -n "$ZSH_VERSION" ] && setopt KSH_ARRAYS
arr=(apple banana cherry)
echo ${arr[0]}  # apple in both
```

#### Option 2: Avoid use traversal
```zsh
for item in "${arr[@]}"; do
    echo "$item"
done
```

Additionally, when parsing positional arguments, extract them to variables directly:
```bash
for item in "$@"; do
    case $item in
        --option)
            option_value="$2"
            shift 2
            ;;
        *)
            positional_args+=("$item")
            shift
            ;;
    esac
done
```

## Script Path Detection

```bash
echo "$0"              # /path/to/script.sh (or bash if sourced)
echo "${BASH_SOURCE[0]}"  # /path/to/script.sh (always reliable)
```

```zsh
echo "$0"              # /path/to/script.sh (or function name if sourced!)
echo "${(%):-%x}"      # /path/to/script.sh (reliable)
# BASH_SOURCE doesn't exist in zsh
```

### Shell-neutral workaround:

A reliable way to get the script path in both shells:
```bash
#!/bin/bash
# Get script path reliably in both shells
if [ -n "$BASH_SOURCE" ]; then
    SCRIPT_PATH="${BASH_SOURCE[0]}"
elif [ -n "$ZSH_VERSION" ]; then
    SCRIPT_PATH="${(%):-%x}"
else
    SCRIPT_PATH="$0"
fi

SCRIPT_DIR="$(dirname "$SCRIPT_PATH")"
echo "Script location: $SCRIPT_DIR"
```

Another option is to reply on environment variables exported by `setup.sh` and we use
absolute paths based on those or absolute paths by `git rev-parse`.

## Variable Expansion & Word Splitting

```bash
var="one two three"
echo $var       # one two three (3 arguments, split!)
echo "$var"     # one two three (1 argument, safe)

for word in $var; do echo "$word"; done
# Outputs: one / two / three
```

```zsh
var="one two three"
echo $var       # one two three (1 argument, NO split by default!)
echo "$var"     # one two three (1 argument)

for word in $var; do echo "$word"; done
# Outputs: one two three (as single item!)


# Need explicit splitting in zsh:
for word in ${=var}; do echo "$word"; done
# Outputs: one / two / three
```

### Shell-neutral workaround:

```bash
#!/bin/bash
# Always quote variables for safety
var="one two three"
echo "$var"

# For intentional splitting, use arrays:
read -ra words <<< "$var"
for word in "${words[@]}"; do
    echo "$word"
done
```

## Globbing

```bash
# Recursive glob needs enabling
shopt -s globstar
echo **/*.txt

# No ** support without the option
echo *.txt  # Only current directory
```

```zsh
# Recursive glob works by default
echo **/*.txt

# Advanced patterns
echo **/*.txt~*test*  # Exclude files with 'test'
echo *.txt(.)         # Only regular files
```

### Shell-neutral workaround:

```bash
#!/bin/bash
# Option 1: Use find instead of globs
find . -name "*.txt" -type f

# Option 2: Enable globstar in bash, works in zsh by default
if [ -n "$BASH_VERSION" ]; then
    shopt -s globstar
fi
echo **/*.txt

# Option 3: Stick to simple globs
echo *.txt
```

## Arrays & Associative Arrays

Bash:
```bash
# Indexed array
arr=(a b c)
echo ${arr[0]}  # a

# Associative array
declare -A map
map[key1]="value1"
map[key2]="value2"
echo ${map[key1]}  # value1
```

Zsh:
```zsh
# Indexed array (1-based!)
arr=(a b c)
echo ${arr[1]}  # a

# Associative array (different syntax)
typeset -A map
map=(key1 value1 key2 value2)
# OR
map[key1]="value1"
echo ${map[key1]}  # value1
```

### Shell-neutral workaround:
```bash
#!/bin/bash
# Force bash-compatible arrays in zsh
[ -n "$ZSH_VERSION" ] && setopt KSH_ARRAYS

# Now arrays work the same way
arr=(a b c)
echo ${arr[0]}  # a in both

# For associative arrays, use bash syntax
declare -A map 2>/dev/null || typeset -A map  # Works in both
map[key1]="value1"
echo ${map[key1]}

## PATH Variable
```zsh
local path="screwed"
echo $PATH # screwed
```

In zsh, `$path` is an array view of the PATH variable, which can lead to confusion.
In bash, `$path` is just a regular variable.

Solution: Always use `$PATH` for environment variable access, and avoid using `$path` as variable name!

## Key Recommendations

1. Use `#!/bin/bash` as shebang (more portable)
2. Add setopt KSH_ARRAYS at the top if you must support zsh
3. Always quote variables: `"$var"` not `$var`
4. Use `"${arr[@]}"` for array expansion
5. Use the script path template for reliable path detection
6. Use find instead of complex globs for portability
7. Avoid using `$path` as in zsh, it is different view of the sameting, `$PATH`
