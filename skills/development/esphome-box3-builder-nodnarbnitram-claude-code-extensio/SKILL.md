---
name: esphome-box3-builder
description: This skill should be used when the user asks to "configure esp32-s3-box-3", "set up box-3", "create box-3 voice assistant", "display lambda on box-3", "configure ili9xxx display", "set up gt911 touch", "configure i2s audio", "es7210 microphone", "es8311 speaker", "box-3 audio pipeline", or mentions error messages like "I2S DMA buffer error", "Touch not responding", "Display flicker", "Audio popping", "PSRAM not detected". Provides complete ESP32-S3-BOX-3 hardware templates, display lambda cookbook, touch patterns, and voice assistant configurations.
version: 0.1.0
allowed-tools: Read, Write, Edit, Grep, Glob, WebFetch, Bash
---

# ESP32-S3-BOX-3 Builder Skill

Specialist skill for ESP32-S3-BOX-3 hardware providing complete configuration templates, display lambda cookbook, touch interaction patterns, and voice assistant integration for complex audio/display/touch projects.

## Purpose

This skill accelerates ESP32-S3-BOX-3 development by providing:
- Complete hardware initialization templates
- Display lambda rendering cookbook (text, shapes, icons, multi-page UI)
- Audio pipeline recipes (I²S, ES7210 ADC, ES8311 DAC)
- Touch interaction patterns (buttons, swipes, gestures)
- Voice assistant integration (wake word, ducking, Home Assistant Assist)
- Material Design UI components
- Hardware-specific troubleshooting and workarounds

Use this skill for ESP32-S3-BOX-3 specific projects. For general ESPHome configuration, use the esphome-config-helper skill instead.

## When to Use This Skill

Use this skill when:
- Configuring ESP32-S3-BOX-3 hardware from scratch
- Implementing display lambda rendering (ILI9xxx)
- Setting up I²S audio pipeline (ES7210, ES8311)
- Configuring GT911 touch interaction
- Building voice assistant with wake word detection
- Creating multi-page touchscreen UI
- Troubleshooting BOX-3 specific issues

Delegate to specialized ESPHome agents for:
- Deep technical explanations (esphome-box3 agent)
- General ESPHome concepts (esphome-core agent)
- Network configuration (esphome-networking agent)

## Hardware Overview

The ESP32-S3-BOX-3 is a complete development kit with:
- **Module**: ESP32-S3-WROOM-1 (16MB Flash, 16MB Octal PSRAM)
- **Display**: ILI9342C (320x240, SPI, PSRAM required for 16-bit color)
- **Touch**: GT911 capacitive (I²C, multi-touch)
- **Microphone**: ES7210 4-channel ADC (I²S, 16kHz)
- **Speaker**: ES8311 mono DAC (I²S, 48kHz, requires MCLK)
- **Sensors**: BME688 environmental, ICM-42607-P IMU

**Critical Requirements**:
- PSRAM must be explicitly configured (2025.2+ breaking change)
- ESP-IDF framework recommended (better audio/display support)
- Shared I²S bus for microphone and speaker
- Reset pin GPIO48 shared between display and touch

For complete hardware specifications, consult:
- **`references/box3-pinout.md`** - Complete GPIO pinout, component addresses, known issues

## Configuration Templates

### Available Templates

Located in `templates/` directory:

1. **`box3-base.yaml`** - Hardware initialization foundation
   - ESP-IDF framework with PSRAM octal mode
   - I²S audio bus configuration
   - ES7210 ADC and ES8311 DAC setup
   - ILI9xxx display basic config
   - GT911 touch initialization
   - Use as foundation for all BOX-3 projects

2. **`box3-voice.yaml`** - Complete voice assistant
   - micro_wake_word with okay_nabu
   - Voice assistant pipeline (wake word → HA Assist → TTS)
   - Audio ducking with Nabu media player
   - State management for voice interaction
   - Use for voice-controlled BOX-3 projects

3. **`box3-display-ui.yaml`** - Multi-page touchscreen UI
   - 3-page navigation system
   - Touch zone binary sensors
   - Display lambda with Material Design
   - Page state management with globals
   - Use for interactive touchscreen projects

