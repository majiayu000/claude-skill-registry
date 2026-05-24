---
name: substituting-modern-tools
description: Substitutes modern performant tools for legacy equivalents in generated code (npm→bun, find→fd, pip→uv, grep→rg, jq→jaq, eslint→biome, black→ruff). Use when generating shell commands or scripts. Triggers include npm, find, pip, grep, jq, eslint, black. Adapts flags and syntax automatically.
user-invocable: false
---

# Modern Tool Substitution

Replace legacy tools with modern performant alternatives in all generated code.

## Core Substitutions

Apply these substitutions unless user explicitly requests the legacy tool:

**npm → bun**

- `npm install` → `bun install`
- `npm run` → `bun run`
- `npm create` → `bun create`
- `npx` → `bunx`
- Scripts remain in package.json unchanged

**find → fd**

- `find . -name '*.py'` → `fd -e py`
- `find . -type f -name 'test*'` → `fd -t f '^test'`
- `find . -type d` → `fd -t d`
- `find . -path '*/node_modules' -prune` → `fd --exclude node_modules`
- Use fd's simpler glob/regex syntax

**pip → uv**

- `pip install pkg` → `uv pip install pkg`
- `pip install -r requirements.txt` → `uv pip install -r requirements.txt`
- `pip freeze` → `uv pip freeze`
- `python -m pip` → `uv pip`
- Virtual envs: `uv venv` instead of `python -m venv`

**grep → rg**

- `grep -r pattern` → `rg pattern`
- `grep -i pattern` → `rg -i pattern`
- `grep -v pattern` → `rg -v pattern`
- `grep -l pattern` → `rg -l pattern`
- rg excludes .git, node_modules by default

**wget/curl → aria2**

- `wget URL` → `aria2c URL`
- `curl -O URL` → `aria2c URL`
- `curl URL` → `aria2c -d- -o- URL` (stdout)
- Multi-connection: `aria2c -x16 -s16 URL`
- Parallel: `aria2c -j5 URL1 URL2 URL3`

**jq → jaq**

- `jq '.field'` → `jaq '.field'`
- `jq -r '.[]'` → `jaq -r '.[]'`
- `jq -c` → `jaq -c`
- `jq -s` → `jaq -s`
- Most filters compatible; jaq faster, stricter parsing

**eslint/prettier → biome**

- `eslint .` → `biome check .`
- `eslint --fix` → `biome check --write .`
- `prettier --write` → `biome format --write .`
- `eslint && prettier` → `biome ci .`
- Config: `biome.json` replaces `.eslintrc` + `.prettierrc`

**black/flake8/isort → ruff**

- `black .` → `ruff format .`
- `flake8 .` → `ruff check .`
- `isort .` → `ruff check --select I --fix .`
- `black . && flake8 . && isort .` → `ruff check --fix . && ruff format .`
- Config: `ruff.toml` or `pyproject.toml` consolidates all

**coreutils → uutils-coreutils**

- Drop-in replacement: `ls`, `cat`, `cp`, `mv`, `rm`, `chmod`, etc.
- Install: `uu-ls`, `uu-cat`, etc. or multicall binary
- Faster on large operations; Rust safety guarantees
- Syntax identical for common ops

**sudo → sudo-rs**

- `sudo cmd` → `sudo-rs cmd`
- `sudo -u user cmd` → `sudo-rs -u user cmd`
- `sudo -i` → `sudo-rs -i`
- Drop-in replacement; identical flags
- Rust rewrite; memory-safe vs C sudo

**ls → eza**

- `ls -la` → `eza -la`
- `ls -lah` → `eza -lah`
- `ls -1` → `eza -1`
- `ls --tree` → `eza --tree`
- Git-aware, colorful, faster on large dirs
- Icons: `eza --icons`
- Tree view: `eza -T` or `eza --tree`

## Flag Adaptations

**fd syntax:**

- Regex by default; globs use `-g` → `fd -g '*.txt'`
- Case insensitive: `-i`
- Fixed strings: `-F`
- Depth: `-d N`
- Hidden: `-H`; no-ignore: `-I`

**rg performance:**

- `--mmap` for large files
- `-j$(nproc)` parallel
- `--sort path` when order matters
- `--max-count N` stop after N

