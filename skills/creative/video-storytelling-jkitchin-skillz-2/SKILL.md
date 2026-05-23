---
name: video-storytelling
description: |
  Create coherent video story sequences with AI-generated images and narrated audio.
  Combines image-generation and elevenlabs skills to produce complete video stories with
  visual and narrative consistency across all scenes. Maintains character appearance,
  style, lighting, and voice consistency throughout the story.

  Use this skill when the user requests:
  - Video stories with narration
  - Animated story sequences
  - Educational video content
  - Character-driven narratives with visuals
  - Multi-scene story videos
  - Narrated image sequences

  Features: Visual consistency locks, character persistence, multi-turn image generation,
  character voice narration, automatic video assembly

  Default: 1 title scene + 5 story scenes
  Dependencies: image-generation skill, elevenlabs skill, ffmpeg
allowed-tools: ["*"]
---

# Video Storytelling

## Purpose

This skill creates coherent video story sequences by combining AI-generated images with narrated audio. Acts as a story director and visual coordinator, maintaining perfect consistency across characters, visual style, lighting, and narrative tone throughout all scenes. Produces complete MP4 videos with synchronized images and character voiceovers.

## When to Use

This skill should be invoked when the user asks to:
- Create a video story or animated sequence
- Generate a narrated story with visuals
- Produce educational video content with characters
- Make a visual storybook with voiceover
- Create character-driven video narratives
- Generate multi-scene story videos
- Produce children's stories with pictures and narration

## Core Capabilities

### Visual Consistency System

**Global Style Lock:**
- Fixed aspect ratio, camera settings, lighting
- Consistent color palette across all scenes
- Uniform visual style and post-processing
- Prevents visual discontinuities

**Character Lock:**
- Maintains character appearance across scenes
- Same outfit, colors, facial features throughout
- Consistent accessories and distinctive traits
- Visual identity preservation

**Multi-Turn Image Generation:**
- Each scene references previous scene's image
- Builds visual continuity through the sequence
- Prevents character/style drift

### Narrative System

**Character Voices:**
- Maps characters to ElevenLabs voices
- Maintains voice consistency per character
- Supports multiple characters in dialogue

**Emotion Tags:**
- Expressive narration with emotion markers
- Sound effects and pauses
- Natural pacing and delivery

**Narrative Structure:**
- 50-80 words per scene (15-20 seconds)
- Neutral narrator for transitions
- Character-specific dialogue

### Video Assembly

**Automated Pipeline:**
- Generates all images in sequence
- Creates character voice narration
- Combines into synchronized MP4 video
- Equal time per scene based on total audio length

## Default Configuration

### Scene Structure
- **Default:** 1 title scene (scene 0) + 5 story scenes (scenes 1-5)
- **Total:** 6 scenes
- **Customizable:** User can specify different scene counts

### Default Style Lock

```
STYLE_LOCK:
- Aspect ratio: 1080×1080 (square)
- Camera: 50mm lens, eye-level perspective
- Lighting: soft three-point lighting, warm key light (4500K)
- Color palette: #0B5FFF, #FFB703, #FB8500, #023047, #8ECAE6
- Materials: matte finish, no film grain or heavy bloom
- Background: subtle gradient, clean composition
- Style: semi-realistic cartoon with clear lines and gentle shading
- Post: crisp focus, no vignette or text artifacts

NEGATIVE_LOCK:
no text errors, no misspellings, no watermarks, no stickers,
no extra characters, no visual noise, no drastic lighting changes
```

**Customization:** Users can override with custom style locks, but defaults ensure consistency.

### Default Voice Mapping

**From ElevenLabs Voices:**

**Narrators:**
- Neutral Narrator (male): George (`JBFqnCBsd6RMkjVDRZzb`)
- Neutral Narrator (female): Rachel (`21m00Tcm4TlvDq8ikWAM`)

**Character Voices:**
- Young Male (energetic): Josh (`TxGEqnHWrfWFTfGW9XjX`)
- Young Female (calm): Rachel (`21m00Tcm4TlvDq8ikWAM`)
- Young Female (expressive): Bella (`EXAVITQu4vr4xnSDxMaL`)
- Male (authoritative): Adam (`pNInz6obpgDQGcFmaJgB`)
- Female (warm): Matilda (`XrExE9yKIg1WjnnlVkGX`)
- Young Male (friendly): Antoni (`ErXwobaYiN019PkySvjV`)

**Assignment Logic:**
- If character gender/age specified, match to appropriate voice
- If unspecified, use Josh for male, Rachel for female
- Narrator defaults to George (male) or Rachel (female)

## Instructions

