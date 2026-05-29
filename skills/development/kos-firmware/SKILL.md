---
name: kos-firmware
description: K-Scale Operating System - Rust-based robot firmware with gRPC services for actuator control, IMU, and sim2real transfer. Platform abstraction layer for hardware/simulation backends.
version: 1.0.0
category: robotics-firmware
author: K-Scale Labs
source: kscalelabs/kos
license: MIT
trit: 1
trit_label: PLUS
color: "#79ED91"
verified: false
featured: true
---

# KOS Firmware Skill

**Trit**: +1 (PLUS - generation/construction)
**Color**: #79ED91 (Bright Green)
**URI**: skill://kos-firmware#79ED91

## Overview

KOS (K-Scale Operating System) is a general-purpose, configurable framework for robot firmware. Written in Rust with gRPC services exposed to Python clients via pykos.

## Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                     KOS ARCHITECTURE                            │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    Python Client (pykos)                  │  │
│  │  KosClient.actuator.command_actuators(...)               │  │
│  │  KosClient.imu.get_imu_values()                          │  │
│  │  KosClient.sim.reset()                                   │  │
│  └──────────────────────────────────────────────────────────┘  │
│                            │ gRPC                               │
│                            ▼                                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                   KOS Runtime Daemon                      │  │
│  │  ┌─────────────┬─────────────┬─────────────────────────┐ │  │
│  │  │ Actuator    │ IMU         │ Simulation              │ │  │
│  │  │ Service     │ Service     │ Service                 │ │  │
│  │  └─────────────┴─────────────┴─────────────────────────┘ │  │
│  └──────────────────────────────────────────────────────────┘  │
│                            │ HAL Traits                         │
│                            ▼                                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Platform Abstraction Layer                   │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐   │  │
│  │  │ KBot HAL    │  │ ZBot HAL    │  │ Stub (Testing)  │   │  │
│  │  │ (Hardware)  │  │ (Hardware)  │  │ (Simulation)    │   │  │
│  │  └─────────────┘  └─────────────┘  └─────────────────┘   │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────┘
```

## gRPC Services

### ActuatorService

```protobuf
service ActuatorService {
  rpc CommandActuators(CommandActuatorsRequest) returns (CommandActuatorsResponse);
  rpc ConfigureActuator(ConfigureActuatorRequest) returns (ActionResponse);
  rpc CalibrateActuator(CalibrateActuatorRequest) returns (ActionResponse);
  rpc GetActuatorsState(GetActuatorsStateRequest) returns (ActuatorStateResponse);
  rpc ParameterDump(ParameterDumpRequest) returns (ParameterDumpResponse);
}
```

### SimulationService (for sim2real)

```protobuf
service SimulationService {
  rpc Reset(ResetRequest) returns (ResetResponse);
  rpc SetPaused(SetPausedRequest) returns (ActionResponse);
  rpc Step(StepRequest) returns (StepResponse);
  rpc AddMarker(AddMarkerRequest) returns (ActionResponse);
  rpc SetParameters(SetParametersRequest) returns (ActionResponse);
}
```

## Python Client Usage

```python
from pykos import KosClient

async def control_robot():
    async with KosClient("localhost:50051") as client:
        # Get actuator states
        states = await client.actuator.get_actuators_state([1, 2, 3])
        
        # Command positions
        await client.actuator.command_actuators([
            {"actuator_id": 1, "position": 0.5},
            {"actuator_id": 2, "position": -0.3},
        ])
        
        # Configure actuator
        await client.actuator.configure_actuator(
            actuator_id=1,
            kp=100.0,
            kd=10.0,
            torque_enabled=True,
        )
        
        # Calibrate
        await client.actuator.calibrate(1)

# For simulation
async def sim_control():
    async with KosClient("localhost:50051") as client:
        await client.sim.reset()
        await client.sim.step(dt=0.002)
        await client.sim.add_marker(
            name="target",
            position=[1.0, 0.0, 0.5],
            color=[1.0, 0.0, 0.0],
        )
```

## Key Contributors

- **codekansas** (Ben Bolte): Core architecture, async client
- **nfreq**: PolicyService, calibration, parameter dump
- **WT-MM**: Markers, visualization
- **hatomist**: Acceleration, telemetry

## GF(3) Triads

This skill participates in balanced triads:

```
ksim-rl (-1) ⊗ kos-firmware (+1) ⊗ mujoco-scenes (0) = 0 ✓
kos-firmware (+1) ⊗ evla-vla (-1) ⊗ ktune-sim2real (0) = 0 ✓
```

## Related Skills

- `ksim-rl` (-1): RL training library
- `evla-vla` (-1): Vision-language-action models
- `kbot-humanoid` (-1): K-Bot robot configuration
- `zeroth-bot` (-1): Zeroth bot 3D-printed platform
- `mujoco-scenes` (0): Scene composition

## References

```bibtex
@misc{kos2024,
  title={KOS: K-Scale Operating System for Robot Firmware},
  author={K-Scale Labs},
  year={2024},
  url={https://github.com/kscalelabs/kos}
}
```


## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 6. Layering

**Concepts**: layered data, metadata, provenance, units

### GF(3) Balanced Triad

```
kos-firmware (−) + SDF.Ch6 (+) + [balancer] (○) = 0
```

**Skill Trit**: -1 (MINUS - verification)

### Secondary Chapters

- Ch2: Domain-Specific Languages

### Connection Pattern

Layering adds metadata. This skill tracks provenance or annotations.
