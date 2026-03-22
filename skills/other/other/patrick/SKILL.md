---
name: patrick
description: Access Patrick's expertise library for executive decision infrastructure. List, fetch, and manage structured expertise with context variables. Use for executive briefings, decision framing, and strategic analysis.
homepage: https://patrickbot.io
metadata: {"openclaw":{"emoji":"🤖","requires":{"bins":["patrick-cli"]},"install":[{"id":"patrick-install","kind":"script","script":"install.sh","bins":["patrick-cli"],"label":"Install Patrick CLI"}]}}
---

# Patrick Skill

**Patrick is a licensed expertise management system** that provides executive decision infrastructure through structured, context-aware expertise.

**⚠️ If Patrick isn't working:** Check `{baseDir}/install.md` for complete setup instructions including license configuration and initialization.

## Setup Workflow

### 1. Install the CLI

Run the install script to download the patrick-cli binary from the Patrick server:

```bash
./install.sh
```

Or install directly via curl:

```bash
curl -fsSL https://portal.patrickbot.io/downloads/latest/install.sh | bash
```

This will download patrick-cli for your platform, verify its SHA256 checksum, and place it in `$PATRICK_DATA_PATH/bin/patrick-cli` (default: `~/.patrick/bin/`). The Dockerfile and run.sh add this to PATH automatically, so you can call `patrick-cli` directly.

### 2. Get Your License