### Step 1: Gather Story Information

Collect necessary information from the user:

**Required:**
- **Story concept:** What is the story about?
- **Tone/Genre:** Educational, adventure, comedy, drama, etc.

**Optional (prompt if missing):**
- **Number of scenes:** Default is 6 (1 title + 5 story), but user can specify
- **Character descriptions:** Names, appearance, personality
- **Custom style locks:** Override defaults if user has specific requirements

**Example Prompts:**
```
"What's your story about?"
"How many scenes would you like? (Default: 1 title + 5 story scenes)"
"Describe your main character(s): name, appearance, personality"
"Any specific visual style preferences? (Default: semi-realistic cartoon)"
```

### Step 2: Define Characters

For each character in the story, create a character profile:

**Character Profile Template:**
```python
character = {
    "name": "Character Name",
    "species": "human/animal/creature",
    "description": "brief description",
    "colors": {
        "primary": "#HEX",
        "secondary": "#HEX"
    },
    "outfit": "clothing description",
    "features": ["distinctive trait 1", "trait 2", "trait 3"],
    "personality": "personality description",
    "voice_id": "elevenlabs-voice-id",
    "voice_name": "ElevenLabs voice name"
}
```

**Example:**
```python
pyter_python = {
    "name": "Pyter Python",
    "species": "friendly snake mascot",
    "description": "A cheerful coding mentor snake",
    "colors": {
        "body": "#0B5FFF",  # Blue
        "belly": "#FFB703"   # Yellow
    },
    "outfit": "tiny white lab coat with circular π logo",
    "features": ["large brown eyes", "rounded head", "cheerful smile"],
    "personality": "enthusiastic, helpful, curious",
    "voice_id": "TxGEqnHWrfWFTfGW9XjX",
    "voice_name": "Josh"
}
```

**Voice Assignment:**
- Ask user for voice preference or auto-assign based on character
- Use default mapping for common types
- Allow custom voice selection from ElevenLabs library

### Step 3: Plan Story Sequence

Create scene-by-scene outline:

**Scene 0 (Title Scene):**
- Visual: Title card with main character(s)
- Audio: Story introduction (narrator or main character)
- Duration: ~15-20 seconds

**Scenes 1-N (Story Scenes):**
- Visual: Sequential story moments
- Audio: Narrative with character dialogue
- Duration: ~15-20 seconds each

**Example Scene Plan:**
```python
scene_plan = [
    {
        "number": 0,
        "type": "title",
        "visual_description": "Pyter Python with laptop, 'Pyter's Coding Adventure' text overlay",
        "characters": ["Pyter Python"],
        "narrative": "[cheerful] Join Pyter Python on an exciting coding adventure!",
        "speaker": "Narrator",
        "voice_id": "JBFqnCBsd6RMkjVDRZzb"
    },
    {
        "number": 1,
        "type": "story",
        "visual_description": "Pyter at desk looking at computer screen showing error message, confused expression",
        "characters": ["Pyter Python"],
        "narrative": "[confused] Hmm... what does this error message mean? [pause] I thought my code was perfect!",
        "speaker": "Pyter Python",
        "voice_id": "TxGEqnHWrfWFTfGW9XjX"
    },
    # ... more scenes
]
```

### Step 4: Build Style and Character Locks

**Prepare Global Style Lock:**
```python
STYLE_LOCK = """
Aspect ratio: 1080×1080 (square)
Camera: 50mm lens, eye-level perspective
Lighting: soft three-point lighting, warm key light (4500K)
Color palette: #0B5FFF, #FFB703, #FB8500, #023047, #8ECAE6
Materials: matte finish, no film grain or heavy bloom
Background: subtle gradient, clean composition
Style: semi-realistic cartoon with clear lines and gentle shading
Post: crisp focus, no vignette or text artifacts
"""

NEGATIVE_LOCK = """
no text errors, no misspellings, no watermarks, no stickers,
no extra characters, no visual noise, no drastic lighting changes
"""
```

**Build Character Lock for Each Scene:**
```python
def build_character_lock(characters_in_scene):
    lock = ""
    for character in characters_in_scene:
        lock += f"""
Character: {character['name']}
Species: {character['species']}
Colors: body {character['colors']['primary']}, secondary {character['colors']['secondary']}
Outfit: {character['outfit']}
Key features: {', '.join(character['features'])}
"""
    return lock
```

### Step 5: Generate Image Sequence

Generate images using multi-turn generation for consistency:

**Implementation:**
```python
from pathlib import Path
import json

# Initialize tracking
previous_image_id = None
image_files = []

# Generate each scene
for scene in scene_plan:
    print(f"Generating Scene {scene['number']}: {scene['visual_description']}")

    # Build character lock for this scene
    character_lock = build_character_lock(
        [char_profiles[name] for name in scene['characters']]
    )

    # Build complete image prompt
    image_prompt = f"""
{STYLE_LOCK}

{character_lock}

Scene Description:
{scene['visual_description']}

{NEGATIVE_LOCK}
"""

    # Add reference to previous scene if not first scene
    if previous_image_id:
        image_prompt += f"\nReference previous scene for consistency: {previous_image_id}"

    # Generate image using image-generation skill
    # (This would invoke the image-generation skill)
    # For implementation, use appropriate model (DALL-E 3 or Gemini Pro)

    result = generate_image(
        prompt=image_prompt,
        model="dall-e-3",  # or gemini-3-pro-image-preview
        size="1024x1024",
        reference_image=previous_image_id
    )

    # Save image
    filename = f"scene-{scene['number']:02d}.png"
    save_image(result, filename)
    image_files.append(filename)

    # Track for next scene reference
    previous_image_id = result['image_id']

    print(f"  ✓ Saved: {filename}")
```

**Key Points:**
- Scene 0 generates base image
- Scenes 1+ reference previous scene for consistency
- Apply STYLE_LOCK and CHARACTER_LOCK to every prompt
- Save with sequential numbering

### Step 6: Generate Narrative Audio

Create voice narration for each scene:

**Implementation:**
```python
from elevenlabs.client import ElevenLabs

client = ElevenLabs(api_key=os.environ['ELEVENLABS_API_KEY'])
audio_files = []

for scene in scene_plan:
    print(f"Generating audio for Scene {scene['number']}")

    # Prepare dialogue input
    dialogue_input = {
        "text": scene['narrative'],
        "name": scene['speaker'],
        "voice_id": scene['voice_id']
    }

    # Generate audio using text_to_dialogue
    audio = client.text_to_dialogue.convert(
        inputs=[dialogue_input]
    )

    # Save audio file
    filename = f"scene-{scene['number']:02d}.mp3"
    with open(filename, 'wb') as f:
        for chunk in audio:
            f.write(chunk)

    audio_files.append(filename)
    print(f"  ✓ Saved: {filename}")
```

**Narrative Guidelines:**
- 50-80 words per scene
- Use emotion tags: `[excited]`, `[thoughtful]`, `[confused]`, `[pause]`
- Include sound effects when appropriate: `[sound effect: door creaking]`
- Vary pacing with pauses

### Step 7: Concatenate Audio

Combine all scene audio into single track:

**Implementation:**
```python
import subprocess

# Build ffmpeg concat command
concat_filter = "concat=n={}:v=0:a=1[out]".format(len(audio_files))

inputs = []
for audio_file in audio_files:
    inputs.extend(['-i', audio_file])

cmd = ['ffmpeg', '-y'] + inputs + [
    '-filter_complex', concat_filter,
    '-map', '[out]',
    'full_audio.mp3'
]

subprocess.run(cmd, check=True)
print("✓ Audio concatenated: full_audio.mp3")
```

### Step 8: Assemble Final Video

Use the included `assemble_video.sh` script:

**Implementation:**
```python
import subprocess
from pathlib import Path

# Prepare command
script_path = Path(__file__).parent / "scripts" / "assemble_video.sh"
cmd = [str(script_path), "full_audio.mp3"] + image_files

# Run assembly
subprocess.run(cmd, check=True)

# Output will be full_audio.mp4
print("✓ Video created: full_audio.mp4")
```

**Script Details:**
- Calculates equal time per image based on total audio length
- Creates video segment for each image
- Ensures all images are exactly 1080×1080 (pads if needed)
- Concatenates segments
- Muxes with audio track
- Outputs high-quality MP4 with H.264

### Step 9: Deliver Results

Provide user with:
1. **Final video file:** `<story-name>.mp4`
2. **Scene breakdown:** Summary of each scene
3. **Individual assets:** Images and audio files (if requested)
4. **Story metadata:** Character profiles, scene plan (if requested)

**Example Output:**
```
✓ Video Story Created: pyter-coding-adventure.mp4

Scenes:
  0. Title: "Pyter's Coding Adventure" (20s)
  1. Pyter encounters an error (18s)
  2. Pyter realizes the mistake (17s)
  3. Pyter fixes the code (19s)
  4. Code runs successfully (16s)
  5. Pyter celebrates (15s)

Total Duration: 1:45
Resolution: 1080×1080
Characters: Pyter Python (voiced by Josh)

Files generated:
  - pyter-coding-adventure.mp4 (final video)
  - scene-00.png through scene-05.png (images)
  - scene-00.mp3 through scene-05.mp3 (audio)
  - full_audio.mp3 (concatenated audio)
```

