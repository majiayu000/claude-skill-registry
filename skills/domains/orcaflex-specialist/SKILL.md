# OrcaFlex Specialist Skill

```yaml
name: orcaflex-specialist
version: 1.0.0
category: sme
tags: [orcaflex, offshore, simulation, python-api, automation, marine-dynamics, mooring, riser]
created: 2026-01-06
updated: 2026-01-06
author: Claude
description: |
  Expert OrcaFlex workflows, Python API automation, model validation, and best
  practices for offshore marine simulations. Covers mooring analysis, riser
  dynamics, installation simulations, and advanced post-processing.
```

## When to Use This Skill

Use this skill when you need to:
- Automate OrcaFlex model creation and analysis
- Build parametric OrcaFlex models via Python API
- Perform batch simulations with varying parameters
- Extract and process time series results
- Validate OrcaFlex models against design criteria
- Integrate OrcaFlex with external tools and workflows
- Optimize mooring and riser configurations
- Conduct sensitivity studies and Monte Carlo simulations

## Core Knowledge Areas

### 1. OrcaFlex Python API Basics

Connecting to OrcaFlex and basic model operations:

```python
import OrcFxAPI
import numpy as np
from pathlib import Path
from typing import List, Dict, Optional

def create_new_model(
    general_data: dict,
    save_path: Path = None
) -> OrcFxAPI.Model:
    """
    Create a new OrcaFlex model with general settings.

    Args:
        general_data: Dictionary with general data parameters
        save_path: Optional path to save the model

    Returns:
        OrcaFlex model object

    Example:
        >>> general_data = {
        ...     'ImplicitUseVariableTimeStep': 'Yes',
        ...     'TargetLogSampleInterval': 0.1,
        ...     'InnerTimeStep': 0.01,
        ...     'StageCount': 2,
        ...     'StageDuration': [100, 3600]
        ... }
        >>> model = create_new_model(general_data)
    """
    # Create new model
    model = OrcFxAPI.Model()

    # Set general data
    general = model.general

    for key, value in general_data.items():
        setattr(general, key, value)

    # Save if path provided
    if save_path:
        model.SaveData(str(save_path))

    return model

def load_model(
    file_path: Path,
    validate: bool = True
) -> OrcFxAPI.Model:
    """
    Load existing OrcaFlex model with optional validation.

    Args:
        file_path: Path to .dat or .sim file
        validate: Whether to validate model after loading

    Returns:
        Loaded OrcaFlex model

    Example:
        >>> model = load_model(Path('mooring_analysis.dat'))
        >>> print(f"Model stages: {model.general.StageCount}")
    """
    model = OrcFxAPI.Model(str(file_path))

    if validate:
        # Run basic validation
        state = model.State()
        if state != OrcFxAPI.ModelState.Reset:
            print(f"Warning: Model state is {state}")

        # Check for invalid objects
        invalid_objects = []
        for obj in model.objects:
            try:
                obj_type = obj.type
            except:
                invalid_objects.append(obj.name)

        if invalid_objects:
            print(f"Warning: Invalid objects found: {invalid_objects}")

    return model

def run_static_analysis(
    model: OrcFxAPI.Model,
    thread_count: int = None
) -> None:
    """
    Run static analysis (statics to whole simulation).

    Args:
        model: OrcaFlex model
        thread_count: Number of threads (None = auto)

    Example:
        >>> model = load_model('mooring.dat')
        >>> run_static_analysis(model, thread_count=4)
        >>> print("Static analysis complete")
    """
    # Configure calculation
    if thread_count:
        model.general.ThreadCount = thread_count

    # Run statics to whole simulation
    model.CalculateStatics()
    model.RunSimulation()

    print(f"Simulation complete. State: {model.State()}")

def run_dynamic_analysis(
    model: OrcFxAPI.Model,
    save_sim: bool = True,
    sim_path: Path = None
) -> Path:
    """
    Run dynamic analysis and save results.

    Args:
        model: OrcaFlex model
        save_sim: Whether to save simulation results
        sim_path: Path to save .sim file

    Returns:
        Path to saved simulation file

    Example:
        >>> model = load_model('mooring.dat')
        >>> sim_file = run_dynamic_analysis(model, sim_path=Path('results.sim'))
        >>> print(f"Results saved: {sim_file}")
    """
    # Run simulation
    model.RunSimulation()

    # Save results
    if save_sim:
        if sim_path is None:
            # Generate default path
            sim_path = Path(model.DataFileName()).with_suffix('.sim')

        model.SaveSimulation(str(sim_path))
        return sim_path

    return None
```

### 2. Building Models Programmatically

Create complex models via Python API:

```python
def create_vessel_model(
    vessel_params: dict,
    mooring_config: dict,
    environment: dict
) -> OrcFxAPI.Model:
    """
    Create complete vessel model with moorings and environment.

    Args:
        vessel_params: Vessel properties
        mooring_config: Mooring line configuration
        environment: Environmental conditions

    Returns:
        Complete OrcaFlex model

    Example:
        >>> vessel_params = {
        ...     'name': 'FPSO',
        ...     'mass': 150000,  # tonnes
        ...     'length': 300,  # m
        ...     'draft': 20,
        ...     'draft_fore': 20,
        ...     'draft_aft': 20
        ... }
        >>> mooring_config = {
        ...     'pattern': 'spread',
        ...     'line_count': 8,
        ...     'line_length': 1500,
        ...     'line_type': 'chain_wire_chain'
        ... }
        >>> environment = {
        ...     'water_depth': 1200,
        ...     'current_speed': 1.0,
        ...     'wave_height': 5.0,
        ...     'wave_period': 12.0
        ... }
        >>> model = create_vessel_model(vessel_params, mooring_config, environment)
    """
    # Create new model
    model = OrcFxAPI.Model()

    # Set environment
    env = model.environment

    # Water depth
    env.WaterDepth = environment['water_depth']

    # Current profile
    env.RefCurrentSpeed = environment['current_speed']
    env.CurrentDepths = [0, -environment['water_depth']]
    env.CurrentSpeeds = [environment['current_speed'], 0.5 * environment['current_speed']]

    # Waves (JONSWAP spectrum)
    env.WaveType = 'JONSWAP'
    env.WaveHs = environment['wave_height']
    env.WaveTp = environment['wave_period']
    env.WaveGamma = 3.3

    # Create vessel
    vessel = model.CreateObject(OrcFxAPI.otVessel, vessel_params['name'])

    # Set vessel properties
    vessel.Length = vessel_params['length']
    vessel.Draft = vessel_params['draft']
    vessel.DraftAtRest = vessel_params['draft']
    vessel.Mass = vessel_params['mass']

    # Displacement check
    rho_sw = 1025  # kg/m³
    g = 9.81
    displacement = vessel_params['mass'] * 1000 * g  # N
    print(f"Vessel displacement: {displacement/1e6:.1f} MN")

    # Create mooring lines
    create_mooring_system(
        model=model,
        vessel=vessel,
        config=mooring_config,
        water_depth=environment['water_depth']
    )

    return model

def create_mooring_system(
    model: OrcFxAPI.Model,
    vessel: OrcFxAPI.OrcaFlexObject,
    config: dict,
    water_depth: float
) -> List[OrcFxAPI.OrcaFlexObject]:
    """
    Create mooring system attached to vessel.

    Args:
        model: OrcaFlex model
        vessel: Vessel object
        config: Mooring configuration
        water_depth: Water depth [m]

    Returns:
        List of mooring line objects

    Example:
        >>> config = {
        ...     'pattern': 'spread',
        ...     'line_count': 8,
        ...     'line_length': 1500,
        ...     'fairlead_radius': 40,
        ...     'anchor_radius': 1400,
        ...     'line_sections': [
        ...         {'type': 'R4 Studless Chain', 'length': 300},
        ...         {'type': '76mm Wire', 'length': 900},
        ...         {'type': 'R4 Studless Chain', 'length': 300}
        ...     ]
        ... }
        >>> lines = create_mooring_system(model, vessel, config, 1200)
    """
    lines = []
    line_count = config['line_count']

    # Create line types if needed
    for section in config['line_sections']:
        line_type_name = section['type']
        if not model.objects.Exists(line_type_name, OrcFxAPI.otLineType):
            # Create line type (simplified - actual properties depend on type)
            line_type = model.CreateObject(OrcFxAPI.otLineType, line_type_name)
            # Set properties based on name
            # (In practice, load from database or specify explicitly)

    # Calculate line positions (evenly distributed)
    for i in range(line_count):
        angle = 360.0 / line_count * i

        # Create line
        line_name = f"Mooring_{i+1}"
        line = model.CreateObject(OrcFxAPI.otLine, line_name)

        # End A: Fairlead (on vessel)
        line.EndAConnection = vessel.name
        line.EndAAzimuth = angle
        line.EndAX = config['fairlead_radius'] * np.cos(np.radians(angle))
        line.EndAY = config['fairlead_radius'] * np.sin(np.radians(angle))
        line.EndAZ = -vessel.Draft  # At keel

        # End B: Anchor
        anchor_x = config['anchor_radius'] * np.cos(np.radians(angle))
        anchor_y = config['anchor_radius'] * np.sin(np.radians(angle))
        line.EndBConnection = 'Fixed'
        line.EndBX = anchor_x
        line.EndBY = anchor_y
        line.EndBZ = -water_depth

        # Set line sections
        line.NumberOfSections = len(config['line_sections'])
        for j, section in enumerate(config['line_sections']):
            line.SectionIndex = j + 1
            line.LineType[j] = section['type']
            line.Length[j] = section['length']

        lines.append(line)

    return lines

def add_6d_buoy(
    model: OrcFxAPI.Model,
    line: OrcFxAPI.OrcaFlexObject,
    arc_length: float,
    buoy_params: dict
) -> OrcFxAPI.OrcaFlexObject:
    """
    Add 6D buoy to mooring line.

    Args:
        model: OrcaFlex model
        line: Line object to attach buoy to
        arc_length: Arc length along line for attachment [m]
        buoy_params: Buoy properties

    Returns:
        6D buoy object

    Example:
        >>> buoy_params = {
        ...     'name': 'Subsurface_Buoy',
        ...     'mass': 10,  # tonnes
        ...     'volume': 12,  # m³
        ...     'Cd': 1.2,
        ...     'Ca': 1.0
        ... }
        >>> buoy = add_6d_buoy(model, mooring_line, 600, buoy_params)
    """
    # Create 6D buoy
    buoy = model.CreateObject(OrcFxAPI.ot6DBuoy, buoy_params['name'])

    # Connection to line
    buoy.Connection = line.name
    buoy.ConnectionArcLength = arc_length

    # Properties
    buoy.Mass = buoy_params['mass']
    buoy.Volume = buoy_params['volume']

    # Drag and added mass
    buoy.Cd = buoy_params.get('Cd', 1.0)
    buoy.Ca = buoy_params.get('Ca', 1.0)

    # Initial position (will be calculated during statics)
    buoy.InitialPosition = 'Calculated from line'

    return buoy
```

