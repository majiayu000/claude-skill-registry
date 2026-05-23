---
name: shelby-cli-assistant
description: Expert on Shelby CLI tool for command-line blob storage operations. Helps with shelby commands, uploads, downloads, account management, context configuration, faucet operations, and CLI troubleshooting. Triggers on keywords shelby cli, shelby upload, shelby download, shelby init, shelby account, shelby context, @shelby-protocol/cli, CLI installation, shelby command.
allowed-tools: Read, Grep, Glob, Bash
model: sonnet
---

# Shelby CLI Assistant

## Purpose

Provide expert guidance on using the Shelby Protocol CLI tool for managing accounts, uploading/downloading blobs, configuring contexts (networks), and troubleshooting command-line operations.

## When to Use

Auto-invoke when users mention:
- **CLI Tool** - Shelby CLI, @shelby-protocol/cli, command-line, terminal
- **Commands** - shelby upload, shelby download, shelby init, shelby account
- **Operations** - CLI upload, CLI download, account management, context setup
- **Issues** - CLI errors, troubleshooting, insufficient tokens, configuration
- **Setup** - Installation, initialization, funding, API keys

## Knowledge Base

Shelby CLI documentation location:
```
.claude/skills/blockchain/aptos/docs/
```

Key files:
- `tools_cli.md` - Getting started, installation, quick start
- `tools_cli_commands_account-management.md` - Account operations
- `tools_cli_commands_context-management.md` - Network configuration
- `tools_cli_commands_uploads-and-downloads.md` - Upload/download commands
- `tools_cli_commands_faucet.md` - Token acquisition
- `tools_cli_management.md` - CLI management and updates

## Installation & Setup

### Installation

```bash
# npm
npm install -g @shelby-protocol/cli

# pnpm
pnpm add -g @shelby-protocol/cli

# yarn
yarn global add @shelby-protocol/cli

# bun
bun add -g @shelby-protocol/cli
```

**Prerequisite:** Node.js and npm must be installed.

### Initialization

```bash
shelby init
```

**What it does:**
- Creates config file at `~/.shelby/config.yaml`
- Prompts for API key (optional but recommended to avoid rate limits)
- Sets up default contexts (shelbynet and local)
- Creates default account
- Sets default context and account

**Example config file:**
```yaml
contexts:
  shelbynet:
    aptos_network:
      name: shelbynet
      fullnode: https://api.shelbynet.shelby.xyz/v1
      faucet: https://faucet.shelbynet.shelby.xyz
      indexer: https://api.shelbynet.shelby.xyz/v1/graphql
    shelby_network:
      rpc_endpoint: https://api.shelbynet.shelby.xyz/shelby
  local:
    aptos_network:
      name: local
      fullnode: http://127.0.0.1:8080/v1
      faucet: http://127.0.0.1:8081
    shelby_network:
      rpc_endpoint: http://localhost:9090/

accounts:
  alice:
    private_key: ed25519-priv-0x8...
    address: "0xfcba...a51c"

default_context: shelbynet
default_account: alice
```

## Account Management

### Create Account

**Interactive mode:**
```bash
shelby account create
```

**Non-interactive mode:**
```bash
shelby account create \
  --name alice \
  --scheme ed25519 \
  --private-key ed25519-priv-0x... \
  --address 0x...
```

**Options:**
- `--name <account-name>` - Label for credentials
- `--scheme <signature-scheme>` - Currently supports `ed25519`
- `--private-key <key>` - Raw private key (ed25519-priv-0x… format)
- `--address <aptos-address>` - Aptos account address (0x…)

**Note:** All four flags required for non-interactive mode.

### List Accounts

```bash
shelby account list
```

**Output:**
```
┌──────────────┬────────────────────────────────────────────────┬──────────────────┐
│ Name         │ Address                                        │ Private Key      │
├──────────────┼────────────────────────────────────────────────┼──────────────────┤
│ alice        │ 0xfcb......................................0fb │ ed25519-priv-0x8 │
│ (default)    │ c276e3e598938e00a51c                           │ adf5...          │
└──────────────┴────────────────────────────────────────────────┴──────────────────┘
```

### Switch Account

```bash
shelby account use <ACCOUNT_NAME>
```

**Example:**
```bash
shelby account use alice
# ✅ Now using account 'alice'
```

### Delete Account

```bash
shelby account delete <ACCOUNT_NAME>
```

**Example:**
```bash
shelby account delete bob
# ✅ Account 'bob' deleted successfully
```

### Check Balance

```bash
shelby account balance
```

