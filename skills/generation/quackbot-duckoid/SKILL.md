---
name: quackbot-duckoid
description: Mechanic wobbling duckoid robot that quacks and generates nonstandard musical scale compositions. Maximally cost-efficient design (~$68 BOM).
version: 1.0.0
category: robotics-musical
author: Plurigrid
source: plurigrid/asi
license: MIT
trit: 1
trit_label: PLUS
color: "#1FC4E0"
verified: false
featured: true
---

# QuackBot Duckoid

**Trit**: +1 (PLUS - generative/constructive)
**Color**: #1FC4E0 (Cyan)
**URI**: skill://quackbot-duckoid#1FC4E0

## Overview

A mechanic wobbling duckoid robot that:
- 🦆 **Quacks** with piezo-synthesized duck calls
- 🎵 **Composes** nonstandard musical scales (Bohlen-Pierce, just intonation, xenharmonic)
- 🌀 **Wobbles** via 2-DOF gimbal base with IMU feedback
- 💰 **Costs ~$68** total BOM

## Physical Design

```
                    ┌───────┐
                   ╱  O  O  ╲     ← LED eyes ($0.50)
                  │  ══════  │    ← Servo beak ($2)
                  │   ))))   │    ← Piezo speaker ($1)
                   ╲________╱
                       │
              ┌────────┴────────┐
             ╱                   ╲
            │    ┌─────────┐     │
            │    │ ESP32-S3│     │   ← MCU ($8)
    Wing ──▶│    │  +IMU   │     │◀── Wing
   ($2ea)   │    └─────────┘     │   ($2ea)
            │     ┌───────┐      │
            │     │ LiPo  │      │   ← Battery ($12)
             ╲    └───────┘     ╱
              └────────┬────────┘
                       │
              ╔════════╧════════╗
              ║   WOBBLE BASE   ║
              ║  ┌───┐   ┌───┐  ║   ← 2x MG996R ($10)
              ║  │ S │───│ S │  ║
              ║  └───┘   └───┘  ║
              ╚════════╤════════╝
                  ◯────┴────◯      ← Rubber feet ($2)
```

## Bill of Materials (BOM)

| Component | Qty | Unit Cost | Total |
|-----------|-----|-----------|-------|
| **Head** | | | **$15** |
| SG90 Micro Servo (beak) | 1 | $2 | $2 |
| Piezo Buzzer/Speaker | 1 | $1 | $1 |
| 5mm LED (eyes) | 2 | $0.25 | $0.50 |
| MPU6050 IMU | 1 | $3 | $3 |
| 3D Print (head shell) | 1 | $8.50 | $8.50 |
| **Body** | | | **$25** |
| ESP32-S3 DevKit | 1 | $8 | $8 |
| PAM8403 Amplifier | 1 | $1 | $1 |
| 2S LiPo 1000mAh | 1 | $12 | $12 |
| PCA9685 PWM Driver | 1 | $4 | $4 |
| **Wobble Base** | | | **$20** |
| MG996R Servo | 2 | $5 | $10 |
| 3D Print (gimbal) | 1 | $5 | $5 |
| Rubber Feet | 2 | $1 | $2 |
| Brass Counterweight | 1 | $3 | $3 |
| **Wings** | | | **$8** |
| SG90 Micro Servo | 2 | $2 | $4 |
| 3D Print (wings) | 2 | $2 | $4 |
| | | | |
| **TOTAL** | | | **$68** |

## Nonstandard Musical Scales

QuackBot composes using xenharmonic scales that are *not* 12-TET:

### Bohlen-Pierce Scale (13 steps per tritave)

```
Ratio:  1   25/21  9/7   7/5   5/3   9/5   15/7  7/3   25/9  3    ...
Step:   0    1      2     3     4     5     6     7     8    9    ...
Cents:  0   133.2  266.9 400.1 533.8 666.9 800.1 933.1 1066.9 1200
```

