---
name: new-plugin
description: Create a new iPlug2 plugin project by duplicating TemplateProject in the iPlug2OOS repository
---

# Create New Plugin (iPlug2OOS)

Use this skill when the user wants to create a new plugin project in this out-of-source repository.

## Workflow

1. **Gather project details:**
   - **Plugin name** (required): No spaces or special characters
   - **Manufacturer name** (required): No spaces

2. **Check for existing projects:**
   - If other project folders exist besides TemplateProject, ask if user wants to continue with existing work or create new

3. **Run duplicate script:**
   ```bash
   ./duplicate.py TemplateProject [PluginName] [ManufacturerName]
   ```

4. **Offer config.h customization:**
   - `PLUG_UNIQUE_ID` - Verify the auto-generated 4-char ID
   - `PLUG_MFR_ID` - Set manufacturer's 4-char ID
   - Copyright, URLs - allow skipping for later

5. **Ask about committing:**
   ```bash
   git add [PluginName]/*
   git add .vscode/*
   git add .github/*
   git add bump_version.py
   git commit -m "created [PluginName] based on TemplateProject"
   ```

6. **Next steps:**
   - Open in Xcode: `open [PluginName]/[PluginName].xcworkspace`
   - Build: Use the `build` skill from iPlug2
   - Setup SDKs: Use the `setup-deps` skill if needed

## Example

```bash
./duplicate.py TemplateProject MySynth MyBrand
```

Creates `MySynth/` with all project files configured and ready to build.