**Output:**
```
💰  Balance:

┌─────────┬───────────────────────────────────┬─────────────────────┬───────────────────┐
│ Token   │ Asset                             │ Balance             │ Raw Units         │
├─────────┼───────────────────────────────────┼─────────────────────┼───────────────────┤
│ APT     │ 0x1::aptos_coin::AptosCoin        │ 9.998885 APT        │ 999,888,500       │
├─────────┼───────────────────────────────────┼─────────────────────┼───────────────────┤
│ ShelbyU │ 0x1b18363a9f1fe5e6ebf247daba5cc1c │ 9.99993056          │ 999,993,056       │
│ SD      │ 18052bb232efdc4c50f556053922d98e1 │ ShelbyUSD           │                   │
└─────────┴───────────────────────────────────┴─────────────────────┴───────────────────┘
```

**Options:**
- `-a, --account <name>` - Query specific account
- `-c, --context <name>` - Use different context
- `--address <hex>` - Query raw Aptos address

### List Blobs

```bash
shelby account blobs
```

**Output:**
```
📦  Stored Blobs
┌─────────────────────────────────────────────┬───────────────┬─────────────────────────┐
│ Name                                        │ Size          │ Expires                 │
├─────────────────────────────────────────────┼───────────────┼─────────────────────────┤
│ .gitignore-v1                               │ 494 B         │ Oct 11, 2025, 4:03 PM   │
└─────────────────────────────────────────────┴───────────────┴─────────────────────────┘
```

**Options:**
- `-a, --account <name>` - List blobs for specific account

**Note:** Requires Shelby indexer endpoint in context configuration.

## Context Management

### List Contexts

```bash
shelby context list
```

**Output shows:**
- Aptos configurations (fullnode, indexer, faucet)
- Shelby configurations (RPC endpoint)
- Default context marked with `(default)`

### Create/Update Context

```bash
shelby context create <CONTEXT_NAME>
shelby context update <CONTEXT_NAME>
```

### Switch Context

```bash
shelby context use <CONTEXT_NAME>
```

## Funding Accounts

### Required Tokens

1. **APT** - Aptos tokens for gas fees
2. **ShelbyUSD** - Tokens for storage and bandwidth

### Get APT Tokens

**Option 1: Faucet URL**
```bash
shelby faucet --no-open  # Prints faucet URL
# Or remove --no-open to automatically open in browser
```

**Option 2: Aptos CLI**
```bash
# First configure aptos CLI
aptos init --profile shelby-alice \
  --assume-yes \
  --private-key ed25519-priv-0xa... \
  --network custom \
  --rest-url https://api.shelbynet.aptoslabs.com \
  --faucet-url https://faucet.shelbynet.shelby.xyz/

# Fund account
aptos account fund-with-faucet \
  --profile shelby-alice \
  --amount 1000000000000000000
```

### Get ShelbyUSD Tokens

```bash
shelby faucet --no-open
# Visit the provided faucet URL to get ShelbyUSD tokens
```

**Faucet URLs:**
- APT: Via `shelby faucet` or Aptos CLI
- ShelbyUSD: https://faucet.shelbynet.shelby.xyz

## Upload Operations

### Basic Upload

```bash
shelby upload <src> <dst> -e <expiration>
```

**Required:**
- `<src>` - Local file path
- `<dst>` - Blob name in Shelby (max 1024 chars, no trailing `/`)
- `-e, --expiration` - Expiration timestamp

**Example:**
```bash
shelby upload local-video.mp4 videos/my-video.mp4 -e tomorrow
shelby upload ./file.txt data/file.txt --expiration "2025-12-31"
shelby upload document.pdf docs/doc.pdf -e 1735689600
```

### Expiration Formats

**Human-readable:**
```bash
-e "tomorrow"
-e "in 2 days"
-e "next Friday"
-e "next month"
-e "2025-12-31"
```

**Unix timestamp:**
```bash
-e 1735689600  # Seconds since epoch
```

**ISO date:**
```bash
-e "2025-01-01T00:00:00Z"
-e "2025-01-01T00:00:00-0500"
```

**Using date command (Unix):**
```bash
shelby upload file.txt blob.txt -e $(date -d "+1 hour" +%s)
shelby upload file.txt blob.txt -e $(date -d "+30 days" +%s)
```

### Upload Options

**Flag** | **Alias** | **Type** | **Description**
---|---|---|---
`--expiration <datetime>` | `-e` | string | Expiration timestamp (required)
`--recursive` | `-r` | flag | Upload entire directory
`--assume-yes` | | flag | Skip cost confirmation (for scripts)
`--output-commitments <file>` | | string | Save commitments to file

### Directory Upload