### 3. Results Extraction and Post-Processing

Extract time series and perform analysis:

```python
def extract_time_series(
    model: OrcFxAPI.Model,
    object_name: str,
    variable_name: str,
    object_extra: OrcFxAPI.OrcaFlexObjectExtra = OrcFxAPI.oeEndA,
    period: OrcFxAPI.SpecifiedPeriod = OrcFxAPI.SpecifiedPeriod(OrcFxAPI.pnWholeSimulation)
) -> tuple:
    """
    Extract time series data from simulation results.

    Args:
        model: OrcaFlex model (with results)
        object_name: Name of object
        variable_name: Variable name (e.g., 'Effective Tension')
        object_extra: Object extra (e.g., oeEndA, oeEndB)
        period: Period specification

    Returns:
        Tuple of (time_array, values_array)

    Example:
        >>> model = OrcFxAPI.Model('results.sim')
        >>> time, tension = extract_time_series(
        ...     model,
        ...     'Mooring_1',
        ...     'Effective Tension',
        ...     OrcFxAPI.oeEndA
        ... )
        >>> print(f"Max tension: {np.max(tension):.1f} kN")
    """
    # Get object
    obj = model[object_name]

    # Extract time series
    time = obj.TimeHistory(
        'Time',
        period=period,
        objectExtra=object_extra
    )

    values = obj.TimeHistory(
        variable_name,
        period=period,
        objectExtra=object_extra
    )

    return np.array(time), np.array(values)

def calculate_statistics(
    time: np.ndarray,
    values: np.ndarray,
    exclude_buildup: float = 100.0
) -> dict:
    """
    Calculate statistical parameters from time series.

    Args:
        time: Time array [s]
        values: Values array
        exclude_buildup: Duration to exclude from start [s]

    Returns:
        Dictionary with statistics

    Example:
        >>> time, tension = extract_time_series(model, 'Mooring_1', 'Effective Tension')
        >>> stats = calculate_statistics(time, tension, exclude_buildup=100)
        >>> print(f"Mean: {stats['mean']:.1f} kN")
        >>> print(f"Std: {stats['std']:.1f} kN")
        >>> print(f"Max: {stats['max']:.1f} kN")
    """
    # Exclude build-up period
    mask = time >= exclude_buildup
    values_trimmed = values[mask]

    if len(values_trimmed) == 0:
        raise ValueError("No data after excluding build-up period")

    stats = {
        'mean': np.mean(values_trimmed),
        'std': np.std(values_trimmed),
        'min': np.min(values_trimmed),
        'max': np.max(values_trimmed),
        'range': np.ptp(values_trimmed),  # Peak-to-peak
        'median': np.median(values_trimmed),
        'p95': np.percentile(values_trimmed, 95),
        'p99': np.percentile(values_trimmed, 99)
    }

    return stats

def extract_range_graph(
    model: OrcFxAPI.Model,
    object_name: str,
    variable_name: str,
    period: OrcFxAPI.SpecifiedPeriod = OrcFxAPI.SpecifiedPeriod(OrcFxAPI.pnWholeSimulation)
) -> tuple:
    """
    Extract range graph data (values along line/riser).

    Args:
        model: OrcaFlex model with results
        object_name: Line/riser name
        variable_name: Variable (e.g., 'Effective Tension', 'Curvature')
        period: Period specification

    Returns:
        Tuple of (arc_length, values)

    Example:
        >>> arc, tension = extract_range_graph(
        ...     model,
        ...     'Riser_1',
        ...     'Effective Tension'
        ... )
        >>> print(f"Tension at TDP: {tension[np.argmin(np.abs(arc-1500))]:.1f} kN")
    """
    obj = model[object_name]

    # Get range graph
    arc_length = obj.RangeGraph(
        'Arc Length',
        period=period
    )

    values = obj.RangeGraph(
        variable_name,
        period=period
    )

    return np.array(arc_length), np.array(values)

def find_touchdown_point(
    model: OrcFxAPI.Model,
    line_name: str
) -> dict:
    """
    Find touchdown point location and tension.

    Args:
        model: OrcaFlex model with results
        line_name: Line/riser name

    Returns:
        Dictionary with TDP info

    Example:
        >>> tdp_info = find_touchdown_point(model, 'Riser_1')
        >>> print(f"TDP arc length: {tdp_info['arc_length']:.1f} m")
        >>> print(f"TDP tension: {tdp_info['tension']:.1f} kN")
    """
    line = model[line_name]

    # Get clearance along line
    period = OrcFxAPI.SpecifiedPeriod(OrcFxAPI.pnWholeSimulation)
    arc, clearance = extract_range_graph(model, line_name, 'Clearance', period)

    # Find where clearance crosses zero
    # TDP is where clearance = 0
    tdp_idx = np.argmin(np.abs(clearance))

    # Get tension and curvature at TDP
    arc_tdp, tension = extract_range_graph(model, line_name, 'Effective Tension', period)
    arc_curv, curvature = extract_range_graph(model, line_name, 'Curvature', period)

    return {
        'arc_length': arc[tdp_idx],
        'clearance': clearance[tdp_idx],
        'tension': tension[tdp_idx],
        'curvature': curvature[tdp_idx]
    }
```

