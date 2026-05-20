---
name: ttyd-remote-terminal-wsl2
description: Setup secure web-based terminal access to WSL2 from mobile/tablet via ttyd + ngrok/Cloudflare/Tailscale. One-command install, start, stop, status. Use when you need remote terminal access, web terminal, browser-based shell, or mobile access to WSL2 environment.
---

# ttyd Remote Terminal for WSL2

Access your WSL2 terminal from any device (phone, tablet, remote computer) via secure web-based terminal using ttyd with ngrok, Cloudflare Tunnel, or Tailscale.

## Overview

**What This Skill Does**:
- Sets up ttyd (web-based terminal emulator) on WSL2
- Configures secure authentication (prevents CVE-2021-34182)
- Establishes encrypted tunnel (ngrok/Cloudflare/Tailscale)
- Provides one-command start/stop/status operations
- Automatically displays connection URL and credentials

**When to Use This Skill**:
- Need to run commands on WSL2 while away from computer
- Want terminal access from phone/tablet
- Need quick remote access without full IDE
- Occasional remote terminal access (vs permanent SSH setup)

**When NOT to Use This Skill**:
- Need full IDE functionality → Use code-server-remote-ide-wsl2 instead
- Need permanent production remote access → Consider dedicated SSH setup
- Need to access non-WSL2 Linux → This is WSL2-specific

**What You'll Get**:
- Lightweight terminal in browser (<50MB memory)
- Secure HTTPS access with authentication
- Auto-generated connection URLs
- Simple start/stop commands
- Works from any device with browser

---

## Prerequisites

**System Requirements**:
- WSL2 installed and working (Ubuntu 22.04 LTS recommended)
- Windows 10 version 2004+ or Windows 11
- 1GB+ free disk space
- Internet connection

**User Requirements**:
- Basic command line knowledge
- Comfortable running bash scripts
- Can create free account on tunnel service (ngrok/Cloudflare/Tailscale)

**Not Required**:
- Advanced networking knowledge
- systemd expertise
- Security expertise (skill provides secure defaults)

---

## Quick Start

Get remote terminal access in <10 minutes:

### 1. Install
```bash
cd ~/.claude/skills/ttyd-remote-terminal-wsl2/scripts
./install.sh
```

Follow prompts to:
- Install ttyd
- Choose tunnel service (ngrok recommended for beginners)
- Install chosen tunnel tool

### 2. Configure Authentication
```bash
./configure-auth.sh
```

This generates a strong password and configures secure access.

### 3. Start Session
```bash
./ttyd-start.sh
```

This will:
- Start ttyd with authentication
- Start tunnel
- Display connection URL and password

**Copy the URL and open in any browser (phone, tablet, etc.)**

### 4. Connect
Open the displayed URL in browser → Login with displayed password → You now have terminal access!

### 5. Stop Session (When Done)
```bash
./ttyd-stop.sh
```

**Done! You now have working remote terminal access.**

For detailed setup, troubleshooting, and advanced configuration, see the full workflow below.

---

## Workflow

### Step 1: One-Time Setup

This step installs ttyd and your chosen tunnel service. You only need to do this once.

#### 1.1 Run the Installer

```bash
cd ~/.claude/skills/ttyd-remote-terminal-wsl2/scripts
./install.sh
```

The installer will:
1. **Check for existing installations** (ttyd, tunnel tools)
2. **Install ttyd** via apt (or manual if apt fails)
3. **Ask you to choose tunnel service**:
   - **ngrok** (recommended for beginners): 1GB/month free, ephemeral URLs
   - **Cloudflare Tunnel** (recommended for production): Unlimited bandwidth, persistent URLs
   - **Tailscale** (recommended for private access): Private VPN, no public exposure
4. **Install chosen tunnel service**
5. **Verify installations successful**

#### 1.2 Choose Your Tunnel Service

**ngrok** - Best for beginners:
- ✅ Easiest to setup
- ✅ Free tier: 1GB/month bandwidth
- ⚠️ URLs change on each restart
- ⚠️ Data limits (1GB/month free tier)

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

