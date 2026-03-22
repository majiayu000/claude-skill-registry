---
name: vvvv-shaders
description: Helps write SDSL shaders for Stride and vvvv gamma — TextureFX, shader mixins, compute shaders, and ShaderFX composition. Use when writing or debugging .sdsl shader files, creating visual effects, working with the Stride rendering pipeline, or composing shader mixins.
license: CC-BY-SA-4.0
compatibility: Designed for coding AI agents assisting with vvvv gamma development
metadata:
  author: Tebjan Halm
  version: "1.0"
---

# SDSL Shaders for vvvv gamma / Stride

## What Is SDSL

SDSL (Stride Shading Language) is Stride's shader language — a superset of HLSL with four key additions: `shader` classes with inheritance, multiple inheritance (mixins), the `streams` system for automatic inter-stage data flow, and `override` for clean method replacement. Shaders are defined in `.sdsl` files.

## Streams System

Streams replace manual VS_INPUT/VS_OUTPUT structs. Declare once, access everywhere:

```hlsl
stream float4 MyData : TEXCOORD5;      // Declare a custom stream variable

// In vertex shader:
streams.MyData = float4(1, 0, 0, 1);   // Write

// In pixel shader:
float4 d = streams.MyData;             // Read (auto-interpolated)
```

Key built-in streams:
- `streams.ShadingPosition` (SV_Position) — clip-space position
- `streams.ColorTarget` (SV_Target0) — pixel shader output
- `streams.Position` (float4) — object-space position
- `streams.TexCoord` (TEXCOORD0) — texture coordinates
- `streams.normalWS` — world-space normal

## Base Shader Hierarchy

### Stride Core (available in both Stride and vvvv)

| Shader | Provides |
|---|---|
| `ShaderBase` | VSMain/PSMain entry points |
| `Texturing` | Texture0-9, Sampler, PointSampler, LinearSampler, TexCoord |
| `Transformation` | World, View, Projection, WorldViewProjection matrices |
| `PositionStream4` | Position, PositionWS, DepthVS |
| `NormalStream` | meshNormal, normalWS, tangentToWorld |
| `ComputeShaderBase` | CSMain entry, Compute() hook, thread groups |
| `ComputeColor` | Interface returning float4 via Compute() |
| `ComputeVoid` | Interface returning void via Compute() |
| `Global` | Time, TimeStep (cbuffer PerFrame) |

### vvvv-Only (NOT available in plain Stride)

| Shader | Inherits | Use For |
|---|---|---|
| `VS_PS_Base` | ShaderBase, PositionStream4, NormalStream, Transformation | DrawFX base |
| `FilterBase` | TextureFX | Pixel-processing texture effects |
| `MixerBase` | TextureFX | Blending textures |
| `TextureFX` | ImageEffectShader, Camera, ShaderUtils | Texture effect base |

**Important**: `VS_PS_Base` already includes Transformation, NormalStream, and PositionStream4. Do NOT re-inherit them.

## File Naming → Auto Node Generation

vvvv automatically creates nodes from shaders based on filename suffix:

| Suffix | Node Type | Description |
|---|---|---|
| `_TextureFX.sdsl` | TextureFX | Image processing effects |
| `_DrawFX.sdsl` | DrawFX | Drawing/rendering shaders |
| `_ComputeFX.sdsl` | ComputeFX | Compute shaders |
| `_ShaderFX.sdsl` | ShaderFX | General shader effects |

Example: `MyBlur_TextureFX.sdsl` automatically creates a "MyBlur" TextureFX node.

## Basic TextureFX Structure

```hlsl
shader MyEffect_TextureFX : FilterBase
{
    float Intensity = 1.0;

    float4 Filter(float4 tex0col)
    {
        return tex0col * Intensity;
    }
};
```

Note the **semicolon after the closing brace** — this is required.

## Syntax Rules

For critical SDSL syntax rules (`static const` scope, semicolons, `override`, variable initialization, common mistakes, branch divergence), see [syntax-rules.md](syntax-rules.md).

## Keywords

| Keyword | Purpose |
|---|---|
| `shader` | Defines a shader class |
| `override` | Required when overriding parent methods |
| `base` | Access parent implementation |
| `stage` | Ensures member defined once across compositions |
| `stream` | Member accessible at every shader stage |
| `static` | Static methods callable without inheritance |
| `compose` | Declare a composition slot for shader mixins |
| `clone` | Force separate instance of a composed shader |
| `abstract` | Method without body (child must implement) |

