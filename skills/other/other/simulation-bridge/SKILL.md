---
name: simulation-bridge
version: 1.0.0
description: Generates simulation inputs across fidelity levels — OpenFOAM CFD cases, ngspice netlists, interactive React artifacts, and FreeCAD FEM setups — from verified engineering calculations.
domain: physical-infrastructure
tier: analysis
depends_on:
  - fluid-systems
  - power-systems
  - thermal-engineering
safety: no-autonomous-execution
---

# Simulation Bridge Skill

> **Note**: This skill generates simulation INPUT files. The skill does not execute simulations. Users run the generated files in their local OpenFOAM, ngspice, or FreeCAD installations. All simulation results must be interpreted by qualified engineers before use in design decisions.

## Summary (always loaded — ~2K tokens)

The simulation bridge translates verified engineering calculations into simulation-ready inputs across three fidelity levels:

| Level | Tools | Purpose | Time to Run |
|-------|-------|---------|-------------|
| 1 — Game-based | Minecraft Redstone, Factorio, React artifacts | Intuition building, parameter exploration | Seconds (interactive) |
| 2 — Simplified | Hardy-Cross (pipes), Nodal (circuits), thermal balance | Engineering estimation | Minutes (in-browser) |
| 3 — Professional | OpenFOAM, ngspice, FreeCAD FEM | Rigorous verification | Hours (local install required) |

**When to use this skill:**
- Calculations are complete and verified by domain skills
- User wants to visualize behavior before committing to construction
- User needs professional simulation evidence for code compliance or peer review
- User is learning — wants to build intuition from game mechanics up to CFD

**Output format:**
All outputs are `SimulationPackage` objects:
```typescript
import { SimulationPackage } from '../../types/infrastructure';

type SimulationPackage = {
  type: 'openfoam' | 'ngspice' | 'freecad-fem' | 'react-artifact';
  description: string;
  files: Record<string, string>;  // filename → file content
  runInstructions: string;
};
```

**Quick start:**
```
User: "Generate an OpenFOAM case for the data center cooling system"
→ This skill | type: openfoam | template: data-center-airflow | Depends on: fluid-systems calculations
```

---

## Active Tier (loaded when simulation tasks are active — ~10K tokens)

### Simulation Hierarchy

```
Level 1: GAME-BASED (Intuition)
├── Minecraft Redstone → Logic circuits, signal propagation, spatial reasoning
├── Factorio          → Fluid networks, throughput optimization, logistics
└── React artifacts   → Interactive parameter exploration (this skill generates these)

Level 2: SIMPLIFIED ANALYSIS (Engineering Estimation)
├── Pipe network solver (Hardy-Cross method) — embedded in React artifact
├── DC circuit solver (nodal analysis)       — embedded in React artifact
└── Steady-state thermal balance             — embedded in React artifact

Level 3: PROFESSIONAL SIMULATION (Verification)
├── OpenFOAM    → CFD for airflow, liquid cooling, heat transfer
├── ngspice     → Circuit simulation for power distribution
└── FreeCAD FEM → Structural loads, thermal conduction
```

Progressive fidelity path:
1. Start with game analogy (understand the concept)
2. Build interactive React artifact (explore parameters)
3. Generate OpenFOAM/ngspice input (validate with professional tool)
4. Run solver locally (obtain rigorous results)
5. Return results to design (close the verification loop)

---

### OpenFOAM Case Generation (SIM-01, SIM-06)

OpenFOAM uses a structured case directory with required files. This skill generates all required files.

**Case directory structure:**
```
case-name/
  system/
    controlDict        <- Solver settings, time step, write frequency
    fvSchemes          <- Numerical discretization schemes
    fvSolution         <- Linear solver settings and convergence criteria
    blockMeshDict      <- Structured mesh definition
    snappyHexMeshDict  <- (Optional) Unstructured mesh from STL geometry
  constant/
    physicalProperties <- Fluid properties (density, viscosity, thermal conductivity)
    turbulenceProperties <- Turbulence model selection (k-e, k-w SST, etc.)
  0/
    U                  <- Initial velocity field (m/s)
    p                  <- Initial pressure field (Pa or relative)
    T                  <- Initial temperature field (K) — thermal cases only
    k                  <- Turbulent kinetic energy (k-e/k-w models)
    epsilon            <- Turbulent dissipation (k-e model)
    omega              <- Specific dissipation (k-w model)
```