**Recommendation**: Start with **ngrok** (easiest), migrate to **Cloudflare Tunnel** if you need more bandwidth.

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
# Check ttyd installed
ttyd --version

# Check tunnel tool installed
ngrok version           # or: cloudflared --version  # or: tailscale version
```

**Troubleshooting Installation**:
- If ttyd install fails, see [Installation Guide](references/installation-guide.md)
- If tunnel install fails, see [Tunneling Options Guide](references/tunneling-options.md)

---

### Step 2: Configure Authentication

Configure secure access with strong password. You only need to do this once.

#### 2.1 Run Configuration Script

```bash
cd ~/.claude/skills/ttyd-remote-terminal-wsl2/scripts
./configure-auth.sh
```

This will:
1. **Generate strong password** (16 characters, mixed case, numbers, symbols)
   - Or you can provide your own password
2. **Store credentials securely** in `~/.ttyd/.env` with 600 permissions
3. **Display username and password** for your records

#### 2.2 Save Your Credentials

The script will display:
```
==================================================
ttyd Remote Terminal Credentials
==================================================
Username: myusername
Password: aB3$xK9#mL2@pQ7!

Store these credentials securely!
==================================================
```

**Save these credentials** - you'll need them to login from browser.

**Security Notes**:
- Password is stored in `~/.ttyd/.env` with restricted permissions (only you can read)
- Never share your password
- Never commit `.env` file to git
- Change password periodically: Re-run `./configure-auth.sh`

**Troubleshooting Authentication**:
- Forgot password? Re-run `./configure-auth.sh` to generate new one
- Want custom password? Run: `./configure-auth.sh --custom-password`
- For security details, see [Security Guide](references/security-guide.md)

---

### Step 3: Start Session

Start ttyd and tunnel, get connection URL. Do this each time you want remote access.

#### 3.1 Start Terminal Session

```bash
cd ~/.claude/skills/ttyd-remote-terminal-wsl2/scripts
./ttyd-start.sh
```

The script will:
1. **Load credentials** from `~/.ttyd/.env`
2. **Start ttyd** on localhost:7681 with authentication
3. **Start tunnel** (ngrok/cloudflare/tailscale)
4. **Wait for tunnel connection** (usually <10 seconds)
5. **Extract public URL**
6. **Display connection information**

#### 3.2 Connection Information Displayed

You'll see output like this:

```
==================================================
ttyd Remote Terminal - CONNECTION READY
==================================================

🌐 Connection URL:
   https://abc123.ngrok-free.app

🔐 Login Credentials:
   Username: myusername
   Password: aB3$xK9#mL2@pQ7!

📱 To connect from phone/tablet/browser:
   1. Open the URL above in any browser
   2. Login with username and password
   3. You'll see your WSL2 terminal

⚠️  Security Warnings:
   - Only share URL with trusted people
   - URL is HTTPS encrypted
   - Session is active until you stop it
   - Remember to stop when done (saves data)

