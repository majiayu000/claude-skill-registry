---
name: shaders
description: Implements visual shaders and shader code for 2D/3D effects including dissolve, outline, water, post-processing, and custom materials. Use when creating custom visual effects.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Godot Shaders

When implementing custom visuals, use these shader patterns for efficient and beautiful effects.

## Shader Basics

### Shader Structure
```gdshader
shader_type canvas_item;  // or spatial, particles, sky, fog

// Uniforms (parameters)
uniform vec4 color : source_color = vec4(1.0);
uniform float intensity : hint_range(0.0, 1.0) = 0.5;
uniform sampler2D texture_albedo : source_color;

// Varyings (passed from vertex to fragment)
varying vec2 world_position;

void vertex() {
    // Modify vertex position
    world_position = (MODEL_MATRIX * vec4(VERTEX, 0.0, 1.0)).xy;
}

void fragment() {
    // Output final color
    COLOR = texture(TEXTURE, UV) * color;
}
```

### Shader Types Reference
```gdshader
// canvas_item - 2D sprites, UI
shader_type canvas_item;
// Built-ins: TEXTURE, UV, COLOR, VERTEX, etc.

// spatial - 3D meshes
shader_type spatial;
// Built-ins: VERTEX, NORMAL, UV, ALBEDO, METALLIC, ROUGHNESS, etc.

// particles - GPU particles
shader_type particles;
// Built-ins: TRANSFORM, COLOR, VELOCITY, etc.

// sky - Skybox/environment
shader_type sky;
// Built-ins: SKY_COORDS, EYEDIR, etc.

// fog - Volumetric fog
shader_type fog;
```

## 2D Shader Effects

### Outline Shader
```gdshader
shader_type canvas_item;

uniform vec4 outline_color : source_color = vec4(0.0, 0.0, 0.0, 1.0);
uniform float outline_width : hint_range(0.0, 10.0) = 1.0;

void fragment() {
    vec2 size = TEXTURE_PIXEL_SIZE * outline_width;

    float outline = texture(TEXTURE, UV + vec2(-size.x, 0)).a;
    outline += texture(TEXTURE, UV + vec2(size.x, 0)).a;
    outline += texture(TEXTURE, UV + vec2(0, -size.y)).a;
    outline += texture(TEXTURE, UV + vec2(0, size.y)).a;
    outline += texture(TEXTURE, UV + vec2(-size.x, -size.y)).a;
    outline += texture(TEXTURE, UV + vec2(size.x, -size.y)).a;
    outline += texture(TEXTURE, UV + vec2(-size.x, size.y)).a;
    outline += texture(TEXTURE, UV + vec2(size.x, size.y)).a;
    outline = min(outline, 1.0);

    vec4 tex_color = texture(TEXTURE, UV);
    COLOR = mix(tex_color, outline_color, outline - tex_color.a);
}
```

### Dissolve Effect
```gdshader
shader_type canvas_item;

uniform float dissolve_amount : hint_range(0.0, 1.0) = 0.0;
uniform sampler2D noise_texture;
uniform vec4 edge_color : source_color = vec4(1.0, 0.5, 0.0, 1.0);
uniform float edge_width : hint_range(0.0, 0.2) = 0.05;

void fragment() {
    vec4 tex_color = texture(TEXTURE, UV);
    float noise = texture(noise_texture, UV).r;

    // Dissolve based on noise
    float dissolve_edge = dissolve_amount + edge_width;

    if (noise < dissolve_amount) {
        discard;
    } else if (noise < dissolve_edge) {
        // Edge glow
        float edge_factor = (noise - dissolve_amount) / edge_width;
        COLOR = mix(edge_color, tex_color, edge_factor);
    } else {
        COLOR = tex_color;
    }
}
```

### Flash/Hit Effect
```gdshader
shader_type canvas_item;

uniform vec4 flash_color : source_color = vec4(1.0, 1.0, 1.0, 1.0);
uniform float flash_amount : hint_range(0.0, 1.0) = 0.0;

void fragment() {
    vec4 tex_color = texture(TEXTURE, UV);
    COLOR = mix(tex_color, flash_color * tex_color.a, flash_amount);
}
```

