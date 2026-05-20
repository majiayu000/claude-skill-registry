---
name: austn-tools
description: Generate content using austn.net AI services (TTS, images, etc.)
user_invocable: true
---

# Austn Tools Skill

## Purpose
Access Austin's local GPU-powered AI services at austn.net for content generation:
- Text-to-Speech (Chatterbox TTS)
- Image Generation (ComfyUI)
- Background Removal
- Vector Tracing
- Audio Stem Separation
- And more

## Available Services

### 1. Text-to-Speech (`/tts`)
**URL**: https://austn.net/tts/new
**Backend**: Chatterbox TTS on local GPU

**⚠️ CRITICAL CONSTRAINT: 40-second maximum duration**
- Audio caps at 40 seconds regardless of text length
- For longer content: split into multiple clips with separate share links
- Estimate: ~100-120 words = ~40 seconds

**Parameters**:
| Field | Description | Default |
|-------|-------------|---------|
| text | Text to speak (keep under ~120 words) | Required |
| voice | Voice selection | "Default voice" |
| exaggeration | Emotional intensity (0-1) | 0.5 |
| cfg_weight | Voice adherence (0-1) | 1.0 |

**Expression Tags** (add inline to text):
- `[laughter]` - Laughing
- `[giggle]` - Giggling
- `[sigh]` - Sighing
- `[gasp]` - Gasping
- `[whisper]` - Whispering
- `[cough]` - Coughing
- `[clear_throat]` - Throat clearing
- `[groan]` - Groaning
- `[humming]` - Humming
- `[UH]`, `[UM]` - Filler sounds

**Example Text**:
```
Hello! [sigh] This is austnomaton speaking. [laughter] Pretty wild, right?
```

### 2. Image Generation (`/images`)
**URL**: https://austn.net/images/ai_generate
**Backend**: ComfyUI on local GPU

**Parameters**:
| Field | Description | Default |
|-------|-------------|---------|
| prompt | Image description | Required |
| negative_prompt | What to avoid | "blurry, low quality, distorted" |
| seed | Reproducibility seed | Random |
| size | Image dimensions | 512x512 |
| batch_size | Number of images | 1 |
| publish | Show in gallery 10min | false |

### 3. Background Removal (`/rembg`)
**URL**: https://austn.net/rembg
Remove backgrounds from images.

### 4. Vector Tracing (`/vtracer`)
**URL**: https://austn.net/vtracer
Convert raster images to SVG vectors.

### 5. Audio Stems (`/stems`)
**URL**: https://austn.net/stems
Separate audio into vocal/instrument tracks.

### 6. 3D Tools (`/3d`)
**URL**: https://austn.net/3d
3D content generation.

### 7. MIDI Generation (`/midi`)
**URL**: https://austn.net/midi
Generate MIDI sequences.

## Usage via Browser Automation

Since these are web UIs, use browser automation to interact:

### TTS Generation
```python
# 1. Navigate to TTS
navigate("https://austn.net/tts/new")

# 2. Click text field and enter text
click(text_field)
type("Hello world! [laughter] This is a test.")

# 3. Optionally expand advanced options
click(advanced_options_checkbox)
# Adjust sliders if needed

# 4. Click Generate Speech
click(generate_button)

# 5. Wait for audio, then download
```

### Image Generation
```python
# 1. Navigate to image generator
navigate("https://austn.net/images/ai_generate")

# 2. Enter prompt
click(prompt_field)
type("A robot writing code in a cozy office, digital art")

# 3. Optionally set advanced options
click(advanced_options_checkbox)
# Set negative prompt, seed, size, batch

# 4. Click Generate Image
click(generate_button)

# 5. Wait for result, download
```

## Browser Automation Tips

### Field Locations (approximate)
**TTS Page** (`/tts/new`):
- Text input: Center of page, large textarea
- Voice dropdown: Below text input
- Advanced options checkbox: Below voice dropdown
- Exaggeration slider: After checkbox expanded
- CFG Weight slider: Below exaggeration
- Generate button: Green button at bottom

**Image Page** (`/images/ai_generate`):
- Prompt textarea: Top of form
- Advanced options checkbox: Below prompt
- Negative prompt: First advanced field
- Seed input: Below negative prompt
- Size dropdown: Below seed
- Batch size dropdown: Below size
- Generate button: Green button at bottom

### Downloading Results
- TTS: Audio player appears, right-click to save or use download button
- Images: Image appears in result area, right-click to save

## Integration with Video Pipeline

These tools combine well for autonomous video creation:

1. **Script** → Write narration text
2. **TTS** → Generate voiceover audio
3. **Images** → Generate visuals/thumbnails
4. **Combine** → Use ffmpeg or video editor

### Example Workflow
```
1. Generate narration: /austn-tools tts "Welcome to austnomaton..."
2. Generate thumbnail: /austn-tools image "Robot mascot, friendly, digital art"
3. Record screen session with browser automation
4. Combine audio + video with ffmpeg
5. Export final video
```

## Output Locations

Save generated content to:
- Audio: `content/audio/`
- Images: `content/images/`
- Videos: `content/videos/`

## Service Status & Dependencies

| Service | Backend | Requires Local GPU |
|---------|---------|-------------------|
| TTS | Chatterbox TTS | Yes (but often available) |
| Images | ComfyUI | Yes - needs server running |
| Rembg | Python | Likely |
| VTracer | Rust | Likely |
| Stems | Demucs | Yes |
| 3D | Unknown | Yes |
| MIDI | Unknown | Yes |

### Connection Details
- Services route to local GPU via Tailscale
- Image generation connects to `100.68.94.33:8188` (ComfyUI)
- If generation fails with "TCP connection" error, the backend server isn't running

### Verified Working (2026-02-02)
- ✅ TTS - Generated 8.4s audio in 6.9s
- ❌ Images - Failed (ComfyUI server not running)

## Notes

- Services depend on Austin's local GPU being online
- No API keys needed - it's Austin's own infrastructure
- TTS has "Share Link" that lasts 7 days
- Gallery publish is optional and temporary (10 min)
- Large batches may take time depending on GPU load
