---
name: voice-call
description: Inicie chamadas de voz via o plugin de voz do Zero.
metadata: {"zero":{"emoji":"📞","skillKey":"voice-call","requires":{"config":["plugins.entries.voice-call.enabled"]}}}
---

# Voice Call

Use the voice-call plugin to start or inspect calls (Twilio, Telnyx, Plivo, or mock).

## CLI

```bash
zero voicecall call --to "+15555550123" --message "Hello from Zero"
zero voicecall status --call-id <id>
```

## Tool

Use `voice_call` for agent-initiated calls.

Actions:

- `initiate_call` (message, to?, mode?)
- `continue_call` (callId, message)
- `speak_to_user` (callId, message)
- `end_call` (callId)
- `get_status` (callId)

Notes:

- Requires the voice-call plugin to be enabled.
- Plugin config lives under `plugins.entries.voice-call.config`.
- Twilio config: `provider: "twilio"` + `twilio.accountSid/authToken` + `fromNumber`.
- Telnyx config: `provider: "telnyx"` + `telnyx.apiKey/connectionId` + `fromNumber`.
- Plivo config: `provider: "plivo"` + `plivo.authId/authToken` + `fromNumber`.
- Dev fallback: `provider: "mock"` (no network).
