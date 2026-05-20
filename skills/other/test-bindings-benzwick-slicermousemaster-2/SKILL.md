---
name: test-bindings
description: Interactively test mouse button bindings in Slicer
allowed-tools:
  - Read
context: manual
---

# Test Bindings Skill

Interactively test mouse button bindings in Slicer.

## When to Use

Use this skill when:
- User wants to verify their bindings work
- User is debugging why a binding isn't triggering
- User wants to see what actions are available

## Steps

1. **Check MouseMaster Status**
   Provide code to check if MouseMaster is active:

   ```python
   import slicer

   try:
       mm = slicer.modules.mousemaster
       widget = slicer.modules.MouseMasterWidget
       print("MouseMaster module loaded")

       # Check if logic is initialized
       if hasattr(widget, 'logic') and widget.logic:
           if widget.logic.is_active():
               print("Event handler: ACTIVE")
           else:
               print("Event handler: INACTIVE")
               print("Click 'Enable' in the module panel to activate")
       else:
           print("Logic not initialized - open the module first")
   except:
       print("MouseMaster not loaded - check Extensions Manager")
   ```

2. **List Current Bindings**
   Show the current preset configuration:

   ```python
   # Get current preset
   logic = slicer.modules.MouseMasterWidget.logic
   preset = logic.get_current_preset()
   mouse = logic.get_current_mouse()

   if preset and mouse:
       print(f"Mouse: {mouse.name}")
       print(f"Preset: {preset.name}")
       print("\nDefault Mappings:")
       for button_id, mapping in preset.mappings.items():
           button = mouse.get_button(button_id)
           name = button.name if button else button_id
           print(f"  {name}: {mapping.action}")

       print("\nContext Mappings:")
       for context, mappings in preset.context_mappings.items():
           print(f"  {context}:")
           for button_id, mapping in mappings.items():
               print(f"    {button_id}: {mapping.action}")
   else:
       print("No preset or mouse selected")
   ```

3. **Test Individual Action**
   Manually trigger an action to verify it works:

   ```python
   from MouseMasterLib.action_registry import ActionRegistry, ActionContext

   registry = ActionRegistry.get_instance()

   # List available actions
   print("Available actions:")
   for action in registry.get_all_actions():
       print(f"  {action.id}: {action.description}")

   # Test specific action
   context = ActionContext(module_name="Welcome")
   result = registry.execute("edit_undo", context)
   print(f"Action executed: {result}")
   ```

4. **Monitor Button Presses**
   Set up real-time monitoring:

   ```python
   def on_button_press(button_id, context):
       print(f"Button: {button_id}, Context: {context}")

   handler = slicer.modules.MouseMasterWidget.logic._event_handler
   handler.set_on_button_press(on_button_press)
   print("Monitoring active. Press buttons to see output.")
   print("Run: handler.set_on_button_press(None) to stop")
   ```

5. **Debug Specific Binding**
   If a binding isn't working:

   ```python
   # Check if button is in profile
   mouse = logic.get_current_mouse()
   button = mouse.get_button("back")
   if button:
       print(f"Button found: {button.name}, Qt code: {button.qt_button}")
       print(f"Remappable: {button.remappable}")
   else:
       print("Button not found in profile")

   # Check if mapping exists
   preset = logic.get_current_preset()
   mapping = preset.get_mapping("back")
   if mapping:
       print(f"Mapping: {mapping.action}")
   else:
       print("No mapping defined")

   # Check if action exists
   registry = ActionRegistry.get_instance()
   action = registry.get_action(mapping.action if mapping else "unknown")
   if action:
       print(f"Action found: {action.description}")
   else:
       print("Action not registered")
   ```

## Common Issues

### Button Press Not Detected

1. Check handler is installed:
   ```python
   print(logic._event_handler.is_installed)
   ```

2. Check handler is enabled:
   ```python
   print(logic._event_handler.is_enabled)
   ```

3. Check Qt button code is in profile

### Action Not Executing

1. Verify action is registered:
   ```python
   print(registry.get_action("action_id"))
   ```

2. Check action availability:
   ```python
   context = ActionContext(module_name="SegmentEditor")
   action = registry.get_action("segment_next")
   print(action.handler.is_available(context))
   ```

### Context Not Detected

1. Check current module:
   ```python
   print(slicer.app.moduleManager().currentModule())
   ```

2. Verify context name in preset matches exactly

## Troubleshooting Checklist

- [ ] MouseMaster module is loaded
- [ ] Logic is initialized
- [ ] Event handler is installed
- [ ] Event handler is enabled
- [ ] Mouse profile is selected
- [ ] Preset is selected
- [ ] Button is in mouse profile
- [ ] Mapping exists for button
- [ ] Action is registered
- [ ] Action is available in current context
