---
name: atmosphere-shader
description: Generate physically-based atmospheric scattering shaders — sky domes, planetary atmospheres, LUT-optimized pipelines, depth-aware post-processing. Four modes — sky-dome, atmosphere-post, planet, lut. Triggers on atmospheric scattering, sky shader, sunset rendering, planet atmosphere, Rayleigh scattering, Mie scattering, volumetric sky, sky dome, atmosphere post-processing, aerial perspective, transmittance LUT, sky rendering, realistic sky, planetary rendering.
argument-hint: "[--mode sky-dome|atmosphere-post|planet|lut] [--planet earth|mars] [--format shadertoy|threejs|r3f]"
---

# Atmosphere Shader Skill

Render physically-accurate skies, sunsets, and planetary atmospheres through atmospheric scattering — Rayleigh, Mie, and Ozone models composed via raymarching in GLSL fragment shaders. Four progressive modes from flat backdrop to LUT-optimized planetary pipeline.

## Modes

| Mode | Output | Complexity |
|------|--------|------------|
| `sky-dome` | Single-pass fragment shader, flat sky backdrop | Entry point |
| `atmosphere-post` | Depth-aware post-processing effect with atmospheric fog | Intermediate |
| `planet` | Spherical atmosphere shell around a mesh, logarithmic depth | Advanced |
| `lut` | Transmittance + Sky View + Aerial Perspective LUTs, FBO pipeline | Production |

## Gotchas — What Claude Gets Wrong

These are the highest-signal items in this skill. Every one is a concrete, reproducible failure mode.

### 1. Wrong scattering coefficients

Claude invents plausible-looking but physically incorrect beta values. Use these exact constants for Earth:

```glsl
const vec3 BETA_R = vec3(5.8e-3, 13.5e-3, 33.1e-3);   // Rayleigh scattering (1/km)
const float BETA_M_SCATTER = 21e-3;                      // Mie scattering
const float BETA_M_EXT = 21e-3 * 1.1;                    // Mie extinction (scatter + absorb)
const vec3 BETA_OZONE_ABS = vec3(0.65e-3, 1.881e-3, 0.085e-3); // Ozone absorption

const float RAYLEIGH_SCALE_HEIGHT = 8.0;   // km
const float MIE_SCALE_HEIGHT = 1.2;        // km
const float MIE_G = 0.76;                  // Henyey-Greenstein anisotropy
const float ATMOSPHERE_HEIGHT = 100.0;     // km (Karman line)
```

See `references/scattering-coefficients.md` for Mars and custom planet parameter sets.

### 2. Missing nested light march

Claude implements only the view-ray loop, producing a blue gradient but **no sunsets**. The critical missing piece: at each sample point along the primary ray, a secondary march toward the sun accumulates `sunOD` (optical depth between sample and sun). Without this, `tau` only contains view-direction extinction and the sky is uniformly blue regardless of sun angle.

```glsl
// WRONG — view ray only, no sunset
vec3 tau = BETA_R * viewODR;

// RIGHT — view ray + sun path
vec3 sunOD = lightMarch(h, sunDirection.y);
vec3 tau = BETA_R * (viewODR + sunOD.x)
         + BETA_M_EXT * (viewODM + sunOD.y)
         + BETA_OZONE_ABS * (viewODO + sunOD.z);
```

The light march denominator uses a `+0.15` offset to prevent infinite path length at exact horizon angles: `float denom = max(sunY + 0.15, 0.04);`

### 3. Incorrect logarithmic depth reconstruction

At planetary scale, a linear depth buffer causes z-fighting between atmosphere and surface. Enable `logarithmicDepthBuffer: true` in the R3F Canvas, then decode in the shader:

```glsl
float logDepthToViewZ(float depth) {
  return -(pow(2.0, depth * log2(cameraFar + 1.0)) - 1.0);
}
```

Claude defaults to `depth * (far - near) + near`, which is the linear formula and fails at planetary distances.

### 4. No LUT pipeline knowledge

Without guidance, Claude attempts the full nested raymarch (24 primary steps x 8 light march steps = 192 texture fetches per pixel) at screen resolution. The LUT approach precomputes transmittance into a 250x64 texture, then downstream LUTs sample it with a single `texture2D` call. See `references/hillaire-lut-pipeline.md`.

### 5. Wrong phase function normalization

