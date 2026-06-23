---
name: specs-e2e-verification
description: "Executes real end-to-end verification against a running application after specification implementation. Detects the application type, starts the local runtime (Docker, Node, Spring Boot, etc.), runs real tests (curl for REST APIs, Playwright for web SPAs, computer-use for desktop apps), verifies acceptance criteria from the functional specification, generates a markdown report, and tears down the environment. Use when: user asks to verify a completed spec with real tests, run e2e checks after implementation, validate acceptance criteria in a live environment, or test the feature for real after task completion."
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, TodoWrite, AskUserQuestion
---

# Specs E2E Verification

## Overview

Performs **real environment verification** after a specification has been implemented and cleaned up. This skill bridges the gap between unit-tested code and observable runtime behavior by:

1. Detecting the application type from project files
2. Starting the local runtime (Docker Compose, dev server, Spring Boot, etc.)
3. Deriving tests from `[IMP]` acceptance criteria in the functional specification
4. Executing real tests (`curl`, Playwright, computer-use)
5. Mapping results to acceptance criteria
6. Generating a verification report
7. Tearing down the environment

**Input**: `docs/specs/[id]/` (spec folder with functional specification and tasks)  
**Output**: `docs/specs/[id]/e2e-report-YYYY-MM-DD-HHMMSS.md`

## When to Use

