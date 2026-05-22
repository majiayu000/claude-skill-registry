---
name: developing-gtk-apps
description: Use when building GTK 4/libadwaita applications; before writing app boilerplate; when debugging threading, signals, or lifecycle issues; when setting up GSettings, resources, or packaging; delegates UI/widget decisions to designing-gnome-ui skill
---

# Developing GTK Apps

Build robust GTK 4/libadwaita applications with correct architecture, lifecycle, and patterns.

**Core principle:** Get the foundation right before the UI. Application lifecycle, threading model, and resource management are where most GTK apps break.

**Relationship to UI skill:** This skill handles architecture and plumbing. For widget selection, layout, and HIG compliance, use `designing-gnome-ui`.

## Decision Flow

| Task | Use |
|------|-----|
| Which widget for settings? | designing-gnome-ui |
| How to structure preferences window? | designing-gnome-ui |
| App crashes on startup | THIS SKILL |
| UI freezes during operation | THIS SKILL |
| How to save user preferences | THIS SKILL (GSettings) |
| Signal not firing/memory leak | THIS SKILL |
| Setting up new app boilerplate | THIS SKILL |
| Packaging for Flatpak | THIS SKILL |

## What's Current (libadwaita 1.7+, GTK 4.18+)

**API deprecations to avoid:**
- `GtkShortcutsWindow` → Use `AdwShortcutsDialog` (libadwaita 1.8+)
- `.dim-label` CSS class → Use `.dimmed` class
- X11/Broadway backends are deprecated in GTK 4 (removal planned for GTK 5)

**New patterns (libadwaita 1.6-1.8):**
- `AdwSpinner` - Preferred over `GtkSpinner`
- `AdwToggleGroup` - Replaces multiple exclusive `GtkToggleButton` instances
- `AdwBottomSheet` - Persistent bottom sheets
- `AdwWrapBox` - Box that wraps children to new lines
- `AdwInlineViewSwitcher` - For cards, sidebars, boxed lists

## Application Boilerplate

```python
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio

class MyApp(Adw.Application):
    def __init__(self):
        super().__init__(
            application_id="com.example.MyApp",
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS
        )

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = MyWindow(application=self)
        win.present()

class MyWindow(Adw.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_default_size(800, 600)

def main():
    app = MyApp()
    return app.run(None)
```

### Application ID Rules

| Rule | Example |
|------|---------|
| Reverse domain notation | `com.example.AppName` |
| Only alphanumeric + dots | `org.gnome.TextEditor` |
| Min 2 segments | `com.myapp` (not `myapp`) |
| Match desktop file | `com.example.MyApp.desktop` |

### Lifecycle Signals

| Signal | When | Use For |
|--------|------|---------|
| `startup` | Once, app launches | Actions, CSS, GSettings |
| `activate` | Each launch/raise | Create/present window |
| `shutdown` | App exits | Save state, cleanup |
| `open` | Files passed to app | Handle file arguments |

```python
def do_startup(self):
    Adw.Application.do_startup(self)  # Chain up FIRST
    self.setup_actions()
```

## Threading - The Critical Rule

**GTK is single-threaded. All UI calls MUST happen on the main thread.**

```python
# WRONG - will crash
def background_task():
    result = slow_computation()
    self.label.set_text(result)  # CRASH

# RIGHT - use GLib.idle_add
def background_task():
    result = slow_computation()
    GLib.idle_add(self.label.set_text, result)  # Safe

threading.Thread(target=background_task).start()
```

For async patterns with `Gio.Task` and cancellation, see `gtk-patterns-reference.md`.

## Actions (Quick Reference)

Actions connect UI to behavior. Define at app level (`app.action`) or window level (`win.action`).

```python
# In do_startup - app-level action
quit_action = Gio.SimpleAction.new("quit", None)
quit_action.connect("activate", lambda a, p: self.quit())
self.add_action(quit_action)
self.set_accels_for_action("app.quit", ["<Control>q"])

# In window __init__ - window-level action
save_action = Gio.SimpleAction.new("save", None)
save_action.connect("activate", self.on_save)
self.add_action(save_action)
self.get_application().set_accels_for_action("win.save", ["<Control>s"])
```

For stateful actions (toggles), parameterized actions, and menu integration, see `gtk-patterns-reference.md`.

## GSettings (Quick Reference)

Persist user preferences with GSettings. Requires a schema file.

```python
# In app __init__
self.settings = Gio.Settings.new("com.example.MyApp")

# Read/write values
dark = self.settings.get_boolean("dark-mode")
self.settings.set_boolean("dark-mode", True)

# Bind to widget property (auto-syncs)
self.settings.bind("window-width", window, "default-width",
    Gio.SettingsBindFlags.DEFAULT)

# React to changes
self.settings.connect("changed::dark-mode", self.on_dark_changed)
```

For schema XML format and installation, see `gtk-patterns-reference.md`.

## Debugging (Quick Reference)

```bash
GTK_DEBUG=interactive myapp      # Open GTK Inspector (Ctrl+Shift+D)
G_MESSAGES_DEBUG=all myapp       # Show all debug messages
G_DEBUG=fatal-criticals myapp    # Abort on critical warnings
GSETTINGS_BACKEND=memory myapp   # Test without persisting settings
```

For full debugging patterns, profiling, and GDB integration, see `gtk-debugging-reference.md`.

## Red Flags - STOP

- Calling UI methods from threads (use `GLib.idle_add`)
- Missing `do_startup` chain-up
- Signal handlers without disconnect on destroy
- Blocking operations in signal handlers
- Hardcoded paths instead of XDG directories
- Missing application ID or wrong format
- Using `time.sleep()` in main thread
- Using `GtkShortcutsWindow` (deprecated - use `AdwShortcutsDialog`)
- Using `GtkSpinner` for libadwaita apps (use `AdwSpinner`)

## Reference Files

| Need | File |
|------|------|
| GObject classes, properties, **signals**, list models, **property bindings**, **factories** | `gtk-gobject-reference.md` |
| Actions, GSettings, Resources, Blueprint, async file ops | `gtk-patterns-reference.md` |
| Desktop file, **AppStream metadata**, Meson, Flatpak, **icons**, **Python deps** | `gtk-packaging-reference.md` |
| Testing with pytest, **async testing**, **headless/CI testing** | `gtk-testing-reference.md` |
| Internationalization, gettext, **ngettext plurals**, .po files, **Blueprint i18n**, **RTL testing** | `gtk-i18n-reference.md` |
| DBus activation, **interface export**, background services, **Flatpak portals** | `gtk-dbus-reference.md` |
| GTK Inspector, env vars, **profiling**, **memory debugging** | `gtk-debugging-reference.md` |
| UI patterns, widgets, HIG | Use `designing-gnome-ui` skill |

## External References

- [Blueprint docs](https://jwestman.pages.gitlab.gnome.org/blueprint-compiler/)
- [Libadwaita API](https://gnome.pages.gitlab.gnome.org/libadwaita/doc/1-latest/)
- [GTK 4 API](https://docs.gtk.org/gtk4/)
