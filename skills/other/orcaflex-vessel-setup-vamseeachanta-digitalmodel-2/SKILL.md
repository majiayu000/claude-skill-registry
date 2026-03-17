---
name: orcaflex-vessel-setup
description: Configure 6-DOF vessels in OrcaFlex with hydrodynamic properties, RAO import
  from AQWA, and vessel type creation. Covers initial position, orientation, calculation
  settings, and motion options.
version: 1.0.0
updated: 2026-01-17
category: offshore-engineering
triggers:
- vessel setup
- create vessel
- vessel configuration
- 6-DOF vessel
- vessel type
- vessel properties
- vessel initialization
- AQWA vessel import
---
# OrcaFlex Vessel Setup Skill

Configure 6-DOF vessels in OrcaFlex with hydrodynamic properties, RAO import, and calculation settings.

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
- Initial release with vessel configuration
- 6-DOF initialization and positioning
- AQWA vessel import with RAO loading
- Vessel type management

## When to Use

- Creating new vessels in OrcaFlex models
- Configuring 6-DOF motion properties
- Importing vessel hydrodynamics from AQWA
- Setting up vessel calculation options
- Defining vessel types with RAO data
- Configuring drift, damping, and wave loads

## Vessel Configuration Components

### Vessel Object

| Property | Description | Units |
|----------|-------------|-------|
| Name | Unique vessel identifier | - |
| VesselType | Reference to vessel type | - |
| Draught | Operating draft | m |
| InitialPosition | X, Y, Z coordinates | m |
| Orientation | Heading angle | deg |
| Connection | Connection point type | - |

### Vessel Type

| Property | Description | Units |
|----------|-------------|-------|
| Name | Type identifier | - |
| Length | Reference length | m |
| DisplacementRAOs | Motion response operators | m/m, deg/m |
| LoadRAOs | Force response operators | kN/m |
| StiffnessAddedMassDamping | Hydrodynamic coefficients | - |
| QTFs | Quadratic Transfer Functions | - |

## Configuration

### Basic Vessel Configuration

```yaml
# configs/vessel_config.yml

vessel:
  name: "FPSO"
  vessel_type: "FPSO_Type"

  # Position and orientation
  initial_position:
    x: 0.0      # m
    y: 0.0      # m
    z: 0.0      # m (relative to sea surface)

  orientation: 0.0    # deg (heading)
  draught: 15.5       # m

  # Calculation settings
  calculation:
    include_applied_loads: "6 DOF"
    primary_motion: "6 DOF calculated (no wave load RAOs)"
    superimposed_motion: "None"

    # Wave load options
    wave_load: "Calculated from RAOs (first order)"
    drift_load: "Calculated from QTFs"

    # Environmental loads
    current_load: "Calculated"
    wind_load: "Calculated"

    # Damping
    damping_calculation: "From hydrodynamic database"

vessel_type:
  name: "FPSO_Type"
  length: 300.0        # m

  # RAO data source
  hydrodynamic_data:
    source: "aqwa"     # or "orcaflex", "csv"
    file: "data/fpso_aqwa.lis"

  # RAO import settings
  rao_import:
    displacement_raos: true
    load_raos: true
    stiffness_added_mass_damping: true
    qtfs: true
    qtf_type: "Full"   # or "Newman"
```

### AQWA Import Configuration

```yaml
# configs/aqwa_vessel_import.yml

aqwa_import:
  # Source file
  source_file: "data/vessel_aqwa.lis"

  # Body mapping (for multi-body systems)
  body_mapping:
    - aqwa_body: 1
      orcaflex_vessel: "FPSO"
    - aqwa_body: 2
      orcaflex_vessel: "Shuttle_Tanker"

  # Data to import
  import_data:
    displacement_raos: true
    load_raos: true
    added_mass: true
    damping: true
    stiffness: true
    qtfs:
      enabled: true
      type: "Full"     # Full or Newman approximation

  # RAO conventions
  conventions:
    frequency_units: "rad/s"
    phase_convention: "OrcaFlex"   # Check AQWA vs OrcaFlex sign
```