4. **`box3-audio-player.yaml`** - Music/media player
   - Media player entity
   - Volume control with touch buttons
   - Display showing playback status
   - Play/pause/skip controls
   - Use for audio playback projects

### Using Templates

To use a template:
1. Read the appropriate template file
2. Customize device name, WiFi credentials
3. Adjust UI elements, colors, fonts as needed
4. Flash using BOX-3 specific script (see Scripts section)

**Template Workflow:**
```yaml
# 1. Read template
cat .claude/skills/esphome-box3-builder/templates/box3-voice.yaml

# 2. Copy to project
cp .claude/skills/esphome-box3-builder/templates/box3-voice.yaml my-box3.yaml

# 3. Edit device-specific values
# - Update device name
# - Set WiFi credentials (use secrets.yaml)
# - Customize wake word model if desired
# - Adjust display text and layout

# 4. Flash with BOX-3 script
./.claude/skills/esphome-box3-builder/scripts/flash-box3.sh my-box3.yaml
```

## Display Lambda Rendering

### Lambda Rendering Cookbook

For complete display lambda examples and patterns, consult:
- **`references/display-lambdas.md`** - Display lambda cookbook
  - Text rendering (fonts, alignment, wrapping)
  - Shapes (rectangles, circles, lines)
  - Icons (Material Design Icons integration)
  - Images and sprites
  - Animation patterns
  - Multi-page navigation
  - Coordinate system and positioning

### Quick Display Patterns

**Basic Text Display**:
```cpp
it.printf(160, 10, id(roboto_16), TextAlign::TOP_CENTER, "ESP32-S3-BOX-3");
```

**Filled Rectangle (Card Background)**:
```cpp
it.filled_rectangle(10, 30, 300, 80, COLOR_PRIMARY);
```

**Multi-Line Text**:
```cpp
it.printf(20, 40, id(roboto_12), "Temperature: %.1f°C", id(temp_sensor).state);
it.printf(20, 60, id(roboto_12), "Humidity: %.1f%%", id(humidity_sensor).state);
```

**Icon Rendering** (Material Design Icons):
```cpp
// Requires MDI font in assets/fonts/
it.printf(30, 100, id(mdi_icons_24), "\U000F0425");  // thermometer icon
```

### Material Design UI Components

For Material Design color schemes, typography, and layouts, consult:
- **`references/material-design.md`** - Material Design UI guide
  - Color palette (primary, accent, background, text)
  - Typography hierarchy (headlines, body, captions)
  - Card layouts and spacing
  - Icon integration
  - Touch zone sizing (minimum 48x48 pixels)

### Font Integration

Required fonts are in `assets/fonts/`:
- **Roboto-Regular.ttf** - Material Design typography
- **materialdesignicons-webfont.ttf** - MDI icon font

**Font Configuration**:
```yaml
font:
  - file: .claude/skills/esphome-box3-builder/assets/fonts/Roboto-Regular.ttf
    id: roboto_16
    size: 16

  - file: .claude/skills/esphome-box3-builder/assets/fonts/materialdesignicons-webfont.ttf
    id: mdi_icons_24
    size: 24
    glyphs: [
      "\U000F0425",  # thermometer
      "\U000F050F",  # water-percent
      "\U000F0493",  # play
      "\U000F03E4",  # pause
    ]
```

Icon codepoints reference: `assets/fonts/mdi-codepoints.txt`

## Touch Interaction Patterns

### Touch Configuration

For complete touch patterns and gesture detection, consult:
- **`references/touch-patterns.md`** - Touch interaction patterns
  - Binary sensor zones for buttons
  - Swipe gesture detection
  - Long press patterns
  - Multi-touch handling
  - Page navigation integration

### Quick Touch Patterns

**Touch Button Zone**:
```yaml
binary_sensor:
  - platform: touchscreen
    name: "Button 1"
    x_min: 10
    x_max: 150
    y_min: 200
    y_max: 230
    on_press:
      - logger.log: "Button 1 pressed"
```

