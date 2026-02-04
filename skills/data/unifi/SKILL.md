---
name: Unifi
description: |
  UniFi Network Monitoring and Management Skill

  Monitor and query UniFi network devices (USG, Cloud Key, Access Points, Switches).
  Provides real-time network status, client information, device health, and alerts.

  USE WHEN: User asks about network status, connected devices, bandwidth, WiFi clients,
  network health, UniFi devices, or home network monitoring.
---

# UniFi Network Monitoring Skill

Monitor and manage UniFi network infrastructure through the UniFi Controller API.

## Device Information

**User's UniFi Setup:**
- **UniFi Security Gateway (USG3)** - Router/Gateway
- **Cloud Key Gen 2** - UniFi Controller host
- Access Points, Switches (to be discovered)

## Available Commands

All commands are executed via the UniFi CLI wrapper located at `~/.claude/skills/Unifi/unifi-cli.ts`.

Run commands using:
```bash
bun ~/.claude/skills/Unifi/unifi-cli.ts <command>
```

### Network Status Commands

1. **Get Site Status**
   ```bash
   bun ~/.claude/skills/Unifi/unifi-cli.ts site-status
   ```
   Shows overall network health, controller version, and site information.

2. **List All Devices**
   ```bash
   bun ~/.claude/skills/Unifi/unifi-cli.ts devices
   ```
   Shows all UniFi devices (USG, APs, Switches) with status, uptime, and firmware.

3. **List Connected Clients**
   ```bash
   bun ~/.claude/skills/Unifi/unifi-cli.ts clients
   ```
   Shows all connected clients with hostname, IP, MAC, connection type, and bandwidth usage.

4. **Get Device Health**
   ```bash
   bun ~/.claude/skills/Unifi/unifi-cli.ts health
   ```
   Shows health metrics for all devices including CPU, memory, uptime.

5. **Get Recent Alerts**
   ```bash
   bun ~/.claude/skills/Unifi/unifi-cli.ts alerts
   ```
   Shows recent network alerts and events.

6. **Get WAN Status**
   ```bash
   bun ~/.claude/skills/Unifi/unifi-cli.ts wan
   ```
   Shows WAN connection status, public IP, speeds, and uptime.

7. **Get Bandwidth Stats**
   ```bash
   bun ~/.claude/skills/Unifi/unifi-cli.ts bandwidth
   ```
   Shows current bandwidth usage by client and overall network.

## Configuration

Configuration is stored in `~/.claude/skills/Unifi/config.json`:

```json
{
  "controller": {
    "host": "192.168.1.x",
    "port": 8443,
    "username": "admin",
    "password": "your-password",
    "site": "default"
  }
}
```

**Security Notes:**
- Config file contains credentials - NEVER commit to public repos
- Stored in `~/.claude/skills/Unifi/` which should be in .gitignore
- Uses local network connection to Cloud Key
- Read-only operations by default (safe queries only)

## First-Time Setup

If this is the first time using the skill:

1. **Install dependencies:**
   ```bash
   cd ~/.claude/skills/Unifi && bun install
   ```

2. **Create config file:**
   ```bash
   cp ~/.claude/skills/Unifi/config.example.json ~/.claude/skills/Unifi/config.json
   ```

3. **Edit config with actual values:**
   - Set `host` to Cloud Key IP address
   - Set `username` and `password` for UniFi Controller
   - Site is usually "default" unless using multiple sites

4. **Test connection:**
   ```bash
   bun ~/.claude/skills/Unifi/unifi-cli.ts site-status
   ```

## Usage Instructions for AI

When user asks about network status:

1. **Check if skill is configured:**
   - Verify `~/.claude/skills/Unifi/config.json` exists
   - If not, guide user through setup

2. **Run appropriate command:**
   - Network status → `site-status`
   - Who's online → `clients`
   - Device health → `health` or `devices`
   - Internet status → `wan`
   - Recent issues → `alerts`

3. **Parse and present results:**
   - Format output in readable tables
   - Highlight important metrics (high bandwidth, offline devices, alerts)
   - Provide context and interpretation

## Example Queries

User asks: "Who's connected to my network?"
```bash
bun ~/.claude/skills/Unifi/unifi-cli.ts clients
```

User asks: "Is my internet working?"
```bash
bun ~/.claude/skills/Unifi/unifi-cli.ts wan
```

User asks: "What's wrong with my network?"
```bash
bun ~/.claude/skills/Unifi/unifi-cli.ts alerts
bun ~/.claude/skills/Unifi/unifi-cli.ts health
```

User asks: "How's my network doing?"
```bash
bun ~/.claude/skills/Unifi/unifi-cli.ts site-status
bun ~/.claude/skills/Unifi/unifi-cli.ts devices
```

## Limitations

- Read-only operations (no configuration changes)
- Requires local network access to Cloud Key
- Depends on UniFi Controller being online and accessible
- Some features require specific UniFi device types

## Future Enhancements

Potential additions:
- Port forwarding management
- DHCP lease information
- Deep packet inspection (DPI) stats
- Guest network management
- WiFi configuration queries
- Historical bandwidth trends
- Alert notifications

## Troubleshooting

**Connection Failed:**
- Verify Cloud Key is online and accessible
- Check IP address in config.json
- Ensure username/password are correct
- Verify port 8443 is accessible (HTTPS to Controller)

**Authentication Failed:**
- Verify username/password in config.json
- Check if account has admin privileges
- Try logging into Controller web UI with same credentials

**Command Not Found:**
- Run `cd ~/.claude/skills/Unifi && bun install`
- Verify bun is installed: `bun --version`
- Check file exists: `ls -la ~/.claude/skills/Unifi/unifi-cli.ts`
