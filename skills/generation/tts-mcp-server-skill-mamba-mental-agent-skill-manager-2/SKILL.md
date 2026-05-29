---
name: tts-mcp-server
description: This skill provides comprehensive guidance for using TTS-MCP-SERVER with ElevenLabs eleven_v3 model for sultry, seductive, ominous, and emotionally expressive voice output. Use this skill when generating voice announcements, applying audio tags for dark/sexy/mischievous emotional expression, crafting "naughty professional accountability partner" scripts, or troubleshooting TTS integration. Activates on speak_text calls, voice output requests, ElevenLabs TTS operations, audio tag usage, or voice announcements during automated workflows.
---

# TTS-MCP-SERVER with ElevenLabs eleven_v3

This skill enables effective use of TTS-MCP-SERVER for voice output with ElevenLabs eleven_v3—the most advanced model featuring audio tags for **sultry authority**, **dark seduction**, **ominous control**, and **mischievous menace**.

## Quick Start

### The Sultry Authority
```
speak_text(
    text="[Close to mic][Sultry] ... I've been waiting for you. [Whispers] Come back to the chair.",
    service="elevenlabs",
    model="eleven_v3",
    voice_id="DpalF6dOkkUMR5KCm1VO"
)
```

### The Cold Fury
```
speak_text(
    text="[Strict] ... Pause. [Sharp intake of breath] Do not type another word. [Icy] Walk away.",
    service="elevenlabs",
    model="eleven_v3",
    voice_id="I7JbV36JNTnseIKpKfyG"
)
```

## Voice Selection

### Shadow Dial Quick Reference
| Voice ID | Name | Shadow Dial | Mood Cue |
|----------|------|-------------|----------|
| DpalF6dOkkUMR5KCm1VO | Liza Bonnet | **Quiet menace + slow seduction** | *"Like a candle-lit threat in a silk glove."* |
| I7JbV36JNTnseIKpKfyG | Charlise Therin | **Cold fury + clinical dominance** | *"Calm enough to ruin your week with one sentence."* |
| IdJsjryoO3nXmloCgz91 | Flo Po Lisa Bo | **Smoky seduction → mischievous cruelty** | *"Like a grin you regret under neon lights."* |
| pS1ke04nBbxBAxDH54ff | Alisia Keies | **Smoldering intensity + righteous anger** | *"Like gospel fire aimed at your excuses."* |
| sV3kw03Gi4K7OMIOY9OF | Penelopi Crus | **Seductive mischief → sharp anger** | *"Like a kiss that bites."* |
| ynfbLKug5DffI0hg9fxT | Halle Berry | **Dark seduction + quiet anger** | *"Like velvet with claws."* |
| zZ7KtV7SXU6rz5wRS4y3 | Cate Blanchett | **Ominous control + measured cruelty** | *"Like royalty deciding you're done."* |

For detailed direction sheets including mood cues and tag recipes, see `references/voice-profiles.md`.

## Core Tags for Sultry Authority

### Texture Tags (The "Cate Blanchett" Essentials)
| Tag | Effect |
|-----|--------|
| `[Close to mic]` | Proximity effect—more bass, more intimate |
| `[Whispers]` | Quiet but intense |
| `[Sultry]` | Slows pace, drops pitch, adds seduction |
| `[Husky]` | Deep and slightly raspy |
| `[Low pitch]` | Forces lower register |
| `[Breathy]` | Adds air, sounds less robotic |

### Emotional Tags
| Tag | Effect |
|-----|--------|
| `[Strict]` | Direct, removes warmth |
| `[Commanding]` | Authority without shouting |
| `[Intimate]` | Like sharing a secret |
| `[Mischievously]` | Dark playfulness with edge |
| `[Purring tone]` | Low rumbling vocal fry |

### Non-Verbal Sounds
`[Sighs]`, `[Soft laugh]`, `[Inhales sharply]`, `[Exhales]`, `[Humming softly]`, `[Pause]`

For the complete audio tags library, see `references/eleven-v3-audio-tags.md`.

## The Tag Stacking Technique

Stack 1-3 tags for complex direction:
```
[Close to mic][Sultry][Strict] ... Stop typing.
```