The Mie phase function (Henyey-Greenstein) has a `(2.0 + g*g)` term in the denominator that Claude drops:

```glsl
// WRONG — missing (2 + gg) denominator
float miePhase(float mu) {
  float gg = MIE_G * MIE_G;
  return (1.0 - gg) / pow(1.0 + gg - 2.0 * MIE_G * mu, 1.5);
}

// RIGHT
float miePhase(float mu) {
  float gg = MIE_G * MIE_G;
  float num = 3.0 * (1.0 - gg) * (1.0 + mu * mu);
  float den = 8.0 * PI * (2.0 + gg) * pow(max(1.0 + gg - 2.0 * MIE_G * mu, 1e-4), 1.5);
  return num / den;
}
```

### 6. Missing ozone

Claude's atmospheric models skip ozone entirely, losing the purple twilight shift and the correct sky-blue (as opposed to pure Rayleigh blue). Ozone peaks at ~25 km altitude with ~15 km width, absorbs but does not scatter:

```glsl
float ozoneDensity(float h) {
  return max(0.0, 1.0 - abs(h - 25.0) / 15.0);
}
```

## Sky Dome Mode

Single-pass fragment shader. Rayleigh + Mie + Ozone scattering with nested light march. Suitable as a full-screen backdrop.

### Architecture

1. Cast ray per pixel from camera position
2. Step through atmosphere volume (24 primary steps)
3. At each step: accumulate Rayleigh, Mie, Ozone optical depth
4. At each step: light march toward sun (8 steps) for sun transmittance
5. Combine: `scattering = SUN_INTENSITY * (phaseR * BETA_R * sumR + phaseM * BETA_M * sumM)`
6. Horizon mask: `smoothstep(-0.12, 0.05, skyDir.y)` to blend to space below horizon
7. Tonemap: `ACESFilm(color)`

Density functions, phase functions, and transmittance: see gotchas #1, #5, #6 above — those contain the correct implementations with wrong/right comparisons.

## Atmosphere Post-Processing Mode

Depth-aware post-processing effect. Reconstructs world-space position from the depth buffer, marches through the scene volume, applies atmospheric fog that thickens with distance.

### World-Space Reconstruction

```glsl
vec3 getWorldPosition(vec2 uv, float depth) {
  float clipZ = depth * 2.0 - 1.0;
  vec4 clip = vec4(uv * 2.0 - 1.0, clipZ, 1.0);
  vec4 view = projectionMatrixInverse * clip;
  vec4 world = viewMatrixInverse * view;
  return world.xyz / world.w;
}
```

### Depth-Driven Step Sizing

```glsl
float sceneDepth = depthToRayDistance(uv, depth);
bool isBackground = depth >= 1.0 - 1e-7;

if (isBackground) {
  sceneDepth = atmosphereHeight * 8.0;
}

float stepSize = sceneDepth / float(PRIMARY_STEPS);
```

Nearby geometry gets dense sampling; distant sky rays distribute steps over a larger volume.

Ground-ray early termination: if `rayDir.y < -1e-5`, compute `tGround = observerAltitude / max(-rayDir.y, 1e-4)` and cap `rayEnd` to prevent marching below the surface.

### R3F Integration

Three uniforms from the scene: `depthBuffer`, `projectionMatrixInverse`, `viewMatrixInverse`. Enable `logarithmicDepthBuffer: true` on the Canvas `gl` prop for planetary scale. FBOs for LUTs use dedicated `WebGLRenderTarget` instances rendered to off-screen scenes.

## Planet Mode

Spherical atmosphere shell. Uses ray-sphere intersection to define atmosphere entry/exit, logarithmic depth buffer for planetary scale.

### Ray-Sphere Intersection

```glsl
vec2 raySphereIntersect(vec3 ro, vec3 rd, vec3 center, float radius) {
  vec3 oc = ro - center;
  float b = dot(oc, rd);
  float c = dot(oc, oc) - radius * radius;
  float disc = b * b - c;
  if (disc < 0.0) return vec2(-1.0);
  float sq = sqrt(disc);
  return vec2(-b - sq, -b + sq);
}
```

### Atmosphere Segment Clipping

Three cases: ray misses atmosphere, ray hits planet surface, scene object occludes planet.

