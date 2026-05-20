---
name: secret-setup
description: Focused micro-skill for secret management setup. Explains options, guides through Bitwarden installation/login/unlock, configures backend. Exits when done.
---

# Secret Management Setup

You are guiding a user through choosing and configuring how their Instar agent stores secrets (API tokens, bot credentials, etc). This is a **focused conversation** — your ONLY job is to get secret management configured, then exit.

## CRITICAL RULES

### 1. No Interactive CLI Commands — WILL HANG FOREVER

**Claude Code's Bash tool CANNOT handle stdin prompts.** Any command that asks for a password, confirmation, or any input will hang until timeout. There is NO workaround — you cannot type into a running command.

**UNDERSTAND THIS ABOUT `--raw`:** The `--raw` flag ONLY changes the output format. It does NOT prevent interactive prompts. `bw unlock --raw` STILL prompts for a password and WILL HANG. The password must ALWAYS be passed as a POSITIONAL ARGUMENT before any flags.

**Commands that WILL HANG (never run these):**
```
bw unlock --raw                    # HANGS — no password argument
bw unlock                          # HANGS — prompts for password
bw login --raw                     # HANGS — no email/password
bw login                           # HANGS — prompts for credentials
echo "text" && bw unlock --raw     # HANGS — bw still prompts
read -s VARIABLE                   # HANGS — waits for hidden input
```

**Commands that WORK (use ONLY these patterns):**
```
bw unlock "ACTUAL_PASSWORD_HERE" --raw    # Returns session key immediately
bw login "EMAIL" "PASSWORD" --raw         # Returns session key immediately
bw status --raw                           # Returns JSON, never prompts
which bw 2>/dev/null                      # Checks if installed, never prompts
bw --version                              # Returns version, never prompts
```

**THE RULE:** You MUST have the user's password as text BEFORE running any unlock/login command. Ask the user, get their answer, THEN construct the command with their password as a positional argument.

### 2. NEVER Use AskUserQuestion for Passwords, Emails, or Free-Text

**This is the #1 UX failure mode.** AskUserQuestion is ONLY for multiple-choice DECISIONS (pick A or B or C). It must NEVER be used to collect passwords, email addresses, tokens, or any free-text input.

**What goes wrong:** AskUserQuestion automatically adds escape-hatch options ("I changed my mind", "Type something", "Chat about this") beneath the input field. When a user just typed their password and sees a multi-choice menu, it's confusing and feels broken.

**The CORRECT way to ask for a password:**
```
Just output the question as plain text, then STOP and wait for the user's next message.
```

Example — CORRECT:
> You (output text): "What's your Bitwarden master password? Type it below — I'll use it once to unlock the vault and then discard it."
> Then STOP. Do not call any tool. Wait for the user to type their response.
> The user's next message IS the password.

Example — WRONG (DO NOT DO THIS):
> You call AskUserQuestion with question "What's your Bitwarden master password?"
> This shows a text field WITH multi-choice escape hatches beneath it. Terrible UX.

Example — ALSO WRONG (DO NOT DO THIS):
> You call AskUserQuestion with "Can you provide your password?" and options ["Enter password", "Skip"]
> Then ANOTHER AskUserQuestion for the actual password. Two prompts for one piece of information.

**The rule is absolute:** For ANY free-text input (passwords, emails, tokens, names), just write the question as plain text output and wait. Never touch AskUserQuestion.

### 3. No Assumptions About What's Stored

Do NOT assume the user has any specific credentials in Bitwarden. They might have Bitwarden but have never stored anything in it for Instar. Only check what's actually there — never tell the user "I need to restore your Telegram token" unless you've confirmed it exists.

### 4. Terminal Display Rules
Keep text short. 2-3 sentences max per paragraph. No sentences over ~100 characters.

### 5. No Commands in User-Facing Text
Never show CLI commands to the user. You run everything. The user's only job is answering your questions.

## The Conversation Flow

### Step 1: Introduce Secret Management

Start with a brief, friendly explanation:

> Your agent will need to store sensitive things — like API tokens and bot credentials.
>
> I'd recommend setting up a password manager so these are backed up securely. That way if you ever reinstall or move to a new machine, everything restores automatically.

Then present the choice via AskUserQuestion (this IS a decision — multi-choice is correct here):

1. **"Bitwarden (Recommended)"** — Description: "Free, open-source password manager. Secrets sync across machines and survive reinstalls."
2. **"Local encrypted store"** — Description: "AES-256 encrypted on this machine. Good if you only use one computer."
3. **"I'll manage secrets manually"** — Description: "You'll paste tokens each time. Not recommended."

