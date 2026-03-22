---
name: stride-shader-asset-workflow
description: Use when adding, renaming, or debugging Stride SDSL shader files (`*.sdsl`) in a Stride project. Enforces the correct shader registration workflow across `.sdpkg` asset folders, `.csproj` linked shader items, generated shader key files (`*.sdsl.cs`), and forced Stride asset rebuild targets before runtime shader debugging, so agents do not misdiagnose stale asset database/module errors as shader code errors.
license: CC-BY-SA-4.0
compatibility: Designed for coding AI agents assisting with Stride development
metadata:
  author: Tebjan Halm
  version: "1.0"
---

# Stride Shader Asset Workflow

## Overview

This skill defines the correct workflow for adding, updating, and debugging Stride shader files (`*.sdsl`) in C# projects.

It helps agents verify project setup, generated shader key files, and Stride asset compilation steps.

## When To Use

- Adding a new Stride shader file (`*.sdsl`) of any kind (compute, material/mixin, effect-related, or custom shader classes)
- Renaming/moving shader files
- Adding/changing shader parameters and needing updated generated C# key files (`*.sdsl.cs`)
- Seeing Stride shader errors like `E1202 ... mixin ... is not in the module`
- Seeing runtime behavior that suggests a new shader is not being loaded
- Working in projects that use both `.sdpkg` asset folders and explicit `.csproj` shader links

## Default Stride Template Layout (Usual Case)

In a standard Stride game created from the template, shader files are usually placed in an `Effects` folder next to the platform-independent game core project (`<GameName>.csproj`), for example:

- `<SolutionRoot>/<GameName>/<GameName>.csproj`
- `<SolutionRoot>/<GameName>/Effects/*.sdsl`
- `<SolutionRoot>/<GameName>/<GameName>.sdpkg`

Typical template behavior:

- `<GameName>.sdpkg` includes `AssetFolders` for both `Assets` and `Effects`
- The core game `.csproj` often has **no explicit shader item entries**
- Shader files are picked up via SDK-style default items (`None`) + Stride's default target metadata (`None Update="**\*.sdsl" Generator="StrideShaderKeyGenerator"`)

Practical implication:

- If you are working inside a normal template game project and shaders live under the project folder (for example `Effects/`), you usually do **not** need explicit `.csproj` shader link items.
- The explicit linked/wildcard `.csproj` patterns in this skill are mainly for:
  - shared external shader folders (for example `..\..\shaders`)
  - runner/test projects
  - non-template layouts

## Generated Shader Keys (Use These, Not String Keys)

Stride has a built-in shader key generator for `.sdsl` files:

- VS custom tool: `StrideShaderKeyGenerator`
- Output: `*.sdsl.cs`
- Generated class pattern: `<ShaderName>Keys`

Use generated keys in C# when possible instead of string-based `ParameterKeys.FindByName(...)`/manual names.

Why:

- Prevents binding bugs from wrong names or missing qualification (for example `Width` vs `MyShader.Width`)
- Keeps parameter bindings in sync when shader parameters change

## Important Trap: `None` vs `Content` Shader Items

Stride's default targets auto-apply the shader key generator to:

- `None Update="**\\*.sdsl" Generator="StrideShaderKeyGenerator"`

If your project links shaders as `Content` items (common in runner/test projects), you might **not** get automatic key generation unless you set generator metadata explicitly on those linked items.

For linked shaders in a C# project (especially external/shared shader folders), prefer `None` items (so the default Stride metadata pattern matches), and set the generator explicitly anyway.

Preferred scalable pattern (works with subfolders):

```xml
<ItemGroup>
  <None Include="..\\..\\shaders\\**\\*.sdsl"
        Link="Assets\\%(RecursiveDir)%(Filename)%(Extension)"
        Generator="StrideShaderKeyGenerator" />
</ItemGroup>

<ItemGroup>
  <Compile Include="..\\..\\shaders\\**\\*.sdsl.cs"
           Link="Assets\\Generated\\%(RecursiveDir)%(Filename)%(Extension)"
           Visible="false"
           AutoGen="True"
           DesignTime="True" />
</ItemGroup>
```

Notes:

- `Generator="StrideShaderKeyGenerator"` is the VS/custom-tool hook that produces `*.sdsl.cs`.
- The recursive wildcard patterns (`..\\..\\shaders\\**\\*.sdsl` and `..\\..\\shaders\\**\\*.sdsl.cs`) keep the project file small and automatically pick up new shaders/subfolders.
- The `Compile Include="..\\..\\shaders\\**\\*.sdsl.cs"` pattern ensures generated key files are compiled when working in CLI/agent workflows and linked shader layouts.
- If a project intentionally uses `Content` for linked shaders, `Generator="StrideShaderKeyGenerator"` must be set explicitly on each shader item.
- This wildcard setup was validated in a Stride runner project with:
  - `StrideAssetUpdateGeneratedFiles`
  - `StrideCleanAsset`
  - `StrideCompileAsset`
  - a real GPU roundtrip run (compress + low-level decompressor fallback + verify pass)

## C# Project Setup (Required for CLI/Agent Workflows)

In addition to `Stride.Engine` / `Stride.Rendering`, ensure the project has the asset compiler targets available (directly or transitively). In standalone runner/test projects, adding this package explicitly makes the CLI targets available:

```xml
<PackageReference Include="Stride.Core.Assets.CompilerApp" Version="4.3.x">
  <PrivateAssets>all</PrivateAssets>
  <IncludeAssets>build;buildTransitive</IncludeAssets>
</PackageReference>
```