## Python API

### Basic Vessel Creation

```python
from digitalmodel.solvers.fea_model.Vessel_components import Vessel
from digitalmodel.solvers.fea_model.VesselType_components import VesselType

def create_vessel(config: dict) -> dict:
    """
    Create OrcaFlex vessel configuration.

    Args:
        config: Vessel configuration dictionary

    Returns:
        OrcaFlex-ready vessel properties
    """
    # Create vessel type
    vessel_type = VesselType(
        name=config["vessel_type"]["name"],
        length=config["vessel_type"]["length"]
    )

    # Create vessel object
    vessel = Vessel(
        name=config["vessel"]["name"],
        vessel_type=vessel_type.name,
        draught=config["vessel"]["draught"]
    )

    # Set position
    vessel.set_initial_position(
        x=config["vessel"]["initial_position"]["x"],
        y=config["vessel"]["initial_position"]["y"],
        z=config["vessel"]["initial_position"]["z"]
    )

    # Set orientation
    vessel.set_orientation(config["vessel"]["orientation"])

    # Get OrcaFlex properties
    return vessel.get_orcaflex_properties()

# Example usage
config = {
    "vessel": {
        "name": "FPSO",
        "draught": 15.5,
        "initial_position": {"x": 0, "y": 0, "z": 0},
        "orientation": 0.0
    },
    "vessel_type": {
        "name": "FPSO_Type",
        "length": 300.0
    }
}

vessel_props = create_vessel(config)
```

### AQWA Vessel Import

```python
from digitalmodel.solvers.fea_model.preprocess.load_vessel import LoadVessel
import OrcFxAPI

def import_vessel_from_aqwa(
    model: OrcFxAPI.Model,
    aqwa_file: str,
    vessel_name: str,
    import_config: dict = None
) -> OrcFxAPI.OrcaFlexObject:
    """
    Import vessel hydrodynamics from AQWA.

    Args:
        model: OrcaFlex model
        aqwa_file: Path to AQWA .lis file
        vessel_name: Name for the vessel type
        import_config: Optional import settings

    Returns:
        OrcaFlex vessel type object
    """
    # Default import settings
    if import_config is None:
        import_config = {
            "displacement_raos": True,
            "load_raos": True,
            "stiffness_added_mass_damping": True,
            "qtfs": True,
            "qtf_type": "Full"
        }

    # Create vessel type
    vessel_type = model.CreateObject(OrcFxAPI.otVesselType, vessel_name)

    # Configure data import
    vessel_type.DisplacementRAOs = OrcFxAPI.vdtLoadRAOs
    vessel_type.LoadRAOs = OrcFxAPI.vdtLoadRAOs

    if import_config.get("stiffness_added_mass_damping"):
        vessel_type.StiffnessAddedMassDamping = OrcFxAPI.vdtStiffnessAddedMassDamping

    # Set import file
    vessel_type.ImportFile = aqwa_file

    # Configure QTF import
    if import_config.get("qtfs"):
        if import_config.get("qtf_type") == "Full":
            vessel_type.FullQTFImportMethod = OrcFxAPI.fqimFromFile
        else:
            vessel_type.NewmanApproximation = True

    # Execute import
    vessel_type.ImportHydrodynamicData()

    return vessel_type

# Example usage
model = OrcFxAPI.Model()
vessel_type = import_vessel_from_aqwa(
    model=model,
    aqwa_file="data/fpso_aqwa.lis",
    vessel_name="FPSO_Type"
)

print(f"Imported vessel type: {vessel_type.Name}")
```

### Vessel Calculation Settings