- Use after `specs.task-implementation` and `specs.code-cleanup` to confirm the feature works in reality.
- Use when a developer says "test it for real", "verify the API actually works", "run e2e checks", or "validate acceptance criteria live".
- Use to generate evidence of feature completion before closing a specification.
- Do NOT use for unit testing, static analysis, or code review — this is runtime behavioral verification only.

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--spec` | Yes | Path to the specification folder (e.g., `docs/specs/001-feature/`) |
| `--task` | No | Specific task ID to limit verification scope (e.g., `TASK-003`) |
| `--keep-alive` | No | If present, skip teardown and leave the environment running |
| `--timeout` | No | Startup and test timeout in seconds (default: 120) |
| `--insecure` | No | If present, allow curl to use `-k` / `--insecure` (TLS bypass opt-in) |

## Best Practices

- **Safety first**: Never run destructive commands (`rm -rf`, `docker system prune`, `sudo`).
- **Detect, don’t assume**: Use file heuristics to determine the app type; ask the user only when ambiguous.
- **AC-driven**: Every test must trace back to an `[IMP]` acceptance criterion from the functional specification.
- **Clean up**: Always teardown unless `--keep-alive` is passed; warn about leftover processes.
- **No code changes**: This skill is read-only regarding source code. It may create reports but never patches logic.
- **Use TodoWrite**: Track progress across all 8 phases.

## Instructions

### Phase 1: Parse Arguments and Load Context

1. Parse `$ARGUMENTS`:
   - `--spec` (required): spec folder path. Validate that the directory exists and contains at least one functional specification file (`YYYY-MM-DD--*.md`). If missing or invalid, abort with an error.
   - `--task` (optional): task ID filter (e.g., `TASK-003`). If provided, validate that `tasks/<task-id>.md` exists inside the spec folder.
   - `--keep-alive` (optional): boolean flag. If present, skip teardown at the end.
   - `--timeout` (optional): positive integer in seconds. Default is `120`. Validate that the value is a positive integer; if not, abort with an error.
   - `--insecure` (optional): boolean flag. If present, curl commands MAY use `-k` / `--insecure` for local development with self-signed certificates. By default, TLS bypass is forbidden (REQ-NR003).

2. Read the functional specification and extract:
   - All acceptance criteria with their taxonomy tags (`[IMP]`, `[SEF]`, `[EXT]`)
   - Only `[IMP]` criteria will generate runtime tests

3. If `--task` is provided, read the task file and limit scope to its `provides` files and related AC.

4. Use `TodoWrite` to create a todo list for all 8 phases.

### Phase 1.5: Security Validation Gate

Before any command is executed, run the following security checks:

1. **Command Whitelist Check**:
   - The startup command derived in Phase 3 MUST match a pattern documented in `references/test-execution-patterns.md`.
   - IF the command is NOT in the whitelist → use `AskUserQuestion` to request explicit user confirmation before execution.
   - Whitelisted commands include: `docker compose up -d --build`, `./mvnw spring-boot:run`, `./gradlew bootRun`, `npm run dev`, `npm run start:dev`, `npm start`, `cargo tauri build --debug`, `cargo tauri dev`, `npm run electron:dev`, `npx electron .`, `open *.app`, and equivalent local process launchers.
   - Any command containing `sudo`, `rm -rf`, `docker system prune`, `mkfs`, `dd`, or similar destructive operations is NOT whitelisted and SHALL be rejected.

2. **Forbidden Pattern Scan** (REQ-NR001):
   - Scan the derived startup command and all generated test commands for:
     - `sudo` → abort with: "Forbidden: sudo is not permitted during E2E verification."
     - `rm -rf` → abort with: "Forbidden: rm -rf is not permitted during E2E verification."
     - `docker system prune` → abort with: "Forbidden: docker system prune is not permitted during E2E verification."
     - Any `rm`, `drop`, `destroy`, `prune` targeting databases, volumes, or local data → abort with: "Forbidden: destructive data operations are not permitted."
   - IF any forbidden pattern is detected → abort immediately; do NOT proceed to startup.

3. **TLS Enforcement Check** (REQ-NR003):
   - For any generated curl command:
     - IF it contains `-k` or `--insecure` AND `--insecure` was NOT passed → abort with: "Forbidden: curl TLS bypass (-k / --insecure) is disabled by default. Pass --insecure to opt-in."
     - IF `--insecure` was passed → log a warning: "WARNING: TLS certificate verification is disabled. Use only for local development."

4. **Data Integrity Pre-Check** (REQ-NR004):
   - Before executing startup commands, inspect them for patterns that would overwrite or delete existing data (e.g., `rm`, `drop`, `prune`, volume deletion flags).
   - IF the command would modify existing databases, volumes, or local data directories → abort with: "Forbidden: startup commands must not overwrite or delete existing data."

### Phase 2: Detect Application Type and Discover Port

1. Set `PROJECT_ROOT` to the directory containing `.git` or the parent directory of `--spec`.

2. Inspect `PROJECT_ROOT` for configuration files using the following heuristics (execute in order):

   **Docker-managed** (highest priority):
   ```bash
   [ -f "$PROJECT_ROOT/docker-compose.yml" ] || [ -f "$PROJECT_ROOT/docker-compose.yaml" ] || [ -f "$PROJECT_ROOT/compose.yml" ]
   ```
   If any of these files exist, classify as **Docker-managed** regardless of other framework configs.

   **JVM / Spring Boot**:
   ```bash
   [ -f "$PROJECT_ROOT/pom.xml" ] || [ -f "$PROJECT_ROOT/build.gradle" ] || [ -f "$PROJECT_ROOT/build.gradle.kts" ]
   ```
   AND verify source directory exists:
   ```bash
   [ -d "$PROJECT_ROOT/src/main/java" ]
   ```
   If both conditions are true, classify as **JVM-based service**.

   **NestJS**:
   ```bash
   [ -f "$PROJECT_ROOT/package.json" ] && grep -q '"@nestjs/core"' "$PROJECT_ROOT/package.json"
   ```
   If true, classify as **NestJS**.

   **Web SPA (React / Vue / Angular)**:
   ```bash
   [ -f "$PROJECT_ROOT/package.json" ] && ( grep -q '"react"' "$PROJECT_ROOT/package.json" || grep -q '"vue"' "$PROJECT_ROOT/package.json" || grep -q '"@angular/core"' "$PROJECT_ROOT/package.json" )
   ```
   If true, classify as **Web SPA**.

   **Desktop App**:
   ```bash
   [ -f "$PROJECT_ROOT/src-tauri/Cargo.toml" ] || ( [ -f "$PROJECT_ROOT/package.json" ] && grep -q '"electron"' "$PROJECT_ROOT/package.json" ) || [ -n "$(find "$PROJECT_ROOT" -maxdepth 2 -name '*.csproj' -print -quit 2>/dev/null)" ]
   ```
   If true, classify as **Desktop App**.

   **Python**:
   ```bash
   [ -f "$PROJECT_ROOT/requirements.txt" ] || [ -f "$PROJECT_ROOT/pyproject.toml" ] || [ -f "$PROJECT_ROOT/app.py" ] || [ -f "$PROJECT_ROOT/manage.py" ]
   ```
   If true, classify as **Python**.

3. Apply priority rules:
   - **Docker Compose is always prioritized**: If a Docker Compose file exists AND any framework config also exists, classify as **Docker-managed**. The compose stack defines the runtime.
   - If multiple non-Docker configs are detected (e.g., both `pom.xml` and `package.json` without Docker Compose):
     - If the spec's domain clearly indicates backend vs frontend (e.g., spec title contains "API", "backend", "service"), prefer **JVM** or **NestJS**.
     - If the spec's domain clearly indicates frontend (e.g., spec title contains "UI", "page", "component"), prefer **Web SPA**.
     - If still ambiguous, proceed to user prompt (step 4).

4. If no recognizable config is found, OR if multiple non-Docker configs exist and the spec domain is ambiguous, use `AskUserQuestion` with exactly these options:
   - "REST API"
   - "Web SPA"
   - "Desktop"
   - "Skip"

5. **Port Discovery**: Once the application type is known, determine the target port by inspecting framework configuration files in this order:

   - **Vite projects** (`vite.config.ts` or `vite.config.js`):
     ```bash
     grep -oE 'port:\s*[0-9]+' "$PROJECT_ROOT/vite.config.ts" 2>/dev/null | grep -oE '[0-9]+' || \
     grep -oE 'port:\s*[0-9]+' "$PROJECT_ROOT/vite.config.js" 2>/dev/null | grep -oE '[0-9]+'
     ```

   - **Spring Boot** (`application.yml`):
     ```bash
     grep -A5 '^server:' "$PROJECT_ROOT/src/main/resources/application.yml" 2>/dev/null | grep 'port:' | head -1 | tr -dc '0-9'
     ```

   - **Spring Boot** (`application.properties`):
     ```bash
     grep '^server.port=' "$PROJECT_ROOT/src/main/resources/application.properties" 2>/dev/null | cut -d= -f2 | tr -dc '0-9'
     ```

   - **Node.js / package.json scripts**:
     ```bash
     grep -oE -- '--port [0-9]+' "$PROJECT_ROOT/package.json" 2>/dev/null | grep -oE '[0-9]+' | head -1
     ```
     Also check for `PORT` environment variable in scripts:
     ```bash
     grep -oE 'PORT=[0-9]+' "$PROJECT_ROOT/package.json" 2>/dev/null | grep -oE '[0-9]+' | head -1
     ```

   - **Fallback defaults** (if no port is found in any config file):
     | App Type | Default Port |
     |----------|-------------|
     | Node.js / NestJS | 3000 |
     | Spring Boot (JVM) | 8080 |
     | Angular | 4200 |
     | Vite (React/Vue) | 5173 |
     | Python | 8000 |

6. Log the detected type and discovered port; both will be recorded in the report.

### Phase 3: Start Environment and Wait for Readiness

Read `references/test-execution-patterns.md` (shipped with this skill) for the command mapping. Based on detection:

**Data integrity pre-flight** (REQ-NR004): Before executing the startup command, verify it does not contain patterns that overwrite or delete existing databases, volumes, or local data (e.g., `rm`, `--volumes`, `prune`, `drop`). If a destructive pattern is detected, abort immediately with: "Startup aborted: command would destroy existing data."

1. **Initialize runtime state**:
   - `STARTUP_COMMAND=""` — the exact command used to start the environment
   - `HEALTH_CHECK_METHOD=""` — description of how readiness was determined
   - `STARTUP_LOGS_FILE="$(mktemp)"` — temp file capturing stdout/stderr from startup
   - `STARTUP_TIMEOUT="${TIMEOUT:-120}"` — seconds to wait for readiness
   - `START_TIME="$(date +%s)"`
   - `STARTUP_PID=""` — background process PID (for local processes)

2. **Pre-startup port check** (all types):
   ```bash
   if lsof -i :"$TARGET_PORT" >/dev/null 2>&1 || nc -z localhost "$TARGET_PORT" 2>/dev/null; then
       echo "Port $TARGET_PORT is already in use."
       EXISTING_PID=$(lsof -ti:"$TARGET_PORT" | head -n1)
       EXISTING_CMD=$(ps -p "$EXISTING_PID" -o comm= 2>/dev/null || echo "unknown")
       if [ "$APP_TYPE" = "Docker-managed" ] && docker ps --format '{{.Names}}' 2>/dev/null | grep -q "$EXISTING_CMD"; then
           echo "Existing Docker container detected on port $TARGET_PORT; reusing it."
           STARTUP_COMMAND="(existing container reused)"
       elif [ "$APP_TYPE" = "JVM-based service" ] && echo "$EXISTING_CMD" | grep -q "java"; then
           echo "Existing Java process detected on port $TARGET_PORT; reusing it."
           STARTUP_COMMAND="(existing Java process reused)"
       else
           echo "Port $TARGET_PORT is occupied by an unrelated process ($EXISTING_CMD). Free the port and retry."
           exit 1
       fi
   fi
   ```

3. **Docker-managed startup**:
   - Verify Docker daemon is reachable:
     ```bash
     if ! docker info >/dev/null 2>&1; then
         echo "Docker is not available. Please start Docker Desktop or use direct framework startup."
         exit 1
     fi
     ```
   - Set `STARTUP_COMMAND="docker compose up -d --build"`
   - Execute:
     ```bash
     cd "$PROJECT_ROOT" && docker compose up -d --build >> "$STARTUP_LOGS_FILE" 2>&1
     ```
   - **Health check loop** (timeout enforced):
     ```bash
     HEALTH_CHECK_METHOD="docker compose ps --format json"
     READY=false
     while [ $(( $(date +%s) - START_TIME )) -lt "$STARTUP_TIMEOUT" ]; do
         # Option A: Docker native health status (supports both JSON array and NDJSON)
         if docker compose ps --format json 2>/dev/null | jq -s -e '.[] | select(.Health=="healthy")' >/dev/null 2>&1; then
             READY=true
             HEALTH_CHECK_METHOD="docker compose ps (HEALTHCHECK=healthy)"
             break
         fi
         # Option B: Fallback port polling if no HEALTHCHECK defined
         if curl -sf "http://localhost:${TARGET_PORT}" >/dev/null 2>&1; then
             READY=true
             HEALTH_CHECK_METHOD="port polling via curl on localhost:${TARGET_PORT} (every 3s)"
             break
         fi
         sleep 3
     done
     if [ "$READY" != "true" ]; then
         echo "Startup timeout (${STARTUP_TIMEOUT}s) exceeded for Docker Compose."
         docker compose logs --tail=50 >> "$STARTUP_LOGS_FILE" 2>&1
         # Attempt cleanup to avoid orphan containers (REQ-NR006)
         docker compose down >/dev/null 2>&1 || true
         exit 1
     fi
     ```

4. **Spring Boot startup**:
   - Determine build tool and launch in background with log capture:
     ```bash
     if [ -f "$PROJECT_ROOT/pom.xml" ]; then
         cd "$PROJECT_ROOT" && ./mvnw spring-boot:run -Dspring-boot.run.profiles=e2e >> "$STARTUP_LOGS_FILE" 2>&1 &
         STARTUP_PID=$!
         STARTUP_COMMAND="./mvnw spring-boot:run -Dspring-boot.run.profiles=e2e"
     elif [ -f "$PROJECT_ROOT/build.gradle" ] || [ -f "$PROJECT_ROOT/build.gradle.kts" ]; then
         cd "$PROJECT_ROOT" && ./gradlew bootRun --args='--spring.profiles.active=e2e' >> "$STARTUP_LOGS_FILE" 2>&1 &
         STARTUP_PID=$!
         STARTUP_COMMAND="./gradlew bootRun --args='--spring.profiles.active=e2e'"
     fi
     ```
   - **Health check loop** (timeout enforced):
     ```bash
     HEALTH_CHECK_METHOD="Spring Boot actuator /actuator/health"
     READY=false
     while [ $(( $(date +%s) - START_TIME )) -lt "$STARTUP_TIMEOUT" ]; do
         # Option A: Actuator health endpoint
         if curl -sf "http://localhost:${TARGET_PORT}/actuator/health" >/dev/null 2>&1; then
             READY=true
             HEALTH_CHECK_METHOD="Spring Boot actuator /actuator/health"
             break
         fi
         # Option B: Fallback to raw port readiness
         if nc -z localhost "$TARGET_PORT" 2>/dev/null; then
             READY=true
             HEALTH_CHECK_METHOD="port polling via nc on localhost:${TARGET_PORT} (every 3s)"
             break
         fi
         # Fail fast if the background process exited early
         if [ -n "$STARTUP_PID" ] && ! kill -0 "$STARTUP_PID" 2>/dev/null; then
             echo "Spring Boot process exited before reaching healthy state."
             break
         fi
         sleep 3
     done
     if [ "$READY" != "true" ]; then
         echo "Startup timeout (${STARTUP_TIMEOUT}s) exceeded for Spring Boot."
         # Capture last lines of startup logs for the report
         tail -n 100 "$STARTUP_LOGS_FILE" >> "$STARTUP_LOGS_FILE".final 2>&1 || true
         # Attempt cleanup (REQ-NR006)
         [ -n "$STARTUP_PID" ] && kill -TERM "$STARTUP_PID" 2>/dev/null || true
         exit 1
     fi
     ```

5. **NestJS / Node.js startup**:
   - Verify `node_modules` exists to avoid cryptic errors:
     ```bash
     if [ ! -d "$PROJECT_ROOT/node_modules" ]; then
         echo "node_modules not found. Run 'npm install' before verification."
         exit 1
     fi
     ```
   - Determine the startup command from `package.json` scripts:
     ```bash
     if [ "$APP_TYPE" = "NestJS" ] && grep -q '"start:dev"' "$PROJECT_ROOT/package.json" 2>/dev/null; then
         cd "$PROJECT_ROOT" && npm run start:dev >> "$STARTUP_LOGS_FILE" 2>&1 &
         STARTUP_PID=$!
         STARTUP_COMMAND="npm run start:dev"
     elif grep -q '"dev"' "$PROJECT_ROOT/package.json" 2>/dev/null; then
         cd "$PROJECT_ROOT" && npm run dev >> "$STARTUP_LOGS_FILE" 2>&1 &
         STARTUP_PID=$!
         STARTUP_COMMAND="npm run dev"
     else
         cd "$PROJECT_ROOT" && npm start >> "$STARTUP_LOGS_FILE" 2>&1 &
         STARTUP_PID=$!
         STARTUP_COMMAND="npm start"
     fi
     ```
   - **Health check loop** (timeout enforced):
     ```bash
     HEALTH_CHECK_METHOD="port polling via nc/curl on localhost:${TARGET_PORT} (every 3s)"
     READY=false
     while [ $(( $(date +%s) - START_TIME )) -lt "$STARTUP_TIMEOUT" ]; do
         # Option A: HTTP readiness via curl
         if curl -sf "http://localhost:${TARGET_PORT}" >/dev/null 2>&1; then
             READY=true
             HEALTH_CHECK_METHOD="curl on localhost:${TARGET_PORT}"
             break
         fi
         # Option B: Raw port readiness via nc
         if nc -z localhost "$TARGET_PORT" 2>/dev/null; then
             READY=true
             HEALTH_CHECK_METHOD="nc -z localhost:${TARGET_PORT}"
             break
         fi
         # Fail fast if the background process exited early
         if [ -n "$STARTUP_PID" ] && ! kill -0 "$STARTUP_PID" 2>/dev/null; then
             echo "Node.js/NestJS process exited before reaching healthy state."
             break
         fi
         sleep 3
     done
     if [ "$READY" != "true" ]; then
         echo "Startup timeout (${STARTUP_TIMEOUT}s) exceeded for Node.js/NestJS."
         tail -n 100 "$STARTUP_LOGS_FILE" >> "$STARTUP_LOGS_FILE".final 2>&1 || true
         # Attempt cleanup (REQ-NR006)
         [ -n "$STARTUP_PID" ] && kill -TERM "$STARTUP_PID" 2>/dev/null || true
         exit 1
     fi
     ```
   - **Console ready detection**: After readiness is confirmed, scan `$STARTUP_LOGS_FILE` for common server-ready messages (e.g., `Nest application successfully started`, `Local:`, `ready in`, `Server running`) and record the first matching line in the report as evidence of successful startup.
6. **Python (FastAPI / Django / Flask)** (see `references/test-execution-patterns.md`):
   - Run `uvicorn main:app --reload`, `python manage.py runserver`, or `flask run`
   - Wait for port readiness
7. **Desktop App** (Tauri / Electron / .NET MAUI) (see `references/test-execution-patterns.md`):

   **Framework detection**:
   ```bash
   DESKTOP_FRAMEWORK=""
   if [ -f "$PROJECT_ROOT/src-tauri/Cargo.toml" ]; then
       DESKTOP_FRAMEWORK="tauri"
   elif [ -f "$PROJECT_ROOT/package.json" ] && grep -q '"electron"' "$PROJECT_ROOT/package.json"; then
       DESKTOP_FRAMEWORK="electron"
   elif [ -n "$(find "$PROJECT_ROOT" -maxdepth 2 -name '*.csproj' -print -quit 2>/dev/null)" ]; then
       DESKTOP_FRAMEWORK="dotnet-maui"
   fi
   ```

   **Build step** (triggered when no pre-built debug binary exists or when source is newer than target):

   - **Tauri**:
     ```bash
     if [ "$DESKTOP_FRAMEWORK" = "tauri" ]; then
         if ! command -v cargo >/dev/null 2>&1; then
             echo "ERROR: Rust/Cargo is not installed. Tauri build requires cargo."
             exit 1
         fi
         BUILD_COMMAND="cargo tauri build --debug"
         cd "$PROJECT_ROOT" && $BUILD_COMMAND >> "$STARTUP_LOGS_FILE" 2>&1
         BUILD_EXIT_CODE=$?
         if [ "$BUILD_EXIT_CODE" -ne 0 ]; then
             echo "Tauri build failed (exit code $BUILD_EXIT_CODE). See startup logs for details."
             exit 1
         fi
         STARTUP_COMMAND="$BUILD_COMMAND (build succeeded)"
     fi
     ```

   - **Electron**:
     ```bash
     if [ "$DESKTOP_FRAMEWORK" = "electron" ]; then
         if [ ! -d "$PROJECT_ROOT/node_modules" ]; then
             echo "ERROR: node_modules not found. Run 'npm install' before verification."
             exit 1
         fi
         BUILD_COMMAND="(no separate build required for dev mode)"
         STARTUP_COMMAND="npm run electron:dev"
         if grep -q '"electron:build"' "$PROJECT_ROOT/package.json" 2>/dev/null; then
             BUILD_COMMAND="npm run electron:build"
             cd "$PROJECT_ROOT" && $BUILD_COMMAND >> "$STARTUP_LOGS_FILE" 2>&1
             BUILD_EXIT_CODE=$?
             if [ "$BUILD_EXIT_CODE" -ne 0 ]; then
                 echo "Electron build failed (exit code $BUILD_EXIT_CODE). See startup logs for details."
                 exit 1
             fi
         fi
     fi
     ```

   **Launch the built application binary**:

   - **Tauri (macOS)**:
     ```bash
     APP_BUNDLE=$(find "$PROJECT_ROOT/src-tauri/target/debug/bundle" -name "*.app" -print -quit 2>/dev/null)
     if [ -n "$APP_BUNDLE" ]; then
         open "$APP_BUNDLE" >> "$STARTUP_LOGS_FILE" 2>&1 &
         STARTUP_PID=$!
         STARTUP_COMMAND="open $APP_BUNDLE"
     else
         DEV_BINARY=$(find "$PROJECT_ROOT/src-tauri/target/debug" -maxdepth 1 -type f -executable ! -name '*.dylib' ! -name '*.so' -print -quit 2>/dev/null)
         if [ -n "$DEV_BINARY" ]; then
             "$DEV_BINARY" >> "$STARTUP_LOGS_FILE" 2>&1 &
             STARTUP_PID=$!
             STARTUP_COMMAND="$DEV_BINARY"
         else
             cargo tauri dev >> "$STARTUP_LOGS_FILE" 2>&1 &
             STARTUP_PID=$!
             STARTUP_COMMAND="cargo tauri dev"
         fi
     fi
     ```

   - **Tauri (Linux)**:
     ```bash
     APP_BINARY=$(find "$PROJECT_ROOT/src-tauri/target/debug" -maxdepth 1 -type f -executable ! -name '*.so' -print -quit 2>/dev/null)
     if [ -n "$APP_BINARY" ]; then
         "$APP_BINARY" >> "$STARTUP_LOGS_FILE" 2>&1 &
         STARTUP_PID=$!
         STARTUP_COMMAND="$APP_BINARY"
     else
         cargo tauri dev >> "$STARTUP_LOGS_FILE" 2>&1 &
         STARTUP_PID=$!
         STARTUP_COMMAND="cargo tauri dev"
     fi
     ```

   - **Electron**:
     ```bash
     if grep -q '"electron:dev"' "$PROJECT_ROOT/package.json" 2>/dev/null; then
         cd "$PROJECT_ROOT" && npm run electron:dev >> "$STARTUP_LOGS_FILE" 2>&1 &
         STARTUP_PID=$!
         STARTUP_COMMAND="npm run electron:dev"
     elif grep -q '"start"' "$PROJECT_ROOT/package.json" 2>/dev/null; then
         cd "$PROJECT_ROOT" && npm start >> "$STARTUP_LOGS_FILE" 2>&1 &
         STARTUP_PID=$!
         STARTUP_COMMAND="npm start"
     else
         cd "$PROJECT_ROOT" && npx electron . >> "$STARTUP_LOGS_FILE" 2>&1 &
         STARTUP_PID=$!
         STARTUP_COMMAND="npx electron ."
     fi
     ```

   **Health check** (process appearance, timeout enforced):
   ```bash
   HEALTH_CHECK_METHOD="process polling via ps/kill -0 (every 3s)"
   READY=false
   while [ $(( $(date +%s) - START_TIME )) -lt "$STARTUP_TIMEOUT" ]; do
       if [ -n "$STARTUP_PID" ] && kill -0 "$STARTUP_PID" 2>/dev/null; then
           READY=true
           HEALTH_CHECK_METHOD="process PID ${STARTUP_PID} confirmed alive"
           break
       fi
       sleep 3
   done
   if [ "$READY" != "true" ]; then
       echo "Startup timeout (${STARTUP_TIMEOUT}s) exceeded for Desktop app."
       tail -n 100 "$STARTUP_LOGS_FILE" >> "$STARTUP_LOGS_FILE".final 2>&1 || true
       [ -n "$STARTUP_PID" ] && kill -TERM "$STARTUP_PID" 2>/dev/null || true
       exit 1
   fi
   ```

8. **Post-startup bookkeeping** (all types):
   - Record `STARTUP_COMMAND` and `HEALTH_CHECK_METHOD` in report metadata (AC-010).
   - Append `STARTUP_LOGS_FILE` contents to the report under **Raw Output** (REQ-020).
   - If startup fails for any reason, capture all available logs and abort with a clear error message.

### Phase 4: Generate and Execute Tests

**CRITICAL**: Only test `[IMP]` acceptance criteria. Translate each into one or more concrete runtime actions.

#### REST API Tests (curl)

**Prerequisite check**: Before generating any tests, verify `curl` is installed:
```bash
if ! command -v curl >/dev/null 2>&1; then
    echo "ERROR: curl is not installed."
    echo "Install instructions:"
    echo "  macOS:    brew install curl"
    echo "  Ubuntu:   sudo apt-get install curl"
    echo "  Windows:  choco install curl   or   winget install curl"
    exit 1
