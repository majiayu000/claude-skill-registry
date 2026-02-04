---
name: script-kit-prompts
description: Prompt system and form handling for script-kit-gpui
---

# script-kit-prompts

The prompts system provides native GPUI UI components for interactive user input in Script Kit scripts. Scripts communicate with the UI via IPC messages, showing various prompt types that collect and return user input.

## Architecture Overview

```
Script (Node.js)                    GPUI App
     |                                  |
     |-- IPC Message: ShowArg --------->|
     |                                  |-- Create prompt entity
     |                                  |-- Render with theme/design
     |                                  |-- Handle user input
     |<-- IPC Response: Submit ---------|
     |                                  |
```

### Message Flow

1. **Script sends prompt message** via IPC (e.g., `ShowArg`, `ShowDiv`, `ShowForm`)
2. **`prompt_handler.rs`** routes to `handle_prompt_message()` in `ScriptListApp`
3. **Creates appropriate `AppView` variant** with entity if needed
4. **Renders prompt** using design tokens and theme colors
5. **User interacts** - input, selection, keyboard shortcuts
6. **Submits response** back to script via `response_sender` channel

## Key Types

### PromptBase (`prompts/base.rs`)

Shared infrastructure for all prompt types:

```rust
pub struct PromptBase {
    pub id: String,              // Unique prompt instance ID
    pub focus_handle: FocusHandle, // GPUI focus management
    pub on_submit: SubmitCallback, // Called on submit/cancel
    pub theme: Arc<theme::Theme>,  // Theme for Default variant
    pub design_variant: DesignVariant, // Design system variant
}
```

**Usage pattern:**
```rust
impl Render for MyPrompt {
    fn render(&mut self, window: &mut Window, cx: &mut Context<Self>) -> impl IntoElement {
        let dc = DesignContext::new(&self.base.theme, self.base.design_variant);
        // Use dc.bg_main(), dc.text_secondary(), etc.
    }
}
```

### DesignContext

Resolves colors based on design variant, eliminating branching in render code:

```rust
let dc = DesignContext::new(&theme, DesignVariant::Default);
dc.bg_main()      // Primary background
dc.bg_secondary() // Search boxes, panels
dc.text_primary() // Main text
dc.text_muted()   // Placeholders, hints
dc.accent()       // Links, highlights
dc.bg_selected()  // Selected item background
```

### SubmitCallback

Standard callback signature for all prompts:

```rust
pub type SubmitCallback = Arc<dyn Fn(String, Option<String>) + Send + Sync>;
// Parameters: (prompt_id: String, value: Option<String>)
// value = None means cancelled/escaped
```

## Prompt Types

### ArgPrompt (render_prompts/arg.rs)

**Purpose:** Single-line text input with optional choice list

**Features:**
- Text input with cursor and selection
- Filterable choice list (virtualized via `uniform_list`)
- Keyboard navigation (up/down arrows)
- Cmd+K actions popup
- SDK action shortcuts

**Message:** `ShowArg { id, placeholder, choices, actions }`

**Submits:** Selected choice value OR typed text

### DivPrompt (prompts/div.rs)

**Purpose:** Display HTML content with optional interactivity

**Features:**
- Parses HTML to native GPUI elements via `parse_html()`
- Supports: headers, paragraphs, bold, italic, code, lists, blockquotes, links
- Tailwind class support via `TailwindStyles`
- `submit:value` links for interactive submissions
- Container customization (background, padding, opacity)

**Message:** `ShowDiv { id, html, container_classes, container_bg, container_padding, opacity, ... }`

**Submits:** None (acknowledgment) or link-specified value

### FormPrompt (form_prompt.rs + form_parser.rs)

**Purpose:** Multi-field form with various input types

**Components:**
- `FormPromptState` - Holds parsed fields and their entities
- `FormFieldEntity` - Enum wrapping TextField/TextArea/Checkbox entities
- `form_parser::parse_form_html()` - Extracts form fields from HTML

**Supported Input Types:**
- `text`, `password`, `email`, `number` -> FormTextField
- `textarea` -> FormTextArea
- `checkbox` -> FormCheckbox
- `select` -> (extracted but basic support)

**Features:**
- Tab navigation between fields
- Delegated focus (returns focused field's handle, not container's)
- Unified keyboard handling via `handle_key_input()`

