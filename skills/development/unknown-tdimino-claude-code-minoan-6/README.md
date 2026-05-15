# atmosphere-shader

Physically-based atmospheric scattering shaders — sky domes, planetary atmospheres, LUT-optimized pipelines, depth-aware post-processing. Four progressive modes from flat backdrop to production-grade planetary rendering.

## Modes

| Mode | Description | Output |
|------|-------------|--------|
| `sky-dome` | Single-pass Rayleigh + Mie + Ozone scattering, flat sky backdrop | GLSL fragment shader |
| `atmosphere-post` | Depth-aware post-processing with atmospheric fog, world-space reconstruction | Three.js/R3F post-processing effect |
| `planet` | Spherical atmosphere shell via ray-sphere intersection, logarithmic depth, eclipse handling | Three.js/R3F scene component |
| `lut` | Transmittance + Sky View + Aerial Perspective LUTs, FBO pipeline, composition pass | Three.js/R3F multi-pass pipeline |

## Architecture

```
atmosphere-shader/
├── SKILL.md                              Skill definition (4 modes, gotchas, code patterns)
├── README.md                             This file
└── references/
    ├── scattering-coefficients.md        Earth, Mars, custom planet parameter tables
    └── hillaire-lut-pipeline.md          LUT architecture from Hillaire (2020)
```

## Key Gotchas

The six concrete failure modes this skill corrects — things Claude gets wrong without the reference material:

1. **Wrong scattering coefficients** — invents plausible but physically incorrect beta values
2. **Missing nested light march** — produces blue gradient but no sunsets
3. **Incorrect logarithmic depth reconstruction** — uses linear formula at planetary scale
4. **No LUT pipeline knowledge** — attempts full nested raymarch at screen resolution
5. **Wrong phase function normalization** — drops `(2 + g^2)` denominator in Henyey-Greenstein
6. **Missing ozone** — loses purple twilight and correct sky-blue shift

## Origin & Attribution

- **Source article**: [On Rendering the Sky, Sunsets, and Planets](https://blog.maximeheckel.com/posts/on-rendering-the-sky-sunsets-and-planets/) by **Maxime Heckel** ([@MaximeHeckel](https://x.com/MaximeHeckel)), 2026-05-12
- **LUT approach**: Sebastian Hillaire, "A Scalable and Production Ready Sky and Atmosphere Rendering Technique" ([EGSR 2020](https://sebh.github.io/publications/egsr2020.pdf))
- **Foundational theory**: Nishita et al., "Display of the Earth Taking into Account Atmospheric Scattering" (SIGGRAPH 1993)
- **Production reference**: [three-geospatial](https://github.com/takram-design-engineering/three-geospatial) by Shota Matsuda
- **Surfaced by**: [theclaymethod](https://github.com/theclaymethod), who brought the Heckel article to our attention
