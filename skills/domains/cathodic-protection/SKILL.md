---
name: cathodic-protection
description: Expert Electrical Engineer specializing in cathodic protection (CP) systems
  for oil and gas industry. Use for CP system design, corrosion prevention, sacrificial
  anode calculations, impressed current systems, pipeline integrity, coating defects,
  and NACE/ISO standards compliance.
version: 1.0.0
updated: 2025-01-02
category: offshore-engineering
triggers:
- cathodic protection
- corrosion prevention
- sacrificial anode
- impressed current
- ICCP system
- SACP system
- pipeline CP
- anode design
- NACE standards
- ISO 15589
- DNV-RP-B401
- coating breakdown
- stray current
---
# Cathodic Protection Skill

Expert guidance on cathodic protection (CP) systems for offshore platforms, subsea pipelines, storage tanks, and onshore oil and gas facilities.

## Version Metadata

```yaml
version: 1.0.0
python_min_version: '3.10'
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

### [1.0.0] - 2026-01-07

**Added:**
- Initial version metadata and dependency management
- Semantic versioning support
- Compatibility information for Python 3.10-3.13

**Changed:**
- Enhanced skill documentation structure


## When to Use

- CP system design (SACP and ICCP)
- Anode calculation and spacing
- Transformer rectifier unit sizing
- Pipeline CP design
- Coating breakdown assessment
- AC/DC interference analysis
- CP monitoring system design
- NACE/ISO/DNV compliance

## Domain Expertise

### Cathodic Protection Systems

| System Type | Applications |
|-------------|--------------|
| **SACP** (Sacrificial Anode) | Offshore structures, pipelines, short-term protection |
| **ICCP** (Impressed Current) | Long pipelines, complex structures, retrofit |
| **Hybrid** | Combined systems for optimal protection |

### Anode Materials

| Material | Application | Environment |
|----------|-------------|-------------|
| Al-Zn-In | Marine, seawater | Offshore, subsea |
| Magnesium | Soil, freshwater | Onshore pipelines |
| MMO (Mixed Metal Oxide) | ICCP anodes | All environments |
| Graphite | Deep well anodes | Soil, groundbeds |
| High-silicon iron | Groundbeds | Soil |

### Industry Standards

| Standard | Scope |
|----------|-------|
| **NACE SP0169** | External corrosion control of pipelines |
| **NACE SP0177** | Mitigation of AC and lightning effects |
| **NACE SP0286** | Electrical isolation of CP systems |
| **NACE RP0176** | Corrosion control of steel fixed offshore platforms |
| **ISO 15589-1** | Pipelines - Onshore |
| **ISO 15589-2** | Pipelines - Offshore |
| **DNV-RP-B401** | Cathodic protection design |
| **API RP 651** | Cathodic protection of aboveground tanks |
| **API RP 1632** | Cathodic protection of underground tanks |

## CP Design Calculations

### Anode Mass Calculation

```python
from digitalmodel.modules.cp import AnodeDesign

# Initialize anode designer
anode = AnodeDesign()

# Calculate required anode mass
result = anode.calculate_mass(
    structure={
        "surface_area": 5000,  # m2
        "coating_efficiency": 0.95,  # 95% coating
        "bare_area": 250  # m2 (5% of total)
    },
    environment={
        "resistivity": 0.25,  # ohm-m (seawater)
        "temperature": 15,  # Celsius
        "water_depth": 100  # m
    },
    design={
        "current_density": 0.03,  # A/m2 (mean)
        "design_life": 25,  # years
        "utilization_factor": 0.85,
        "anode_material": "Al-Zn-In"
    }
)

print(f"Total current required: {result['current_required']:.2f} A")
print(f"Total anode mass: {result['mass_required']:.0f} kg")
print(f"Number of anodes: {result['anode_count']}")
print(f"Anode spacing: {result['spacing']:.1f} m")
```

### Pipeline Attenuation

```python
from digitalmodel.modules.cp import PipelineCP

# Initialize pipeline CP designer
pipeline = PipelineCP()

