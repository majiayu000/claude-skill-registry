---
name: skyrim-audio
description: Handle Skyrim audio files including FUZ, XWM, and WAV formats. Use when the user wants to inspect audio, extract voice files, create FUZ files, or convert audio formats.
---

# Skyrim Audio Module

Handle Skyrim audio file operations including FUZ, XWM, and WAV formats using Spooky's AutoMod Toolkit.

## Prerequisites

Run all commands from the toolkit directory:
```bash
cd "<TOOLKIT_PATH>"
# Example: cd "C:\Tools\spookys-automod-toolkit"
```

## Overview

Skyrim uses several audio formats:

| Format | Extension | Purpose |
|--------|-----------|---------|
| FUZ | .fuz | Combined voice audio + lip sync |
| XWM | .xwm | Compressed audio (xWMA codec) |
| WAV | .wav | Uncompressed audio |
| LIP | .lip | Lip sync data |

Voice files are typically stored as FUZ (XWM audio + LIP lip sync combined).

## Command Reference

### Get Audio Info
```bash
dotnet run --project src/SpookysAutomod.Cli -- audio info "<audio>"
```
| Input | Description |
|-------|-------------|
| `<audio>` | Path to .fuz, .xwm, or .wav file |

Output includes: File type, file size, audio data size, lip sync presence (for FUZ).

### Extract FUZ
```bash
dotnet run --project src/SpookysAutomod.Cli -- audio extract-fuz "<fuz>" --output "<dir>"
```
Extracts FUZ into XWM and LIP components.

| Option | Description |
|--------|-------------|
| `--output`, `-o` | Output directory |

Output files:
- `filename.xwm` - Audio data
- `filename.lip` - Lip sync data (if present)

### Create FUZ
```bash
dotnet run --project src/SpookysAutomod.Cli -- audio create-fuz "<xwm>" --output "<file>" [options]
```
| Option | Description |
|--------|-------------|
| `<xwm>` | Path to XWM audio file |
| `--output`, `-o` | Output FUZ file path |
| `--lip` | Path to LIP file (optional) |

### Convert WAV to XWM
```bash
dotnet run --project src/SpookysAutomod.Cli -- audio wav-to-xwm "<wav>" --output "<file>"
```
| Option | Description |
|--------|-------------|
| `<wav>` | Path to WAV file |
| `--output`, `-o` | Output XWM file path |

**WAV Requirements:**
- PCM format
- 16-bit
- Mono or stereo
- 44100 Hz recommended for voice

## Common Workflows

### Inspect Voice File
```bash
# Check FUZ file info
dotnet run --project src/SpookysAutomod.Cli -- audio info "./Sound/Voice/MyMod.esp/NPC/Line01.fuz"

# Check if it has lip sync data
# Output will show hasLipSync: true/false
```

### Extract Existing Voice Files for Analysis
```bash
# 1. Extract from BSA if needed
dotnet run --project src/SpookysAutomod.Cli -- archive extract "SomeMod.bsa" --output "./Extracted" --filter "sound/*"

# 2. Extract FUZ to components
dotnet run --project src/SpookysAutomod.Cli -- audio extract-fuz "./Extracted/Sound/Voice/SomeMod.esp/NPC/Line01.fuz" --output "./AudioDebug"

# Creates:
#   ./AudioDebug/Line01.xwm
#   ./AudioDebug/Line01.lip (if present)
```

### Create Voice Line (Full Workflow)
```bash
# 1. Record/obtain WAV file (44100 Hz, 16-bit, mono recommended)

# 2. Convert WAV to XWM
dotnet run --project src/SpookysAutomod.Cli -- audio wav-to-xwm "./Source/Line01.wav" --output "./Audio/Line01.xwm"

# 3. Generate LIP file (requires FaceFX or external tool - not included)
#    Or use existing LIP from similar dialogue

# 4. Create FUZ with lip sync
dotnet run --project src/SpookysAutomod.Cli -- audio create-fuz "./Audio/Line01.xwm" --lip "./Audio/Line01.lip" --output "./Sound/Voice/MyMod.esp/NPC/Line01.fuz"

# Or without lip sync (for sound effects)
dotnet run --project src/SpookysAutomod.Cli -- audio create-fuz "./Audio/Line01.xwm" --output "./Sound/Voice/MyMod.esp/NPC/Line01.fuz"
```