**Visit [patrickbot.io](https://patrickbot.io)** to obtain your Patrick license.

Once you have your license, **send it to me via chat:**

```
Here's my Patrick license: <paste-your-license-here>
```

I'll configure it automatically. Alternatively, you can set it manually:

```bash
patrick-cli set-license "your-license-here"
```

To switch to a different account (wipes existing data since it's tied to your identity):

```bash
patrick-cli set-license "new-license" --wipe-data
```

### 3. Initialize Patrick Context

**CRITICAL: Before running any Patrick expertise, initialize the context:**

```bash
patrick-cli fetch initialize
```

This bootstraps Patrick with information about you, your company, and your team. Without initialization, other expertise prompts won't work properly.

### 4. Verify Installation

Test it by listing available expertise:

```bash
patrick-cli list
```

**Note**: The server URL defaults to `https://portal.patrickbot.io`. For local development:

- **Host machine**: `export PATRICK_SERVER_URL="http://localhost:8080"`
- **Docker container**: `export PATRICK_SERVER_URL="http://host.docker.internal:8080"`

The patrick-moltbot Docker container is pre-configured with the correct URL.

### 4. Set Up Cronjobs (Critical)

**Patrick requires scheduled cronjobs to function properly.** Read `INSTALL.md` in this directory for complete setup instructions including recommended cronjob schedules for daily briefings and commitment tracking.

**License auto-renewal in cron:** Before running any scheduled task, check if the license is about to expire and renew it:

```bash
# Check license expiry and renew if <1 day remaining
DAYS=$(patrick-cli license 2>&1 | grep "days remaining" | grep -oP '\d+')
if [ -n "$DAYS" ] && [ "$DAYS" -lt 1 ]; then
  patrick-cli renew
fi

# Then run your scheduled expertise
patrick-cli fetch daily-briefing --json
```

The `patrick-cli renew` command contacts the server, verifies your active subscription, and saves a fresh license with the remaining subscription days.

### 5. Keeping Patrick Updated

Check for updates and upgrade to the latest version:

```bash
# Check if update is available
patrick-cli upgrade --check

# Upgrade to latest version
patrick-cli upgrade
```

The upgrade process:
1. Contacts Patrick server for latest version info
2. Verifies SHA256 checksum of downloaded binary
3. Backs up current version
4. Installs new version
5. Shows release notes

Updates are cryptographically verified and signed by the Patrick server.

## What You Get

When you list expertise, you'll see:
- Expertise ID and version
- Name and description
- Category (sense, interpret, decide, align, execute, learn, reporting, intelligence)
- Response format (structured JSON, markdown, mixed)
- Required context variables
- Whether it's bidirectional (accepts data back)

## IMPORTANT: Gathering Context Before Using Patrick

**For AI Agents:** Before running any Patrick expertise, you MUST:

1. **Check for company data files** in `/app/company/` or similar locations
2. **Read all available context:**
   - Company data JSON files
   - Slack message archives
   - JIRA tickets
   - Git commit history
   - Calendar events
   - Any operational data available
3. **Load this context into your working memory**
4. **Then run Patrick expertise** with full awareness of company operations

Patrick expertise is most effective when you have complete situational awareness. Don't run Patrick commands without first gathering all available company data.

## Commands Overview

| Command | Purpose | Example |
|---------|---------|---------|
| `set-license` | Set or update your Patrick license | `patrick-cli set-license "LICENSE_TOKEN"` |
| `list` | List all available expertise | `patrick-cli list` |
| `fetch` | Get expertise template from server | `patrick-cli fetch daily-briefing` |
| `send` | Store results back to Patrick | `patrick-cli send daily-briefing --data @output.json` |
| `get` | Retrieve previously stored results | `patrick-cli get daily-briefing` |

**Key Distinction:**
- **`fetch`** = Get the expertise template/prompt FROM the server
- **`get`** = Retrieve your stored data/results THAT YOU SENT BACK

## Using Expertise with LLMs

### Workflow Overview

1. **List expertise** to see what's available in your license
2. **Fetch an expertise** with optional context variables
3. **Send expertise content** to an LLM for processing
4. **Validate response** against the provided JSON schema (if structured)
5. **Store response** back to Patrick using `send` (if bidirectional)
6. **Retrieve stored data** later using `get`

### Step 1: List Available Expertise

```bash
patrick-cli list
```

Example output:
```
Available Expertise:

  daily-briefing (v1.0.0)
    Name: Daily Executive Briefing
    Category: sense
    Response Format: structured
    Bidirectional: ✓ (stores to 'daily-briefing')
    Required Context: (none)
    Description: What's urgent, developing, changed, and the one question

  decision-framing (v1.0.0)
    Name: Decision Framing
    Category: decide
    Response Format: structured
    Bidirectional: ✓ (stores to 'decision-framing')
    Required Context:
      - decision
    Description: Structures ambiguous decisions into clear trade-offs...
```

### Step 2: Fetch Expertise

**Without context (for expertise that doesn't need it):**

```bash
patrick-cli fetch daily-briefing
```

**With context variables:**

```bash
patrick-cli fetch decision-framing \
  --context '{"decision":"Should we raise prices?"}'
```

**Get JSON output for LLM integration:**

```bash
patrick-cli fetch daily-briefing \
  --json
```

### Step 3: Send to LLM

When you fetch expertise, you receive:
- **content**: The filled expertise text to send to the LLM
- **response_schema**: JSON schema for validating the LLM response (if structured)
- **response_format**: How the LLM should format its response (structured/markdown/mixed)

**Example workflow:**

```bash
# Fetch expertise as JSON
EXPERTISE_DATA=$(patrick-cli fetch daily-briefing --json)

# Extract the content field
EXPERTISE_CONTENT=$(echo "$EXPERTISE_DATA" | jq -r '.content')

# Send to your LLM (pseudo-code)
# LLM_RESPONSE=$(send_to_llm "$EXPERTISE_CONTENT")

# If structured format, validate against schema
RESPONSE_SCHEMA=$(echo "$EXPERTISE_DATA" | jq -r '.response_schema')
# validate_json "$LLM_RESPONSE" "$RESPONSE_SCHEMA"
```

### Step 4: Store Results (Optional)

For bidirectional expertise, send the LLM response back to Patrick:

```bash
# Store the response
patrick-cli send daily-briefing \
  --data @llm-response.json

# Later, retrieve stored data
patrick-cli get daily-briefing
```

## Key Concepts

### Context Variables

Many prompts require context to fill template variables. Use `--context` with a JSON object:

```json
{
  "current_phase": "pre-launch",
  "launch_date": "2026-02-15",
  "completed_items": 12,
  "target_platforms": ["iOS", "Android"]
}
```

Variables are substituted using `{{context.key}}` syntax in the expertise content.

### Response Formats

- **structured**: LLM must return JSON matching the provided schema
- **markdown**: LLM returns markdown text
- **mixed**: LLM returns markdown with embedded JSON blocks

### Bidirectional Expertise

Some expertise accepts data back from the LLM and stores it in Patrick's datastore:

- `✓ (stores to 'key')` - Use `send` command to store response
- `✗ (one-way)` - Expertise is read-only, no data storage

## Common Patterns

### Pattern 1: Simple Fetch

```bash
# No context needed
patrick-cli fetch daily-briefing
```

### Pattern 2: Contextual Fetch

```bash
# Provide context variables
patrick-cli fetch decision-framing \
  --context '{"decision":"Should we expand to EMEA?"}'
```

### Pattern 3: Full Bidirectional Workflow

```bash
# 1. Fetch expertise template
patrick-cli fetch daily-briefing --json > expertise.json

# 2. Process with LLM (pseudo-code)
# llm_process < expertise.json > response.json

# 3. Store response back to Patrick
patrick-cli send daily-briefing --data @response.json

# 4. Later, retrieve stored data
patrick-cli get daily-briefing
```

## Troubleshooting

### License Errors

```
Error: No license found at ~/.patrick/license.jwt
```

**Solution**: Get a license from [patrickbot.io](https://patrickbot.io) and save it:

```bash
patrick-cli set-license "YOUR_LICENSE_HERE"
```

```
Error: Expertise 'X' not in license
```

**Solution**: Visit [patrickbot.io](https://patrickbot.io) to upgrade your license or add the expertise

### Fetch Errors

```
Error fetching expertise: 401 Unauthorized
```

**Solution**: Check your license is valid and not expired

```
Expertise 'X' not found
```

**Solution**: List available expertise with `list` to see what's accessible

### Context Errors

```
Warning: Missing required context variables
```

**Solution**: Check `list-prompts` output for required context fields and provide them via `--context`

### Signature Verification Errors

```
Error: HMAC signature verification failed for 'storage_key'
```

**Cause**: Files in `~/.patrick/data/` were manually edited, corrupted, or modified outside of Patrick CLI.

**Solution**: Delete the corrupted file and regenerate the data:

```bash
rm ~/.patrick/data/storage_key.json
# Re-run the command that generates this data
```

**Prevention**: Never manually edit files in `~/.patrick/` - all data is signed with HMAC-SHA256 tied to your customer identity.

### Switching Licenses

```
Error: License belongs to a different account.
```

**Cause**: You're trying to set a license for a different account. Stored data is signed with your current customer identity and cannot be read under a different account.

**Solution**: Use `set-license` with `--wipe-data` to switch accounts:

```bash
patrick-cli set-license "NEW_LICENSE" --wipe-data
```

This deletes all stored data in `~/.patrick/data/` and saves the new license. You'll need to re-initialize afterwards.

## Security

- Never commit `license.jwt` or environment files with real credentials
- Licenses are authenticated on every API call
- Expertise content is verified with SHA256 checksums
- Only expertise listed in your license are accessible

**⚠️ IMPORTANT: Do not manually edit files in `~/.patrick/`**

All data stored in `~/.patrick/` is signed with HMAC-SHA256 tied to your verified customer identity:
- **`license.jwt`** - Your license token
- **`jwks_cache.json`** - Public key cache for license verification
- **`data/`** - Stored expertise responses (if using bidirectional expertise)

Manual modifications will break signature verification and cause errors like:
```
Error: Stored data signature verification failed
```

If you need to reset your data, delete the specific file and re-run the command - don't edit it manually.

See `{baseDir}/references/security.md` for detailed information on Patrick's cryptographic signing model.

## Reference Documentation

See `{baseDir}/references/` for:
- `prompts-api.md` - Full API documentation (now uses /v1/expertise endpoints)
- `prompt-format.md` - Expertise structure specification
- `llm-integration.md` - LLM integration patterns
- `security.md` - Cryptographic signing and data integrity model

## Advanced Usage

### Custom Server URL

Point to a self-hosted Patrick server:

```bash
export PATRICK_SERVER_URL="https://patrick.mycompany.com"
```

### Data Storage Path

Configure where Patrick stores local data (directory, not file):

```bash
export PATRICK_DATA_PATH=~/.patrick  # Default location
```

Patrick will store customer data files in `$PATRICK_DATA_PATH/data/<storage_key>.json`

### Debug Logging

Enable detailed logging:

```bash
export RUST_LOG="patrick_cli=debug"
```