### Just Intonation (Ptolemaic)

```python
JUST_RATIOS = {
    'C': 1/1,      # Unison
    'D': 9/8,      # Major second
    'E': 5/4,      # Major third
    'F': 4/3,      # Perfect fourth
    'G': 3/2,      # Perfect fifth
    'A': 5/3,      # Major sixth
    'B': 15/8,     # Major seventh
}
```

### Wendy Carlos Alpha/Beta/Gamma

```python
CARLOS_ALPHA = 78.0   # cents per step (15.385 steps/octave)
CARLOS_BETA = 63.8    # cents per step (18.809 steps/octave)
CARLOS_GAMMA = 35.1   # cents per step (34.188 steps/octave)
```

### Quack-Native Scale (custom)

A duck-optimized scale based on duck vocalization formants:

```python
QUACK_SCALE = [
    1.0,      # Root quack
    1.059,    # Minor second quack
    1.189,    # Minor third quack  
    1.335,    # Fourth quack
    1.498,    # Fifth quack
    1.682,    # Sixth quack
    1.888,    # Seventh quack
]
# Formant frequencies: F1=1200Hz, F2=2400Hz, F3=3600Hz
```

## Wobble Dynamics

The 2-DOF gimbal creates a chaotic wobble pattern using coupled oscillators:

```python
import numpy as np

class WobbleDynamics:
    """Kuramoto-style coupled oscillator for duck wobble."""
    
    def __init__(self, natural_freq=2.0, coupling=0.5):
        self.omega = natural_freq  # rad/s
        self.K = coupling
        self.theta = [0.0, np.pi/4]  # pitch, roll phases
        
    def step(self, dt: float, imu_feedback: tuple) -> tuple:
        """Compute next wobble angles."""
        pitch_accel, roll_accel = imu_feedback
        
        # Kuramoto coupling
        phase_diff = self.theta[1] - self.theta[0]
        
        # Update phases with coupling and feedback
        self.theta[0] += dt * (
            self.omega + 
            self.K * np.sin(phase_diff) + 
            0.1 * pitch_accel
        )
        self.theta[1] += dt * (
            self.omega * 1.1 +  # Slight detuning
            self.K * np.sin(-phase_diff) + 
            0.1 * roll_accel
        )
        
        # Convert to servo angles (±30°)
        pitch_angle = 30 * np.sin(self.theta[0])
        roll_angle = 30 * np.sin(self.theta[1])
        
        return pitch_angle, roll_angle


class QuackSynthesizer:
    """Duck vocalization synthesizer."""
    
    FORMANTS = [1200, 2400, 3600]  # Hz
    
    def quack(self, duration_ms: int = 200, pitch_shift: float = 1.0):
        """Generate a quack waveform."""
        sr = 16000
        t = np.linspace(0, duration_ms/1000, int(sr * duration_ms/1000))
        
        # Fundamental with pitch shift
        f0 = 220 * pitch_shift
        
        # Sum formants
        signal = np.zeros_like(t)
        for i, formant in enumerate(self.FORMANTS):
            amp = 1.0 / (i + 1)  # Decreasing amplitude
            signal += amp * np.sin(2 * np.pi * formant * pitch_shift * t)
        
        # Apply envelope (sharp attack, quick decay)
        envelope = np.exp(-t * 20) * (1 - np.exp(-t * 100))
        
        return (signal * envelope * 32767).astype(np.int16)
    
    def compose_nonstandard(self, scale: list, pattern: list) -> list:
        """Compose using nonstandard scale."""
        quacks = []
        for note_idx, duration in pattern:
            pitch = scale[note_idx % len(scale)]
            quacks.append(self.quack(duration, pitch))
        return quacks
```

## MJCF Model