Without the asset compiler targets, `StrideAssetUpdateGeneratedFiles`, `StrideCleanAsset`, and `StrideCompileAsset` may be unavailable.

## Workflow (Do This In Order)

1. Add the shader file to the repository.

- Example: `shaders/MyPass.sdsl`

2. Verify the Stride package includes the folder that contains the shader.

- Check `<project>.sdpkg` `AssetFolders`.
- Example valid entry:

```yaml
AssetFolders:
  - Path: !dir ../../shaders
```

3. If the project also links shader files in the `.csproj`, add the new shader there too.

- This is easy to miss and can cause "mixin not in module" even if `.sdpkg` looks correct.
- Prefer linked `None` items for shaders (not `Content`) and set `Generator="StrideShaderKeyGenerator"` so `*.sdsl.cs` key files regenerate.
- Ensure generated `*.sdsl.cs` files are compiled (prefer recursive wildcard `Compile Include` pattern).
- Example pattern:

```xml
<None Include="..\..\shaders\**\*.sdsl"
      Link="Assets\%(RecursiveDir)%(Filename)%(Extension)"
      Generator="StrideShaderKeyGenerator" />

<Compile Include="..\..\shaders\**\*.sdsl.cs"
         Link="Assets\Generated\%(RecursiveDir)%(Filename)%(Extension)"
         Visible="false"
         AutoGen="True"
         DesignTime="True" />
```

4. Refresh generated shader key files (especially in agent/CLI workflows, outside VS).

- In current Stride NuGet targets, `StrideAssetUpdateGeneratedFiles` is a standalone target and may require `_StridePrepareAssetCompiler` first when invoked directly.
- Run (PowerShell-safe quoted `/t:` form):

```powershell
dotnet msbuild src/MyStrideApp/MyStrideApp.csproj "/t:_StridePrepareAssetCompiler;StrideAssetUpdateGeneratedFiles" /p:Configuration=Debug
```

5. Force a Stride asset rebuild (do not trust normal `dotnet build` up-to-date checks).

- Run these targets explicitly:

```powershell
dotnet msbuild src/MyStrideApp/MyStrideApp.csproj /t:StrideCleanAsset /p:Configuration=Debug
dotnet msbuild src/MyStrideApp/MyStrideApp.csproj /t:StrideCompileAsset /p:Configuration=Debug
```

6. Build and run only after the asset rebuild.

```powershell
dotnet build src/MyStrideApp/MyStrideApp.csproj -c Debug
dotnet run --project src/MyStrideApp/MyStrideApp.csproj -c Debug
```

7. If still failing, then debug shader code/runtime bindings.

- At this point, errors are more likely real shader syntax/semantics/binding issues.

## Failure Signatures (Interpretation)

- `E1202: The mixin [X] ... is not in the module`
- Meaning:
  - Shader not included in Stride asset module yet (stale asset DB), or
  - Shader file not reachable via `.sdpkg` `AssetFolders`, or
  - Shader file not linked in `.csproj` when the project relies on explicit linked shader `Content`
- Action:
  - Re-run the workflow above from step 2, especially steps 3-4

- Stride asset build says many items are `up-to-date` but new shader still missing
- Meaning:
  - Up-to-date inputs did not include your new shader path (or cache state is stale)
- Action:
  - Run `StrideCleanAsset` then `StrideCompileAsset`

- C# bindings suddenly stop working after shader parameter rename/addition
- Meaning:
  - Generated `*.sdsl.cs` keys are stale or missing, or code is using string keys manually
- Action:
  - Run `_StridePrepareAssetCompiler;StrideAssetUpdateGeneratedFiles`
  - Prefer generated `<ShaderName>Keys` over string key lookup

- Generated `*.sdsl.cs` fails to compile on a shader `float` default value
- Meaning:
  - The shader default literal was written as `100.0` (double-like in generated C#) and the generated key file emits `ParameterKeys.NewValue<float>(100.0)`
- Action:
  - Write explicit float literals in SDSL defaults (for example `100.0f`)
  - Re-run generated-file update target

## Agent Rules (Preventing Workarounds Too Early)

- Do not add low-level D3D/SharpDX shader dispatch workarounds for a newly-added shader until the explicit Stride asset rebuild workflow has been executed.
- Always inspect both:
  - `.sdpkg` `AssetFolders`
  - `.csproj` linked shader `Content` items (if present in that project)
- Prefer generated `*.sdsl.cs` key classes for parameter binding; avoid string keys unless necessary.
- When reporting results, state whether `StrideAssetUpdateGeneratedFiles`, `StrideCleanAsset`, and `StrideCompileAsset` were run.

## Quick Checklist

- `.sdsl` file exists
- `.sdpkg` asset folder includes its directory
- `.csproj` links the shader (if project uses linked shader `Content`)
- `.csproj` uses linked `None` shader items (preferred) or explicit generator metadata on linked shader items
- `Generator="StrideShaderKeyGenerator"` set on linked shader items
- `Compile Include="..\\..\\shaders\\**\\*.sdsl.cs"` (or equivalent) present so generated keys compile
- `_StridePrepareAssetCompiler;StrideAssetUpdateGeneratedFiles` run after shader changes
- `StrideCleanAsset` run
- `StrideCompileAsset` run
- `dotnet build` / `dotnet run` run after asset rebuild