### 4. Batch Simulation and Parametric Studies

Automate multiple simulation runs:

```python
def batch_simulation(
    base_model_path: Path,
    parameter_sets: List[dict],
    output_dir: Path,
    parallel: bool = False
) -> List[dict]:
    """
    Run batch simulations with varying parameters.

    Args:
        base_model_path: Path to base model .dat file
        parameter_sets: List of parameter dictionaries
        output_dir: Directory to save results
        parallel: Whether to run in parallel (not implemented - OrcaFlex limitation)

    Returns:
        List of results dictionaries

    Example:
        >>> parameter_sets = [
        ...     {'Hs': 5.0, 'Tp': 10.0, 'current': 1.0},
        ...     {'Hs': 7.5, 'Tp': 12.0, 'current': 1.5},
        ...     {'Hs': 10.0, 'Tp': 14.0, 'current': 2.0}
        ... ]
        >>> results = batch_simulation(
        ...     base_model_path=Path('base_model.dat'),
        ...     parameter_sets=parameter_sets,
        ...     output_dir=Path('batch_results')
        ... )
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    results = []

    for i, params in enumerate(parameter_sets):
        print(f"Running simulation {i+1}/{len(parameter_sets)}")
        print(f"Parameters: {params}")

        # Load base model
        model = OrcFxAPI.Model(str(base_model_path))

        # Apply parameters
        if 'Hs' in params:
            model.environment.WaveHs = params['Hs']
        if 'Tp' in params:
            model.environment.WaveTp = params['Tp']
        if 'current' in params:
            model.environment.RefCurrentSpeed = params['current']

        # Run simulation
        try:
            model.RunSimulation()

            # Save results
            sim_path = output_dir / f"run_{i+1:03d}.sim"
            model.SaveSimulation(str(sim_path))

            # Extract key results
            result = {
                'run_id': i + 1,
                'parameters': params,
                'sim_file': sim_path,
                'status': 'SUCCESS'
            }

            # Extract mooring tensions (example)
            mooring_results = {}
            for mooring_name in ['Mooring_1', 'Mooring_2', 'Mooring_3']:
                if model.objects.Exists(mooring_name):
                    time, tension = extract_time_series(
                        model,
                        mooring_name,
                        'Effective Tension',
                        OrcFxAPI.oeEndA
                    )
                    stats = calculate_statistics(time, tension)
                    mooring_results[mooring_name] = stats

            result['mooring_tensions'] = mooring_results

        except Exception as e:
            result = {
                'run_id': i + 1,
                'parameters': params,
                'status': 'FAILED',
                'error': str(e)
            }

        results.append(result)

    return results

def parametric_study_mooring_pretension(
    base_model: OrcFxAPI.Model,
    line_name: str,
    pretension_range: np.ndarray,
    output_dir: Path
) -> dict:
    """
    Parametric study varying mooring line pretension.

    Args:
        base_model: Base OrcaFlex model
        line_name: Mooring line name
        pretension_range: Array of pretension values to test [kN]
        output_dir: Output directory

    Returns:
        Dictionary with results for each pretension

    Example:
        >>> model = load_model('mooring.dat')
        >>> pretensions = np.linspace(500, 2000, 10)
        >>> results = parametric_study_mooring_pretension(
        ...     model,
        ...     'Mooring_1',
        ...     pretensions,
        ...     Path('pretension_study')
        ... )
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    results = {}

    for pretension in pretension_range:
        print(f"Testing pretension: {pretension:.1f} kN")

        # Create model copy
        model = OrcFxAPI.Model()
        model.LoadData(base_model.DataFileName())

        # Set pretension
        line = model[line_name]
        line.WinchPayoutControlMode = 'Specified Pretension'
        line.Pretension = pretension

        # Run static analysis
        model.CalculateStatics()

        # Extract static results
        line_after_statics = model[line_name]
        static_tension_a = line_after_statics.StaticResult(
            'Effective Tension',
            objectExtra=OrcFxAPI.oeEndA
        )
        static_tension_b = line_after_statics.StaticResult(
            'Effective Tension',
            objectExtra=OrcFxAPI.oeEndB
        )

        # Run dynamic simulation
        model.RunSimulation()

        # Extract dynamic results
        time, tension_a = extract_time_series(
            model,
            line_name,
            'Effective Tension',
            OrcFxAPI.oeEndA
        )

        stats_a = calculate_statistics(time, tension_a)

        results[pretension] = {
            'static_tension_a': static_tension_a,
            'static_tension_b': static_tension_b,
            'dynamic_stats': stats_a
        }

    return results
```

