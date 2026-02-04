---
name: tado
description: Control your Tado smart thermostat - check temperature, set heating, manage home/away modes, and monitor presence via geolocation.
homepage: https://www.tado.com
metadata: {"openclaw":{"emoji":"🌡️","requires":{"bins":["python3","pip3"]}}}
---

# Tado Smart Thermostat Skill

Control your Tado smart thermostat from OpenClaw.

## Features

- 📊 **Status:** Get current temperature, humidity, heating status per zone
- 🌡️ **Temperature Control:** Set target temperature with optional timer
- 🏠 **Presence:** Check who is home (geolocation)
- 🔄 **Modes:** Home, Away, Auto (schedule-based)
- ⚙️ **Zone Management:** Support for multi-zone setups
- 📋 **JSON Output:** Machine-readable format for scripting

## Installation

### 1. Install Dependencies

```bash
cd ~/clawd/skills/tado
pip3 install libtado --break-system-packages
```

**Minimum version:** libtado 4.1.1+ (OAuth2 support required)

### 2. OAuth2 Authentication (One-Time Setup)

**⚠️ Important:** libtado 4.1.1+ requires OAuth2. Username/password authentication is **no longer supported**.

**First-time setup:**

```bash
# Run the libtado CLI to authenticate via browser
python3 -m libtado -f ~/.tado_auth.json zones
```

**What happens:**
1. libtado generates a Tado login URL
2. Your browser opens (or you paste the URL manually)
3. Log in with your Tado credentials
4. libtado saves OAuth2 tokens to `~/.tado_auth.json`
5. You'll see your zones listed (confirming success)

**After setup:**
- The skill will automatically use `~/.tado_auth.json`
- No further browser login needed
- Tokens refresh automatically

**Security Note:** The token file should be readable only by you:

```bash
chmod 600 ~/.tado_auth.json
```

### 3. Test Connection

```bash
cd ~/clawd/skills/tado
./scripts/tado.py zones
```

You should see a list of your configured zones.

**If authentication fails:**
```bash
# Re-authenticate (regenerates tokens)
python3 -m libtado -f ~/.tado_auth.json zones
```

## Authentication

### OAuth2 Flow (Required)

As of **libtado 4.1.1+**, OAuth2 is the only supported authentication method.

**Token file location:** `~/.tado_auth.json`

**How it works:**
1. First run: Browser login via `python3 -m libtado -f ~/.tado_auth.json zones`
2. libtado saves access token + refresh token
3. Skill uses `token_file_path` parameter: `Tado(token_file_path='~/.tado_auth.json')`
4. libtado automatically refreshes expired tokens

**Token structure (managed by libtado):**
```json
{
  "access_token": "...",
  "refresh_token": "...",
  "expires_at": 1234567890
}
```

**Do NOT manually edit this file!** Let libtado manage it.

### Migration from Username/Password

**Old authentication (no longer works):**
```python
Tado(username='email', password='pass')  # ❌ Not supported
```

**New authentication (required):**
```python
Tado(token_file_path='~/.tado_auth.json')  # ✅ Works
```

**Migration steps:**
1. Delete old `~/.tado_credentials.json` (no longer used)
2. Run `python3 -m libtado -f ~/.tado_auth.json zones`
3. Follow browser login flow
4. Done! Skill will work automatically

**No backward compatibility:** Once you upgrade to libtado 4.1.1+, you MUST use OAuth2.

## Usage

### Status Commands

**Get status of all zones:**
```bash
./scripts/tado.py status
```

**Output:**
```
🏠 Woonkamer (Zone 1)
  Current: 20.5°C (55% humidity)
  Target:  21.0°C
  Heating: ON (45%)
  Mode:    Auto (following schedule)

🏠 Slaapkamer (Zone 2)
  Current: 18.2°C (58% humidity)
  Target:  18.0°C
  Heating: OFF (0%)
  Mode:    Auto (following schedule)
```

**Get status of specific zone:**
```bash
./scripts/tado.py status --zone 1
./scripts/tado.py status --zone "Woonkamer"
```

**JSON output (for scripting):**
```bash
./scripts/tado.py status --json
```

### Temperature Control