```python
import OrcFxAPI

def configure_vessel_calculations(
    vessel: OrcFxAPI.OrcaFlexObject,
    settings: dict
) -> None:
    """
    Configure vessel calculation options.

    Args:
        vessel: OrcaFlex vessel object
        settings: Calculation settings dictionary
    """
    # Primary motion
    motion_map = {
        "6 DOF calculated": OrcFxAPI.vmCalculated,
        "6 DOF calculated (no wave load RAOs)": OrcFxAPI.vmCalculatedNoRAO,
        "Prescribed": OrcFxAPI.vmPrescribed,
        "None": OrcFxAPI.vmNone
    }
    vessel.PrimaryMotion = motion_map.get(
        settings.get("primary_motion", "6 DOF calculated"),
        OrcFxAPI.vmCalculated
    )

    # Wave loads
    wave_load_map = {
        "Calculated from RAOs (first order)": OrcFxAPI.wlCalculatedFromRAOs,
        "Calculated (full hydrodynamic)": OrcFxAPI.wlCalculated,
        "None": OrcFxAPI.wlNone
    }
    vessel.IncludeWaveLoad = wave_load_map.get(
        settings.get("wave_load", "Calculated from RAOs (first order)"),
        OrcFxAPI.wlCalculatedFromRAOs
    )

    # Drift loads
    drift_load_map = {
        "Calculated from QTFs": OrcFxAPI.dlCalculatedFromQTFs,
        "Newman approximation": OrcFxAPI.dlNewmanApproximation,
        "None": OrcFxAPI.dlNone
    }
    vessel.IncludeDriftLoad = drift_load_map.get(
        settings.get("drift_load", "None"),
        OrcFxAPI.dlNone
    )

    # Current load
    vessel.IncludeCurrentLoad = settings.get("current_load", True)

    # Wind load
    vessel.IncludeWindLoad = settings.get("wind_load", True)

# Example usage
vessel = model["FPSO"]
configure_vessel_calculations(vessel, {
    "primary_motion": "6 DOF calculated",
    "wave_load": "Calculated from RAOs (first order)",
    "drift_load": "Calculated from QTFs",
    "current_load": True,
    "wind_load": True
})
```

### Multi-Body Import

```python
import OrcFxAPI

def import_multi_body_system(
    model: OrcFxAPI.Model,
    aqwa_file: str,
    body_mapping: list
) -> dict:
    """
    Import multi-body system from AQWA.

    Args:
        model: OrcaFlex model
        aqwa_file: Path to AQWA .lis file
        body_mapping: List of {aqwa_body: int, orcaflex_vessel: str}

    Returns:
        Dictionary of vessel type objects
    """
    vessel_types = {}

    for mapping in body_mapping:
        aqwa_body = mapping["aqwa_body"]
        vessel_name = mapping["orcaflex_vessel"]

        # Create vessel type
        vessel_type = model.CreateObject(
            OrcFxAPI.otVesselType,
            f"{vessel_name}_Type"
        )

        # Configure body map
        body_map = OrcFxAPI.VesselTypeDataDiffractionImportBodyMap()
        body_map.AQWABody = aqwa_body
        body_map.OrcaFlexVesselType = vessel_type

        # Set import file and body mapping
        vessel_type.ImportFile = aqwa_file
        vessel_type.DiffractionImportBodyMap = [body_map]

        # Import data
        vessel_type.ImportHydrodynamicData()

        vessel_types[vessel_name] = vessel_type

    return vessel_types

# Example: FPSO + Shuttle Tanker system
body_mapping = [
    {"aqwa_body": 1, "orcaflex_vessel": "FPSO"},
    {"aqwa_body": 2, "orcaflex_vessel": "Shuttle_Tanker"}
]

vessel_types = import_multi_body_system(
    model=model,
    aqwa_file="data/multi_body_aqwa.lis",
    body_mapping=body_mapping
)
```

## Output Formats

### Vessel Properties YAML