### 5. Model Validation and QA

Automated model checking:

```python
def validate_model(
    model: OrcFxAPI.Model,
    checks: List[str] = None
) -> dict:
    """
    Comprehensive model validation checks.

    Args:
        model: OrcaFlex model
        checks: List of checks to perform (None = all)

    Returns:
        Dictionary with validation results

    Example:
        >>> model = load_model('mooring.dat')
        >>> validation = validate_model(model)
        >>> if validation['overall_status'] == 'PASS':
        ...     print("Model validation passed")
        >>> else:
        ...     print("Validation issues:", validation['issues'])
    """
    if checks is None:
        checks = [
            'general_data',
            'environment',
            'objects',
            'connections',
            'statics'
        ]

    issues = []
    warnings = []

    # 1. General Data Check
    if 'general_data' in checks:
        general = model.general

        # Check time steps
        if general.InnerTimeStep > general.TargetLogSampleInterval:
            issues.append(
                f"InnerTimeStep ({general.InnerTimeStep}) > "
                f"TargetLogSampleInterval ({general.TargetLogSampleInterval})"
            )

        # Check simulation duration
        if general.StageCount == 0:
            issues.append("No simulation stages defined")

        # Check thread count
        if general.ThreadCount > 16:
            warnings.append(f"High thread count: {general.ThreadCount}")

    # 2. Environment Check
    if 'environment' in checks:
        env = model.environment

        # Check water depth
        if env.WaterDepth <= 0:
            issues.append(f"Invalid water depth: {env.WaterDepth}")

        # Check wave parameters
        if env.WaveType == 'JONSWAP':
            if env.WaveHs <= 0:
                issues.append(f"Invalid wave Hs: {env.WaveHs}")
            if env.WaveTp <= 0:
                issues.append(f"Invalid wave Tp: {env.WaveTp}")

    # 3. Objects Check
    if 'objects' in checks:
        # Check for duplicate names
        object_names = [obj.name for obj in model.objects]
        duplicates = [name for name in object_names if object_names.count(name) > 1]
        if duplicates:
            issues.append(f"Duplicate object names: {set(duplicates)}")

        # Check line types
        for obj in model.objects:
            if obj.type == OrcFxAPI.otLine:
                if obj.NumberOfSections == 0:
                    issues.append(f"Line {obj.name} has no sections")

                # Check line lengths
                for i in range(obj.NumberOfSections):
                    if obj.Length[i] <= 0:
                        issues.append(
                            f"Line {obj.name} section {i+1} has invalid length: "
                            f"{obj.Length[i]}"
                        )

    # 4. Connections Check
    if 'connections' in checks:
        for obj in model.objects:
            if hasattr(obj, 'Connection'):
                connection = obj.Connection
                if connection not in ['Fixed', 'Free'] and connection != '':
                    # Check if connected object exists
                    if not model.objects.Exists(connection):
                        issues.append(
                            f"Object {obj.name} connected to non-existent "
                            f"object: {connection}"
                        )

    # 5. Statics Check
    if 'statics' in checks:
        try:
            model.CalculateStatics()

            # Check for warnings in statics
            # (OrcaFlex API doesn't provide direct access to warnings,
            #  would need to check specific conditions)

        except Exception as e:
            issues.append(f"Statics calculation failed: {str(e)}")

    # Overall status
    overall_status = 'PASS' if len(issues) == 0 else 'FAIL'

    return {
        'overall_status': overall_status,
        'issues': issues,
        'warnings': warnings,
        'checks_performed': checks
    }

def check_mooring_system_integrity(
    model: OrcFxAPI.Model,
    vessel_name: str,
    design_criteria: dict
) -> dict:
    """
    Check mooring system against design criteria.

    Args:
        model: OrcaFlex model (with results)
        vessel_name: Vessel object name
        design_criteria: Dictionary with design limits

    Returns:
        Dictionary with integrity check results

    Example:
        >>> design_criteria = {
        ...     'max_offset': 50,  # m
        ...     'max_tension_uls': 8000,  # kN
        ...     'max_tension_als': 10000,  # kN
        ...     'min_line_clearance': 5  # m
        ... }
        >>> integrity = check_mooring_system_integrity(
        ...     model,
        ...     'FPSO',
        ...     design_criteria
        ... )
    """
    results = {
        'overall_status': 'PASS',
        'checks': {}
    }

    # 1. Vessel offset check
    vessel = model[vessel_name]
    time, x = extract_time_series(model, vessel_name, 'X')
    time, y = extract_time_series(model, vessel_name, 'Y')

    offset = np.sqrt(x**2 + y**2)
    max_offset = np.max(offset)

    results['checks']['vessel_offset'] = {
        'max_offset': max_offset,
        'limit': design_criteria['max_offset'],
        'status': 'PASS' if max_offset <= design_criteria['max_offset'] else 'FAIL'
    }

    # 2. Mooring line tension checks
    mooring_lines = [
        obj for obj in model.objects
        if obj.type == OrcFxAPI.otLine and 'Mooring' in obj.name
    ]

    line_tension_results = {}

    for line in mooring_lines:
        time, tension = extract_time_series(
            model,
            line.name,
            'Effective Tension',
            OrcFxAPI.oeEndA
        )

        stats = calculate_statistics(time, tension)

        # Check against ULS limit
        status = 'PASS' if stats['max'] <= design_criteria['max_tension_uls'] else 'FAIL'

        line_tension_results[line.name] = {
            'max_tension': stats['max'],
            'mean_tension': stats['mean'],
            'limit': design_criteria['max_tension_uls'],
            'status': status
        }

        if status == 'FAIL':
            results['overall_status'] = 'FAIL'

    results['checks']['line_tensions'] = line_tension_results

    # 3. Line clearance check (if seafloor specified)
    # (Simplified - would need seabed profile)

    return results
```