## Character Voice Reference

### ElevenLabs Voice IDs

**Narrators:**
- **George** (male, middle-aged, narrative): `JBFqnCBsd6RMkjVDRZzb`
- **Rachel** (female, young, calm): `21m00Tcm4TlvDq8ikWAM`

**Young Characters:**
- **Josh** (male, energetic): `TxGEqnHWrfWFTfGW9XjX`
- **Bella** (female, expressive): `EXAVITQu4vr4xnSDxMaL`
- **Antoni** (male, friendly): `ErXwobaYiN019PkySvjV`
- **Elli** (female, emotional): `MF3mGyEYCl7XYWbV9V6O`

**Adult Characters:**
- **Adam** (male, authoritative): `pNInz6obpgDQGcFmaJgB`
- **Domi** (female, confident): `AZnzlk1XvdvUeBnXmlld`
- **Matilda** (female, warm): `XrExE9yKIg1WjnnlVkGX`

**Assignment Strategy:**
```python
def assign_voice(character):
    """Auto-assign voice based on character attributes"""

    # Check for explicit assignment
    if 'voice_preference' in character:
        return get_voice_id(character['voice_preference'])

    # Auto-assign based on attributes
    age = character.get('age', 'young')
    gender = character.get('gender', 'male')

    if age == 'young':
        if gender == 'male':
            return 'TxGEqnHWrfWFTfGW9XjX'  # Josh
        else:
            return '21m00Tcm4TlvDq8ikWAM'  # Rachel
    else:  # adult
        if gender == 'male':
            return 'pNInz6obpgDQGcFmaJgB'  # Adam
        else:
            return 'XrExE9yKIg1WjnnlVkGX'  # Matilda
```

## Example Story Generation

### Complete Example: "Pyter's First Bug"

**User Request:** "Create a short story about a coding snake fixing his first bug"

**Step 1: Character Definition**
```python
pyter = {
    "name": "Pyter Python",
    "species": "friendly snake",
    "colors": {"body": "#0B5FFF", "belly": "#FFB703"},
    "outfit": "white lab coat with π logo",
    "features": ["large brown eyes", "rounded head", "cheerful smile"],
    "personality": "enthusiastic learner",
    "voice_id": "TxGEqnHWrfWFTfGW9XjX"  # Josh
}
```

**Step 2: Scene Plan**
```python
scenes = [
    {
        "number": 0,
        "visual": "Pyter with laptop, title 'Pyter's First Bug'",
        "narrative": "[cheerful] Today, Pyter Python will fix his very first coding bug!",
        "speaker": "Narrator",
        "voice_id": "JBFqnCBsd6RMkjVDRZzb"
    },
    {
        "number": 1,
        "visual": "Pyter staring at screen with red error message",
        "narrative": "[confused] Wait... why isn't my code working? [pause] The computer says there's a syntax error!",
        "speaker": "Pyter",
        "voice_id": "TxGEqnHWrfWFTfGW9XjX"
    },
    {
        "number": 2,
        "visual": "Pyter reading a Python book, thoughtful",
        "narrative": "[thoughtful] Let me check the Python book... [pause] Oh! I need to look at line 5 carefully.",
        "speaker": "Pyter",
        "voice_id": "TxGEqnHWrfWFTfGW9XjX"
    },
    {
        "number": 3,
        "visual": "Close-up of Pyter pointing at screen, realization",
        "narrative": "[excited] I found it! I forgot to close the parentheses! [pause] That's the bug!",
        "speaker": "Pyter",
        "voice_id": "TxGEqnHWrfWFTfGW9XjX"
    },
    {
        "number": 4,
        "visual": "Screen showing 'Success!' with green checkmark",
        "narrative": "[proud] I fixed it! My code is running perfectly now!",
        "speaker": "Pyter",
        "voice_id": "TxGEqnHWrfWFTfGW9XjX"
    },
    {
        "number": 5,
        "visual": "Pyter celebrating, confetti in background",
        "narrative": "[warm] And that's how Pyter learned that every programmer makes mistakes... and that's okay!",
        "speaker": "Narrator",
        "voice_id": "JBFqnCBsd6RMkjVDRZzb"
    }
]
```

**Step 3: Generate** (using process described above)

**Output:** `pyters-first-bug.mp4` with 6 scenes, ~90 seconds total

## Requirements

**Skills:**
- `image-generation` - For creating consistent visual scenes
- `elevenlabs` - For character voice narration