# Calculate attenuation and CP spread
result = pipeline.calculate_attenuation(
    pipeline={
        "length": 50000,  # m (50 km)
        "diameter": 0.914,  # m (36 inch)
        "wall_thickness": 0.0254,  # m (1 inch)
        "coating_type": "FBE",
        "coating_resistance": 10000  # ohm-m2
    },
    soil={
        "resistivity": 50,  # ohm-m
        "type": "clay"
    },
    cp_stations={
        "type": "ICCP",
        "voltage": -1.1,  # V vs Cu/CuSO4
        "locations": [0, 25000, 50000]  # m
    }
)

print(f"Attenuation constant: {result['attenuation_constant']:.6f} 1/m")
print(f"Effective CP spread: {result['effective_spread']:.0f} m")
print(f"Minimum potential: {result['min_potential']:.3f} V")
print(f"Protection criteria met: {result['criteria_met']}")
```

### Coating Breakdown Factor

```python
from digitalmodel.modules.cp import CoatingAnalysis

coating = CoatingAnalysis()

# Calculate coating breakdown factor
cbf = coating.calculate_breakdown_factor(
    coating_type="3LPE",
    initial_quality=0.99,  # 99% initial efficiency
    design_life=25,  # years
    temperature=65,  # Celsius (operating)
    method="DNV-RP-F103"  # or ISO 15589
)

print(f"Initial CBF: {cbf['initial']:.4f}")
print(f"Mean CBF: {cbf['mean']:.4f}")
print(f"Final CBF: {cbf['final']:.4f}")
print(f"Bare area at design life: {cbf['bare_area_percentage']:.1f}%")
```

## ICCP System Design

### Transformer Rectifier Sizing

```python
from digitalmodel.modules.cp import ICCPDesign

iccp = ICCPDesign()

# Size transformer rectifier unit
tru = iccp.size_tru(
    current_requirement={
        "initial": 50,  # A
        "mean": 75,  # A
        "final": 100  # A
    },
    anode_string={
        "resistance": 0.5,  # ohm
        "count": 10,
        "type": "MMO"
    },
    cable={
        "length": 500,  # m
        "type": "XLPE",
        "size": 25  # mm2
    },
    safety_factor=1.25
)

print(f"TRU Rating: {tru['power_rating']:.1f} kW")
print(f"Output Voltage: {tru['voltage']:.1f} V DC")
print(f"Output Current: {tru['current']:.1f} A")
print(f"Efficiency: {tru['efficiency']:.1f}%")
```

### Deep Well Anode Design

```python
# Design deep well anode groundbed
groundbed = iccp.design_groundbed(
    type="deep_well",
    soil_resistivity=100,  # ohm-m
    current_output=50,  # A
    design_life=30,  # years
    anode_material="graphite"
)

print(f"Well depth: {groundbed['depth']:.1f} m")
print(f"Anode count: {groundbed['anode_count']}")
print(f"Anode length: {groundbed['anode_length']:.1f} m")
print(f"Groundbed resistance: {groundbed['resistance']:.3f} ohm")
```

## Monitoring and Assessment

### Remote Monitoring System

```python
from digitalmodel.modules.cp import CPMonitoring

monitoring = CPMonitoring()

# Design monitoring system
system = monitoring.design_system(
    structure_type="offshore_platform",
    monitoring_points=25,
    parameters=[
        "potential",
        "current",
        "temperature",
        "reference_electrode_check"
    ],
    communication="satellite",
    data_interval=3600  # seconds
)

print(f"Monitoring units: {system['unit_count']}")
print(f"Reference electrodes: {system['reference_electrodes']}")
print(f"Communication: {system['communication_type']}")
```

### Survey Analysis

```python
from digitalmodel.modules.cp import SurveyAnalysis

survey = SurveyAnalysis()

# Analyze CIPS/CIS survey data
analysis = survey.analyze_cips(
    data_file="pipeline_survey.csv",
    criteria={
        "on_potential": -0.85,  # V vs Cu/CuSO4
        "off_potential": -0.85,
        "100mV_shift": True
    }
)

print(f"Protected length: {analysis['protected_percentage']:.1f}%")
print(f"Under-protected sections: {len(analysis['under_protected'])}")
print(f"Coating defects detected: {len(analysis['coating_defects'])}")

