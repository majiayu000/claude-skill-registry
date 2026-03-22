---
name: code-server-remote-ide-wsl2
description: Setup secure VS Code IDE in browser with code-server on WSL2, accessible from mobile/tablet via ngrok/Cloudflare/Tailscale. Full IDE features with extension support, resource management, and performance optimization. Use when you need remote IDE access, VS Code in browser, remote development, or full coding environment on mobile/tablet.
---

# code-server Remote IDE for WSL2

Access full VS Code IDE from any device (phone, tablet, remote computer) via secure web-based code-server with ngrok, Cloudflare Tunnel, or Tailscale.

## Overview

**What This Skill Does**:
- Sets up code-server (VS Code in browser) on WSL2
- Configures secure authentication (prevents CVE-2023-26114)
- Establishes encrypted tunnel (ngrok/Cloudflare/Tailscale)
- Manages VS Code extensions
- Optimizes WSL2 resources (memory/CPU limits)
- Provides one-command start/stop/status operations
- Automatically displays connection URL and credentials

**When to Use This Skill**:
- Need full IDE functionality remotely
- Coding from tablet with keyboard
- Want IntelliSense, debugging, extensions
- Serious development work while traveling
- Review/edit large codebases remotely

**When NOT to Use This Skill**:
- Just need quick terminal commands → Use ttyd-remote-terminal-wsl2 instead
- Need desktop VS Code features not in browser version
- Limited system resources (<4GB RAM)
- Very slow internet connection

**What You'll Get**:
- Full VS Code IDE in browser
- Extension support (most VS Code extensions work)
- IntelliSense, debugging, git integration
- Integrated terminal
- File explorer, search, multi-file editing
- Secure HTTPS access with authentication
- Resource usage monitoring

---

## Prerequisites

**System Requirements**:
- WSL2 installed and working (Ubuntu 22.04 LTS recommended)
- Windows 10 version 2004+ or Windows 11
- **Minimum**: 4GB RAM, 2 CPU cores, 2GB disk space
- **Recommended**: 8GB+ RAM, 4+ CPU cores, 5GB+ disk space
- Internet connection

**User Requirements**:
- Comfortable with VS Code (desktop version)
- Basic command line knowledge
- Comfortable running bash scripts
- Can create free account on tunnel service

**Not Required**:
- Advanced networking knowledge
- systemd expertise
- Extension development knowledge
- Security expertise (skill provides secure defaults)

---

## Quick Start

Get remote VS Code IDE access in <15 minutes:

### 1. Install
```bash
cd ~/.claude/skills/code-server-remote-ide-wsl2/scripts
./install.sh
```

Follow prompts to:
- Install code-server
- Choose tunnel service (ngrok recommended for beginners)
- Install chosen tunnel tool

### 2. Configure Authentication
```bash
./configure-auth.sh
```

This generates a strong hashed password and configures secure access.

### 3. Configure Resources (Recommended)
```bash
./configure-resources.sh
```

This sets WSL2 memory/CPU limits to prevent resource exhaustion.

### 4. Start Session
```bash
./code-server-start.sh
```

This will:
- Start code-server with authentication
- Start tunnel
- Display connection URL and password

**Copy the URL and open in any browser (tablet, phone, computer)**

### 5. Connect & Code
Open the displayed URL in browser → Enter password → You now have full VS Code IDE!

### 6. Stop Session (When Done)
```bash
./code-server-stop.sh
```

**Done! You now have working remote IDE access.**

For detailed setup, extension management, and optimization, see the full workflow below.

---

## Workflow

### Step 1: One-Time Setup

This step installs code-server and your chosen tunnel service. You only need to do this once.

#### 1.1 Run the Installer

```bash
cd ~/.claude/skills/code-server-remote-ide-wsl2/scripts
./install.sh
```

The installer will:
1. **Check for existing installations** (code-server, tunnel tools)
2. **Install code-server** via official script (or manual if fails)
3. **Ask you to choose tunnel service**:
   - **ngrok** (recommended for beginners): 1GB/month free, ephemeral URLs
   - **Cloudflare Tunnel** (recommended for production): Unlimited bandwidth, persistent URLs
   - **Tailscale** (recommended for private access): Private VPN, no public exposure
4. **Install chosen tunnel service**
5. **Verify installations successful**
6. **Check WSL2 version and resources**

#### 1.2 Choose Your Tunnel Service