```xml
<mujoco model="quackbot">
  <compiler angle="radian" meshdir="meshes"/>
  
  <default>
    <joint damping="0.1" armature="0.01"/>
    <geom friction="0.8 0.02 0.01"/>
  </default>
  
  <asset>
    <mesh name="body" file="duck_body.stl"/>
    <mesh name="head" file="duck_head.stl"/>
    <mesh name="beak" file="duck_beak.stl"/>
    <mesh name="wing" file="duck_wing.stl"/>
  </asset>
  
  <worldbody>
    <!-- Wobble Base -->
    <body name="base" pos="0 0 0.05">
      <geom type="cylinder" size="0.08 0.02" rgba="0.2 0.2 0.2 1"/>
      
      <!-- Pitch Joint -->
      <body name="pitch_link" pos="0 0 0.03">
        <joint name="pitch" type="hinge" axis="0 1 0" range="-0.5 0.5"/>
        
        <!-- Roll Joint -->
        <body name="roll_link" pos="0 0 0.02">
          <joint name="roll" type="hinge" axis="1 0 0" range="-0.5 0.5"/>
          
          <!-- Duck Body -->
          <body name="body" pos="0 0 0.08">
            <geom type="mesh" mesh="body" rgba="1 0.9 0 1"/>
            <inertial pos="0 0 0" mass="0.3" diaginertia="0.001 0.001 0.001"/>
            
            <!-- Head -->
            <body name="head" pos="0 0.06 0.05">
              <geom type="mesh" mesh="head" rgba="1 0.9 0 1"/>
              
              <!-- Beak -->
              <body name="beak" pos="0 0.03 0">
                <joint name="beak" type="hinge" axis="1 0 0" range="0 0.3"/>
                <geom type="mesh" mesh="beak" rgba="1 0.5 0 1"/>
              </body>
            </body>
            
            <!-- Left Wing -->
            <body name="wing_l" pos="-0.06 0 0.02">
              <joint name="wing_l" type="hinge" axis="0 1 0" range="-0.5 0.5"/>
              <geom type="mesh" mesh="wing" rgba="1 0.9 0 1"/>
            </body>
            
            <!-- Right Wing -->
            <body name="wing_r" pos="0.06 0 0.02">
              <joint name="wing_r" type="hinge" axis="0 1 0" range="-0.5 0.5"/>
              <geom type="mesh" mesh="wing" rgba="1 0.9 0 1" euler="0 0 3.14"/>
            </body>
          </body>
        </body>
      </body>
    </body>
  </worldbody>
  
  <actuator>
    <position name="pitch_servo" joint="pitch" kp="50"/>
    <position name="roll_servo" joint="roll" kp="50"/>
    <position name="beak_servo" joint="beak" kp="20"/>
    <position name="wing_l_servo" joint="wing_l" kp="10"/>
    <position name="wing_r_servo" joint="wing_r" kp="10"/>
  </actuator>
</mujoco>
```

## ESP32 Firmware Skeleton