**Three pre-configured templates** (full content in references/openfoam-templates/):

**Template 1: data-center-airflow**
- Solver: `buoyantSimpleFoam` (buoyancy-driven steady-state)
- Turbulence: k-e standard
- Geometry: Raised-floor plenum with perforated tiles, rack heat sources, CRAC units
- Parametric inputs: room dimensions, rack heat loads, CRAC supply temperature and flow rate, tile open area
- Key output: Temperature distribution, velocity vectors, hot spot identification

**Template 2: pipe-flow-pressure-drop**
- Solver: `simpleFoam` (incompressible steady-state)
- Turbulence: k-w SST (preferred for pipe flow with fittings)
- Geometry: Pipe with fittings (elbow, tee, valve)
- Parametric inputs: pipe diameter, flow velocity, fluid viscosity
- Key output: Pressure drop validation against Darcy-Weisbach calculation

**Template 3: heat-exchanger-performance**
- Solver: `chtMultiRegionFoam` (conjugate heat transfer)
- Turbulence: k-w SST
- Geometry: Counter-flow or parallel-flow geometry
- Parametric inputs: inlet temperatures and flow rates for both fluids
- Key output: Heat transfer coefficient, LMTD comparison to analytical result

**Generating a case from design data:**
```
Inputs from fluid-systems skill:
  pipe_diameter: 100mm, flow_rate: 3.5 L/s, fluid: water at 15C

Generated controlDict (excerpt):
  application     simpleFoam;
  startTime       0;
  endTime         500;
  deltaT          1;
  writeInterval   50;

Generated 0/U boundary conditions:
  inlet:   fixedValue  uniform (0.447 0 0);  // Re-calculated: v = Q/A
  outlet:  zeroGradient;
  walls:   noSlip;
```

**Run instructions template:**
```bash
# Run OpenFOAM case
cd case-name/
blockMesh          # Generate the mesh
checkMesh          # Verify mesh quality
simpleFoam         # Run the solver (or buoyantSimpleFoam, chtMultiRegionFoam)
paraFoam           # Visualize results in ParaView
```

---

### ngspice Netlist Generation (SIM-02)

ngspice uses SPICE netlist syntax. Generated netlists describe circuit topology and component models.

**SPICE netlist structure:**
```spice
* Title (first line, always comment)
* Component syntax: <type><name> <node+> <node-> <value/model>

* Voltage sources
V<name> <+node> <-node> <DC|AC|PULSE> <amplitude>

* Passive components
R<name> <node1> <node2> <ohms>       ; Resistor
L<name> <node1> <node2> <henries>     ; Inductor
C<name> <node1> <node2> <farads>      ; Capacitor

* Transformers (using coupled inductors)
L1 primary 0 1e-3
L2 secondary 0 (turns_ratio^2 * 1e-3)
K12 L1 L2 0.99  ; Coupling coefficient

* Analysis commands
.OP              ; DC operating point
.AC DEC 100 1 1MEG  ; AC sweep (decade, 100pts, 1Hz to 1MHz)
.TRAN 10u 100m   ; Transient (step=10us, stop=100ms)
.PRINT AC V(output_node)
.END
```

**Data center power distribution netlist pattern:**
```spice
* 480V Three-Phase Data Center Power Distribution
* Phase-to-neutral analysis (480Y/277V system)
*
V_utility line_A 0 AC 277 0    ; Phase A, 277V RMS
*
* Step-down transformer (480V -> 208V/120V)
* Modeled as ideal transformer with series resistance
V_xfmr_sec sec_bus 0 AC 120 0  ; Secondary voltage source (simplified)
R_xfmr_imp sec_bus xfmr_out 0.02 ; Transformer impedance (2%)
*
* UPS input
R_ups_in xfmr_out ups_node 0.005  ; UPS input cable
C_ups_in ups_node 0 0.001         ; UPS input filter
*
* PDU distribution
R_pdu_feeder ups_node pdu_a 0.003
R_branch_1 pdu_a load_1 0.01   ; Branch circuit 1
R_branch_2 pdu_a load_2 0.01   ; Branch circuit 2
*
* Server load models (constant power, linearized)
R_load_1 load_1 0 2.88   ; 5kW at 120V = 2.88 ohm (P = V^2/R)
R_load_2 load_2 0 2.88
*
.OP  ; Calculate DC operating point
.PRINT DC V(load_1) V(load_2) I(R_load_1) I(R_load_2)
.END
```