### Create Sound Effect (No Lip Sync)
```bash
# 1. Convert WAV to XWM
dotnet run --project src/SpookysAutomod.Cli -- audio wav-to-xwm "./Source/effect.wav" --output "./Sound/FX/MyMod/effect.xwm"

# Or package as FUZ without LIP (some mods prefer this)
dotnet run --project src/SpookysAutomod.Cli -- audio wav-to-xwm "./Source/effect.wav" --output "./temp/effect.xwm"
dotnet run --project src/SpookysAutomod.Cli -- audio create-fuz "./temp/effect.xwm" --output "./Sound/FX/MyMod/effect.fuz"
```

### Batch Extract Voice Files
```bash
# Extract all FUZ files from a mod's BSA
dotnet run --project src/SpookysAutomod.Cli -- archive extract "VoiceMod.bsa" --output "./Extracted" --filter "*.fuz"

# Then extract each FUZ individually to analyze
# (Loop through files in script)
```

## Voice File Organization

Skyrim expects voice files in specific locations:
```
Data/
  Sound/
    Voice/
      MyMod.esp/              # Must match plugin name exactly
        NPC_EditorID/         # Must match NPC's Editor ID
          DialogueTopic_ResponseNumber.fuz
```

Example path:
```
Data/Sound/Voice/MyMod.esp/MerchantBob/DialogueMerchantGreeting_00001234_1.fuz
```

### Voice File Naming Convention
```
<TopicEditorID>_<FormID>_<ResponseNumber>.fuz
```
- `TopicEditorID` - The dialogue topic's Editor ID
- `FormID` - 8-digit hex form ID of the dialogue response
- `ResponseNumber` - Response index (usually 1)

## FUZ File Format

FUZ files combine audio and lip sync:
```
Header:
  Magic: "FUZE" (4 bytes)
  Version: uint32
  LIP size: uint32

Data:
  LIP data: [LIP size bytes]
  XWM data: [remaining bytes]
```

## Audio Recommendations

### For Voice Lines
- Sample Rate: 44100 Hz
- Bit Depth: 16-bit
- Channels: Mono (recommended) or Stereo
- Format: PCM WAV before conversion

### For Sound Effects
- Sample Rate: 44100 Hz or 22050 Hz
- Bit Depth: 16-bit
- Channels: Mono or Stereo depending on effect
- Format: PCM WAV before conversion

### For Music
- Sample Rate: 44100 Hz
- Bit Depth: 16-bit
- Channels: Stereo
- Format: Use XWM or vanilla formats

## Limitations

This module **CAN**:
- Read FUZ/XWM/WAV file information
- Extract FUZ to components
- Create FUZ from components
- Convert WAV to XWM

This module **CANNOT**:
- Generate LIP (lip sync) files
- Convert XWM back to WAV
- Edit audio content
- Generate voice from text

For LIP generation, use:
- **FaceFX** (included with Creation Kit)
- **LipGen** community tools
- **xVASynth** for AI voice generation (separate tool)

## Important Notes

1. **LIP files required for good lip sync** - Without LIP, NPCs won't move lips
2. **Path must match plugin name** - `Sound/Voice/PluginName.esp/`
3. **NPC folder must match Editor ID** - Case sensitive
4. **FUZ preferred for voice** - Combines audio and lip sync cleanly
5. **Use `--json` flag** for machine-readable output when scripting

## JSON Output

All commands support `--json` for structured output:
```bash
dotnet run --project src/SpookysAutomod.Cli -- audio info "./Sound/Voice/MyMod/Line01.fuz" --json
```

Example response:
```json
{
  "success": true,
  "result": {
    "fileName": "Line01.fuz",
    "type": "FUZ",
    "fileSize": 45678,
    "audioSize": 42000,
    "hasLipSync": true,
    "lipSyncSize": 3678,
    "sampleRate": 44100,
    "channels": 1,
    "bitsPerSample": 16
  }
}
```