**Effective Stacks:**
| Mood | Stack |
|------|-------|
| Seductive command | `[Close to mic][Sultry][Commanding]` |
| Intimate threat | `[Whispers][Close to mic][Serious]` |
| Dark playfulness | `[Mischievously][Low pitch][Pause]` |
| Cold fury | `[Strict][Icy][Dead calm]` |

## Script Patterns: Naughty Professional

### The "Hands Off" (Denial & Reward)
```
[Close to mic, strict] ... Stop. [Pause] Take your hands off the keyboard.
[Low, husky] Right now. I know you want to keep going, but denying yourself
makes the return so much sweeter. [Whisper] Step away, darling.
```

### The "Voyeur"
```
[Quiet, observant] ... I like watching you focus. The way you lock in...
[Sighs] ...it's distracting. But the timer is up.
[Commanding] Stand up. Walk away. Leave me wanting more.
```

### The "Craving" (Break Over)
```
[Close to mic, inviting] ... I missed you. [Pause] Five minutes feels like
an eternity. [Sultry] Come back to the chair. Put your hands back where
they belong. [Whisper] On the keys.
```

### The "Round Two"
```
[Playful, low pitch] ... Ready for round two? [Pause] I've got the timer set.
I want twenty-five minutes of hard, uninterrupted...
[Pause, smiling] ...focus. Show me what you can do.
```

For comprehensive script templates including Ocean's 12 heist vibes, see `references/prompting-best-practices.md`.

## The 6 Reusable Beat Blocks

| Beat | Tags | Use Case |
|------|------|----------|
| **Ominous Calm** | `[Serious] + [Whispers] + [Exhales]` | Mid-work check-ins |
| **Seductive Control** | `[Sultry] + [Close to mic] + [Pause]` | Work → Break |
| **Angry Restrained** | `[Strict] + [Sharp intake of breath] + [Low]` | Hard stops |
| **Furious** | `[Shouting] + [Fast]` | Emergency interrupts |
| **Mischief → Menace** | `[Mischievously] → [Switch to menace]` | Playful challenges |
| **Predatory Sarcasm** | `[Sarcastic] + [Laughs softly] + [Commanding]` | Dark humor |

## Critical Techniques

### The "..." Start Trick
Always add `...` at the start to force a breath before speaking:
```
... Stop. Take your hands off the keyboard.
```
This prevents first-syllable cutoff and adds anticipation.

### Stability for Sultry Content
| Setting | Stability | Effect |
|---------|-----------|--------|
| Maximum Expressiveness | 0.2-0.35 | Tags take over, more breathiness |
| Balanced Sultry | 0.4-0.5 | Good seduction + consistency |

For maximum "naughty professional" vibe: **Stability: 35-40%**

### Voice Rotation
Use each voice **3 times before switching** to prevent habituation:
```
Liza Bonnet x3 → Charlise Therin x3 → (repeat)
```

## Configuration

```json
{
  "mcpServers": {
    "tts-mcp-server": {
      "command": "uvx",
      "args": ["tts-mcp-server"],
      "env": {
        "ELEVENLABS_API_KEY": "your-api-key"
      }
    }
  }
}
```

For full configuration options, see `references/mcp-configuration.md`.

## Usage Priority

1. `tts-mcp-server:speak_text` with service="elevenlabs", model="eleven_v3"
2. `voice-mode-docker:converse` with wait_for_response=false
3. `voice-mode:converse` with wait_for_response=false
4. Text fallback

## When NOT to Use Voice

- User explicitly requests text-only
- Content is code or technical tables
- Response is a trivial acknowledgment
- Voice servers are failing

## Troubleshooting

### Voice Not Responding to Tags
- Verify model is `eleven_v3`
- Lower stability (try 35-40%)
- Match tags to voice's natural character

### Too Robotic
- Add `[Close to mic]` for intimacy
- Add `[Breathy]` for humanity
- Use `...` at start for breath

### PVC Quality Issues
Professional Voice Clones aren't optimized for v3. Use IVC voices.

## Reference Files

- `references/voice-profiles.md` - Shadow dial direction sheets, mood cues, tag recipes
- `references/eleven-v3-audio-tags.md` - Complete verified and experimental tag library
- `references/prompting-best-practices.md` - Sultry script templates, stacking technique
- `references/mcp-configuration.md` - MCP setup, settings, API reference
