---
name: orcaflex-environment-config
description: Configure OrcaFlex environmental conditions including wave spectra (JONSWAP,
  Dean Stream), current profiles, wind loading, and seabed properties for offshore
  analysis.
version: 1.0.0
updated: 2026-01-17
category: offshore-engineering
triggers:
- environment setup
- wave configuration
- current profile
- wind setup
- JONSWAP spectrum
- sea state
- environmental loading
- seabed properties
---
# OrcaFlex Environment Configuration Skill

Configure complete environmental conditions for OrcaFlex simulations including waves, currents, wind, and seabed.

## Version Metadata

```yaml
version: 1.0.0
python_min_version: '3.10'
dependencies:
  orcaflex-modeling: '>=2.0.0,<3.0.0'
  hydrodynamics: '>=1.0.0,<2.0.0'
orcaflex_version: '>=11.0'
compatibility:
  tested_python:
  - '3.10'
  - '3.11'
  - '3.12'
  - '3.13'
  os:
  - Windows
  - Linux
  - macOS
```

## Changelog

### [1.0.0] - 2026-01-17

**Added:**
- Initial release with complete environment configuration
- Wave spectrum support (JONSWAP, Dean Stream, Ochi-Hubble)
- Current profile configuration
- Wind loading setup
- Seabed property management

## When to Use

- Setting up wave conditions for simulations
- Configuring depth-varying current profiles
- Adding wind loads to vessel/structure analysis
- Defining seabed properties for touchdown regions
- Creating consistent environmental load cases
- Multi-directional wave/current combinations

## Environment Components

### Wave Types

| Type | Description | Parameters |
|------|-------------|------------|
| **JONSWAP** | Joint North Sea Wave Project spectrum | Hs, Tp, gamma |
| **Dean Stream** | Non-linear stream function | H, T, order |
| **Ochi-Hubble** | Double-peaked spectrum | Hs1, Tp1, Hs2, Tp2 |
| **Pierson-Moskowitz** | Fully developed sea | Hs, Tp |
| **Torsethaugen** | Combined wind-sea/swell | Hs, Tp |
| **User Defined** | Custom spectrum | S(f) table |

### Current Profile

| Parameter | Description | Units |
|-----------|-------------|-------|
| Surface Speed | Current at water surface | m/s |
| Direction | Current direction | deg |
| Profile Type | Depth variation method | - |
| Depth Points | Depth/speed pairs | m, m/s |

### Wind Parameters

| Parameter | Description | Units |
|-----------|-------------|-------|
| Speed | Reference wind speed | m/s |
| Direction | Wind from direction | deg |
| Height | Reference height | m |
| Profile | Vertical profile type | - |

## Configuration

### Complete Environment Configuration

```yaml
# configs/environment_config.yml

environment:
  # General settings
  water_depth: 1500.0     # m
  water_density: 1025.0   # kg/m³
  air_density: 1.225      # kg/m³

  # Wave configuration
  waves:
    type: "JONSWAP"
    significant_height: 5.5    # m (Hs)
    peak_period: 12.0          # s (Tp)
    direction: 180.0           # deg (waves from)
    gamma: 3.3                 # JONSWAP peak enhancement
    spreading: "Cos2s"         # Directional spreading
    spreading_exponent: 2      # s parameter

    # Or multiple wave components
    components:
      - type: "JONSWAP"
        Hs: 4.0
        Tp: 10.0
        direction: 180.0
        gamma: 2.5
      - type: "Swell"
        Hs: 2.0
        Tp: 16.0
        direction: 210.0
        gamma: 6.0

  # Current configuration
  current:
    surface_speed: 1.2      # m/s
    direction: 165.0        # deg (flowing towards)
    profile_type: "Interpolated"

    # Depth profile
    depth_profile:
      - depth: 0.0
        factor: 1.0
      - depth: 50.0
        factor: 0.9
      - depth: 200.0
        factor: 0.5
      - depth: 500.0
        factor: 0.2
      - depth: 1500.0
        factor: 0.05

  # Wind configuration
  wind:
    speed: 25.0           # m/s (1-hour mean)
    direction: 180.0      # deg (from)
    reference_height: 10.0  # m above sea level
    profile: "Power Law"
    exponent: 0.12        # Wind shear exponent

    # Load inclusion
    apply_to:
      vessels: true
      lines: false
      buoys: true

  # Seabed configuration
  seabed:
    type: "Flat"          # or "3D Profile"
    stiffness: 100.0      # kN/m/m²
    friction: 0.5         # Coefficient
    damping: 1.0          # % critical
    slope: 0.0            # deg
```

