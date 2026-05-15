# Hillaire LUT Pipeline Reference

Source: Sebastian Hillaire, "A Scalable and Production Ready Sky and Atmosphere Rendering Technique" (EGSR 2020)
Paper: https://sebh.github.io/publications/egsr2020.pdf

## Overview

Replace per-pixel nested raymarching with precomputed lookup textures. Three LUTs compose to produce the full atmospheric scattering effect at a fraction of the runtime cost.

## Pipeline Architecture

```
                  Transmittance LUT
                    (250 x 64)
                        |
            +-----------+-----------+
            |                       |
      Sky View LUT          Aerial Perspective LUT
       (256 x 128)            (screen resolution)
            |                       |
            +-----------+-----------+
                        |
                 Composition Pass
                  (screen resolution)
```

Each LUT is rendered to a dedicated FBO (Frame Buffer Object). In WebGL2, this means a `WebGLRenderTarget` with a full-screen quad and a custom shader material. In WebGPU, these would be compute shader passes.

## Transmittance LUT

**Purpose**: Precompute how much light survives traveling through the atmosphere for any altitude and zenith angle. Replaces the nested light march loop.

**Resolution**: 250 x 64 (low resolution is fine — transmittance varies smoothly)

**Parameterization**:
- x-axis: `mu = cos(zenith angle)`, mapped from -1 (downward toward ground) to +1 (upward toward space). When mu=0, light travels horizontally, grazing the atmosphere.
- y-axis: altitude, mapped from `planetRadius` (bottom = ground) to `atmosphereRadius` (top = edge of atmosphere)

**Shader logic**:
```glsl
void main() {
  float mu = mix(-1.0, 1.0, vUv.x);
  float radius = mix(planetRadius, atmosphereRadius, vUv.y);
  vec3 rayOrigin = vec3(0.0, radius, 0.0);
  vec3 rayDir = normalize(vec3(sqrt(max(1.0 - mu*mu, 0.0)), mu, 0.0));

  // Ray-sphere intersect to find path length through atmosphere
  vec2 atmosphereHit = raySphereIntersect(rayOrigin, rayDir, vec3(0.0), atmosphereRadius);
  vec2 planetHit = raySphereIntersect(rayOrigin, rayDir, vec3(0.0), planetRadius);

  float rayLength = atmosphereHit.y;
  if (planetHit.x > 0.0) { gl_FragColor = vec4(0.0, 0.0, 0.0, 1.0); return; }

  // March along ray, accumulate optical depth
  float stepSize = rayLength / float(TRANSMITTANCE_STEPS);
  float odR = 0.0, odM = 0.0, odO = 0.0;
  for (int i = 0; i < TRANSMITTANCE_STEPS; i++) {
    vec3 sp = rayOrigin + rayDir * (float(i) + 0.5) * stepSize;
    odR += rayleighDensity(sp) * stepSize;
    odM += mieDensity(sp) * stepSize;
    odO += ozoneDensity(sp) * stepSize;
  }

  vec3 tau = BETA_R * odR + BETA_M_EXT * odM + BETA_OZONE_ABS * odO;
  gl_FragColor = vec4(exp(-tau), 1.0);
}
```

**Reading the texture**: Pure white = 100% transmittance (clear path). Dark = light is extinct. The blue channel is the first to darken at low angles because Rayleigh scatters blue most strongly.

**Sampling in downstream LUTs**:
```glsl
vec3 sampleTransmittanceLUT(vec3 samplePoint, vec3 lightDir) {
  float h = length(samplePoint) - planetRadius;
  float mu = dot(normalize(samplePoint), lightDir);
  vec2 uv = vec2((mu + 1.0) * 0.5, h / ATMOSPHERE_HEIGHT);
  return texture2D(transmittanceLUT, uv).rgb;
}
```

## Sky View LUT

**Purpose**: Store the color of the sky for every direction in the sky dome, as seen from the camera's position. Replaces the primary raymarch for background (sky) pixels.

**Resolution**: 256 x 128

**Parameterization**:
- x-axis: azimuth around the projected sun direction, -PI to +PI
- y-axis: elevation angle, quadratic mapping `(vUv.y^2 - 0.5) * PI` — concentrates resolution near the horizon where color changes most

