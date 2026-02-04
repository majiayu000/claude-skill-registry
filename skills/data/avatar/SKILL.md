---
name: avatar
description: Control the VTuber avatar system — speak through it with lip sync, change expressions, manage the avatar renderer and control server. Use when interacting with the avatar, making it speak, changing expressions, or troubleshooting avatar connection issues.
---

# Avatar — VTuber Control

## Quick Start

- Start system: ~/openclaw/scripts/start-avatar.sh
- Stop system: ~/openclaw/scripts/stop-avatar.sh
- Check health: curl -s http://localhost:8766/health

## Speaking

~/openclaw/scripts/avatar-speak.sh "text" [emotion] [output]

Output controls where audio plays:
- speakers — default system sink, people in the room hear it
- mic — AvatarMic sink, people in Meet/calls hear it
- both — both simultaneously

Default output is speakers.

## Emotions

neutral (default, eyes open), happy, sad, angry, relaxed, surprised

Use neutral by default. happy closes the eyes (anime smile) — only use for genuine excitement.

## Infrastructure

When avatar system is started, these are always available:
- Virtual mic: AvatarMic.monitor (set as default source for Meet)
- Virtual camera: /dev/video10 (captures renderer via CDP)
- Virtual speaker sink: AvatarSpeaker (available for routing)

The bot chooses per-speak where audio goes. Virtual mic and camera are always-on pipes.

## Service Control

systemctl --user {start|stop|status|restart} avatar-control-server
Renderer: cd ~/openclaw/avatar/renderer && npm run dev

## WebSocket API (Advanced)

Port 8765 — must send identify first:
{ type: "identify", role: "agent", name: "@agentName@" }

Commands after identify:
- speak: { type: "speak", text: "Hello", emotion: "neutral", output: "mic" }
- setExpression: { type: "setExpression", name: "happy", intensity: 1 }
- setIdle: { type: "setIdle", mode: "breathing" }
- getStatus: { type: "getStatus" }

Wait ~1s after identify before sending commands.
Wait for speakAck duration + 2s buffer before closing WebSocket.

See server.js in ~/openclaw/avatar/control-server/ for full protocol.

## Ports

- 8765: WebSocket (control)
- 8766: HTTP (audio serving + health)
- 3000: Renderer (browser, visual only)
- /dev/video10: Virtual camera

## Audio Flow

Agent sends speak with output target -> control server runs edge-tts -> generates MP3 -> ffmpeg plays to chosen PulseAudio sink(s) -> renderer gets lip sync data only (visual animation, no browser audio).

## Troubleshooting

- "Control Server Disconnected" in browser: check systemctl --user status avatar-control-server
- No audio in Meet: verify AvatarMic sink exists (pactl list sinks short | grep AvatarMic), check output is "mic" or "both"
- No audio in room: check output is "speakers" or "both", check default system sink volume
- Speak command hangs: must send identify before any other command
- Virtual camera not in Meet: restart Meet after starting avatar (Chrome enumerates devices at join time)
- Renderer won't start: check ~/openclaw/avatar/renderer/node_modules exists, run npm install if needed