### Sea State Matrix Configuration

```yaml
# configs/sea_states.yml

sea_states:
  # Design conditions
  100_year:
    Hs: 8.5
    Tp: 14.0
    gamma: 3.3
    current_speed: 1.5
    wind_speed: 35.0

  10_year:
    Hs: 6.5
    Tp: 12.5
    gamma: 3.0
    current_speed: 1.2
    wind_speed: 28.0

  1_year:
    Hs: 5.0
    Tp: 11.0
    gamma: 2.5
    current_speed: 1.0
    wind_speed: 22.0

  operational:
    Hs: 2.5
    Tp: 8.0
    gamma: 2.0
    current_speed: 0.5
    wind_speed: 12.0

# Heading combinations
headings:
  wave: [0, 15, 30, 45, 60, 75, 90]
  current_offset: 0    # degrees from wave
  wind_offset: 0       # degrees from wave
```

## Python API

### Basic Environment Setup

```python
from digitalmodel.solvers.fea_model.environment_components import Environment

def setup_environment(config: dict) -> dict:
    """
    Configure OrcaFlex environment from config.

    Args:
        config: Environment configuration dictionary

    Returns:
        OrcaFlex-ready environment properties
    """
    env = Environment()

    # Set general properties
    env.set_water_depth(config["water_depth"])
    env.set_water_density(config.get("water_density", 1025.0))

    # Configure waves
    wave_config = config["waves"]
    if wave_config["type"] == "JONSWAP":
        env.set_jonswap_spectrum(
            Hs=wave_config["significant_height"],
            Tp=wave_config["peak_period"],
            gamma=wave_config.get("gamma", 3.3),
            direction=wave_config["direction"]
        )

    # Configure current
    current_config = config["current"]
    env.set_current_profile(
        surface_speed=current_config["surface_speed"],
        direction=current_config["direction"],
        profile=current_config["depth_profile"]
    )

    # Configure wind
    wind_config = config["wind"]
    env.set_wind(
        speed=wind_config["speed"],
        direction=wind_config["direction"],
        reference_height=wind_config["reference_height"]
    )

    return env.get_orcaflex_environment()

# Example usage
config = {
    "water_depth": 1500.0,
    "waves": {
        "type": "JONSWAP",
        "significant_height": 5.5,
        "peak_period": 12.0,
        "direction": 180.0,
        "gamma": 3.3
    },
    "current": {
        "surface_speed": 1.2,
        "direction": 165.0,
        "depth_profile": [
            {"depth": 0, "factor": 1.0},
            {"depth": 500, "factor": 0.3}
        ]
    },
    "wind": {
        "speed": 25.0,
        "direction": 180.0,
        "reference_height": 10.0
    }
}

env_props = setup_environment(config)
```

### Direct OrcFxAPI Configuration

```python
import OrcFxAPI

def configure_orcaflex_environment(
    model: OrcFxAPI.Model,
    config: dict
) -> OrcFxAPI.OrcaFlexObject:
    """
    Configure environment directly in OrcFxAPI.

    Args:
        model: OrcaFlex model
        config: Environment configuration

    Returns:
        Environment object
    """
    env = model.environment
    general = model.general

    # General settings
    general.WaterDepth = config["water_depth"]
    general.WaterDensity = config.get("water_density", 1025.0)
    general.AirDensity = config.get("air_density", 1.225)

    # Wave configuration
    waves = config["waves"]

    if waves["type"] == "JONSWAP":
        env.WaveType = OrcFxAPI.wtIrregular
        env.WaveSpectrumType = OrcFxAPI.wsJONSWAP
        env.WaveHs = waves["significant_height"]
        env.WaveTp = waves["peak_period"]
        env.WaveGamma = waves.get("gamma", 3.3)
        env.WaveDirection = waves["direction"]

    elif waves["type"] == "Dean Stream":
        env.WaveType = OrcFxAPI.wtDeanStream
        env.WaveHeight = waves["height"]
        env.WavePeriod = waves["period"]
        env.StreamFunctionOrder = waves.get("order", 10)
        env.WaveDirection = waves["direction"]

    elif waves["type"] == "Regular":
        env.WaveType = OrcFxAPI.wtAiry
        env.WaveHeight = waves["height"]
        env.WavePeriod = waves["period"]
        env.WaveDirection = waves["direction"]

    # Directional spreading
    if waves.get("spreading"):
        env.SpreadingType = OrcFxAPI.stCosNTheta
        env.SpreadingExponent = waves.get("spreading_exponent", 2)

    return env

# Example
env = configure_orcaflex_environment(model, config)
```