### 6. Advanced Analysis Techniques

```python
def extreme_response_analysis(
    model_path: Path,
    sea_states: List[dict],
    response_variable: tuple,
    method: str = 'most_probable_maximum'
) -> dict:
    """
    Extreme response analysis using irregular wave simulations.

    Args:
        model_path: Path to base model
        sea_states: List of sea state parameters
        response_variable: Tuple of (object_name, variable_name, object_extra)
        method: 'most_probable_maximum' or 'rayleigh_distribution'

    Returns:
        Extreme response statistics

    Example:
        >>> sea_states = [
        ...     {'Hs': 10.0, 'Tp': 14.0, 'duration': 3600, 'seeds': range(1, 11)},
        ...     {'Hs': 12.5, 'Tp': 15.0, 'duration': 3600, 'seeds': range(1, 11)}
        ... ]
        >>> extreme = extreme_response_analysis(
        ...     model_path=Path('mooring.dat'),
        ...     sea_states=sea_states,
        ...     response_variable=('Mooring_1', 'Effective Tension', OrcFxAPI.oeEndA)
        ... )
        >>> print(f"Most Probable Maximum: {extreme['mpm']:.1f} kN")
    """
    all_maxima = []

    for sea_state in sea_states:
        print(f"Sea State: Hs={sea_state['Hs']}, Tp={sea_state['Tp']}")

        for seed in sea_state['seeds']:
            # Load model
            model = OrcFxAPI.Model(str(model_path))

            # Set sea state
            model.environment.WaveHs = sea_state['Hs']
            model.environment.WaveTp = sea_state['Tp']
            model.environment.WaveSeed = seed

            # Set duration
            model.general.StageDuration[0] = 100  # Build-up
            model.general.StageDuration[1] = sea_state['duration']

            # Run simulation
            model.RunSimulation()

            # Extract response
            obj_name, var_name, obj_extra = response_variable
            time, response = extract_time_series(model, obj_name, var_name, obj_extra)

            # Get maximum (excluding build-up)
            mask = time >= 100
            max_response = np.max(response[mask])

            all_maxima.append({
                'Hs': sea_state['Hs'],
                'Tp': sea_state['Tp'],
                'seed': seed,
                'max': max_response
            })

            print(f"  Seed {seed}: Max = {max_response:.2f}")

    # Calculate statistics
    maxima_values = [m['max'] for m in all_maxima]

    # Most Probable Maximum (mean of maxima)
    mpm = np.mean(maxima_values)

    # Rayleigh distribution fit
    # For Rayleigh: mean_max = sigma * sqrt(2*ln(N))
    # where N = number of cycles
    # Solve for sigma
    N_cycles_estimate = sea_states[0]['duration'] / sea_states[0]['Tp']
    sigma_rayleigh = mpm / np.sqrt(2 * np.log(N_cycles_estimate))

    # Extreme value (e.g., 10000-year return period)
    # Using Rayleigh: X_extreme = sigma * sqrt(2*ln(N_extreme))
    N_extreme = 10000 * 365 * 24 * 3600 / sea_states[0]['Tp']  # 10000 years
    extreme_rayleigh = sigma_rayleigh * np.sqrt(2 * np.log(N_extreme))

    return {
        'all_maxima': all_maxima,
        'mpm': mpm,
        'std_maxima': np.std(maxima_values),
        'max_of_maxima': np.max(maxima_values),
        'min_of_maxima': np.min(maxima_values),
        'rayleigh_sigma': sigma_rayleigh,
        'extreme_10000yr_rayleigh': extreme_rayleigh
    }
```

