---
name: ralph-amp
description: Interactive planning skill for Amp. Generates specs, implementation plans, and loop infrastructure through clarifying questions.
allowed-tools:
  - "*"
---

# Ralph Planning Skill (Amp)

Generate specs, implementation plans, and loop infrastructure for iterative AI-driven development.

## Entry

**Usage:** `/skill ralph-amp [optional/path/to/plan.md]`

- If path provided: Read that `.md` file as the source specification
- If no path: Use the current conversation context

---

## Step 1: Interview the User

You MUST ask clarifying questions before generating any files. Present questions with lettered options for quick responses.

**Interview approach:**
1. Present 3-5 questions covering scope, constraints, and validation
2. Use A/B/C/D multiple choice format for quick answers
3. Allow the user to respond with shorthand like "1A, 2C, 3B"
4. Ask follow-up questions if answers are unclear

**Example interview:**

> I'll help you plan this feature. First, let me ask a few questions:
>
> **1. Scope** - How broad is this change?
> - A) Single file/module
> - B) Multiple related files  
> - C) Cross-cutting (many parts of codebase)
> - D) Greenfield (new feature from scratch)
>
> **2. Risk tolerance** - How aggressive should changes be?
> - A) Conservative - minimal changes
> - B) Balanced - reasonable refactoring OK
> - C) Aggressive - significant refactoring acceptable
>
> **3. Validation** - How should we verify the implementation?
> - A) Existing test suite
> - B) Add new tests
> - C) Manual testing sufficient
>
> Reply with your choices (e.g., "1B, 2A, 3B") or answer in your own words.

**WAIT for user response before proceeding.**

---

## Step 2: Oracle Review (Optional)

After receiving answers, offer to analyze the codebase:

> Would you like me to analyze the codebase architecture before generating the plan?
> - Reply **oracle** for architectural analysis
> - Reply **skip** to proceed directly

### If user chooses `oracle`:
1. Use the Oracle tool to analyze relevant code areas
2. Identify existing patterns, potential conflicts, dependencies
3. Present findings and any additional clarifying questions
4. **WAIT for user response before proceeding**

### If user chooses `skip`:
Proceed directly to Step 3.

---

## Step 3: Generate Files

**Always overwrite existing files** — never add suffixes like `-v2`, `-new`, or `_backup`. These files are ephemeral and meant to be regenerated. Use the exact filenames specified below.

### 1. `specs/<feature-slug>.md`

Requirements specification containing:
- Feature overview
- User stories
- Acceptance criteria
- Edge cases and error handling
- Out of scope items

### 2. `IMPLEMENTATION_PLAN.md`

Format:
```markdown
# Implementation Plan: <Feature Name>

> **Scope**: <scope choice> | **Risk**: <risk choice> | **Constraints**: <constraint choice>

## Summary

<2-3 sentence overview of the implementation approach>

## Tasks

- [ ] Task 1: Description with enough context for implementation
- [ ] Task 2: Description with enough context for implementation
- [ ] Task 3: Description with enough context for implementation
...
```

Tasks should be:
- Ordered by priority/dependency
- Small enough for single iteration
- Include file paths when known
- Self-contained with sufficient context

### 3. `PROMPT_plan.md`

Generate with this content (replace `[DIRECTORIES]` with relevant source directories):

```markdown
# Planning Mode

You are in PLANNING mode. Analyze specifications against existing code and generate a prioritized implementation plan.

## Phase 0: Orient

### 0a. Study specifications
Read all files in `specs/` directory using finder and parallel reads.

### 0b. Study existing implementation
Use finder to analyze relevant source directories:
[DIRECTORIES]

### 0c. Study the current plan
Read `IMPLEMENTATION_PLAN.md` if it exists.

## Phase 1: Gap Analysis

Compare specs against implementation:
- What's already implemented?
- What's missing?
- What's partially done?

**CRITICAL**: Don't assume something isn't implemented. Use finder to search the codebase first.

## Phase 2: Generate Plan

Update `IMPLEMENTATION_PLAN.md` with:
- Tasks sorted by priority (P0 → P1 → P2)
- Clear descriptions with file locations
- Dependencies noted where relevant
- Discoveries from gap analysis

**CRITICAL: ALL tasks MUST use checkbox format:**
- `- [ ] **Task Name**` for pending tasks
- `- [x] **Task Name**` for completed tasks

Do NOT use other formats like `#### P1.1: Task Name` or `**Task Name**` without checkboxes. The build loop relies on `grep -c "^\- \[ \]"` to count remaining tasks.