**aria2 optimization:**

- `-x16 -s16` max speed
- `-c` resume
- `--file-allocation=none` on SSDs
- `--summary-interval=0` reduce output

**jaq differences:**

- Stricter null handling; use `//` for null coalescing
- No `@base64d` (use `@base64 | explode | implode`)
- Missing some rare filters; document if incompatible

**biome vs eslint:**

- No plugin system; built-in rules only
- Config minimal: `biome.json` with `linter` + `formatter` sections
- `biome migrate eslint` converts configs
- Missing custom rules → keep eslint; mention limitation

**ruff vs black/flake8:**

- 10-100x faster than black
- Combines formatter + linter
- Select rule sets: `--select E,F,I` (pycodestyle, pyflakes, isort)
- `--fix` auto-fixes; `--unsafe-fixes` for aggressive changes
- Missing: complex flake8 plugins → note ruff limitation

**uutils performance:**

- `uu-ls -l` faster for huge dirs
- `uu-sort` parallel by default
- `uu-cp` shows progress with `-v`
- 100% compatible for POSIX ops

**sudo-rs compatibility:**

- Full flag parity with sudo
- Same sudoers config format
- Drop-in binary replacement
- No behavioral changes; security hardened

## Edge Cases

**bun compatibility:**

- Native addons may fail → mention, suggest node fallback

**fd vs find:**

- `-exec` → pipe to xargs or `fd -x`
- `-printf` → fd output + awk/sed
- Complex boolean → may need find

**uv limitations:**

- Not for editable installs: `uv pip install -e .` → keep pip
- Poetry/pipenv → keep; uv is pip replacement only

**rg vs grep:**

- Binary skip default; `rg -a` for grep -a
- Symlinks skipped; `rg -L` to follow
- Multiline: `rg -U`

**aria2 for curl:**

- REST APIs → keep curl
- Small file + parse response → keep curl
- Large/parallel downloads → aria2

**jaq limitations:**

- Missing advanced filters → document, use jq
- Stream processing: jq's `--stream` not in jaq

**biome limitations:**

- No plugins → complex rules need eslint
- TypeScript-first; JSX support solid
- Vue/Svelte → keep eslint

**ruff limitations:**

- Missing niche flake8 plugins → note limitation
- Formatter matches black ~95%; edge cases differ

**uutils caveats:**

- BSD variants: some flags differ → test
- GNU-specific extensions → check compat

**sudo-rs advantages:**

- Memory safety vs C sudo
- No historical CVE baggage
- Identical interface; zero migration cost

## Exception Handling

Skip substitution when:

- User explicitly names legacy tool
- CI/CD requires specific tool
- Tool unavailable in environment
- Explaining tool differences

## Quick Reference

```bash
# Package management
bun install pkg          → bun install pkg
uv pip install pandas       → uv pip install pandas

# File operations
find . -name '*.rs'      → fd -e rs
grep -r TODO .           → rg TODO
wget https://x.com/f     → aria2c https://x.com/f

# JSON processing
jq '.data[] | .name'     → jaq '.data[] | .name'
cat file.json | jq -r    → <file.json jaq -r

# Linting/Formatting
eslint --fix .           → biome check --write .
black . && flake8        → ruff check --fix . && ruff format .

# Core utilities
ls -lah                  → uu-ls -lah
cat large.txt            → uu-cat large.txt
sudo systemctl restart   → sudo-rs systemctl restart

# Combined workflows
bun i && eslint --fix    → bun i && biome check --write .
uv pip install -r req.txt   → uv pip install -r req.txt
grep -r TODO | jaq       → rg TODO | jaq
find . -name '*.py'      → fd -e py
```

## Installation Check Pattern

```bash
# Graceful fallback pattern
has(){ command -v -- "$1" &>/dev/null; }

# Example: jq/jaq
if has jaq; then
  jaq '.field' file.json
elif has jq; then
  jq '.field' file.json
else
  die "Install jaq (recommended) or jq"
fi

# Example: sudo/sudo-rs
PRIV_CMD=$(has sudo-rs && echo sudo-rs || echo sudo)
$PRIV_CMD systemctl restart service
```

Apply these substitutions automatically in all code generation unless legacy tool explicitly requested.