**Set temperature (permanent until next schedule change):**
```bash
./scripts/tado.py set --zone 1 --temperature 21
./scripts/tado.py set --zone "Woonkamer" --temperature 21.5
```

**Set temperature with timer (temporary override):**
```bash
# Set 22°C for 60 minutes, then return to schedule
./scripts/tado.py set --zone 1 --temperature 22 --duration 60

# Short form
./scripts/tado.py set --zone 1 -t 22 -d 60
```

**Reset to automatic schedule:**
```bash
./scripts/tado.py reset --zone 1
./scripts/tado.py reset --zone "Woonkamer"
```

### Home/Away Modes

**Set home mode (all zones follow schedule):**
```bash
./scripts/tado.py mode home
```

**Set away mode (energy-saving temperatures):**
```bash
./scripts/tado.py mode away
```

**Set auto mode (geolocation-based):**
```bash
./scripts/tado.py mode auto
```

When in auto mode, Tado automatically switches between home/away based on your phone's location.

### Presence Detection

**Check who is home:**
```bash
./scripts/tado.py presence
```

**Output:**
```
👥 Presence
  Anyone home: Yes
  - Sander's iPhone: 🏠 Home
  - Partner's iPhone: 🚶 Away
```

### Zone Management

**List all zones:**
```bash
./scripts/tado.py zones
```

**Output:**
```
📍 Available Zones:
  1: Woonkamer (HEATING)
  2: Slaapkamer (HEATING)
  3: Badkamer (HOT_WATER)
```

## Zone Identification

Zones can be referenced by **ID** or **name**:

```bash
# By ID (faster)
./scripts/tado.py status --zone 1

# By name (case-insensitive)
./scripts/tado.py status --zone "Woonkamer"
./scripts/tado.py status --zone "woonkamer"
```

## JSON Output for Scripting

All commands support `--json` flag for machine-readable output:

```bash
./scripts/tado.py status --zone 1 --json
```

**Example output:**
```json
{
  "zone_id": 1,
  "zone_name": "Woonkamer",
  "current_temp": 20.5,
  "current_humidity": 55,
  "target_temp": 21.0,
  "heating": true,
  "heating_power": 45,
  "mode": "MANUAL",
  "overlay": true
}
```

**Use in scripts:**
```bash
# Get current temperature as number
TEMP=$(./scripts/tado.py status --zone 1 --json | jq -r '.current_temp')

# Check if heating is on
HEATING=$(./scripts/tado.py status --zone 1 --json | jq -r '.heating')

# Get all zones data
./scripts/tado.py status --json | jq '.zones[] | {name: .zone_name, temp: .current_temp}'
```

## OpenClaw Integration

**From OpenClaw chat:**

```
@jarvis What's the temperature in the living room?
→ Uses: ./scripts/tado.py status --zone "Woonkamer"

@jarvis Set living room to 22 degrees for 1 hour
→ Uses: ./scripts/tado.py set --zone "Woonkamer" -t 22 -d 60

@jarvis Is anyone home?
→ Uses: ./scripts/tado.py presence

@jarvis Turn on away mode
→ Uses: ./scripts/tado.py mode away
```

## Troubleshooting

### Authentication Errors

**Error:** `Tado OAuth2 token not found!`

**Solution:** Run the one-time authentication flow:
```bash
python3 -m libtado -f ~/.tado_auth.json zones
```

Then follow the browser login prompt.

---

**Error:** `Failed to connect to Tado: 401 Unauthorized`

**Possible causes:**
- Expired or invalid OAuth2 token
- Token file corrupted
- Tado service outage

**Solutions:**
1. Re-authenticate:
   ```bash
   python3 -m libtado -f ~/.tado_auth.json zones
   ```
2. Check token file exists: `ls -la ~/.tado_auth.json`
3. Verify token file permissions: `chmod 600 ~/.tado_auth.json`
4. Check Tado service status at https://status.tado.com

### API Errors

**Error:** `Failed to get status: HTTP 500`

**Solution:** Tado API may be temporarily down. Check https://status.tado.com

---

**Error:** `Zone 'X' not found`

**Solution:** 
1. List available zones: `./scripts/tado.py zones`
2. Use exact zone ID or name from the list