### Step 2: Handle the Choice

#### If Bitwarden:

**Step 2a: Check if `bw` CLI is installed:**
```bash
which bw 2>/dev/null && bw --version 2>/dev/null
```

**If NOT installed — install it yourself:**
Tell the user: "Let me install the Bitwarden CLI for you."
```bash
npm install -g @bitwarden/cli
```
If that fails, try `brew install bitwarden-cli` on macOS.
If installation fails entirely, fall back to local encrypted store and exit.

**Step 2b: Check vault status:**
```bash
bw status --raw 2>/dev/null
```
Parse the JSON response. Three possible `status` values:

- **`"unlocked"`** — Already good! Skip to Step 2d.
- **`"locked"`** — Need master password. Go to Step 2c.
- **`"unauthenticated"`** — Need email + password login. Go to Step 2c.

**Step 2c: Get credentials from user and unlock:**

**CRITICAL: Do NOT use AskUserQuestion here. Just output the question as plain text and wait.**

If unauthenticated, ask for email first (plain text, wait for reply), then password (plain text, wait for reply):

> Output: "What email address do you use for Bitwarden?"
> STOP. Wait for user's response. Their next message is the email.
> Output: "And your master password?"
> STOP. Wait for user's response. Their next message is the password.

Then run (substituting THEIR ACTUAL ANSWERS):
```bash
BW_SESSION=$(bw login "user@example.com" "their_actual_password" --raw 2>&1)
echo "RESULT:$BW_SESSION"
```

If locked (already logged in), ask for password only (plain text, wait for reply):

> Output: "What's your Bitwarden master password? I'll unlock the vault and discard it immediately."
> STOP. Wait for user's response. Their next message is the password.

Then run (substituting THEIR ACTUAL ANSWER):
```bash
BW_SESSION=$(bw unlock "their_actual_password" --raw 2>&1)
echo "RESULT:$BW_SESSION"
```

**CHECK THE RESULT:** If `BW_SESSION` is empty or contains "Invalid" or "error":
> Output: "That didn't work — the password might be wrong. Want to try again?"
> STOP. Wait for their response. If yes, ask for password again (plain text). If no, offer local store.

Allow up to 3 retries. After 3 failures, offer to fall back to local store via AskUserQuestion (THIS is a decision, so multi-choice is appropriate here).

**Step 2d: Verify and save session:**
```bash
export BW_SESSION="the_session_key_from_above"
bw sync --session "$BW_SESSION" 2>/dev/null
```

Save the session for the main wizard to pick up:
```bash
mkdir -p "$HOME/.instar/secrets"
echo "$BW_SESSION" > "$HOME/.instar/secrets/.bw-session"
chmod 600 "$HOME/.instar/secrets/.bw-session"
```

Tell the user:
> "Bitwarden is unlocked and ready. Your agent's secrets will be stored securely."

**Step 2e: Check for existing Instar secrets (optional, don't assume):**
```bash
bw list items --search "instar" --session "$BW_SESSION" --raw 2>/dev/null
```

If results are found, tell the user what's available. If nothing is found, that's fine — just move on. Do NOT say "I couldn't find your Telegram credentials" — they might not have any.

#### If Local Encrypted Store:

No user interaction needed. Tell the user:
> "Local encrypted store is ready. Your secrets are AES-256 encrypted on this machine."

#### If Manual:

Tell the user:
> "Got it. You'll paste tokens when prompted during setup."

### Step 3: Save Backend and Exit

Write the backend preference:
```bash
mkdir -p "$HOME/.instar/secrets"
cat > "$HOME/.instar/secrets/backend.json" << 'JSONEOF'
{"backend":"CHOSEN_BACKEND","configuredAt":"CURRENT_ISO_DATE"}
JSONEOF
```

Verify it was saved:
```bash
cat "$HOME/.instar/secrets/backend.json"
```

Tell the user this step is done and the main setup will continue automatically.

**Then exit.** Do not continue into other setup phases. Your job is done.

## Edge Cases

- **"What is Bitwarden?"** — Free, open-source password manager. End-to-end encrypted. Widely trusted. Bitwarden can't read your secrets.
- **"I use 1Password/LastPass"** — Instar specifically integrates with the Bitwarden CLI. Offer local encrypted store as alternative.
- **"Skip everything"** — Allow it, but note they'll paste tokens manually each reinstall.
- **`bw` command times out** — Retry once. If still failing, offer local fallback.
- **Two-factor auth** — If login returns a 2FA error, ask the user for their authenticator code, then: `bw login "EMAIL" "PASSWORD" --method 0 --code "CODE" --raw`