## Complete Examples

### Example 1: Automated Mooring Analysis Workflow

```python
from pathlib import Path
import OrcFxAPI
import numpy as np
import pandas as pd

def complete_mooring_analysis_workflow(
    vessel_params: dict,
    mooring_config: dict,
    environment: dict,
    design_criteria: dict,
    output_dir: Path
) -> dict:
    """
    Complete automated mooring analysis workflow.

    Steps:
    1. Create model
    2. Run static analysis
    3. Run dynamic analysis
    4. Extract results
    5. Check against criteria
    6. Generate report

    Example:
        >>> vessel_params = {
        ...     'name': 'FPSO',
        ...     'mass': 150000,
        ...     'length': 300,
        ...     'draft': 20
        ... }
        >>> mooring_config = {
        ...     'pattern': 'spread',
        ...     'line_count': 8,
        ...     'line_length': 1500,
        ...     'fairlead_radius': 40,
        ...     'anchor_radius': 1400,
        ...     'line_sections': [
        ...         {'type': 'R4 Studless Chain', 'length': 300},
        ...         {'type': '76mm Wire', 'length': 900},
        ...         {'type': 'R4 Studless Chain', 'length': 300}
        ...     ]
        ... }
        >>> environment = {
        ...     'water_depth': 1200,
        ...     'current_speed': 1.0,
        ...     'wave_height': 8.0,
        ...     'wave_period': 13.0
        ... }
        >>> design_criteria = {
        ...     'max_offset': 50,
        ...     'max_tension_uls': 8000,
        ...     'safety_factor': 2.5
        ... }
        >>> results = complete_mooring_analysis_workflow(
        ...     vessel_params,
        ...     mooring_config,
        ...     environment,
        ...     design_criteria,
        ...     Path('mooring_analysis_results')
        ... )
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    print("="*70)
    print("AUTOMATED MOORING ANALYSIS WORKFLOW")
    print("="*70)

    # Step 1: Create model
    print("\n[Step 1/6] Creating model...")
    model = create_vessel_model(vessel_params, mooring_config, environment)

    # Save data file
    dat_file = output_dir / 'mooring_model.dat'
    model.SaveData(str(dat_file))
    print(f"Model saved: {dat_file}")

    # Step 2: Validate model
    print("\n[Step 2/6] Validating model...")
    validation = validate_model(model)
    if validation['overall_status'] == 'FAIL':
        print("Model validation failed!")
        print(f"Issues: {validation['issues']}")
        return {'status': 'FAILED', 'reason': 'Model validation failed'}

    print("Model validation passed")

    # Step 3: Run static analysis
    print("\n[Step 3/6] Running static analysis...")
    model.CalculateStatics()
    print("Static analysis complete")

    # Extract static results
    vessel = model[vessel_params['name']]
    static_x = vessel.StaticResult('X')
    static_y = vessel.StaticResult('Y')
    static_offset = np.sqrt(static_x**2 + static_y**2)

    print(f"Static offset: {static_offset:.2f} m")

    # Step 4: Run dynamic simulation
    print("\n[Step 4/6] Running dynamic simulation...")
    model.RunSimulation()

    # Save simulation
    sim_file = output_dir / 'mooring_model.sim'
    model.SaveSimulation(str(sim_file))
    print(f"Simulation saved: {sim_file}")

    # Step 5: Extract results
    print("\n[Step 5/6] Extracting results...")

    # Vessel motions
    time, x = extract_time_series(model, vessel_params['name'], 'X')
    time, y = extract_time_series(model, vessel_params['name'], 'Y')
    offset = np.sqrt(x**2 + y**2)

    offset_stats = calculate_statistics(time, offset)

    print(f"Vessel offset - Max: {offset_stats['max']:.2f} m, "
          f"Mean: {offset_stats['mean']:.2f} m")

    # Mooring line tensions
    mooring_results = {}

    for i in range(mooring_config['line_count']):
        line_name = f"Mooring_{i+1}"
        time, tension = extract_time_series(
            model,
            line_name,
            'Effective Tension',
            OrcFxAPI.oeEndA
        )

        stats = calculate_statistics(time, tension)
        mooring_results[line_name] = stats

        print(f"{line_name} - Max: {stats['max']:.1f} kN, Mean: {stats['mean']:.1f} kN")

    # Step 6: Check design criteria
    print("\n[Step 6/6] Checking design criteria...")

    integrity = check_mooring_system_integrity(
        model,
        vessel_params['name'],
        design_criteria
    )

    print(f"Design check status: {integrity['overall_status']}")

    # Generate summary report
    summary = {
        'status': 'SUCCESS',
        'files': {
            'model': dat_file,
            'results': sim_file
        },
        'static_results': {
            'offset': static_offset
        },
        'dynamic_results': {
            'offset': offset_stats,
            'mooring_tensions': mooring_results
        },
        'design_check': integrity
    }

    # Save summary to JSON
    import json
    summary_file = output_dir / 'analysis_summary.json'
    with open(summary_file, 'w') as f:
        # Convert numpy types to native Python types for JSON serialization
        json.dump(summary, f, indent=2, default=lambda x: float(x) if isinstance(x, np.number) else str(x))

    print(f"\nSummary saved: {summary_file}")
    print("\n" + "="*70)
    print("WORKFLOW COMPLETE")
    print("="*70)

    return summary

# Run workflow
vessel_params = {
    'name': 'FPSO',
    'mass': 150000,
    'length': 300,
    'draft': 20,
    'draft_fore': 20,
    'draft_aft': 20
}

mooring_config = {
    'pattern': 'spread',
    'line_count': 8,
    'line_length': 1500,
    'fairlead_radius': 40,
    'anchor_radius': 1400,
    'line_sections': [
        {'type': 'R4 Studless Chain', 'length': 300},
        {'type': '76mm Wire', 'length': 900},
        {'type': 'R4 Studless Chain', 'length': 300}
    ]
}

environment = {
    'water_depth': 1200,
    'current_speed': 1.0,
    'wave_height': 8.0,
    'wave_period': 13.0
}

design_criteria = {
    'max_offset': 50,
    'max_tension_uls': 8000,
    'safety_factor': 2.5
}

workflow_results = complete_mooring_analysis_workflow(
    vessel_params,
    mooring_config,
    environment,
    design_criteria,
    Path('mooring_analysis_results')
)
```