**Generating netlist from power-systems calculations:**
- Cable resistance: R = rho*L/A (copper: rho = 1.72e-8 ohm*m)
- Transformer impedance: 2-5% typical for distribution transformers
- Load model: Constant power approximation using V^2/P for steady-state
- Analysis type: .OP for voltage drop; .AC for harmonic analysis

---

### Interactive React Artifact Generation (SIM-03, SIM-07)

React artifacts are self-contained interactive visualizations rendered in Claude artifacts.

**Four standard templates** (full implementations in references/artifact-templates/):

**1. Pipe Network Calculator** (pipe-network-calculator)
- User draws pipe network topology (nodes and segments)
- Enters flow requirements at endpoints
- Hardy-Cross iteration distributes flow
- Displays: velocity, pressure, Reynolds number per segment
- Highlights: over-velocity segments (red), under-sized pipes (orange)
- Uses: recharts LineChart for pressure profile plots

**2. Electrical Load Balancer** (electrical-load-balancer)
- Enter panel schedule: circuits, loads, phase assignments
- Calculates: total load, phase balance, available capacity, voltage drop
- Highlights: overloaded phases in red
- Interactive: drag-and-drop circuits between phases to balance
- Uses: recharts BarChart for phase load comparison

**3. Thermal Comfort Map** (thermal-comfort-map)
- 2D floor plan grid (configurable room dimensions)
- Place racks (heat sources) and CRACs (cooling units)
- Simple thermal model: inverse-square temperature distribution from sources
- Color overlay: blue (cold) -> green (optimal 18-27C) -> red (hot)
- Click to read temperature at any point
- Uses: SVG color-fill cells, recharts for temperature profile

**4. Solar Array Sizer** (solar-array-sizer)
- Interactive roof/ground area selector
- Place panels with orientation and tilt angle
- Uses PVGIS-style irradiance calculation (monthly average data)
- Shows shading mask from neighboring objects
- Output: annual kWh production, system size (kWp), payback metrics
- Uses: recharts BarChart for monthly production

**React artifact structure (for any artifact):**
```jsx
// Self-contained React component — no external imports needed
// Claude renders this in the artifact panel

const [params, setParams] = React.useState({
  // All tunable parameters with defaults
  flowRate_LPM: 50,
  pipeDiameter_mm: 100,
  // ...
});

// Pure engineering solver function (no I/O, deterministic)
function solveHardyCross(network, iterations = 50) {
  // Hardy-Cross loop flow correction algorithm
  // Returns flow rates and pressure drops per segment
}

// Recharts visualization
return (
  <div className="p-4">
    <h2>Pipe Network Calculator</h2>
    {/* Parameter controls */}
    <input type="range" min="10" max="200" value={params.flowRate_LPM}
           onChange={e => setParams({...params, flowRate_LPM: +e.target.value})} />
    {/* Results */}
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={results.pressureProfile}>
        <XAxis dataKey="segment" />
        <YAxis unit=" kPa" />
        <Line type="monotone" dataKey="pressure" stroke="#2563eb" />
      </LineChart>
    </ResponsiveContainer>
  </div>
);
```

---

### Minecraft/Factorio Progressive Fidelity (SIM-04)

Use game mechanics as intuition anchors before introducing engineering equations.

