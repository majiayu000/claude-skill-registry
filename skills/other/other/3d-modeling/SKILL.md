---
name: 3d-modeling
cluster: ar-vr
description: "Skill for creating and editing 3D models using software like Blender for AR/VR applications."
tags: ["3d-modeling","blender","ar-vr"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "3d modeling blender ar vr mesh rendering"
---

# 3d-modeling

## Purpose
This skill provides tools for creating, editing, and optimizing 3D models using Blender, specifically tailored for AR/VR applications. It focuses on generating assets like meshes and textures that integrate seamlessly into virtual environments.

## When to Use
Use this skill when developing AR/VR prototypes that require custom 3D models, such as designing interactive objects for VR simulations or overlaying digital assets in AR scenes. Apply it in workflows involving asset creation, modification, or export for platforms like Unity or Oculus.

## Key Capabilities
- Create and manipulate 3D meshes using Blender's Python API, e.g., generating a cube with `bpy.ops.mesh.primitive_cube_add()`.
- Apply materials and textures for AR/VR realism, such as using `bpy.data.materials.new()` to add shaders.
- Render scenes optimized for AR/VR, including exporting to GLTF format with embedded textures via `bpy.ops.export_scene.gltf()`.
- Perform batch operations via CLI for automation, like processing multiple files.
- Integrate with AR/VR tools by exporting models that support real-time rendering, such as low-poly meshes for mobile VR.

## Usage Patterns
Follow these patterns to leverage the skill effectively. Always run Blender in a compatible environment with Python 3.7+ installed.

1. **Basic Model Creation:** Start by launching Blender from the command line and scripting a simple object. Use this for quick AR prototypes.
   - Example: Create a cube and export it as GLTF for AR integration.
     ```
     import bpy
     bpy.ops.mesh.primitive_cube_add(size=2, location=(0,0,0))
     bpy.ops.export_scene.gltf(filepath="cube.gltf")
     ```

2. **Model Editing for VR:** Import an existing model, apply modifications, and optimize for VR performance.
   - Example: Load a mesh, reduce polygons, and export for VR headset compatibility.
     ```
     import bpy
     bpy.ops.import_scene.obj(filepath="model.obj")
     bpy.ops.object.modifier_add(type='DECIMATE')
     bpy.ops.export_scene.gltf(filepath="optimized_model.gltf", export_format='GLTF_SEPARATE')
     ```

For complex tasks, wrap these in scripts and run via Blender's CLI to automate AR/VR asset pipelines.

## Common Commands/API
Use Blender's CLI and Python API for core operations. Specify exact flags for efficiency.

- **CLI Commands:** Run scripts in background mode.
  - `blender --background input.blend --python script.py --render-output output.png`: Loads a file, runs a script, and renders an image for AR previews.
  - `blender -b file.blend -P script.py -F PNG -o //render_`: Executes a script on a blend file and outputs renders; use `-F` for format like PNG for VR thumbnails.

- **Python API Snippets:** Access via `bpy` module in Blender scripts.
  - Snippet for adding a material:
    ```
    mat = bpy.data.materials.new("AR_Material")
    mat.diffuse_color = (1, 0, 0, 1)  # Red color for AR visibility
    ```
  - Snippet for mesh manipulation:
    ```
    obj = bpy.context.active_object
    obj.scale = (1.5, 1.5, 1.5)  # Scale object for VR fitting
    ```

Config formats: Use JSON-like structures in Blender files (.blend) for custom properties, e.g., add via `bpy.types.Scene.my_prop = "value"`. For exports, specify GLTF options in scripts, like `export_extras=True` for metadata.

## Integration Notes
Integrate this skill with AR/VR frameworks by exporting models in compatible formats. For external services (e.g., cloud rendering), use environment variables for authentication, such as `$BLENDER_API_KEY` if accessing paid APIs, though Blender itself is local. Pattern: Set `export os.environ['BLENDER_API_KEY'] = 'your_key'` in scripts before API calls. Ensure dependencies like Python packages (e.g., `bpy`) are installed via `pip install bpy` if using external editors. For AR/VR platforms, import GLTF files directly into Unity or Unreal, matching coordinate systems (e.g., Z-up for Blender).

## Error Handling
Anticipate and handle errors in scripts to maintain AR/VR workflow reliability. Check for file existence before imports: Use `if not bpy.data.filepath: raise ValueError("File not found")`. For API failures, like failed exports, catch exceptions: 
```
try:
    bpy.ops.export_scene.gltf(filepath="output.gltf")
except RuntimeError as e:
    print(f"Export failed: {e}")  # Log and retry or fallback
```
Common issues: Invalid paths (use absolute paths), memory errors on large models (optimize with decimate modifier first), or version mismatches (ensure Blender 2.8+). Always test scripts in a non-destructive environment.

## Graph Relationships
- Belongs to cluster: ar-vr
- Related tags: 3d-modeling, blender, ar-vr
- Connected skills: rendering (for post-processing AR/VR assets), mesh-optimization (for performance in VR)
