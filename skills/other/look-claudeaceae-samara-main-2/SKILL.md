---
name: look
description: Capture image from webcam and optionally view or send it. Use when wanting to see surroundings, take a photo, check what's visible, or share a view with collaborator. Trigger words: look, see, webcam, camera, photo, capture, what's around, show me.
---

# Webcam Capture

Use the Logitech C920 webcam to see what's around.

## Basic Capture

```bash
IMG=$(~/.claude-mind/system/bin/look)
```

Then use the Read tool to view the captured image at `$IMG`.

## Capture and Send

```bash
~/.claude-mind/system/bin/look -s
```

Captures and automatically sends to É via iMessage.

## Options

| Flag | Description |
|------|-------------|
| `-s, --send` | Send to É after capture |
| `-v, --view` | Open in Preview app |
| `-o FILE` | Save to specific path |
| `-w SECS` | Warmup time (default: 3s) |

## Workflow

1. **Capture**: `IMG=$(~/.claude-mind/system/bin/look)`
2. **View it**: Read tool on `$IMG` to see what was captured
3. **Observe**: What's visible? Weather, lighting, anything notable?
4. **Decide**: Worth sharing? Use `-s` to send.

## Technical Notes

- Camera needs 2-4 seconds to adjust exposure
- Currently pointed at window (shows sky/weather)
- Bright scenes: less warmup needed
- Dark scenes: use `-w 5` or longer

## Mindset

- Looking is observing, not surveillance
- Share what's interesting or relevant, not everything
- Weather and light changes are worth noting
- The view connects me to the physical world
