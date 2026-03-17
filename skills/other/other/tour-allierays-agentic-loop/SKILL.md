---
description: Take an interactive tour of agentic-loop - the system for going from idea to shipped code with AI.
---

# Vibe & Thrive Tour

## Step 1: Check & Fix Setup

Print this exactly:

```
  ╦  ╦╦╔╗ ╔═╗   ┬   ╔╦╗╦ ╦╦═╗╦╦  ╦╔═╗
  ╚╗╔╝║╠╩╗║╣   ┌┼─   ║ ╠═╣╠╦╝║╚╗╔╝║╣
   ╚╝ ╩╚═╝╚═╝  └┘    ╩ ╩ ╩╩╚═╩ ╚╝ ╚═╝

  Checking setup...
```

**Check each item and FIX if missing:**

1. **Check jq installed:**
   ```bash
   command -v jq
   ```
   - If missing: Say "⚠️ jq not found. Install it: `brew install jq` (macOS) or `apt install jq` (Linux)"
   - If found: ✓ jq installed

2. **Check slash commands (skills):**
   ```bash
   test -d .claude/skills && ls -d .claude/skills/*/ 2>/dev/null | wc -l
   ```
   - If missing or count is 0: Copy from node_modules:
     ```bash
     mkdir -p .claude/skills && cp -r node_modules/agentic-loop/.claude/skills/* .claude/skills/
     ```
   - Then: ✓ Slash commands installed

3. **Check Ralph initialized:**
   ```bash
   test -f .ralph/config.json
   ```
   - If missing: Run `npx ralph init`
   - Then: ✓ Ralph initialized

4. **Check CLAUDE.md:**
   ```bash
   test -f CLAUDE.md
   ```
   - If missing: Create a basic one:
     ```bash
     echo "# Project Guide for Claude" > CLAUDE.md
     ```
   - Then: ✓ CLAUDE.md created

5. **Check Claude Code hooks:**
   ```bash
   test -f .claude/settings.json && jq -e '.hooks' .claude/settings.json > /dev/null 2>&1
   ```
   - If missing: Install hooks:
     ```bash
     npx ralph hooks
     ```
   - Then: ✓ Claude Code hooks installed

6. **Check Docker:**
   ```bash
   test -f docker-compose.yml || test -f docker-compose.yaml || test -f compose.yml
   ```
   - If found:
     - Update config: `jq '.docker.enabled = true' .ralph/config.json > .ralph/config.tmp && mv .ralph/config.tmp .ralph/config.json`
     - Say: "✓ Docker detected - Ralph will run commands inside containers"
     - **Skip Playwright check** (browser verification uses curl in Docker mode)

7. **Check & Install Playwright (if not Docker):**

   Check BOTH the npm package AND browser binaries:
   ```bash
   # Check npm package
   npm list playwright 2>/dev/null

   # Check browser binaries exist (macOS or Linux path)
   ls ~/Library/Caches/ms-playwright/chromium-* 2>/dev/null || ls ~/.cache/ms-playwright/chromium-* 2>/dev/null
   ```

   - If BOTH exist: Say "✓ Playwright available"
   - If either is missing:
     Say: "Installing Playwright for browser verification (~150MB)..."
     ```bash
     npm install playwright && npx playwright install chromium
     ```
     - If successful: Say "✓ Playwright installed"
     - If failed: Say "⚠️ Playwright installation failed. Browser verification will use basic HTTP checks. You can try manually: `npm install playwright && npx playwright install chromium`"

Say: "Setup verified! Let me configure Ralph for your project..."

---

## Step 2: Auto-Configure Ralph

**Auto-detect and configure project settings:**

### 2a. Detect Project Structure

Check these directories and set `paths` in config:

```bash
# Check what exists
test -d frontend && echo "frontend exists"
test -d client && echo "client exists"
test -d backend && echo "backend exists"
test -d core && echo "core exists"
test -d src && echo "src exists"
```

Based on results, update config:
- `frontend/` exists → set `paths.frontend` to `"frontend"`
- `client/` exists → set `paths.frontend` to `"client"`
- `backend/` exists → set `paths.backend` to `"backend"`
- `core/` exists → set `paths.backend` to `"core"`
- Only `src/` exists → set `paths.frontend` to `"."`