==================================================
Session running. Press Ctrl+C to stop (or use ./ttyd-stop.sh)
```

#### 3.3 Keep Terminal Running

**Option 1**: Keep terminal open (simplest)
- Leave the terminal window running
- ttyd and tunnel stay active
- Press Ctrl+C to stop

**Option 2**: Run in background (advanced)
```bash
./ttyd-start.sh &
disown
```

Now you can close terminal and ttyd keeps running.

**Troubleshooting Start**:
- ttyd won't start? Check port 7681 not in use: `lsof -i :7681`
- Tunnel won't connect? Check your auth token configured correctly
- No URL displayed? Check internet connection
- For more help, see [Troubleshooting Guide](references/troubleshooting.md)

---

### Step 4: Connect from Remote Device

Use the connection URL from any device with browser.

#### 4.1 Open URL in Browser

On your phone, tablet, or remote computer:
1. **Open browser** (Chrome, Safari, Firefox, etc.)
2. **Enter the connection URL** (from Step 3.2)
3. **Accept any security warnings** (ngrok free tier shows warning page - click "Visit Site")

#### 4.2 Login

You'll see HTTP Basic Auth prompt:
- **Username**: The username from Step 3.2
- **Password**: The password from Step 3.2

Click "Sign In" or "Login"

#### 4.3 Use Terminal

You now see your WSL2 terminal in browser!

**What You Can Do**:
- Run any command you normally run in terminal
- Navigate directories
- Edit files (with vim, nano, etc.)
- Run scripts
- Check logs
- Anything you'd do in regular terminal

**Tips**:
- **Mobile keyboards**: May need to use special keyboard for Ctrl/Tab keys
- **Copy/paste**: Works via browser's copy/paste
- **Performance**: Should feel responsive (<100ms latency on good connection)
- **Timeouts**: Session stays active until you stop it

**Example Commands to Try**:
```bash
# Check you're in WSL2
uname -a

# Navigate your projects
cd ~/projects
ls -la

# Check resource usage
htop

# Run your development commands
npm run dev
python manage.py runserver
```

#### 4.4 Disconnect

**To disconnect** (without stopping ttyd):
- Simply close browser tab
- ttyd keeps running (can reconnect anytime using same URL)

**To fully stop** (free up resources, data usage):
- See Step 5 below

---

### Step 5: Stop Session

Stop ttyd and tunnel when you're done. This frees up resources and saves data (ngrok).

#### 5.1 Stop Terminal Session

```bash
cd ~/.claude/skills/ttyd-remote-terminal-wsl2/scripts
./ttyd-stop.sh
```

This will:
1. **Find tunnel process** and kill gracefully
2. **Find ttyd process** and kill gracefully
3. **Confirm both stopped**
4. **Report session ended**

#### 5.2 Verify Stopped

The script will show:
```
Stopping ttyd remote terminal session...
✓ Tunnel stopped
✓ ttyd stopped
Session ended successfully.
```

**Verify Nothing Running**:
```bash
./ttyd-status.sh
```

Should show: `ttyd is not running`

**Why Stop?**:
- **Saves data** (ngrok free tier: 1GB/month limit)
- **Security** (no active tunnel means no way to connect)
- **Resources** (frees ~50MB memory)
- **Best practice** (only run when actively using)

**Troubleshooting Stop**:
- Process won't stop? See running processes: `ps aux | grep ttyd`
- Forcefully kill: `pkill -9 ttyd && pkill -9 ngrok`

---

### Step 6: Check Status

Check if ttyd session is running and get connection info.

#### 6.1 Check Current Status

```bash
cd ~/.claude/skills/ttyd-remote-terminal-wsl2/scripts
./ttyd-status.sh
```

**If Running**, you'll see:
```
==================================================
ttyd Remote Terminal - STATUS
==================================================

Status: RUNNING ✓

🌐 Connection URL:
   https://abc123.ngrok-free.app

🔐 Login Credentials:
   Username: myusername
   Password: aB3$xK9#mL2@pQ7!

⏱️  Session Duration: 1 hour 23 minutes

📊 Resource Usage:
   ttyd process: 15 MB
   Tunnel process: 24 MB

To stop session: ./ttyd-stop.sh
==================================================
```

**If Stopped**, you'll see:
```
==================================================
ttyd Remote Terminal - STATUS
==================================================

Status: NOT RUNNING

