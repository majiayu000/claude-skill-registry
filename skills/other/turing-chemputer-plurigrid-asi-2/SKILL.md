---
name: turing-chemputer
description: Cronin's Turing-complete chemputer for programmable chemical synthesis
  via XDL.
license: UNLICENSED
metadata:
  trit: 1
  source: local
---

# Turing Chemputer Skill: Programmable Chemical Synthesis

**Status**: ✅ Production Ready
**Trit**: 0 (ERGODIC - coordinator)
**Color**: #26D826 (Green)
**Principle**: Chemistry as computation
**Frame**: XDL programs executed on modular hardware

---

## Overview

**Turing Chemputer** coordinates chemical synthesis as program execution. Using XDL (Chemical Description Language), any synthesis protocol becomes an executable program on modular robotic hardware.

1. **XDL**: XML-based chemical programming language
2. **Chempiler**: Compile XDL to hardware instructions
3. **Modular hardware**: Reactors, filters, separators as primitives
4. **Turing completeness**: Loops, conditionals, recursion

## Core Framework

```xml
<!-- XDL: Chemical Description Language -->
<Synthesis>
  <Hardware>
    <Reactor id="reactor1" volume="100 mL"/>
    <Filter id="filter1"/>
    <Separator id="sep1"/>
  </Hardware>
  
  <Procedure>
    <Add reagent="A" vessel="reactor1" amount="10 mmol"/>
    <Add reagent="B" vessel="reactor1" amount="12 mmol"/>
    <HeatChill vessel="reactor1" temp="80 °C" time="2 h"/>
    <Filter from="reactor1" to="filter1"/>
  </Procedure>
</Synthesis>
```

```python
def compile_xdl(xdl: str) -> HardwareInstructions:
    """Chempiler: XDL → executable hardware program."""
    tree = parse_xdl(xdl)
    graph = build_synthesis_graph(tree)
    return optimize_and_schedule(graph)
```

## Key Concepts

### 1. XDL Programming

```python
class XDLProgram:
    def __init__(self):
        self.steps = []
    
    def add(self, reagent: str, vessel: str, amount: str):
        self.steps.append(Add(reagent, vessel, amount))
    
    def heat(self, vessel: str, temp: str, time: str):
        self.steps.append(HeatChill(vessel, temp, time))
    
    def filter(self, from_vessel: str, to_vessel: str):
        self.steps.append(Filter(from_vessel, to_vessel))
    
    def loop(self, times: int, body: list):
        """Turing-complete: iteration."""
        self.steps.append(Loop(times, body))
    
    def conditional(self, sensor: str, threshold: float, then: list, else_: list):
        """Turing-complete: branching."""
        self.steps.append(Conditional(sensor, threshold, then, else_))
```

### 2. Hardware Abstraction

```python
class Chemputer:
    def __init__(self, hardware_graph: nx.DiGraph):
        self.graph = hardware_graph
        self.state = ChemicalState()
    
    def execute(self, program: XDLProgram):
        """Execute XDL on hardware."""
        for step in program.steps:
            self.validate_hardware(step)
            self.execute_step(step)
            self.update_state(step)
    
    def validate_hardware(self, step):
        """Check hardware connectivity and capacity."""
        if not self.graph.has_path(step.source, step.target):
            raise HardwareError("No fluidic path")
```

### 3. Synthesis Graph Optimization

```python
def optimize_synthesis(xdl: XDLProgram) -> XDLProgram:
    """Optimize for time, yield, and hardware utilization."""
    graph = to_dag(xdl)
    
    # Parallelize independent operations
    parallel = find_parallel_steps(graph)
    
    # Minimize transfers
    optimized = minimize_transfers(graph)
    
    # Schedule for hardware
    return schedule(optimized, hardware_constraints)
```

## Commands

```bash
# Compile XDL to hardware
just chemputer-compile synthesis.xdl

# Validate hardware graph
just chemputer-validate hardware.json

# Simulate synthesis
just chemputer-simulate synthesis.xdl --dry-run

# Execute on hardware
just chemputer-execute synthesis.xdl --hardware lab1
```

## Integration with GF(3) Triads

```
assembly-index (-1) ⊗ turing-chemputer (0) ⊗ crn-topology (+1) = 0 ✓  [Molecular Complexity]
kolmogorov-compression (-1) ⊗ turing-chemputer (0) ⊗ dna-origami (+1) = 0 ✓  [Self-Assembly]
persistent-homology (-1) ⊗ turing-chemputer (0) ⊗ crn-topology (+1) = 0 ✓  [Topological CRN]
```

## Related Skills

- **assembly-index** (-1): Validate molecular complexity
- **crn-topology** (+1): Generate reaction networks
- **acsets** (0): Algebraic hardware graph representation

---

**Skill Name**: turing-chemputer
**Type**: Chemical Synthesis Coordinator
**Trit**: 0 (ERGODIC)
**Color**: #26D826 (Green)
