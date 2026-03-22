---
name: test-as
description: Open a browser and log in as a selected user for manual testing
---

# Login as User

Open the frontend in a browser, already logged in as a selected user. Optimized for speed — minimal tool calls.

## Step 1: Ask Who to Log In As

Use AskUserQuestion to present the user selection. The top 3 are pinned; the rest are listed under "Other".

```
question: "Who do you want to log in as?"
header: "User"
options:
  - label: "Cooper Mayne"
    description: "cmayne@galipolaw.com"
  - label: "Darci Gilbert"
    description: "dgilbert@galipolaw.com"
  - label: "Dave Galipo"
    description: "davegalipo@galipolaw.com"
  - label: "Someone else"
    description: "Pick from the full user list"
```

If the user selects "Someone else", use AskUserQuestion again with these options:

```
question: "Which user?"
header: "User"
options:
  - label: "Santiago Laurel"
    description: "slaurel@galipolaw.com"
  - label: "Leslie DeLeon"
    description: "ldeleon@galipolaw.com"
  - label: "Dale Galipo"
    description: "dalekgalipo@yahoo.com"
  - label: "Another user"
    description: "Enter email manually"
```

Map the selected user to their email:
- Cooper Mayne → cmayne@galipolaw.com
- Darci Gilbert → dgilbert@galipolaw.com
- Dave Galipo → davegalipo@galipolaw.com
- Santiago Laurel → slaurel@galipolaw.com
- Leslie DeLeon → ldeleon@galipolaw.com
- Dale Galipo → dalekgalipo@yahoo.com

If "Another user" is selected, ask for the email as free text.

## Step 2: Get Token AND Open Browser (IN PARALLEL)

**These two calls MUST happen in the same message (parallel tool calls):**

**Call A — Bash:** Load env, get token, and echo both token and VITE_PORT:
```bash
set -a && source .env 2>/dev/null && set +a
PORT=${PORT:-8000}
VITE_PORT=${VITE_PORT:-5173}

TOKEN=$(curl -s -X POST "http://localhost:$PORT/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "$USER_EMAIL", "password": "home3232"}' | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('token','FAIL'))")

echo "TOKEN=$TOKEN"
echo "VITE_PORT=$VITE_PORT"
```
Replace `$USER_EMAIL` with the selected user's email.

**Call B — browser_navigate:** Navigate to `http://localhost:5173` (use VITE_PORT if known from env, default 5173).

## Step 3: Set Token and Reload

After both parallel calls complete, check the token from Call A:
- If token is `FAIL` → tell the user login failed, close browser, stop.
- Otherwise → use `browser_evaluate` to set the token and reload:

```
browser_evaluate → () => {
  localStorage.setItem('token', '<TOKEN>');
  window.location.href = '/';
}
```

**Do NOT wait or take a snapshot.** The user can see the browser themselves.

## Step 4: Report (brief)

One line: `Logged in as **[Name]** ([email]) — browser is open.`

Do NOT close the browser — the user needs it for manual testing.
