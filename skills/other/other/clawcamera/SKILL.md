---
name: office-cam
description: Multi-camera surveillance system with motion detection, continuous monitoring (Overwatch), and AI analysis. Supports USB webcams, Wyze RTSP, and ESP32-CAM. Features random check-ins with GIF updates.
homepage: https://github.com/Snail3D/ClawCamera
metadata:
  {
    "openclaw":
      {
        "emoji": "📹",
        "requires": { "bins": ["ffmpeg", "identify"], "env": ["GROQ_API_KEY"] },
        "install":
          [
            {
              "id": "npm",
              "kind": "npm",
              "packages": ["express", "multer", "axios"],
              "label": "Install Node dependencies",
            },
            {
              "id": "homebrew",
              "kind": "brew",
              "formula": "ffmpeg imagemagick",
              "bins": ["ffmpeg", "identify"],
              "label": "Install ffmpeg & ImageMagick",
            },
          ],
      },
  }
---

# office-cam

Multi-camera surveillance system with motion detection, continuous monitoring (Overwatch mode), and AI-powered analysis. Perfect for office/home monitoring with random check-in alerts.

## Features

### 📸 **Tier 1: One-Shot Capture**
Instant visual Q&A on demand:
- `capture.sh` — Take a photo from the office camera
- Ask "Is anyone here?" and get instant AI analysis
- Great for quick status checks

### 🎥 **Tier 2: Motion Detection**
Continuous monitoring with configurable alerts:
- `motion-detect.sh` — Detect motion and alert on change
- File-size comparison method (fast, reliable)
- Configurable cooldown and threshold
- Three modes:
  - **report-all** — Alert on ANY motion
  - **report-suspicious** — Alert only on threats (weapons, breaking, etc.)
  - **report-match** — Alert on exact BOLO text match with strict feature matching

### 🕵️ **Tier 3: Overwatch (24/7 Monitoring)**
Background daemon with automatic check-ins:
- `overwatch start` — Launch continuous background monitoring
- `overwatch stop` — Stop the daemon
- Saves motion alerts to `~/.clawdbot/overwatch/`
- **Random check-ins** — Periodically takes snapshots and posts GIF updates to Telegram
- AI analysis on every trigger
- Automatic image storage and cleanup

### 🎯 **Tier 4: BOLO (Be On Lookout)**
Visual fingerprinting and exact matching:
- Upload a photo → auto-extract features (faces, clothing, items, etc.)
- Monitor for exact matches across angles/lighting/distance
- Critical features (moles, scars, plates) MUST all match
- High priority features (hair, eyes, vehicle type) should match
- Medium/low priority features can vary

### 🎬 **GIF Reactions**
- Random check-in captures paired with GIF reactions ("spy camera", "watching", etc.)
- Makes alerts fun and conversational
- Telegram integration for instant notifications

## Quick Start

### Setup
```bash
git clone https://github.com/Snail3D/ClawCamera.git
cd ClawCamera
npm install
export GROQ_API_KEY=your_key_here
```

### Commands
```bash
# One-shot capture
./scripts/capture.sh

# Motion detection
./scripts/motion-detect.sh --cooldown 180 --threshold 10

# Start Overwatch (continuous monitoring)
./scripts/overwatch start

# Stop Overwatch
./scripts/overwatch stop

# Check Overwatch status
./scripts/overwatch status
```

## Configuration

### Environment Variables
```bash
# Required
export GROQ_API_KEY=gsk_xxxxx

# Optional
export CAMERA_SOURCE="/dev/video0"      # USB webcam device
export WYZE_IP="192.168.1.100"          # Wyze camera IP (RTSP)
export MOTION_COOLDOWN=180              # Seconds between alerts (default: 180)
export MOTION_INTERVAL=2000             # Check interval in ms (default: 2000)
export MOTION_THRESHOLD=10              # Motion threshold % (default: 10)
export TELEGRAM_TOKEN="your_token"      # For check-in notifications
export TELEGRAM_CHAT_ID="your_id"       # Your Telegram chat
```

