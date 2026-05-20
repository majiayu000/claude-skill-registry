---
name: export-preset
description: Help user export a preset configuration for sharing or backup
allowed-tools:
  - Read
  - Bash
context: manual
---

# Export Preset Skill

Help user export a preset for sharing.

## When to Use

Use this skill when:
- User wants to share their preset configuration
- User needs to backup their presets
- User wants to contribute a preset to the community

## Steps

1. **Identify Preset to Export**
   Ask user which preset they want to export:
   - By name
   - By file path if they know it
   - Show available presets from `presets/builtin/` and user directory

2. **Validate Preset**
   Check the preset JSON for:
   - Required fields: id, name, version, mouseId, mappings
   - Valid action references
   - Proper JSON syntax

3. **Prepare for Sharing**
   If sharing publicly, suggest:
   - Add descriptive `description` field
   - Add `author` field with attribution
   - Remove any personal/sensitive data
   - Add comments about intended workflow

4. **Export Options**

   **Option A: File Export**
   ```python
   # In Slicer console
   import json
   from pathlib import Path

   preset_path = Path("~/.slicer/MouseMaster/presets/my_preset.json").expanduser()
   export_path = Path("~/Desktop/my_preset.json").expanduser()

   with open(preset_path) as f:
       preset = json.load(f)

   # Add metadata
   preset["author"] = "Your Name"
   preset["description"] = "Description of workflow"

   with open(export_path, "w") as f:
       json.dump(preset, f, indent=2)

   print(f"Exported to {export_path}")
   ```

   **Option B: Clipboard Copy**
   ```python
   import json
   import qt

   with open(preset_path) as f:
       preset = json.load(f)

   clipboard = qt.QApplication.clipboard()
   clipboard.setText(json.dumps(preset, indent=2))
   print("Preset copied to clipboard")
   ```

5. **Sharing Instructions**

   For GitHub Discussion submission:
   ```markdown
   ## Preset: [Name]

   **Mouse**: [Mouse Model]
   **Workflow**: [Description of what this preset is optimized for]

   ### Mappings
   - Back: [Action]
   - Forward: [Action]
   - ...

   ### Attached File
   [my_preset.json]

   ### Screenshots
   [Optional: show the workflow in action]
   ```

## Preset Validation Checklist

- [ ] Has unique `id`
- [ ] Has descriptive `name`
- [ ] Has `version` field (use "1.0")
- [ ] `mouseId` matches a valid profile
- [ ] All `action` values are valid action IDs
- [ ] No empty mappings
- [ ] JSON syntax is valid

## Example Preset Structure

```json
{
  "id": "segmentation_optimized",
  "name": "Segmentation Optimized",
  "version": "1.0",
  "mouseId": "logitech_mx_master_3s",
  "author": "Username",
  "description": "Optimized for fast segmentation with segment navigation on thumb buttons",
  "mappings": {
    "back": {"action": "segment_previous"},
    "forward": {"action": "segment_next"},
    "thumb": {"action": "segment_editor_paint"}
  },
  "contextMappings": {
    "SegmentEditor": {
      "middle": {"action": "view_center_crosshair"}
    }
  }
}
```

## Common Issues

**"mouseId not found"**
- Ensure the mouse profile exists
- Use exact ID from Resources/MouseDefinitions/

**"Invalid action"**
- Check action ID spelling
- Verify action is registered in ActionRegistry
