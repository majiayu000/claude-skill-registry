---
name: shader-programming
cluster: game-dev
description: "Writing and optimizing GLSL or HLSL shaders for real-time graphics rendering in game engines."
tags: ["shaders","glsl","hlsl","graphics-programming","game-dev"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "shader programming glsl hlsl graphics rendering game development"
---

## Purpose

This skill allows OpenClaw to generate, optimize, and debug GLSL or HLSL shaders for real-time graphics in game engines. It focuses on tasks like writing vertex, fragment, or compute shaders, ensuring compatibility with APIs like OpenGL, Vulkan, or DirectX.

## When to Use

Use this skill when users request custom shaders for visual effects, performance tweaks, or integration with game engines. Specifically:
- Optimizing shaders for mobile games to reduce GPU load (e.g., minimizing texture samples).
- Creating advanced effects like water rendering or post-processing in tools like Unity or Unreal.
- Debugging shader code during game development iterations.

## Key Capabilities

- Generate complete GLSL/HLSL code snippets based on user specs (e.g., shader type, inputs, outputs).
- Optimize shaders by analyzing and modifying code for better performance, such as reducing instructions or using precision qualifiers.
- Debug common issues like compilation errors or runtime artifacts by suggesting fixes.
- Support shader versions like GLSL 330 or HLSL 5.0, with checks for hardware compatibility.

## Usage Patterns

To invoke this skill in OpenClaw, use the command: `openclaw execute shader-programming --task <task-type> --input <details>`. Always specify the shader language (e.g., --lang glsl) and target platform (e.g., --platform vulkan). For code generation, provide a JSON config like: {"type": "vertex", "inputs": ["position", "normal"], "outputs": ["gl_Position"]}. Follow this pattern:
- Start with a clear task: e.g., `openclaw execute shader-programming --task generate --lang hlsl --input '{"features": ["lighting"]}'`.
- For optimization, pipe existing code: e.g., echo "existing shader code" | openclaw execute shader-programming --task optimize --lang glsl.
- If authentication is needed (e.g., for external compilers), set $OPENCLAW_API_KEY in your environment before running commands.

## Common Commands/API

Use these OpenClaw-integrated commands for shader tasks:
- Compile GLSL shaders: Run `glslangValidator -V -o output.spv input.vert` via OpenClaw's subprocess, e.g., `openclaw execute shader-programming --subprocess "glslangValidator -V -o myShader.spv myShader.vert"`.
- Compile HLSL shaders: Use `fxc /T vs_5_0 /E MainVS /Fo compiled.bin input.hlsl`, invoked as `openclaw execute shader-programming --subprocess "fxc /T vs_5_0 /E MainVS /Fo output.bin input.hlsl"`.
- API endpoints: POST to OpenClaw's /api/shader/generate with JSON payload, e.g., curl -H "Authorization: Bearer $OPENCLAW_API_KEY" -d '{"lang": "glsl", "type": "fragment"}' https://api.openclaw.com/api/shader/generate.
- Config formats: Use JSON for inputs, e.g., {"shader": {"version": "330", "precision": "highp float"}}. For error checks, include flags like --validate in commands, e.g., `openclaw execute shader-programming --task validate --input "shader code" --flags "--validate"`.

## Integration Notes

Integrate this skill by embedding generated shaders into your project workflow. For Unity, save GLSL/HLSL files in the Assets/Shaders directory and reference them in materials. In Unreal, use the .usf format for HLSL. Always wrap OpenClaw calls in a script, e.g., in Python: import subprocess; subprocess.run(["openclaw", "execute", "shader-programming", "--task", "generate", "--lang", "glsl"]). For cross-engine compatibility, specify profiles in configs (e.g., {"profile": "gles3"} for mobile). If using external tools, ensure $OPENCLAW_API_KEY is set for authenticated API calls to avoid failures.

## Error Handling

Handle shader errors by parsing compiler output. For GLSL, check glslangValidator logs for patterns like "ERROR: 0:5: 'undeclared identifier'", then suggest fixes, e.g., add missing variables. In code: try { subprocess.run(["glslangValidator", "-V", "input.vert"]) } catch e { print(e.stderr); if "syntax error" in e.stderr: return "Fix line 5 with correct syntax" }. For HLSL, fxc errors like "error X3004: undeclared identifier" require redeclaring variables. Use OpenClaw's built-in validation: `openclaw execute shader-programming --task debug --input "shader code"`, which returns JSON like {"errors": ["Line 10: missing semicolon"]}. Always log errors with timestamps and retry with corrected inputs.

## Concrete Usage Examples

1. Generate a basic GLSL vertex shader for a simple 3D object: Use `openclaw execute shader-programming --task generate --lang glsl --input '{"type": "vertex", "inputs": ["vec3 position"]}'`. This produces: attribute vec3 aPosition; void main() { gl_Position = vec4(aPosition, 1.0); }
   
2. Optimize an existing HLSL fragment shader for performance: Run `openclaw execute shader-programming --task optimize --lang hlsl --input "float4 PSMain(float2 uv : TEXCOORD) : SV_Target { return float4(uv, 0.0, 1.0); }"`. Output might be: float4 PSMain(float2 uv : TEXCOORD) : SV_Target { return float4(uv.x, uv.y, 0.0, 1.0); } // Optimized by inlining.

## Graph Relationships

- Related to: game-dev cluster (e.g., shares nodes with graphics-programming for rendering pipelines).
- Links to: graphics-programming (for broader API integration), rendering-engines (for engine-specific shader hooks), and performance-optimization (for shader tuning techniques).