Capture the WHY, not just the WHAT.

## Phase 3: Exit

After updating the plan, output **RALPH_COMPLETE** and exit.

## Guardrails

999. NEVER implement code in planning mode
1000. Use Task tool for parallel analysis of different areas
1001. Each task must be completable in ONE loop iteration
1002. Use Oracle to review priorities before finalizing
1003. **ALWAYS use checkbox format `- [ ]` or `- [x]` for tasks in IMPLEMENTATION_PLAN.md** - The build loop relies on `grep -c "^\- \[ \]"` to count remaining tasks. Never use `####` headers or bold text without checkboxes.
```

### 4. `PROMPT_build.md`

Generate with this content (replace `[VALIDATION_COMMAND]` with the appropriate command from AGENTS.md or project config):

```markdown
# Build Mode

Implement ONE task from the plan, validate, commit, exit.

## Phase 0: Orient

Study:
- @AGENTS.md (how to build/test)
- @specs/* (requirements)
- @IMPLEMENTATION_PLAN.md (current state)

### Check for completion

```bash
grep -c "^\- \[ \]" IMPLEMENTATION_PLAN.md || echo 0
```

- If 0: Run validation → commit → output **RALPH_COMPLETE** → exit
- If > 0: Continue to Phase 1

## Phase 1: Implement

1. **Study the plan** — Choose the most important task from @IMPLEMENTATION_PLAN.md
2. **Search first** — Don't assume not implemented. Use finder to verify behavior doesn't already exist
3. **Implement** — ONE task only. Implement completely — no placeholders or stubs
4. **Validate** — Run `[VALIDATION_COMMAND]`, must pass before continuing

If stuck, use Oracle to debug. Add extra logging if needed.

## Phase 2: Update & Learn

**Update IMPLEMENTATION_PLAN.md:**
- Mark task `- [x] Completed`
- Add discovered bugs or issues (even if unrelated to current task)
- Note any new tasks discovered
- Periodically clean out completed items when file gets large

**Update AGENTS.md** (if you learned something new):
- Add correct commands discovered through trial and error
- Keep it brief and operational only — no status updates or progress notes

## Phase 3: Commit & Exit

```bash
git add -A && git commit -m "feat([scope]): [description]

Thread: $AMP_THREAD_URL"
```

Check remaining:
```bash
grep -c "^\- \[ \]" IMPLEMENTATION_PLAN.md || echo 0
```

- If > 0: Say "X tasks remaining" and EXIT
- If = 0: Output **RALPH_COMPLETE**

## Guardrails

99999. When authoring documentation, capture the why — tests and implementation importance.
999999. Single sources of truth, no migrations/adapters. If tests unrelated to your work fail, resolve them as part of the increment.
9999999. Implement functionality completely. Placeholders and stubs waste time redoing the same work.
99999999. Keep @IMPLEMENTATION_PLAN.md current with learnings — future iterations depend on this to avoid duplicating efforts.
999999999. Keep @AGENTS.md operational only — status updates and progress notes pollute every future loop's context.
9999999999. For any bugs you notice, resolve them or document them in @IMPLEMENTATION_PLAN.md even if unrelated to current work.
99999999999. ONE task per iteration. Search before implementing. Validation MUST pass. Never output RALPH_COMPLETE if tasks remain.
```

### 5. `loop.sh`

Generate with this content (replace `[FEATURE_NAME]` with a short kebab-case feature name like `auth-system` or `api-refactor`):

```bash
#!/bin/bash

# Ralph Wiggum Build Loop (Amp)
# Usage:
#   ./loop.sh           # Auto mode: plan first, then build (default)
#   ./loop.sh plan      # Planning mode only
#   ./loop.sh build     # Build mode only
#   ./loop.sh 10        # Auto mode, max 10 build iterations
#   ./loop.sh build 5   # Build mode, max 5 iterations

set -e

FEATURE_NAME="[FEATURE_NAME]"
MODE="plan"
AUTO_MODE=true
MAX_ITERATIONS=0
ITERATION=0
CONSECUTIVE_FAILURES=0
PARENT_THREAD_FILE=$(mktemp)

# Colors
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

for arg in "$@"; do
  if [[ "$arg" == "plan" ]]; then
    MODE="plan"
    AUTO_MODE=false
  elif [[ "$arg" == "build" ]]; then
    MODE="build"
    AUTO_MODE=false
  elif [[ "$arg" =~ ^[0-9]+$ ]]; then
    MAX_ITERATIONS=$arg
  fi
done

PROMPT_FILE="PROMPT_${MODE}.md"

if [[ ! -f "$PROMPT_FILE" ]]; then
  echo -e "${RED}Error: $PROMPT_FILE not found${NC}"
  echo "Run the ralph-amp skill first to generate the required files."
  exit 1
fi

cleanup() {
  rm -f "$PARENT_THREAD_FILE"
}
trap cleanup EXIT

switch_to_build_mode() {
  echo ""
  echo -e "${CYAN}=== Switching to Build Mode ===${NC}"
  echo ""
  MODE="build"
  PROMPT_FILE="PROMPT_${MODE}.md"
  ITERATION=0
}

seconds_until_next_hour() {
  local now=$(date +%s)
  local current_minute=$(date +%M)
  local current_second=$(date +%S)
  local seconds_past_hour=$((10#$current_minute * 60 + 10#$current_second))
  local seconds_until=$((3600 - seconds_past_hour))
  echo $seconds_until
}

seconds_until_daily_reset() {
  local reset_hour=5
  local now=$(date +%s)
  local today_reset=$(date -v${reset_hour}H -v0M -v0S +%s 2>/dev/null || date -d "today ${reset_hour}:00:00" +%s)

  if [[ $now -ge $today_reset ]]; then
    local tomorrow_reset=$((today_reset + 86400))
    echo $((tomorrow_reset - now))
  else
    echo $((today_reset - now))
  fi
}

countdown() {
  local seconds=$1
  local message=$2

  while [[ $seconds -gt 0 ]]; do
    local hours=$((seconds / 3600))
    local minutes=$(((seconds % 3600) / 60))
    local secs=$((seconds % 60))
    printf "\r${CYAN}%s${NC} Time remaining: %02d:%02d:%02d " "$message" $hours $minutes $secs
    sleep 1
    ((seconds--))
  done
  printf "\r%-80s\r" " "
}

is_recoverable_error() {
  local output="$1"
  local exit_code="$2"

  # Check JSON error field from stream-json output
  if [[ "$output" =~ \"error\":\"rate_limit\" ]]; then
    return 0
  fi
  if [[ "$output" =~ "rate limit" ]] || [[ "$output" =~ "Rate limit" ]]; then
    return 0
  fi
  if [[ "$output" =~ Error:\ 429 ]] || [[ "$output" =~ Error:\ 529 ]]; then
    return 0
  fi
  return 1
}

get_sleep_duration() {
  local output="$1"

  local json_reset=$(echo "$output" | grep -oE '"resetsAt"\s*:\s*"[^"]+"' | head -1 | sed 's/.*"\([^"]*\)"$/\1/')
  if [[ -n "$json_reset" ]]; then
    local reset_epoch=$(date -jf "%Y-%m-%dT%H:%M:%S%z" "$json_reset" +%s 2>/dev/null || \
                        date -d "$json_reset" +%s 2>/dev/null)
    if [[ -n "$reset_epoch" ]]; then
      local now=$(date +%s)
      local diff=$((reset_epoch - now))
      if [[ $diff -gt 0 ]]; then
        echo $((diff + 60))
        return
      fi
    fi
  fi

  if [[ "$output" =~ retry.after[[:space:]]*:?[[:space:]]*([0-9]+) ]]; then
    echo "${BASH_REMATCH[1]}"
    return
  fi

  if [[ "$output" =~ "try again in "([0-9]+)" minute" ]]; then
    echo $(( ${BASH_REMATCH[1]} * 60 + 60 ))
    return
  fi

  if [[ "$output" =~ "try again in "([0-9]+)" hour" ]]; then
    echo $(( ${BASH_REMATCH[1]} * 3600 + 60 ))
    return
  fi

  if [[ "$output" =~ (daily|day|24.?hour) ]]; then
    seconds_until_daily_reset
    return
  fi

  if [[ "$output" =~ resets[[:space:]]+([0-9]+)(am|pm) ]]; then
    local reset_hour="${BASH_REMATCH[1]}"
    local ampm="${BASH_REMATCH[2]}"
    local tz="UTC"
    if [[ "$output" =~ \(([A-Za-z_/]+)\) ]]; then
      tz="${BASH_REMATCH[1]}"
    fi
    
    if [[ "$ampm" == "pm" && "$reset_hour" -ne 12 ]]; then
      reset_hour=$((reset_hour + 12))
    elif [[ "$ampm" == "am" && "$reset_hour" -eq 12 ]]; then
      reset_hour=0
    fi
    
    local now=$(date +%s)
    local target=$(TZ="$tz" date -v${reset_hour}H -v0M -v0S +%s 2>/dev/null || TZ="$tz" date -d "today ${reset_hour}:00:00" +%s)
    
    if [[ $now -ge $target ]]; then
      target=$((target + 86400))
    fi
    
    echo $((target - now + 60))
    return
  fi

  echo 300
}

handle_recoverable_error() {
  local output="$1"
  local sleep_duration=$(get_sleep_duration "$output")

  echo ""
  echo -e "${YELLOW}=== Recoverable Error Detected ===${NC}"
  echo -e "${YELLOW}Waiting before retry...${NC}"
  echo ""

  local tz="UTC"
  if [[ "$output" =~ \(([A-Za-z_/]+)\) ]]; then
    tz="${BASH_REMATCH[1]}"
  fi
  local resume_time=$(TZ="$tz" date -v+${sleep_duration}S "+%Y-%m-%d %H:%M:%S" 2>/dev/null || TZ="$tz" date -d "+${sleep_duration} seconds" "+%Y-%m-%d %H:%M:%S")
  echo -e "Expected resume: ${CYAN}${resume_time}${NC}"
  echo ""

  countdown $sleep_duration "Waiting..."

  echo ""
  echo -e "${GREEN}Resuming...${NC}"
  echo ""

  CONSECUTIVE_FAILURES=0
}

if [[ "$AUTO_MODE" == true ]]; then
  echo -e "${GREEN}Ralph loop: AUTO mode (plan → build)${NC}"
  [[ $MAX_ITERATIONS -gt 0 ]] && echo "Max build iterations: $MAX_ITERATIONS"
else
  echo -e "${GREEN}Ralph loop: $(echo "$MODE" | tr '[:lower:]' '[:upper:]') mode${NC}"
  [[ $MAX_ITERATIONS -gt 0 ]] && echo "Max iterations: $MAX_ITERATIONS"
fi
echo "Press Ctrl+C to stop"
echo "---"

while true; do
  ITERATION=$((ITERATION + 1))
  echo ""
  MODE_DISPLAY=$(echo "$MODE" | tr '[:lower:]' '[:upper:]')
  if [[ "$AUTO_MODE" == true ]]; then
    echo -e "${GREEN}=== ${MODE_DISPLAY} Iteration $ITERATION ===${NC}"
  else
    echo -e "${GREEN}=== Iteration $ITERATION ===${NC}"
  fi
  echo ""

  TEMP_OUTPUT=$(mktemp)
  PARENT_THREAD=$(cat "$PARENT_THREAD_FILE" 2>/dev/null || true)
  set +e

  if [[ -n "$PARENT_THREAD" ]]; then
    echo -e "${CYAN}Creating handoff from parent ${PARENT_THREAD}...${NC}"
    
    cat "$PROMPT_FILE" | amp threads handoff "$PARENT_THREAD" \
      --goal "$(cat "$PROMPT_FILE")" \
      -x \
      --dangerously-allow-all \
      --stream-json > "$TEMP_OUTPUT" 2>&1
  else
    amp -x --dangerously-allow-all --stream-json < "$PROMPT_FILE" > "$TEMP_OUTPUT" 2>&1
  fi

  THREAD_ID=$(jq -r 'select(.type == "system") | .session_id' "$TEMP_OUTPUT" 2>/dev/null | head -1)

  cat "$TEMP_OUTPUT" | jq -r '
      def tool_info:
        if .name == "edit_file" or .name == "create_file" or .name == "Read" then
          (.input.path | split("/") | last | .[0:60])
        elif .name == "todo_write" then
          ((.input.todos // []) | map(.content) | join(", ") | if contains("\n") then .[0:60] else . end)
        elif .name == "Bash" then
          (.input.cmd | if contains("\n") then split("\n") | first | .[0:50] else .[0:80] end)
        elif .name == "Grep" then
          (.input.pattern | .[0:40])
        elif .name == "glob" then
          (.input.filePattern | .[0:40])
        elif .name == "finder" then
          (.input.query | if contains("\n") then .[0:40] else . end)
        elif .name == "oracle" then
          (.input.task | if contains("\n") then .[0:40] else .[0:80] end)
        elif .name == "Task" then
          (.input.description // .input.prompt | if contains("\n") then .[0:40] else .[0:80] end)
        else null end;
      if .type == "assistant" then
        .message.content[] |
        if .type == "text" then
          if (.text | split("\n") | length) <= 3 then .text else empty end
        elif .type == "tool_use" then
          "    [" + .name + "]" + (tool_info | if . then " " + . else "" end)
        else empty end
      elif .type == "result" then
        "--- " + ((.duration_ms / 1000 * 10 | floor / 10) | tostring) + "s, " + (.num_turns | tostring) + " turns ---"
      else empty end
    ' 2>/dev/null

  EXIT_CODE=$?
  OUTPUT=$(cat "$TEMP_OUTPUT")
  RESULT_MSG=$(jq -r 'select(.type == "result") | .result // empty' "$TEMP_OUTPUT" 2>/dev/null | tail -1)
  rm -f "$TEMP_OUTPUT"
  set -e

  if [[ -n "$THREAD_ID" ]]; then
    if [[ -z "$PARENT_THREAD" ]]; then
      echo "$THREAD_ID" > "$PARENT_THREAD_FILE"
      amp threads rename "$THREAD_ID" "ralph: ${FEATURE_NAME} ${MODE} (parent)" 2>/dev/null || true
      echo -e "${CYAN}Parent thread: $THREAD_ID${NC}"
    else
      amp threads rename "$THREAD_ID" "ralph: ${FEATURE_NAME} ${MODE} #${ITERATION}" 2>/dev/null || true
      echo -e "${CYAN}Child thread: $THREAD_ID${NC}"
    fi
  fi

  if is_recoverable_error "$OUTPUT" "$EXIT_CODE"; then
    handle_recoverable_error "$OUTPUT"
    ITERATION=$((ITERATION - 1))
    continue
  fi

  if [[ $EXIT_CODE -ne 0 ]]; then
    CONSECUTIVE_FAILURES=$((CONSECUTIVE_FAILURES + 1))
    echo ""
    echo -e "${RED}=== Error (exit code: $EXIT_CODE) ===${NC}"

    BACKOFF=$((30 * (2 ** (CONSECUTIVE_FAILURES - 1))))
    [[ $BACKOFF -gt 300 ]] && BACKOFF=300

    echo -e "${YELLOW}Retrying in ${BACKOFF}s... (consecutive failures: $CONSECUTIVE_FAILURES)${NC}"
    countdown $BACKOFF "Waiting..."
    ITERATION=$((ITERATION - 1))
    continue
  fi

  CONSECUTIVE_FAILURES=0

  if [[ "$RESULT_MSG" =~ "RALPH_COMPLETE" ]] || [[ "$OUTPUT" =~ "RALPH_COMPLETE" ]]; then
    echo ""
    echo -e "${GREEN}=== Ralph Complete ===${NC}"

    if [[ "$AUTO_MODE" == true && "$MODE" == "plan" ]]; then
      # Reset parent thread for build phase
      rm -f "$PARENT_THREAD_FILE"
      switch_to_build_mode
      continue
    fi

    echo -e "${GREEN}All tasks finished.${NC}"
    break
  fi

  if [[ $MAX_ITERATIONS -gt 0 && $ITERATION -ge $MAX_ITERATIONS ]]; then
    if [[ "$AUTO_MODE" == true && "$MODE" == "plan" ]]; then
      rm -f "$PARENT_THREAD_FILE"
      switch_to_build_mode
      continue
    fi
    echo ""
    echo -e "${GREEN}Reached max iterations ($MAX_ITERATIONS).${NC}"
    break
  fi

  sleep 2
done

echo ""
echo -e "${GREEN}Ralph loop complete. Iterations: $ITERATION${NC}"
```

Make the script executable:
```bash
chmod +x loop.sh
```

---

## End: Next Steps

After generating all files, tell the user:

> **Files generated:**
> - `specs/<feature-slug>.md` - Requirements specification
> - `IMPLEMENTATION_PLAN.md` - Task list with checkboxes
> - `PROMPT_plan.md` - Planning mode instructions
> - `PROMPT_build.md` - Build mode instructions
> - `loop.sh` - Dual-mode build loop script
>
> **Usage:**
> - `./loop.sh` - Auto mode: plan first, then build
> - `./loop.sh plan` - Planning mode only
> - `./loop.sh build` - Build mode only
> - `./loop.sh build 10` - Build mode, max 10 iterations
>
> **Thread organization:**
> - Each phase creates its own parent thread
> - Child threads named: `ralph: <feature-name> <mode> #N`
> - View thread hierarchy at https://ampcode.com/threads
>
> **Next step:** Run `./loop.sh` to start the loop.