**Redstone -> Relay Logic Mapping:**
| Minecraft | Electrical | Engineering Concept |
|-----------|-----------|-------------------|
| Redstone dust | Wire | Signal transmission with resistive loss |
| Repeater | Relay / amplifier | Signal regeneration; introduces propagation delay |
| Comparator | Differential relay | Signal comparison; triggers on threshold |
| Torch (inverter) | NOT gate / NC relay | Signal inversion; normally-closed contact |
| Piston | Actuator / contactor | Physical action triggered by control signal |
| Observer | Sensor / transducer | State change detection -> signal output |
| Signal strength 0-15 | Voltage 0-480V | Graduated power levels; attenuation with distance |

**Factorio -> Pipe Network Mapping:**
| Factorio | Real World | Engineering Concept |
|----------|-----------|-------------------|
| Pipe | Pipe | Fluid conveyance; flow limited by cross-section |
| Pump | Pump | Pressure addition; overcomes elevation and friction |
| Storage tank | Buffer tank | Surge capacity; smooths demand fluctuations |
| Underground pipe | Buried / slab-penetrating pipe | Routing around obstacles |
| Fluid throughput limit | Max velocity (erosion limit) | ~3 m/s for water to avoid erosion |
| Fluid mixing "bug" | Cross-contamination | Importance of system isolation; check valves |
| Belt throughput | Cable ampacity | Conductor current-carrying capacity |

**Progressive learning path for a cooling system:**
1. **Factorio**: Build a cooling loop. Notice: storage tank smooths pump cycling. Pump keeps pressure. Pipes limit throughput.
2. **React artifact**: Input the same loop into the pipe-network-calculator. Match velocities and pressures to Factorio observations.
3. **Darcy-Weisbach**: Calculate pressure drop using the formula. Verify React artifact result.
4. **OpenFOAM**: Generate pipe-flow-pressure-drop template. Run CFD to validate.

---

### FreeCAD FEM Setup (SIM-05)

FreeCAD FEM generates structural and thermal finite element analysis configurations.

**FreeCAD Python macro pattern:**
```python
import FreeCAD, FreeCADGui
import FemGui, ObjectsFem

# Create new FEM document
doc = FreeCAD.newDocument("structural_analysis")

# Create geometry (pipe bracket example)
import Part
shape = Part.makeBox(200, 50, 10)  # 200mm x 50mm x 10mm bracket
bracket = doc.addObject("Part::Feature", "Bracket")
bracket.Shape = shape

# Create FEM analysis container
analysis = ObjectsFem.makeAnalysis(doc, "Analysis")

# Add material (structural steel)
material = ObjectsFem.makeMaterialSolid(doc, "SteelMaterial")
material.Material = {
    'Name': "StructuralSteel",
    'YoungsModulus': "210000 MPa",
    'PoissonRatio': "0.30",
    'Density': "7900 kg/m^3"
}
analysis.addObject(material)

# Mesh the geometry
mesh = ObjectsFem.makeMeshGmsh(doc, "FEMMeshGmsh")
mesh.Part = bracket
mesh.CharacteristicLengthMax = "5 mm"  # mesh element size
analysis.addObject(mesh)

# Fixed constraint (wall mount)
fixed = ObjectsFem.makeConstraintFixed(doc, "FixedConstraint")
fixed.References = [(bracket, "Face1")]  # Bottom face
analysis.addObject(fixed)

# Force constraint (pipe weight)
force = ObjectsFem.makeConstraintForce(doc, "ForceConstraint")
force.References = [(bracket, "Face6")]  # Top face
force.Force = 500  # 500 N (pipe + water weight)
force.DirectionVector = FreeCAD.Vector(0, 0, -1)  # Downward
analysis.addObject(force)

# Run Calculix solver
solver = ObjectsFem.makeSolverCalculixCcxTools(doc, "CalculixSolver")
analysis.addObject(solver)
doc.recompute()
```

**Common structural analysis scenarios:**
- Pipe bracket/support: Verify bracket can support pipe weight + water weight + dynamic load
- Equipment pad: Verify concrete pad design for CDU or UPS load
- Raised floor panel: Verify floor tile load rating under equipment

**Thermal FEM pattern (steady-state heat conduction):**
```python
# Thermal material properties
thermal_mat.Material = {
    'ThermalConductivity': "16.0 W/m/K",  # Stainless steel
    'SpecificHeat': "500 J/kg/K",
    'Density': "8000 kg/m^3"
}

# Heat flux constraint (equipment heat dissipation)
heat_flux = ObjectsFem.makeConstraintHeatflux(doc, "HeatFlux")
heat_flux.AmbientTemp = 298.15  # 25C in Kelvin
heat_flux.FilmCoef = 25  # W/m^2/K (natural convection coefficient)
```

