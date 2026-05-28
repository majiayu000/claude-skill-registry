---
name: scrcpy-option-ui-builder
description: This skill should modify the category screens and add the requested scrcpy options to the UI, depending on the type of the option (text, toggle, dropdown, etc.). Use this skill for adding new scrcpy options in the UI.
---

# Scrcpy option UI builder

Working directory: [/lib/presentation/scrcpy_config/](/lib/presentation/scrcpy_config/)

UI option screens are present in `@lib/presentation/scrcpy_config`.

Common, re-usable widgets are present in `@lib/presentation/scrcpy_config/widgets`.

## Steps

1. Gather information
2. Extend or create UI code in the `<category_screen>.dart` file
3. Create necessary translations for the the UI Control

## 1. Gather information

- Refer to [/docs/scrcpy_options](/docs/scrcpy_options) to find information about the scrcpy option (Argument, name,
  description, is advanced).
- Find the corresponding argument class
  in [/lib/application/model/scrcpy/arguments/](/lib/application/model/scrcpy/arguments/)
- If the argument class doesn't exist, first create it
  using [this skill](/.claude/skills/scrcpy-cli-argument-to-code-mapper)
- Use this argument class in the UI code to get existing value and to update it.

## 2. Create `<category_screen>.dart`

- Refer to [/lib/presentation/scrcpy_config/video_screen.dart](/lib/presentation/scrcpy_config/video/video_screen.dart)
- Create a similar scrollable screen with necessary dependencies for the new category screen.
- Create a new route inside [routes.dart](/lib/routes.dart)
- Introduce new `NavigationPaneItem` inside [home_screen.dart](/lib/presentation/home/home_screen.dart) using the new route
- Follow the next section to extend the screen code with UI controls.

## 2. Extend existing UI Code

- If the `<category_screen>.dart` file for requested scrcpy option and the respective category already exists, then
  extend the Scrollable `Column`, with the new control(s)
-
Use [/lib/presentation/scrcpy_config/widgets/config_item.dart](/lib/presentation/scrcpy_config/widgets/config_item.dart)
for wrapping the actual UI control.
- The `ConfigItem` widget expects:

1. `label` (key and translation label) to show title, description and argument tooltip.
2. `child` the actual control widget (toggle/switch/text input/comboBox/etc.)

- Use [`ConfigTextBox`](/lib/presentation/scrcpy_config/widgets/config_text_box.dart) for text input controls

## 3. Create translations

- Currently, the project only supports english language.
- The translation file is present [here](/assets/i18n/en.json)
- Refer to the existing translations under this path inside the JSON: e.g. `confg/video/noVideo`
- Expected path: `config/<category>/<argument.label>`
- Required translations: `title`, `description`, `arg`
- Optional: `default` (default value for the control e.g. for comboBox)