### Connection Issues

**Error:** `Failed to connect to Tado: Network unreachable`

**Solution:**
1. Check internet connection
2. Verify DNS is working: `ping my.tado.com`
3. Check firewall settings

### Library Errors

**Error:** `ModuleNotFoundError: No module named 'PyTado'`

**Solution:**
```bash
pip3 install libtado --break-system-packages
```

---

**Error:** `AttributeError: 'Tado' object has no attribute 'setAutoMode'`

**Possible cause:** Outdated `libtado` version

**Solution:**
```bash
pip3 install --upgrade libtado
```

## API Rate Limits

Tado API has rate limits (exact numbers not publicly documented):

**Best practices:**
- Don't poll status more than once per minute
- Use `--json` output and cache results when possible
- Batch multiple zones in one `status` call instead of separate calls

**If rate limited:**
- Wait 1-2 minutes before retrying
- Reduce polling frequency

## Data Privacy

**Local data:**
- Credentials stored in `~/.tado_credentials.json` (mode 600 recommended)
- No usage tracking or telemetry
- All API calls go directly to Tado servers

**Never exposed:**
- Your credentials are never sent anywhere except Tado API
- Zone names, temperatures, and presence data stay local
- No third-party analytics

## Advanced Usage

### Temperature Scheduling

Create a simple heating schedule script:

```bash
#!/bin/bash
# morning-heat.sh - Warm up before wake-up

# Set living room to 21°C at 6:30 AM
./scripts/tado.py set --zone "Woonkamer" -t 21 -d 120

# Reset to schedule after 2 hours
sleep 7200
./scripts/tado.py reset --zone "Woonkamer"
```

Run with cron:
```
30 6 * * * /path/to/morning-heat.sh
```

### Smart Away Detection

```bash
#!/bin/bash
# smart-away.sh - Set away mode if nobody home

ANYONE_HOME=$(./scripts/tado.py presence --json | jq -r '.anyone_home')

if [ "$ANYONE_HOME" = "false" ]; then
    ./scripts/tado.py mode away
    echo "Nobody home - enabled away mode"
fi
```

### Energy Monitoring

```bash
#!/bin/bash
# energy-log.sh - Log heating activity

DATE=$(date +%Y-%m-%d_%H:%M)
./scripts/tado.py status --json > ~/logs/tado-$DATE.json

# Analyze with jq
jq '.zones[] | select(.heating == true) | {zone: .zone_name, power: .heating_power}' \
  ~/logs/tado-$DATE.json
```

## Known Limitations

1. **Hot Water Control:** Basic support only (ON/OFF), no temperature setting
2. **Weather Data:** Not yet implemented (available in Tado API)
3. **Energy IQ:** Statistics not yet exposed (available in Tado API)
4. **Multi-Home:** Only one Tado home supported per token file

## Future Enhancements

- [x] OAuth2 authentication (✅ Implemented in v1.1.0)
- [ ] Weather data integration
- [ ] Energy IQ statistics
- [ ] Multi-home support
- [ ] Web dashboard (optional)
- [ ] Push notifications for temperature alerts

## Resources

- **libtado Documentation:** https://libtado.readthedocs.io/
- **libtado GitHub:** https://github.com/germainlefebvre4/libtado
- **Tado API (unofficial):** https://blog.scphillips.com/posts/2017/01/the-tado-api-v2/
- **Tado Service Status:** https://status.tado.com

## Support

**For skill issues:**
- Check this SKILL.md
- Read error messages carefully (they include hints)
- Try `--json` output for debugging

**For Tado API/account issues:**
- Check Tado app first (does it work?)
- Visit https://my.tado.com
- Contact Tado support

## Changelog

**v1.1.0** (2026-02-03)
- ✅ **OAuth2 authentication** (libtado 4.1.1+)
- ⚠️ **BREAKING:** Username/password auth removed (no longer supported by libtado)
- One-time browser login flow via `python3 -m libtado`
- Automatic token refresh
- Updated all documentation for OAuth2

**v0.1.0** (2026-01-29)
- Initial release
- Status, temperature control, modes, presence
- JSON output support
- Zone management (ID and name-based)
- Error handling and troubleshooting