**Key function — ray direction from UV**:
```glsl
vec3 getSkyViewRayDir(vec2 uv, vec3 up) {
  vec3 forward = normalize(sunDirection - up * dot(sunDirection, up));
  vec3 right = normalize(cross(forward, up));
  float azimuth = (uv.x * 2.0 - 1.0) * PI;
  float elevation = (uv.y * uv.y - 0.5) * PI;
  float cosElev = cos(elevation);
  return normalize(cos(azimuth) * forward * cosElev
                 + sin(azimuth) * right * cosElev
                 + up * sin(elevation));
}
```

**Shader**: Same scattering accumulation loop as before, but uses `sampleTransmittanceLUT` instead of the nested light march.

**Sampling in composition**:
```glsl
vec2 getSkyViewLUTUv(vec3 rayDir, vec3 planetCenter) {
  vec3 up = normalize(cameraPosition - planetCenter);
  vec3 forward = normalize(sunDirection - up * dot(sunDirection, up));
  vec3 right = normalize(cross(forward, up));
  float vertical = clamp(dot(rayDir, up), -1.0, 1.0);
  vec3 horizontal = rayDir - up * vertical;
  float azimuth = atan(dot(horizontal, right), dot(horizontal, forward));
  float elevation = asin(vertical);
  float elevation01 = clamp(elevation / PI + 0.5, 0.0, 1.0);
  return vec2(azimuth / (2.0 * PI) + 0.5, sqrt(elevation01));
}
```

## Aerial Perspective LUT

**Purpose**: Store per-pixel atmospheric fog between camera and scene geometry. RGB = scattered light added, A = view transmittance (how much of the original scene color survives).

**Resolution**: Screen resolution (or half-resolution for performance)

**Parameterization**: Screen UV, same as the depth buffer. Uses depth to determine ray march distance.

**Shader**: Same as the atmosphere-post mode's scattering loop, but with `sampleTransmittanceLUT` replacing the light march. Outputs `vec4(scatteredLight, packedTransmittance)`.

**Deviation from Hillaire**: The original paper uses a 3D texture (32x32x32) parameterized by screen UV + depth. Heckel's implementation uses a 2D screen-resolution texture that reads depth directly. This is simpler but doesn't allow depth-independent reuse.

## Composition Pass

The final full-screen pass reads both LUTs and the original scene color:

```glsl
void mainImage(vec4 inputColor, vec2 uv, out vec4 outputColor) {
  float depth = readDepth(depthBuffer, uv);
  vec3 rayDir = normalize(getWorldPosition(uv, depth) - cameraPosition);
  vec3 color = inputColor.rgb;
  bool isBackground = depth >= 1.0 - 1e-7;

  // Scene geometry: blend with atmospheric haze
  if (!isBackground) {
    vec4 aerial = texture2D(aerialPerspectiveLUT, uv);
    color = color * aerial.a + aerial.rgb;
  }

  // Background: replace with sky color
  if (isBackground) {
    color = inputColor.rgb + sampleSkyViewLUT(rayDir, vec3(0.0));
  }

  color = ACESFilm(color);
  color = pow(color, vec3(1.0 / 2.2));
  outputColor = vec4(color, 1.0);
}
```

## Performance Comparison

| Approach | Per-pixel cost | Sunset quality |
|----------|---------------|----------------|
| Single-pass (sky-dome mode) | 24 primary x 8 light = 192 samples | Excellent |
| LUT-based | 1-3 texture reads | Excellent (precomputed) |

The LUT approach moves the O(n*m) cost to a one-time precomputation step (or per-frame at low resolution for moving sun), then the full-screen pass is O(1) per pixel.

## R3F FBO Setup Pattern

```jsx
const transmittanceFBO = useFBO(250, 64, { type: FloatType });
const skyViewFBO = useFBO(256, 128, { type: FloatType });
const aerialFBO = useFBO(width, height, { type: FloatType });

// Render each LUT to its FBO in useFrame
useFrame(({ gl }) => {
  gl.setRenderTarget(transmittanceFBO);
  gl.render(transmittanceScene, orthoCamera);

  gl.setRenderTarget(skyViewFBO);
  skyViewMaterial.uniforms.transmittanceLUT.value = transmittanceFBO.texture;
  gl.render(skyViewScene, orthoCamera);

  gl.setRenderTarget(aerialFBO);
  aerialMaterial.uniforms.transmittanceLUT.value = transmittanceFBO.texture;
  gl.render(aerialScene, orthoCamera);

  gl.setRenderTarget(null);
});
```
