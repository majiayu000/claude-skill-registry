---
context: current
model: sonnet
description: Voice-controlled Claude Code - speak commands, hear responses in Olivia voice
---

# /voice-chat

Voice-controlled Claude Code. Speak your commands/questions, Claude processes them verbatim (as if you typed them), and responds with Inworld Olivia voice.

## Usage

```
/voice-chat               # Start voice-controlled mode
/voice-chat stop          # Exit voice mode
```

## Requirements (from .claude/voice-chat-requirements.md)

### R1: Voice Input → Claude Code Verbatim

Your spoken words are transcribed and passed **directly to Claude Code** — exactly as if you typed them.

### R2: Response in Inworld Olivia Voice

Claude Code's response is spoken using **Inworld TTS with Olivia voice**.

## Prerequisites

1. **voice-bridge server** running with `INWORLD_API_KEY` set:

   ```bash
   cd ~/Documents/GitHub/voice-bridge
   VOICE_BACKEND=inworld INWORLD_API_KEY=<your-key> npm start
   ```

2. Microphone permissions granted

## Instructions

### Starting Voice Mode

When `/voice-chat` is invoked:

1. **Announce start**:

   ```
   mcp__voice-mcp__voice_speak({
     text: "Voice mode active. Speak your command.",
     voice_id: "Olivia",
     speed: 1.0
   })
   ```

2. **Display**: `🎤 **Listening...**`

3. **Listen for voice**:

   ```
   mcp__voice-mcp__voice_listen({
     timeout_seconds: 30,
     language: "en-GB"
   })
   ```

4. **Display the transcription**: `👤 **You said:** "<transcribed text>"`

5. **CRITICAL: Process the transcribed text as if the user typed it directly.**
   - Do NOT interpret it as a "voice chat question"
   - Execute it as a normal Claude Code command/request
   - Use all available tools (Read, Edit, Grep, Bash, etc.) as needed
   - Generate your normal response

6. **Display speaking indicator**: `🔊 **Speaking...**`

7. **Speak the response** (or summary if long):

   ```
   mcp__voice-mcp__voice_speak({
     text: "<response or summary>",
     voice_id: "Olivia",
     speed: 1.0,
     wait: true
   })
   ```

8. **Smart Output Router** - Decide what to speak:

   | Content Type           | Action             | Voice Says              |
   | ---------------------- | ------------------ | ----------------------- |
   | Short (< 100 words)    | Speak fully        | Full response           |
   | Medium (100-300 words) | Display + announce | "Here's what I found"   |
   | Long (> 300 words)     | Display only       | "Please read this"      |
   | Contains code          | Display + announce | "Here's the code"       |
   | Contains table         | Display + announce | "Here's a table"        |
   | Error                  | Speak              | Brief error description |

9. **Loop back** to step 2 for next command

### Exit Conditions

- User says: "stop", "exit", "bye", "goodbye", "end voice mode"
- User types: `/voice-chat stop`
- Timeout with no input

### Stopping Voice Mode

```
mcp__voice-mcp__voice_speak({
  text: "Voice mode ended.",
  voice_id: "Olivia",
  speed: 1.0
})
```

Display: `👋 **Voice mode ended.** Returning to text input.`

## Example Flow

```
User: /voice-chat

🎤 **Listening...**
Olivia: "Voice mode active. Speak your command."

[User speaks: "What projects am I working on?"]

👤 **You said:** "What projects am I working on?"

[Claude searches vault, finds projects]

🔊 **Speaking...**

🤖 **Claude:** You have 3 active projects: Alpha, Beta, and Gamma.

Olivia: "You have 3 active projects: Alpha, Beta, and Gamma."

🎤 **Listening...**

[User speaks: "Create a meeting note for today"]

👤 **You said:** "Create a meeting note for today"

[Claude creates meeting note using normal workflow]

🔊 **Speaking...**

🤖 **Claude:** Created Meeting - 2026-01-29 [Title].md

Olivia: "Meeting note created."

🎤 **Listening...**

[User speaks: "Stop"]

Olivia: "Voice mode ended."

👋 **Voice mode ended.** Returning to text input.
```

## Key Principle

**The transcribed text IS the user's command.** Process it exactly as you would if they typed it. The only difference is:

- Input comes from voice transcription
- Output is spoken via Inworld Olivia TTS

## Troubleshooting

- **Male voice playing**: Check `INWORLD_API_KEY` is set and voice-bridge restarted
- **No voice at all**: Check voice-bridge is running on port 4000
- **TTS error**: Verify API key is valid base64-encoded Inworld key
