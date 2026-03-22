---
name: setup-sonos-lastfm
description: Interactive setup guide for Sonos Last.fm Scrobbler — installs the package, configures Last.fm credentials, and sets up a persistent daemon on Linux, macOS, or Windows so your Sonos speakers automatically scrobble to Last.fm.
---

# Setup Sonos Last.fm Scrobbler

You are guiding a user through the complete setup of **sonos-lastfm**, a tool that automatically scrobbles music playing on Sonos speakers to Last.fm.

PyPI: https://pypi.org/project/sonos-lastfm/
Source: https://github.com/denya/sonos-lastfm

## Overview

Walk the user through these steps in order. At each step, confirm success before moving on. If something fails, help them troubleshoot before continuing.

## Step 1: Detect the Environment

Determine the user's operating system and existing tooling:

```bash
uname -s 2>/dev/null || echo Windows
python3 --version 2>/dev/null || python --version 2>/dev/null
pip --version 2>/dev/null
which uv 2>/dev/null || where uv 2>/dev/null
```

Based on the results:
- **Linux**: will use `systemd --user` for the daemon
- **macOS**: will use `launchd` (a plist in `~/Library/LaunchAgents/`)
- **Windows**: will use Task Scheduler or NSSM

If Python is not installed or is below 3.14, guide the user to install it:
- **macOS**: `brew install python@3.14` or download from python.org
- **Linux**: `sudo apt install python3.14` / `sudo dnf install python3.14` or use `pyenv`
- **Windows**: Download from https://www.python.org/downloads/ — check "Add to PATH"

## Step 2: Install sonos-lastfm from PyPI

Always install the **latest version from PyPI** so the user gets the newest features and fixes.

If `uv` is available (preferred):
```bash
uv pip install --upgrade sonos-lastfm
```

Otherwise:
```bash
pip install --upgrade sonos-lastfm
```

Verify the installation:
```bash
sonos-lastfm --help
```

If the command is not found, check if `~/.local/bin` is in PATH and guide the user to add it.

## Step 3: Get Last.fm API Credentials

The user needs four values from Last.fm. Guide them through obtaining these:

1. Open https://www.last.fm/api/account/create in their browser
2. Fill in the form:
   - **Application name**: anything, e.g. "sonos-scrobbler"
   - **Application description**: optional
   - **Callback URL**: leave blank
   - **Application homepage**: leave blank
3. Submit and note down the **API Key** and **Shared Secret** (also called API Secret)
4. They also need their Last.fm **username** and **password**

Tell the user to keep these values ready for the next step.

## Step 4: Configure Credentials

Run the interactive setup:

```bash
sonos-lastfm setup
```

This will prompt for:
1. **Storage method**: system keyring (most secure) or config file (`~/.sonos_lastfm/.env`)
2. **Username**: their Last.fm username
3. **Password**: their Last.fm password (hidden input)
4. **API Key**: the key from step 3
5. **API Secret**: the secret from step 3 (hidden input)

After setup, it automatically tests the connection and shows account info. If the connection test fails, help troubleshoot (wrong credentials, network issues, etc.).

### Alternative: Environment Variables

If the user prefers environment variables (useful for containers or CI):
```bash
export LASTFM_USERNAME=your_username
export LASTFM_PASSWORD=your_password
export LASTFM_API_KEY=your_api_key
export LASTFM_API_SECRET=your_api_secret
```

## Step 5: Test the Scrobbler

Before setting up the daemon, verify everything works:

```bash
sonos-lastfm info
```

This should show the user's Last.fm profile and recent scrobbles. If Sonos speakers are on the network, also try a quick run:

```bash
sonos-lastfm run
```

Press Ctrl+C to stop after confirming it detects speakers and tracks.

## Step 6: Set Up as a Persistent Daemon

### Linux (systemd)

Create the service file:

```bash
mkdir -p ~/.config/systemd/user
```

Write `~/.config/systemd/user/sonos-lastfm.service`:

```ini
[Unit]
Description=Sonos Last.fm Scrobbler
After=network-online.target

[Service]
Type=simple
ExecStart=%h/.local/bin/sonos-lastfm run --daemon
Restart=on-failure
RestartSec=10

[Install]
WantedBy=default.target
```

Enable and start:
```bash
systemctl --user daemon-reload
systemctl --user enable --now sonos-lastfm
```

Verify it's running:
```bash
systemctl --user status sonos-lastfm
journalctl --user -u sonos-lastfm -f
```

Enable lingering so the service runs even when the user is not logged in:
```bash
loginctl enable-linger $USER
```

### macOS (launchd)

Write `~/Library/LaunchAgents/com.sonos-lastfm.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.sonos-lastfm</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/sonos-lastfm</string>
        <string>run</string>
        <string>--daemon</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/tmp/sonos-lastfm.out.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/sonos-lastfm.err.log</string>
</dict>
</plist>
```

**Important**: Adjust the path to `sonos-lastfm` — find it with `which sonos-lastfm`. If installed via `uv`, it may be at `~/.local/bin/sonos-lastfm`.

Load and start:
```bash
launchctl load ~/Library/LaunchAgents/com.sonos-lastfm.plist
```

Verify:
```bash
launchctl list | grep sonos-lastfm
tail -f /tmp/sonos-lastfm.out.log
```

To stop and unload:
```bash
launchctl unload ~/Library/LaunchAgents/com.sonos-lastfm.plist
```

### Windows (Task Scheduler)

Open PowerShell as Administrator:

```powershell
$action = New-ScheduledTaskAction `
    -Execute "sonos-lastfm" `
    -Argument "run --daemon"

$trigger = New-ScheduledTaskTrigger -AtLogOn

$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -RestartCount 3 `
    -RestartInterval (New-TimeSpan -Minutes 1)

Register-ScheduledTask `
    -TaskName "SonosLastfmScrobbler" `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Description "Sonos Last.fm Scrobbler"
```

Alternatively, if the user prefers a GUI approach, guide them through Task Scheduler:
1. Open Task Scheduler
2. Create Basic Task > Name: "Sonos Last.fm Scrobbler"
3. Trigger: When I log on
4. Action: Start a program > `sonos-lastfm` with arguments `run --daemon`
5. Finish

## Step 7: Upgrading

To upgrade to the latest version in the future:

```bash
pip install --upgrade sonos-lastfm
# or with uv:
uv pip install --upgrade sonos-lastfm
```

Then restart the daemon:
- **Linux**: `systemctl --user restart sonos-lastfm`
- **macOS**: `launchctl unload ~/Library/LaunchAgents/com.sonos-lastfm.plist && launchctl load ~/Library/LaunchAgents/com.sonos-lastfm.plist`
- **Windows**: Restart via Task Scheduler or reboot

## Troubleshooting

### "No Sonos speakers found"
- Ensure your computer and Sonos speakers are on the **same network/VLAN**
- Some WiFi routers isolate clients — check your router settings for "AP isolation" or "client isolation" and disable it
- Try running `sonos-lastfm run` again after a few seconds — mDNS discovery can take time

### "sonos-lastfm: command not found"
- Add `~/.local/bin` to your PATH:
  - **bash**: `echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc && source ~/.bashrc`
  - **zsh**: `echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc && source ~/.zshrc`
  - **fish**: `fish_add_path ~/.local/bin`
- On Windows, ensure the Python Scripts directory is in your PATH

### Credential issues
- Re-run `sonos-lastfm setup` to reconfigure
- Verify your API key at https://www.last.fm/api/accounts
- Ensure your Last.fm password is correct (not your email password)

### Daemon not starting
- **Linux**: Check logs with `journalctl --user -u sonos-lastfm -f`
- **macOS**: Check `/tmp/sonos-lastfm.err.log`
- **Windows**: Check Task Scheduler history

## Scrobble Rules

For reference, sonos-lastfm follows these rules:
- A track is scrobbled after **25%** of its duration has been played (configurable via `--threshold`) or **4 minutes**, whichever comes first
- The same track won't be scrobbled again within 30 minutes
- In daemon mode, only song changes, scrobbles, and errors are logged
