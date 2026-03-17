---
name: ha-voice
description: "Configure Home Assistant Assist voice control with pipelines, intents, wake words, and speech processing. Use when setting up voice control, creating custom intents, configuring TTS/STT, or building voice satellites. Activates on keywords: Assist, voice control, wake word, intent, sentence, TTS, STT, Piper, Whisper, Wyoming."
---

# Home Assistant Voice Control

> Configure Assist pipelines, custom intents, wake words, speech processing, and voice satellites for local voice control.

## Quick Start

### Setting up Assist Pipeline

```yaml
# configuration.yaml
assist_pipeline:
  pipelines:
    - language: en
      name: Default Pipeline
      stt_engine: faster_whisper  # Local STT
      tts_engine: tts.piper       # Local TTS
      conversation_engine: conversation.home_assistant
      wake_word_entity: binary_sensor.wake_word
```

**Why this matters:** The pipeline connects all components (STT, TTS, intent, conversation agent) into a single voice workflow.

### Creating Custom Intents

```yaml
# custom_sentences/en/turn_on.yaml
language: en
version: 1

intents:
  TurnOn:
    data:
      - sentences:
          - "turn on the [area] {name:list}"
          - "turn on {name:list}"
          - "[please] activate {name:list}"
        lists:
          name: light_names

lists:
  light_names:
    - "bedroom light"
    - "kitchen overhead"
    - "living room"
```

**Why this matters:** Custom sentence patterns enable natural voice commands tailored to your home.

### Configuring Text-to-Speech (TTS)

**Local Option - Piper:**
```yaml
tts:
  - platform: piper
    language: en_GB
    voice: jenny_dioco
```

**Cloud Option - OpenAI:**
```yaml
tts:
  - platform: tts
    service: google_translate_say  # or openai, google cloud
    language: en
```

**Why this matters:** TTS gives voice feedback; local options require no cloud dependencies.

### Configuring Speech-to-Text (STT)

**Local Option - Faster Whisper:**
```yaml
stt:
  - platform: faster_whisper
    language: en
```

**Cloud Option - Google Cloud Speech:**
```yaml
stt:
  - platform: google_cloud
    language_code: en-US
```

**Why this matters:** STT converts spoken commands to text; local options provide privacy.

## Critical Rules

### ✅ Always Do

- ✅ Use `custom_sentences/` directory for intent configuration (not deprecated `sentences/`)
- ✅ Test intents with Assist Developer Tools before deploying
- ✅ Use `{name:list}` syntax for slot-based entity matching
- ✅ Configure both STT and TTS engines in the same pipeline
- ✅ Verify wake word entity exists before enabling in pipeline
- ✅ Document intent lists so voice commands are discoverable

### ❌ Never Do

- ❌ Don't hardcode entity IDs in sentence patterns (use lists and slots)
- ❌ Don't forget `version: 1` in custom_sentences YAML files
- ❌ Don't mix old `sentences/` directory with new `custom_sentences/` (use `custom_sentences/` only)
- ❌ Don't enable Piper TTS without adequate disk space (models are 100+ MB)
- ❌ Don't use wildcard `{query}` for every slot (makes intents ambiguous)
- ❌ Don't skip testing with Assist Developer Tools

### Common Mistakes

**❌ Wrong - Hardcoded entity IDs:**
```yaml
intents:
  TurnOn:
    data:
      - sentences:
          - "turn on light.bedroom"
          - "turn on light.kitchen"
```

**✅ Correct - Using slot lists:**
```yaml
intents:
  TurnOn:
    data:
      - sentences:
          - "turn on [the] {name:list}"
        lists:
          name: light_names

lists:
  light_names:
    - "bedroom"
    - "kitchen"
```

**Why:** Lists are dynamic and can be generated from Home Assistant entities programmatically.

## Sentence Pattern Syntax

### Slots

**Named slots** match list values:
```yaml
sentences:
  - "turn on {name:list}"  # Matches list value, captures as 'name' slot
```

### Lists

**List matching** provides slot values:
```yaml
lists:
  room:
    - "bedroom"
    - "kitchen"
    - "living room"
```

### Optional Groups

**Square brackets** make words optional:
```yaml
sentences:
  - "[please] turn on the {name:list}"
  - "activate [the] {device:list}"
```

### Wildcards