### Pixelation
```gdshader
shader_type canvas_item;

uniform float pixel_size : hint_range(1.0, 100.0) = 8.0;

void fragment() {
    vec2 grid_uv = round(UV * pixel_size) / pixel_size;
    COLOR = texture(TEXTURE, grid_uv);
}
```

### Wave Distortion
```gdshader
shader_type canvas_item;

uniform float wave_amplitude : hint_range(0.0, 0.1) = 0.02;
uniform float wave_frequency : hint_range(0.0, 50.0) = 10.0;
uniform float wave_speed : hint_range(0.0, 10.0) = 2.0;

void fragment() {
    vec2 uv = UV;
    uv.x += sin(uv.y * wave_frequency + TIME * wave_speed) * wave_amplitude;
    uv.y += cos(uv.x * wave_frequency + TIME * wave_speed) * wave_amplitude;
    COLOR = texture(TEXTURE, uv);
}
```

### Color Palette Swap
```gdshader
shader_type canvas_item;

uniform sampler2D palette_old;
uniform sampler2D palette_new;

void fragment() {
    vec4 tex_color = texture(TEXTURE, UV);

    // Find matching color in old palette
    float best_match = 999.0;
    vec4 new_color = tex_color;

    for (int i = 0; i < textureSize(palette_old, 0).x; i++) {
        vec4 old_pal = texelFetch(palette_old, ivec2(i, 0), 0);
        float dist = distance(tex_color.rgb, old_pal.rgb);

        if (dist < best_match && dist < 0.1) {
            best_match = dist;
            new_color = texelFetch(palette_new, ivec2(i, 0), 0);
            new_color.a = tex_color.a;
        }
    }

    COLOR = new_color;
}
```

## 3D Shader Effects

### Toon/Cel Shading
```gdshader
shader_type spatial;

uniform vec4 albedo_color : source_color = vec4(1.0);
uniform int color_levels : hint_range(2, 10) = 4;
uniform float outline_size : hint_range(0.0, 0.1) = 0.02;

void vertex() {
    // Outline pass (render in separate pass with inverted normals)
}

void fragment() {
    ALBEDO = albedo_color.rgb;
}

void light() {
    // Quantize lighting
    float NdotL = dot(NORMAL, LIGHT);
    float intensity = max(NdotL, 0.0);
    intensity = floor(intensity * float(color_levels)) / float(color_levels);

    DIFFUSE_LIGHT += intensity * LIGHT_COLOR * ATTENUATION;
}
```

### Fresnel/Rim Lighting
```gdshader
shader_type spatial;

uniform vec4 albedo_color : source_color = vec4(1.0);
uniform vec4 rim_color : source_color = vec4(0.0, 0.5, 1.0, 1.0);
uniform float rim_power : hint_range(0.0, 10.0) = 3.0;

void fragment() {
    ALBEDO = albedo_color.rgb;

    // Fresnel effect
    float fresnel = pow(1.0 - dot(NORMAL, VIEW), rim_power);
    EMISSION = rim_color.rgb * fresnel;
}
```

### Triplanar Mapping
```gdshader
shader_type spatial;

uniform sampler2D texture_albedo : source_color;
uniform float texture_scale = 1.0;

varying vec3 world_position;
varying vec3 world_normal;

void vertex() {
    world_position = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz;
    world_normal = (MODEL_MATRIX * vec4(NORMAL, 0.0)).xyz;
}

void fragment() {
    vec3 blend = abs(normalize(world_normal));
    blend = pow(blend, vec3(4.0));
    blend /= blend.x + blend.y + blend.z;

    vec3 x_proj = texture(texture_albedo, world_position.yz * texture_scale).rgb;
    vec3 y_proj = texture(texture_albedo, world_position.xz * texture_scale).rgb;
    vec3 z_proj = texture(texture_albedo, world_position.xy * texture_scale).rgb;

    ALBEDO = x_proj * blend.x + y_proj * blend.y + z_proj * blend.z;
}
```

