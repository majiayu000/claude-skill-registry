---
name: kscale
description: K-Scale Labs robotics skill collection - unified index for humanoid robot development, RL training, sim-to-real transfer, and deployment. Aggregates 9 specialized skills with GF(3) triadic organization.
version: 1.0.0
category: robotics-index
author: K-Scale Labs + Plurigrid
source: kscalelabs/*
license: MIT
trit: 0
trit_label: ERGODIC
color: "#5B8DEE"
verified: false
featured: true
---

# K-Scale Robotics Skill Collection

**Trit**: 0 (ERGODIC - coordination/infrastructure)
**Color**: #5B8DEE (Sky Blue)
**URI**: skill://kscale#5B8DEE

## Overview

This skill indexes the K-Scale Labs robotics ecosystem - a comprehensive open-source stack for building, training, and deploying humanoid robots. The collection follows GF(3) triadic organization with `kos-firmware` (+1) as the primary generator and `mujoco-scenes` (0) as the coordinator.

## Skill Inventory

```
┌────────────────────────────────────────────────────────────────────┐
│                    K-SCALE SKILL ECOSYSTEM                          │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  PLUS (+1) - Generation/Construction                               │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ kos-firmware        #79ED91  Robot firmware & gRPC services │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ERGODIC (0) - Coordination/Infrastructure                         │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ mujoco-scenes       #9FD875  Scene composition for MuJoCo   │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  MINUS (-1) - Analysis/Verification                                 │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ ksim-rl             #3A2F9E  RL training for locomotion     │   │
│  │ evla-vla            #DBA51D  Vision-language-action model   │   │
│  │ urdf2mjcf           #4615B7  URDF to MJCF conversion        │   │
│  │ kbot-humanoid       #5B45C2  K-Bot robot specifications     │   │
│  │ zeroth-bot          #8CC136  3D-printed humanoid platform   │   │
│  │ kscale-actuator     #B9172E  Robstride motor control        │   │
│  │ entropy-sim2real    #E85B8E  Entropy-driven sim2real        │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└────────────────────────────────────────────────────────────────────┘
```

## GF(3) Balance Analysis

**Current State**: UNBALANCED (trit sum = -6)

| Trit | Count | Skills |
|------|-------|--------|
| +1 (PLUS) | 1 | kos-firmware |
| 0 (ERGODIC) | 1 | mujoco-scenes |
| -1 (MINUS) | 7 | ksim-rl, evla-vla, urdf2mjcf, kbot-humanoid, zeroth-bot, kscale-actuator, entropy-sim2real |

### Balanced Triads

The primary balanced triad anchors the ecosystem:

```
ksim-rl (-1) ⊗ kos-firmware (+1) ⊗ mujoco-scenes (0) = 0 ✓
```

**Pattern**: Each MINUS skill can form a balanced triad by reusing the (kos-firmware, mujoco-scenes) pair:

```
evla-vla (-1)         ⊗ kos-firmware (+1) ⊗ mujoco-scenes (0) = 0 ✓
urdf2mjcf (-1)        ⊗ kos-firmware (+1) ⊗ mujoco-scenes (0) = 0 ✓
kbot-humanoid (-1)    ⊗ kos-firmware (+1) ⊗ mujoco-scenes (0) = 0 ✓
zeroth-bot (-1)       ⊗ kos-firmware (+1) ⊗ mujoco-scenes (0) = 0 ✓
kscale-actuator (-1)  ⊗ kos-firmware (+1) ⊗ mujoco-scenes (0) = 0 ✓
entropy-sim2real (-1) ⊗ kos-firmware (+1) ⊗ mujoco-scenes (0) = 0 ✓
```

### Recommendations for Balance

To achieve independent balanced triads (no skill reuse), add PLUS (+1) skills:

1. **kscale-deploy** (+1): Deployment automation, OTA updates
2. **kscale-onboard** (+1): On-robot compute orchestration
3. **kscale-teleop** (+1): Teleoperation and remote control
4. **kinfer-runtime** (+1): On-device inference runtime

## Architecture

```
                           ┌─────────────────────┐
                           │      TRAINING       │
                           │  ┌───────────────┐  │
                           │  │   ksim-rl     │  │
                           │  │  (PPO, AMP)   │  │
                           │  └───────────────┘  │
                           │         │           │
                           │         ▼           │
                           │  ┌───────────────┐  │
                           │  │ mujoco-scenes │  │
                           │  │ (environments)│  │
                           │  └───────────────┘  │
                           └─────────┬───────────┘
                                     │
              ┌──────────────────────┼──────────────────────┐
              │                      │                      │
              ▼                      ▼                      ▼
     ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
     │   MODELS        │    │   PERCEPTION    │    │   TRANSFER      │
     │ ┌─────────────┐ │    │ ┌─────────────┐ │    │ ┌─────────────┐ │
     │ │ urdf2mjcf   │ │    │ │   evla-vla  │ │    │ │entropy-sim2r│ │
     │ │ kbot-humanoi│ │    │ │  (VLA)      │ │    │ │  (domain    │ │
     │ │ zeroth-bot  │ │    │ └─────────────┘ │    │ │  random.)   │ │
     │ └─────────────┘ │    └─────────────────┘    │ └─────────────┘ │
     └─────────────────┘                           └─────────────────┘
              │                                             │
              └──────────────────────┬──────────────────────┘
                                     │
                                     ▼
                           ┌─────────────────────┐
                           │    DEPLOYMENT       │
                           │  ┌───────────────┐  │
                           │  │ kos-firmware  │  │
                           │  │   (+1)        │  │
                           │  └───────────────┘  │
                           │         │           │
                           │         ▼           │
                           │  ┌───────────────┐  │
                           │  │kscale-actuator│  │
                           │  │ (CAN motors)  │  │
                           │  └───────────────┘  │
                           └─────────────────────┘
```

## Usage

### Training Pipeline

```python
# Full K-Scale training pipeline
from ksim import PPOTask
from ksim.robots.kbot import KBotConfig
from mujoco_scenes import SceneBuilder, Terrain

class KBotWalkingTask(PPOTask):
    robot = KBotConfig(model_path="kbot.mjcf")
    
    def build_scene(self):
        scene = SceneBuilder()
        scene.add_terrain(Terrain.FLAT)
        scene.add_random_obstacles(count=5)
        return scene.to_mjcf()
    
    # Entropy-driven domain randomization
    physics_randomizers = [
        StaticFrictionRandomizer(scale=0.5),
        MassMultiplicationRandomizer(scale=0.2),
    ]

# Train
task = KBotWalkingTask()
task.run_training(num_envs=4096)
```

### Deployment Pipeline

```python
from pykos import KosClient

async def deploy_policy():
    async with KosClient("kbot.local:50051") as client:
        # Load trained policy
        await client.policy.load("walking_v1.onnx")
        
        # Start control loop
        await client.policy.start()
        
        # Monitor
        while True:
            state = await client.actuator.get_actuators_state()
            print(f"Position: {state.positions}")
```

## Key Contributors

- **codekansas** (Ben Bolte): Core architecture across ksim, kos
- **budzianowski**: EdgeVLA, dataset standardization
- **nfreq**: KOS PolicyService, calibration
- **WT-MM**: Visualization, integration
- **b-vm**: Randomizers, disturbances

## Repository Links

| Skill | Repository |
|-------|------------|
| ksim-rl | [kscalelabs/ksim](https://github.com/kscalelabs/ksim) |
| kos-firmware | [kscalelabs/kos](https://github.com/kscalelabs/kos) |
| evla-vla | [kscalelabs/evla](https://github.com/kscalelabs/evla) |
| urdf2mjcf | [kscalelabs/urdf2mjcf](https://github.com/kscalelabs/urdf2mjcf) |
| kbot-humanoid | [kscalelabs/kbot](https://github.com/kscalelabs/kbot) |
| zeroth-bot | [kscalelabs/zeroth-bot](https://github.com/kscalelabs/zeroth-bot) |
| mujoco-scenes | [kscalelabs/mujoco-scenes](https://github.com/kscalelabs/mujoco-scenes) |
| kscale-actuator | [kscalelabs/actuator](https://github.com/kscalelabs/actuator) |

## Related Skills

- `jaxlife-open-ended` (+1): Open-ended evolution for behavior discovery
- `ergodicity` (0): Ergodic theory foundations
- `wobble-dynamics` (0): Perturbation response analysis
- `stability` (-1): Dynamical system stability analysis

## References

```bibtex
@misc{kscale2024,
  title={K-Scale Labs Open Source Robotics Stack},
  author={K-Scale Labs},
  year={2024},
  url={https://github.com/kscalelabs}
}
```


## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 4. Pattern Matching

**Concepts**: unification, match, segment variables, pattern

### GF(3) Balanced Triad

```
kscale (−) + SDF.Ch4 (+) + [balancer] (○) = 0
```

**Skill Trit**: -1 (MINUS - verification)

### Secondary Chapters

- Ch5: Evaluation
- Ch2: Domain-Specific Languages

### Connection Pattern

Pattern matching extracts structure. This skill recognizes and transforms patterns.