To start session: ./ttyd-start.sh
==================================================
```

#### 6.2 Use Cases for Status

**Check before starting**: Avoid starting duplicate sessions
```bash
./ttyd-status.sh && ./ttyd-start.sh
```

**Get URL when you forgot it**: Status shows current URL
```bash
./ttyd-status.sh  # Copy URL from output
```

**Check if forgotten session running**: See if you left it running
```bash
./ttyd-status.sh  # If running, consider stopping
```

**Monitor session duration**: See how long it's been running
```bash
watch -n 60 './ttyd-status.sh'  # Update every minute
```

---

## Security Essentials

**Security-First Design**:
This skill implements defense-in-depth security to protect your WSL2 environment.

### Default Security Features

✅ **Authentication Required**
- All connections require username + password
- Strong passwords generated by default (16+ characters)
- Prevents CVE-2021-34182 (insecure default permissions)

✅ **HTTPS Encryption**
- All traffic encrypted via tunnel (ngrok/Cloudflare/Tailscale)
- Prevents eavesdropping
- Browser shows secure padlock

✅ **Localhost Binding**
- ttyd binds to 127.0.0.1 only (not 0.0.0.0)
- Cannot be accessed directly from network
- Must go through authenticated tunnel

✅ **Secure Credential Storage**
- Credentials stored in `~/.ttyd/.env` with 600 permissions
- Only your user can read the file
- Never committed to git (.gitignore recommended)

✅ **No Hardcoded Secrets**
- All passwords generated or user-provided
- No default passwords
- No credentials in code

### Security Best Practices

**Do**:
- ✅ Use strong passwords (default generator creates these)
- ✅ Stop sessions when not in use
- ✅ Keep ttyd and tunnel tools updated
- ✅ Only share URLs with trusted people
- ✅ Monitor active sessions (use `./ttyd-status.sh`)
- ✅ Review tunnel logs periodically

**Don't**:
- ❌ Share your password publicly
- ❌ Use weak custom passwords (<12 characters)
- ❌ Leave sessions running indefinitely
- ❌ Expose ttyd directly without tunnel
- ❌ Bind to 0.0.0.0 on public networks
- ❌ Disable authentication

### Threat Model

**Protected Against**:
- ✅ Unauthorized access (authentication required)
- ✅ Eavesdropping (HTTPS encryption)
- ✅ Network scanning (localhost binding)
- ✅ Weak passwords (strong generation)
- ✅ Credential theft from filesystem (600 permissions)

**Not Protected Against** (out of scope):
- ⚠️ Compromised WSL2 system (if system compromised, terminal access is too)
- ⚠️ Malicious code execution (if you run malicious code in terminal)
- ⚠️ Social engineering (sharing password with attacker)
- ⚠️ Browser vulnerabilities (keep browser updated)

### Security Warnings

**⚠️ ngrok Free Tier Warning**:
ngrok free tier URLs are public (anyone with URL can access). However:
- URL is random and hard to guess (e.g., `abc123xyz.ngrok-free.app`)
- Authentication still required (username + password)
- HTTPS encrypted
- **Recommendation**: Don't share ngrok URLs publicly, only with trusted people

**⚠️ WSL2 Firewall**:
If you have Windows Firewall enabled (you should), ttyd running on localhost is protected. If you modify scripts to bind to 0.0.0.0, ensure Windows Firewall blocks port 7681.

**⚠️ Session Hijacking**:
If someone gets your URL + password, they can access your terminal. Treat these like SSH credentials.

### Advanced Security (Optional)

For enhanced security, see [Security Guide](references/security-guide.md):
- fail2ban integration (brute force protection)
- Access logging and monitoring
- Reverse proxy with additional auth (nginx + OAuth)
- Certificate pinning
- IP whitelisting (Cloudflare Tunnel)

---

## Troubleshooting Quick Fixes

### ttyd Won't Start

**Error**: `ttyd: command not found`
**Fix**:
```bash
# Reinstall ttyd
./install.sh
```

**Error**: `Address already in use (port 7681)`
**Fix**:
```bash
# Find what's using port
lsof -i :7681

# Kill the process
kill <PID>

