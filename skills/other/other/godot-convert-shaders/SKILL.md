---
name: godot-convert-shaders
version: 1.0.0
displayName: "Godot 3.x to 4.x Shader Converter"
description: >
  Converts Godot 3.x shader code to Godot 4.x shader syntax. Updates SCREEN_TEXTURE
  to screen_texture uniform, DEPTH_TEXTURE to depth_texture uniform, texture() function
  changes, built-in varyings updates, and light function signature changes. Essential
  for rendering and visual effect migrations.
author: "Asreonn"
license: MIT
category: game-development
type: tool
difficulty: advanced
audience: [developers, technical-artists, migrators]
keywords:
  - godot
  - shader
  - shaders
  - conversion
  - migration
  - godot3
  - godot4
  - screen_texture
  - depth_texture
  - texture
  - glsl
  - visual-effects
platforms: [macos, linux, windows]
repository: https://github.com/asreonn/godot-superpowers
homepage: https://github.com/asreonn/godot-superpowers#readme
filesystem:
  read:
    - "${PROJECT_ROOT}/**/*.gdshader"
    - "${PROJECT_ROOT}/**/*.shader"
    - "${PROJECT_ROOT}/project.godot"
  write:
    - "${PROJECT_ROOT}/**/*.gdshader"
    - "${PROJECT_ROOT}/**/*.shader"
  deny:
    - "**/.env*"
    - "**/secrets*"
    - "**/*.key"
behavior:
  timeout: 300
  retry: 2
  cache: true
  interactive: true
---

# Godot 3.x to 4.x Shader Converter

**Converts Godot 3.x shader code to Godot 4.x shader syntax.**

## Core Conversions

This skill performs five key shader modernizations:

| Godot 3.x | Godot 4.x | Type |
|-----------|-----------|------|
| `SCREEN_TEXTURE` | `uniform sampler2D screen_texture` | Screen sampling |
| `DEPTH_TEXTURE` | `uniform sampler2D depth_texture` | Depth sampling |
| `texture(SCREEN_TEXTURE, ...)` | `textureLod(screen_texture, ...)` | Texture sampling |
| `varying` → `VARIABLE` | `varying` → `variable` | Built-in varyings |
| `light()` signature | `light()` with new params | Light functions |

---

## UPON INVOCATION - START HERE

When this skill is invoked, IMMEDIATELY execute:

### 1. Verify Godot Project (5 seconds)

```bash
ls project.godot 2>/dev/null && echo "✓ Godot project detected" || echo "✗ Not a Godot project"
```

**If NOT a Godot project:**
- Inform user this skill only works on Godot projects
- STOP here

**If IS a Godot project:**
- Proceed to step 2

### 2. Detect Shader Files (10 seconds)

```bash
# Find all shader files
echo "=== Detecting Shader Files ==="
echo ".gdshader files (Godot 4.x format):"
find . -name "*.gdshader" -type f | wc -l

echo ".shader files (Godot 3.x format):"
find . -name "*.shader" -type f | wc -l
```

### 3. Detect Godot 3.x Patterns (15 seconds)

```bash
echo "=== Detecting Godot 3.x Shader Patterns ==="

echo "SCREEN_TEXTURE references:"
grep -rn "SCREEN_TEXTURE" --include="*.shader" --include="*.gdshader" . 2>/dev/null | wc -l

echo "DEPTH_TEXTURE references:"
grep -rn "DEPTH_TEXTURE" --include="*.shader" --include="*.gdshader" . 2>/dev/null | wc -l

echo "texture() with hint_screen_texture:"
grep -rn "hint_screen_texture" --include="*.shader" --include="*.gdshader" . 2>/dev/null | wc -l

echo "Built-in varying uppercase (VERTEX, UV, COLOR):"
grep -rn "^varying.*VERTEX\|^varying.*UV\|^varying.*COLOR" --include="*.shader" --include="*.gdshader" . 2>/dev/null | wc -l

echo "Light functions (light():"
grep -rn "^void light()" --include="*.shader" --include="*.gdshader" . 2>/dev/null | wc -l
echo "Light functions with old signature:"
grep -rn "light.*DIFFUSE\|light.*SPECULAR" --include="*.shader" --include="*.gdshader" . 2>/dev/null | wc -l
```

