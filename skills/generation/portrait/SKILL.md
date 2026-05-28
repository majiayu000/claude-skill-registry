---
name: portrait
description: Generate character portraits using Gemini NanoBanana. Reads from character YAML and calls gemini directly with full guardrails.
allowed-tools: Bash, Read, Glob, Write
user-invocable: true
proactive: false
---

# Portrait Generation

Generate character portraits using Gemini's NanoBanana extension. Reads character appearance from YAML files and builds explicit prompts with all guardrails to prevent style drift.

## Usage

```
/portrait <character_name>
/portrait cipher
/portrait elder_kara
/portrait vex --regenerate
```

## How It Works

1. Read the character YAML from `assets/characters/{name}.yaml`
2. Build an explicit prompt with all guardrails
3. Call `gemini --yolo -e nanobanana` directly via Bash
4. Handle the nanobanana-output fallback if needed
5. Report success with the file path

## Step 1: Find and Read Character YAML

Look for the character file:
```
C:\dev\SENTINEL\assets\characters\{name}.yaml
C:\dev\SENTINEL\assets\characters\{name}_detailed.yaml
```

If not found, ask the user if they want to create one.

## Step 2: Build the Prompt

### Required Structure

```
Cinematic portrait, photorealistic digital art style.
Modern post-apocalyptic cyberpunk aesthetic. NOT fantasy, NOT medieval, NOT anime, NOT elf, NOT blue hair.
[EXPLICIT_PERSON_DESCRIPTOR] with [BUILD] build, [HAIR_DESCRIPTION], [EYE_DESCRIPTION], [FACIAL_FEATURES], [DISTINGUISHING_MARKS], [EXPRESSION].
[FACTION] [ROLE] survivor. [FACTION_GEAR].
Dark atmospheric background with [FACTION_COLOR] accent lighting.
High detail, dramatic rim lighting, shallow depth of field.
Bust framing, 3/4 angle, looking slightly off-camera.
Save the image to C:\dev\SENTINEL\assets\portraits\npcs\{name}.png
```

### Person Descriptor Mapping (CRITICAL)

Build explicit descriptors to anchor generation. DO NOT use vague terms.

| Skin Tone | Gender: Masculine | Gender: Feminine | Gender: Androgynous |
|-----------|-------------------|------------------|---------------------|
| pale | pale-skinned white man | pale-skinned white woman | pale-skinned person |
| light | light-skinned white man | light-skinned white woman | light-skinned person |
| medium | olive-skinned man | olive-skinned woman | olive-skinned person |
| tan | tan Latino man | tan Latina woman | tan person |
| brown | Black man | Black woman | Black person |
| dark | dark-skinned Black man | dark-skinned Black woman | dark-skinned Black person |

For elderly characters, prepend "elderly" (e.g., "elderly olive-skinned woman").

### Faction Colors

| Faction | Color | Hex | Gear Description |
|---------|-------|-----|------------------|
| nexus | blue | #00A8E8 | Data visors, sensor arrays, sleek tech fabric |
| ember_colonies | orange | #E85D04 | Salvaged leather, wool layers, fire-scarred gear |
| lattice | yellow | #FFD000 | Work gear, tool belts, utility harness |
| convergence | purple | #7B2CBF | Bio-tech integration, visible augmentations |
| covenant | white | #E8E8E8 | Clean white/silver cloth, formal bearing |
| wanderers | tan | #C9A227 | Dust cloaks, travel packs, road-worn appearance |
| cultivators | green | #2D6A4F | Natural fibers, soil-stained hands |
| steel_syndicate | gunmetal | #5C677D | Heavy armor layers, tactical gear, intimidating |
| witnesses | sepia | #8B4513 | Document satchels, ink-stained fingers |
| architects | cyan | #0077B6 | Pre-collapse uniforms, credential badges |
| ghost_networks | black | #0D0D0D | Nondescript dark clothing, deep shadows |

### Expression Mapping

| YAML Value | Prompt Description |
|------------|-------------------|
| neutral | calm alert expression |
| wary | wary guarded expression |
| warm | warm approachable expression |
| stern | stern serious expression |
| tired | tired world-weary expression |

## Step 3: Execute Generation

Run the command directly via Bash:

```bash
gemini --yolo -e nanobanana "Generate a portrait image: [FULL_PROMPT]"
```

Use a 3-minute timeout (180000ms).

## Step 4: Handle Output

NanoBanana sometimes saves to `nanobanana-output/` instead of the requested path.

1. Check if file exists at `assets/portraits/npcs/{name}.png`
2. If not, check `nanobanana-output/` for recent PNG files
3. Move the most recent one to the correct location:
   ```bash
   mv "C:/dev/SENTINEL/nanobanana-output/[filename].png" "C:/dev/SENTINEL/assets/portraits/npcs/{name}.png"
   ```

## Step 5: Report Result

Show the user the generated portrait using the Read tool on the PNG file.

## Example: Full Prompt for Cipher

Character YAML:
```yaml
name: Cipher
faction: nexus
role: analyst
gender: masculine
age: adult
skin_tone: brown
build: lean
hair_color: black
hair_length: short
hair_style: dreadlocks
eye_color: augmented
facial_features: [sharp, high cheekbones]
augmentations: subtle blue data overlay in eyes, small temple implant
other_features: always wears a data visor
default_expression: neutral
```

Generated prompt:
```
Cinematic portrait, photorealistic digital art style.
Modern post-apocalyptic cyberpunk aesthetic. NOT fantasy, NOT medieval, NOT anime, NOT elf, NOT blue hair.
Black man with lean build, short black dreadlocks, cybernetic eyes with subtle blue data overlay, sharp features, high cheekbones, small temple implant, always wears a data visor, calm alert expression.
Nexus analyst survivor. Data visors, sensor arrays, sleek tech fabric.
Dark atmospheric background with blue (#00A8E8) accent lighting.
High detail, dramatic rim lighting, shallow depth of field.
Bust framing, 3/4 angle, looking slightly off-camera.
Save the image to C:\dev\SENTINEL\assets\portraits\npcs\cipher.png
```

## Error Handling

- **YAML not found**: Ask user if they want to create one with `/portrait create {name}`
- **Gemini not available**: Report error, suggest checking Gemini CLI installation
- **Generation fails**: Show error output, suggest retrying
- **Wrong style generated**: Regenerate with stronger guardrails (add more NOT constraints)

## Creating New Characters

If the user wants to create a new character:

1. Ask for the key details (or use the table format from create_character.py)
2. Create the YAML file in `assets/characters/{name}.yaml`
3. Generate the portrait

Or direct them to run:
```bash
python scripts/create_character.py
```