### Current Profile Configuration

```python
import OrcFxAPI

def set_current_profile(
    model: OrcFxAPI.Model,
    surface_speed: float,
    direction: float,
    depth_factors: list
) -> None:
    """
    Configure depth-varying current profile.

    Args:
        model: OrcaFlex model
        surface_speed: Surface current speed (m/s)
        direction: Current direction (deg)
        depth_factors: List of (depth, factor) tuples
    """
    env = model.environment

    # Set current method
    env.CurrentMethod = OrcFxAPI.cmInterpolated
    env.RefCurrentSpeed = surface_speed
    env.RefCurrentDirection = direction

    # Set profile points
    env.NumberOfCurrentDataPoints = len(depth_factors)

    for i, (depth, factor) in enumerate(depth_factors):
        env.CurrentDepth[i] = depth
        env.CurrentFactor[i] = factor

# Example: Gulf of Mexico loop current profile
current_profile = [
    (0.0, 1.0),      # Surface
    (50.0, 0.95),    # Near surface
    (100.0, 0.8),    # Thermocline
    (300.0, 0.4),    # Mid-depth
    (600.0, 0.15),   # Deep
    (1500.0, 0.02)   # Near seabed
]

set_current_profile(
    model,
    surface_speed=1.5,
    direction=165.0,
    depth_factors=current_profile
)
```

### Wind Configuration

```python
import OrcFxAPI

def configure_wind(
    model: OrcFxAPI.Model,
    speed: float,
    direction: float,
    reference_height: float = 10.0,
    apply_to_vessels: bool = True,
    apply_to_lines: bool = False,
    apply_to_buoys: bool = True
) -> None:
    """
    Configure wind loading.

    Args:
        model: OrcaFlex model
        speed: Wind speed at reference height (m/s)
        direction: Wind from direction (deg)
        reference_height: Reference height above sea level (m)
        apply_to_vessels: Include wind on vessels
        apply_to_lines: Include wind on lines
        apply_to_buoys: Include wind on buoys
    """
    env = model.environment

    # Wind parameters
    env.WindSpeed = speed
    env.WindDirection = direction
    env.WindReferenceHeight = reference_height

    # Wind profile (power law)
    env.VerticalWindVariation = OrcFxAPI.vwvPowerLaw
    env.WindExponent = 0.12  # Typical offshore value

    # Apply to objects
    env.IncludeVesselWindLoads = apply_to_vessels
    env.IncludeLineWindLoads = apply_to_lines
    env.IncludeBuoyWindLoads = apply_to_buoys

# Example
configure_wind(
    model,
    speed=25.0,
    direction=180.0,
    reference_height=10.0,
    apply_to_vessels=True,
    apply_to_buoys=True
)
```

### JONSWAP Gamma Calculation

```python
import math

def calculate_jonswap_gamma(Hs: float, Tp: float) -> float:
    """
    Calculate JONSWAP gamma from Hs and Tp.

    Uses DNV-RP-C205 relationship.

    Args:
        Hs: Significant wave height (m)
        Tp: Peak period (s)

    Returns:
        JONSWAP gamma parameter
    """
    steepness = 2 * math.pi * Hs / (9.81 * Tp**2)

    # DNV-RP-C205 empirical relationship
    if steepness <= 0.031:
        gamma = 5.0
    elif steepness >= 0.054:
        gamma = 1.0
    else:
        gamma = math.exp(3.484 * (1 - 0.1975 * (0.036 - steepness) * Tp**4 / Hs**2))

    return max(1.0, min(7.0, gamma))

# Example
Hs = 5.5  # m
Tp = 12.0  # s
gamma = calculate_jonswap_gamma(Hs, Tp)
print(f"Calculated gamma: {gamma:.2f}")
```