### 4. Present Findings

Show the user:
```
=== Godot 4.x Shader Conversion Analysis ===

Project: [project name]
Shaders to convert:
- .shader files (Godot 3.x): X
- .gdshader files: X

Patterns requiring conversion:
- SCREEN_TEXTURE usage: X
- DEPTH_TEXTURE usage: X
- hint_screen_texture uniforms: X
- Built-in varyings (uppercase): X
- Light function signatures: X

Total shaders to update: X

Conversion includes:
✓ SCREEN_TEXTURE → screen_texture uniform
✓ DEPTH_TEXTURE → depth_texture uniform
✓ texture() → textureLod() for screen/depth
✓ Varying built-ins → lowercase
✓ Light function parameters → new signature
✓ File extension .shader → .gdshader
✓ Git commit per file
✓ Backup before changes

Would you like me to:
1. Convert all shaders (recommended)
2. Show detailed breakdown first
3. Select specific conversions
4. Cancel
```

### 5. Wait for User Choice

- **If 1 (Proceed):** Start Phase 2 immediately
- **If 2 (Details):** Show file-by-file breakdown, then offer to proceed
- **If 3 (Selective):** Ask which conversions to apply
- **If 4 (Cancel):** Exit skill

---

## Phase 1: Analysis & Inventory

### 1.1 Create Shader Inventory

```bash
# Find all shader files (both .shader and .gdshader)
find . -name "*.shader" -o -name "*.gdshader" | sort > /tmp/shader_files.txt
wc -l /tmp/shader_files.txt
echo "shader files found"
```

### 1.2 Analyze Each Shader

For each shader file, detect patterns:

```bash
# Analyze patterns per file
for file in $(cat /tmp/shader_files.txt); do
    echo "=== $file ==="
    grep -c "SCREEN_TEXTURE" "$file" 2>/dev/null || echo 0
    grep -c "DEPTH_TEXTURE" "$file" 2>/dev/null || echo 0
    grep -c "hint_screen_texture" "$file" 2>/dev/null || echo 0
    grep -c "^void light()" "$file" 2>/dev/null || echo 0
    # Check if .shader extension (needs rename)
    [[ "$file" == *.shader ]] && echo "RENAME_NEEDED" || echo "EXTENSION_OK"
done
```

### 1.3 Create Conversion Plan

```
Shader Conversion Plan:
=======================

1. SCREEN_TEXTURE → screen_texture (X files)
2. DEPTH_TEXTURE → depth_texture (X files)
3. texture() → textureLod() (X files)
4. Built-in varyings lowercase (X files)
5. Light function signatures (X files)
6. File extension .shader → .gdshader (X files)

Total files to modify: X
Estimated time: Auto (user doesn't wait)
Backup created: YES (git tag)
Rollback available: YES
```

---

## Phase 2: Conversion Operations

### Conversion A: SCREEN_TEXTURE → screen_texture uniform

**Detection:**
```bash
grep -rn "SCREEN_TEXTURE" --include="*.shader" --include="*.gdshader" .
```

**Transformation Process:**

1. **Add uniform declaration at top of shader:**
   ```glsl
   // Add near top of file, after shader_type
   uniform sampler2D screen_texture : hint_screen_texture, filter_linear_mipmap;
   ```

2. **Replace SCREEN_TEXTURE references:**
   ```glsl
   // Before (Godot 3.x)
   vec4 screen_color = texture(SCREEN_TEXTURE, SCREEN_UV);
   
   // After (Godot 4.x)
   vec4 screen_color = textureLod(screen_texture, SCREEN_UV, 0.0);
   ```

**Mapping Table:**

| Godot 3.x | Godot 4.x |
|-----------|-----------|
| `SCREEN_TEXTURE` | `screen_texture` (uniform) |
| `texture(SCREEN_TEXTURE, uv)` | `textureLod(screen_texture, uv, 0.0)` |
| `texture(SCREEN_TEXTURE, uv, lod)` | `textureLod(screen_texture, uv, lod)` |

