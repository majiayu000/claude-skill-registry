---
name: ksim-rl
description: RL training library for humanoid locomotion and manipulation built on MuJoCo and JAX. Provides PPO, AMP, and custom task abstractions for sim-to-real robotics policy training.
version: 1.0.0
category: robotics-rl
author: K-Scale Labs
source: kscalelabs/ksim
license: MIT
trit: -1
trit_label: MINUS
color: "#3A2F9E"
verified: false
featured: true
---

# KSIM-RL Skill

**Trit**: -1 (MINUS - analysis/verification)
**Color**: #3A2F9E (Deep Purple)
**URI**: skill://ksim-rl#3A2F9E

## Overview

KSIM is K-Scale Labs' reinforcement learning library for humanoid robot locomotion and manipulation. Built on MuJoCo for physics simulation and JAX for hardware-accelerated training.

## Core Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        KSIM ARCHITECTURE                        │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │  RLTask     │  │  PPOTask    │  │  AMPTask                │  │
│  │  (abstract) │──│  (PPO impl) │──│  (Adversarial Motion)   │  │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘  │
│         │                                                        │
│         ▼                                                        │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                    PhysicsEngine                             │ │
│  │  ┌───────────────┐  ┌───────────────────────────────┐       │ │
│  │  │ MujocoEngine  │  │ MjxEngine (JAX-accelerated)   │       │ │
│  │  └───────────────┘  └───────────────────────────────┘       │ │
│  └─────────────────────────────────────────────────────────────┘ │
│         │                                                        │
│         ▼                                                        │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  Environment Components                                      │ │
│  │  • Actuators: Position, Velocity, Torque control            │ │
│  │  • Observations: Joint states, IMU, local view              │ │
│  │  • Rewards: Velocity tracking, gait, energy, stability      │ │
│  │  • Terminations: Fall detection, boundary violations        │ │
│  └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Key Features

- **JAX-Accelerated**: Uses MJX for parallel environment simulation on GPU/TPU
- **PPO Training**: Proximal Policy Optimization with configurable hyperparameters
- **AMP Support**: Adversarial Motion Priors for realistic humanoid locomotion
- **Modular Rewards**: Composable reward functions for gait, velocity, energy
- **Domain Randomization**: Built-in randomizers for sim-to-real transfer

## API Usage

```python
import ksim
from ksim import PPOTask, MjxEngine
from ksim.tasks.humanoid import HumanoidWalkingTask

# Define custom task
class KBotWalkingTask(PPOTask):
    model_path = "kbot.mjcf"
    
    # Observations
    observations = [
        ksim.JointPosition(),
        ksim.JointVelocity(),
        ksim.IMUAngularVelocity(),
        ksim.BaseOrientation(),
    ]
    
    # Rewards
    rewards = [
        ksim.LinearVelocityReward(scale=1.0),
        ksim.GaitPhaseReward(scale=0.5),
        ksim.EnergyPenalty(scale=-0.01),
    ]
    
    # Actuators
    actuators = [
        ksim.PositionActuator(
            joint_name=".*",
            kp=100.0,
            kd=10.0,
            action_scale=0.5,
        )
    ]

# Train
task = KBotWalkingTask()
task.run_training(
    num_envs=4096,
    num_steps=1000000,
    learning_rate=3e-4,
)
```

## GF(3) Triads

This skill participates in balanced triads:

```
ksim-rl (-1) ⊗ kos-firmware (+1) ⊗ mujoco-scenes (0) = 0 ✓
ksim-rl (-1) ⊗ kos-firmware (+1) ⊗ urdf2mjcf (0) = needs balancing
```

## Key Contributors

- **codekansas** (Ben Bolte): Core architecture, PPO, rewards
- **b-vm**: Randomizers, disturbances, policy training
- **carlosdp**: Adaptive KL, action scaling
- **WT-MM**: Visualization, markers

## Related Skills

- `kos-firmware` (+1): Robot firmware and gRPC services
- `mujoco-scenes` (0): Scene composition for MuJoCo
- `evla-vla` (-1): Vision-language-action models
- `urdf2mjcf` (-1): URDF to MJCF conversion
- `ktune-sim2real` (-1): Servo tuning for sim2real

## References

```bibtex
@misc{ksim2024,
  title={K-Sim: RL Training for Humanoid Locomotion},
  author={K-Scale Labs},
  year={2024},
  url={https://github.com/kscalelabs/ksim}
}
```


## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 5. Evaluation

**Concepts**: eval, apply, interpreter, environment

### GF(3) Balanced Triad

```
ksim-rl (○) + SDF.Ch5 (−) + [balancer] (+) = 0
```

**Skill Trit**: 0 (ERGODIC - coordination)

### Secondary Chapters

- Ch2: Domain-Specific Languages

### Connection Pattern

Evaluation interprets expressions. This skill processes or generates evaluable forms.