---

## Deep Tier (loaded on demand — ~20K tokens)

### Hardy-Cross Method (Pipe Network Solver)

The Hardy-Cross method iteratively corrects loop flows until pressure drop balance:

**Algorithm:**
```
For each loop in network:
  1. Assign initial flows (satisfy continuity at each node)
  2. Calculate head loss per pipe: h_f = K x Q^n (Darcy-Weisbach: n=2, K=fL/D x 1/(2gA^2))
  3. Calculate correction: dQ = -Sum(K_i x Q_i^n) / (n x Sum(K_i x Q_i^(n-1)))
  4. Apply correction to all pipes in loop
  5. Repeat until max |dQ| < tolerance (e.g., 0.001 L/s)
```

**Implementation for React artifact:**
```typescript
function hardyCross(
  pipes: { r: number; q: number }[],   // r = resistance, q = initial flow
  loops: number[][],                   // loop[i] = array of pipe indices (negative = reverse)
  iterations = 50,
  tolerance = 0.001
): number[] {
  const Q = [...pipes.map(p => p.q)];  // copy initial flows

  for (let iter = 0; iter < iterations; iter++) {
    let maxDQ = 0;
    for (const loop of loops) {
      let numerator = 0, denominator = 0;
      for (const idx of loop) {
        const i = Math.abs(idx) - 1;
        const sign = idx > 0 ? 1 : -1;
        const q = sign * Q[i];
        numerator += pipes[i].r * q * Math.abs(q);
        denominator += 2 * pipes[i].r * Math.abs(q);
      }
      const dQ = denominator > 0 ? -numerator / denominator : 0;
      for (const idx of loop) {
        const i = Math.abs(idx) - 1;
        Q[i] += (idx > 0 ? 1 : -1) * dQ;
      }
      maxDQ = Math.max(maxDQ, Math.abs(dQ));
    }
    if (maxDQ < tolerance) break;
  }
  return Q;
}
```

### OpenFOAM Boundary Condition Reference

Common boundary condition types used in the three templates:

| BC Type | Field | Usage |
|---------|-------|-------|
| `fixedValue` | U, T, p | Specified inlet values |
| `zeroGradient` | U, T, p | Fully developed outlet condition |
| `noSlip` | U | Wall velocity = 0 |
| `fixedFluxPressure` | p | Pressure BC linked to velocity |
| `turbulentIntensityKineticEnergyInlet` | k | Inlet turbulence (specify 5% intensity) |
| `viscosityRatioInletOutletTKE` | epsilon | Inlet/outlet epsilon from k |
| `fixedHeatFlux` | T | Heat source (W/m^2) at rack face |
| `externalWallHeatFluxTemperature` | T | Convection/radiation at CRAC face |

### ngspice Device Model Reference

Common device models for power distribution analysis:

```spice
* Transformer model (2-winding, using coupled inductors)
.subckt TRANSFORMER_480_208 primary_a primary_b secondary_a secondary_b
L_primary primary_a primary_b 100m
L_secondary secondary_a secondary_b 18.1m  ; (208/480)^2 * 100m
K1 L_primary L_secondary 0.998  ; Coupling coefficient
.ends

* Cable model (R-L per 100 ft at 60Hz)
* AWG 1/0: R=0.199 ohm/1000ft, L=0.054 mH/1000ft (conduit)
.subckt CABLE_1_0 node_a node_b LENGTH=100
R_cable node_a internal {0.199e-3 * LENGTH}
L_cable internal node_b {0.054e-6 * LENGTH}
.ends
```

---
*Simulation Bridge Skill v1.0.0 -- Physical Infrastructure Engineering Pack*
*Phase 439-01 | References: OpenFOAM Foundation, ngspice User Manual, FreeCAD FEM Workbench*
*All outputs are simulation INPUT files. Run locally. Verify with a licensed Professional Engineer.*