**Important:** Use `textureLod()` instead of `texture()` for screen and depth textures in Godot 4.x to ensure correct mipmap behavior.

---

### Conversion B: DEPTH_TEXTURE → depth_texture uniform

**Detection:**
```bash
grep -rn "DEPTH_TEXTURE" --include="*.shader" --include="*.gdshader" .
```

**Transformation Process:**

1. **Add uniform declaration at top of shader:**
   ```glsl
   // Add near top of file, after shader_type
   uniform sampler2D depth_texture : hint_depth_texture, filter_linear_mipmap;
   ```

2. **Replace DEPTH_TEXTURE references:**
   ```glsl
   // Before (Godot 3.x)
   float depth = texture(DEPTH_TEXTURE, SCREEN_UV).r;
   
   // After (Godot 4.x)
   float depth = textureLod(depth_texture, SCREEN_UV, 0.0).r;
   ```

**Mapping Table:**

| Godot 3.x | Godot 4.x |
|-----------|-----------|
| `DEPTH_TEXTURE` | `depth_texture` (uniform) |
| `texture(DEPTH_TEXTURE, uv)` | `textureLod(depth_texture, uv, 0.0)` |
| `texture(DEPTH_TEXTURE, uv, lod)` | `textureLod(depth_texture, uv, lod)` |

---

### Conversion C: texture() Function Changes

**Detection:**
```bash
grep -rn "texture(SCREEN_TEXTURE\|texture(DEPTH_TEXTURE" --include="*.shader" --include="*.gdshader" .
```

**Core Changes:**

Godot 4.x requires `textureLod()` for screen and depth textures to ensure explicit mipmap level control:

```glsl
// Godot 3.x - implicit LOD
vec4 color = texture(SCREEN_TEXTURE, uv);

// Godot 4.x - explicit LOD
uniform sampler2D screen_texture : hint_screen_texture, filter_linear_mipmap;
vec4 color = textureLod(screen_texture, uv, 0.0);
```

**Conversion Pattern:**

| Pattern | Replacement |
|---------|-------------|
| `texture(SCREEN_TEXTURE, UV)` | `textureLod(screen_texture, UV, 0.0)` |
| `texture(SCREEN_TEXTURE, UV, 2.0)` | `textureLod(screen_texture, UV, 2.0)` |
| `texture(DEPTH_TEXTURE, UV)` | `textureLod(depth_texture, UV, 0.0)` |
| `texture(DEPTH_TEXTURE, UV, lod)` | `textureLod(depth_texture, UV, lod)` |

---

### Conversion D: Built-in Varyings (Uppercase → Lowercase)

**Detection:**
```bash
grep -rn "^varying.*VERTEX\|^varying.*UV\|^varying.*COLOR\|^varying.*NORMAL" --include="*.shader" --include="*.gdshader" .
```

**Built-in Varying Changes:**

In Godot 3.x, built-in varyings like `VERTEX`, `UV`, `COLOR` were accessed as-is.
In Godot 4.x, when you declare your own `varying`, the built-ins become lowercase in the fragment shader.

**Mapping Table:**

| Declared Varying | Godot 3.x Fragment | Godot 4.x Fragment |
|------------------|-------------------|-------------------|
| `varying vec2 my_uv` | `my_uv` (unchanged) | `my_uv` (unchanged) |
| Built-in `VERTEX` | `VERTEX` | `vertex` |
| Built-in `UV` | `UV` | `uv` |
| Built-in `COLOR` | `COLOR` | `color` |
| Built-in `NORMAL` | `NORMAL` | `normal` |

**Important:** Only built-in varyings change to lowercase. User-declared varyings keep their original case.

**Example:**
```glsl
// Before (Godot 3.x)
shader_type spatial;
varying vec2 custom_uv;

void vertex() {
    custom_uv = UV;  // UV is uppercase built-in
    VERTEX.y += 1.0; // VERTEX is uppercase
}

void fragment() {
    ALBEDO = texture(TEXTURE, custom_uv).rgb;
    if (VERTEX.y > 0.0) {  // VERTEX still uppercase in vertex(), but...
        // In Godot 4.x, would be 'vertex' in fragment()
    }
}

// After (Godot 4.x)
shader_type spatial;
varying vec2 custom_uv;

void vertex() {
    custom_uv = uv;  // uv is lowercase built-in
    vertex.y += 1.0; // vertex is lowercase
}

void fragment() {
    ALBEDO = texture(TEXTURE, custom_uv).rgb;  // custom_uv unchanged
    if (vertex.y > 0.0) {  // vertex is lowercase in fragment()
        
    }
}
```