### Multi-Directional Waves

```python
import OrcFxAPI

def configure_multi_directional_waves(
    model: OrcFxAPI.Model,
    wave_components: list
) -> None:
    """
    Configure multi-directional wave system.

    Args:
        model: OrcaFlex model
        wave_components: List of wave dictionaries
    """
    env = model.environment

    # Enable wave trains
    env.NumberOfWaveTrains = len(wave_components)

    for i, wave in enumerate(wave_components):
        env.WaveTrainType[i] = OrcFxAPI.wtIrregular
        env.WaveTrainSpectrumType[i] = OrcFxAPI.wsJONSWAP
        env.WaveTrainHs[i] = wave["Hs"]
        env.WaveTrainTp[i] = wave["Tp"]
        env.WaveTrainGamma[i] = wave.get("gamma", 3.3)
        env.WaveTrainDirection[i] = wave["direction"]

        # Optional: Set spectral seed
        if "seed" in wave:
            env.WaveTrainSeed[i] = wave["seed"]

# Example: Wind sea + swell
wave_components = [
    {"Hs": 4.0, "Tp": 10.0, "gamma": 2.5, "direction": 180, "seed": 12345},
    {"Hs": 2.0, "Tp": 16.0, "gamma": 6.0, "direction": 210, "seed": 67890}
]

configure_multi_directional_waves(model, wave_components)
```

## Output Formats

### Environment YAML Output

```yaml
Environment:
  WaterDepth: 1500.0
  WaterDensity: 1025.0
  SeabedType: Flat
  SeabedStiffness: 100.0

  Waves:
    Type: JONSWAP
    Hs: 5.5
    Tp: 12.0
    Gamma: 3.3
    Direction: 180.0
    SpreadingType: Cos2s
    SpreadingExponent: 2

  Current:
    Method: Interpolated
    RefSpeed: 1.2
    RefDirection: 165.0
    Profile:
      - [0.0, 1.0]
      - [50.0, 0.9]
      - [200.0, 0.5]
      - [500.0, 0.2]

  Wind:
    Speed: 25.0
    Direction: 180.0
    ReferenceHeight: 10.0
    Profile: PowerLaw
    Exponent: 0.12
```

## Best Practices

### Wave Configuration

1. **Gamma selection** - Use calculated value or site-specific data
2. **Frequency range** - Ensure adequate coverage for RAO response
3. **Duration** - 3-hour simulations for design
4. **Seed selection** - Use consistent seeds for comparisons

### Current Profile

1. **Depth resolution** - Include thermocline effects
2. **Near-seabed** - Adequate resolution at touchdown
3. **Directionality** - May differ from wave direction
4. **Variation** - Consider loop current or seasonal changes

### Wind Loading

1. **Gust factor** - Include for dynamic response
2. **Height correction** - Apply appropriate profile
3. **Drag coefficients** - Verify vessel wind areas
4. **Shielding** - Consider in tandem operations

## Error Handling

```python
try:
    env_props = setup_environment(config)
except ValueError as e:
    print(f"Configuration error: {e}")
    print("Check wave/current/wind parameters")

except KeyError as e:
    print(f"Missing parameter: {e}")
```

## Related Skills

- [orcaflex-modeling](../orcaflex-modeling/SKILL.md) - Run OrcaFlex simulations
- [orcaflex-operability](../orcaflex-operability/SKILL.md) - Multi-sea-state analysis
- [hydrodynamics](../hydrodynamics/SKILL.md) - Wave spectra management
- [mooring-design](../mooring-design/SKILL.md) - Environmental loading

## References

- DNV-RP-C205: Environmental Conditions and Loads
- API RP 2MET: Metocean
- OrcaFlex: Environment Data
- Source: `src/digitalmodel/modules/fea_model/environment_components.py`