**Wildcard slots** capture any text:
```yaml
sentences:
  - "remind me {reminder:text}"  # Captures any text as 'reminder'
  - "set a timer for {duration:text}"
```

### Combined Pattern Example

```yaml
intents:
  TurnOn:
    data:
      - sentences:
          - "[please] [turn on | switch on | activate] [the] {area} {name:list}"
          - "[please] turn on {name:list}"
          - "activate {name:list} [in the] {room:list}"
        lists:
          name: light_names
          room: room_names

  Reminder:
    data:
      - sentences:
          - "remind me {reminder:text}"
          - "[please] [create | set] a reminder [for me] [to] {reminder:text}"

lists:
  light_names:
    - "bedroom light"
    - "kitchen overhead"
    - "living room lamps"
  room_names:
    - "bedroom"
    - "kitchen"
    - "living room"
```

**Why this matters:** Flexible patterns enable natural phrasing while maintaining intent recognition accuracy.

## Built-In Intents Reference

Home Assistant provides default intents:

### Navigation Intents
- `HassTurnOn` / `HassTurnOff` - Control devices
- `HassToggle` - Toggle switches/lights
- `HassOpenCover` / `HassCloseCover` - Control covers
- `HassSetClimate` - Control climate (heat/cool)

### Information Intents
- `HassGetState` - Get entity state
- `HassGetHistory` - Query automation history

### Home Control Intents
- `HassArmAlarm` / `HassDisarmAlarm` - Arm/disarm alarms
- `HassLockDoor` / `HassUnlockDoor` - Control locks

### Custom Intents
You create additional intents in `custom_sentences/` by defining new intent blocks:
```yaml
intents:
  CustomIntentName:
    data:
      - sentences: [...]
```

## Wake Word Configuration

### openWakeWord (Local)
```yaml
conversation:
  engine: openai

# Enable openWakeWord
binary_sensor:
  - platform: openwakeword
    models:
      - alexa    # "Alexa, help"
      - hey_google  # "Hey Google, ..."
      - hey_siri
```

### Porcupine (Local, Paid)
```yaml
binary_sensor:
  - platform: porcupine
    access_key: !secret porcupine_key
    keywords:
      - hey_home_assistant
```

## Voice Satellite Setup

### Hardware Requirements
- **Microphone:** INMP441 (I2S digital) or similar
- **Speaker:** MAX98357A amplifier or similar
- **Board:** ESP32-S3, ESP32-S3-BOX-3 preferred
- **Connectivity:** WiFi required

### ESPHome Voice Assistant Config

```yaml
# ESPHome device
packages:
  voice_assistant: !include packages/voice_assistant.yaml

# Or inline configuration:
i2s_audio:
  i2s_lrclk_pin: GPIO33
  i2s_bclk_pin: GPIO34
  i2s_mclk_pin: GPIO32

microphone:
  - platform: i2s_audio
    id: mic
    adc_type: external
    i2s_din_pin: GPIO35
    pdm: false

speaker:
  - platform: i2s_audio
    id: speaker
    dac_type: external
    i2s_dout_pin: GPIO36
    mode: mono

voice_assistant:
  microphone: mic
  speaker: speaker
  noise_suppression_level: 2
  auto_gain: 80dB
  volume_multiplier: 0.8
```

**Why this matters:** Voice satellites extend Assist to multiple rooms with local processing.

## Speech Processing Configuration

### Language Support

**Full Support (20+ languages):** en, de, fr, it, es, nl, pl, pt, ru, sv, tr, uk, zh, ja, ko, and more

**Partial Support (40+ languages):** Regional variants and additional languages with varying STT/TTS availability

**Community Support (80+ languages):** Community-contributed sentence templates

**Language Config:**
```yaml
assist_pipeline:
  pipelines:
    - language: de  # German
      name: Deutsche Pipeline
      tts_engine: tts.piper  # Set voice per language
```

### Performance Tuning

**STT (Faster Whisper):**
```yaml
stt:
  - platform: faster_whisper
    language: en
    model: base  # tiny, base, small, medium, large
    acceleration: gpu  # CPU or GPU
```

**TTS (Piper):**
```yaml
tts:
  - platform: piper
    voice: en_GB-jenny
    rate: 11025  # Audio sample rate
    volume_normalize: true
```

