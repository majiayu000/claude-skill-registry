---
name: new-cask
argument-hint: "<url>"
description: >-
  This skill should be used when the user asks to "add a cask to homebrew",
  "create a homebrew cask", "add an app to homebrew", "new cask for",
  "homebrew cask for", "package an app for homebrew", "submit to homebrew-cask",
  "make a cask", "contribute a cask", or wants to package a macOS application
  for Homebrew.
allowed-tools: >-
  Read,
  Grep,
  Glob,
  WebFetch,
  WebSearch,
  Bash(brew *),
  Bash(gh *),
  Bash(curl *),
  Bash(hdiutil *),
  Bash(defaults read *),
  Bash(shasum *),
  Bash(git *),
  Bash(plutil *),
  Bash(file *),
  Bash(lipo *),
  Bash(ls *),
  Bash(find *),
  Bash(strings *),
  Bash(unzip *),
  Bash(open *),
  Bash(${CLAUDE_PLUGIN_ROOT}/scripts/*)
---

# Creating a New Homebrew Cask

You are orchestrating the creation of a new Homebrew cask. This skill coordinates multiple specialist agents and scripts to complete the workflow.

**IMPORTANT:** This skill runs in the main conversation context. You will use the Task tool to spawn agents for specialized work.

## Input

**URL provided:** $ARGUMENTS

If no URL was provided, ask the user for:
1. The app name, OR
2. A download URL (direct link to DMG/ZIP), OR
3. The product homepage (you'll find the download link)

## Workflow Overview

```
1. Pre-flight checks    → Agent: pre-flight-checker
2. Download & inspect   → Agent: app-inspector
3. Livecheck strategy   → Agent: livecheck-advisor
4. Write cask file      → Agent: cask-writer
5. Testing              → Automated tests, install, createzap, uninstall
6. Submit PR            → Agent: pr-submitter
```

**Create a task list** to track progress through these steps.

## Step-by-Step Execution

### Step 1: Pre-flight Checks

Before investing time, verify the app is suitable:

```
Use the Task tool:
- subagent_type: homebrew:pre-flight-checker
- prompt: Check if this app is suitable for homebrew-cask submission.
  <include whatever info you have: URL, app name, homepage>
```

The agent will derive any missing info (app name from URL, homepage via search, etc.) and include it in the output.

**Capture from output:** App name, homepage, download URL, description - you'll need these for later steps.

**Decision point:** If the agent returns REJECT, stop and explain why to the user. If CAUTION, inform the user and ask if they want to proceed.

### Step 2: Download and Inspect

Download and inspect the app in one step:

```
Use the Task tool:
- subagent_type: homebrew:app-inspector
- prompt: Download and inspect the app.
  Download URL: <url>
  Homepage: <homepage>
```

The agent will download the file, compute the SHA256, extract all metadata, and run Homebrew's `generate_cask_token` tool to get the canonical token.

**Capture from output:** Suggested token, SHA256, version, bundle ID, app name, min macOS, auto-update info (framework, appcast URL if found), architecture.

**Use the suggested token** from app-inspector for subsequent steps. This token comes from Homebrew's tooling and handles naming conventions and collision detection.

**Note on versioned URLs:** If the download URL is unversioned (e.g., `App.dmg`), the livecheck-advisor may find a versioned URL in an appcast, release feed, or other source. If so, you'll need to re-download using the versioned URL to get the correct SHA256.

### Step 3: Livecheck Strategy

Determine how to check for updates:

```
Use the Task tool:
- subagent_type: homebrew:livecheck-advisor
- prompt: Recommend a livecheck strategy for <app-name>.
  Download URL: <url>
  Homepage: <homepage>
  Update URL: <appcast-or-feed-url-if-found>
  Current version: <version>
```

Get the recommended livecheck block.

### Step 4: Write the Cask

Synthesize everything into a cask file:

```
Use the Task tool:
- subagent_type: homebrew:cask-writer
- prompt: Write a cask for <app-name> with this metadata:
  Token: <token>
  Version: <version>
  URL: <download-url>
  SHA256: <checksum> (or :no_check if unversioned URL)
  (If separate binaries per architecture, provide URL and SHA256 for each)
  Name: <display-name>
  Description: <one-line-desc>
  Homepage: <homepage>
  Bundle ID: <bundle-id>
  App bundle: <app-name>.app
  Min macOS: <min-version>
  Auto-updates: <yes/no>
  Livecheck: <livecheck-block>
  Architecture: <arm64/intel/universal, only if not universal>
```

**Note:** The zap stanza is added later after running createzap during testing.

### Step 5: Testing

#### Automated Tests

Run the validation script:

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/test-cask.sh "<token>"
```

If tests fail, review the output, fix the cask (often `brew style --fix` handles style issues), and re-run.

**For unversioned URLs:** Use `--skip-livecheck` flag.

#### Install and Validate

1. **Install:**
   ```bash
   HOMEBREW_NO_INSTALL_FROM_API=1 brew install --cask <token>
   ```

2. **Launch:**
   ```bash
   open -a "<App Name>"
   ```

3. **User verification:** Ask the user to sign in or set up the app if needed, then confirm when done.

#### Zap Discovery

4. **Run createzap** (try both app name and bundle ID):
   ```bash
   brew tap nrlquaker/createzap 2>/dev/null || true
   brew createzap "<App Name>"
   brew createzap "<bundle-id>"
   ```

5. **Update the cask** - Add the discovered zap paths using the Edit tool. For simple additions you can edit directly; for significant changes, re-invoke the cask-writer agent.

6. **Uninstall:**
   ```bash
   brew uninstall --cask <token>
   ```

7. **Re-run automated tests** if zap stanza was added.

### Step 6: Submit PR

When ready to submit:

```
Use the Task tool:
- subagent_type: homebrew:pr-submitter
- prompt: Submit a PR for the <token> cask.
  Version: <version>
  Cask path: <path-to-cask-file>
  All tests passed: yes
```

## Error Recovery

If any step fails:
- The task list shows which steps completed
- You can resume from the failed step
- Agent outputs are preserved in conversation history

## Reference Documentation

For detailed guidance, agents can read these docs (at `/opt/homebrew/docs/`):
- `Acceptable-Casks.md` - What's allowed
- `Cask-Cookbook.md` - Stanza reference
- `Brew-Livecheck.md` - Livecheck strategies
- `Adding-Software-to-Homebrew.md` - Contribution process

## Scripts Location

Scripts are at `${CLAUDE_PLUGIN_ROOT}/scripts/`:
- `download-checksum.sh <url> [filename]` - Download and SHA256
- `test-cask.sh <token> [--skip-livecheck]` - Run audit/style/livecheck