**Page Navigation**:
```yaml
binary_sensor:
  - platform: touchscreen
    name: "Next Page"
    x_min: 240
    x_max: 310
    y_min: 200
    y_max: 230
    on_press:
      - lambda: |-
          id(current_page) = (id(current_page) + 1) % 3;
          id(box3_display).show_page(id(current_page));
```

## Audio Pipeline Configuration

### I²S Audio Setup

**Shared I²S Bus** (LRCLK=GPIO45, BCLK=GPIO17, MCLK=GPIO2):
```yaml
i2s_audio:
  - id: i2s_shared
    i2s_lrclk_pin: GPIO45
    i2s_bclk_pin: GPIO17
    i2s_mclk_pin: GPIO2
```

**ES7210 Microphone ADC** (16kHz, GPIO16):
```yaml
audio_adc:
  - platform: es7210
    id: es7210_adc
    bits_per_sample: 16bit
    sample_rate: 16000
    mic_gain: 24DB
    address: 0x40

microphone:
  - platform: i2s_audio
    adc_type: external
    i2s_din_pin: GPIO16
    sample_rate: 16000
```

**ES8311 Speaker DAC** (48kHz, GPIO15, requires MCLK):
```yaml
audio_dac:
  - platform: es8311
    id: es8311_dac
    bits_per_sample: 16bit
    sample_rate: 48000
    use_mclk: true  # Required
    address: 0x18

speaker:
  - platform: i2s_audio
    dac_type: external
    i2s_dout_pin: GPIO15
    sample_rate: 48000
    buffer_duration: 100ms  # Prevents audio popping
```

## Voice Assistant Integration

### Wake Word Configuration

**micro_wake_word** (on-device detection):
```yaml
micro_wake_word:
  models:
    - model: okay_nabu  # or hey_jarvis, alexa, hey_mycroft
```

**Voice Assistant Pipeline**:
```yaml
voice_assistant:
  microphone: box_mic
  speaker: box_speaker
  noise_suppression_level: 1
  auto_gain: 31dBFS
  volume_multiplier: 2.0

  on_listening:
    - logger.log: "Listening..."

  on_tts_start:
    - logger.log: "Speaking..."

  on_end:
    - logger.log: "Done"
```

### Audio Ducking

**Nabu Media Player** (30dB reduction during voice):
```yaml
media_player:
  - platform: nabu
    name: "Media Player"
    on_play:
      - media_player.volume_set:
          volume: 70%  # Reduce to 70% when voice assistant active
```

## Scripts and Utilities

### BOX-3 Flashing Script

The validation and flashing utility provides BOX-3 specific workflow:

**Script**: `scripts/flash-box3.sh`

**Usage:**
```bash
# Validate, compile, and flash BOX-3
./.claude/skills/esphome-box3-builder/scripts/flash-box3.sh my-box3.yaml

# The script runs:
# 1. Validates configuration
# 2. Compiles firmware with BOX-3 optimizations
# 3. Flashes via USB (auto-detects /dev/ttyACM0 or /dev/ttyUSB0)
# 4. Monitors logs after flash
```

## Troubleshooting BOX-3 Issues

### Common BOX-3 Errors

**I²S DMA Buffer Error**:
- **Solution**: Increase `buffer_duration` to 100ms in speaker config

**Touch Not Responding**:
- **Solution**: Check GPIO48 reset pin (inverted: true, shared with display)

**Display Flicker**:
- **Solution**: Ensure PSRAM enabled with `color_palette: NONE`

**Audio Popping**:
- **Solution**: Verify sample rates (16kHz mic, 48kHz speaker), increase buffer_duration

**PSRAM Not Detected**:
- **Solution**: Confirm `psram: { mode: octal, speed: 80MHz }` in config

**Voice Assistant Crashes**:
- **Solution**: Disable Bluetooth/BLE completely (causes crashes on ESP32-S3)

**UI Freezing During OTA**:
- **Solution**: Add `execute_from_psram: true` in esp32.framework.advanced

For complete BOX-3 troubleshooting, consult:
- esphome-box3 agent (deep technical issues)
- `references/box3-pinout.md` (hardware-specific known issues section)