## Best Practices

### 1. Model Organization

```python
# Naming conventions
NAMING_CONVENTIONS = {
    'vessels': 'VesselName',  # e.g., 'FPSO', 'FSO_1'
    'lines': 'Mooring_N' or 'Riser_N',  # e.g., 'Mooring_1', 'Riser_2'
    'buoys': 'Buoy_N' or 'Subsurface_Buoy_N',
    '6d_buoys': '6DBuoy_N',
    'winches': 'Winch_N',
    'line_types': 'Descriptive_Name',  # e.g., 'R4_Studless_Chain', '76mm_Wire'
}

# Model structure best practices
MODEL_STRUCTURE = {
    'stages': [
        'Build-up',  # 100-200s
        'Main simulation',  # 3600-10800s
        'Optional: Transient event'
    ],
    'time_steps': {
        'inner': 0.01,  # 0.01-0.05s
        'log_sample': 0.1  # 0.1-1.0s
    }
}
```

### 2. Simulation Settings

```python
# Recommended simulation settings
SIMULATION_SETTINGS = {
    'implicit': {
        'use_variable_timestep': 'Yes',
        'target_log_sample_interval': 0.1,
        'inner_timestep': 0.01,
        'max_iterations': 20,
        'tolerance': 1e-6
    },
    'explicit': {
        'timestep': 0.001,  # Much smaller for explicit
        'log_sample_interval': 0.1
    }
}
```

### 3. Error Handling

```python
def safe_simulation_run(
    model: OrcFxAPI.Model,
    max_retries: int = 3
) -> bool:
    """
    Run simulation with error handling and retries.

    Args:
        model: OrcaFlex model
        max_retries: Maximum number of retry attempts

    Returns:
        True if successful, False otherwise
    """
    for attempt in range(max_retries):
        try:
            model.RunSimulation()
            return True
        except OrcFxAPI.DynamicsError as e:
            print(f"Dynamics error (attempt {attempt+1}): {e}")
            # Try reducing time step
            current_dt = model.general.InnerTimeStep
            model.general.InnerTimeStep = current_dt * 0.5
            print(f"Reducing time step to {model.general.InnerTimeStep}")
        except Exception as e:
            print(f"Unexpected error: {e}")
            return False

    return False
```

## Resources

### OrcaFlex Documentation

- **OrcaFlex Help**: Built-in help system (F1 in OrcaFlex)
- **Python API Reference**: OrcaFlex installation → Python folder → OrcFxAPIDocumentation.html
- **Example Scripts**: OrcaFlex → Examples → Python folder
- **Orcina Website**: https://www.orcina.com/resources/

### Training and Support

- **Orcina Training Courses**: Official OrcaFlex training
- **User Forum**: https://www.orcina.com/forums/
- **Technical Support**: support@orcina.com

### Related Standards

- **DNV-RP-C205**: Environmental Conditions and Environmental Loads
- **DNV-RP-F205**: Global Performance Analysis of Deepwater Floating Structures
- **API RP 2SM**: Recommended Practice for Design, Manufacture, Installation, and Maintenance of Synthetic Fiber Ropes
- **API RP 2SK**: Design and Analysis of Stationkeeping Systems for Floating Structures

### Additional Resources

- Noble Denton (2013). *OrcaFlex Training Manual*
- Orcina (2023). *OrcaFlex Manual Version 11.4*
- Various industry webinars and tutorials on YouTube

---

**Use this skill for:** Expert-level OrcaFlex modeling, automation, and analysis for offshore marine simulations with full Python API integration.