---

### Conversion E: Light Function Signature Changes

**Detection:**
```bash
grep -rn "^void light()" --include="*.shader" --include="*.gdshader" .
grep -rn "light.*DIFFUSE\|light.*SPECULAR\|light.*ATTENUATION" --include="*.shader" --include="*.gdshader" .
```

**Light Function Changes:**

Godot 4.x changes how light calculations are accessed within the `light()` function.

**Mapping Table:**

| Godot 3.x | Godot 4.x |
|-----------|-----------|
| `DIFFUSE` | `diffuse_light` |
| `SPECULAR` | `specular_light` |
| `ATTENUATION` | `attenuation` |
| `SHADOW_ATTENUATION` | `shadow_attenuation` |

**Complete Example:**

```glsl
// Before (Godot 3.x)
shader_type spatial;

void light() {
    DIFFUSE = ALBEDO * ATTENUATION;
    SPECULAR = vec3(0.5) * pow(max(dot(NORMAL, LIGHT), 0.0), 32.0) * ATTENUATION;
}

// After (Godot 4.x)
shader_type spatial;

void light() {
    diffuse_light = ALBEDO * attenuation;
    specular_light = vec3(0.5) * pow(max(dot(normal, LIGHT), 0.0), 32.0) * attenuation;
}
```

**Light Function Parameter Changes:**

```glsl
// Godot 3.x - no parameters
void light() {
    // Access global light properties
}

// Godot 4.x - accepts light index (for multi-light)
void light(int light_index) {
    // Access light properties via LIGHT, attenuation, etc.
}
```

---

### Conversion F: File Extension (.shader → .gdshader)

**Detection:**
```bash
find . -name "*.shader" -type f | grep -v ".gdshader"
```

**Transformation:**
Rename files from `.shader` to `.gdshader`:

```bash
# Rename all .shader files to .gdshader
for file in $(find . -name "*.shader" -type f); do
    newname="${file%.shader}.gdshader"
    mv "$file" "$newname"
    echo "Renamed: $file → $newname"
done
```

**Note:** Godot 4.x uses `.gdshader` extension exclusively. `.shader` files from Godot 3.x should be renamed.

---

## Phase 3: Execution & Safety

### 3.1 Create Git Baseline

```bash
# Create backup tag
git tag shader-baseline-$(date +%Y%m%d-%H%M%S)

# Stage any current changes
git add .
git commit -m "Baseline: Pre-shader conversion" || echo "No changes to commit"
```

### 3.2 Process Files Sequentially

For each shader file:

```bash
# Read and process shader content
python3 << 'EOF'
import re
import sys

def convert_shader(content, filename):
    original = content
    conversions_applied = []
    
    # Conversion 1: Add screen_texture uniform if SCREEN_TEXTURE is used
    if 'SCREEN_TEXTURE' in content and 'uniform sampler2D screen_texture' not in content:
        # Find shader_type line and add uniform after it
        content = re.sub(
            r'(shader_type\s+\w+;\n?)',
            r'\1\nuniform sampler2D screen_texture : hint_screen_texture, filter_linear_mipmap;\n',
            content
        )
        conversions_applied.append("Added screen_texture uniform")
    
    # Conversion 2: Add depth_texture uniform if DEPTH_TEXTURE is used
    if 'DEPTH_TEXTURE' in content and 'uniform sampler2D depth_texture' not in content:
        content = re.sub(
            r'(shader_type\s+\w+;\n?)',
            r'\1\nuniform sampler2D depth_texture : hint_depth_texture, filter_linear_mipmap;\n',
            content
        )
        conversions_applied.append("Added depth_texture uniform")
    
    # Conversion 3: SCREEN_TEXTURE → screen_texture in texture() calls
    if 'texture(SCREEN_TEXTURE' in content or 'textureLod(screen_texture' in content:
        # Replace texture(SCREEN_TEXTURE, ...) with textureLod(screen_texture, ..., 0.0)
        content = re.sub(
            r'texture\s*\(\s*SCREEN_TEXTURE\s*,\s*([^,\)]+)\s*\)',
            r'textureLod(screen_texture, \1, 0.0)',
            content
        )
        # Replace texture(SCREEN_TEXTURE, ..., lod) with textureLod(screen_texture, ..., lod)
        content = re.sub(
            r'texture\s*\(\s*SCREEN_TEXTURE\s*,\s*([^,\)]+)\s*,\s*([^\)]+)\s*\)',
            r'textureLod(screen_texture, \1, \2)',
            content
        )
        # Replace remaining SCREEN_TEXTURE references
        content = content.replace('SCREEN_TEXTURE', 'screen_texture')
        conversions_applied.append("Converted SCREEN_TEXTURE to screen_texture")
    
    # Conversion 4: DEPTH_TEXTURE → depth_texture
    if 'texture(DEPTH_TEXTURE' in content or 'textureLod(depth_texture' in content:
        content = re.sub(
            r'texture\s*\(\s*DEPTH_TEXTURE\s*,\s*([^,\)]+)\s*\)',
            r'textureLod(depth_texture, \1, 0.0)',
            content
        )
        content = re.sub(
            r'texture\s*\(\s*DEPTH_TEXTURE\s*,\s*([^,\)]+)\s*,\s*([^\)]+)\s*\)',
            r'textureLod(depth_texture, \1, \2)',
            content
        )
        content = content.replace('DEPTH_TEXTURE', 'depth_texture')
        conversions_applied.append("Converted DEPTH_TEXTURE to depth_texture")
    
    # Conversion 5: Light function variables (only in light() function)
    if 'void light()' in content:
        # Replace light variables
        content = content.replace('DIFFUSE', 'diffuse_light')
        content = content.replace('SPECULAR', 'specular_light')
        content = content.replace('ATTENUATION', 'attenuation')
        conversions_applied.append("Converted light function variables")
    
    # Conversion 6: Built-in varyings in fragment() function (lowercase)
    # This is complex - only affect fragment() scope
    if 'void fragment()' in content:
        # Find fragment function and convert built-in varyings there
        fragment_start = content.find('void fragment()')
        if fragment_start != -1:
            # Find the end of fragment function (next void or end of file)
            fragment_end = len(content)
            next_func = re.search(r'\nvoid\s+\w+\s*\(\)', content[fragment_start+1:])
            if next_func:
                fragment_end = fragment_start + 1 + next_func.start()
            
            fragment_section = content[fragment_start:fragment_end]
            # Convert built-ins in fragment only
            fragment_section = re.sub(r'\bVERTEX\b', 'vertex', fragment_section)
            fragment_section = re.sub(r'\bUV\b', 'uv', fragment_section)
            fragment_section = re.sub(r'\bCOLOR\b', 'color', fragment_section)
            fragment_section = re.sub(r'\bNORMAL\b', 'normal', fragment_section)
            
            content = content[:fragment_start] + fragment_section + content[fragment_end:]
            conversions_applied.append("Converted built-in varyings to lowercase in fragment()")
    
    return content, conversions_applied

# Process file
filename = sys.argv[1] if len(sys.argv) > 1 else "shader.gdshader"
with open(filename, 'r') as f:
    content = f.read()

new_content, conversions = convert_shader(content, filename)

with open(filename, 'w') as f:
    f.write(new_content)

print(f"Applied {len(conversions)} conversions:")
for c in conversions:
    print(f"  - {c}")
EOF
```

### 3.3 Rename File Extensions

```bash
# Rename .shader to .gdshader after conversion
for file in $(find . -name "*.shader" -type f); do
    if [[ "$file" != *.gdshader ]]; then
        newname="${file%.shader}.gdshader"
        mv "$file" "$newname"
        git add "$newname"
        git rm "$file" 2>/dev/null || echo "Old file: $file (deleted)"
    fi
done
```