fi
if ! command -v jq >/dev/null 2>&1; then
    echo "WARNING: jq is not installed. JSON body assertions will fall back to grep (less precise)."
    echo "Install instructions:"
    echo "  macOS:    brew install jq"
    echo "  Ubuntu:   sudo apt-get install jq"
    echo "  Windows:  choco install jq   or   winget install jqlang.jq"
fi
```

**1. Parse `[IMP]` AC for endpoint hints**

For each `[IMP]` acceptance criterion in the specification:
- Extract the HTTP method by searching for keywords: `GET`, `POST`, `PUT`, `PATCH`, `DELETE` (case-insensitive).
- Extract the endpoint path by searching for patterns starting with `/` followed by alphanumeric segments, e.g., `/api/users`, `/v1/health`.
- Extract the expected HTTP status code by searching for numeric patterns `2xx`, `3xx`, `4xx`, `5xx` or specific codes like `200`, `201`, `204`, `400`, `401`, `403`, `404`, `500`.
- Extract expected `Content-Type` by searching for `application/json`, `text/plain`, `text/html`, etc.
- Extract expected response body hints (field names, array presence, string values) from the AC text.

If an `[IMP]` AC does **not** contain a parseable endpoint path and method, mark it `MANUAL CHECK REQUIRED` and skip to the next criterion.

**2. Discover authentication credentials**

Before constructing curl commands, attempt to locate test credentials by scanning the following files in `PROJECT_ROOT` (in order):

| File | Key Patterns |
|------|-------------|
| `.env.test` | `E2E_AUTH_TOKEN=...`, `E2E_USERNAME=...`, `E2E_PASSWORD=...` |
| `.env.local` | `E2E_AUTH_TOKEN=...`, `E2E_USERNAME=...`, `E2E_PASSWORD=...` |
| `application-test.yml` | `e2e.auth-token: ...`, `e2e.username: ...`, `e2e.password: ...` |
| `application-test.properties` | `e2e.auth-token=...`, `e2e.username=...`, `e2e.password=...` |
| `e2e.credentials.json` | Top-level keys `E2E_AUTH_TOKEN`, `E2E_USERNAME`, `E2E_PASSWORD` |

Discovery logic:
```bash
# .env files
[ -f "$PROJECT_ROOT/.env.test" ] && export $(grep -E '^(E2E_AUTH_TOKEN|E2E_USERNAME|E2E_PASSWORD)=' "$PROJECT_ROOT/.env.test" | xargs)
[ -f "$PROJECT_ROOT/.env.local" ] && export $(grep -E '^(E2E_AUTH_TOKEN|E2E_USERNAME|E2E_PASSWORD)=' "$PROJECT_ROOT/.env.local" | xargs)