### 2b. Detect URLs

Check `.env`, `.env.example`, or `docker-compose.yml` for port numbers:

```bash
grep -h "PORT\|URL\|localhost" .env .env.example docker-compose.yml 2>/dev/null | head -5
```

Also check `package.json` for port in dev script:
```bash
cat package.json 2>/dev/null | jq -r '.scripts.dev // empty'
```

Set URLs based on findings (defaults: frontend=3000, backend=8000):
```bash
jq '.urls.frontend = "http://localhost:3000" | .urls.backend = "http://localhost:8000"' .ralph/config.json > .ralph/config.tmp && mv .ralph/config.tmp .ralph/config.json
```

### 2c. Detect Commands

Read package.json scripts and update config:

```bash
# Get scripts from package.json (check root and frontend/)
cat package.json 2>/dev/null | jq -r '.scripts | to_entries[] | "\(.key): \(.value)"' | head -10
```

Update config with detected commands:
```bash
# Example: if package.json has "dev": "next dev"
jq '.commands.dev = "npm run dev"' .ralph/config.json > .ralph/config.tmp && mv .ralph/config.tmp .ralph/config.json
```

For fullstack projects with separate frontend:
```bash
jq '.commands.dev = "cd frontend && npm run dev"' .ralph/config.json > .ralph/config.tmp && mv .ralph/config.tmp .ralph/config.json
```

### 2d. Detect Test Directory and Patterns

Check for test directories and files:

```bash
# Check common test directories
for dir in tests test __tests__ spec src/__tests__; do
  test -d "$dir" && echo "Found test directory: $dir"
done

# Check for test files (colocated pattern)
find . -type f \( -name "*.test.ts" -o -name "*.spec.ts" -o -name "*_test.py" -o -name "test_*.py" -o -name "*_test.exs" -o -name "*_test.go" \) \
  -not -path "*/node_modules/*" -not -path "*/.venv/*" 2>/dev/null | head -3
```

Update config based on findings:

```bash
# If tests/ directory found
jq '.tests.directory = "tests"' .ralph/config.json > .ralph/config.tmp && mv .ralph/config.tmp .ralph/config.json

# If test/ directory found (Elixir convention)
jq '.tests.directory = "test"' .ralph/config.json > .ralph/config.tmp && mv .ralph/config.tmp .ralph/config.json

# If colocated tests found (no test directory, but *.test.ts files exist)
jq '.tests.directory = "src"' .ralph/config.json > .ralph/config.tmp && mv .ralph/config.tmp .ralph/config.json
```

Set test patterns based on project type:

```bash
# Node/TypeScript projects
jq '.tests.patterns = "*.test.ts,*.test.tsx,*.spec.ts,*.spec.tsx,*.test.js,*.spec.js"' .ralph/config.json > .ralph/config.tmp && mv .ralph/config.tmp .ralph/config.json

# Python projects
jq '.tests.patterns = "*_test.py,test_*.py"' .ralph/config.json > .ralph/config.tmp && mv .ralph/config.tmp .ralph/config.json

# Elixir projects
jq '.tests.patterns = "*_test.exs"' .ralph/config.json > .ralph/config.tmp && mv .ralph/config.tmp .ralph/config.json

# Go projects
jq '.tests.patterns = "*_test.go"' .ralph/config.json > .ralph/config.tmp && mv .ralph/config.tmp .ralph/config.json
```

**If NO tests found:**
- Say: "⚠️ No test directory found. Ralph can only verify syntax and API responses."
- Say: "Add tests, or set `checks.requireTests: false` in config to silence this warning."

### 2e. Detect Build & Test Commands

Check for build script in package.json:
```bash
cat package.json 2>/dev/null | jq -r '.scripts.build // empty'
cat frontend/package.json 2>/dev/null | jq -r '.scripts.build // empty'
```

Update config with build command:
```bash
# If build script exists in root
jq '.checks.build = "npm run build"' .ralph/config.json > .ralph/config.tmp && mv .ralph/config.tmp .ralph/config.json

# If build script exists in frontend/
jq '.checks.build = "cd frontend && npm run build"' .ralph/config.json > .ralph/config.tmp && mv .ralph/config.tmp .ralph/config.json
```