### Conversation Agent Integration

**Built-in Agent:**
```yaml
conversation:
  engine: home_assistant
```

**OpenAI Agent:**
```yaml
conversation:
  engine: openai
  api_key: !secret openai_api_key
  model: gpt-4
```

**Custom Conversation Agent:**
```yaml
conversation:
  engine: custom
  module: custom_components.my_agent
```

## Common Intent Patterns

### Device Control Pattern
```yaml
intents:
  TurnOn:
    data:
      - sentences:
          - "turn on [the] {name:list}"
          - "[please] activate {name:list}"
        lists:
          name: light_names
```

### Climate Control Pattern
```yaml
intents:
  SetClimate:
    data:
      - sentences:
          - "set [the] {room:list} [thermostat] to {temp:number} degrees"
          - "make it {temp:number} in [the] {room:list}"
        lists:
          room: room_names
```

### Query Pattern
```yaml
intents:
  GetState:
    data:
      - sentences:
          - "what is the temperature [in the] {room:list}"
          - "is [the] {name:list} on"
        lists:
          room: room_names
          name: device_names
```

## Testing with Developer Tools

1. Go to **Developer Tools** → **Assist**
2. Enter test sentence: "turn on the bedroom light"
3. Check:
   - ✅ Intent matched correctly
   - ✅ Slots extracted properly
   - ✅ Audio plays (if TTS configured)
4. Debug mismatches by:
   - Reviewing sentence patterns
   - Checking list values
   - Verifying slot names

## Troubleshooting

### Intent Not Recognized

**Symptoms:** Voice command doesn't match any intent

**Solution:**
```yaml
# Check custom_sentences directory structure
ls -R config/custom_sentences/

# Verify YAML syntax
cat config/custom_sentences/en/custom.yaml

# Test in Assist Developer Tools with exact phrase
# Adjust sentence patterns to match expected phrasing
```

### TTS/STT Engine Not Working

**Symptoms:** "Engine not available" error in Assist

**Solution:**
```yaml
# Verify engine is configured
service: tts.piper  # Must exist

# Check dependencies installed
pip install piper-tts  # for Piper
pip install faster-whisper  # for Whisper

# Restart Home Assistant to load engines
```

### Wake Word Not Triggering

**Symptoms:** Binary sensor stays off despite noise

**Solution:**
```yaml
# Verify entity_id is correct
service: homeassistant.update_entity
target:
  entity_id: binary_sensor.wake_word

# Check binary sensor configuration
# Review noise levels and model sensitivity
# Test microphone separately
```

### Voice Satellite Connection Issues

**Symptoms:** ESP32 disconnects from WiFi or Assist pipeline

**Solution:**
```bash
# Check WiFi signal strength in ESPHome logs
# Reduce WiFi distance or add access point
# Update ESPHome firmware
esphome run voice_assistant.yaml --upload-speed 115200
```

## Dependencies

### Required

| Component | Version | Purpose |
|-----------|---------|---------|
| Home Assistant | 2024.1+ | Assist platform |
| Faster Whisper | 0.5+ | Local STT engine |
| Piper TTS | 1.0+ | Local TTS engine |

### Optional

| Component | Version | Purpose |
|-----------|---------|---------|
| OpenWakeWord | 0.3+ | Wake word detection |
| Porcupine | Latest | Premium wake word |
| ESPHome | 2024.1+ | Voice satellite devices |

## Official Documentation

- [Home Assistant Voice Control](https://www.home-assistant.io/voice_control/)
- [Assist Pipeline Configuration](https://www.home-assistant.io/integrations/assist_pipeline/)
- [Intent Recognition Guide](https://developers.home-assistant.io/docs/voice/intent-recognition)
- [Conversation Integration](https://www.home-assistant.io/integrations/conversation/)

## Setup Checklist

Before using voice commands, verify:

- [ ] Assist pipeline configured with STT, TTS, and conversation engine
- [ ] `custom_sentences/en/` directory created with intent definitions
- [ ] Sentence patterns tested in Assist Developer Tools
- [ ] Wake word entity exists (if using wake word)
- [ ] Microphone and speaker working (test via Developer Tools)
- [ ] Intent lists contain correct entity aliases
- [ ] Language setting matches your configuration
- [ ] All YAML syntax is valid (no tabs, proper indentation)
