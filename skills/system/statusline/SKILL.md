---
name: statusline
description: Configure Claude Code's terminal status line display
version: 1.0.0
---

# Statusline Implementation

Complete reference for building Claude Code status line scripts with themes, modules, and helpers.

## Themes

Five built-in themes with consistent indicator mappings:

### Theme: default

Standard emoji theme - works in all modern terminals.

```bash
# Status indicators (3-level: good/warn/critical)
STATUS_OK="🟢"
STATUS_WARN="🟡"
STATUS_CRIT="🔴"

# Status indicators (4-level: good/fair/warn/critical)
STATUS_4_OK="🟢"
STATUS_4_FAIR="🔵"
STATUS_4_WARN="🟡"
STATUS_4_CRIT="🔴"

# Module icons
ICON_DIR="📁"
ICON_MODEL="🤖"
ICON_CONTEXT="📊"
ICON_GIT="🌿"
ICON_COST="💰"
ICON_RATE="⚡"
ICON_PROJECT="📦"
ICON_LINES="📝"
ICON_BATTERY="🔋"
ICON_CPU="💻"
ICON_MEM="🧠"
ICON_DOCKER="🐳"
ICON_TIME="🕐"
ICON_CCA="☁️"

# Separators
SEP=" | "
```

### Theme: minimal

Geometric shapes - clean and compact.

```bash
STATUS_OK="◦"
STATUS_WARN="○"
STATUS_CRIT="●"
STATUS_4_OK="◦"
STATUS_4_FAIR="◦"
STATUS_4_WARN="○"
STATUS_4_CRIT="●"

ICON_DIR="→"
ICON_MODEL=""
ICON_CONTEXT=""
ICON_GIT="⎇"
ICON_COST="$"
ICON_RATE="~"
ICON_PROJECT=""
ICON_LINES="±"
ICON_BATTERY="◐"
ICON_CPU=""
ICON_MEM=""
ICON_DOCKER="◫"
ICON_TIME=""
ICON_CCA="☁"

SEP=" "
```

### Theme: vibrant

Bold, colorful emoji - high visibility.

```bash
STATUS_OK="💚"
STATUS_WARN="💛"
STATUS_CRIT="🧡"
STATUS_4_OK="💚"
STATUS_4_FAIR="💙"
STATUS_4_WARN="💛"
STATUS_4_CRIT="❤️"

ICON_DIR="📂"
ICON_MODEL="🤖"
ICON_CONTEXT="🎯"
ICON_GIT="🔀"
ICON_COST="💵"
ICON_RATE="⚡"
ICON_PROJECT="🚀"
ICON_LINES="✏️"
ICON_BATTERY="🔌"
ICON_CPU="🖥️"
ICON_MEM="💾"
ICON_DOCKER="🐋"
ICON_TIME="⏰"
ICON_CCA="🌐"

SEP=" │ "
```

### Theme: monochrome

ASCII only - maximum compatibility.

```bash
STATUS_OK="[OK]"
STATUS_WARN="[~~]"
STATUS_CRIT="[!!]"
STATUS_4_OK="[OK]"
STATUS_4_FAIR="[--]"
STATUS_4_WARN="[~~]"
STATUS_4_CRIT="[!!]"

ICON_DIR="DIR:"
ICON_MODEL=""
ICON_CONTEXT="CTX:"
ICON_GIT="GIT:"
ICON_COST="$"
ICON_RATE="RATE:"
ICON_PROJECT="PRJ:"
ICON_LINES="+/-"
ICON_BATTERY="BAT:"
ICON_CPU="CPU:"
ICON_MEM="MEM:"
ICON_DOCKER="DOCK:"
ICON_TIME=""
ICON_CCA="CCA:"

SEP=" | "
```

### Theme: nerd