```glsl
vec2 atmosphereHit = raySphereIntersect(ro, rd, vec3(0.0), atmosphereRadius);
vec2 planetHit = raySphereIntersect(ro, rd, vec3(0.0), planetRadius);

float atmosphereNear = max(atmosphereHit.x, 0.0);
float atmosphereFar = atmosphereHit.y;

if (planetHit.x > 0.0) {
  atmosphereFar = min(atmosphereFar, planetHit.x);
  if (sceneDepth < planetHit.x - 2.0) {
    atmosphereFar = min(atmosphereFar, sceneDepth);
  }
} else {
  atmosphereFar = min(atmosphereFar, sceneDepth);
}
```

### Eclipse Handling

Compare angular radii and separation of sun/moon from each sample point. Three cases: no overlap, moon >= sun angular size (total/annular), moon < sun (partial). Multiply transmittance by this value at each sample.

```glsl
float sunVisibility(vec3 point) {
  vec3 sunDir = normalize(sunDirection);
  vec3 toMoon = moonPosition - point;
  float moonDist = length(toMoon);
  vec3 moonDir = normalize(toMoon);

  if (moonDist <= 1e-5 || dot(sunDir, moonDir) < 0.9) return 1.0;

  float angularSep = acos(clamp(dot(sunDir, moonDir), -1.0, 1.0));
  float sunAngularRadius = SUN_RADIUS / SUN_DISTANCE;
  float moonAngularRadius = moonRadius / moonDist;
  float outerEdge = sunAngularRadius + moonAngularRadius;

  if (moonAngularRadius >= sunAngularRadius) {
    float innerEdge = moonAngularRadius - sunAngularRadius;
    return max(0.075, smoothstep(innerEdge, outerEdge, angularSep));
  }

  float innerEdge = sunAngularRadius - moonAngularRadius;
  float minVis = clamp(1.0 - (moonAngularRadius * moonAngularRadius)
                            / (sunAngularRadius * sunAngularRadius), 0.0, 1.0);
  return mix(minVis, 1.0, smoothstep(innerEdge, outerEdge, angularSep));
}
```

## LUT Mode

Precompute expensive scattering into textures, compose in a final pass. Based on Hillaire (2020).

### Pipeline

```
Transmittance LUT (250x64)
        |
   +---------+---------+
   |                   |
Sky View LUT      Aerial Perspective LUT
(256x128)         (screen resolution)
   |                   |
   +---------+---------+
        |
  Composition Pass
```

Each LUT is rendered to a dedicated FBO, passed as a uniform to downstream passes.

### Transmittance LUT Parameterization

- **x-axis**: `mu = cos(zenith)` from -1 (toward ground) to +1 (toward space)
- **y-axis**: altitude from `planetRadius` to `atmosphereRadius`
- **Output**: `vec3(exp(-tau))` — surviving light fraction per channel

### Composition

```glsl
// Geometry pixels: blend original color with atmospheric haze
color = color * aerialPerspective.a + aerialPerspective.rgb;

// Background pixels: replace with sky color
color = sampleSkyViewLUT(rayDir, planetCenter);

color = ACESFilm(color);
color = pow(color, vec3(1.0 / 2.2));
```

See `references/hillaire-lut-pipeline.md` for full LUT shader implementations.

## Scope Boundaries

This skill covers **volumetric atmospheric light transport**. It does NOT cover:
- Volumetric clouds (separate rendering concern)
- Domain warping / procedural effects (that's `rocaille-shader`)
- Particle systems (that's `threejs-particle-canvas`)
- TSL/WebGPU API reference (that's `webgpu-threejs-tsl`)
- CSS-based sky gradients or surface effects (that's `grainient`)

## Reference Documentation

- `references/scattering-coefficients.md` — Earth, Mars, and custom planet parameter tables
- `references/hillaire-lut-pipeline.md` — LUT architecture from Hillaire (2020)

## Attribution

- **Atmospheric scattering model** — Nishita et al., "Display of the Earth Taking into Account Atmospheric Scattering" (SIGGRAPH 1993)
- **LUT-based approach** — Sebastian Hillaire, "A Scalable and Production Ready Sky and Atmosphere Rendering Technique" (EGSR 2020)
- **Implementation reference** — Maxime Heckel, "On Rendering the Sky, Sunsets, and Planets" (2026)
- **Production reference** — [three-geospatial](https://github.com/takram-design-engineering/three-geospatial) by Shota Matsuda