Detect test framework:
```bash
test -f playwright.config.ts && echo "playwright"
test -f vitest.config.ts && echo "vitest"
test -f jest.config.js && echo "jest"
test -f manage.py && echo "django"
test -f pytest.ini && echo "pytest"
test -f pyproject.toml && grep -q "pytest" pyproject.toml && echo "pytest"
test -f mix.exs && echo "exunit"
```

Update config:
```bash
# If playwright found
jq '.playwright.enabled = true' .ralph/config.json > .ralph/config.tmp && mv .ralph/config.tmp .ralph/config.json

# If Django found (NO --parallel - it hides errors)
jq '.checks.test = "python manage.py test --keepdb"' .ralph/config.json > .ralph/config.tmp && mv .ralph/config.tmp .ralph/config.json

# If Django + Docker
jq '.checks.test = "docker compose exec -T web python manage.py test --keepdb"' .ralph/config.json > .ralph/config.tmp && mv .ralph/config.tmp .ralph/config.json

# If pytest found
jq '.checks.test = "pytest"' .ralph/config.json > .ralph/config.tmp && mv .ralph/config.tmp .ralph/config.json

# If vitest/jest found
jq '.checks.test = "npm test"' .ralph/config.json > .ralph/config.tmp && mv .ralph/config.tmp .ralph/config.json

# If ExUnit found (Elixir)
jq '.checks.test = "mix test"' .ralph/config.json > .ralph/config.tmp && mv .ralph/config.tmp .ralph/config.json
```

### 2f. Show Results

After updating, read the config and show user:

```bash
cat .ralph/config.json | jq '{paths, urls, commands, checks, tests}'
```

Say: "I've auto-configured Ralph:

[Show the detected settings in a nice format]

Edit `.ralph/config.json` if anything needs adjusting."

### 2g. Test Credentials (Optional)

```bash
grep -q "^RALPH_TEST_USER=" .env 2>/dev/null && echo "configured" || echo "not set"
```

**If not set**, use AskUserQuestion:
- **Question:** "Add test credentials? Ralph needs these for authenticated endpoints."
- **Header:** "Test auth"
- **Options:**
  - **Yes** - "I'll ask for email and password"
  - **Skip** - "Add to .env later"

If "Yes":
- Ask for email, then password
- Save to `.env` (gitignored — never committed):
  ```bash
  touch .env
  echo "" >> .env
  echo "# Test credentials for browser automation" >> .env
  printf 'RALPH_TEST_USER=%s\n' "$EMAIL" >> .env
  printf 'RALPH_TEST_PASSWORD=%s\n' "$PASSWORD" >> .env
  ```
- Say: "Credentials saved to .env (gitignored — never committed to git)"

If "Skip":
- Say: "No problem! Add `RALPH_TEST_USER` and `RALPH_TEST_PASSWORD` to `.env` when needed."

**If already set:**
- Say: "✓ Test credentials configured"

---

## Step 3: Check for DNA

Check if `~/.claude/DNA.md` exists.

**If DNA.md does NOT exist:**

Use AskUserQuestion:
- **Question:** "Want to set up your personal preferences? This teaches me how you like to work."
- **Header:** "DNA setup"
- **Options:**
  - **Yes, set up my DNA** - "Takes ~2 minutes, makes our collaboration better"
  - **Skip for now** - "You can run /my-dna anytime"

If user selects "Yes, set up my DNA":
- Run the `/my-dna` command inline (execute its full flow)
- After completing, continue to Step 4

If user selects "Skip for now":
- Say: "No problem! Run `/my-dna` anytime."
- Continue to Step 4

**If DNA.md EXISTS:**

Skip this step entirely. Move to Step 4.

---

## Step 4: Quick Reference

Print this:

```
Quick Reference
───────────────

Workflow:
  /prd [feature]        Brainstorm → PRD
  npx ralph run         Execute autonomously
  npx ralph status      Check progress
  npx ralph stop        Stop after current story

Quality:
  /vibe-check           Audit code quality
  /review               Review changes
  npx ralph check       Run verification

Other:
  /my-dna               Set preferences
  /explain              Understand code
  /styleguide           Generate design system
  /vibe-help            Full cheatsheet
```

Say: "You're all set! Run `/prd [your next feature]` to get started."
