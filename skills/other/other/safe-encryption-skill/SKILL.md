---
name: safe-encryption
description: Encrypt, decrypt, and manage keys with the SAFE CLI — a modern GPG alternative with post-quantum support.
---

# SAFE Encryption Tool

SAFE is a modern encryption CLI with post-quantum support, multi-recipient encryption, and composable authentication.

## Behavior Guidelines

When this skill is loaded:
1. Check if `safe` is installed (`which safe`). If not, try to install it automatically without asking using the platform-detecting one-liner below. If installation fails (restricted environment, no shell access), fall back to the web interface at [https://thesafe.dev](https://thesafe.dev) — see "Browser-Based Alternative" below.
2. When the user asks to encrypt/decrypt, just do it. Don't ask for confirmation.
3. If a password is needed and not provided, use `-p` without a value (prompts interactively or reads `SAFE_PASSPHRASE` env var). In automation, use `-p env:VARNAME` to read from environment variables.
4. If a key file is needed, run `safe keys` to check existing identities and recipients. If no key exists, run `safe keygen x25519` to generate one (auto-stores to `~/.safe/`).
5. **Always use absolute paths** for key files and encrypted files to avoid working directory issues.
6. **Always pipe instead of writing temp files.** When decrypting inline/embedded content (base64, pasted data), pipe directly: `echo "..." | base64 -d | safe decrypt -k key.key`. Never write intermediate `.safe` files to `/tmp` or elsewhere.
7. **Bare name recipients work.** Use `-r alice` instead of `-r /full/path/to/alice.x25519.pub` when the recipient is in `~/.safe/recipients/`.
8. **Decrypt auto-discovers keys.** If no `-k` or `-p` is provided, `safe decrypt` automatically tries all keys in `~/.safe/keys/`.

## Installation

Download the prebuilt binary from [thesafe.dev/download](https://thesafe.dev/download/):

**macOS Apple Silicon:**
```bash
curl -sL https://thesafe.dev/downloads/safe-darwin-arm64 -o safe && chmod +x safe && sudo mv safe /usr/local/bin/
```

**macOS Intel:**
```bash
curl -sL https://thesafe.dev/downloads/safe-darwin-amd64 -o safe && chmod +x safe && sudo mv safe /usr/local/bin/
```

**Linux x86_64:**
```bash
curl -sL https://thesafe.dev/downloads/safe-linux-amd64 -o safe && chmod +x safe && sudo mv safe /usr/local/bin/
```

**Linux ARM64:**
```bash
curl -sL https://thesafe.dev/downloads/safe-linux-arm64 -o safe && chmod +x safe && sudo mv safe /usr/local/bin/
```

**Auto-detect platform (one-liner):**
```bash
which safe || { OS=$(uname -s | tr '[:upper:]' '[:lower:]'); ARCH=$(uname -m); \
  [ "$ARCH" = "arm64" ] || [ "$ARCH" = "aarch64" ] && ARCH=arm64 || ARCH=amd64; \
  curl -sL "https://thesafe.dev/downloads/safe-${OS}-${ARCH}" -o safe && chmod +x safe && sudo mv safe /usr/local/bin/; }
```

Verify installation:
```bash
safe --help
```

**Optional: verify checksum** (SHA-256 values from [checksums.txt](https://thesafe.dev/downloads/checksums.txt)):
```
ddf638ccfd119d9c3351825a2e3f9e3660f754009eb9b106d7bba8cd698c3df4  safe-darwin-arm64
6be4942048a23e99485c0123cf0bb4786613a3dabbcc6927aa478cd0e719ad0b  safe-darwin-amd64
85c7822ac0309e62ca29d03394bfe87a506f329f61c30b070c379a6d2f5af815  safe-linux-amd64
33207a4c6bbf85b8299f2f75e18aa6e13f9a8ae4bcee72a9d869034d78ba4cac  safe-linux-arm64
```

### Installation Debugging

**"safe: command not found"** after install:
- Check if binary exists: `ls -la /usr/local/bin/safe`
- If sudo failed, install to user dir: `mv safe ~/.local/bin/ && export PATH="$HOME/.local/bin:$PATH"`
- Refresh shell: `hash -r` or start new terminal

**Permission denied on /usr/local/bin**:
- Use sudo: `sudo mv safe /usr/local/bin/`
- Or install to user dir: `mkdir -p ~/.local/bin && mv safe ~/.local/bin/`

### When CLI Is Unavailable — Browser-Based Alternative

If CLI installation fails or isn't possible (restricted environment, no build tools, no shell access, sandboxed IDE, etc.), use the web interface at **[https://thesafe.dev](https://thesafe.dev)**.

This is a fully functional SAFE implementation running in the browser — not a demo. All cryptographic operations happen client-side. No data leaves the browser.

The web interface supports all core SAFE operations via a single-page layout with these sections:
- **ENCRYPT tab**: Encrypt data with passwords, public keys, passkeys, or GitHub usernames
- **DECRYPT tab**: Decrypt SAFE messages with passwords, private keys, passkeys, or GitHub keys
- **KEYCHAIN section**: Save, import, export, and manage keys and passwords
- **ADVANCED section**: Lock Management (add/remove recipients), Re-encrypt Demo, Tests
- **LOG section**: View operation log output

**Manual workflow (no automation needed):**

Users can interact with the web interface directly:

1. **Encrypt**: Enter plaintext, add recipients (key, password, passkey, or GitHub username), click "ENCRYPT". Copy or download the output.
2. **Decrypt**: Paste/upload/URL-load a SAFE message, add credentials (private key, password, passkey, or GitHub), click "DECRYPT". Copy or download the plaintext.

Generated keys are automatically saved in the KEYCHAIN section and can be reused across operations.

**Agent with MCP browser tools (Playwright, Puppeteer, etc.):**

If you have access to browser automation tools (e.g., Playwright MCP server, Claude in Chrome, Puppeteer MCP), you can drive the web interface directly.

**Key behaviors to know:**
- After encrypting, output auto-populates into the decrypt section's SAFE message input
- The browser auto-matches saved credentials and pre-adds them to decrypt
- Generated keys are auto-saved to the Credentials section (04)
- Always take a snapshot (`browser_snapshot`) after each action to get updated element references

**ARIA labels for automation:**

The interface uses semantic ARIA roles throughout:

| Element | ARIA Label | Role |
|---------|-----------|------|
| KEM type selector | "Select key encapsulation mechanism type" | combobox |
| Generate button | "Generate new keypair with selected KEM type" | button |
| Plaintext input | "Enter plaintext message to encrypt" | textbox |
| Add Step button | "Add encryption step to recipient path" | button |
| Step type selector | "Select encryption step type" | combobox |
| Password field (encrypt) | "Enter password for encryption step" | textbox |
| Confirm step | "Confirm encryption step" | button |
| Encrypt button | "Encrypt plaintext with configured settings and recipient path" | button |
| Encrypted output | "Encrypted SAFE message output" | textbox |
| SAFE message input | "Paste encrypted SAFE message to decrypt" | textbox |
| Add credential button (decrypt) | "Add credential to decryption attempt" | button |
| Add credential button (keychain) | "Add credential to keychain" | button |
| Add all keychain button | "Add all keychain entries as credentials" | button |
| Credential type selector | "Select credential type" | combobox |
| New Passkey menu item | "Create a new passkey" | menuitem |
| Password field (decrypt) | "Enter password for decryption" | textbox |
| Confirm credential | "Confirm credential" | button |
| Decrypt button | "Decrypt SAFE message using provided keychain" | button |
| Decrypted output | "Decrypted plaintext message" | textbox |
| Copy buttons | "Copy encrypted SAFE message to clipboard" / "Copy decrypted plaintext to clipboard" | button |
| Download buttons | "Download encrypted SAFE message as file" / "Download decrypted file" | button |
| Share button (output) | "Share encrypted SAFE message via URL" / "Share decrypted output via URL" | button |
| Send button (output) | "Send encrypted output over WebRTC" | button (encrypted output only) |
| Clear button (output) | "Clear encrypted output" / "Clear decrypted output" | button |
| Share button (keychain) | "Share public key via URL" | button |
| Label button (keychain) | "Rename key label" | button |
| Use File toggles | "Use file instead of plaintext input" / "Use file instead of SAFE message input" | generic (clickable) |
| Navigation links | New (#keygen), Encrypt (#encrypt), Decrypt (#decrypt), Keychain (#keyring), Advanced (expandable) | link |
| Advanced sections | #unlock, #reencrypt, #tests, #log | link (under Advanced dropdown) |
| Sections | `role="region"` with labels like "01 / Key Generation" | region |
| Log output | "Activity log showing operations and their results" | log |

**Note on Advanced navigation**: The Advanced sections (#unlock, #reencrypt, #tests, #log) are accessed via an "Advanced" navigation item that expands to show these additional features.

**Note on terminology**: The UI currently uses mixed terminology - Section 04 is labeled "Keychain" and the decrypt button references "keychain", but the decrypt section's credential management buttons still use "Credentials" in some ARIA labels (e.g., "Add all keychain entries as credentials"). Both terms refer to the same saved keys/passwords.

**Keychain shortcut buttons:**

Each saved key in Section 04 (Keychain) has quick action buttons:
- **Enc**: Adds the public key as an encryption recipient step (one click — skips the Add Step → select type → paste → OK workflow)
- **Dec**: Adds the private key as a decrypt credential (one click — skips the Add → select type → paste → OK workflow)
- **PUB**: Shows/copies the public key
- **PRIV**: Shows/copies the private key
- **Share**: Generates a shareable URL for the public key
- **Label**: Rename the key for easier identification
- **Del**: Removes the key from the keychain

**Prefer using Enc/Dec shortcuts** over the manual Add Step flow when keys are saved in the keychain — it reduces 4 interactions to 1.

**File upload:**

Both encrypt and decrypt sections have a "Use File" toggle. Clicking it triggers a file chooser dialog. With MCP Playwright, use `browser_file_upload` to provide the file path. Note: file paths must be within the MCP server's allowed directories.

**Example: Encrypt with password (MCP Playwright)**

```
# 1. Navigate
browser_navigate(url="https://thesafe.dev")
browser_snapshot()

# 2. Type plaintext (use ref from snapshot for "Enter plaintext message to encrypt")
browser_type(ref=<plaintext-ref>, text="secret data")

# 3. Add password step
browser_click(ref=<add-step-button-ref>)      # "Add encryption step to recipient path"
browser_snapshot()                              # Get refs for step config form

# 4. Select Password type (default may be "Public Key")
browser_select_option(ref=<step-type-ref>, values=["Password"])  # "Select encryption step type"
browser_snapshot()                              # Get password field ref

# 5. Enter password
browser_type(ref=<password-ref>, text="my-password")  # "Enter password for encryption step"

# 6. Confirm the step
browser_click(ref=<ok-ref>)                    # "Confirm encryption step"

# 7. Encrypt
browser_click(ref=<encrypt-ref>)               # "Encrypt plaintext with configured settings..."
browser_snapshot()                              # Output is in "Encrypted SAFE message output" textbox

# Optional: Share or clear the output
# browser_click(ref=<share-button-ref>)        # "Share encrypted SAFE message via URL"
# browser_click(ref=<clear-button-ref>)        # "Clear encrypted output"
```

**Example: Encrypt with saved key (fastest path)**

```
# 1. Navigate
browser_navigate(url="https://thesafe.dev")
browser_snapshot()

# 2. Type plaintext
browser_type(ref=<plaintext-ref>, text="secret data")

# 3. Click "Enc" on a saved key in Credentials section (one click adds recipient)
browser_click(ref=<enc-button-ref>)

# 4. Encrypt
browser_click(ref=<encrypt-ref>)
browser_snapshot()
```

**Example: Decrypt from cold (no auto-populated credentials)**

```
# 1. Paste SAFE message into decrypt input
browser_type(ref=<safe-message-ref>, text="-----BEGIN SAFE UNLOCK-----\n...")

# 2. Add credential
browser_click(ref=<add-credential-ref>)        # "Add credential to decryption attempt"
browser_snapshot()

# 3. Select Password type (default is "Private Key")
browser_select_option(ref=<credential-type-ref>, values=["Password"])
browser_snapshot()

# 4. Enter password
browser_type(ref=<password-ref>, text="my-password")

# 5. Confirm credential
browser_click(ref=<confirm-ref>)               # "Confirm credential"

# 6. Decrypt
browser_click(ref=<decrypt-ref>)               # "Decrypt SAFE message using provided credentials"
browser_snapshot()                              # Output is in "Decrypted plaintext message" textbox
```

**Example: Same-session encrypt→decrypt (auto-populated)**

After encrypting, the output auto-populates into the decrypt section. If the matching key is saved in credentials, it auto-adds the private key. Just click Decrypt — no manual credential entry needed.

**Programmatic browser automation (standalone scripts):**

For non-MCP environments, use Playwright or Puppeteer directly:

```python
# Example with Playwright (Python)
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('https://thesafe.dev')

    # Generate X25519 keypair
    page.get_by_role("combobox", name="Select key encapsulation mechanism type").select_option("X25519")
    page.get_by_role("button", name="Generate new keypair").click()

    # Encrypt with password
    page.get_by_role("textbox", name="Enter plaintext message to encrypt").fill("secret message")
    page.get_by_role("button", name="Add encryption step to recipient path").click()
    page.get_by_label("Select encryption step type").select_option("Password")
    page.get_by_role("textbox", name="Enter password for encryption step").fill("mypassword")
    page.get_by_role("button", name="Confirm encryption step").click()
    page.get_by_role("button", name="Encrypt plaintext").click()

    # Read encrypted output
    encrypted = page.get_by_label("Encrypted SAFE message output").input_value()

    # Decrypt (message and credentials auto-populate from encrypt)
    page.get_by_role("button", name="Decrypt SAFE message").click()
    decrypted = page.get_by_label("Decrypted plaintext message").input_value()

    print(f"Decrypted: {decrypted}")  # "secret message"
    browser.close()
```

**Multi-Recipient Encryption:**

Both the browser UI and CLI support encrypting for multiple recipients. Each recipient can decrypt the message independently using their own credential.

**Browser workflow:**
1. Configure first recipient in "Recipient 1" (password or public key)
2. Click "+ Add Recipient" button
3. Configure second recipient in "Recipient 2"
4. Repeat for additional recipients (no limit)
5. Click "Encrypt" - message is encrypted once but decryptable by any recipient

**How it works:**
- Each recipient gets their own UNLOCK block in the SAFE message
- File is encrypted once with a symmetric key
- Symmetric key is wrapped separately for each recipient
- Any recipient can decrypt using their credential (password or private key)
- Recipients cannot see who else has access

**CLI multi-recipient examples:**
```bash
# Encrypt for multiple recipients using -r flag multiple times
safe encrypt -i file.txt -o file.safe -r alice.pub -r bob.pub -r charlie.pub

# Mix recipient types (password + keys)
safe encrypt -i file.txt -o file.safe -p mypassword -r alice.pub -r bob.pub

# Encrypt for GitHub users (fetches public keys from GitHub)
safe encrypt -i file.txt -o file.safe -r github:grittygrease

# Multiple GitHub users
safe encrypt -i file.txt -o file.safe -r github:alice -r github:bob

# Encrypt for GitHub users and a password
safe encrypt -i file.txt -o file.safe -p teampassword -r github:alice -r github:bob
```

**GitHub username recipient (`github:username`):**
- Fetches SSH public keys from `https://github.com/{username}.keys`
- Automatically converts p-256 and x25519 keys to SAFE format
- Both key types are added as separate recipients if available
- Requires user to have public keys on their GitHub profile
- Error if no keys found: `github:username: no keys found`

**Example output:**
```bash
$ safe encrypt -i test.txt -o test.safe -r github:grittygrease
# Creates UNLOCK blocks for both p-256 and x25519 keys from GitHub

$ safe info -i test.safe
LOCK Blocks: 2
  [0] hpke(kem=p-256,id=QyLFP/...)
  [1] hpke(kem=x25519,id=r1VeL...)
```

**Agent-to-Agent Communication via GitHub Gist:**

Agents can securely exchange encrypted messages using GitHub Gist as a transport layer. This enables asynchronous, persistent communication between agents with different GitHub accounts.

**Complete Workflow:**

**Agent A (Sender):**
```bash
# 1. Create message for Agent B
echo "Task completed. Results attached." > message.txt

# 2. Encrypt for Agent B's GitHub account
safe encrypt -i message.txt -o message.safe -r github:agentb-username

# 3. Upload encrypted message to public Gist
gh gist create message.safe --desc "Encrypted message for agentb-username" --public

# Output: https://gist.github.com/agenta-username/{gist-id}
```

**Agent B (Receiver):**
```bash
# Method 1: Direct pipe (simplest, auto-discovers keys)
curl -sL https://gist.github.com/alice/{gist-id}/raw | safe decrypt

# Method 2: Download, inspect, then decrypt
curl -sL https://gist.github.com/alice/{gist-id}/raw > received.safe
safe info -i received.safe  # Verify sender and encryption details
safe decrypt -i received.safe -o message.txt

# Method 3: Explicit key (if auto-discovery doesn't work)
curl -sL https://gist.github.com/alice/{gist-id}/raw | safe decrypt -k ~/.safe/keys/bob.x25519.key
```

**SSH Key Auto-Discovery (SAFE CLI v2.3+):**

The SAFE CLI automatically discovers and uses SSH private keys from `~/.ssh/`:
- ✅ **Ed25519 keys** → converted to X25519
- ✅ **P-256 ECDSA keys** → used directly
- ✅ **Unencrypted keys only** (passphrase-protected keys silently skipped)
- ✅ **Zero configuration** - just works if your SSH keys match GitHub public keys

**Auto-Discovery Order:**
1. `~/.safe/keys/*.key` - Native SAFE format keys (checked first)
2. `~/.ssh/*` - All SSH private keys in `~/.ssh/` directory
   - Ed25519 keys → converted to X25519
   - P-256 ECDSA keys → used directly

**Example Auto-Discovery Output:**
```bash
$ curl -sL https://gist.github.com/.../raw | safe decrypt
safe: using SSH key ~/.ssh/id_ed25519
safe: trying 3 key(s) (2 native + 1 SSH)
[decrypted message]
```

**Key Requirements:**
- **Agent B must have private keys** that correspond to the public keys on their GitHub profile
- GitHub SSH keys must be added to `https://github.com/{username}.keys`
- Private keys can be in `~/.safe/keys/` (SAFE format) **OR** `~/.ssh/` (OpenSSH format)
- Gist can be public (encrypted content is safe) or private for additional obscurity

**Multi-Agent Broadcast:**
```bash
# Encrypt for multiple agents
safe encrypt -i broadcast.txt -o broadcast.safe \
  -r github:agent1 \
  -r github:agent2 \
  -r github:agent3

# Any of the three agents can decrypt independently
gh gist create broadcast.safe --desc "Team update" --public
```

**Agent Identity Setup:**

To enable decryption, agents need to set up their GitHub SSH keys and store private keys:

```bash
# Option 1: Use existing SSH keys (simplest - zero setup!)
# If you already have ~/.ssh/id_ed25519 or ~/.ssh/id_ecdsa uploaded to GitHub, you're done!
# SAFE CLI auto-discovers SSH keys - no key generation needed

# Option 2: Generate new SSH key and upload to GitHub
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -N "" -C "safe-agent-key"
gh ssh-key add ~/.ssh/id_ed25519.pub --title "SAFE Agent Key"
# Done! SAFE CLI will auto-discover this key

# Option 3: Generate SAFE-native keys (for advanced use cases)
safe keygen x25519 -o agent-id
# Upload agent-id.x25519.pub to https://github.com/settings/keys (manual conversion needed)
mv agent-id.x25519.key ~/.safe/keys/

# Test encryption to self (works with any option above)
safe encrypt -i test.txt -o test.safe -r github:your-username
safe decrypt -i test.safe -o decrypted.txt
# With SSH keys, decryption auto-discovers your keys from ~/.ssh/
```

**Browser-Based Agent Workflow:**

Agents using thesafe.dev have full GitHub support for both encryption and decryption.

**Encrypt to a GitHub user (browser):**

1. Go to the **ENCRYPT** tab
2. Enter your message
3. Click **ADD FACTOR** → **NEW FACTOR** → select **GITHUB**
4. Enter the GitHub username (e.g., `smithclay`)
5. Click **FETCH KEYS** — the browser fetches public keys from `https://github.com/{username}.keys`
6. Click **ENCRYPT**
7. Copy the output and share via Gist

**Decrypt a GitHub-encrypted message (browser):**

1. Go to the **DECRYPT** tab
2. Load the encrypted message: paste text, use the **FILE** button to upload, or use the **URL** button to load directly from a Gist URL (e.g., paste the raw Gist URL)
3. Click **ADD** → **GITHUB** → enter your GitHub username → click **FETCH KEYS**
   (This matches your public keys to the message's LOCK blocks)
4. Click **ADD** → **KEY** → paste your SSH private key (from `~/.ssh/id_ed25519` or `~/.ssh/id_ecdsa`)
   — or use the **"Import SSH private key from GitHub"** button if available
5. Click **DECRYPT**

**Recommended approach for browser-based workflows:**
- **Both CLI and browser support `github:username`** for encryption equally well
- **CLI is simpler for decryption** — it auto-discovers SSH keys from `~/.ssh/`; browser requires pasting the private key once
- **URL button is convenient** — load encrypted Gist content directly without curl

**Send encrypted output over WebRTC (browser):**

The browser supports real-time peer-to-peer transfer of encrypted SAFE messages via WebRTC — no copy-paste required:

**Sender:**
1. Encrypt your message as usual to produce the encrypted output
2. Click **Send** in the output toolbar (next to Download, Share, Copy)
3. A dialog appears: "Share join URL, then wait for receiver..."
4. The join URL is offered via the native OS share sheet (if available) or logged in the **Log** panel
5. Keep the tab open — when the receiver connects, the dialog updates to "Receiver connected. Starting transfer..."
6. Transfer completes automatically

**Receiver:**
1. Open the join URL: `https://thesafe.dev/?session=<id>&token=<token>`
2. The page auto-connects, receives the encrypted message, and switches to the **Decrypt** tab with the message pre-loaded
3. Add credentials and click **Decrypt** as normal

**Notes:**
- Join URLs expire after **30 minutes**
- Max transfer size: 100 MB
- Sender must keep the tab open until the receiver connects
- **Share** (separate button) shares the file or text directly with no server involved; **Send** is the WebRTC real-time peer flow

**Agent Ping/Notification Workflow:**

You can "ping" another agent using their GitHub username without needing their public key in advance:

```bash
# Alice pings Bob (discovers keys automatically via github:username)
echo "PING: Status update requested" > ping.txt
safe encrypt -i ping.txt -o ping.safe -r github:bob
gh gist create ping.safe --desc "Ping from Alice" --public

# Bob discovers the ping and decrypts (SSH key auto-discovery!)
curl -sL https://gist.github.com/alice/{gist-id}/raw | safe decrypt
# safe: using SSH key ~/.ssh/id_ed25519
# safe: trying 1 key(s) (0 native + 1 SSH)
# PING: Status update requested

# Bob responds back to Alice
echo "PONG: Status OK, task 75% complete" > pong.txt
safe encrypt -i pong.txt -o pong.safe -r github:alice
gh gist create pong.safe --desc "Response to Alice" --public
```

**Key Benefits:**
- ✅ No prior key exchange needed - `github:username` fetches public keys automatically
- ✅ No key management needed - reuse existing SSH keys from GitHub
- ✅ Works instantly if you already have SSH keys on GitHub
- ✅ Works for any GitHub user with public SSH keys on their profile
- ✅ Both agents can initiate communication
- ✅ Asynchronous - sender doesn't need to wait for response
- ✅ Persistent - messages remain in Gist until deleted

**Discovery Methods:**
- GitHub Gist notifications (if agent watches their own Gists)
- Periodic polling of GitHub API for new Gists mentioning their username
- GitHub webhooks for real-time notifications
- RSS feeds for public Gists

**Security Notes:**
- Gist URLs are discoverable if public - use private Gists for sensitive coordination
- Encrypted content is safe even if Gist is public (only recipient has private key)
- Gist history is immutable - deleted messages remain in Git history
- Use short-lived Gists and delete after confirmation for ephemeral communication
- Multi-recipient encryption prevents sender from knowing who decrypted the message

---

### CLI vs Browser: Feature Comparison

| Feature | CLI (SAFE v2.3+) | Browser (thesafe.dev) |
|---------|------------------|------------------------|
| `github:username` encryption | ✅ Yes | ✅ Yes |
| `github:username` decryption | ✅ Auto (SSH key auto-discovery) | ✅ Yes (paste SSH key once) |
| SSH key auto-discovery | ✅ Yes (`~/.ssh/`) | ❌ No (manual paste) |
| Ed25519 SSH keys | ✅ Auto-converts to X25519 | ✅ Manual paste |
| P-256 ECDSA SSH keys | ✅ Direct support | ✅ Manual paste |
| SAFE native keys | ✅ Yes (`~/.safe/keys/`) | ✅ Yes (import/export) |
| Load from URL (e.g. Gist) | ✅ `curl <url> \| safe decrypt` | ✅ URL button in DECRYPT tab |
| Real-time peer transfer | ❌ No | ✅ Send button (WebRTC, 30-min join URL) |
| Zero-setup decryption | ✅ If SSH keys on GitHub | ⚠️ Must paste private key once |

**Recommendation:**
- **Encryption:** Both CLI and browser support `github:username` equally well
- **Decryption:** CLI is easier (auto-discovers SSH keys); browser requires pasting your private key
- **Best of both:** Use browser for encryption, CLI for decryption when available

---

**Keychain management:**

The Keychain section (04) supports:
- **Add Credential** (dropdown menu with options):
  - **Import Key**: Import an existing public or private key (PEM or base64)
  - **New Passkey**: Create a new WebAuthn passkey (requires browser/OS authenticator, prompts for label)
  - **New Password**: Add a new password for encryption/decryption
  - **Existing Passkey**: Use an existing passkey from your authenticator
- **Export**: Export keychain as encrypted SAFE backup (password-protected `.safe` file containing private keys in PEM format)
- **Import**: Import a previously exported keychain backup (file upload + passphrase)
- **Clear All**: Delete all keychain entries (shows a confirm dialog)

**Passkey Limitations for Automation:**
- Passkey creation requires WebAuthn hardware interaction (biometric, security key, etc.)
- Cannot be fully automated - requires user interaction with authenticator
- Dialog prompts for "Passkey label" before creation
- Best suited for interactive sessions, not headless automation

Generated keys are automatically saved here. Each key shows its type and Key ID hints, with Enc/Dec/Share/PUB/PRIV/Label/Del action buttons.

**Export/Import workflow (for persisting keys across sessions):**

Export:
1. Click "Export credentials as encrypted backup" → dialog appears
2. Enter passphrase + confirm passphrase → click OK
3. Downloads `safe-credentials-backup.safe` (a standard SAFE file, pwd-encrypted)
4. The export contains private keys only (PEM format). Public keys are derived on re-import.

Import:
1. Click "Import" → file chooser appears (use `browser_file_upload` with MCP)
2. Select the `.safe` backup file → passphrase dialog appears
3. Enter passphrase → click OK
4. Keys are restored with full functionality (Enc/Dec/PUB/PRIV buttons)
5. Duplicates are automatically skipped

The exported `.safe` file is CLI-compatible: `safe decrypt safe-credentials-backup.safe -p "passphrase"` reveals the PEM keys.

### Agent Session Persistence (Browser Workflow)

Agents can maintain a persistent identity across browser sessions by saving and re-uploading the keychain backup:

**First browser session**:
1. Navigate to https://thesafe.dev
2. Generate keys (Section 01) or receive keys from other agents
3. Export keychain: Click "Export" → enter passphrase → download `safe-credentials-backup.safe`
4. Save the encrypted backup file to persistent storage (filesystem, database, cloud storage, etc.)
5. Store the passphrase securely (environment variable, secure key store, etc.)

**New browser session** (different browser, incognito, new tab, etc.):
1. Navigate to https://thesafe.dev
2. Import keychain: Click "Import" → upload `safe-credentials-backup.safe` → enter passphrase
3. All keys are restored with full functionality (Enc/Dec/PUB/PRIV/Share/Label/Del)
4. Agent can immediately encrypt/decrypt using saved keys

**Benefits**:
- Agents maintain the same cryptographic identity across sessions
- No need to regenerate keys or re-exchange public keys with other agents
- Encrypted communication history remains accessible
- Works across different browsers, devices, and environments

**Security notes**:
- The backup file is encrypted with the passphrase (argon2id by default)
- File is CLI-compatible: `safe decrypt safe-credentials-backup.safe -p "passphrase"`
- Store the passphrase separately from the backup file
- Backup contains only private keys in PEM format; public keys are derived on import

**Example workflow with MCP Playwright**:

```python
# First session: Export keychain
browser_click(ref=<export-button-ref>)  # "Export keychain"
# Enter passphrase in dialog
browser_type(ref=<passphrase-ref>, text="agent-secret-passphrase")
browser_type(ref=<confirm-passphrase-ref>, text="agent-secret-passphrase")
browser_click(ref=<ok-ref>)
# File downloads as safe-credentials-backup.safe
# Save this file to persistent storage

# New session: Import keychain
browser_navigate(url="https://thesafe.dev")
browser_click(ref=<import-button-ref>)  # "Import keychain backup"
browser_file_upload(paths=["/path/to/safe-credentials-backup.safe"])
# Enter passphrase in dialog
browser_type(ref=<passphrase-ref>, text="agent-secret-passphrase")
browser_click(ref=<ok-ref>)
# All keys restored, agent can now encrypt/decrypt
```

This enables agents to maintain cryptographic identities across:
- Browser restarts
- Incognito/private browsing sessions
- Different physical machines
- Cloud-based agent deployments

**When to use the web interface:**
- CLI can't be installed (no Go/Rust, restricted environment, sandboxed IDE)
- No shell access (browser-only agent, web-based coding environment)
- One-off encryption/decryption tasks
- Testing SAFE format without installing dependencies
- Quick key generation or format exploration

**When to prefer the CLI:**
- Production systems or automated pipelines
- Batch or high-volume operations (CLI is significantly faster)
- Air-gapped or offline environments
- Scripting with shell pipes and file I/O

## Quick Reference

### Key Storage Convention

Personal keys are stored in `~/.safe/` (similar to `~/.ssh/`). The CLI manages this directory automatically:

```bash
safe keygen x25519                     # Generates keypair, auto-stores to ~/.safe/
safe keygen x25519 -n alice            # Named identity "alice"
safe keys                              # List all identities and recipients
```

**Key Discovery Order (SAFE CLI v2.3+):**
1. `~/.safe/keys/*.key` - SAFE-native keys (checked first)
2. `~/.ssh/*` - All SSH private keys in `~/.ssh/` directory
   - Ed25519 keys → auto-converted to X25519
   - P-256 ECDSA keys → used directly

**Note:** You can use EITHER format - SSH keys from GitHub work with zero configuration!

Directory structure (auto-created by `safe keygen`):
- `~/.safe/keys/` — Private keys (0700, never share). E.g., `nick.x25519.key`
- `~/.safe/*.pub` — Your own public keys (safe to share). E.g., `nick.x25519.pub`
- `~/.safe/recipients/` — Other people's public keys (managed by `safe keys add`)

Override with `SAFE_HOME` env var. Fallback: `./.safe/` in current directory.

### Generate Keys

| Key Type | Command | Use Case |
|----------|---------|----------|
| x25519 | `safe keygen x25519` | Fast, default, widely supported |
| p-256 | `safe keygen p-256` | FIPS compliance |
| ml-kem-768 | `safe keygen ml-kem-768` | Post-quantum security (seed by default) |

By default, keygen uses `$USER` as the identity name and stores keys in `~/.safe/`. Override with `-n name` or `-o path`.

```bash
safe keygen x25519                     # ~/.safe/keys/$USER.x25519.key + ~/.safe/$USER.x25519.pub
safe keygen x25519 -n alice            # ~/.safe/keys/alice.x25519.key + ~/.safe/alice.x25519.pub
safe keygen ml-kem-768                 # Generates seed (compact format, default for ML-KEM)
safe keygen ml-kem-768 -no-seed        # Raw keypair instead of seed
safe keygen x25519 -o /tmp/throwaway   # Custom output path
safe keygen x25519 -force              # Overwrite existing files
```

Output: `<name>.<type>.pub` (share this) and `<name>.<type>.key` (keep secret). Public key is always written to `~/.safe/`.

### Manage Keys

```bash
# List all identities and known recipients
safe keys

# Import a recipient's public key
safe keys add alice.x25519.pub --name alice

# Remove a recipient
safe keys remove alice

# Derive public key from private key (by name or path)
safe pubkey alice                       # Looks up ~/.safe/keys/alice.*.key
safe pubkey /path/to/key.key            # Direct file path

# View key details
safe keyinfo alice.x25519.pub
```

Bare names work as recipients after import: `safe encrypt data.txt -r alice` resolves from `~/.safe/recipients/`. Also resolves system users: `-r bob` checks `~bob/.safe/*.pub`.

### Encrypt

stdin is the default input, stdout is the default output. Positional argument sets input file.

```bash
# Password-protect a file
safe encrypt secrets.txt -o secrets.safe -p "strong-password"

# Encrypt to recipient (bare name or key file)
safe encrypt file.txt -o file.safe -r alice

# Multiple recipients (OR - any one can decrypt)
safe encrypt file.txt -o file.safe -r alice -r bob

# Two-factor: password AND key required (+ is AND separator)
safe encrypt file.txt -o file.safe -r "pwd:secret + alice.pub"

# Pipe from stdin (default)
echo "secret" | safe encrypt -p "pw" > msg.safe

# Password from environment variable
safe encrypt file.txt -o file.safe -p env:MY_PASSWORD

# PBKDF2 instead of argon2id
safe encrypt file.txt -o file.safe -p "pw" --kdf pbkdf2
```

### Decrypt

stdin is the default input, stdout is the default output. If no credentials are provided, keys from `~/.safe/keys/` are tried automatically.

```bash
# With password
safe decrypt file.safe -p "password"

# With private key
safe decrypt file.safe -k alice.x25519.key

# Auto-discover keys (no -k needed if keys are in ~/.safe/keys/)
safe decrypt file.safe

# age-compatible --identity flag
safe decrypt file.safe --identity alice.key

# Two-factor (all credentials required)
safe decrypt file.safe -o file.txt -p "secret" -k alice.key

# Write to file instead of stdout
safe decrypt file.safe -o plaintext.txt -p "password"

# Password from environment variable
safe decrypt file.safe -p env:MY_PASSWORD
```

### Info

Inspect a SAFE file's metadata without credentials:

```bash
safe info file.safe
# Output:
#   AEAD: aes-256-gcm
#   Block Size: 65536
#   Key Hash: spki-sha256-16
#   Data size: 1048 bytes
#   UNLOCK Blocks: 2
#     [0] pwd(argon2id)
#     [1] hpke(kem=x25519, id=r3YlsKxQHj1q1d/kKi5e3Q==)

# From stdin
cat file.safe | safe info
```

### Piping (stdin/stdout)

stdin and stdout are the defaults — no `-i -` or `-o -` needed. All operations are binary-safe.

**Default behavior:** Always prefer piping over writing intermediate files to disk. This avoids leaving decrypted content on disk and is cleaner.

```bash
# Decrypt base64-encoded content (PREFERRED - no temp file)
echo "LS0tLS1CRUdJTi..." | base64 -d | safe decrypt -k ~/.safe/keys/id.x25519.key

# AVOID: Writing intermediate files
# echo "LS0tLS1CRUdJTi..." | base64 -d > /tmp/file.safe && safe decrypt /tmp/file.safe ...

# Basic stdin/stdout
echo "secret" | safe encrypt -p "pw" > encrypted.safe
cat encrypted.safe | safe decrypt -p "pw"

# Chain operations (re-encrypt with different key)
safe decrypt a.safe -p "pw1" | safe encrypt -o b.safe -p "pw2"

# Encrypt with compression
tar cz src/ | safe encrypt -o backup.safe -r alice

# Decrypt and decompress
safe decrypt backup.safe -k team.key | tar xz

# Decrypt remote file
curl -s https://example.com/data.safe | safe decrypt -k my.key

# Pipe through compression then encrypt
safe encrypt -p "pw" < large.bin | gzip > encrypted.safe.gz

# Decrypt gzipped safe file
gunzip -c encrypted.safe.gz | safe decrypt -p "pw" > large.bin
```

**Note:** `-i -` and `-o -` still work for explicit stdin/stdout but are no longer required.

## Common Use Cases

### Protect API Keys / .env Files

```bash
safe encrypt .env -o .env.safe -p "dev-password"
safe encrypt credentials.json -o credentials.safe -r ops-team
```

### Share Secrets with a Teammate

```bash
# They generate their key
safe keygen x25519 -n teammate

# You import their public key
safe keys add teammate.x25519.pub --name teammate

# You encrypt for them (bare name!)
safe encrypt api-keys.txt -o api-keys.safe -r teammate

# They decrypt (auto-discovers keys from ~/.safe/keys/)
safe decrypt api-keys.safe -o api-keys.txt
```

### Encrypt Backup Before Cloud Upload

```bash
tar czf backup.tar.gz ~/Documents
safe encrypt backup.tar.gz -o backup.safe -p "backup-phrase" -r recovery
# Upload backup.safe to S3/GCS/Dropbox
```

### Encrypt Entire Directories

```bash
# Encrypt a folder
tar cz project/ | safe encrypt -o project.safe -r team

# Decrypt and extract
safe decrypt project.safe -k team.key | tar xz
```

### Git-Friendly Encrypted Secrets

```bash
# Encrypt secrets, commit the .safe file
safe encrypt .env.production -o .env.production.safe -r deploy
git add .env.production.safe  # Safe to commit

# On deploy server (auto-discovers deploy key from ~/.safe/keys/)
safe decrypt .env.production.safe -o .env.production
```

### Separation of Duties (Two People Required)

```bash
# Encrypt requiring BOTH Alice and Bob (+ is AND)
safe encrypt codes.txt -o codes.safe -r "alice.pub + bob.pub"

# Decrypt (both must provide keys)
safe decrypt codes.safe -o codes.txt -k alice.key -k bob.key
```

### Two-Factor Encryption (Password + Key)

```bash
# Encrypt: requires password AND key
safe encrypt secrets.txt -o secrets.safe -r "pwd:mypassword + hardware.pub"

# Decrypt: must provide both
safe decrypt secrets.safe -o secrets.txt -p "mypassword" -k hardware.key
```

### Team Encryption + Emergency Backup

```bash
safe encrypt secrets.txt -o secrets.safe \
  -r alice -r bob -r carol \
  -p "emergency-recovery-phrase"
```

### Post-Quantum Hybrid Protection

```bash
# Generate both classical and PQ keys
safe keygen x25519 -n alice
safe keygen ml-kem-768 -n alice

# Encrypt with both (future-proof against quantum computers)
safe encrypt data.txt -o data.safe \
  -r "pwd:phrase + alice.x25519.pub + alice.ml-kem-768.pub"
```

### Temporary Decryption (No File on Disk)

```bash
# Use decrypted content without writing to disk
./my-app --config <(safe decrypt config.safe -p "pw")

# Compare two encrypted files
diff <(safe decrypt old.safe -p pw) <(safe decrypt new.safe -p pw)
```

### Password Rotation

```bash
# Change password without re-encrypting data
safe unlock replace secrets.safe -p "old-password" \
  --index 0 --recipient "pwd:new-password"
```

### Key Rotation (Compromised Key)

```bash
# View current recipients
safe info secrets.safe

# Remove compromised key, add new one
safe unlock remove secrets.safe -k admin.key --index 2
safe unlock add secrets.safe -k admin.key --recipient new-employee.pub
```

## Composable Paths (AND vs OR Logic)

| Encrypt With | Decrypt Requires | Logic |
|--------------|------------------|-------|
| `-r alice -r bob` | `-k alice.key` OR `-k bob.key` | OR |
| `-r "alice.pub + bob.pub"` | `-k alice.key` AND `-k bob.key` | AND |
| `-r "pwd:x + alice.pub"` | `-p x` AND `-k alice.key` | AND |
| `-p backup -r alice` | `-p backup` OR `-k alice.key` | OR |

Multiple `-r` or `-p` flags = OR (any one works)
`+` within one `-r` = AND (all required)

**Note:** `->` is deprecated but still works. Use `+` for new code.

## Editing Encrypted Files

SAFE supports random-access editing without full re-encryption. Only modified chunks are re-encrypted - unchanged chunks are copied byte-for-byte.

### Data Input Options

| Option | Use | Example |
|--------|-----|---------|
| `--data "string"` | Literal text on command line | `--data "hello"` |
| `--data-file path` | Read content from a file | `--data-file patch.bin` |

### Read Bytes at Offset

Read a portion of an encrypted file without decrypting the whole thing:

```bash
# Read first 100 bytes
safe read file.safe -p "pw" --offset 0 --length 100

# Read bytes 500-600 to a file
safe read file.safe -o excerpt.txt -k key.key --offset 500 --length 100

# Shorthand with -n for offset
safe read file.safe -p "pw" -n 1024 --length 256

# age-compatible --identity flag
safe read file.safe --identity key.key -n 0 --length 100
```

### Write Bytes at Offset (In-Place Edit)

Modify bytes at a specific position. In-place by default (no `-o` needed):

```bash
# Overwrite bytes starting at offset 10
safe write file.safe -p "pw" -n 10 --data "new content"

# Replace header from a file
safe write config.safe -p "pw" -n 0 --data-file header.bin

# With --identity flag
safe write file.safe --identity key.key -n 0 --data "UPDATED"
```

**Note:** Write only supports in-place modification. Output defaults to overwriting the input file.

### Append Data

Add data to the end of an encrypted file (in-place by default):

```bash
# Append log entry
safe append log.safe -p "pw" --data "$(date): Event occurred\n"

# Append from file
safe append data.safe -k key.key --data-file new-records.csv

# Append binary data
safe append archive.safe -p "pw" --data-file chunk.bin
```

### In-Place Editing Workflow

```bash
# 1. Check current content
safe read config.safe -p "pw" -n 0 --length 50

# 2. Make targeted edit
safe write config.safe -p "pw" -n 25 --data "new_value"

# 3. Verify the change
safe read config.safe -p "pw" -n 0 --length 50
```

## Managing Recipients (UNLOCK Blocks)

Modify who can decrypt without re-encrypting the data. These operations only change the UNLOCK blocks — the encrypted DATA remains identical.

```bash
# View current recipients and their indexes
safe info file.safe
# Shows: [0] pwd(argon2id)
#        [1] hpke(kem=x25519, id=ABC123...)

# Add new recipient (in-place by default)
safe unlock add file.safe -p "current-pw" -r alice.pub
safe unlock add file.safe -k admin.key -r "pwd:backup-pass"

# Add composable recipient (password + key required)
safe unlock add file.safe -p "pw" -r "pwd:secret + bob.pub"

# Remove recipient by index (in-place)
safe unlock remove file.safe -k admin.key --index 0

# Replace recipient at index (in-place)
safe unlock replace file.safe -p "old-pw" --index 0 -r "pwd:new-pw"

# Write to new file instead of in-place
safe unlock add file.safe -o new-file.safe -p "pw" -r alice.pub

# With --identity flag
safe unlock add file.safe --identity admin.key -r bob.pub
```

**Note:** You cannot remove the last UNLOCK block — the file would become undecryptable.

## Algorithm Options

### AEAD (Content Encryption)

| Algorithm | Flag | Use Case |
|-----------|------|----------|
| AES-256-GCM | `--aead aes-256-gcm` | Default, hardware accelerated |
| ChaCha20-Poly1305 | `--aead chacha20-poly1305` | ARM, older CPUs without AES-NI |
| AEGIS-256 | `--aead aegis-256` | **CLI only** - Key-committing, highest security. Not available in browser UI. |

### Key Types

| Type | Security | Size (pub/priv) |
|------|----------|-----------------|
| x25519 | Classical, fast | 32B / 32B |
| p-256 | FIPS compliant | 65B / 32B |
| ml-kem-768 | Post-quantum | 1184B / 2400B |

### Key ID Modes

Control how much key identity information is included in UNLOCK blocks:

| Mode | Flag | Behavior |
|------|------|----------|
| Full | `--key-id-mode full` | Default. Full key ID included — recipients can check if a message is for them without attempting decryption |
| Hint | `--key-id-mode hint` | 4-digit hint only — reduces metadata, recipients may need to try decryption |
| Anonymous | `--key-id-mode anonymous` | No key ID — recipient must try all their keys. Maximum privacy |

```bash
# Encrypt with hint-only key ID
safe encrypt file.txt -o file.safe -r alice --key-id-mode hint

# Encrypt with no key ID (anonymous recipient)
safe encrypt file.txt -o file.safe -r alice --key-id-mode anonymous
```

Use `hint` or `anonymous` when you want to hide *who* can decrypt a message. The encrypted data is identical — only the metadata changes.

### Password KDF

| Algorithm | Flag | Use Case |
|-----------|------|----------|
| Argon2id | `--kdf argon2id` | Default. Memory-hard, GPU-resistant (64 MiB, 2 iterations) |
| PBKDF2 | `--kdf pbkdf2` | Constrained environments (600,000 iterations) |

```bash
safe encrypt file.txt -o file.safe -p "pw" --kdf pbkdf2
```

### Key Hash Algorithm

| Algorithm | Flag | Use Case |
|-----------|------|----------|
| SPKI-SHA256-16 | `--key-hash spki-sha256-16` | Default. 16-byte truncated SHA-256 |
| SPKI-TurboSHAKE256 | `--key-hash spki-turboshake256` | Alternative hash function |

```bash
safe encrypt file.txt -o file.safe -r alice --key-hash spki-turboshake256
```

## Migration from GPG/PGP

```bash
# Decrypt old GPG file, re-encrypt with SAFE
gpg -d old-secrets.gpg | safe encrypt -o secrets.safe -r newkey
```

## Edge Cases & Tips

**Empty files:** Encrypting empty files works correctly and produces valid .safe output.

**Binary data:** SAFE handles all byte values (0x00-0xFF) correctly. No text encoding issues.

**Unicode passwords:** Passwords are UTF-8 encoded. Multi-byte characters work correctly.

**Large files:** Files are encrypted in 64KB chunks by default. Only modified chunks are re-encrypted during edits.

**Block size options:** Use `--block-size` flag (16384, 32768, or 65536 bytes) to tune for your use case.

## Troubleshooting

**Decryption fails:**
1. Check password/key is correct
2. For composable paths, ALL credentials must be provided (partial won't work)
3. Verify file integrity: `safe info file.safe`
4. Wrong key type? Check with `safe keyinfo mykey.key`
5. Check available keys: `safe keys`

**"safe: command not found":**
Run installation steps above. Verify with `which safe`.

**Composable path errors:**
- `pwd:secret + alice.pub` requires BOTH `-p secret` AND `-k alice.key` to decrypt
- Providing only the password or only the key will fail
- Order of `-k` flags doesn't matter, but all must be present

## Security Notes

- `.key` files are secret — never share them
- `.pub` files are safe to distribute
- Composable paths (`+`) provide defense-in-depth
- ML-KEM-768 protects against future quantum computers
- Argon2id password hashing is memory-hard and GPU-resistant (64 MiB memory, 2 iterations)

### Password Security

**Warning:** Passwords passed via `-p` are visible in shell history and process listings.

Mitigations:
```bash
# 1. Prefix with space to skip history (bash/zsh with HISTCONTROL=ignorespace)
 safe encrypt file.txt -o file.safe -p "secret"

# 2. Use a key file instead of password
safe encrypt file.txt -o file.safe -r alice

# 3. Read password from environment variable (RECOMMENDED for automation)
MY_PW="secret" safe encrypt file.txt -o file.safe -p env:MY_PW

# 4. Use SAFE_PASSPHRASE env var with bare -p
export SAFE_PASSPHRASE="secret"
safe encrypt file.txt -o file.safe -p

# 5. Read password from file (careful with permissions)
safe encrypt file.txt -o file.safe -p "$(cat ~/.safe/.password)"

# 6. Clear history after use
history -d $(history 1 | awk '{print $1}')
```

**`env:VARNAME` security:** Environment variables are visible to the current process and child processes. They're safer than command-line args (not in `/proc/*/cmdline`) but still visible via `/proc/*/environ` on Linux. For maximum security, use key-based encryption.

## Agent-to-Agent Encrypted Communication

Agents can exchange encrypted messages across any text-based channel: email, forums, GitHub issues, Slack, shared files, etc.

The key management system makes agent-to-agent communication simple:
- **`safe keygen`** — generates identity keys (auto-stored in `~/.safe/`)
- **`safe keys add`** — imports other agents' public keys as named recipients
- **`safe encrypt -r name`** — encrypts to any known recipient by name
- **`safe decrypt`** — auto-discovers keys, no `-k` flag needed

### First-Run Setup

On first use, check for existing keys and generate if missing:

```bash
# Check if any agent identities exist
safe keys 2>/dev/null || true

# Generate if missing
if [ ! -f ~/.safe/keys/*.key ]; then
    safe keygen x25519
    echo "Generated new agent identity"
    safe keys
fi
```

This creates:
- `~/.safe/keys/$USER.x25519.key` — your private key (never share)
- `~/.safe/$USER.x25519.pub` — your public key (share freely)

### Exchanging Keys Between Agents

Agents discover each other by sharing public keys. The `safe keys add` command imports keys into the recipients directory:

```bash
# Agent A: Share your public key
cat ~/.safe/$USER.x25519.pub
# Copy this to the other agent (paste, file, AGENTS.md, etc.)

# Agent B: Import Agent A's public key
safe keys add /path/to/agent-a.x25519.pub --name agent-a

# Verify import
safe keys
# Shows:
#   Identities:
#     nick         x25519         /Users/nick/.safe/keys/nick.x25519.key
#   Recipients:
#     agent-a      x25519         /Users/nick/.safe/recipients/agent-a.x25519.pub

# Now Agent B can encrypt to Agent A by name
safe encrypt message.txt -o message.safe -r agent-a
```

**Advertising your keys directory:** Agents should make their `~/.safe/*.pub` files discoverable. Common approaches:

| Location | How |
|----------|-----|
| `AGENTS.md` in repo | Include PEM block in markdown |
| `~/.safe/*.pub` files | Other agents on same system: `-r username` resolves `~username/.safe/*.pub` |
| GitHub gist | Post PEM key, recipient imports with `curl \| safe keys add` |
| Forum/email signature | Include PEM block or link to public key |

### Convention: Reply-To Keys

To enable replies, prepend your public key(s) to the message before encrypting:

```
-----BEGIN X25519 PUBLIC KEY-----
fBhEEEB+CepxNQIfPtxnIhWbDUyo+Z/W17cYKlCbsDg=
-----END X25519 PUBLIC KEY-----

Here is the secret data you requested...
```

When an agent decrypts a message and finds PEM public key blocks at the top, it saves them with `safe keys add` and encrypts the reply to that name.

**Multiple reply-to keys:** If the sender wants multiple agents/identities to decrypt the reply:

```
-----BEGIN X25519 PUBLIC KEY-----
fBhEEEB+CepxNQIfPtxnIhWbDUyo+Z/W17cYKlCbsDg=
-----END X25519 PUBLIC KEY-----
-----BEGIN ML-KEM-768 PUBLIC KEY-----
<base64...>
-----END ML-KEM-768 PUBLIC KEY-----

Message body here...
```

The receiving agent extracts all key blocks, imports them with `safe keys add`, and encrypts the reply to all of them.

### Workflow: Send a Message

```bash
# 1. Create message with your public key as reply address
safe pubkey $USER > message.txt
echo "" >> message.txt
echo "Here are the API credentials you requested..." >> message.txt

# 2. Encrypt to recipient (bare name from recipients dir)
safe encrypt message.txt -o message.safe -r recipient

# 3. Share message.safe via any channel (email, forum, git, shared folder, etc.)
```

### Checking if a Message is For You

Before attempting to decrypt, check if your key ID matches any unlock block:

```bash
# Get Key IDs from the encrypted file
safe info message.safe
# Output includes:
#   UNLOCK Blocks: 2
#   [0] hpke(kem=x25519, id=1SB5W2LJ8/DNu8rn+vaGHA==)
#   [1] hpke(kem=ml-kem-768, id=abc123...)

# Get your key info
safe keyinfo ~/.safe/$USER.x25519.pub

# Or just try to decrypt — auto-key discovery handles it
safe decrypt message.safe -o message.txt
```

**Note on key ID modes:** If the sender used `--key-id-mode hint`, you'll see `hint=XXXX` instead of a full ID. If they used `--key-id-mode anonymous`, there will be no key ID at all — you'll need to try decrypting (auto-discovery handles this).

### Workflow: Receive and Reply

```bash
# 1. Decrypt the message (auto-discovers keys from ~/.safe/keys/)
safe decrypt message.safe -o message.txt

# 2. Extract reply-to keys and import them
# Save PEM blocks to a temp file, then import:
grep -A2 'BEGIN.*PUBLIC KEY' message.txt > /tmp/sender.pub
safe keys add /tmp/sender.pub --name sender

# 3. Create and encrypt reply
safe pubkey $USER > reply.txt
echo "" >> reply.txt
echo "Thanks, here's my response..." >> reply.txt

# Encrypt to sender (bare name!)
safe encrypt reply.txt -o reply.safe -r sender
```

### Publishing Your Public Key

Share your public key so others can send you encrypted messages:

| Location | Use Case |
|----------|----------|
| `AGENTS.md` in repo | Project-specific agent identity |
| GitHub profile / gist | Personal agent key |
| Forum signature | Community communication |
| Shared team folder | Internal team use |
| Email signature | Email-based exchange |

Example `AGENTS.md`:

```markdown
## Agent Keys

### Deploy Agent
\`\`\`
-----BEGIN X25519 PUBLIC KEY-----
fBhEEEB+CepxNQIfPtxnIhWbDUyo+Z/W17cYKlCbsDg=
-----END X25519 PUBLIC KEY-----
\`\`\`

To send encrypted data to this agent:
\`\`\`bash
# Import the key
safe keys add deploy-agent.pub --name deploy

# Encrypt
safe encrypt data.txt -o data.safe -r deploy
\`\`\`
```

### Handling Multiple Identities

Agents may have different keys for different contexts:

```bash
safe keygen x25519 -n personal     # ~/.safe/keys/personal.x25519.key
safe keygen x25519 -n work         # ~/.safe/keys/work.x25519.key
safe keygen ml-kem-768 -n pq       # ~/.safe/keys/pq.ml-kem-768.key

# List all
safe keys
```

When sending, choose the appropriate reply-to key for the context. When receiving, auto-discovery tries all keys in `~/.safe/keys/`.

### Error Handling

If decryption fails even though key ID matched:
1. The file may be corrupted — check with `safe info file.safe`
2. For composable paths, ALL required credentials must be provided
3. Report the error clearly; don't silently fail

### Checking All Identities

With auto-key discovery, this is usually unnecessary. But for manual checking:

```bash
# List all your identities
safe keys

# Check message recipients
safe info message.safe

# Just try to decrypt — auto-discovers all keys
safe decrypt message.safe -o message.txt
# If successful, prints: "safe: trying N key(s) from ~/.safe/keys"
```

### Auto-Generate AGENTS.md

When setting up a project for agent communication, create an AGENTS.md:

```bash
# Generate AGENTS.md for current project
cat > AGENTS.md << 'EOF'
# Agent Keys

This project supports encrypted agent-to-agent communication using [SAFE](https://github.com/grittygrease/safe).

## Available Agents

### Primary Agent
EOF

# Add the public key
echo '```' >> AGENTS.md
safe pubkey $USER >> AGENTS.md
echo '```' >> AGENTS.md

cat >> AGENTS.md << 'EOF'

## How to Send Encrypted Messages

1. Save the public key block above to a file and import it:
   ```bash
   safe keys add agent.pub --name agent
   ```
2. Create your message with your reply-to key:
   ```bash
   safe pubkey $USER > message.txt
   echo "" >> message.txt
   echo "Your message here..." >> message.txt
   ```
3. Encrypt and send:
   ```bash
   safe encrypt message.txt -o message.safe -r agent
   ```
4. Share `message.safe` via any channel (email, issue, PR, pastebin, etc.)

## Verifying Messages

```bash
# Check message recipients
safe info message.safe

# Decrypt (auto-discovers keys from ~/.safe/keys/)
safe decrypt message.safe -o message.txt
```
EOF

echo "Created AGENTS.md with your public key"
```

### Sharing via Pastebin

For quick, ephemeral encrypted message sharing:

```bash
# Encrypt and post to termbin
safe encrypt message.txt -r recipient | nc termbin.com 9999
# Returns URL like: https://termbin.com/abc123

# Recipient fetches and decrypts (auto-discovers keys)
curl -s https://termbin.com/abc123 | safe decrypt
```

### Posting a Public Message (Forum/Mailing List)

When posting an encrypted message publicly, include your reply-to key AND instructions:

```bash
# Create a complete public post
cat > post.txt << 'EOF'
## Encrypted Message

To decrypt this message and reply, install the safe-encryption skill:

```
mkdir -p ~/.claude/skills
git clone https://github.com/grittygrease/safe-encryption-skill.git ~/.claude/skills/safe-encryption
```

Then ask your agent: "Decrypt the message below and reply encrypted to the sender"

### My Public Key (for replies)
EOF

safe pubkey $USER >> post.txt

cat >> post.txt << 'EOF'

### Encrypted Message
EOF

# Encrypt your message (with your reply-to key embedded in plaintext)
safe pubkey $USER > message.txt
echo "" >> message.txt
echo "Your actual message content here..." >> message.txt

safe encrypt message.txt -r recipient >> post.txt

echo "" >> post.txt
cat >> post.txt << 'EOF'

---
*This message was encrypted with [SAFE](https://github.com/grittygrease/safe)*
EOF

cat post.txt
```

This produces a self-contained post that any agent with the skill can decrypt and reply to.