**ngrok** - Best for beginners:
- ✅ Easiest to setup
- ✅ Free tier: 1GB/month bandwidth
- ⚠️ URLs change on each restart
- ⚠️ Data limits (IDE uses more data than terminal)

**Cloudflare Tunnel** - Best for production:
- ✅ Unlimited bandwidth (free)
- ✅ Persistent URLs (don't change)
- ✅ Better performance
- ⚠️ Slightly more complex setup

**Tailscale** - Best for private access:
- ✅ Private network (not exposed to internet)
- ✅ Unlimited bandwidth
- ✅ No public URL (only accessible to your Tailscale network)
- ⚠️ Requires Tailscale on connecting device

**Recommendation**: Start with **Cloudflare Tunnel** (unlimited bandwidth important for IDE).

#### 1.3 Get Tunnel Authentication Token

After choosing tunnel service, you'll need to create free account and get auth token:

**For ngrok**:
1. Go to https://dashboard.ngrok.com/signup
2. Sign up (free)
3. Copy your authtoken from https://dashboard.ngrok.com/get-started/your-authtoken
4. Run: `ngrok config add-authtoken YOUR_TOKEN_HERE`

**For Cloudflare Tunnel**:
1. Go to https://dash.cloudflare.com/
2. Sign up (free)
3. Follow installer prompts (installer will guide you through `cloudflared tunnel login`)

**For Tailscale**:
1. Go to https://login.tailscale.com/start
2. Sign up (free)
3. Run: `sudo tailscale up`
4. Follow authentication link

#### 1.4 Verify Installation

```bash
# Check code-server installed
code-server --version

# Check tunnel tool installed
ngrok version           # or: cloudflared --version  # or: tailscale version

# Run health check
./health-check.sh
```

**Troubleshooting Installation**:
- If code-server install fails, see [Installation Guide](references/installation-guide.md)
- If tunnel install fails, see [Tunneling Options Guide](references/tunneling-options.md)
- For WSL2 issues, see [WSL2 Configuration Guide](references/wsl2-configuration.md)

---

### Step 2: Configure Authentication

Configure secure access with hashed password. You only need to do this once.

#### 2.1 Run Configuration Script

```bash
cd ~/.claude/skills/code-server-remote-ide-wsl2/scripts
./configure-auth.sh
```

This will:
1. **Generate strong password** (16 characters, mixed case, numbers, symbols)
   - Or you can provide your own password
2. **Hash password** (SHA-256 or bcrypt)
3. **Create config.yaml** with hashed password and settings
4. **Set file permissions** (600 - owner read/write only)
5. **Display password** for your records (you'll need it to login)

#### 2.2 Save Your Password

The script will display:
```
==================================================
code-server Remote IDE Credentials
==================================================
Password: aB3$xK9#mL2@pQ7!

Save this password securely!
You'll need it to login to VS Code in browser.

Configuration saved to:
  ~/.config/code-server/config.yaml

==================================================
```

**Save this password** - you'll need it to login from browser.

**Security Notes**:
- Password is **hashed** in config.yaml (more secure than ttyd's plain text)
- Hashed password stored in `~/.config/code-server/config.yaml` with 600 permissions
- Plain password stored in `~/.code-server/.env` (for scripts only)
- Never share your password
- Never commit config files to git
- Change password periodically: Re-run `./configure-auth.sh`

**Troubleshooting Authentication**:
- Forgot password? Re-run `./configure-auth.sh` to generate new one
- Want custom password? Run: `./configure-auth.sh --custom-password`
- For security details, see [Security Guide](references/security-guide.md)

---

### Step 3: Configure Resources (Recommended)

Configure WSL2 resource limits to prevent code-server from consuming all memory.

#### 3.1 Why Resource Configuration Matters

**code-server resource usage**:
- **Base**: ~200MB (no extensions)
- **Light use** (few extensions): ~500MB-1GB
- **Heavy use** (many extensions, large project): 2-4GB

**Without limits**: code-server can consume all available RAM, slowing down Windows.

**With limits**: WSL2 restricted to safe amount, system stays responsive.

#### 3.2 Run Resource Configuration Script

```bash
cd ~/.claude/skills/code-server-remote-ide-wsl2/scripts
./configure-resources.sh
```

This will:
1. **Detect total system memory**
2. **Recommend memory limit** (50-75% of total)
3. **Recommend processor count**
4. **Generate .wslconfig** (Windows file)
5. **Prompt to restart WSL** (required to apply)
6. **Verify new limits** after restart

#### 3.3 Recommended Resource Limits

| System RAM | WSL2 Memory Limit | Processors | code-server Usage |
|------------|-------------------|------------|-------------------|
| 8 GB | 4 GB | 2 | Light use OK |
| 16 GB | 8 GB | 4 | Moderate use OK |
| 32 GB+ | 12-16 GB | 6-8 | Heavy use OK |

**Example .wslconfig**:
```ini
[wsl2]
memory=8GB
processors=4
swap=2GB
```

#### 3.4 Apply Resource Limits

**Restart WSL2** (PowerShell as Admin):
```powershell
wsl --shutdown
```

**Wait 8 seconds**, then start WSL2:
```powershell
wsl
```

**Verify new limits** (in WSL2):
```bash
# Check memory
free -h

# Check CPUs
nproc
```

**Troubleshooting Resources**:
- For resource management details, see [Resource Management Guide](references/resource-management.md)
- For performance optimization, see [Performance Optimization Guide](references/performance-optimization.md)

---

### Step 4: Start Session

Start code-server and tunnel, get connection URL. Do this each time you want remote access.

#### 4.1 Start IDE Session

```bash
cd ~/.claude/skills/code-server-remote-ide-wsl2/scripts
./code-server-start.sh
```

The script will:
1. **Check WSL2 resources available**
2. **Load config** from config.yaml
3. **Start code-server** on localhost:8080 with authentication
4. **Wait for code-server ready** (usually <5 seconds)
5. **Start tunnel** (ngrok/cloudflare/tailscale)
6. **Wait for tunnel connection** (usually <10 seconds)
7. **Extract public URL**
8. **Display connection information** and password
9. **Show resource usage baseline**

#### 4.2 Connection Information Displayed

You'll see output like this:

```
==================================================
code-server Remote IDE - CONNECTION READY
==================================================

🌐 Connection URL:
   https://abc123.ngrok-free.app

🔐 Login Password:
   aB3$xK9#mL2@pQ7!

💻 To connect from tablet/phone/browser:
   1. Open the URL above in any browser
   2. Enter the password above
   3. You'll see full VS Code IDE

📊 Resource Usage (baseline):
   code-server: 245 MB
   Tunnel: 24 MB
   Total: 269 MB

⚠️  Security Warnings:
   - Only share URL with trusted people
   - URL is HTTPS encrypted
   - Session is active until you stop it
   - Remember to stop when done (saves resources)

==================================================
Session running. Press Ctrl+C to stop (or use ./code-server-stop.sh)
```

#### 4.3 Keep Terminal Running

**Option 1**: Keep terminal open (simplest)
- Leave the terminal window running
- code-server and tunnel stay active
- Press Ctrl+C to stop

**Option 2**: Run in background (advanced)
```bash
./code-server-start.sh &
disown
```

Now you can close terminal and code-server keeps running.

**Troubleshooting Start**:
- code-server won't start? Check port 8080 not in use: `lsof -i :8080`
- Tunnel won't connect? Check your auth token configured correctly
- No URL displayed? Check internet connection
- For more help, see [Troubleshooting Guide](references/troubleshooting.md)

---

### Step 5: Connect & Use IDE

Use the connection URL from any device with browser.

#### 5.1 Open URL in Browser

On your tablet, phone, or remote computer:
1. **Open browser** (Chrome recommended for best compatibility)
2. **Enter the connection URL** (from Step 4.2)
3. **Accept any security warnings** (ngrok free tier shows warning page - click "Visit Site")

#### 5.2 Login

You'll see code-server password prompt:
- **Enter the password** from Step 4.2
- Click "Enter" or "Submit"

#### 5.3 Use Full VS Code IDE

You now see full VS Code interface in browser!

**What You Can Do**:
- **File Explorer**: Navigate your project files
- **Editor**: Edit code with syntax highlighting
- **IntelliSense**: Auto-complete, parameter hints
- **Integrated Terminal**: Run commands without switching apps
- **Extensions**: Install VS Code extensions (most work)
- **Git Integration**: Commit, push, pull
- **Debugging**: Set breakpoints, debug code
- **Search**: Find in files, replace across project
- **Multi-file editing**: Split editor, multiple tabs

**First Time Setup**:
1. **Open Folder**: File → Open Folder → Select your project directory
2. **Install Extensions**: See Step 6 below
3. **Configure Settings**: Settings → Preferences (same as desktop VS Code)

#### 5.4 Using on Mobile/Tablet

**Tablet (iPad/Android with keyboard)**:
- Works great for serious coding
- Keyboard shortcuts work
- Mouse/trackpad supported
- Multi-touch gestures

**Phone**:
- Possible but challenging
- Recommend for:
  - Quick edits
  - Code review
  - Running commands in terminal
- Not recommended for:
  - Long coding sessions
  - Complex debugging

**Tips**:
- **Landscape mode** for more screen space
- **Split editor** carefully (small screen)
- **Use terminal** for quick tasks
- **File search** (Ctrl+P) faster than file explorer

#### 5.5 Disconnect

**To disconnect** (without stopping code-server):
- Simply close browser tab
- code-server keeps running (can reconnect anytime using same URL)
- Your work is saved on WSL2

**To fully stop** (free up resources):
- See Step 7 below

---

### Step 6: Manage Extensions & Resources

Manage VS Code extensions and monitor resource usage.

#### 6.1 Install Extensions

**Method 1**: Via UI (easiest)
1. Click Extensions icon (sidebar)
2. Search for extension
3. Click "Install"
4. Wait for installation
5. Reload if prompted

**Method 2**: Via CLI
```bash
# Use our helper script
./manage-extensions.sh

# Or manually:
code-server --install-extension EXTENSION_ID
```

**Popular Extensions**:
- **Python**: `ms-python.python`
- **ESLint**: `dbaeumer.vscode-eslint`
- **Prettier**: `esbenp.prettier-vscode`
- **GitLens**: `eamonn.gitlens`
- **Docker**: `ms-azuretools.vscode-docker`

**Example**:
```bash
# Install Python extension
code-server --install-extension ms-python.python
```

#### 6.2 Extension Compatibility

**Most extensions work**, but some don't:

✅ **Work Well**:
- Language support (Python, JavaScript, TypeScript, Go, Rust, etc.)
- Linters (ESLint, Pylint)
- Formatters (Prettier, Black)
- Git tools (GitLens)
- Themes, icons
- Snippets

⚠️ **May Not Work**:
- Extensions requiring desktop integration
- Extensions needing native modules
- Some debuggers (check extension docs)

**Check compatibility**: See extension's marketplace page for web/remote support.

#### 6.3 Monitor Resource Usage

```bash
# Check current status
./code-server-status.sh
```

This shows:
- code-server memory usage
- Tunnel memory usage
- Total CPU usage
- Session duration
- Number of extensions loaded

**If resource usage high**:
- Remove unused extensions
- Close unused editor tabs
- Restart code-server session

#### 6.4 Manage Extensions Script

```bash
./manage-extensions.sh
```

Interactive menu:
1. List installed extensions
2. Search marketplace
3. Install extension
4. Update all extensions
5. Remove extension
6. Show extension resource impact (if available)

**Example**:
```bash
$ ./manage-extensions.sh
1) List installed
2) Install extension
3) Remove extension
Enter choice: 1

Installed Extensions:
- ms-python.python (Python)
- dbaeumer.vscode-eslint (ESLint)
- esbenp.prettier-vscode (Prettier)
```

**For detailed extension management**, see [Extension Management Guide](references/extension-management.md).

---

### Step 7: Stop Session

Stop code-server and tunnel when you're done. This frees up resources.

#### 7.1 Stop IDE Session

```bash
cd ~/.claude/skills/code-server-remote-ide-wsl2/scripts
./code-server-stop.sh
```

This will:
1. **Find tunnel process** and kill gracefully
2. **Find code-server process** and kill gracefully
3. **Confirm both stopped**
4. **Report final resource usage**
5. **Report session ended**

#### 7.2 Verify Stopped

The script will show:
```
Stopping code-server remote IDE session...
✓ Tunnel stopped
✓ code-server stopped

Final resource usage:
  code-server: 1.2 GB (peak)
  Session duration: 2 hours 15 minutes

Session ended successfully.
```

**Verify Nothing Running**:
```bash
./code-server-status.sh
```

Should show: `code-server is not running`

#### 7.3 Why Stop?

- **Saves resources** (200MB-4GB memory freed)
- **Saves data** (ngrok free tier: 1GB/month limit)
- **Security** (no active tunnel means no way to connect)
- **Best practice** (only run when actively using)

**Troubleshooting Stop**:
- Process won't stop? See running processes: `ps aux | grep code-server`
- Forcefully kill: `pkill -9 code-server && pkill -9 ngrok`

---

### Step 8: Check Status

Check if code-server session is running and get connection info.

#### 8.1 Check Current Status

```bash
cd ~/.claude/skills/code-server-remote-ide-wsl2/scripts
./code-server-status.sh
```

**If Running**, you'll see:
```
==================================================
code-server Remote IDE - STATUS
==================================================

Status: RUNNING ✓

🌐 Connection URL:
   https://abc123.ngrok-free.app

🔐 Login Password:
   aB3$xK9#mL2@pQ7!

⏱️  Session Duration: 1 hour 23 minutes

📊 Resource Usage:
   code-server: 856 MB
   Tunnel: 24 MB
   Total: 880 MB

💻 System Resources:
   WSL2 Memory Limit: 8 GB
   Currently Used: 2.1 GB (26%)
   Available: 5.9 GB

📦 Extensions Loaded: 8

To stop session: ./code-server-stop.sh
==================================================
```

**If Stopped**, you'll see:
```
==================================================
code-server Remote IDE - STATUS
==================================================

Status: NOT RUNNING

To start session: ./code-server-start.sh
==================================================
```

#### 8.2 Use Cases for Status

**Check before starting**: Avoid starting duplicate sessions
```bash
./code-server-status.sh && ./code-server-start.sh
```

**Get URL when you forgot it**: Status shows current URL
```bash
./code-server-status.sh  # Copy URL from output
```

**Monitor resource usage**: See if memory is getting high
```bash
./code-server-status.sh  # Check memory usage
```

**Check if forgotten session running**: See if you left it running
```bash
./code-server-status.sh  # If running, consider stopping
```

---

## Security Essentials

**Security-First Design**:
This skill implements defense-in-depth security to protect your WSL2 development environment.

### Default Security Features

✅ **Authentication Required**
- All connections require password
- Password is hashed (SHA-256 or bcrypt)
- Prevents CVE-2023-26114 (WebSocket origin validation)

✅ **HTTPS Encryption**
- All traffic encrypted via tunnel (ngrok/Cloudflare/Tailscale)
- Prevents eavesdropping
- Browser shows secure padlock

✅ **Localhost Binding**
- code-server binds to 127.0.0.1 only (not 0.0.0.0)
- Cannot be accessed directly from network
- Must go through authenticated tunnel

✅ **Secure Credential Storage**
- Hashed password in config.yaml (600 permissions)
- Plain password in .env for scripts only (600 permissions)
- Not committed to git (.gitignore recommended)

✅ **WebSocket Origin Validation**
- Prevents CSRF attacks
- Mitigates CVE-2023-26114

### Security Best Practices

**Do**:
- ✅ Use strong passwords (default generator creates these)
- ✅ Stop sessions when not in use
- ✅ Keep code-server and tunnel tools updated
- ✅ Only share URLs with trusted people
- ✅ Monitor active sessions (use `./code-server-status.sh`)
- ✅ Review tunnel logs periodically
- ✅ Use WSL2 resource limits (.wslconfig)

**Don't**:
- ❌ Share your password publicly
- ❌ Use weak custom passwords (<12 characters)
- ❌ Leave sessions running indefinitely
- ❌ Expose code-server directly without tunnel
- ❌ Bind to 0.0.0.0 on public networks
- ❌ Disable authentication

### Threat Model

**Protected Against**:
- ✅ Unauthorized access (password required)
- ✅ Eavesdropping (HTTPS encryption)
- ✅ Network scanning (localhost binding)
- ✅ Weak passwords (strong generation)
- ✅ Credential theft from filesystem (600 permissions)
- ✅ WebSocket CSRF (origin validation)

**Not Protected Against** (out of scope):
- ⚠️ Compromised WSL2 system (if system compromised, IDE access is too)
- ⚠️ Malicious code execution (if you run malicious code in terminal)
- ⚠️ Social engineering (sharing password with attacker)
- ⚠️ Browser vulnerabilities (keep browser updated)

### Security Warnings

**⚠️ code-server Has Full Access**:
- Can read/write all files in WSL2
- Can execute commands as your user
- Can access git credentials
- Treat code-server password like SSH key

**⚠️ Extensions Can Execute Code**:
- Extensions run with your privileges
- Only install trusted extensions
- Review extension permissions
- Check extension ratings/reviews

**⚠️ ngrok Free Tier Warning**:
ngrok free tier URLs are public. However:
- URL is random and hard to guess
- Authentication still required (password)
- HTTPS encrypted
- **Recommendation**: Don't share ngrok URLs publicly

### Advanced Security (Optional)

For enhanced security, see [Security Guide](references/security-guide.md):
- OAuth integration (Google/GitHub login)
- IP whitelisting (Cloudflare Tunnel)
- Access logging and monitoring
- Extension security scanning

---

## Performance Tips

### Optimize for Speed

**1. Choose Fast Tunnel**:
- Cloudflare often faster than ngrok
- Tailscale fastest (direct peer connection)

**2. Limit Extensions**:
- Only install extensions you use
- Disable unused extensions
- Remove extensions you don't need

**3. Close Unused Tabs**:
- Each open file uses memory
- Close files when done editing
- Use "Close All" periodically

**4. Optimize Settings**:
```json
{
  "files.watcherExclude": {
    "**/node_modules/**": true,
    "**/.git/objects/**": true
  },
  "search.exclude": {
    "**/node_modules": true,
    "**/bower_components": true
  }
}
```

**5. Use Search Wisely**:
- Use .gitignore to exclude files
- Don't search in node_modules
- Use specific file patterns

### Monitor Performance

```bash
# Check resource usage
./code-server-status.sh

# If high:
# - Remove extensions
# - Close tabs
# - Restart session
```

For detailed optimization, see [Performance Optimization Guide](references/performance-optimization.md).

---

## Troubleshooting Quick Fixes

### code-server Won't Start

**Error**: `code-server: command not found`
**Fix**:
```bash
# Reinstall code-server
./install.sh
```

**Error**: `Address already in use (port 8080)`
**Fix**:
```bash
# Find what's using port
lsof -i :8080

# Kill the process
kill <PID>

# Or use different port
CODE_SERVER_PORT=8081 ./code-server-start.sh
```

### Can't Login (Wrong Password)

**Error**: "Incorrect password" or password doesn't work

**Fix**:
```bash
# Reset password
./configure-auth.sh

# Get new password
./code-server-status.sh
```

### WebSocket Connection Failed

**Error in browser console**: `WebSocket connection failed`

**Fix**:
1. Check code-server running: `./code-server-status.sh`
2. Restart session: `./code-server-stop.sh && ./code-server-start.sh`
3. Try different browser (Chrome recommended)

### High Memory Usage

**Issue**: code-server using >2GB memory

**Fix**:
1. Check extensions: Remove unused
2. Close unused tabs
3. Restart session
4. Configure WSL2 limits: `./configure-resources.sh`

### Extensions Not Loading

**Issue**: Installed extension doesn't appear

**Fix**:
1. Reload window: Command Palette → "Reload Window"
2. Check compatibility (see Extension Management)
3. Check logs: Developer → Toggle Developer Tools → Console

### Slow Performance / Lag

**Issue**: IDE feels sluggish, typing delayed

**Fix**:
1. Check network: `ping 8.8.8.8` (should be <100ms)
2. Try different tunnel (Cloudflare usually faster)
3. Close unused tabs/extensions
4. Check WSL2 resources: `htop`

For more issues, see [Troubleshooting Guide](references/troubleshooting.md).

---

## Reference Guides

Comprehensive guides for deeper understanding:

### Installation & Setup
- **[Installation Guide](references/installation-guide.md)** - Detailed installation for code-server + all tunnel options, version management, verification

### Security
- **[Security Guide](references/security-guide.md)** - CVE-2023-26114 analysis, authentication methods, password hashing, defense in depth

### Extensions
- **[Extension Management Guide](references/extension-management.md)** - Install/update/remove extensions, compatibility, performance impact

### Resources & Performance
- **[Resource Management Guide](references/resource-management.md)** - WSL2 .wslconfig, memory limits, CPU allocation, monitoring
- **[Performance Optimization Guide](references/performance-optimization.md)** - Settings, extension selection, search optimization, monitoring

### Tunneling
- **[Tunneling Options Guide](references/tunneling-options.md)** - Comprehensive comparison of ngrok vs Cloudflare vs Tailscale, setup for each

### Configuration
- **[WSL2 Configuration Guide](references/wsl2-configuration.md)** - .wslconfig examples, systemd support, resource limits

### Troubleshooting
- **[Troubleshooting Guide](references/troubleshooting.md)** - Extensive error catalog, debugging techniques, solutions

---

## Automation Scripts

All automation scripts are in `scripts/` directory:

### Installation
```bash
./install.sh              # Interactive installer for code-server + tunnel
./install.sh --ngrok      # Non-interactive: install with ngrok
./install.sh --cloudflare # Non-interactive: install with Cloudflare
./install.sh --tailscale  # Non-interactive: install with Tailscale
```

### Configuration
```bash
./configure-auth.sh                    # Interactive: generate hashed password
./configure-auth.sh --custom-password  # Interactive: use your password
./configure-resources.sh               # Interactive: configure WSL2 limits
```

### Session Management
```bash
./code-server-start.sh   # Start code-server + tunnel, display URL
./code-server-stop.sh    # Stop both gracefully
./code-server-status.sh  # Check status, show URL + resources
```

### Extension Management
```bash
./manage-extensions.sh   # Interactive extension manager
```

### Health Check
```bash
./health-check.sh  # Verify installation and configuration
```

---

## Templates

Configuration templates for advanced users:

### code-server Configuration
**File**: `templates/config.yaml.template`

Example config.yaml (created automatically by `configure-auth.sh`):
```yaml
bind-addr: 127.0.0.1:8080
auth: password
password: HASHED_PASSWORD_HERE
cert: false
```

### WSL2 Resource Configuration
**File**: `templates/.wslconfig.template`

Example .wslconfig for Windows (created by `configure-resources.sh`):
```ini
[wsl2]
memory=8GB
processors=4
swap=2GB
```

### systemd Service
**File**: `templates/code-server.service`

For auto-start on WSL2 boot (requires systemd support):
```bash
# Copy template
cp templates/code-server.service ~/.config/systemd/user/

# Enable auto-start
systemctl --user enable code-server
systemctl --user start code-server
```

### Environment Variables
**File**: `templates/.env.template`

Example .env configuration (created by `configure-auth.sh`):
```bash
CODE_SERVER_PASSWORD=strongpassword
TUNNEL_TYPE=cloudflare
CLOUDFLARE_TUNNEL_TOKEN=your_token_here
```

---

## Comparison: code-server vs ttyd

**When to use code-server** (this skill):
- ✅ Full IDE functionality needed
- ✅ IntelliSense, debugging, extensions
- ✅ Editing large codebases
- ✅ Long development sessions
- ✅ Tablet with keyboard
- ✅ Serious coding work

**When to use ttyd**:
- Quick command execution
- Lightweight (<50MB vs 200MB-4GB)
- Simple terminal tasks
- Low resource usage acceptable
- Mobile phone (not tablet)

**Can use both**: Install both skills, use ttyd for quick tasks, code-server for serious coding.

---

## Next Steps

**After Setup**:
1. ✅ Test connection from tablet/computer
2. ✅ Install your favorite extensions
3. ✅ Configure settings (same as desktop VS Code)
4. ✅ Open your project folder
5. ✅ Bookmark connection URL
6. ✅ Practice start/stop workflow

**Advanced Setup**:
- Configure systemd auto-start (see templates/)
- Setup Cloudflare Tunnel for persistent URLs
- Optimize WSL2 resources for your workflow
- Configure VS Code settings sync

**Explore More**:
- [Extension Management](references/extension-management.md) - Manage extensions
- [Resource Management](references/resource-management.md) - Optimize resources
- [Performance Optimization](references/performance-optimization.md) - Speed up IDE
- [Security Guide](references/security-guide.md) - Advanced security

---

## Success Checklist

You've successfully setup remote IDE access when:

- [x] code-server installed and verified
- [x] Tunnel service installed (ngrok/Cloudflare/Tailscale)
- [x] Authentication configured (strong hashed password)
- [x] WSL2 resources configured (.wslconfig)
- [x] Can start session (`./code-server-start.sh`)
- [x] Connection URL displayed
- [x] Can access VS Code from browser (tablet/phone/computer)
- [x] Can login with password
- [x] Full VS Code functionality works (edit, IntelliSense, terminal)
- [x] Can install extensions
- [x] Can stop session (`./code-server-stop.sh`)
- [x] Can check status (`./code-server-status.sh`)

**Congratulations! You now have secure remote VS Code IDE access from any device.**

---

**code-server-remote-ide-wsl2** - Full VS Code IDE, anywhere you go.