**Python Packages:**
```bash
pip install elevenlabs pillow
```

**System:**
- Python 3.8+
- ffmpeg (for video assembly)
- Bash shell (for assemble_video.sh script)
- 2GB+ free disk space (for temporary files)

**API Keys:**
- OpenAI or Google (for image generation)
- ElevenLabs (for voice narration)

**File Permissions:**
- Execute permission for `assemble_video.sh`

## Best Practices

### Story Planning

1. **Keep it Simple:**
   - Start with 6 scenes (1 title + 5 story)
   - Clear beginning, middle, end
   - Single main character for first stories

2. **Character Consistency:**
   - Define characters completely before starting
   - Use distinctive visual features
   - Maintain outfit/colors throughout

3. **Pacing:**
   - 15-20 seconds per scene ideal
   - Use pauses for dramatic effect
   - Vary emotion tags for expressiveness

### Visual Consistency

1. **Use Style Locks:**
   - Apply to every scene without exception
   - Don't modify mid-story
   - Custom locks should be complete, not partial

2. **Character Locks:**
   - Specify colors with hex codes
   - List 3-5 distinctive features
   - Include outfit details

3. **Multi-Turn References:**
   - Always reference previous scene
   - Mention "maintain character appearance"
   - Note "same lighting and style"

### Audio Quality

1. **Narrative Guidelines:**
   - Write naturally for speech
   - Use emotion tags sparingly (1-2 per scene)
   - Include pauses for pacing

2. **Voice Selection:**
   - Match voice to character age/personality
   - Keep narrator voice neutral
   - Maintain voice consistency per character

3. **Audio Testing:**
   - Generate one scene first to test
   - Verify voice/emotion match intent
   - Adjust before generating all scenes

### Video Assembly

1. **File Organization:**
   - Use consistent naming (scene-XX.png/mp3)
   - Keep in flat directory structure
   - Clean up temp files after assembly

2. **Quality Settings:**
   - Default 1080×1080 ensures quality
   - H.264 baseline profile for compatibility
   - AAC audio at 192kbps

3. **Testing:**
   - Verify all images are same size
   - Check audio files are valid
   - Test script with 2-3 scenes first

## Troubleshooting

### Visual Inconsistencies

**Problem:** Character looks different across scenes

**Solutions:**
- Ensure character lock is applied to every prompt
- Verify previous image is referenced
- Add "maintain exact character appearance from previous scene"
- Use more specific color hex codes

### Audio Issues

**Problem:** Voice doesn't match character

**Solutions:**
- Verify voice_id is correct
- Test voice with sample text first
- Check character voice assignment logic

**Problem:** Concatenated audio has gaps

**Solutions:**
- Ensure all audio files are valid MP3
- Check ffmpeg concat filter syntax
- Verify no missing scene audio files

### Video Assembly Errors

**Problem:** Script fails with "file not found"

**Solutions:**
- Verify all image files exist
- Check audio file path
- Ensure script has execute permissions

**Problem:** Images different sizes in video

**Solutions:**
- Verify all images are 1080×1080
- Check image generation settings
- Script auto-pads, but prefer exact size

## Limitations

1. **Scene Count:**
   - Practical limit: 10-12 scenes (video length ~3 minutes)
   - More scenes = longer generation time
   - Audio/video file size considerations

2. **Character Complexity:**
   - 1-3 main characters recommended
   - Too many characters = harder consistency
   - Background characters okay if not detailed

3. **Visual Changes:**
   - Can't change style mid-story
   - Character outfit changes require new character lock
   - Major scene changes (day/night) may reduce consistency

4. **Audio Length:**
   - Each scene 15-20 seconds ideal
   - Very short scenes (<10s) feel rushed
   - Very long scenes (>30s) slow pacing

5. **Processing Time:**
   - Image generation: 30-60s per scene
   - Audio generation: 10-20s per scene
   - Video assembly: 30-60s total
   - Total: ~10-15 minutes for 6-scene story

## Related Skills

- `image-generation` - Required for visual generation
- `elevenlabs` - Required for voice narration
- `python-plotting` - For visualizing story analytics
- `scientific-writing` - For writing narrative scripts

## Additional Resources

- **Image Generation Skill**: See `image-generation/SKILL.md`
- **ElevenLabs Skill**: See `elevenlabs/SKILL.md`
- **Style Lock Reference**: See `references/style-locks.md`
- **Narrative Design**: See `references/narrative-design.md`
- **Video Assembly**: See `references/video-assembly.md`
- **Example Stories**: See `examples/example-stories.md`