### .env.example
```
GROQ_API_KEY=gsk_xxxxx
CAMERA_SOURCE=/dev/video0
WYZE_IP=192.168.1.100
MOTION_COOLDOWN=180
MOTION_INTERVAL=2000
MOTION_THRESHOLD=10
TELEGRAM_TOKEN=your_token
TELEGRAM_CHAT_ID=your_chat_id
```

## Multi-Camera Support

### USB Webcam
```bash
# Find your camera
ls /dev/video*

# Capture from USB
ffmpeg -f avfoundation -i "0" -frames 1 photo.jpg
```

### Wyze Camera (RTSP)
```bash
# Configure WYZE_IP in .env
ffmpeg -rtsp_transport tcp -i "rtsp://wyze_ip:554/live" -frames 1 photo.jpg
```

### ESP32-CAM
- Firmware sends images via HTTP POST to media receiver
- Analyzer polls for new images and processes them
- See `guides/esp32-setup.md` for full setup

## Architecture

```
User Request
    ↓
Capture/Motion Detection
    ↓
Image Storage (~/.clawdbot/overwatch/)
    ↓
Groq Vision API (AI Analysis)
    ↓
Alert + GIF Reaction
    ↓
Telegram Notification
```

## Files

- `scripts/capture.sh` — One-shot photo capture
- `scripts/motion-detect.sh` — Continuous motion monitoring
- `scripts/overwatch.js` — Background daemon with check-ins
- `scripts/analyzer.js` — Groq Vision API integration
- `scripts/gifgrep-integration.js` — GIF reaction selection
- `guides/esp32-setup.md` — ESP32-CAM firmware & config
- `guides/wyze-setup.md` — Wyze RTSP configuration
- `guides/troubleshooting.md` — Common issues & solutions

## Troubleshooting

### No images captured
- Check `CAMERA_SOURCE` is correct: `ls /dev/video*`
- Verify permissions: `ls -l /dev/video0`
- Try manual ffmpeg: `ffmpeg -f avfoundation -i "0" -frames 1 test.jpg`

### Overwatch not alerting
- Check daemon is running: `./scripts/overwatch status`
- Verify `GROQ_API_KEY` is set: `echo $GROQ_API_KEY`
- Check logs: `tail -f ~/.clawdbot/overwatch/overwatch.log`

### Motion detection too sensitive
- Increase `MOTION_THRESHOLD` (default: 10%)
- Increase `MOTION_COOLDOWN` (default: 180s)
- Reduce `MOTION_INTERVAL` (default: 2000ms)

### BOLO matching too strict
- Adjust feature priority weights in `scripts/bolo-analyzer.js`
- Use `--strict` flag for exact matching only

## Performance

- **USB Webcam:** Real-time, <500ms per capture
- **Overwatch:** ~2-5s per check including AI analysis
- **Motion Detection:** <1s detection, configurable interval
- **Groq Vision:** ~1-2s analysis per image

## Privacy & Security

✅ **Secrets are .gitignored** — Never commit API keys, credentials, or auth tokens
✅ **No cloud storage** — All images stored locally in `~/.clawdbot/overwatch/`
✅ **Local analysis** — Groq API used only for vision analysis (encrypted transit)
✅ **Configurable retention** — Images auto-cleaned after retention period

## Integration with OpenClaw

### Heartbeat Monitoring
Add to your `HEARTBEAT.md`:
```bash
# Check for overwatch triggers
ls ~/.clawdbot/overwatch/triggers/trigger_*.json 2>/dev/null | wc -l
```

### Cron Jobs
```bash
# Random check-in every 15 minutes
openclaw cron add --schedule "every 15 minutes" --task "office-cam check-in"
```

### Natural Language
```
"Is anyone in the office?"
→ Takes photo + analyzes → "No one detected"

"Watch for movement"
→ Starts Overwatch + sends check-in GIFs

"Look out for a tall person with a blue jacket"
→ BOLO mode + feature matching active
```

## Contributing

Found a bug or want to improve? Open an issue or PR!

## License

MIT

---

**Built with ❤️ by Clawd for Snail** 🦾
