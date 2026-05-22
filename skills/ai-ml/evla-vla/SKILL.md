---
name: evla-vla
description: EdgeVLA - Open-source edge vision-language-action model for robotics. Standardizes Open-X Embodiment datasets for consistent VLA training and deployment.
version: 1.0.0
category: robotics-vla
author: K-Scale Labs
source: kscalelabs/evla
license: MIT
trit: -1
trit_label: MINUS
color: "#DBA51D"
verified: false
featured: true
---

# EdgeVLA Skill

**Trit**: -1 (MINUS - analysis/verification)
**Color**: #DBA51D (Golden Yellow)
**URI**: skill://evla-vla#DBA51D

## Overview

EdgeVLA is an open-source edge vision-language-action model for robotics. It standardizes diverse robotics datasets from the Open-X Embodiment (OXE) collection for consistent training and deployment.

## Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                     EdgeVLA ARCHITECTURE                        │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Open-X Embodiment Datasets                   │  │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐         │  │
│  │  │ DROID   │ │ Bridge  │ │ LIBERO  │ │ RT-X    │ + 60... │  │
│  │  └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘         │  │
│  └───────┼───────────┼───────────┼───────────┼──────────────┘  │
│          │           │           │           │                  │
│          ▼           ▼           ▼           ▼                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │           OXE_DATASET_CONFIGS Standardization            │  │
│  │  • image_obs_keys: primary, secondary, wrist cameras     │  │
│  │  • state_encoding: POS_EULER, POS_QUAT, JOINT           │  │
│  │  • action_encoding: EEF_POS, JOINT_POS                  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                  │
│                              ▼                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                  Unified Data Format                      │  │
│  │  ┌─────────────────────────────────────────────────────┐ │  │
│  │  │ Images: resized, normalized, multi-view             │ │  │
│  │  │ States: 8-dim standardized proprioception           │ │  │
│  │  │ Actions: 7-dim EEF or joint actions                 │ │  │
│  │  └─────────────────────────────────────────────────────┘ │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                  │
│                              ▼                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                     VLA Model                             │  │
│  │  Vision Encoder → Language Model → Action Decoder        │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────┘
```

## Dataset Configuration

```python
from evla.config import OXE_DATASET_CONFIGS, StateEncoding, ActionEncoding

# DROID dataset configuration
droid_config = OXE_DATASET_CONFIGS["droid"]
# {
#     "image_obs_keys": {
#         "primary": "exterior_image_1_left",
#         "secondary": "exterior_image_2_left",
#         "wrist": "wrist_image_left",
#     },
#     "state_encoding": StateEncoding.POS_QUAT,
#     "action_encoding": ActionEncoding.EEF_POS,
# }

# Bridge dataset configuration
bridge_config = OXE_DATASET_CONFIGS["bridge"]
# {
#     "image_obs_keys": {
#         "primary": "image_0",
#         "wrist": "image_1",
#     },
#     "state_encoding": StateEncoding.POS_EULER,
#     "action_encoding": ActionEncoding.EEF_POS,
# }
```

## Named Mixtures

```python
from evla.config import OXE_NAMED_MIXTURES

# Comprehensive multi-dataset training
oxe_magic_soup = OXE_NAMED_MIXTURES["oxe_magic_soup"]

# RT-X reproduction
rtx_mixture = OXE_NAMED_MIXTURES["rtx"]

# Custom mixture with weights
custom_mixture = {
    "droid": 1.0,
    "bridge": 0.5,
    "libero": 0.3,
}
```

## Usage

```python
from evla import EdgeVLA, DataLoader

# Load model
model = EdgeVLA.from_pretrained("kscale/evla-base")

# Create dataloader with mixture
loader = DataLoader(
    mixture="oxe_magic_soup",
    batch_size=32,
    image_size=(224, 224),
)

# Training loop
for batch in loader:
    images = batch["images"]  # (B, V, H, W, C)
    states = batch["states"]  # (B, 8)
    actions = batch["actions"]  # (B, 7)
    
    loss = model.train_step(images, states, actions)

# Inference
with torch.no_grad():
    image = camera.capture()
    state = robot.get_state()
    action = model.predict(image, state, "pick up the red block")
    robot.execute(action)
```

## Key Contributors

- **budzianowski**: Core architecture, dataset configs, finetuning
- **moojink**: LIBERO eval, dataset transforms
- **WT-MM**: README, integration

## GF(3) Triads

This skill participates in balanced triads:

```
evla-vla (-1) ⊗ kos-firmware (+1) ⊗ mujoco-scenes (0) = 0 ✓
ksim-rl (-1) ⊗ topos-generate (+1) ⊗ evla-vla (-1) = needs balancing
```

## Related Skills

- `kos-firmware` (+1): Robot firmware for deployment
- `ksim-rl` (-1): RL training for locomotion
- `kbot-humanoid` (-1): K-Bot configuration
- `mujoco-scenes` (0): Scene composition

## References

```bibtex
@misc{evla2024,
  title={EdgeVLA: Open-Source Edge Vision-Language-Action Model},
  author={K-Scale Labs},
  year={2024},
  url={https://github.com/kscalelabs/evla}
}

@article{openvla2024,
  title={OpenVLA: An Open-Source Vision-Language-Action Model},
  author={Kim, Moo Jin and others},
  journal={arXiv:2406.09246},
  year={2024}
}
```


## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 5. Evaluation

**Concepts**: eval, apply, interpreter, environment

### GF(3) Balanced Triad

```
evla-vla (−) + SDF.Ch5 (−) + [balancer] (−) = 0
```

**Skill Trit**: -1 (MINUS - verification)

### Secondary Chapters

- Ch2: Domain-Specific Languages

### Connection Pattern

Evaluation interprets expressions. This skill processes or generates evaluable forms.
