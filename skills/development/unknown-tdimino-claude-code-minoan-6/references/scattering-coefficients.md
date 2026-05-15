# Scattering Coefficients Reference

## Earth

Standard atmosphere parameters validated against Nishita (1993) and Hillaire (2020).

```glsl
// Rayleigh
const vec3 BETA_R = vec3(5.8e-3, 13.5e-3, 33.1e-3); // 1/km — R scatters least, B most
const float RAYLEIGH_SCALE_HEIGHT = 8.0;               // km

// Mie
const float BETA_M_SCATTER = 21e-3;      // 1/km
const float BETA_M_EXT = 21e-3 * 1.1;    // scatter + absorption
const float MIE_SCALE_HEIGHT = 1.2;       // km
const float MIE_G = 0.76;                 // Henyey-Greenstein anisotropy (0 = isotropic, 1 = full forward)

// Ozone
const vec3 BETA_OZONE_ABS = vec3(0.65e-3, 1.881e-3, 0.085e-3); // 1/km — absorbs, does not scatter
const vec3 BETA_OZONE_SCATTER = vec3(0.0);                       // zero — ozone only absorbs
const float OZONE_CENTER_HEIGHT = 25.0;   // km — peak density altitude
const float OZONE_WIDTH = 15.0;           // km — half-width of density profile

// Geometry
const float PLANET_RADIUS = 6371.0;       // km
const float ATMOSPHERE_HEIGHT = 100.0;     // km (Karman line)
const float ATMOSPHERE_RADIUS = 6471.0;    // PLANET_RADIUS + ATMOSPHERE_HEIGHT

// Lighting
const float SUN_INTENSITY = 22.0;         // tunable — affects overall brightness
```

## Mars

Dusty, CO2-dominated atmosphere. Thinner than Earth. Produces orange sky with distinctive blue sunset (Mie forward-scatters blue at sunset angles through the dust).

```glsl
// Approximative values
const float PLANET_RADIUS = 3390.0;        // km
const float ATMOSPHERE_RADIUS = 3500.0;     // ~110 km thick
const float RAYLEIGH_SCALE_HEIGHT = 11.1;   // km — taller due to lower gravity
const vec3 BETA_R = vec3(0.019, 0.013, 0.0057); // inverted vs Earth — red scatters more
const float MIE_SCALE_HEIGHT = 1.5;
const float BETA_M_SCATTER = 0.04;          // higher dust content
const float BETA_M_EXT = 0.044;
const float MIE_G = 0.65;                   // less forward-biased than Earth
const float OZONE_CENTER_HEIGHT = 0.0;      // no ozone layer
const float OZONE_WIDTH = 1.0;
const vec3 BETA_OZONE_ABS = vec3(0.0);      // no ozone absorption
const float SUN_INTENSITY = 15.0;           // further from sun
```

## Custom Planet Template

Adjust these knobs to create alien atmospheres:

| Parameter | Effect | Earth | Mars |
|-----------|--------|-------|------|
| `BETA_R` | Sky color (higher channels scatter more) | Blue-dominant | Red-dominant |
| `RAYLEIGH_SCALE_HEIGHT` | How fast atmosphere thins with altitude | 8 km | 11.1 km |
| `BETA_M_SCATTER` | Haze/glow intensity around sun | 21e-3 | 0.04 |
| `MIE_G` | Forward-scatter bias (0 = uniform, 1 = laser) | 0.76 | 0.65 |
| `OZONE_CENTER_HEIGHT` | Altitude of ozone layer | 25 km | 0 (none) |
| `SUN_INTENSITY` | Overall brightness | 22 | 15 |
| `ATMOSPHERE_HEIGHT` | Shell thickness | 100 km | 110 km |

### Gas Giant (hypothetical)

```glsl
const vec3 BETA_R = vec3(2.0e-3, 4.0e-3, 8.0e-3);
const float RAYLEIGH_SCALE_HEIGHT = 27.0;
const float BETA_M_SCATTER = 0.1;
const float MIE_G = 0.85;
const float ATMOSPHERE_HEIGHT = 500.0;
const float SUN_INTENSITY = 8.0;
```

### Thin Lunar-Type (hypothetical)

```glsl
const vec3 BETA_R = vec3(0.5e-3, 1.0e-3, 2.0e-3);
const float RAYLEIGH_SCALE_HEIGHT = 4.0;
const float BETA_M_SCATTER = 0.001;
const float MIE_G = 0.5;
const float ATMOSPHERE_HEIGHT = 20.0;
const float SUN_INTENSITY = 30.0;
```