```yaml
Vessels:
  - Name: FPSO
    VesselType: FPSO_Type
    Draught: 15.5
    Connection: Free
    InitialPosition: [0.0, 0.0, 0.0]
    InitialHeading: 0.0

    Calculation:
      PrimaryMotion: 6 DOF calculated
      SuperimposedMotion: None
      IncludeWaveLoad: Calculated from RAOs (first order)
      IncludeDriftLoad: Calculated from QTFs
      IncludeCurrentLoad: Yes
      IncludeWindLoad: Yes

VesselTypes:
  - Name: FPSO_Type
    Length: 300.0
    DisplacementRAOs: Imported from file
    LoadRAOs: Imported from file
    StiffnessAddedMassDamping: Imported from file
    QTFs: Full QTFs from file
```

## Common Use Cases

### 1. FPSO with AQWA Hydrodynamics

```python
# Import FPSO hydrodynamics from AQWA
vessel_type = import_vessel_from_aqwa(
    model=model,
    aqwa_file="fpso_aqwa.lis",
    vessel_name="FPSO_Type",
    import_config={
        "displacement_raos": True,
        "load_raos": True,
        "qtfs": True,
        "qtf_type": "Full"
    }
)

# Create vessel using the type
vessel = model.CreateObject(OrcFxAPI.otVessel, "FPSO")
vessel.VesselType = "FPSO_Type"
vessel.Draught = 22.5
vessel.InitialPosition = [0, 0, 0]
```

### 2. Shuttle Tanker Approach

```python
# Shuttle tanker at offset position
vessel = model.CreateObject(OrcFxAPI.otVessel, "Shuttle_Tanker")
vessel.VesselType = "Shuttle_Type"
vessel.InitialPosition = [80, 0, 0]  # 80m offset from FPSO
vessel.InitialHeading = 180  # Stern-to-stern
```

### 3. Barge for Installation

```python
# Installation barge
vessel = model.CreateObject(OrcFxAPI.otVessel, "Installation_Barge")
vessel.VesselType = "Barge_Type"
vessel.PrimaryMotion = OrcFxAPI.vmPrescribed  # Follow prescribed motion
```

## Best Practices

### Data Import

1. **Verify AQWA output** - Check analysis completed successfully
2. **Check sign conventions** - AQWA vs OrcaFlex phase conventions
3. **Validate RAO magnitudes** - Compare with expected responses
4. **Test at single frequency** - Verify motion response

### Vessel Configuration

1. **Correct draught** - Match analysis loading condition
2. **Coordinate system** - Align with AQWA body axes
3. **Connection point** - Set appropriate attachment
4. **Calculation options** - Match analysis requirements

### Multi-Body Systems

1. **Body mapping** - Match AQWA body numbers
2. **Coupling terms** - Include hydrodynamic interaction
3. **Connection constraints** - Link vessels appropriately

## Error Handling

```python
try:
    vessel_type = import_vessel_from_aqwa(model, aqwa_file, "Vessel_Type")
except OrcFxAPI.OrcaFlexError as e:
    print(f"Import failed: {e}")
    print("Check AQWA file path and format")

except FileNotFoundError:
    print("AQWA file not found")

except ValueError as e:
    print(f"Configuration error: {e}")
```

## Related Skills

- [orcaflex-modeling](../orcaflex-modeling/SKILL.md) - Run OrcaFlex simulations
- [orcaflex-rao-import](../orcaflex-rao-import/SKILL.md) - RAO data import
- [aqwa-analysis](../aqwa-analysis/SKILL.md) - AQWA analysis
- [hydrodynamics](../hydrodynamics/SKILL.md) - Hydrodynamic coefficients

## References

- OrcaFlex: Vessel Type Data
- OrcaFlex: Importing Hydrodynamic Data
- ANSYS AQWA: Output File Format
- Source: `src/digitalmodel/modules/fea_model/Vessel_components.py`
- Source: `src/digitalmodel/modules/fea_model/VesselType_components.py`
- Source: `src/digitalmodel/modules/fea_model/preprocess/load_vessel.py`