# Analyze DCVG survey
dcvg = survey.analyze_dcvg(
    data_file="dcvg_survey.csv"
)

for defect in dcvg['defects']:
    print(f"Defect at {defect['chainage']}m: {defect['severity']} ({defect['ir_drop']}mV)")
```

## Interference Analysis

### AC Interference

```python
from digitalmodel.modules.cp import InterferenceAnalysis

interference = InterferenceAnalysis()

# Analyze AC interference from power line
ac_analysis = interference.analyze_ac(
    pipeline={
        "length": 10000,  # m parallel exposure
        "coating_resistance": 10000,  # ohm-m2
        "diameter": 0.6  # m
    },
    power_line={
        "voltage": 400000,  # V
        "current": 500,  # A
        "separation": 50  # m
    },
    soil_resistivity=100  # ohm-m
)

print(f"Induced AC voltage: {ac_analysis['voltage']:.1f} V")
print(f"AC current density: {ac_analysis['current_density']:.2f} A/m2")
print(f"Mitigation required: {ac_analysis['mitigation_required']}")
```

### Stray Current

```python
# Analyze DC stray current
dc_analysis = interference.analyze_stray_current(
    pipeline={
        "coating_resistance": 10000,  # ohm-m2
        "length": 5000  # m affected
    },
    source={
        "type": "railway",
        "current": 1000,  # A
        "distance": 100  # m
    }
)

print(f"Stray current pickup: {dc_analysis['pickup_current']:.2f} A")
print(f"Discharge current density: {dc_analysis['discharge_density']:.4f} A/m2")
print(f"Corrosion rate: {dc_analysis['corrosion_rate']:.2f} mm/year")
```

## MCP Tool Integration

### Swarm Coordination
```javascript
// Initialize CP design swarm
mcp__claude-flow__swarm_init { topology: "hierarchical", maxAgents: 4 }

// Spawn specialized agents
mcp__claude-flow__agent_spawn { type: "analyst", name: "cp-calculator" }
mcp__claude-flow__agent_spawn { type: "reviewer", name: "standards-checker" }
```

### Memory Coordination
```javascript
// Store CP design parameters
mcp__claude-flow__memory_usage {
  action: "store",
  key: "cp/design/parameters",
  namespace: "corrosion",
  value: JSON.stringify({
    structure: "offshore_platform",
    system: "SACP",
    design_life: 25,
    standards: ["DNV-RP-B401", "NACE SP0176"]
  })
}
```

## Design Workflow

### CP System Design Process

1. **Environment Assessment**
   - Soil/water resistivity
   - Temperature
   - Oxygen content
   - Biological activity

2. **Current Requirement**
   - Surface area calculation
   - Coating efficiency
   - Current density selection

3. **System Selection**
   - SACP vs ICCP decision
   - Hybrid considerations

4. **Component Design**
   - Anode sizing and distribution
   - Cable sizing
   - TRU specification (ICCP)

5. **Interference Analysis**
   - AC/DC interference
   - Stray current
   - Galvanic interaction

6. **Monitoring Design**
   - Reference electrode placement
   - Test point locations
   - Remote monitoring

## Best Practices

1. **Conservatism**: Apply appropriate safety factors
2. **Standards Compliance**: Follow NACE/ISO requirements
3. **Design Life**: Consider coating degradation over time
4. **Monitoring**: Design for long-term performance tracking
5. **Documentation**: Record all assumptions and calculations

## Related Skills

- [structural-analysis](../structural-analysis/SKILL.md) - Structural integrity
- [mooring-design](../mooring-design/SKILL.md) - Mooring system protection
- [fatigue-analysis](../fatigue-analysis/SKILL.md) - Corrosion-fatigue interaction

## References

- NACE International Standards
- ISO 15589-1/2: Cathodic Protection of Pipelines
- DNV-RP-B401: Cathodic Protection Design
- API RP 651/1632: Tank Cathodic Protection
- Agent Source: `agents/cathodic-protection-engineer.md`

---

## Version History

- **1.0.0** (2025-01-02): Initial release from agents/cathodic-protection-engineer.md