### Water Shader
```gdshader
shader_type spatial;
render_mode blend_mix, depth_draw_opaque, cull_back;

uniform vec4 water_color : source_color = vec4(0.0, 0.3, 0.5, 0.8);
uniform vec4 foam_color : source_color = vec4(1.0);
uniform sampler2D normal_map : hint_normal;
uniform sampler2D wave_texture;
uniform float wave_speed = 0.03;
uniform float wave_strength = 0.1;
uniform float foam_amount : hint_range(0.0, 1.0) = 0.2;

uniform sampler2D DEPTH_TEXTURE : hint_depth_texture, filter_linear_mipmap;
uniform sampler2D SCREEN_TEXTURE : hint_screen_texture, filter_linear_mipmap;

void fragment() {
    // Animated UVs
    vec2 uv1 = UV + TIME * wave_speed;
    vec2 uv2 = UV - TIME * wave_speed * 0.7;

    // Normal mapping
    vec3 normal1 = texture(normal_map, uv1).rgb;
    vec3 normal2 = texture(normal_map, uv2).rgb;
    vec3 combined_normal = normalize(normal1 + normal2 - 1.0);
    NORMAL_MAP = combined_normal;

    // Depth-based effects
    float depth = texture(DEPTH_TEXTURE, SCREEN_UV).r;
    float scene_depth = PROJECTION_MATRIX[3][2] / (depth * 2.0 - 1.0 + PROJECTION_MATRIX[2][2]);
    float water_depth = VERTEX.z;
    float depth_diff = scene_depth - water_depth;

    // Foam at edges
    float foam = 1.0 - smoothstep(0.0, foam_amount, depth_diff);

    ALBEDO = mix(water_color.rgb, foam_color.rgb, foam);
    ALPHA = water_color.a;
    METALLIC = 0.0;
    ROUGHNESS = 0.1;
}
```

### Hologram Effect
```gdshader
shader_type spatial;
render_mode unshaded, cull_disabled;

uniform vec4 hologram_color : source_color = vec4(0.0, 1.0, 0.8, 1.0);
uniform float scanline_count : hint_range(10.0, 200.0) = 50.0;
uniform float scanline_speed : hint_range(0.0, 10.0) = 1.0;
uniform float flicker_speed : hint_range(0.0, 50.0) = 10.0;
uniform float glow_intensity : hint_range(0.0, 5.0) = 1.5;

void fragment() {
    // Scanlines
    float scanline = sin((UV.y + TIME * scanline_speed) * scanline_count * 3.14159) * 0.5 + 0.5;

    // Flicker
    float flicker = sin(TIME * flicker_speed) * 0.1 + 0.9;

    // Fresnel glow
    float fresnel = pow(1.0 - dot(NORMAL, VIEW), 2.0);

    vec3 color = hologram_color.rgb * (0.5 + scanline * 0.5) * flicker;
    color += hologram_color.rgb * fresnel * glow_intensity;

    ALBEDO = color;
    EMISSION = color * 0.5;
    ALPHA = (0.3 + fresnel * 0.7) * flicker;
}
```

## Post-Processing Shaders

### Chromatic Aberration
```gdshader
shader_type canvas_item;

uniform float offset : hint_range(0.0, 0.01) = 0.002;

void fragment() {
    vec2 dir = UV - vec2(0.5);

    float r = texture(TEXTURE, UV + dir * offset).r;
    float g = texture(TEXTURE, UV).g;
    float b = texture(TEXTURE, UV - dir * offset).b;

    COLOR = vec4(r, g, b, 1.0);
}
```

### Vignette
```gdshader
shader_type canvas_item;

uniform float vignette_intensity : hint_range(0.0, 1.0) = 0.4;
uniform float vignette_opacity : hint_range(0.0, 1.0) = 0.5;

void fragment() {
    vec4 tex_color = texture(TEXTURE, UV);

    vec2 uv = UV * (1.0 - UV.yx);
    float vignette = uv.x * uv.y * 15.0;
    vignette = pow(vignette, vignette_intensity);

    COLOR = mix(tex_color, tex_color * vignette, vignette_opacity);
}
```