### 3.4 Commit Per File

```bash
# After each file modification
git add "$file"
git commit -m "Convert shader: $file to Godot 4.x

- Updated texture sampling (SCREEN_TEXTURE/DEPTH_TEXTURE)
- Added uniform declarations with hints
- Converted texture() to textureLod()
- Updated built-in varyings to lowercase
- Fixed light function variables
- Renamed extension to .gdshader"
```

---

## Phase 4: Verification & Testing

### 4.1 Syntax Validation

```bash
# Check all modified shaders for syntax errors
echo "=== Validating Shader Syntax ==="
for file in $(git diff --name-only HEAD~10..HEAD | grep "\.gdshader$"); do
    echo "Checking $file..."
    # Godot can validate shaders by loading them
    godot --headless --quit-after 2 project.godot 2>&1 | grep -i "$file" && echo "Warning: Possible issue in $file"
done
```

### 4.2 Pattern Verification

```bash
echo "=== Verifying Godot 3.x Patterns Removed ==="

echo "SCREEN_TEXTURE references remaining:"
grep -rn "SCREEN_TEXTURE" --include="*.gdshader" . 2>/dev/null | wc -l

echo "DEPTH_TEXTURE references remaining:"
grep -rn "DEPTH_TEXTURE" --include="*.gdshader" . 2>/dev/null | wc -l

echo "texture(SCREEN_TEXTURE remaining:"
grep -rn "texture\s*(\s*SCREEN_TEXTURE" --include="*.gdshader" . 2>/dev/null | wc -l

echo "Godot 3.x light variables (DIFFUSE/SPECULAR) remaining:"
grep -rn "\bDIFFUSE\b\|\bSPECULAR\b" --include="*.gdshader" . 2>/dev/null | wc -l

echo ".shader files (should be 0):"
find . -name "*.shader" -type f | grep -v ".gdshader" | wc -l
```

### 4.3 Godot Project Test

```bash
# Open project in Godot to verify shaders compile
echo "=== Testing in Godot ==="
godot --editor project.godot &
sleep 5

# Check Output panel for shader errors
# (User should visually verify no shader-related errors)
```

---

## Examples

### Example 1: Screen Distortion Shader

**Before (Godot 3.x):**
```glsl
shader_type canvas_item;

uniform float distortion_strength : hint_range(0.0, 1.0) = 0.1;

void fragment() {
    vec2 distorted_uv = SCREEN_UV + (UV - 0.5) * distortion_strength;
    vec4 screen_color = texture(SCREEN_TEXTURE, distorted_uv);
    COLOR = screen_color;
}
```

**After (Godot 4.x):**
```glsl
shader_type canvas_item;

uniform sampler2D screen_texture : hint_screen_texture, filter_linear_mipmap;
uniform float distortion_strength : hint_range(0.0, 1.0) = 0.1;

void fragment() {
    vec2 distorted_uv = SCREEN_UV + (uv - 0.5) * distortion_strength;
    vec4 screen_color = textureLod(screen_texture, distorted_uv, 0.0);
    COLOR = screen_color;
}
```

### Example 2: Depth-Based Fog Shader

**Before (Godot 3.x):**
```glsl
shader_type spatial;
render_mode depth_draw_opaque, cull_disabled;

uniform vec4 fog_color : source_color = vec4(0.5, 0.6, 0.7, 1.0);
uniform float fog_density : hint_range(0.0, 1.0) = 0.1;

void fragment() {
    float depth = texture(DEPTH_TEXTURE, SCREEN_UV).r;
    float fog_factor = exp(-fog_density * depth);
    
    ALBEDO = fog_color.rgb;
    ALPHA = 1.0 - fog_factor;
}
```

**After (Godot 4.x):**
```glsl
shader_type spatial;
render_mode depth_draw_opaque, cull_disabled;

uniform sampler2D depth_texture : hint_depth_texture, filter_linear_mipmap;
uniform vec4 fog_color : source_color = vec4(0.5, 0.6, 0.7, 1.0);
uniform float fog_density : hint_range(0.0, 1.0) = 0.1;

void fragment() {
    float depth = textureLod(depth_texture, SCREEN_UV, 0.0).r;
    float fog_factor = exp(-fog_density * depth);
    
    ALBEDO = fog_color.rgb;
    ALPHA = 1.0 - fog_factor;
}
```