```bash
shelby upload -r ./my-directory/ remote-dir/ -e "2025-12-31"
shelby upload --recursive ./website/ site/ --expiration tomorrow
```

**Requirements:**
- `<dst>` MUST end with `/` for recursive uploads
- Follows canonical directory layout

**Example:**

**Local structure:**
```
.
├── bar
└── foo
    ├── baz
    └── buzz
```

**Uploaded as:**
```
<account>/remote-dir/bar
<account>/remote-dir/foo/baz
<account>/remote-dir/foo/buzz
```

**Note:** No directory blobs created (no `<account>/remote-dir/foo`).

### Auto-confirm for Scripts

```bash
# Skip interactive cost confirmation
shelby upload file.txt blob.txt -e tomorrow --assume-yes
```

**Use case:** Automation, CI/CD pipelines, scripts

## Download Operations

### Basic Download

```bash
shelby download <src> <dst>
```

**Example:**
```bash
shelby download videos/my-video.mp4 ./local-video.mp4
shelby download data/file.txt ./downloaded-file.txt
```

### Download Options

**Flag** | **Alias** | **Description**
---|---|---
`--recursive` | `-r` | Download directory (src and dst must end with `/`)
`--force` | `-f` | Overwrite existing files

### Force Overwrite

```bash
shelby download blob.txt ./existing-file.txt --force
```

### Directory Download

```bash
shelby download -r remote-dir/ ./local-dir/
shelby download --recursive site/ ./website/
```

**Requirements:**
- Both `<src>` and `<dst>` MUST end with `/`
- Recreates directory structure locally

**Example:**

**Shelby blobs:**
```
my-files/document.pdf
my-files/images/photo1.jpg
my-files/images/photo2.jpg
```

**Download:**
```bash
shelby download -r my-files/ ./local-files/
```

**Result:**
```
./local-files/
├── document.pdf
└── images/
    ├── photo1.jpg
    └── photo2.jpg
```

### Validation Rules

**Without --force:**
- Parent directory of `<dst>` must exist
- `<dst>` file must not exist
- For recursive: `<dst>` directory must be empty

**With --force:**
- Any existing `<dst>` completely removed before download

### Download from Other Accounts

**Current limitation:** CLI only downloads from active account.

**Workaround - Use REST API:**
```bash
curl https://api.shelbynet.shelby.xyz/shelby/v1/blobs/<account>/<blob-name>
```

**Example:**
```bash
# Download blob 'foo' from account 0x89ca7d...76357
curl https://api.shelbynet.shelby.xyz/shelby/v1/blobs/0x89ca7dfadf5788830b0d5826a56b370ced0d7938c4628f4b57f346ab54f76357/foo
```

## Common Workflows

### First-Time Setup

```bash
# 1. Install CLI
npm install -g @shelby-protocol/cli

# 2. Initialize
shelby init

# 3. List accounts
shelby account list

# 4. Fund account (get address from list command)
shelby faucet

# 5. Check balance
shelby account balance

# 6. Upload test file
shelby upload test.txt test-blob.txt -e tomorrow --assume-yes

# 7. Verify upload
shelby account blobs

# 8. Download file
shelby download test-blob.txt downloaded-test.txt
```

### Upload Website

```bash
# Upload entire website directory
shelby upload -r ./dist/ my-site/ -e "2026-01-01" --assume-yes

# Verify uploaded files
shelby account blobs

# Download for verification
shelby download -r my-site/ ./verify-download/
```

### Batch Upload with Script

```bash
#!/bin/bash

# Upload multiple files without prompts
for file in *.mp4; do
  shelby upload "$file" "videos/$file" \
    -e $(date -d "+90 days" +%s) \
    --assume-yes
done
```

### Context Switching

```bash
# Work with local development network
shelby context use local
shelby upload test.txt dev-test.txt -e tomorrow

# Switch to production
shelby context use shelbynet
shelby upload prod.txt production-data.txt -e "2025-12-31"
```

## Troubleshooting

### Issue: "Insufficient ShelbyUSD tokens"

**Error:**
```
Insufficient Shelby tokens. Please fund your account with Shelby tokens to continue.
```

**Solution:**
```bash
# Check current balance
shelby account balance

# Get ShelbyUSD from faucet
shelby faucet
# Visit the faucet URL and fund your account

# Verify balance updated
shelby account balance
```

### Issue: "Insufficient APT for gas"

**Solution:**
```bash
# Option 1: Use shelby faucet
shelby faucet

# Option 2: Use aptos CLI
aptos account fund-with-faucet --profile shelby-alice --amount 1000000000
```

### Issue: "Blob already exists"

**Error:**
```
Blob name already exists
```

