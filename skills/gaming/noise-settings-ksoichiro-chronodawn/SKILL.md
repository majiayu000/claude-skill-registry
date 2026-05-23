---
name: noise-settings
description: Terrain generation and noise settings customization guide
---

# Custom Noise Settings (Terrain Generation)

**Purpose**: Guide for understanding and customizing Minecraft's terrain generation system.

**How it works**: This skill is automatically activated when you mention tasks related to:
- Customizing terrain generation
- Modifying noise settings
- Adjusting biome sizes
- Creating custom dimension terrain
- Troubleshooting terrain generation issues

Simply describe what you want to do, and Claude will reference the appropriate guidance from this skill.

---

## Difficulty Assessment

Based on T299 experiment (2025-12-13):

**Simple Approach** (BiomeScalingMixin):
- **Difficulty**: Easy
- **Effectiveness**: High
- **Use Case**: Biome size adjustment

**Custom Noise Settings**:
- **Difficulty**: Very difficult
- **Time Required**: 10-15 hours of trial-and-error
- **Use Case**: Complete terrain customization

---

## Lessons Learned from T299 Experiment

### 1. Vanilla Settings Are Highly Optimized

`minecraft:overworld` provides balanced, natural terrain that's the result of extensive testing and tuning.

**Implication**: Starting from scratch requires deep understanding of noise mathematics.

### 2. Parameter Tuning Is Complex

Small changes cause drastic terrain changes:

**Observed Issues**:
- Mountains extending from Y=-40 to Y=320
- Lava seas at surface level
- Flat mountain summits
- Unnatural terrain transitions

**Root Cause**: Density function parameters are highly sensitive and interdependent.

### 3. Density Functions Require Mathematical Understanding

**Challenge**: Understanding how noise values translate to terrain density (block placement).

**Key Concepts**:
- **Noise Functions**: Generate pseudo-random values
- **Density Functions**: Convert noise to block density
- **Threshold Values**: Determine air vs. block
- **Interpolation**: Smooth transitions between biomes

**Learning Curve**: Requires studying vanilla implementations and experimenting extensively.

### 4. BiomeScalingMixin Is More Practical

**Approach**: Scale biome coordinates via Mixin injection

**Advantages**:
- Simple implementation (1 Mixin class)
- Predictable results
- No terrain generation issues
- Maintains vanilla terrain quality

**Disadvantages**:
- Limited to biome size adjustment
- Cannot modify terrain shape/height

---

## Recommended Approaches

### For Biome Size Adjustment

**Use**: Mixin-based coordinate scaling

**Implementation**: BiomeScalingMixin

**Reason**: Effective, simple, no terrain artifacts

### For Terrain Customization

**Use**: Vanilla density functions as base, modify incrementally

**Process**:
1. Copy vanilla `minecraft:overworld` noise settings
2. Make small adjustments to one parameter
3. Test extensively in-game
4. Iterate until desired result

**Avoid**: Creating noise_settings from scratch unless absolutely necessary

### For Custom Dimensions

**Use**: Vanilla presets as templates

**Available Presets**:
- `minecraft:overworld` - Standard terrain
- `minecraft:nether` - Ceiling + floor with open middle
- `minecraft:end` - Floating islands
- `minecraft:amplified` - Extreme height variation

**Strategy**: Start with closest vanilla preset, modify parameters gradually

---

## Understanding Noise Settings Components

### 1. Noise Router

Routes different noise generators to terrain features:

**Key Routes**:
- `final_density` - Determines block vs. air
- `continents` - Continental scale features
- `erosion` - Erosion effects
- `ridges` - Mountain ridges
- `depth` - Ocean depth

### 2. Density Functions

Mathematical functions that generate terrain density:

**Types**:
- Noise-based (e.g., `noise`, `shifted_noise`)
- Mathematical (e.g., `add`, `mul`, `clamp`)
- Positional (e.g., `y_clamped_gradient`)

### 3. Spawn Target

Defines spawn point terrain preferences:

**Parameters**:
- `continentalness` - Distance from ocean
- `erosion` - Erosion level
- `weirdness` - Terrain weirdness
- `temperature` - Temperature range
- `humidity` - Humidity range

---

## Parameter Tuning Guidelines

### Start Conservative

Make small adjustments (5-10% changes) and test

### Test Frequently

Generate test worlds after each change to verify results

### Document Changes

Keep notes on what each parameter change does:

```
Change: Increased continentalness scale from 1.0 to 1.2
Result: Larger continents, more ocean space
Side Effects: None observed
```

### Use Debug Visualization

Press F3 in-game to see:
- Current biome
- Biome parameters
- Coordinates

---

## Common Pitfalls

### 1. Extreme Parameter Values

**Problem**: Using values too far from vanilla (e.g., multiplying by 10)

**Result**: Broken terrain, impossible landscapes

**Solution**: Adjust incrementally (1.1x, 1.2x, etc.)

### 2. Ignoring Interdependencies

**Problem**: Changing one parameter without considering related parameters

**Result**: Inconsistent terrain, artifacts

**Solution**: Understand parameter relationships, adjust related parameters together

### 3. Not Testing Edge Cases

**Problem**: Only testing one biome or area

**Result**: Terrain breaks in specific biomes or coordinates

**Solution**: Test multiple biomes, visit various X/Z coordinates

### 4. Forgetting Vertical Range

**Problem**: Not considering Y-level effects

**Result**: Underground caverns at surface, solid ground at build limit

**Solution**: Test terrain at multiple Y-levels (Y=-64, Y=0, Y=64, Y=256)

---

## Debugging Terrain Generation

### Symptom: Terrain Too Flat

**Possible Causes**:
- Erosion parameter too high
- Continentalness variation too low
- Ridge noise scale too small

### Symptom: Extreme Mountains

**Possible Causes**:
- Ridge noise scale too high
- Erosion parameter too low
- Y-gradient too steep

### Symptom: Lava Seas at Surface

**Possible Causes**:
- Depth parameter misconfigured
- Final density threshold incorrect
- Y-gradient inverted

### Symptom: Unnatural Biome Transitions

**Possible Causes**:
- Biome parameters too discrete
- Interpolation disabled or misconfigured
- Temperature/humidity ranges not overlapping

---

## Tools and Resources

### In-Game Debug Tools

- **F3 Debug Screen**: Shows current biome and parameters
- **F3 + G**: Shows chunk boundaries
- **Debug Stick**: Modify block states (creative mode)

### External Tools

- **MCA Selector**: View world from above, export regions
- **Amidst**: Preview biome distribution (1.12 and earlier)
- **Cubiomes Viewer**: Biome visualization (1.13+)

### Reference Implementations

- **Vanilla Data Packs**: `minecraft:overworld`, `minecraft:amplified`
- **Terralith**: Advanced terrain generation datapack
- **William Wythers' Overhauled Overworld**: Custom terrain example

---

## Reference: T299 Experiment Summary

**Goal**: Create custom noise settings for larger biome sizes

**Approach Tried**: Custom noise_settings.json from scratch

**Results**:
- ❌ Extreme mountains (Y=-40 to Y=320)
- ❌ Lava seas at surface
- ❌ Flat mountain summits
- ❌ Unnatural terrain transitions
- ✅ Biome sizes increased (desired effect)

**Conclusion**: BiomeScalingMixin approach is more practical and reliable

**Time Invested**: Multiple hours of parameter tuning

**Recommendation**: Use BiomeScalingMixin unless terrain shape modification is required

---

**Last Updated**: 2026-01-16
**Maintained by**: Chrono Dawn Development Team