# Spring YAML
[ -f "$PROJECT_ROOT/src/main/resources/application-test.yml" ] && \
  E2E_AUTH_TOKEN=$(grep -A1 'e2e:' "$PROJECT_ROOT/src/main/resources/application-test.yml" | grep 'auth-token:' | sed 's/.*: *//')

# Spring properties
[ -f "$PROJECT_ROOT/src/main/resources/application-test.properties" ] && \
  E2E_AUTH_TOKEN=$(grep '^e2e.auth-token=' "$PROJECT_ROOT/src/main/resources/application-test.properties" | cut -d= -f2-)

# JSON credentials file
[ -f "$PROJECT_ROOT/e2e.credentials.json" ] && \
  E2E_AUTH_TOKEN=$(jq -r '.E2E_AUTH_TOKEN // empty' "$PROJECT_ROOT/e2e.credentials.json")
```

If **no** credentials are found after scanning all files AND the AC text implies authentication is required (mentions "auth", "login", "token", "protected", "bearer", "API key"), use `AskUserQuestion` to prompt the user:
- "Enter E2E_AUTH_TOKEN (or leave blank if none)"
- "Enter E2E_USERNAME (or leave blank if none)"
- "Enter E2E_PASSWORD (or leave blank if none)"

**Security**: Redact token values in the E2E report; show only the header name (e.g., `Authorization: Bearer <redacted>`).

**3. Generate curl commands**

For each parseable `[IMP]` AC, construct the curl command using this exact pattern:
```bash
curl -s -w "\n%{http_code}" -o /tmp/e2e_resp.json \
  -X <METHOD> \
  -H "Content-Type: application/json" \
  <AUTH_HEADER> \
  -d '<REQUEST_BODY>' \
  "http://localhost:${TARGET_PORT}<PATH>"
```

Rules:
- Always include `-s -w "\n%{http_code}" -o /tmp/e2e_resp.json`.
- `-X <METHOD>`: only add if the method is not `GET`. For `GET`, omit `-X` entirely.
- `-H "Content-Type: application/json"`: only add for `POST`, `PUT`, `PATCH`.
- `-d '<REQUEST_BODY>'`: only add when the AC describes a request body. If no body is described, omit `-d`.
- `<AUTH_HEADER>`:
  - If `E2E_AUTH_TOKEN` is set: `-H "Authorization: Bearer ${E2E_AUTH_TOKEN}"`
  - If `E2E_USERNAME` and `E2E_PASSWORD` are set: `-u "${E2E_USERNAME}:${E2E_PASSWORD}"`
  - If no credentials found: omit auth header.
- **TLS enforcement** (REQ-NR003): NEVER add `-k` or `--insecure` to curl commands unless the `--insecure` flag was explicitly passed when invoking the skill. If `--insecure` was passed, log a warning that TLS verification is disabled.
- Store the raw response body in `/tmp/e2e_resp.json` and the status code on the last line of stdout.

**4. Execute curl and assert (no retry)**

Execute each curl command **exactly once** (REQ-NR008). Do NOT retry on failure.

```bash
HTTP_CODE=$(curl -s -w "\n%{http_code}" -o /tmp/e2e_resp.json <curl args> | tail -n 1)
```

Assertions (all must pass for the AC to be `VERIFIED`):

a. **HTTP status code**:
   ```bash
   if [ "$HTTP_CODE" -ne "$EXPECTED_STATUS" ]; then
       echo "FAIL: Expected status $EXPECTED_STATUS, got $HTTP_CODE"
       STATUS="FAILED"
   fi
   ```

b. **Content-Type header** (only if specified in the AC):
   ```bash
   ACTUAL_CT=$(curl -s -o /dev/null -D - <curl args> | grep -i "Content-Type:" | head -1 | sed 's/Content-Type: //i' | tr -d '\r')
   if [ -n "$EXPECTED_CT" ] && ! echo "$ACTUAL_CT" | grep -qi "$EXPECTED_CT"; then
       echo "FAIL: Expected Content-Type '$EXPECTED_CT', got '$ACTUAL_CT'"
       STATUS="FAILED"
   fi
   ```

c. **Response body structure** using `jq` (preferred) or `grep` (fallback):
   - If `jq` is installed and the response is JSON:
     ```bash
     # Assert field exists
     jq -e '.fieldName' /tmp/e2e_resp.json >/dev/null || { echo "FAIL: Missing .fieldName"; STATUS="FAILED"; }

     # Assert field equals expected value
     jq -e '.fieldName == "expectedValue"' /tmp/e2e_resp.json >/dev/null || { echo "FAIL: .fieldName mismatch"; STATUS="FAILED"; }

     # Assert array length
     jq -e '(.items | length) > 0' /tmp/e2e_resp.json >/dev/null || { echo "FAIL: .items is empty"; STATUS="FAILED"; }

     # Assert nested field
     jq -e '.data.user.email' /tmp/e2e_resp.json >/dev/null || { echo "FAIL: Missing .data.user.email"; STATUS="FAILED"; }
     ```
   - If `jq` is NOT installed, use `grep` as fallback:
     ```bash
     grep -q '"fieldName"' /tmp/e2e_resp.json || { echo "FAIL: Missing fieldName"; STATUS="FAILED"; }
     ```

**5. Record results**

For each curl test, record:
- AC ID and text (truncated)
- Generated curl command (with auth tokens redacted)
- Expected status code, Content-Type, body assertions
- Actual status code, Content-Type, body snippet (first 500 chars)
- Pass/fail status
- Execution time (optional, for report reference)

If any assertion fails, mark the AC as `FAILED` immediately. Do not retry.


#### Web SPA Tests (Playwright)

**Prerequisite check**: Before generating any SPA tests, verify Playwright is installed:

```bash
PLAYWRIGHT_VERSION=$(npx playwright --version 2>/dev/null || echo "")
if [ -z "$PLAYWRIGHT_VERSION" ]; then
    echo "ERROR: Playwright is not installed."
    echo "Install instructions:"
    echo "  npm install -D @playwright/test"
    echo "  npx playwright install chromium"
    echo ""
    echo "Skipping all Web SPA tests. Acceptance criteria for SPA interactions will be marked MANUAL CHECK REQUIRED."
    for ac_id in $(get_spa_ac_ids); do
        record_result "$ac_id" "MANUAL CHECK REQUIRED" "Playwright not installed"
    done
    # Continue to next test category; do not abort the whole verification
fi
echo "Playwright version: $PLAYWRIGHT_VERSION"
```

If Playwright is missing, the skill MUST report the gap with the install commands above and skip SPA tests. Do NOT attempt to auto-install.

**1. Prepare artifact directory**

```bash
ARTIFACT_DIR="${SPEC_FOLDER}/e2e-artifacts"
mkdir -p "$ARTIFACT_DIR"
```

**2. Parse `[IMP]` AC for UI behavior hints**

For each `[IMP]` acceptance criterion in the specification that relates to Web SPA behavior:
- Extract UI interaction keywords: `click`, `fill`, `type`, `select`, `submit`, `navigate`, `scroll`, `hover`.
- Extract target selectors by searching for patterns:
  - `data-testid="..."` or `data-testid='...'` → `[data-testid=...]`
  - `id="..."` or `id='...'` → `#...`
  - `class="..."` or `class='...'` → `.class-name` (replace spaces with dots)
  - Button/link text mentions → `text=...`
  - URL path mentions → `/path`
- Extract expected visible states: text content expectations, URL expectations, element presence/absence, count expectations.
- Extract form field names and expected input values.

If an `[IMP]` AC does **not** contain parseable UI behavior or visible state hints, mark it `MANUAL CHECK REQUIRED` and skip to the next criterion.

**3. Launch headless browser context**

Browser MUST be headless by default. Only use headed mode if the user explicitly passes `--headed`.

For each SPA test, generate a temporary Playwright script and execute it with `node`:

```bash
DEV_SERVER_URL="http://localhost:${TARGET_PORT}"
TEST_SCRIPT="$(mktemp /tmp/e2e-spa-XXXXXX.js)"

cat > "$TEST_SCRIPT" << 'PLAYWRIGHT_EOF'
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1280, height: 720 },
    userAgent: 'DeveloperKit-E2E/1.0'
  });
  const page = await context.newPage();
  // Actions and assertions injected here
  await browser.close();
})();
PLAYWRIGHT_EOF

node "$TEST_SCRIPT"
```

**4. Translate AC into Playwright actions**

For each parsed UI interaction, generate the corresponding Playwright action inside the temporary script:

| AC Description Pattern | Playwright Action |
|------------------------|-------------------|
| "click [selector]" | `await page.click('[data-testid=refresh]');` |
| "fill [selector] with [value]" | `await page.fill('#username', 'testuser');` |
| "type [value] into [selector]" | `await page.type('input[name=search]', 'query');` |
| "select [value] in [selector]" | `await page.selectOption('select[name=country]', 'US');` |
| "submit [form]" | `await page.click('button[type=submit]');` |
| "navigate to [path]" | `await page.goto('http://localhost:${TARGET_PORT}/path');` |
| "hover over [selector]" | `await page.hover('.tooltip-trigger');` |
| "scroll to [selector]" | `await page.locator('[data-testid=footer]').scrollIntoViewIfNeeded();` |

**Selector precedence** (most specific to least specific):
1. `[data-testid=...]` — preferred, most stable
2. `#id` — unique element ID
3. `.class-name` — CSS class
4. `[name=...]` — form element name
5. `text=...` — visible text content (fallback)

**5. Assert visible states**

For each expected visible state, generate the corresponding assertion inside the temporary script:

| AC Description Pattern | Playwright Assertion |
|------------------------|----------------------|
| "page shows [text]" | `await expect(page.locator('body')).toContainText('text');` |
| "[selector] has text [value]" | `await expect(page.locator('[data-testid=title]')).toHaveText('value');` |
| "[selector] contains [text]" | `await expect(page.locator('.message')).toContainText('text');` |
| "table has [N] rows" | `expect(await page.locator('table tbody tr').count()).toBe(N);` |
| "URL is [path]" | `expect(page.url()).toBe('http://localhost:${TARGET_PORT}/path');` |
| "URL contains [fragment]" | `expect(page.url()).toContain('/fragment');` |
| "[selector] is visible" | `await expect(page.locator('[data-testid=modal]')).toBeVisible();` |
| "[selector] is hidden" | `await expect(page.locator('[data-testid=spinner]')).toBeHidden();` |

**6. Execute test with timeout enforcement**

Each Playwright test MUST enforce a per-test timeout to prevent indefinite hangs (REQ-NR007). The wrapper script uses the `timeout` command:

```bash
TEST_TIMEOUT_SEC=30

npx playwright --version >/dev/null 2>&1 || {
    echo "Playwright not installed; skipping SPA tests."
    record_spa_manual_check
    continue
}

# Build the inline test script
TEST_SCRIPT="$(mktemp /tmp/e2e-spa-XXXXXX.js)"
cat > "$TEST_SCRIPT" << EOF
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  page.setDefaultTimeout(${TEST_TIMEOUT_SEC}000);
  page.setDefaultNavigationTimeout(${TEST_TIMEOUT_SEC}000);
  try {
    await page.goto('${DEV_SERVER_URL}');
    // --- GENERATED ACTIONS ---
    // --- GENERATED ASSERTIONS ---
    console.log('RESULT: PASS');
  } catch (error) {
    console.error('RESULT: FAIL:', error.message);
    const screenshotPath = '${ARTIFACT_DIR}/screenshot-' + Date.now() + '-ac-${AC_ID}.png';
    await page.screenshot({ path: screenshotPath, fullPage: true }).catch(() => {});
    console.error('SCREENSHOT:', screenshotPath);
    process.exitCode = 1;
  } finally {
    await browser.close();
  }
})();
EOF

# Run with timeout wrapper; if the test hangs, it is killed and marked FAILED
if timeout --signal=TERM $((TEST_TIMEOUT_SEC + 5)) node "$TEST_SCRIPT"; then
    STATUS="VERIFIED"
else
    EXIT_CODE=$?
    if [ "$EXIT_CODE" -eq 124 ]; then
        echo "FAIL: Test hung and was terminated after ${TEST_TIMEOUT_SEC}s timeout"
    fi
    STATUS="FAILED"
fi
rm -f "$TEST_SCRIPT"
```

If the test process hangs beyond the timeout, the `timeout` command sends SIGTERM, the AC is marked `FAILED`, and the evidence records: "Test hung and was terminated after ${TEST_TIMEOUT_SEC}s".

**7. Screenshot capture on failure**

When any assertion or action fails:
1. Capture a full-page screenshot using `page.screenshot({ path: ..., fullPage: true })`.
2. Save to `${ARTIFACT_DIR}/screenshot-<timestamp>-ac-<AC_ID>.png`.
3. Record the screenshot path in the test result evidence.

When a test passes, screenshots are optional and only captured if `--capture-success` is passed.

**8. Record results**

For each SPA test, record:
- AC ID and text (truncated)
- Playwright actions executed
- Assertions performed
- Pass/fail status
- Screenshot path (on failure)
- Execution time
- Error message (on failure)

If any assertion fails, mark the AC as `FAILED` immediately. Do not retry.

**Edge cases — error handling**:
- **Playwright not installed**: Report clear error with `npm install -D @playwright/test` and `npx playwright install chromium` suggestion. Mark all SPA ACs as `MANUAL CHECK REQUIRED`. Continue with other test categories.
- **Dev server not running**: If `page.goto()` throws `net::ERR_CONNECTION_REFUSED` or similar, report: "Dev server not reachable at ${DEV_SERVER_URL}. Ensure the server is running before verification." Mark affected ACs as `FAILED`.
- **Browser launch failure**: If Chromium fails to launch (e.g., missing system dependencies), report the error and suggest `npx playwright install-deps chromium`. Mark affected ACs as `MANUAL CHECK REQUIRED`.

#### Desktop Tests (Computer-use / MCP)

**Prerequisite check**: Before generating any desktop tests, verify that computer-use or MCP-based GUI automation tools are available. This skill does NOT auto-install these tools.

```bash
GUI_TOOLS_AVAILABLE=false
GUI_TOOL_NAME=""

if [ -n "$CLAUDE_COMPUTER_USE_AVAILABLE" ] || command -v computer-use >/dev/null 2>&1; then
    GUI_TOOLS_AVAILABLE=true
    GUI_TOOL_NAME="computer-use"
fi

if [ -n "$MCP_GUI_SERVER_URL" ] || command -v mcp-gui >/dev/null 2>&1; then
    GUI_TOOLS_AVAILABLE=true
    GUI_TOOL_NAME="mcp-gui"
fi

if [ "$GUI_TOOLS_AVAILABLE" != "true" ]; then
    echo "ERROR: Desktop testing tools are not available."
    echo "This skill requires computer-use or MCP GUI automation tools to verify desktop applications."
    echo ""
    echo "To enable desktop verification:"
    echo "  - Run in an environment with computer-use support, OR"
    echo "  - Install and configure an MCP GUI automation server"
    echo ""
    echo "Aborting desktop verification. No tests will be executed."
    exit 1
fi
echo "Desktop GUI tool detected: $GUI_TOOL_NAME"
```

**1. Prepare artifact directory**

```bash
ARTIFACT_DIR="${SPEC_FOLDER}/e2e-artifacts"
mkdir -p "$ARTIFACT_DIR"
```

**2. Parse `[IMP]` AC for desktop behavior hints**

For each `[IMP]` acceptance criterion in the specification that relates to Desktop App behavior:
- Extract **window title** hints: look for phrases like "window opens", "dialog appears", "modal shows", "title contains", "screen shows".
- Extract **UI element** descriptions: look for button labels, input placeholders, menu items, checkbox labels, toggle names.
- Extract **workflow steps**: look for action sequences like "click ... then ...", "select ... and press ...", "toggle ...".
- Extract **expected state changes**: look for visual changes like "theme changes to dark", "status indicator turns green", "list updates".

If an `[IMP]` AC does **not** contain parseable desktop behavior hints (no window, element, or workflow descriptions), mark it `MANUAL CHECK REQUIRED` and skip to the next criterion.

**3. Verify the application is running**

If the desktop app was not started in Phase 3 or its process has exited, re-launch using the commands from Phase 3:
```bash
if [ -n "$STARTUP_PID" ] && ! kill -0 "$STARTUP_PID" 2>/dev/null; then
    echo "Desktop app process is not running. Re-launching..."
    # Re-run the appropriate launch command from Phase 3 based on DESKTOP_FRAMEWORK
fi
```

**4. Verify window/UI elements via visual or accessibility-tree inspection**

For each AC describing a window or UI element (AC-022):

- **Visual inspection** (computer-use):
  - Capture a screenshot of the desktop.
  - Analyze the image for the expected window title, button label, or visual element.
  - Example: "Settings window opens" → capture screenshot, verify a window titled "Settings" is visible.

- **Accessibility-tree inspection** (MCP GUI automation):
  - Query the accessibility tree for elements matching the expected name, role, or state.
  - Example: "Settings window opens" → query for a window element with name containing "Settings".
  - Example: "Toggle dark mode" → query for a switch/checkbox element with label containing "Dark mode".

**5. Simulate user workflows through GUI automation**

For each AC describing a user workflow (AC-023), translate the description into GUI automation actions:

| AC Description Pattern | GUI Automation Action |
|------------------------|----------------------|
| "click [button label]" | Click the UI element with the matching accessible name or label |
| "fill [field] with [value]" | Focus the input field and type the value |
| "toggle [switch/checkbox]" | Click the toggle or checkbox element |
| "select [option] from [dropdown]" | Open the dropdown and click the option element |
| "navigate to [menu item]" | Click the menu item with the matching label |
| "type [value] into [field]" | Focus the field and type the value |

**6. Screenshot capture at each verification step**

At EVERY step (before actions, after actions, and on assertions), capture a screenshot:

```bash
SCREENSHOT_PATH="${ARTIFACT_DIR}/screenshot-$(date +%s)-ac-${AC_ID}-step-${STEP_NUM}.png"
# computer-use: capture screenshot and save to SCREENSHOT_PATH
# MCP: use the GUI automation server's screenshot capability
```

Screenshots are saved for every step regardless of pass/fail status, satisfying AC-024 (SEF).

**7. Per-test timeout enforcement**

Each desktop test MUST enforce a per-test timeout to prevent indefinite hangs (REQ-NR007):

```bash
TEST_TIMEOUT_SEC=60
TEST_START_TIME=$(date +%s)
TEST_STATUS="RUNNING"

while [ "$TEST_STATUS" = "RUNNING" ]; do
    if [ $(( $(date +%s) - TEST_START_TIME )) -gt "$TEST_TIMEOUT_SEC" ]; then
        echo "FAIL: Desktop test hung and was terminated after ${TEST_TIMEOUT_SEC}s timeout"
        STATUS="FAILED"
        TEST_STATUS="TIMEOUT"
        FINAL_SCREENSHOT="${ARTIFACT_DIR}/screenshot-$(date +%s)-ac-${AC_ID}-timeout.png"
        # capture screenshot to FINAL_SCREENSHOT
        break
    fi
    # Execute next workflow step; if all steps complete, set TEST_STATUS="COMPLETED"
done
```

If a test times out:
- Mark the AC as `FAILED`
- Capture a final timeout screenshot
- Record evidence: "Test hung and was terminated after ${TEST_TIMEOUT_SEC}s timeout"
- Attempt to reset application state (close and reopen the window) before the next AC

**8. Record results**

For each desktop test, record:
- AC ID and text (truncated)
- GUI automation actions executed (step list)
- Screenshots captured (list of paths with step descriptions)
- Pass/fail status
- Error message, timeout reason, or assertion mismatch (on failure)

If any assertion or action fails, mark the AC as `FAILED` immediately. Do not retry.

**Edge cases — error handling**:
- **No computer-use or MCP tools available**: Abort verification with a clear error message. Do NOT silently skip desktop tests.
- **Build failure**: Build output is captured in `$STARTUP_LOGS_FILE` and reported. Verification aborts before launch.
- **App crash during test**: If the desktop process exits during testing, capture any crash output from logs, mark the current AC as `FAILED`, and attempt to restart the app for the next AC.
- **Window/element not found**: If the expected window or element does not appear within the test timeout, mark the AC as `FAILED` and capture a screenshot of the current desktop state.

**Fallback**: If a specific AC cannot be translated into an automated test (e.g., it requires human aesthetic judgment), mark it as `MANUAL CHECK REQUIRED` and continue.

### Phase 5: Map Results to Acceptance Criteria

**Goal**: Compare every test execution result against the `[IMP]` acceptance criteria from the functional specification and produce a deterministic verdict for each.

#### 5.1 Initialize the Results Table

Create an associative results structure (e.g., shell associative array, JSON object, or temporary file) keyed by AC ID. For every `[IMP]` acceptance criterion extracted in Phase 1, pre-populate a row with:

| Field | Initial Value |
|-------|---------------|
| `ac_id` | The AC identifier (e.g., `AC-012`) |
| `ac_text` | The full criterion text, truncated to 120 characters for display |
| `status` | `PENDING` (updated in 5.2) |
| `evidence` | Empty string (updated in 5.2) |
| `actual` | Empty string (populated only on mismatch) |
| `expected` | Empty string (populated only on mismatch) |

Iterate over the specification’s acceptance criteria table and include **only** rows whose taxonomy tag is `[IMP]`. `[SEF]` and `[EXT]` criteria are excluded from runtime verification; they may be listed in an appendix but do not require a status verdict.

#### 5.2 Apply Verdict Rules

For each AC that was targeted by a test in Phase 4, apply the following rules **in order**:

1. **VERIFIED** (REQ-016):
   - IF the test completed without assertion failures, timeouts, or tool errors
   - THEN set `status = "VERIFIED"`
   - Set `evidence` to a concise description:
     - REST API: ``curl returned HTTP <code> in <N>ms``
     - Web SPA: ``Playwright assertion passed: <selector> <condition>``
     - Desktop: ``GUI automation confirmed: <window/element> present``

2. **FAILED** (REQ-018):
   - IF any assertion failed, the test timed out, the tool crashed, or the dev server was unreachable
   - THEN set `status = "FAILED"`
   - Set `actual` to the observed value (e.g., `HTTP 400`, `element not found`, `timeout after 30s`)
   - Set `expected` to the value demanded by the AC (e.g., `HTTP 201`, `element visible`)
   - Set `evidence` to a human-readable sentence combining `actual` vs `expected`, plus the path to any captured artifact (screenshot, response dump) if available.

3. **MANUAL CHECK REQUIRED** (REQ-017):
   - IF no test was generated for the AC because:
     - The AC text lacked parseable endpoint / UI / desktop behavior hints
     - A required tool was missing (e.g., Playwright not installed)
     - The AC describes human judgment (e.g., "UI looks correct")
   - THEN set `status = "MANUAL CHECK REQUIRED"`
   - Set `evidence` to the reason: ``No automated test could be derived: <reason>``

**IMPORTANT**: Every `[IMP]` AC MUST have a final status of `VERIFIED`, `FAILED`, or `MANUAL CHECK REQUIRED`. No AC may remain in `PENDING` when Phase 5 ends.

#### 5.3 Compute Summary Counts

After all rows are populated, compute:

```bash
TOTAL_IMP=$(count_implementation_acs)
VERIFIED_COUNT=$(grep -c '"status":"VERIFIED"' "$RESULTS_FILE")
FAILED_COUNT=$(grep -c '"status":"FAILED"' "$RESULTS_FILE")
MANUAL_COUNT=$(grep -c '"status":"MANUAL CHECK REQUIRED"' "$RESULTS_FILE")
```

Store these counts; they are required in the report Summary section (REQ-020).

### Phase 6: Generate Report

**Goal**: Produce a deterministic, human-readable markdown report that follows the format defined in Phase 6.3 and contains no secrets.

#### 6.1 Prepare Report Paths and Directories

```bash
REPORT_TIMESTAMP=$(date +%Y-%m-%d-%H%M%S)
REPORT_DIR="${SPEC_FOLDER}"
ARTIFACT_DIR="${REPORT_DIR}/e2e-artifacts"
REPORT_FILE="${REPORT_DIR}/e2e-report-${REPORT_TIMESTAMP}.md"

mkdir -p "$ARTIFACT_DIR"
```

- `SPEC_FOLDER` is the value of the `--spec` argument (e.g., `docs/specs/001-real-e2e-verification/`).
- The report filename MUST use the exact pattern `e2e-report-YYYY-MM-DD-HHMMSS.md` (AC-026).
- The artifact directory MUST exist before any artifact paths are written into the report.

#### 6.2 Redact Secrets from Raw Output

Before writing any command output into the report, run the raw logs through a redaction pass (REQ-NR002):

```bash
# Redact Authorization header values
sed -E 's/(Authorization:[[:space:]]*[Bb]earer[[:space:]]+)[^[:space:]]+/\1***REDACTED***/g' "$STARTUP_LOGS_FILE" > "$STARTUP_LOGS_FILE.redacted"

# Redact tokens in JSON bodies
sed -E 's/("token"[[:space:]]*:[[:space:]]*")[^"]+/\1***REDACTED***/g' "$STARTUP_LOGS_FILE.redacted" > "$STARTUP_LOGS_FILE.redacted2"

# Redact passwords in curl -u arguments
sed -E 's/(-u[[:space:]]+[^:]*:)[^[:space:]]+/\1***REDACTED***/g' "$STARTUP_LOGS_FILE.redacted2" > "$STARTUP_LOGS_FILE.redacted3"

# Redact E2E_* environment variables (REQ-NR002)
sed -E 's/(E2E_[A-Z_]+=)[^[:space:]]+/\1***REDACTED***/g' "$STARTUP_LOGS_FILE.redacted3" > "$STARTUP_LOGS_FILE.redacted_final"
```

Only the redacted version (`$STARTUP_LOGS_FILE.redacted_final`) is included in the report. The original temp file is discarded.

#### 6.3 Write Report Sections

Generate the report by appending each section in the exact order below. All paths inside the report MUST be relative to the report file location.

**Section 1 — Summary**

```markdown
## Summary

| Metric | Count |
|--------|-------|
| Total AC Evaluated | ${TOTAL_IMP} |
| ✅ VERIFIED | ${VERIFIED_COUNT} |
| ❌ FAILED | ${FAILED_COUNT} |
| ⚠️ MANUAL CHECK REQUIRED | ${MANUAL_COUNT} |
```

**Section 2 — Environment**

```markdown
## Environment

| Property | Value |
|----------|-------|
| Application Type | ${APP_TYPE} |
| Startup Command | \`${STARTUP_COMMAND}\` |
| Target Port | ${TARGET_PORT} |
| Health Endpoint | ${HEALTH_CHECK_METHOD} |
| Runtime Version | ${RUNTIME_VERSION} |
| Verification Started | ${ISO8601_START_TIME} |
```