**Message:** `ShowForm { id, html, actions }`

**Submits:** JSON object `{"field_name": "value", ...}`

### PathPrompt (prompts/path.rs)

**Purpose:** File/folder picker with navigation

**Features:**
- Browse filesystem starting from path
- Filter by name
- Navigate: left/backspace (parent), right/tab (into directory)
- Enter always submits selected path
- Cmd+K actions with path-specific context
- EventEmitter pattern for actions dialog

**Message:** `ShowPath { id, start_path, hint, ... }`

**Submits:** Selected file/folder path

### EnvPrompt (prompts/env.rs)

**Purpose:** Environment variable input with keyring storage

**Features:**
- Auto-retrieves from system keyring on show
- Stores secrets in macOS Keychain (via `keyring` crate)
- Mask input for secret values
- Full text selection and clipboard support

**Message:** `ShowEnv { id, key, prompt, secret, ... }`

**Submits:** Entered value (also stored in keyring if secret)

### SelectPrompt (prompts/select.rs)

**Purpose:** Multi-select from choice list

**Features:**
- Toggle selection with Space
- Filter by typing
- Cmd+A select/deselect all
- Shows selection count

**Message:** `ShowSelect { id, placeholder, choices, multiple, ... }`

**Submits:** JSON array of selected values

### DropPrompt (prompts/drop.rs)

**Purpose:** Drag-and-drop file receiving

**Features:**
- Visual drop zone
- Displays dropped file info
- Submit on Enter

**Message:** `ShowDrop { id, placeholder, hint, ... }`

**Submits:** JSON array of dropped files `[{path, name, size}, ...]`

### TemplatePrompt (prompts/template.rs)

**Purpose:** Fill in template with `{{placeholder}}` syntax

**Features:**
- Parses `{{name}}` placeholders
- Tab through inputs
- Live preview of filled template
- Unique placeholders only (first occurrence)

**Message:** `ShowTemplate { id, template, ... }`

**Submits:** Filled template string

### EditorPrompt (render_prompts/editor.rs)

**Purpose:** Multi-line code/text editor

**Features:**
- Syntax highlighting
- Find/Replace
- Template tabstops (`${1:name}`, `$1`)
- Configurable height

**Message:** `ShowEditor { id, content, language, template, actions }`

**Submits:** Editor content

### TermPrompt (render_prompts/term.rs)

**Purpose:** Terminal emulator

**Features:**
- PTY-backed terminal
- Command execution
- Configurable height

**Message:** `ShowTerm { id, command, actions }`

**Submits:** Terminal output or signal

## Form Parsing

The form parser (`form_parser.rs`) extracts fields from HTML:

```rust
let fields = parse_form_html(r#"
    <label for="username">Username:</label>
    <input type="text" name="username" id="username" placeholder="Enter username" />
    <textarea name="bio" placeholder="About you"></textarea>
    <input type="checkbox" name="subscribe" value="yes" />
"#);
```

**Extracts:**
- `name` attribute (required)
- `type` attribute (defaults to "text")
- `placeholder` attribute
- `value` attribute
- `checked` boolean attribute
- Associated `<label>` text via `for` attribute

**Skips:** `hidden`, `submit`, `button` input types

**Preserves document order** for consistent field layout.

## Rendering Patterns

### Using Design Tokens

All prompts should use design tokens for consistent theming:

```rust
let tokens = get_tokens(self.design_variant);
let colors = tokens.colors();
let spacing = tokens.spacing();
let visual = tokens.visual();
let typography = tokens.typography();

div()
    .bg(rgb(colors.background))
    .text_color(rgb(colors.text_primary))
    .p(px(spacing.padding_lg))
    .rounded(px(visual.radius_lg))
    .font_family(typography.font_family)
```

### Vibrancy Support

Use foundation helper for transparent backgrounds when vibrancy is enabled:

```rust
let vibrancy_bg = get_vibrancy_background(&self.theme);

div()
    .when_some(vibrancy_bg, |d, bg| d.bg(bg)) // Only apply bg when vibrancy disabled
```

### Keyboard Handling

Standard pattern for prompt key handling:

```rust
let handle_key = cx.listener(|this, event: &KeyDownEvent, window, cx| {
    let key_str = event.keystroke.key.to_lowercase();
    let has_cmd = event.keystroke.modifiers.platform;
    
    match key_str.as_str() {
        "enter" => this.submit(),
        "escape" => this.submit_cancel(),
        "up" | "arrowup" => this.move_up(cx),
        "down" | "arrowdown" => this.move_down(cx),
        _ => {
            // Handle character input
            if let Some(ref key_char) = event.keystroke.key_char {
                if let Some(ch) = key_char.chars().next() {
                    if !ch.is_control() {
                        this.handle_char(ch, cx);
                    }
                }
            }
        }
    }
});
```

### Focusable Implementation

Standard implementation via macro:

```rust
impl_focusable_via_base!(MyPrompt, base);
```

Or delegated focus (for forms):

```rust
impl Focusable for FormPromptState {
    fn focus_handle(&self, cx: &App) -> FocusHandle {
        // Return focused field's handle, not container's
        self.fields.get(self.focused_index)
            .map(|(_, entity)| entity.focus_handle(cx))
            .unwrap_or(self.focus_handle.clone())
    }
}
```

## Anti-patterns

### Don't use track_focus() on form containers

Form containers should NOT track focus directly - the child fields handle focus:

```rust
// WRONG
div()
    .track_focus(&self.focus_handle) // Steals focus from fields
    .child(entity)

// RIGHT
div()
    .on_key_down(handle_key) // Handle keys without tracking focus
    .child(entity)
```

### Don't forget to call notify()

After state changes, always notify GPUI:

```rust
// WRONG
fn move_down(&mut self) {
    self.selected_index += 1;
    // Missing notify - UI won't update
}

// RIGHT
fn move_down(&mut self, cx: &mut Context<Self>) {
    self.selected_index += 1;
    cx.notify();
}
```

### Don't hardcode colors

Always use theme or design tokens:

```rust
// WRONG
div().bg(rgb(0x1a1a2e))

// RIGHT
div().bg(rgb(colors.background))
```

### Don't block the UI thread

Use try_send for response channels:

```rust
// WRONG
sender.send(response).unwrap(); // Blocks

// RIGHT
match sender.try_send(response) {
    Ok(()) => {}
    Err(TrySendError::Full(_)) => logging::log("WARN", "Channel full"),
    Err(TrySendError::Disconnected(_)) => logging::log("UI", "Script exited"),
}
```

### Don't use byte indexing for text

Text operations must be char-based:

```rust
// WRONG
let before = &text[..cursor]; // May panic on multi-byte chars

// RIGHT
let chars: Vec<char> = text.chars().collect();
let before: String = chars[..cursor].iter().collect();
```

## Creating New Prompts

1. **Create struct** with `PromptBase` or equivalent fields
2. **Implement `Focusable`** (use macro or delegate)
3. **Implement `Render`** using design tokens
4. **Add message variant** to `PromptMessage` enum
5. **Handle in `prompt_handler.rs`** to create entity and set `AppView`
6. **Add render method** in `render_prompts/` if complex
7. **Add `AppView` variant** if needed

## File Reference

| File | Purpose |
|------|---------|
| `prompts/mod.rs` | Module exports, SubmitCallback type |
| `prompts/base.rs` | PromptBase, DesignContext, impl_focusable_via_base! |
| `prompts/div.rs` | DivPrompt, HTML rendering, ContainerOptions |
| `prompts/path.rs` | PathPrompt, file browser |
| `prompts/env.rs` | EnvPrompt, keyring integration |
| `prompts/select.rs` | SelectPrompt, multi-select |
| `prompts/drop.rs` | DropPrompt, drag-and-drop |
| `prompts/template.rs` | TemplatePrompt, placeholder filling |
| `form_prompt.rs` | FormPromptState, FormFieldEntity |
| `form_parser.rs` | parse_form_html(), field extraction |
| `prompt_handler.rs` | handle_prompt_message(), message routing |
| `render_prompts/arg.rs` | ArgPrompt rendering |
| `render_prompts/form.rs` | FormPrompt rendering |
| `render_prompts/editor.rs` | EditorPrompt |
| `render_prompts/term.rs` | TermPrompt |
| `render_prompts/div.rs` | DivPrompt additional rendering |
| `render_prompts/path.rs` | PathPrompt additional rendering |
| `render_prompts/other.rs` | Other prompt render methods |
