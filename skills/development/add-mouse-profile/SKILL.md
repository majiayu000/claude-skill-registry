---
name: add-mouse-profile
description: Create a new mouse profile for a mouse model not yet supported
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
context: manual
---

# Add Mouse Profile Skill

Create a new mouse profile for MouseMaster.

## When to Use

Use this skill when:
- User wants to add support for a new mouse model
- User has button detection results to formalize
- User provides vendor/product IDs for a mouse

## Steps

1. **Gather Information**
   Ask the user for:
   - Mouse name (e.g., "Logitech MX Master 3S")
   - Vendor name
   - Vendor ID (hex, e.g., "0x046D") - optional
   - Product IDs (hex array) - optional
   - Number of buttons

2. **Create Profile ID**
   Generate from name: lowercase, underscores for spaces
   Example: "Logitech MX Master 3S" -> "logitech_mx_master_3s"

3. **Define Buttons**
   For each button, define:
   ```json
   {
     "id": "button_id",
     "name": "Human Name",
     "qtButton": <qt_code>,
     "remappable": true/false,
     "defaultAction": "action_id"  // optional
   }
   ```

   Standard Qt button codes:
   - 1: Left Click (not remappable)
   - 2: Right Click (not remappable)
   - 4: Middle Click
   - 8: Back/Button 4
   - 16: Forward/Button 5
   - 32: Extra Button 1
   - 64: Extra Button 2

4. **Create JSON File**
   Write to: `MouseMaster/Resources/MouseDefinitions/<profile_id>.json`

   ```json
   {
     "id": "<profile_id>",
     "name": "<mouse_name>",
     "vendor": "<vendor>",
     "vendorId": "<vendor_id>",
     "productIds": ["<product_id>"],
     "buttons": [...],
     "features": {
       "horizontalScroll": false,
       "thumbWheel": false,
       "gestureButton": false
     }
   }
   ```

5. **Create Default Preset**
   Write to: `presets/builtin/default_<profile_id>.json`

   ```json
   {
     "id": "default_<profile_id>",
     "name": "<mouse_name> Default",
     "version": "1.0",
     "mouseId": "<profile_id>",
     "mappings": {
       "middle": {"action": "view_reset_3d"},
       "back": {"action": "edit_undo"},
       "forward": {"action": "edit_redo"}
     },
     "contextMappings": {}
   }
   ```

6. **Update Documentation**
   Add to README.md supported mice table:
   ```markdown
   | <Mouse Name> | <Vendor ID> | <Button Count> | Fully Supported |
   ```

## Example Interaction

User: "Add support for Razer DeathAdder V3"

Claude:
1. Creates `logitech_razer_deathadder_v3.json` in MouseDefinitions
2. Creates `default_razer_deathadder_v3.json` in presets/builtin
3. Updates README.md supported mice table
4. Confirms creation with file paths

## Validation

After creating files:
- Verify JSON is valid
- Verify all required fields present
- Verify button IDs are unique
- Verify preset mouseId matches profile id