Nerd Font glyphs - requires [Nerd Fonts](https://www.nerdfonts.com/).

```bash
STATUS_OK=""
STATUS_WARN=""
STATUS_CRIT=""
STATUS_4_OK=""
STATUS_4_FAIR=""
STATUS_4_WARN=""
STATUS_4_CRIT=""

ICON_DIR=""
ICON_MODEL="󰚩"
ICON_CONTEXT=""
ICON_GIT=""
ICON_COST="󰄛"
ICON_RATE=""
ICON_PROJECT=""
ICON_LINES=""
ICON_BATTERY=""
ICON_CPU=""
ICON_MEM=""
ICON_DOCKER=""
ICON_TIME=""
ICON_CCA=""

SEP="  "
```

---

## Helper Functions

### get_status (3-level)

Returns status indicator based on percentage threshold.

```bash
get_status() {
  local pct=$1
  local warn_threshold=${2:-50}
  local crit_threshold=${3:-75}

  if (( pct >= crit_threshold )); then
    echo "$STATUS_CRIT"
  elif (( pct >= warn_threshold )); then
    echo "$STATUS_WARN"
  else
    echo "$STATUS_OK"
  fi
}
```

### get_status_4level (4-level)

Returns status indicator with fair level (for rate limits).

```bash
get_status_4level() {
  local pct=$1
  local fair_threshold=${2:-25}
  local warn_threshold=${3:-50}
  local crit_threshold=${4:-75}

  if (( pct >= crit_threshold )); then
    echo "$STATUS_4_CRIT"
  elif (( pct >= warn_threshold )); then
    echo "$STATUS_4_WARN"
  elif (( pct >= fair_threshold )); then
    echo "$STATUS_4_FAIR"
  else
    echo "$STATUS_4_OK"
  fi
}
```

### progress_bar

Creates visual progress bar.

```bash
progress_bar() {
  local pct=$1
  local width=${2:-10}
  local filled=$(( pct * width / 100 ))
  local empty=$(( width - filled ))

  printf "["
  printf "%${filled}s" | tr ' ' '='
  printf "%${empty}s" | tr ' ' '-'
  printf "]"
}
```

### safe_int

Safely converts value to integer.

```bash
safe_int() {
  local val="$1"
  local default="${2:-0}"

  # Remove decimal portion and non-numeric chars
  val="${val%%.*}"
  val="${val//[^0-9-]/}"

  if [[ "$val" =~ ^-?[0-9]+$ ]]; then
    echo "$val"
  else
    echo "$default"
  fi
}
```

### json_get

Safe JSON extraction (handles missing jq gracefully).

```bash
json_get() {
  local json="$1"
  local path="$2"
  local default="${3:-}"

  if command -v jq &>/dev/null; then
    local result
    result=$(echo "$json" | jq -r "$path // empty" 2>/dev/null)
    echo "${result:-$default}"
  else
    echo "$default"
  fi
}
```

---

## Modules

### Module: directory

Current directory name (basename only).

```bash
# --- directory ---
get_directory() {
  local dir
  dir=$(json_get "$INPUT" '.workspace.current_dir')
  if [ -n "$dir" ]; then
    echo "${ICON_DIR}$(basename "$dir")"
  fi
}
DIRECTORY=$(get_directory)
```

### Module: model

Claude model display name.

```bash
# --- model ---
get_model() {
  local model
  model=$(json_get "$INPUT" '.model.display_name' 'Claude')
  # Shorten common names
  case "$model" in
    "Claude Opus 4.5") echo "${ICON_MODEL}Opus4.5" ;;
    "Claude Sonnet 4") echo "${ICON_MODEL}Sonnet4" ;;
    "Claude Haiku 3.5") echo "${ICON_MODEL}Haiku3.5" ;;
    *) echo "${ICON_MODEL}${model}" ;;
  esac
}
MODEL=$(get_model)
```

### Module: context

Context window usage with optional progress bar.

```bash
# --- context ---
get_context() {
  local pct
  pct=$(json_get "$INPUT" '.context_window.used_percentage' '0')
  pct=$(safe_int "$pct")

  local status
  status=$(get_status "$pct" 50 75)

  if [ "$DISPLAY_MODE" = "verbose" ]; then
    local bar
    bar=$(progress_bar "$pct" 10)
    echo "${ICON_CONTEXT}${bar} ${pct}%${status}"
  else
    echo "${ICON_CONTEXT}${pct}%${status}"
  fi
}
CONTEXT=$(get_context)
```

### Module: git

Branch name and status indicators.

```bash
# --- git ---
get_git() {
  local dir
  dir=$(json_get "$INPUT" '.workspace.current_dir')
  [ -z "$dir" ] && return

  local branch
  branch=$(cd "$dir" 2>/dev/null && git branch --show-current 2>/dev/null) || return
  [ -z "$branch" ] && return

  local status_indicator=""
  if [ "$DISPLAY_MODE" != "compact" ]; then
    # Check for uncommitted changes
    if cd "$dir" && ! git diff --quiet 2>/dev/null; then
      status_indicator="*"
    fi
    # Check for staged changes
    if cd "$dir" && ! git diff --cached --quiet 2>/dev/null; then
      status_indicator="${status_indicator}+"
    fi
  fi

  echo "${ICON_GIT}${branch}${status_indicator}"
}
GIT=$(get_git)
```

### Module: cost

Session cost in USD.

```bash
# --- cost ---
get_cost() {
  local cost
  cost=$(json_get "$INPUT" '.total_cost_usd' '0')

  # Skip if zero or empty
  [ "$cost" = "0" ] || [ -z "$cost" ] && return

  # Format based on magnitude
  if (( $(echo "$cost >= 1" | bc -l 2>/dev/null || echo 0) )); then
    printf "${ICON_COST}\$%.2f" "$cost"
  else
    printf "${ICON_COST}\$%.3f" "$cost"
  fi
}
COST=$(get_cost)
```

### Module: rate-limits

API usage via OAuth token (5h/7d limits).

```bash
# --- rate-limits ---
get_rate_limits() {
  # Get OAuth token from Claude config
  local token_file="$HOME/.claude/.credentials"
  [ ! -f "$token_file" ] && return

  local access_token
  access_token=$(jq -r '.oauth.accessToken // empty' "$token_file" 2>/dev/null)
  [ -z "$access_token" ] && return

  # Fetch usage (with timeout)
  local usage
  usage=$(curl -s --max-time 2 \
    -H "Authorization: Bearer $access_token" \
    "https://api.claude.ai/api/usage" 2>/dev/null)
  [ -z "$usage" ] && return

  # Parse usage (example fields - adjust based on actual API)
  local hour_pct day_pct
  hour_pct=$(echo "$usage" | jq -r '.fiveHourUsagePercent // 0' 2>/dev/null)
  day_pct=$(echo "$usage" | jq -r '.sevenDayUsagePercent // 0' 2>/dev/null)

  hour_pct=$(safe_int "$hour_pct")
  day_pct=$(safe_int "$day_pct")

  local hour_status day_status
  hour_status=$(get_status_4level "$hour_pct" 25 50 75)
  day_status=$(get_status_4level "$day_pct" 25 50 75)

  echo "${ICON_RATE}5h:${hour_pct}%${hour_status} 7d:${day_pct}%${day_status}"
}
RATE_LIMITS=$(get_rate_limits)
```

### Module: project

Detect project type by manifest files.

```bash
# --- project ---
get_project() {
  local dir
  dir=$(json_get "$INPUT" '.workspace.current_dir')
  [ -z "$dir" ] && return

  # Priority order - check most specific first
  if [ -f "$dir/Cargo.toml" ]; then
    echo "${ICON_PROJECT}Rust"
  elif [ -f "$dir/go.mod" ]; then
    echo "${ICON_PROJECT}Go"
  elif [ -f "$dir/pyproject.toml" ] || [ -f "$dir/setup.py" ]; then
    echo "${ICON_PROJECT}Python"
  elif [ -f "$dir/package.json" ]; then
    # Check for specific frameworks
    if [ -f "$dir/next.config.js" ] || [ -f "$dir/next.config.mjs" ]; then
      echo "${ICON_PROJECT}Next.js"
    elif [ -f "$dir/nuxt.config.ts" ] || [ -f "$dir/nuxt.config.js" ]; then
      echo "${ICON_PROJECT}Nuxt"
    elif [ -f "$dir/vite.config.ts" ] || [ -f "$dir/vite.config.js" ]; then
      echo "${ICON_PROJECT}Vite"
    elif [ -f "$dir/tsconfig.json" ]; then
      echo "${ICON_PROJECT}TypeScript"
    else
      echo "${ICON_PROJECT}Node"
    fi
  elif [ -f "$dir/Gemfile" ]; then
    echo "${ICON_PROJECT}Ruby"
  elif [ -f "$dir/pom.xml" ] || [ -f "$dir/build.gradle" ]; then
    echo "${ICON_PROJECT}Java"
  elif [ -f "$dir/composer.json" ]; then
    echo "${ICON_PROJECT}PHP"
  elif [ -f "$dir/mix.exs" ]; then
    echo "${ICON_PROJECT}Elixir"
  elif [ -f "$dir/pubspec.yaml" ]; then
    echo "${ICON_PROJECT}Dart"
  fi
}
PROJECT=$(get_project)
```

### Module: lines-changed

Lines added/removed in current session (approximation via git).

```bash
# --- lines-changed ---
get_lines_changed() {
  local dir
  dir=$(json_get "$INPUT" '.workspace.current_dir')
  [ -z "$dir" ] && return

  cd "$dir" 2>/dev/null || return

  # Get diff stats (staged + unstaged)
  local stats
  stats=$(git diff --stat HEAD 2>/dev/null | tail -1)
  [ -z "$stats" ] && return

  # Parse "X files changed, Y insertions(+), Z deletions(-)"
  local insertions deletions
  insertions=$(echo "$stats" | grep -oE '[0-9]+ insertion' | grep -oE '[0-9]+' || echo 0)
  deletions=$(echo "$stats" | grep -oE '[0-9]+ deletion' | grep -oE '[0-9]+' || echo 0)

  [ "$insertions" = "0" ] && [ "$deletions" = "0" ] && return

  echo "${ICON_LINES}+${insertions}/-${deletions}"
}
LINES_CHANGED=$(get_lines_changed)
```

### Module: battery (macOS)

Battery percentage with charging indicator.

```bash
# --- battery ---
get_battery() {
  # macOS only
  [ "$(uname)" != "Darwin" ] && return

  local battery_info
  battery_info=$(pmset -g batt 2>/dev/null)
  [ -z "$battery_info" ] && return

  local pct charging
  pct=$(echo "$battery_info" | grep -oE '[0-9]+%' | head -1 | tr -d '%')
  [ -z "$pct" ] && return

  charging=""
  echo "$battery_info" | grep -q "charging" && charging="+"
  echo "$battery_info" | grep -q "AC Power" && charging="⚡"

  local status
  # Battery: low is critical (inverted thresholds)
  if (( pct <= 10 )); then
    status="$STATUS_CRIT"
  elif (( pct <= 25 )); then
    status="$STATUS_WARN"
  else
    status="$STATUS_OK"
  fi

  echo "${ICON_BATTERY}${pct}%${charging}${status}"
}
BATTERY=$(get_battery)
```

### Module: cpu

CPU usage percentage.

```bash
# --- cpu ---
get_cpu() {
  local cpu_pct

  if [ "$(uname)" = "Darwin" ]; then
    # macOS
    cpu_pct=$(top -l 1 -n 0 2>/dev/null | grep "CPU usage" | awk '{print int($3)}')
  else
    # Linux
    cpu_pct=$(top -bn1 2>/dev/null | grep "Cpu(s)" | awk '{print int($2)}')
  fi

  [ -z "$cpu_pct" ] && return

  local status
  status=$(get_status "$cpu_pct" 50 80)

  echo "${ICON_CPU}${cpu_pct}%${status}"
}
CPU=$(get_cpu)
```

### Module: memory

RAM usage percentage.

```bash
# --- memory ---
get_memory() {
  local mem_pct

  if [ "$(uname)" = "Darwin" ]; then
    # macOS - approximate from vm_stat
    local page_size pages_free pages_active pages_speculative pages_wired
    page_size=$(pagesize 2>/dev/null || echo 4096)

    local vm_stats
    vm_stats=$(vm_stat 2>/dev/null)
    pages_free=$(echo "$vm_stats" | awk '/Pages free/ {gsub(/\./,""); print $3}')
    pages_active=$(echo "$vm_stats" | awk '/Pages active/ {gsub(/\./,""); print $3}')
    pages_speculative=$(echo "$vm_stats" | awk '/Pages speculative/ {gsub(/\./,""); print $3}')
    pages_wired=$(echo "$vm_stats" | awk '/Pages wired/ {gsub(/\./,""); print $4}')

    local total_mem used_mem
    total_mem=$(sysctl -n hw.memsize 2>/dev/null)
    used_mem=$(( (pages_active + pages_wired) * page_size ))

    [ -z "$total_mem" ] || [ "$total_mem" = "0" ] && return
    mem_pct=$(( used_mem * 100 / total_mem ))
  else
    # Linux
    mem_pct=$(free 2>/dev/null | awk '/Mem:/ {printf "%.0f", $3/$2 * 100}')
  fi

  [ -z "$mem_pct" ] && return

  local status
  status=$(get_status "$mem_pct" 60 85)

  echo "${ICON_MEM}${mem_pct}%${status}"
}
MEMORY=$(get_memory)
```

### Module: docker

Running container count.

```bash
# --- docker ---
get_docker() {
  command -v docker &>/dev/null || return

  local count
  count=$(docker ps -q 2>/dev/null | wc -l | tr -d ' ')

  [ "$count" = "0" ] && return

  echo "${ICON_DOCKER}${count}"
}
DOCKER=$(get_docker)
```

### Module: time

Current time display.

```bash
# --- time ---
get_time() {
  if [ "$DISPLAY_MODE" = "verbose" ]; then
    echo "${ICON_TIME}$(date '+%Y-%m-%d %H:%M')"
  else
    echo "${ICON_TIME}$(date '+%H:%M')"
  fi
}
TIME=$(get_time)
```

### Module: cca-status

Claude Code Anywhere status.

```bash
# --- claude-code-anywhere status ---
get_cca_status() {
  local port_file="$HOME/.config/claude-code-anywhere/port"
  [ ! -f "$port_file" ] && return

  local port
  port=$(cat "$port_file" 2>/dev/null)
  [ -z "$port" ] && return

  # Check if service is responding
  local status
  if curl -s --max-time 1 "http://127.0.0.1:${port}/health" &>/dev/null; then
    status="${STATUS_OK}"
  else
    status="${STATUS_WARN}"
  fi

  echo "${ICON_CCA}CCA${status}"
}
CCA_STATUS=$(get_cca_status)
```

---

## Complete Template

Full statusline.sh script template. When generating, include only enabled modules.

```bash
#!/bin/bash
# Claude Code Status Line Script
# Generated by /bluera-base:statusline
# Theme: {{THEME}}
# Modules: {{MODULES}}
# Display Mode: {{DISPLAY_MODE}}

set -e

# Read JSON input
read -r INPUT

# === THEME: {{THEME}} ===
{{THEME_VARS}}

# === DISPLAY MODE ===
DISPLAY_MODE="{{DISPLAY_MODE}}"

# === HELPER FUNCTIONS ===

get_status() {
  local pct=$1
  local warn_threshold=${2:-50}
  local crit_threshold=${3:-75}

  if (( pct >= crit_threshold )); then
    echo "$STATUS_CRIT"
  elif (( pct >= warn_threshold )); then
    echo "$STATUS_WARN"
  else
    echo "$STATUS_OK"
  fi
}

get_status_4level() {
  local pct=$1
  local fair_threshold=${2:-25}
  local warn_threshold=${3:-50}
  local crit_threshold=${4:-75}

  if (( pct >= crit_threshold )); then
    echo "$STATUS_4_CRIT"
  elif (( pct >= warn_threshold )); then
    echo "$STATUS_4_WARN"
  elif (( pct >= fair_threshold )); then
    echo "$STATUS_4_FAIR"
  else
    echo "$STATUS_4_OK"
  fi
}

progress_bar() {
  local pct=$1
  local width=${2:-10}
  local filled=$(( pct * width / 100 ))
  local empty=$(( width - filled ))

  printf "["
  printf "%${filled}s" | tr ' ' '='
  printf "%${empty}s" | tr ' ' '-'
  printf "]"
}

safe_int() {
  local val="$1"
  local default="${2:-0}"
  val="${val%%.*}"
  val="${val//[^0-9-]/}"
  if [[ "$val" =~ ^-?[0-9]+$ ]]; then
    echo "$val"
  else
    echo "$default"
  fi
}

json_get() {
  local json="$1"
  local path="$2"
  local default="${3:-}"
  if command -v jq &>/dev/null; then
    local result
    result=$(echo "$json" | jq -r "$path // empty" 2>/dev/null)
    echo "${result:-$default}"
  else
    echo "$default"
  fi
}

# === MODULES ===
{{MODULE_CODE}}

# === OUTPUT ===
OUTPUT=""
{{OUTPUT_ASSEMBLY}}

echo "$OUTPUT"
```

---

## File Operations (REQUIRED)

After generating the statusline script, you MUST complete these steps:

1. **Determine config directory**:

   ```bash
   CLAUDE_CONFIG="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
   ```

2. **Backup existing statusline** (if present):

   ```bash
   if [ -f "$CLAUDE_CONFIG/statusline.sh" ]; then
       BACKUP_TS=$(date +%Y%m%d-%H%M%S)
       cp "$CLAUDE_CONFIG/statusline.sh" "$CLAUDE_CONFIG/statusline.sh.bluera-base-backup-$BACKUP_TS"
   fi
   ```

3. **Write the script** to the config directory:

   ```bash
   cat > "$CLAUDE_CONFIG/statusline.sh" << 'STATUSLINE_EOF'
   <generated script content here>
   STATUSLINE_EOF
   ```

4. **Make executable**:

   ```bash
   chmod +x "$CLAUDE_CONFIG/statusline.sh"
   ```

5. **Verify** the file exists and is executable:

   ```bash
   ls -la "$CLAUDE_CONFIG/statusline.sh"
   ```

**The statusline will not work until these steps are completed.**

---

## Preserving User Customizations

When modifying an existing `$CLAUDE_CONFIG/statusline.sh`, preserve user-added content:

### Detection Patterns

Look for these indicators of custom code:

1. **Boundary comments:**
   - `# --- custom ---` / `# --- end custom ---`
   - `# --- user ---` / `# --- end user ---`
   - `# --- <name> status ---` / `# --- end <name> status ---`

2. **Custom function definitions:**
   - Functions not matching standard module names
   - Example: `get_cca_status()`, `get_k8s_status()`

3. **External service integration:**
   - `curl` to localhost/127.0.0.1 addresses
   - Reads from non-standard config files
   - Environment-specific ports or paths

4. **Custom variables in output:**
   - Variables referenced in final `echo`/`printf` that aren't from standard modules

### Preservation Algorithm

```text
1. Read existing script
2. Extract sections between boundary comments
3. Identify custom variables used in output format
4. Generate new script with standard modules
5. Append preserved custom sections before output
6. Update output format to include custom variables
```

### Example: CCA Integration (Preserve)

```bash
# --- claude-code-anywhere status ---
CCA_STATUS=""
_CCA_PORT=$(cat ~/.config/claude-code-anywhere/port 2>/dev/null)
if [ -n "$_CCA_PORT" ]; then
    _CCA_RESP=$(curl -s --max-time 1 "http://127.0.0.1:${_CCA_PORT}/health" 2>/dev/null)
    if [ -n "$_CCA_RESP" ]; then
        CCA_STATUS="${SEP}${ICON_CCA}CCA${STATUS_OK}"
    fi
fi
# --- end claude-code-anywhere status ---
```

This should be preserved because:

- Has clear boundary comments
- Fetches from local service (127.0.0.1)
- Defines `CCA_STATUS` variable used in output

---

## Configuration Examples

### Minimal Developer

```bash
THEME="minimal"
MODULES="directory,context,git"
DISPLAY_MODE="compact"
```

Output: `→myproject 45% ⎇main*`

### Full System Monitor

```bash
THEME="default"
MODULES="directory,model,context,git,cost,rate-limits,cpu,memory,docker"
DISPLAY_MODE="normal"
```

Output: `📁myproject | 🤖Opus4.5 | 📊45%🟢 | 🌿main* | 💰$1.23 | ⚡5h:12%🟢 7d:8%🟢 | 💻15%🟢 | 🧠62%🟡 | 🐳3`

### Server/Remote

```bash
THEME="monochrome"
MODULES="directory,context,git,cpu,memory"
DISPLAY_MODE="compact"
```

Output: `DIR:myproject | CTX:45%[OK] | GIT:main | CPU:15%[OK] | MEM:62%[~~]`

---

## Preview All Presets

When `statusline preset` is run without a name argument, display this preview table:

| Preset | Example Output |
|--------|----------------|
| **minimal** | `Opus 4.5 45%` |
| **informative** | `🤖 Opus 4.5 │ 📊 45%🟢 │ 💰 $1.23` |
| **developer** | `📁project │ 🤖Opus4.5 │ 📊45%🟢 │ 🌿main* │ 📦Node │ 💰$1.23` |
| **system** | `📁project │ 🤖Opus4.5 │ 📊45%🟢 │ 🌿main │ 💻15%🟢 │ 🧠62%🟡 │ 🐳3` |
| **bluera** | `Opus4.5 project 🐍 main* │ $1.23 │ ██████░░░░ 60% │ +42/-8 │ 5h:12% 7d:8%` |

Then use AskUserQuestion to let the user select which preset to apply.

---

## Preset Definitions

### Preset: minimal

```bash
THEME="minimal"
MODULES="model,context"
DISPLAY_MODE="compact"
```

Static string alternative: `%model% | %context%`

### Preset: informative

```bash
THEME="default"
MODULES="model,context,cost"
DISPLAY_MODE="normal"
```

Static string alternative: `🤖 %model% | 📊 %context% | 💰 %cost%`

### Preset: developer

```bash
THEME="default"
MODULES="directory,model,context,git,project,cost"
DISPLAY_MODE="normal"
```

### Preset: system

```bash
THEME="default"
MODULES="directory,model,context,git,cpu,memory,docker"
DISPLAY_MODE="normal"
```

### Preset: bluera

Advanced statusline with rate limits, context bar, and ANSI colors.

**Features:**

- ANSI terminal colors (not emojis for status)
- 10-character context progress bar (█░)
- Rate limits (5h/7d) from Anthropic API with caching
- Lines changed (+/-) in session
- Project type detection (🦀🐹🐍💧💎📦🦕▲⚡🍞)

**Output format:**

`Model dir project branch │ $cost │ [ctx bar] pct% │ +added/-removed │ 5h:X% 7d:Y%`

**Example:**

`Opus 4.5 myproject 🐍 main* │ $1.23 │ ██████░░░░ 60% │ +42/-8 │ 5h:12% 7d:8%`

---

## Ready-to-Use Preset Scripts

**IMPORTANT:** When applying a preset, copy the entire script below to `~/.claude/statusline.sh` and make it executable with `chmod +x ~/.claude/statusline.sh`.

### Script: minimal

```bash
#!/bin/bash
input=$(cat)
MODEL=$(echo "$input" | jq -r '.model.display_name // "?"')
CTX=$(echo "$input" | jq -r '.context_window.used_percentage // 0' | cut -d. -f1)
echo "$MODEL $CTX%"
```

### Script: informative

```bash
#!/bin/bash
input=$(cat)

MODEL=$(echo "$input" | jq -r '.model.display_name // "?"')
CTX=$(echo "$input" | jq -r '.context_window.used_percentage // 0' | cut -d. -f1)
COST=$(echo "$input" | jq -r '.cost.total_cost_usd // 0')

# Status indicator
if [ "$CTX" -lt 50 ]; then STATUS="🟢"
elif [ "$CTX" -lt 80 ]; then STATUS="🟡"
else STATUS="🔴"; fi

# Format cost
if (( $(echo "$COST < 1" | bc -l 2>/dev/null || echo 1) )); then
    COST_FMT=$(printf "%.0f¢" "$(echo "$COST * 100" | bc -l 2>/dev/null || echo 0)")
else
    COST_FMT=$(printf "$%.2f" "$COST")
fi

echo "🤖 $MODEL │ 📊 ${CTX}%${STATUS} │ 💰 $COST_FMT"
```

### Script: developer

```bash
#!/bin/bash
input=$(cat)

# Extract values
MODEL=$(echo "$input" | jq -r '.model.display_name // "?"')
CURRENT_DIR=$(echo "$input" | jq -r '.workspace.current_dir // "."')
DIR_NAME=$(basename "$CURRENT_DIR")
CTX=$(echo "$input" | jq -r '.context_window.used_percentage // 0' | cut -d. -f1)
COST=$(echo "$input" | jq -r '.cost.total_cost_usd // 0')

# Status indicator
if [ "$CTX" -lt 50 ]; then STATUS="🟢"
elif [ "$CTX" -lt 80 ]; then STATUS="🟡"
else STATUS="🔴"; fi

# Format cost
if (( $(echo "$COST < 1" | bc -l 2>/dev/null || echo 1) )); then
    COST_FMT=$(printf "%.0f¢" "$(echo "$COST * 100" | bc -l 2>/dev/null || echo 0)")
else
    COST_FMT=$(printf "$%.2f" "$COST")
fi

# Git branch
GIT_INFO=""
if git -C "$CURRENT_DIR" rev-parse --git-dir > /dev/null 2>&1; then
    BRANCH=$(git -C "$CURRENT_DIR" --no-optional-locks branch --show-current 2>/dev/null)
    if [ -n "$(git -C "$CURRENT_DIR" --no-optional-locks status --porcelain 2>/dev/null)" ]; then
        GIT_INFO="🌿${BRANCH}*"
    else
        GIT_INFO="🌿${BRANCH}"
    fi
fi

# Project type
PROJECT=""
if [ -f "$CURRENT_DIR/Cargo.toml" ]; then PROJECT="🦀Rust"
elif [ -f "$CURRENT_DIR/go.mod" ]; then PROJECT="🐹Go"
elif [ -f "$CURRENT_DIR/pyproject.toml" ] || [ -f "$CURRENT_DIR/requirements.txt" ]; then PROJECT="🐍Python"
elif [ -f "$CURRENT_DIR/package.json" ]; then
    if [ -f "$CURRENT_DIR/next.config.js" ] || [ -f "$CURRENT_DIR/next.config.ts" ]; then PROJECT="▲Next.js"
    elif [ -f "$CURRENT_DIR/bun.lockb" ]; then PROJECT="🍞Bun"
    else PROJECT="📦Node"
    fi
fi

# Build output
OUTPUT="📁$DIR_NAME │ 🤖$MODEL │ 📊${CTX}%${STATUS}"
[ -n "$GIT_INFO" ] && OUTPUT="$OUTPUT │ $GIT_INFO"
[ -n "$PROJECT" ] && OUTPUT="$OUTPUT │ $PROJECT"
OUTPUT="$OUTPUT │ 💰$COST_FMT"

echo "$OUTPUT"
```

### Script: system

```bash
#!/bin/bash
input=$(cat)

# Extract values
MODEL=$(echo "$input" | jq -r '.model.display_name // "?"')
CURRENT_DIR=$(echo "$input" | jq -r '.workspace.current_dir // "."')
DIR_NAME=$(basename "$CURRENT_DIR")
CTX=$(echo "$input" | jq -r '.context_window.used_percentage // 0' | cut -d. -f1)

# Status indicator
if [ "$CTX" -lt 50 ]; then CTX_STATUS="🟢"
elif [ "$CTX" -lt 80 ]; then CTX_STATUS="🟡"
else CTX_STATUS="🔴"; fi

# Git branch
GIT_INFO=""
if git -C "$CURRENT_DIR" rev-parse --git-dir > /dev/null 2>&1; then
    BRANCH=$(git -C "$CURRENT_DIR" --no-optional-locks branch --show-current 2>/dev/null)
    GIT_INFO="🌿$BRANCH"
fi

# CPU usage (cross-platform)
CPU_PCT=0
if [[ "$OSTYPE" == "darwin"* ]]; then
    CPU_PCT=$(top -l 1 -n 0 2>/dev/null | grep "CPU usage" | awk '{print int($3)}')
else
    CPU_PCT=$(top -bn1 2>/dev/null | grep "Cpu(s)" | awk '{print int($2)}')
fi
if [ "$CPU_PCT" -lt 50 ]; then CPU_STATUS="🟢"
elif [ "$CPU_PCT" -lt 80 ]; then CPU_STATUS="🟡"
else CPU_STATUS="🔴"; fi

# Memory usage (cross-platform)
MEM_PCT=0
if [[ "$OSTYPE" == "darwin"* ]]; then
    MEM_PCT=$(vm_stat 2>/dev/null | awk '/Pages active/ {active=$3} /Pages inactive/ {inactive=$3} /Pages speculative/ {spec=$3} /Pages wired/ {wired=$4} /Pages free/ {free=$3} END {used=active+inactive+spec+wired; total=used+free; if(total>0) printf "%d", (used/total)*100}')
else
    MEM_PCT=$(free 2>/dev/null | awk '/Mem:/ {printf "%d", $3/$2*100}')
fi
if [ "$MEM_PCT" -lt 50 ]; then MEM_STATUS="🟢"
elif [ "$MEM_PCT" -lt 80 ]; then MEM_STATUS="🟡"
else MEM_STATUS="🔴"; fi

# Docker containers
DOCKER_COUNT=$(docker ps -q 2>/dev/null | wc -l | tr -d ' ')

# Build output
OUTPUT="📁$DIR_NAME │ 🤖$MODEL │ 📊${CTX}%${CTX_STATUS}"
[ -n "$GIT_INFO" ] && OUTPUT="$OUTPUT │ $GIT_INFO"
OUTPUT="$OUTPUT │ 💻${CPU_PCT}%${CPU_STATUS} │ 🧠${MEM_PCT}%${MEM_STATUS}"
[ "$DOCKER_COUNT" -gt 0 ] && OUTPUT="$OUTPUT │ 🐳$DOCKER_COUNT"

echo "$OUTPUT"
```

### Script: bluera

```bash
#!/bin/bash
# Bluera preset - advanced statusline with rate limits, context bar, and ANSI colors

input=$(cat)

# --- Project Type Detection ---
get_project_type() {
    local dir="$1"
    if [ -f "$dir/Cargo.toml" ]; then echo "🦀"
    elif [ -f "$dir/go.mod" ]; then echo "🐹"
    elif [ -f "$dir/pyproject.toml" ] || [ -f "$dir/requirements.txt" ]; then echo "🐍"
    elif [ -f "$dir/mix.exs" ]; then echo "💧"
    elif [ -f "$dir/Gemfile" ]; then echo "💎"
    elif [ -f "$dir/package.json" ]; then
        if [ -f "$dir/next.config.js" ] || [ -f "$dir/next.config.ts" ] || [ -f "$dir/next.config.mjs" ]; then echo "▲"
        elif [ -f "$dir/nuxt.config.ts" ] || [ -f "$dir/nuxt.config.js" ]; then echo "⚡"
        elif [ -f "$dir/vite.config.ts" ] || [ -f "$dir/vite.config.js" ]; then echo "⚡"
        elif [ -f "$dir/bun.lockb" ]; then echo "🍞"
        else echo "📦"
        fi
    elif [ -f "$dir/deno.json" ]; then echo "🦕"
    else echo ""
    fi
}

# --- Rate Limits (fetches from Anthropic API via keychain - macOS only) ---
get_rate_limits() {
    local cache_file="/tmp/.claude_usage_cache"
    local cache_max_age=60
    local usage_data=""

    # Check cache
    if [ -f "$cache_file" ]; then
        local cache_age=$(($(date +%s) - $(stat -f %m "$cache_file" 2>/dev/null || stat -c %Y "$cache_file" 2>/dev/null || echo 0)))
        if [ "$cache_age" -lt "$cache_max_age" ]; then
            usage_data=$(cat "$cache_file")
        fi
    fi

    # Fetch if no cache (macOS keychain)
    if [ -z "$usage_data" ]; then
        local token
        token=$(security find-generic-password -s 'Claude Code-credentials' -w 2>/dev/null | jq -r '.claudeAiOauth.accessToken // empty' 2>/dev/null)
        if [ -n "$token" ]; then
            usage_data=$(curl -s --max-time 2 "https://api.anthropic.com/api/oauth/usage" \
                -H "Authorization: Bearer $token" \
                -H "anthropic-beta: oauth-2025-04-20" \
                -H "Accept: application/json" 2>/dev/null)
            [ -n "$usage_data" ] && echo "$usage_data" > "$cache_file" 2>/dev/null
        fi
    fi

    if [ -z "$usage_data" ]; then echo ""; return; fi

    local five_hour=$(echo "$usage_data" | jq -r '(.five_hour // .five_hour_opus // .five_hour_sonnet // {}).utilization // 0' 2>/dev/null)
    local seven_day=$(echo "$usage_data" | jq -r '(.seven_day // .seven_day_opus // .seven_day_sonnet // {}).utilization // 0' 2>/dev/null)

    local five_int=$(printf "%.0f" "$five_hour" 2>/dev/null || echo "0")
    local seven_int=$(printf "%.0f" "$seven_day" 2>/dev/null || echo "0")

    # Color based on usage
    local five_color="\033[32m"; [ "$five_int" -ge 50 ] && five_color="\033[33m"; [ "$five_int" -ge 75 ] && five_color="\033[38;5;208m"; [ "$five_int" -ge 95 ] && five_color="\033[31m"
    local seven_color="\033[32m"; [ "$seven_int" -ge 50 ] && seven_color="\033[33m"; [ "$seven_int" -ge 75 ] && seven_color="\033[38;5;208m"; [ "$seven_int" -ge 95 ] && seven_color="\033[31m"

    printf "${five_color}5h:%d%%\033[0m ${seven_color}7d:%d%%\033[0m" "$five_int" "$seven_int"
}

# Extract values
MODEL=$(echo "$input" | jq -r '.model.display_name // "?"')
CURRENT_DIR=$(echo "$input" | jq -r '.workspace.current_dir')
DIR_NAME=$(basename "$CURRENT_DIR")
COST=$(echo "$input" | jq -r '.cost.total_cost_usd // 0')
LINES_ADDED=$(echo "$input" | jq -r '.cost.total_lines_added // 0')
LINES_REMOVED=$(echo "$input" | jq -r '.cost.total_lines_removed // 0')
CONTEXT_SIZE=$(echo "$input" | jq -r '.context_window.context_window_size // 200000')
USAGE=$(echo "$input" | jq '.context_window.current_usage')

# Calculate context percentage
if [ "$USAGE" != "null" ]; then
    INPUT_TOKENS=$(echo "$USAGE" | jq '.input_tokens // 0')
    CACHE_CREATE=$(echo "$USAGE" | jq '.cache_creation_input_tokens // 0')
    CACHE_READ=$(echo "$USAGE" | jq '.cache_read_input_tokens // 0')
    CURRENT_TOKENS=$((INPUT_TOKENS + CACHE_CREATE + CACHE_READ))
    CONTEXT_PCT=$((CURRENT_TOKENS * 100 / CONTEXT_SIZE))
else
    CONTEXT_PCT=0
fi

# Git info with colors
GIT_INFO=""
if git -C "$CURRENT_DIR" rev-parse --git-dir > /dev/null 2>&1; then
    BRANCH=$(git -C "$CURRENT_DIR" --no-optional-locks branch --show-current 2>/dev/null)
    if [ -n "$(git -C "$CURRENT_DIR" --no-optional-locks status --porcelain 2>/dev/null)" ]; then
        GIT_INFO=$(printf " \033[33m%s\033[0m\033[31m*\033[0m" "$BRANCH")
    else
        GIT_INFO=$(printf " \033[36m%s\033[0m" "$BRANCH")
    fi
fi

# Format cost
if (( $(echo "$COST < 1" | bc -l) )); then
    COST_FMT=$(printf "%.0f¢" "$(echo "$COST * 100" | bc -l)")
else
    COST_FMT=$(printf "$%.2f" "$COST")
fi

# Format lines changed
if [ "$LINES_ADDED" -gt 0 ] || [ "$LINES_REMOVED" -gt 0 ]; then
    LINES_FMT=$(printf "\033[32m+%d\033[0m/\033[31m-%d\033[0m" "$LINES_ADDED" "$LINES_REMOVED")
else
    LINES_FMT="-"
fi

# Build context bar (10 chars wide)
BAR_WIDTH=10
FILLED=$((CONTEXT_PCT * BAR_WIDTH / 100))
[ "$FILLED" -gt "$BAR_WIDTH" ] && FILLED=$BAR_WIDTH
EMPTY=$((BAR_WIDTH - FILLED))
BAR=""; for ((i=0; i<FILLED; i++)); do BAR+="█"; done; for ((i=0; i<EMPTY; i++)); do BAR+="░"; done

# Project type and rate limits
PROJECT_TYPE=$(get_project_type "$CURRENT_DIR")
[ -n "$PROJECT_TYPE" ] && PROJECT_TYPE=" $PROJECT_TYPE"

RATE_LIMITS=$(get_rate_limits)
[ -n "$RATE_LIMITS" ] && RATE_LIMITS=" │ $RATE_LIMITS"

# Output with colored context bar
if [ "$CONTEXT_PCT" -lt 50 ]; then
    printf "\033[35m%s\033[0m \033[1m%s\033[0m%s%s │ \033[33m%s\033[0m │ \033[32m%s\033[0m %d%% │ %s%s" \
        "$MODEL" "$DIR_NAME" "$PROJECT_TYPE" "$GIT_INFO" "$COST_FMT" "$BAR" "$CONTEXT_PCT" "$LINES_FMT" "$RATE_LIMITS"
elif [ "$CONTEXT_PCT" -lt 80 ]; then
    printf "\033[35m%s\033[0m \033[1m%s\033[0m%s%s │ \033[33m%s\033[0m │ \033[33m%s\033[0m %d%% │ %s%s" \
        "$MODEL" "$DIR_NAME" "$PROJECT_TYPE" "$GIT_INFO" "$COST_FMT" "$BAR" "$CONTEXT_PCT" "$LINES_FMT" "$RATE_LIMITS"
else
    printf "\033[35m%s\033[0m \033[1m%s\033[0m%s%s │ \033[33m%s\033[0m │ \033[31m%s\033[0m %d%% │ %s%s" \
        "$MODEL" "$DIR_NAME" "$PROJECT_TYPE" "$GIT_INFO" "$COST_FMT" "$BAR" "$CONTEXT_PCT" "$LINES_FMT" "$RATE_LIMITS"
fi
```