- `RUNTIME_VERSION`: capture the runtime version detected during startup:
  - Docker: `docker --version`
  - Node.js: `node --version`
  - Java: `java -version 2>&1 | head -1`
  - Python: `python --version` or `python3 --version`
- `ISO8601_START_TIME`: the timestamp when Phase 3 began, in ISO-8601 format.

**Section 3 — Test Results**

```markdown
## Test Results

| AC ID | Criterion (truncated) | Status | Evidence |
|-------|----------------------|--------|----------|
| AC-012 | WHEN the app is classified... | VERIFIED | \`curl\` returned 200 |
| AC-013 | WHEN a curl test executes... | FAILED | Expected 201, got 400 |
| AC-014 | WHEN authentication is required... | MANUAL CHECK REQUIRED | No credentials found |
```

- The "Criterion (truncated)" column MUST be truncated to 120 characters, appended with `...` if longer.
- The "Status" column MUST be one of `VERIFIED`, `FAILED`, or `MANUAL CHECK REQUIRED`.
- The "Evidence" column MUST reference artifacts using relative paths when applicable (e.g., `./e2e-artifacts/ac-019-screenshot.png`).

**Section 4 — Raw Output**

```markdown
## Raw Output

### Startup Logs
\`\`\`
[contents of $STARTUP_LOGS_FILE.redacted_final]
\`\`\`

### Test Commands
\`\`\`
[For each test: the exact command executed (auth redacted) and its first 2000 chars of stdout/stderr]
\`\`\`
```

- If a test produced no output, write `(no output)`.
- Limit each code block to 2000 lines to avoid overwhelming the report; if logs are larger, append a note: ``(truncated; full logs available in <path>)``.

**Section 5 — Artifacts**

```markdown
## Artifacts

| AC ID | Type | Path |
|-------|------|------|
| AC-019 | Screenshot | ./e2e-artifacts/screenshot-1717189200-ac-019.png |
| AC-014 | Response Dump | ./e2e-artifacts/ac-014-response.json |
```

- List every artifact file present in `$ARTIFACT_DIR`.
- If no artifacts were generated, write ``No artifacts captured for this run.``

**Section 6 — Teardown Status**

```markdown
## Teardown Status

| Property | Value |
|----------|-------|
| Teardown Executed | ${TEARDOWN_EXECUTED} |
| Port Released | ${PORT_RELEASED} |
| Remaining Processes | ${REMAINING_PROCESSES} |
```

- `TEARDOWN_EXECUTED`: `true` / `false` / `skipped (--keep-alive)`
- `PORT_RELEASED`: `true` / `false` / `unknown`
- `REMAINING_PROCESSES`: A comma-separated list of PIDs or container names still active after teardown, or `none`.

#### 6.4 Finalize and Persist Report

```bash
cat > "$REPORT_FILE" << 'REPORT_EOF'
[all sections assembled above]
REPORT_EOF

echo "E2E report saved to: $REPORT_FILE"
```

- The report MUST be valid Markdown (passes basic `markdownlint` rules): proper heading levels, no trailing spaces, consistent pipe table delimiters.
- The report MUST NOT be modified after it is written (REQ-NR005).
- Set a variable `REPORT_PATH="$REPORT_FILE"` for use in Phase 8.

### Phase 7: Teardown Environment

**Goal**: Gracefully stop all runtime resources started in Phase 3, verify that ports and processes are fully released, and record the outcome. If `--keep-alive` is passed, skip teardown entirely and warn the user.

#### 7.1 `--keep-alive` Guard

```bash
if [ "$KEEP_ALIVE" = "true" ]; then
    TEARDOWN_EXECUTED="skipped (--keep-alive)"
    PORT_RELEASED="skipped"
    REMAINING_PROCESSES="skipped"
    echo "WARNING: --keep-alive was passed. The runtime environment is still running."
    echo "You are responsible for cleaning up:"
    if [ "$APP_TYPE" = "Docker-managed" ]; then
        echo "  docker compose -f '${PROJECT_ROOT}/docker-compose.yml' down"
    else
        echo "  kill $(lsof -ti:${TARGET_PORT})"
    fi
    echo "Report was saved before teardown; artifacts are in ${ARTIFACT_DIR}."
    # Skip remaining teardown steps and proceed to Phase 8
    # (Phase 7 cleanup is bypassed when --keep-alive is active)
fi
```

#### 7.2 Graceful Teardown by Application Type

**Docker-managed** (AC-029):

```bash
TEARDOWN_EXECUTED="true"
DOCKER_TEARDOWN_FAILED=false

if [ "$APP_TYPE" = "Docker-managed" ]; then
    cd "$PROJECT_ROOT"
    if docker compose down >> "$STARTUP_LOGS_FILE" 2>&1; then
        echo "Docker Compose stack stopped successfully."
    else
        echo "WARNING: docker compose down exited with a non-zero code."
        DOCKER_TEARDOWN_FAILED=true
    fi
fi
```

**Local processes (JVM, Node.js/NestJS, Python, Desktop)** (AC-029):

```bash
if [ -n "$STARTUP_PID" ] && kill -0 "$STARTUP_PID" 2>/dev/null; then
    echo "Sending SIGTERM to process $STARTUP_PID ..."
    kill -TERM "$STARTUP_PID" 2>/dev/null || true
    # Wait up to 10 seconds for graceful exit
    GRACEFUL_WAIT=0
    while [ "$GRACEFUL_WAIT" -lt 10 ] && kill -0 "$STARTUP_PID" 2>/dev/null; do
        sleep 1
        GRACEFUL_WAIT=$((GRACEFUL_WAIT + 1))
    done
    # If still alive, send SIGKILL
    if kill -0 "$STARTUP_PID" 2>/dev/null; then
        echo "Process $STARTUP_PID did not exit after 10s; sending SIGKILL."
        kill -KILL "$STARTUP_PID" 2>/dev/null || true
        sleep 2
    fi
fi

# Also terminate any child processes that may still hold the port
PORT_PIDS=$(lsof -ti:"$TARGET_PORT" 2>/dev/null || true)
if [ -n "$PORT_PIDS" ]; then
    echo "Additional PIDs holding port $TARGET_PORT: $PORT_PIDS"
    for pid in $PORT_PIDS; do
        kill -TERM "$pid" 2>/dev/null || true
    done
    sleep 3
    for pid in $PORT_PIDS; do
        if kill -0 "$pid" 2>/dev/null; then
            kill -KILL "$pid" 2>/dev/null || true
        fi
    done
fi
```

**Emergency cleanup — orphan processes from a crashed test**:

```bash
# If the original STARTUP_PID is empty or already dead, but the port is still occupied,
# this indicates an orphan process from a crash or a detached child.
if [ -z "$STARTUP_PID" ] || ! kill -0 "$STARTUP_PID" 2>/dev/null; then
    ORPHAN_PIDS=$(lsof -ti:"$TARGET_PORT" 2>/dev/null || true)
    if [ -n "$ORPHAN_PIDS" ]; then
        echo "WARNING: Orphan process(es) detected on port $TARGET_PORT: $ORPHAN_PIDS"
        for pid in $ORPHAN_PIDS; do
            kill -TERM "$pid" 2>/dev/null || true
        done
        sleep 3
        for pid in $ORPHAN_PIDS; do
            if kill -0 "$pid" 2>/dev/null; then
                kill -KILL "$pid" 2>/dev/null || true
            fi
        done
    fi
fi
```

#### 7.3 Verify Port Release (AC-030)

```bash
PORT_RELEASED="false"
PORT_CHECK_WAIT=0
MAX_PORT_CHECK_WAIT=15

while [ "$PORT_CHECK_WAIT" -lt "$MAX_PORT_CHECK_WAIT" ]; do
    if ! lsof -i :"$TARGET_PORT" >/dev/null 2>&1 && ! nc -z localhost "$TARGET_PORT" 2>/dev/null; then
        PORT_RELEASED="true"
        echo "Port $TARGET_PORT is free."
        break
    fi
    sleep 1
    PORT_CHECK_WAIT=$((PORT_CHECK_WAIT + 1))
done

if [ "$PORT_RELEASED" != "true" ]; then
    echo "WARNING: Port $TARGET_PORT is still occupied after teardown."
fi
```

#### 7.4 Identify Remaining Resources (REQ-023)

```bash
REMAINING_PROCESSES="none"

if [ "$APP_TYPE" = "Docker-managed" ]; then
    REMAINING_CONTAINERS=$(docker compose ps --format '{{.Name}}' 2>/dev/null | tr '\n' ',' | sed 's/,$//')
    if [ -n "$REMAINING_CONTAINERS" ]; then
        REMAINING_PROCESSES="containers: $REMAINING_CONTAINERS"
    fi
else
    REMAINING_PIDS=$(lsof -ti:"$TARGET_PORT" 2>/dev/null | tr '\n' ' ' | sed 's/ $//')
    if [ -n "$REMAINING_PIDS" ]; then
        REMAINING_PROCESSES="PIDs: $REMAINING_PIDS"
    fi
fi
```

#### 7.5 Warn User on Incomplete Teardown

```bash
if [ "$PORT_RELEASED" != "true" ] || [ "$DOCKER_TEARDOWN_FAILED" = "true" ]; then
    echo "WARNING: Teardown did not complete cleanly. Manual cleanup may be required."
    if [ "$APP_TYPE" = "Docker-managed" ]; then
        echo "  Remaining containers: ${REMAINING_PROCESSES}"
        echo "  Manual command: docker compose -f '${PROJECT_ROOT}/docker-compose.yml' down"
    else
        echo "  Remaining PIDs on port ${TARGET_PORT}: ${REMAINING_PIDS}"
        echo "  Manual command: kill ${REMAINING_PIDS}"
    fi
fi
```