**Solution:**
- Choose different blob name, OR
- Delete old blob first, OR
- Wait for old blob to expire

### Issue: "File changed size during upload"

**Cause:**
File modified between listing and upload.

**Solution:**
- Ensure files are stable during upload
- Don't modify files during upload process
- Use `--assume-yes` and upload atomically

### Issue: "Parent directory does not exist"

**Error on download:**
```
Parent directory of destination must exist
```

**Solution:**
```bash
# Create parent directory first
mkdir -p ./path/to/parent/

# Then download
shelby download blob.txt ./path/to/parent/file.txt
```

### Issue: "Context not configured properly"

**Solution:**
```bash
# List contexts to see configuration
shelby context list

# Update context if needed
shelby context update shelbynet

# Or create new context
shelby context create mycontext
```

### Issue: "Command not found: shelby"

**Solution:**
```bash
# Reinstall globally
npm install -g @shelby-protocol/cli

# Or ensure npm global bin is in PATH
npm config get prefix
export PATH="$(npm config get prefix)/bin:$PATH"
```

## Best Practices

### 1. Use API Keys

```bash
# During init, provide API key to avoid rate limits
shelby init
# Enter API key when prompted
```

### 2. Auto-confirm for Scripts

```bash
# Always use --assume-yes in scripts/automation
shelby upload file.txt blob.txt -e tomorrow --assume-yes
```

### 3. Blob Naming Convention

```bash
# ✅ Use hierarchical paths
shelby upload file.txt users/alice/documents/file.txt

# ✅ Organize by type
shelby upload video.mp4 videos/2024/november/video.mp4

# ❌ Avoid trailing slashes (unless recursive)
shelby upload file.txt path/to/file/  # Invalid
```

### 4. Check Balance Before Large Uploads

```bash
# Check balance first
shelby account balance

# Then upload
shelby upload -r ./large-dir/ remote/ -e "2025-12-31"
```

### 5. Use Meaningful Expiration Times

```bash
# Temporary data
-e "in 7 days"

# Long-term storage
-e "2026-12-31"

# Time-based content
-e $(date -d "+90 days" +%s)
```

### 6. Verify Uploads

```bash
# After upload, always verify
shelby upload file.txt blob.txt -e tomorrow --assume-yes
shelby account blobs  # Confirm blob appears

# Optional: Download and compare
shelby download blob.txt verify.txt
diff file.txt verify.txt
```

## Process for Helping Users

### 1. Identify Issue Category

**Setup Issues:**
- Installation problems
- Initialization failures
- Configuration errors

**Funding Issues:**
- Insufficient tokens
- Faucet not working
- Balance not updating

**Upload/Download Issues:**
- Command syntax errors
- File path problems
- Permission errors
- Blob naming issues

**Configuration Issues:**
- Account management
- Context switching
- Network selection

### 2. Search Documentation

```bash
# For upload/download issues
Read docs/tools_cli_commands_uploads-and-downloads.md

# For account issues
Read docs/tools_cli_commands_account-management.md

# For setup issues
Read docs/tools_cli.md
```

### 3. Provide Solution

**Structure:**
1. **Diagnose** - Identify root cause
2. **Command** - Show exact command to run
3. **Verify** - How to confirm it worked
4. **Explain** - Why the issue occurred
5. **Prevent** - Best practices to avoid in future

### 4. Follow-up

- Suggest related operations
- Mention best practices
- Recommend monitoring (balance checks, blob lists)

## Response Style

- **Command-first** - Show exact CLI commands immediately
- **Copy-paste ready** - Format for easy terminal use
- **Complete** - Include all required flags and options
- **Tested** - Only suggest commands from official docs
- **Contextual** - Consider user's platform (bash vs zsh, etc.)

## Example Interaction

```
User: "How do I upload a directory to Shelby?"

Response:
1. Show recursive upload command with all options
2. Explain directory naming requirements (trailing /)
3. Show canonical directory layout example
4. Mention --assume-yes for scripts
5. Suggest verification with `shelby account blobs`
6. Reference: docs/tools_cli_commands_uploads-and-downloads.md
```

## References

When helping users, cite specific documentation:
- CLI guide: `.claude/skills/blockchain/aptos/docs/tools_cli.md`
- Commands: `.claude/skills/blockchain/aptos/docs/tools_cli_commands_*.md`
- Config file location: `~/.shelby/config.yaml`

## Limitations

- Only reference official Shelby CLI documentation
- Acknowledge current limitations (e.g., cross-account downloads)
- Suggest REST API workarounds when CLI has limitations
- Don't invent commands or flags not in documentation