## Configuration Best Practices

### PSRAM Configuration (Critical)

**Always include explicit PSRAM config** (2025.2+ requirement):
```yaml
psram:
  mode: octal  # BOX-3 has 16MB Octal PSRAM
  speed: 80MHz
```

### ESP-IDF Framework (Recommended)

**Use ESP-IDF over Arduino** for BOX-3:
```yaml
esp32:
  board: esp32-s3-devkitc-1
  framework:
    type: esp-idf
    advanced:
      execute_from_psram: true  # Prevents UI freezing during OTA
```

### Display Configuration

**16-bit color requires PSRAM**:
```yaml
display:
  - platform: ili9xxx
    model: S3BOX
    color_palette: NONE  # Requires PSRAM (2025.2+)
    # ...
```

### Touch Configuration

**Shared reset pin with display**:
```yaml
touchscreen:
  - platform: gt911
    reset_pin:
      number: GPIO48
      inverted: true  # Shared with display reset
    interrupt_pin:
      number: GPIO3
      ignore_strapping_warning: true
```

## Integration with Other Skills and Agents

### When to Use Other Resources

- **General ESPHome config**: Use esphome-config-helper skill
  - Basic device setup
  - WiFi configuration
  - Common sensors (not BOX-3 specific)

- **Deep BOX-3 technical questions**: Delegate to esphome-box3 agent
  - Audio pipeline architecture
  - Display lambda API deep dive
  - Voice assistant tuning
  - Hardware-specific optimizations

- **ESPHome core concepts**: Delegate to esphome-core agent
  - YAML structure and organization
  - Substitutions and secrets
  - Package management

## Additional Resources

### Reference Files

For detailed BOX-3 information, consult:
- **`references/box3-pinout.md`** - Complete ESP32-S3-BOX-3 hardware reference with GPIO pinout, I²C addresses, component specifications, and known issues
- **`references/display-lambdas.md`** - Comprehensive display lambda cookbook with text rendering, shapes, icons, images, animation, and multi-page navigation patterns
- **`references/touch-patterns.md`** - Touch interaction patterns including button zones, swipe gestures, long press detection, and page navigation integration
- **`references/material-design.md`** - Material Design UI guide with color palette, typography hierarchy, card layouts, icon usage, and touch zone sizing guidelines

### Template Files

Complete working BOX-3 configurations in `templates/`:
- **`box3-base.yaml`** - Hardware initialization foundation
- **`box3-voice.yaml`** - Voice assistant with wake word
- **`box3-display-ui.yaml`** - Multi-page touchscreen UI
- **`box3-audio-player.yaml`** - Music/media player

### Asset Files

Material Design resources in `assets/`:
- **`fonts/Roboto-Regular.ttf`** - Material Design typography
- **`fonts/materialdesignicons-webfont.ttf`** - MDI icon font
- **`fonts/mdi-codepoints.txt`** - Icon codepoint reference

### Utility Scripts

Validation and flashing tools in `scripts/`:
- **`flash-box3.sh`** - BOX-3 specific validation and flashing workflow

## Quick Start Workflow

For new ESP32-S3-BOX-3 project:

1. **Select template** based on project type (base, voice, display-ui, audio-player)
2. **Copy template** to project directory
3. **Customize configuration**:
   - Update device name and WiFi credentials
   - Adjust display text, colors, layout
   - Modify touch zones for custom UI
   - Configure wake word model if using voice
4. **Add custom features** using references (display-lambdas.md, touch-patterns.md)
5. **Validate and flash** using `scripts/flash-box3.sh`
6. **Monitor logs** and troubleshoot if needed using reference guides

For adding to existing BOX-3 config:
1. **Consult references** for specific feature (display, touch, audio)
2. **Copy relevant code** from templates
3. **Integrate with existing config**
4. **Test incrementally** (add one feature at a time)
5. **Validate** before final flash

This skill provides rapid BOX-3 development for complex audio/display/touch projects. For general ESPHome configuration or deep technical questions, use the esphome-config-helper skill or delegate to ESPHome specialist agents.
