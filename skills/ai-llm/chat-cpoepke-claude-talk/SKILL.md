---
name: chat
description: Quick single voice exchange. Speaks a prompt, captures one response via TTS. No persistent session needed.
disable-model-invocation: true
---

# Quick Voice Chat

Single voice exchange without starting a full voice chat session. Good for quick questions.

## Prerequisites

The audio server must be running. If not, start it first by following the audio server startup steps from the start skill.

## Steps

1. Check if audio server is running (use Bash):
   ```bash
   claude-talk server status
   ```
   If it fails, tell the user the audio server isn't running and they should start a voice chat session first with `/claude-talk:start`, or you can start the server for them.

2. Speak a prompt asking the user their question (use Bash):
   ```bash
   source ~/.claude-talk/venvs/wlk/bin/activate && claude-talk server speak "What can I help you with?"
   ```
   This speaks the prompt, captures the user's response, and routes it back via tmux.

3. Wait for the transcription to arrive as a user message. Then respond conversationally.

4. Speak the response via TTS (use Bash):
   ```bash
   source ~/.claude-talk/venvs/wlk/bin/activate && claude-talk server speak "<your response>"
   ```

5. Show the exchange to the user:
   - "You said: <transcription>"
   - "Response: <your response>"