### Example 3: Custom Light Shader

**Before (Godot 3.x):**
```glsl
shader_type spatial;

uniform vec4 highlight_color : source_color = vec4(1.0, 0.8, 0.0, 1.0);

void fragment() {
    ALBEDO = vec3(0.5);
}

void light() {
    float dot_product = max(dot(NORMAL, LIGHT), 0.0);
    
    if (dot_product > 0.9) {
        DIFFUSE = highlight_color.rgb * ATTENUATION;
    } else {
        DIFFUSE = ALBEDO * dot_product * ATTENUATION;
    }
    
    SPECULAR = vec3(0.0);
}
```

**After (Godot 4.x):**
```glsl
shader_type spatial;

uniform vec4 highlight_color : source_color = vec4(1.0, 0.8, 0.0, 1.0);

void fragment() {
    ALBEDO = vec3(0.5);
}

void light() {
    float dot_product = max(dot(normal, LIGHT), 0.0);
    
    if (dot_product > 0.9) {
        diffuse_light = highlight_color.rgb * attenuation;
    } else {
        diffuse_light = ALBEDO * dot_product * attenuation;
    }
    
    specular_light = vec3(0.0);
}
```

### Example 4: Vertex Displacement Shader

**Before (Godot 3.x):**
```glsl
shader_type spatial;

uniform float wave_height : hint_range(0.0, 2.0) = 0.5;
uniform float wave_speed : hint_range(0.0, 10.0) = 2.0;

void vertex() {
    float wave = sin(VERTEX.x * 2.0 + TIME * wave_speed) * wave_height;
    VERTEX.y += wave;
}

void fragment() {
    vec2 uv_offset = UV * 2.0;
    ALBEDO = vec3(uv_offset, 0.5);
}
```

**After (Godot 4.x):**
```glsl
shader_type spatial;

uniform float wave_height : hint_range(0.0, 2.0) = 0.5;
uniform float wave_speed : hint_range(0.0, 10.0) = 2.0;

void vertex() {
    float wave = sin(vertex.x * 2.0 + TIME * wave_speed) * wave_height;
    vertex.y += wave;
}

void fragment() {
    vec2 uv_offset = uv * 2.0;
    ALBEDO = vec3(uv_offset, 0.5);
}
```

---

## Complete Conversion Mapping Reference

### Texture Uniforms

| Godot 3.x | Godot 4.x Declaration | Godot 4.x Usage |
|-----------|----------------------|----------------|
| `SCREEN_TEXTURE` | `uniform sampler2D screen_texture : hint_screen_texture, filter_linear_mipmap;` | `textureLod(screen_texture, uv, lod)` |
| `DEPTH_TEXTURE` | `uniform sampler2D depth_texture : hint_depth_texture, filter_linear_mipmap;` | `textureLod(depth_texture, uv, lod)` |

### Texture Sampling Functions

| Godot 3.x | Godot 4.x |
|-----------|-----------|
| `texture(SCREEN_TEXTURE, uv)` | `textureLod(screen_texture, uv, 0.0)` |
| `texture(SCREEN_TEXTURE, uv, lod)` | `textureLod(screen_texture, uv, lod)` |
| `texture(DEPTH_TEXTURE, uv)` | `textureLod(depth_texture, uv, 0.0)` |
| `texture(TEXTURE, uv)` | `texture(TEXTURE, uv)` (unchanged) |
| `texture(NORMAL_TEXTURE, uv)` | `texture(NORMAL_TEXTURE, uv)` (unchanged) |

### Built-in Varyings (fragment() scope only)

| Godot 3.x | Godot 4.x |
|-----------|-----------|
| `VERTEX` | `vertex` |
| `UV` | `uv` |
| `COLOR` | `color` |
| `NORMAL` | `normal` |
| `TANGENT` | `tangent` |
| `BINORMAL` | `binormal` |

### Light Function Variables