### CRT Effect
```gdshader
shader_type canvas_item;

uniform float scanline_intensity : hint_range(0.0, 1.0) = 0.3;
uniform float curvature : hint_range(0.0, 0.1) = 0.02;
uniform vec2 resolution = vec2(320.0, 240.0);

void fragment() {
    // Screen curvature
    vec2 uv = UV;
    vec2 curved_uv = uv * 2.0 - 1.0;
    vec2 offset = curved_uv.yx / curvature;
    curved_uv += curved_uv * offset * offset;
    curved_uv = curved_uv * 0.5 + 0.5;

    // Bounds check
    if (curved_uv.x < 0.0 || curved_uv.x > 1.0 || curved_uv.y < 0.0 || curved_uv.y > 1.0) {
        COLOR = vec4(0.0, 0.0, 0.0, 1.0);
        return;
    }

    vec4 tex_color = texture(TEXTURE, curved_uv);

    // Scanlines
    float scanline = sin(curved_uv.y * resolution.y * 3.14159) * 0.5 + 0.5;
    tex_color.rgb *= 1.0 - scanline_intensity * (1.0 - scanline);

    // RGB subpixels
    float pixel_x = fract(curved_uv.x * resolution.x);
    if (pixel_x < 0.333) {
        tex_color.gb *= 0.8;
    } else if (pixel_x < 0.666) {
        tex_color.rb *= 0.8;
    } else {
        tex_color.rg *= 0.8;
    }

    COLOR = tex_color;
}
```

### Blur
```gdshader
shader_type canvas_item;

uniform float blur_amount : hint_range(0.0, 5.0) = 1.0;

void fragment() {
    vec2 pixel_size = TEXTURE_PIXEL_SIZE * blur_amount;

    vec4 color = vec4(0.0);

    // 9-tap Gaussian blur
    color += texture(TEXTURE, UV + vec2(-pixel_size.x, -pixel_size.y)) * 0.0625;
    color += texture(TEXTURE, UV + vec2(0.0, -pixel_size.y)) * 0.125;
    color += texture(TEXTURE, UV + vec2(pixel_size.x, -pixel_size.y)) * 0.0625;
    color += texture(TEXTURE, UV + vec2(-pixel_size.x, 0.0)) * 0.125;
    color += texture(TEXTURE, UV) * 0.25;
    color += texture(TEXTURE, UV + vec2(pixel_size.x, 0.0)) * 0.125;
    color += texture(TEXTURE, UV + vec2(-pixel_size.x, pixel_size.y)) * 0.0625;
    color += texture(TEXTURE, UV + vec2(0.0, pixel_size.y)) * 0.125;
    color += texture(TEXTURE, UV + vec2(pixel_size.x, pixel_size.y)) * 0.0625;

    COLOR = color;
}
```

## Visual Shader Tips

### Common Nodes Combinations
```
# Outline:
UV -> VectorOp(Add) -> Texture -> ...
     ^-- float(outline_width) * ScreenUV pixel size

# Gradient:
UV.y -> Remap(0,1 to colors) -> Output

# Animated UV:
Time * speed -> Sin/Cos -> VectorOp(Add UV) -> Texture

# Fresnel:
Normal dot View -> OneMinus -> Power(rim_power) -> Emission
```

## Shader Performance Tips

```gdshader
// GOOD: Use step() instead of if statements
float result = step(0.5, value);  // Returns 0.0 or 1.0

// GOOD: Use mix() for lerping
vec3 blended = mix(color_a, color_b, factor);

// GOOD: Use built-in functions
float clamped = clamp(value, 0.0, 1.0);
float smooth = smoothstep(0.0, 1.0, value);

// AVOID: Branching in fragment shader
// BAD:
if (value > 0.5) {
    color = red;
} else {
    color = blue;
}

// GOOD: Branchless alternative
color = mix(blue, red, step(0.5, value));

// Minimize texture samples
// Cache texture lookups when using same UV multiple times
vec4 tex = texture(TEXTURE, UV);
// Reuse tex instead of calling texture() again
```