#### 7.6 Record Teardown Status

Update the report file in-place (append the Teardown Status section if it was not written in Phase 6, or ensure the variables are correctly set before Phase 6 finalizes). The preferred order is:

1. Phase 6 writes the report with placeholder teardown variables.
2. Phase 7 executes teardown.
3. Phase 7 updates the placeholders with actual values using an in-place edit (e.g., `sed`):

```bash
sed -i.bak \
    -e "s/\${TEARDOWN_EXECUTED}/${TEARDOWN_EXECUTED}/g" \
    -e "s/\${PORT_RELEASED}/${PORT_RELEASED}/g" \
    -e "s/\${REMAINING_PROCESSES}/${REMAINING_PROCESSES}/g" \
    "$REPORT_FILE" && rm -f "$REPORT_FILE.bak"
```

If the report was already finalized before teardown (a valid alternative), append a **Post-Teardown Update** section at the end of the report:

```markdown
## Post-Teardown Update

| Property | Value |
|----------|-------|
| Teardown Executed | ${TEARDOWN_EXECUTED} |
| Port Released | ${PORT_RELEASED} |
| Remaining Processes | ${REMAINING_PROCESSES} |
```

**IMPORTANT**: Do NOT delete the report or modify any spec/task files during teardown (REQ-NR005).

### Phase 8: Present Results

1. Print a concise summary to the user:
   - ✅ VERIFIED: N | ❌ FAILED: N | ⚠️ MANUAL: N
   - Report path
   - Teardown status (or `--keep-alive` notice)
2. If any AC failed:
   - Highlight the failed AC and evidence
   - Recommend running `/developer-kit-specs:specs.task-implementation` again for the failing task
3. Mark all todos complete.

## Examples

### Spring Boot REST API Verification

```bash
/developer-kit-specs:specs.e2e-verify --spec=docs/specs/001-user-auth/
```

Actions:
1. Detect `pom.xml` + `docker-compose.yml` → Docker-managed Spring Boot
2. Run `docker compose up -d`
3. Wait for `localhost:8080/actuator/health`
4. Read AC from spec; find `[IMP]` AC describing login endpoint
5. Execute: `curl -s -w "\n%{http_code}" -X POST http://localhost:8080/api/login -d '{"email":"test@example.com","password":"secret"}'`
6. Assert status `200` and response contains `token`
7. Generate report: `docs/specs/001-user-auth/e2e-report-2026-05-31-143022.md`
8. Run `docker compose down`

### React SPA Verification

```bash
/developer-kit-specs:specs.e2e-verify --spec=docs/specs/002-dashboard/
```

Actions:
1. Detect `package.json` with `react` dependency
2. Run `npm run dev`; wait for `localhost:5173`
3. Launch Playwright, navigate to `/dashboard`
4. AC says "User can click 'Refresh' to reload data" → `page.click('[data-testid=refresh]')`, assert table rows update
5. Screenshot on success; capture on failure
6. Generate report with screenshot artifacts
7. Kill dev server process

### Desktop App Verification

```bash
/developer-kit-specs:specs.e2e-verify --spec=docs/specs/003-settings-app/
```

Actions:
1. Detect `src-tauri/Cargo.toml` → Tauri desktop app
2. Run `cargo tauri build --debug` then launch the `.app`/`.exe`
3. Use computer-use to verify Settings window opens
4. AC says "User can toggle dark mode" → click toggle, capture screenshot, verify theme change
5. Generate report with step screenshots
6. Close app and verify process terminated

## Command Whitelist

Only commands documented in `references/test-execution-patterns.md` may be executed automatically. The whitelist covers:

| Category | Allowed Commands |
|----------|-----------------|
| Docker | `docker compose up -d --build`, `docker compose down`, `docker compose ps`, `docker compose logs` |
| JVM / Spring Boot | `./mvnw spring-boot:run`, `./gradlew bootRun` |
| Node.js / NestJS | `npm run dev`, `npm run start:dev`, `npm start`, `node server.js` |
| Python | `uvicorn main:app --reload`, `python manage.py runserver`, `flask run` |
| Desktop (Tauri) | `cargo tauri build --debug`, `cargo tauri dev`, `open *.app`, direct binary execution |
| Desktop (Electron) | `npm run electron:dev`, `npx electron .` |
| Testing | `curl` (without `-k`/`--insecure` unless `--insecure` passed), `npx playwright`, `node` (for inline Playwright scripts) |
| Teardown | `docker compose down`, `kill -TERM`, `kill -KILL` (for stuck processes only), `lsof`, `nc` |

**Non-whitelisted command policy**: IF a derived command is NOT in the whitelist → use `AskUserQuestion` to request explicit user confirmation before execution. The user MUST approve the command; otherwise, abort.

## Security Guards and Negative Requirements

The following negative requirements (REQ-NR001 through REQ-NR008) are enforced at multiple points in the skill workflow:

### REQ-NR001: No Destructive Commands

The system SHALL NOT run `sudo`, `rm -rf`, `docker system prune`, `mkfs`, `dd`, or any other destructive system command during startup, test, or teardown.

**Enforcement**:
- Phase 1.5 scans all commands for forbidden patterns before execution.
- Phase 3 data integrity pre-flight rejects commands that would destroy data.
- Teardown commands are restricted to `docker compose down` and graceful process termination (`kill -TERM` / `kill -KILL` for stuck orphans only).

### REQ-NR002: No Secrets in Report

The system SHALL NOT expose secrets, API keys, or passwords in the E2E report.

**Enforcement**:
- Phase 6 redaction pass removes:
  - `Authorization: Bearer <token>` → `Authorization: Bearer ***REDACTED***`
  - `E2E_AUTH_TOKEN=...`, `E2E_USERNAME=...`, `E2E_PASSWORD=...` → `E2E_xxx=***REDACTED***`
  - `"token": "..."` → `"token": "***REDACTED***"`
  - Passwords in `curl -u user:password` → `curl -u user:***REDACTED***`
- Only the redacted version of logs is written to the report.
- The original unredacted temp file is discarded immediately after redaction.

### REQ-NR003: No TLS Bypass by Default

The system SHALL NOT disable TLS certificate verification (`-k` / `--insecure`) in curl by default.

**Enforcement**:
- Phase 1.5 rejects curl commands containing `-k` or `--insecure` unless the `--insecure` flag was explicitly passed.
- Phase 4 curl command generation rules explicitly forbid adding `-k` / `--insecure`.
- IF `--insecure` is passed → a warning is logged: "TLS certificate verification is disabled. Use only for local development."

### REQ-NR004: No Data Overwrite on Startup

The system SHALL NOT overwrite or delete existing databases, volumes, or local data unless the startup command itself does so.

**Enforcement**:
- Phase 1.5 data integrity pre-check rejects commands containing `rm`, `--volumes`, `prune`, `drop`, or similar destructive data patterns.
- Phase 3 data integrity pre-flight aborts startup if the command would destroy existing data.

### REQ-NR005: No Spec or Task File Modification

The system SHALL NOT modify the functional specification or task files during report generation or teardown.

**Enforcement**:
- Phase 6 writes the report as a new file (`e2e-report-YYYY-MM-DD-HHMMSS.md`) only.
- Phase 7 teardown appends only a Post-Teardown Update section to the report; it never modifies spec or task files.
- The skill is read-only regarding source code, specs, and tasks.

### REQ-NR006: No Orphan Processes on Failure

The system SHALL NOT leave orphan processes or containers running when startup fails.

**Enforcement**:
- Phase 3 Docker startup: on timeout, `docker compose down` is executed before exiting.
- Phase 3 Spring Boot / Node.js startup: on timeout, `kill -TERM $STARTUP_PID` is executed before exiting.
- Phase 7 teardown includes emergency orphan cleanup for processes still holding the target port.

### REQ-NR007: Per-Test Timeout Enforcement

The system SHALL NOT block indefinitely on a hanging test.

**Enforcement**:
- Phase 4 Playwright tests: wrapped with `timeout --signal=TERM <N>`; if timeout occurs, the AC is marked `FAILED`.
- Phase 4 Desktop tests: a manual polling loop checks elapsed time against `TEST_TIMEOUT_SEC`; if exceeded, the AC is marked `FAILED`.
- If a test hangs, it is terminated and marked `FAILED`, never `VERIFIED` or `PENDING`.

### REQ-NR008: No Retry on Failed curl Tests

The system SHALL NOT retry failed curl requests.

**Enforcement**:
- Phase 4 curl execution: each command is executed exactly once.
- NO `--retry` flag, NO retry loops, NO fallback re-execution.
- The first result is recorded immediately; if it fails, the AC is marked `FAILED`.

## Constraints and Warnings

- **Read-only on source**: This skill never edits application source code, test files, configuration, functional specifications, or task files.
- **No auto-install**: If Playwright or Docker is missing, the skill reports the gap and suggests install commands. It does NOT run `npm install -g` or `brew install` automatically.
- **Local only**: Tests run against `localhost`. Remote URLs, staging, or production endpoints are out of scope.
- **Destructive guard**: Startup, test, and teardown commands are whitelisted per `references/test-execution-patterns.md`. Any command outside the whitelist requires user confirmation via `AskUserQuestion`.
- **Secret hygiene**: Authorization headers, bearer tokens, `E2E_*` environment variables, and passwords are redacted from the report. Only header names and redacted values appear.
- **TLS default**: curl commands use strict TLS verification by default. Pass `--insecure` only for local development with self-signed certificates.
- **Cleanup responsibility**: If `--keep-alive` is passed, the user is responsible for manual teardown.
- **No persistent test suite**: The skill generates ad-hoc tests for verification. It does not create permanent test files in the project.