# Or use different port
TTYD_PORT=7682 ./ttyd-start.sh
```

### Tunnel Won't Connect

**ngrok Error**: `authtoken not configured`
**Fix**:
```bash
# Add your ngrok authtoken
ngrok config add-authtoken YOUR_TOKEN_HERE
```

**ngrok Error**: `Bandwidth limit exceeded`
**Fix**:
- You've used 1GB free tier data
- Wait until next month, or upgrade to paid plan
- Or switch to Cloudflare Tunnel (unlimited):
  ```bash
  ./install.sh  # Choose Cloudflare Tunnel
  ```

**Cloudflare Error**: `not logged in`
**Fix**:
```bash
cloudflared tunnel login
```

**Tailscale Error**: `not authenticated`
**Fix**:
```bash
sudo tailscale up
```

### Can't Connect from Browser

**Issue**: URL opens but shows "Unable to connect"
**Fix**:
1. Check ttyd running: `./ttyd-status.sh`
2. Check tunnel running: `pgrep ngrok` (or cloudflared, tailscale)
3. Restart session: `./ttyd-stop.sh && ./ttyd-start.sh`

**Issue**: Authentication not working (wrong password)
**Fix**:
```bash
# Reset password
./configure-auth.sh

# Get new credentials
./ttyd-status.sh
```

**Issue**: ngrok warning page (free tier)
**Fix**:
- This is normal for ngrok free tier
- Click "Visit Site" button
- Then login with credentials

### WebSocket Connection Failed

**Error in browser console**: `WebSocket connection failed`
**Fix**:
- Usually means ttyd stopped
- Check status: `./ttyd-status.sh`
- Restart: `./ttyd-start.sh`

### High Latency / Slow Terminal

**Issue**: Commands feel laggy
**Fixes**:
1. **Check internet connection** (need stable connection)
2. **Try different tunnel service** (Cloudflare often faster than ngrok)
3. **Check WSL2 resources**:
   ```bash
   htop  # Check CPU/memory not maxed out
   ```

### Cannot Type in Terminal (CRITICAL)

**Issue**: Terminal displays but keyboard input doesn't work
**Cause**: ttyd runs in **readonly mode by default** (security feature)
**Fix**: The `ttyd-start.sh` script now includes the `--writable` flag automatically.

If you're running ttyd manually, you MUST use the `-W` or `--writable` flag:
```bash
ttyd --writable --credential user:pass bash
```

**References**:
- GitHub Issue: https://github.com/tsl0922/ttyd/issues/1217
- Official docs: ttyd is readonly by default, use `-W` to enable input

### Permission Denied

**Error**: `./ttyd-start.sh: Permission denied`
**Fix**:
```bash
# Make scripts executable
chmod +x ~/.claude/skills/ttyd-remote-terminal-wsl2/scripts/*.sh
```

### For More Help

**Detailed Troubleshooting**: See [Troubleshooting Guide](references/troubleshooting.md)
- Complete error catalog
- Advanced debugging
- Log analysis
- Performance tuning

**Community Help**:
- GitHub Issues: https://github.com/tsl0922/ttyd/issues
- ngrok Support: https://ngrok.com/docs
- Cloudflare Community: https://community.cloudflare.com/

---

## Reference Guides

Comprehensive guides for deeper understanding:

### Installation & Setup
- **[Installation Guide](references/installation-guide.md)** - Detailed installation instructions for ttyd + all tunnel options, manual installation, version management, verification tests

### Security
- **[Security Guide](references/security-guide.md)** - CVE-2021-34182 analysis, authentication methods, password best practices, defense in depth, fail2ban setup, access logging

### Tunneling
- **[Tunneling Options Guide](references/tunneling-options.md)** - Comprehensive comparison of ngrok vs Cloudflare Tunnel vs Tailscale, detailed setup for each, performance benchmarks, cost analysis

### Networking
- **[WSL2 Networking Guide](references/wsl2-networking-guide.md)** - Mirrored mode vs NAT mode, .wslconfig configuration, port forwarding, firewall setup, connectivity troubleshooting

### Troubleshooting
- **[Troubleshooting Guide](references/troubleshooting.md)** - Extensive error catalog, debugging techniques, log analysis, performance optimization, common issues and solutions

---

## Automation Scripts

All automation scripts are in `scripts/` directory:

### Installation
```bash
./install.sh              # Interactive installer for ttyd + tunnel
./install.sh --ngrok      # Non-interactive: install with ngrok
./install.sh --cloudflare # Non-interactive: install with Cloudflare
./install.sh --tailscale  # Non-interactive: install with Tailscale
```

### Configuration
```bash
./configure-auth.sh                    # Interactive: generate password
./configure-auth.sh --custom-password  # Interactive: use your password
```

### Session Management
```bash
./ttyd-start.sh   # Start ttyd + tunnel, display URL
./ttyd-stop.sh    # Stop both gracefully
./ttyd-status.sh  # Check status, show URL if running
```

### Health Check
```bash
./health-check.sh  # Verify installation and configuration
```

---

## Templates

Configuration templates for advanced users:

### systemd Service
**File**: `templates/ttyd.service`

For auto-start on WSL2 boot (requires systemd support):
```bash
# Copy template
cp templates/ttyd.service ~/.config/systemd/user/

# Enable auto-start
systemctl --user enable ttyd
systemctl --user start ttyd
```

### Environment Variables
**File**: `templates/.env.template`

Example `.env` configuration (created automatically by `configure-auth.sh`):
```bash
TTYD_USER=myusername
TTYD_PASSWORD=strongpassword
TUNNEL_TYPE=ngrok
NGROK_AUTH_TOKEN=your_token_here
```

---

## Tips & Tricks

### Save Connection URL to Phone

**iOS**: Save URL as Home Screen bookmark
1. Open URL in Safari
2. Tap Share → Add to Home Screen
3. Now one-tap access

**Android**: Save URL as Chrome shortcut
1. Open URL in Chrome
2. Menu → Add to Home screen
3. Now one-tap access

### Multiple Concurrent Sessions

Want terminal AND web server accessible?

**Use different ports**:
```bash
# Terminal on 7681
TTYD_PORT=7681 ./ttyd-start.sh

# Another service on different port
ngrok http 8080  # Your web server
```

### Check Data Usage (ngrok)

```bash
# View ngrok dashboard
ngrok http 7681 --log stdout | grep -i "bytes"
```

### Quick Restart

```bash
# One-liner restart
./ttyd-stop.sh && ./ttyd-start.sh
```

### Run on Custom Port

```bash
# Use port 8080 instead of 7681
TTYD_PORT=8080 ./ttyd-start.sh
```

### Persistent URLs (Cloudflare)

Unlike ngrok (URLs change each restart), Cloudflare Tunnel URLs persist:
```bash
# First time: creates persistent URL
cloudflared tunnel create ttyd-terminal
cloudflared tunnel route dns ttyd-terminal terminal.yourdomain.com

# Now this URL never changes
# https://terminal.yourdomain.com
```

See [Tunneling Options Guide](references/tunneling-options.md) for details.

---

## Performance Expectations

**Resource Usage**:
- ttyd process: ~10-15 MB memory
- Tunnel process: ~20-30 MB memory
- Total: ~50 MB memory
- CPU: <5% when idle, <15% when actively typing

**Network Latency** (typical):
- ngrok: 50-150ms
- Cloudflare Tunnel: 30-100ms
- Tailscale: 20-80ms (depends on peer distance)

**Bandwidth Usage** (approximate):
- Idle session: ~1 KB/minute
- Active typing: ~10-50 KB/minute
- Streaming output (logs, builds): ~1-5 MB/minute

**ngrok Free Tier Data Budget**:
- 1GB/month limit
- Typical usage: ~10-50 MB/hour active use
- **Estimation**: 20-100 hours/month of active use

---

## Comparison: ttyd vs code-server

**When to use ttyd** (this skill):
- ✅ Quick command execution
- ✅ Lightweight (<50MB)
- ✅ Simple setup
- ✅ Low data usage
- ✅ Works well on mobile

**When to use code-server**:
- Need full IDE (IntelliSense, debugging, extensions)
- Editing large codebases
- Long development sessions
- Tablet with keyboard
- High resource usage acceptable (200MB-4GB)

**Can use both**: Install both skills, use ttyd for quick tasks, code-server for serious coding.

---

## Next Steps

**After Setup**:
1. ✅ Test connection from mobile device
2. ✅ Bookmark connection URL on devices
3. ✅ Practice start/stop workflow
4. ✅ Explore reference guides for advanced features

**Advanced Setup**:
- Configure systemd auto-start (see templates/)
- Setup Cloudflare Tunnel for persistent URLs
- Enable access logging (see Security Guide)
- Setup fail2ban for brute-force protection

**Explore More**:
- [Installation Guide](references/installation-guide.md) - All installation methods
- [Security Guide](references/security-guide.md) - Advanced security
- [Tunneling Options](references/tunneling-options.md) - Compare tunnel services
- [WSL2 Networking](references/wsl2-networking-guide.md) - Network configuration
- [Troubleshooting](references/troubleshooting.md) - Solve issues

---

## Success Checklist

You've successfully setup remote terminal access when:

- [x] ttyd installed and verified
- [x] Tunnel service installed (ngrok/Cloudflare/Tailscale)
- [x] Authentication configured (strong password)
- [x] Can start session (`./ttyd-start.sh`)
- [x] Connection URL displayed
- [x] Can access terminal from browser (phone/tablet/computer)
- [x] Can login with credentials
- [x] Terminal is responsive and functional
- [x] Can stop session (`./ttyd-stop.sh`)
- [x] Can check status (`./ttyd-status.sh`)

**Congratulations! You now have secure remote terminal access to WSL2 from any device.**

---

**ttyd-remote-terminal-wsl2** - Secure web-based terminal access made simple.

### Connection Timeout / Reconnect Button

**Issue**: Terminal shows "reconnect" button after being idle or switching apps on mobile
**Cause**: Mobile browsers suspend background tabs to save battery (by design)
**Fix Applied**: Aggressive 3-second ping interval (`--ping-interval 3`)

**Understanding the Behavior:**
- ✅ **Active tab:** Connection stays alive indefinitely (3-second pings keep it alive)
- ⚠️ **Background tab:** Will disconnect after ~30-60 seconds (browser power-saving)
- ✅ **Your session persists!** When you click reconnect, you're back in the same bash session

**Best Practices:**
- Keep browser tab active while using
- When you see reconnect button, just click it (one click, no data lost!)
- Use tmux/screen for long-running processes: `tmux new -s work`
- Try "Desktop Mode" in browser settings for less aggressive timeouts

**References:**
- [Browser WebSocket Power-Saving](https://www.pixelstech.net/article/1719122489-the-pitfall-of-websocket-disconnections-caused-by-browser-power-saving-mechanisms)
- Complete guide: `cat ~/.ttyd/CONNECTION-KEEPALIVE-GUIDE.md`


### Persistent Session Across Connections

**NEW:** ttyd now uses a persistent tmux session by default!

**What this means:**
- ✅ **Same session every time** you connect (mobile, desktop, anywhere)
- ✅ **Never lose your place** - directory, history, running processes all preserved
- ✅ **Multi-device sharing** - connect from phone and laptop simultaneously, see same terminal in real-time!
- ✅ **Survives disconnects** - close browser, come back days later, right where you left off

**How it works:**
```bash
# The magic command (in ttyd-start.sh line 102)
tmux new -As ttyd-mobile
```

This creates a session called "ttyd-mobile" on first connection, and every subsequent connection attaches to the same session.

**Example:**
```bash
# Connection 1 (mobile):
cd /mnt/c/projects
echo "Working on project" > status.txt

# <close browser, go to sleep>

# Connection 2 (desktop, next morning):
pwd  # Shows: /mnt/c/projects
cat status.txt  # Shows: Working on project
# Exactly where you left off!
```

**Complete guide:** `cat ~/.ttyd/PERSISTENT-SESSION-GUIDE.md`