```cpp
#include <ESP32Servo.h>
#include <driver/i2s.h>
#include <MPU6050.h>

// Servos
Servo pitchServo, rollServo, beakServo, wingLServo, wingRServo;

// IMU
MPU6050 imu;

// Wobble state
float theta[2] = {0, M_PI/4};
const float omega = 2.0;
const float K = 0.5;

void setup() {
    // Attach servos
    pitchServo.attach(13);
    rollServo.attach(12);
    beakServo.attach(14);
    wingLServo.attach(27);
    wingRServo.attach(26);
    
    // Init IMU
    Wire.begin();
    imu.initialize();
    
    // Init I2S for audio
    i2s_config_t i2s_config = {
        .mode = I2S_MODE_MASTER | I2S_MODE_TX,
        .sample_rate = 16000,
        .bits_per_sample = I2S_BITS_PER_SAMPLE_16BIT,
        .channel_format = I2S_CHANNEL_FMT_ONLY_LEFT,
        .communication_format = I2S_COMM_FORMAT_I2S,
        .dma_buf_count = 8,
        .dma_buf_len = 64,
    };
    i2s_driver_install(I2S_NUM_0, &i2s_config, 0, NULL);
}

void loop() {
    // Read IMU
    int16_t ax, ay, az, gx, gy, gz;
    imu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
    
    // Wobble dynamics (Kuramoto)
    float dt = 0.02;
    float phase_diff = theta[1] - theta[0];
    theta[0] += dt * (omega + K * sin(phase_diff) + 0.0001 * ax);
    theta[1] += dt * (omega * 1.1 + K * sin(-phase_diff) + 0.0001 * ay);
    
    // Servo angles
    int pitch = 90 + 30 * sin(theta[0]);
    int roll = 90 + 30 * sin(theta[1]);
    
    pitchServo.write(pitch);
    rollServo.write(roll);
    
    // Occasional quack
    if (random(100) < 2) {
        quack();
    }
    
    // Wing flap (sync with wobble)
    wingLServo.write(90 + 20 * sin(theta[0] * 2));
    wingRServo.write(90 - 20 * sin(theta[0] * 2));
    
    delay(20);
}

void quack() {
    // Generate quack waveform
    int16_t buffer[800];
    for (int i = 0; i < 800; i++) {
        float t = i / 16000.0;
        float env = exp(-t * 20) * (1 - exp(-t * 100));
        float sig = sin(2 * M_PI * 1200 * t) + 
                    0.5 * sin(2 * M_PI * 2400 * t) +
                    0.25 * sin(2 * M_PI * 3600 * t);
        buffer[i] = (int16_t)(sig * env * 16000);
    }
    
    // Beak animation
    beakServo.write(120);
    
    size_t bytes_written;
    i2s_write(I2S_NUM_0, buffer, sizeof(buffer), &bytes_written, portMAX_DELAY);
    
    beakServo.write(90);
}
```

## GF(3) Triads

```
quackbot-duckoid (+1) ⊗ wobble-dynamics (0) ⊗ nonstandard-scales (+1) = needs -1
quackbot-duckoid (+1) ⊗ topos-of-music (-1) ⊗ wobble-dynamics (0) = 0 ✓
quackbot-duckoid (+1) ⊗ ksim-rl (-1) ⊗ mujoco-scenes (0) = 0 ✓
```

## Related Skills

- `topos-of-music` (-1): Mazzola's mathematical music theory
- `wobble-dynamics` (0): Kuramoto oscillators for motion
- `nonstandard-scales` (+1): Xenharmonic scale generation
- `ksim-rl` (-1): RL training for behaviors
- `catsharp-sonification` (0): GF(3) color → sound mapping

## Cost Optimization Strategies

1. **Use SG90 over MG996R** where torque permits (saves $6)
2. **ESP32-C3** instead of S3 if BLE sufficient (saves $3)
3. **Passive piezo** instead of active speaker (saves $0.50)
4. **Shared 3D print batch** for multiple units (saves 30%)

**Minimum viable BOM: $52**

## References

```bibtex
@article{bohlen1978,
  title={13 Tonstufen in der Duodezime},
  author={Bohlen, Heinz},
  journal={Acustica},
  year={1978}
}

@book{carlos1987,
  title={Tuning: At the Crossroads},
  author={Carlos, Wendy},
  year={1987}
}

@article{kuramoto1975,
  title={Self-entrainment of a population of coupled oscillators},
  author={Kuramoto, Yoshiki},
  journal={Lecture Notes in Physics},
  year={1975}
}
```


## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 1. Flexibility through Abstraction

**Concepts**: combinators, compose, parallel-combine, spread-combine, arity

### GF(3) Balanced Triad

```
quackbot-duckoid (○) + SDF.Ch1 (+) + [balancer] (−) = 0
```

**Skill Trit**: 0 (ERGODIC - coordination)

### Secondary Chapters

- Ch4: Pattern Matching
- Ch6: Layering
- Ch10: Adventure Game Example

### Connection Pattern

Combinators compose operations. This skill provides composable abstractions.