## Inheritance & Mixins

```hlsl
// Single inheritance
shader Child : Parent
{
    override float4 Filter(float4 tex0col)
    {
        return base.Filter(tex0col) * 0.5;
    }
};

// Multiple inheritance (mixins)
shader MyShader : FilterBase, ColorUtils, MathUtils
{
    float4 Filter(float4 tex0col)
    {
        float3 linear = ColorUtils.GammaToLinear(tex0col.rgb);
        return float4(linear, tex0col.a);
    }
};

// Static function calls (no inheritance needed)
float3 result = ColorUtils.LinearToGamma(col.rgb);
```

## Enum Binding — C# Enum in Shaders

In the shader (`.sdsl`):
```hlsl
[EnumType("MyNamespace.BlendMode, MyAssembly")]
int Mode = 0;
```

In C# (`.cs`):
```csharp
namespace MyNamespace;
public enum BlendMode
{
    Normal = 0,
    Add = 1,
    Multiply = 2,
    Screen = 3
}
```

Requirements:
- The enum DLL must be pre-compiled (not from dynamic csproj)
- Assembly name is the project name
- vvvv must be restarted after enum DLL changes

## GPU Best Practices

### Protect Against Math Errors

```hlsl
float3 safeLog = log2(max(x, 1e-10));     // Avoid log2(0)
float3 safe = x / max(y, 0.0001);          // Avoid div by zero
float3 safePow = pow(max(x, 0.0), gamma);  // Avoid pow(negative)
```

### Texture Sampling

```hlsl
// In TextureFX, tex0col is already sampled from Texture0
float4 Filter(float4 tex0col)
{
    // Sample additional textures:
    float4 tex1 = Texture1.Sample(Texturex1Sampler, streams.TexCoord);
    return lerp(tex0col, tex1, 0.5);
}
```

## ShaderFX / ComputeColor Pattern

Composable shader nodes using `compose` keyword:

```hlsl
shader MyTonemap_ShaderFX : ComputeColor, TonemapOperators
{
    compose ComputeColor ColorIn;

    [EnumType("MyNamespace.TonemapOp, MyAssembly")]
    int Operator = 1;

    float Exposure = 0.0;

    override float4 Compute()
    {
        float4 color = ColorIn.Compute();
        color.rgb *= exp2(Exposure);
        color.rgb = ApplyTonemap(color.rgb, Operator);
        return color;
    }
};
```

In vvvv patching, connect a ShaderFX node to a TextureFX's `compose` input to chain processing.

## Mixin Composition — Virtual Method Dispatch

Base shader with a virtual method, overridden by dynamically composed mixins:

```hlsl
// Base shader declares the virtual method
shader ColorProcessorBase
{
    float4 ProcessColor(float4 inPixel) { return inPixel; }
};

// Host shader uses composition
shader ColorTransform_TextureFX : TextureFX
{
    stage compose ColorProcessorBase Processor;

    stage override float4 Shading()
    {
        float4 col = Texture0.SampleLevel(PointSampler, streams.TexCoord, 0);
        return Processor.ProcessColor(col);
    }
};
```

## Template / Generic Shaders

```hlsl
// Declaration with type parameter
shader ComputeColorWave<float Frequency> : ComputeColor, Texturing
{
    override float4 Compute()
    {
        return float4(sin(streams.TexCoord.x * Frequency), 0, 0, 1);
    }
};

// Instantiation via inheritance
shader MyEffect : ComputeColorWave<2.0f> { };
```

Supported template parameter types: `float`, `int`, `float2`, `float3`, `float4`, `Texture2D`, `SamplerState`.

## Composition Arrays

Multiple composed shaders of the same type:

```hlsl
compose ComputeColor lights[];

override float4 Compute()
{
    float4 total = 0;
    foreach (var light in lights)
        total += light.Compute();
    return total;
}
```

## Shared Struct Types Across Shaders

Define once, use in emit/simulate/draw pipeline:

```hlsl
shader ParticleTypes
{
    struct Particle { float3 Position; float3 Velocity; float Life; };
};

shader Emit_ComputeFX : ComputeShaderBase, ParticleTypes { /* fills buffer */ };
shader Simulate_ComputeFX : ComputeShaderBase, ParticleTypes { /* physics */ };
shader Draw_DrawFX : VS_PS_Base, ParticleTypes { /* renders */ };
```

For detailed SDSL syntax rules, see [syntax-rules.md](syntax-rules.md).