| Godot 3.x | Godot 4.x |
|-----------|-----------|
| `DIFFUSE` | `diffuse_light` |
| `SPECULAR` | `specular_light` |
| `ATTENUATION` | `attenuation` |
| `SHADOW_ATTENUATION` | `shadow_attenuation` |

---

## Success Criteria

Conversion complete when:

- ✓ Zero `SCREEN_TEXTURE` references remain (converted to uniform)
- ✓ Zero `DEPTH_TEXTURE` references remain (converted to uniform)
- ✓ All `texture()` calls for screen/depth use `textureLod()`
- ✓ Built-in varyings in `fragment()` are lowercase
- ✓ Light function uses new variable names (`diffuse_light`, `specular_light`, etc.)
- ✓ All `.shader` files renamed to `.gdshader`
- ✓ Uniform declarations include proper hints (`hint_screen_texture`, `hint_depth_texture`)
- ✓ All shaders compile without errors in Godot 4.x
- ✓ Visual output matches Godot 3.x behavior
- ✓ Git history shows clear conversion commits

---

## Common Issues & Solutions

### Issue 1: texture() vs textureLod()

**Problem:**
```glsl
// Won't work in Godot 4.x
vec4 color = texture(screen_texture, UV);
```

**Solution:**
```glsl
// Correct Godot 4.x syntax
vec4 color = textureLod(screen_texture, UV, 0.0);
```

**Explanation:** Godot 4.x requires explicit LOD for screen and depth textures. Always use `textureLod()` with an explicit LOD value (0.0 for no mipmapping).

### Issue 2: Missing Uniform Declarations

**Problem:**
```glsl
shader_type canvas_item;

void fragment() {
    COLOR = textureLod(screen_texture, UV, 0.0);  // ERROR: screen_texture not declared
}
```

**Solution:**
```glsl
shader_type canvas_item;

uniform sampler2D screen_texture : hint_screen_texture, filter_linear_mipmap;

void fragment() {
    COLOR = textureLod(screen_texture, uv, 0.0);
}
```

**Explanation:** Godot 3.x provided SCREEN_TEXTURE implicitly. Godot 4.x requires explicit uniform declarations with hints.

### Issue 3: Wrong Case in Built-in Varyings

**Problem:**
```glsl
void fragment() {
    ALBEDO = texture(TEXTURE, UV).rgb;  // ERROR in Godot 4.x
}
```

**Solution:**
```glsl
void fragment() {
    ALBEDO = texture(TEXTURE, uv).rgb;  // Lowercase in fragment()
}
```

**Note:** Built-in varyings remain uppercase in `vertex()` but become lowercase in `fragment()` in Godot 4.x.

### Issue 4: Light Function Variable Names

**Problem:**
```glsl
void light() {
    DIFFUSE = ALBEDO;  // ERROR: DIFFUSE doesn't exist
}
```

**Solution:**
```glsl
void light() {
    diffuse_light = ALBEDO;  // Correct variable name
}
```

### Issue 5: Multiple hint declarations

**Problem:**
```glsl
uniform sampler2D screen_texture : hint_screen_texture;
uniform sampler2D depth_texture : hint_depth_texture;

// Later in code, trying to use both
```

**Issue:** If shader already has uniforms declared, don't duplicate them.

**Solution:** Check for existing declarations before adding.

---

## Rollback Procedure

If conversion causes issues:

```bash
# Find baseline tag
git tag | grep "shader-baseline"

# Reset to pre-conversion state
git reset --hard <baseline-tag>

# Or revert specific commits
git revert <conversion-commit-hash>

# Rename files back if needed
for file in $(find . -name "*.gdshader" -type f); do
    if [ ! -f "${file%.gdshader}.shader" ]; then
        mv "$file" "${file%.gdshader}.shader"
    fi
done
```

---

## Integration with Other Skills

**Use before:**
- `godot-modernize-gdscript` - Update shaders first, then scripts
- `godot-migrate-tilemap` - Visual effects often tied to tilemaps

**Use after:**
- Project conversion from Godot 3.x to 4.x
- `godot-organize-assets` - Organize shader files first

---

**This skill automates the tedious parts of Godot 3.x to 4.x shader migration while preserving exact visual output.**
