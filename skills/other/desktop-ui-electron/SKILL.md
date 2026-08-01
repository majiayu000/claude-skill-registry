---
name: desktop-ui-electron
description: Frameless windows, custom title bars, tray, menus, dock badges, vibrancy, kiosk mode, window state persistence
---

# Electron Desktop UI Patterns

> **Quick Guide:** Use `titleBarStyle: 'hidden'` for custom title bars with native traffic lights on macOS, combined with `titleBarOverlay` for Windows/Linux window controls. Mark draggable regions with `app-region: drag` in CSS and exclude interactive elements with `app-region: no-drag`. Keep a module-level reference to `Tray` objects (garbage collection silently destroys the icon). Use `vibrancy` for macOS translucency effects and `backgroundMaterial` for Windows 11 Mica/Acrylic. Persist window bounds manually with `getBounds()`/`setBounds()` on the `close` event.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST keep a module-level reference to `Tray` objects -- garbage collection silently destroys the tray icon with no error)**

**(You MUST use `app-region: no-drag` on ALL interactive elements (buttons, inputs, links) inside a drag region -- draggable areas swallow all pointer events)**

**(You MUST add `user-select: none` to draggable title bar regions -- dragging conflicts with text selection)**

**(You MUST NOT use `transparent: true` with `backgroundMaterial` on Windows -- set `backgroundColor: '#00000000'` instead to allow the DWM material to show through)**

</critical_requirements>

---

**Auto-detection:** titleBarStyle, titleBarOverlay, trafficLightPosition, frameless window, frame false, app-region drag, custom title bar, Tray, system tray, tray icon, Menu.buildFromTemplate, context menu, app.setBadgeCount, dock badge, splash screen, kiosk, alwaysOnTop, vibrancy, backgroundMaterial, mica, acrylic, transparent window, electron-window-state, window state persistence, getBounds, setBounds

**When to use:**

- Building custom title bars (frameless, overlay controls, macOS traffic light positioning)
- Creating system tray icons with context menus
- Building application menus and context menus
- Adding dock/taskbar badges for notifications
- Implementing splash screens or always-on-top windows
- Making windows transparent or applying vibrancy/material effects
- Persisting and restoring window position and size
- Entering kiosk mode for single-app displays

**When NOT to use:**

- Choosing a UI framework for the renderer content (not this skill's scope)
- Styling renderer page content (not this skill's scope)
- Configuring IPC or preload security (separate from window chrome customization)
- Packaging or distributing the application (separate from window chrome customization)

**Key patterns covered:**

- Frameless windows with `titleBarStyle: 'hidden'` and `titleBarOverlay`
- Custom title bars with CSS `app-region: drag` / `no-drag`
- macOS traffic light positioning via `trafficLightPosition`
- Native application menus and context menus
- System tray icons with menus and click handlers
- Dock/taskbar badges (`app.setBadgeCount`, `app.dock.setBadge`)
- Splash screens and always-on-top windows
- Window state persistence (position, size, maximized)
- Transparent windows, vibrancy (macOS), backgroundMaterial (Windows 11)
- Kiosk mode

---

<philosophy>

## Philosophy

Electron desktop UI customization operates at two levels: **window chrome** (title bar, frame, transparency, system tray) controlled via `BrowserWindow` constructor options and main process APIs, and **in-window layout** (drag regions, custom title bar HTML/CSS) controlled via the renderer. The main process owns window-level behavior; the renderer owns the visual presentation within the window.

**Platform-aware design is essential.** macOS has native traffic lights and vibrancy. Windows 11 has Mica/Acrylic materials and `titleBarOverlay` for window controls. Linux varies by desktop environment. Always test UI customizations on all target platforms -- what works on macOS may look wrong on Windows or be unsupported on Linux.

**When to customize window chrome:**

- App requires a branded header or sidebar navigation alongside window controls
- App needs to minimize visual chrome (media player, creative tool)
- App runs in kiosk/display mode (digital signage, POS terminal)
- App needs persistent system tray presence (background services, communication tools)

**When NOT to customize:**

- Standard document-based apps where native title bar is expected
- Apps where accessibility is the top priority (custom title bars can break screen readers)
- When native platform look-and-feel is more important than branding

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Frameless Windows and Custom Title Bars

Use `titleBarStyle: 'hidden'` to remove the native title bar while keeping macOS traffic lights. On Windows/Linux, add `titleBarOverlay` to get native window control buttons overlaid on your content.

```javascript
const TITLE_BAR_OVERLAY_HEIGHT = 40;

const mainWindow = new BrowserWindow({
  titleBarStyle: "hidden",
  // Windows/Linux: overlay native controls on custom title bar
  titleBarOverlay: {
    color: "#2f3241",
    symbolColor: "#74b1be",
    height: TITLE_BAR_OVERLAY_HEIGHT,
  },
  // macOS: position traffic lights within custom title bar
  trafficLightPosition: { x: 16, y: 12 },
});
```

**Key point:** `titleBarStyle: 'hidden'` hides the title text and title bar area but keeps macOS traffic lights visible. `titleBarOverlay` creates a Windows Controls Overlay (WCO) with native minimize/maximize/close buttons on Windows and Linux. See [examples/core.md](examples/core.md) for the full CSS title bar implementation.

---

### Pattern 2: CSS Drag Regions

Mark custom title bar areas as draggable with `app-region: drag`. All interactive elements (buttons, inputs) inside a drag region MUST be marked `app-region: no-drag` or they will be unclickable.

```css
.title-bar {
  app-region: drag;
  user-select: none;
  height: 40px;
}

.title-bar button,
.title-bar input {
  app-region: no-drag;
}
```

**Key point:** Draggable areas swallow ALL pointer events -- no clicks, no hover, no cursor changes. Only rectangular regions are supported. Never use custom context menus on drag regions (right-click triggers the system window menu on some platforms). See [examples/core.md](examples/core.md).

---

### Pattern 3: Application Menus and Context Menus

Use `Menu.buildFromTemplate()` for both application menus and right-click context menus. On macOS, the first menu item is always the app name menu.

```javascript
const { Menu, app } = require("electron/main");

const template = [
  ...(process.platform === "darwin"
    ? [{ label: app.name, submenu: [{ role: "about" }, { role: "quit" }] }]
    : []),
  {
    label: "File",
    submenu: [
      {
        label: "Open",
        accelerator: "CmdOrCtrl+O",
        click: () => {
          /* ... */
        },
      },
      process.platform === "darwin" ? { role: "close" } : { role: "quit" },
    ],
  },
];
Menu.setApplicationMenu(Menu.buildFromTemplate(template));
```

**Key point:** Use built-in `role` values (undo, copy, paste, quit, about, etc.) for standard actions -- Electron handles platform-specific labels and shortcuts automatically. See [examples/core.md](examples/core.md) for context menus.

---

### Pattern 4: System Tray

Create a persistent system tray icon with a context menu. You MUST keep a module-level reference to the `Tray` object or it will be garbage collected and the icon disappears silently.

```javascript
const { Tray, Menu, nativeImage } = require("electron/main");

let tray = null; // MUST keep reference -- GC destroys the icon silently

function createTray(mainWindow) {
  const icon = nativeImage.createFromPath(
    path.join(__dirname, "assets", "tray-icon.png"),
  );
  if (process.platform === "darwin") icon.setTemplateImage(true);

  tray = new Tray(icon);
  tray.setToolTip(app.name);
  tray.setContextMenu(
    Menu.buildFromTemplate([
      {
        label: "Show",
        click: () => {
          mainWindow.show();
          mainWindow.focus();
        },
      },
      { type: "separator" },
      { label: "Quit", click: () => app.quit() },
    ]),
  );
}
```

**Key point:** macOS tray icons should be 16x16 template images (monochrome) -- call `setTemplateImage(true)` so the OS renders them correctly in dark/light mode. On Windows/Linux, handle `tray.on('click')` for left-click behavior. See [examples/core.md](examples/core.md) for balloon notifications.

---

### Pattern 5: Dock and Taskbar Badges

Use `app.setBadgeCount()` (macOS, Linux/Unity) for numeric badges or `app.dock.setBadge()` (macOS only) for text badges.

```javascript
// Numeric badge (macOS + Linux/Unity)
app.setBadgeCount(5); // Shows "5" on dock/taskbar icon
app.setBadgeCount(0); // Hides the badge

// Text badge (macOS only)
app.dock.setBadge("!"); // Shows "!" on dock icon
app.dock.setBadge(""); // Clears the badge
```

**Key point:** `setBadgeCount` returns `boolean` (false if platform doesn't support it). On Windows, use a third-party overlay solution -- native badge API is not available. See [examples/core.md](examples/core.md).

---

### Pattern 6: Window State Persistence

Save and restore window position, size, and maximized state across app restarts using `getBounds()`/`setBounds()` and a local JSON file.

```javascript
const WINDOW_STATE_FILE = "window-state.json";

function loadWindowState() {
  try {
    const data = fs.readFileSync(
      path.join(app.getPath("userData"), WINDOW_STATE_FILE),
      "utf-8",
    );
    return JSON.parse(data);
  } catch {
    return null;
  }
}

function saveWindowState(win) {
  const bounds = win.getBounds();
  const data = { ...bounds, isMaximized: win.isMaximized() };
  fs.writeFileSync(
    path.join(app.getPath("userData"), WINDOW_STATE_FILE),
    JSON.stringify(data),
  );
}
```

**Key point:** Save state on the `close` event (not `closed` -- the window is already destroyed). Validate saved bounds against current display geometry to avoid restoring off-screen. See [examples/window-state.md](examples/window-state.md) for the complete implementation with display validation.

---

### Pattern 7: Transparent Windows and Visual Effects

Use `transparent: true` for fully transparent windows (overlays, widgets). Use `vibrancy` (macOS) or `backgroundMaterial` (Windows 11) for system-level translucency effects.

```javascript
// macOS vibrancy
const win = new BrowserWindow({
  vibrancy: "sidebar",
  visualEffectState: "active",
  backgroundColor: "#00000000",
});

// Windows 11 Mica/Acrylic -- do NOT use transparent: true
const win = new BrowserWindow({
  backgroundMaterial: "mica",
  backgroundColor: "#00000000",
});
```

**Key point:** For `backgroundMaterial` on Windows, set `backgroundColor: '#00000000'` instead of `transparent: true` -- the latter enables layered window mode which breaks material rendering. `vibrancy` accepts 15+ values; `sidebar` and `under-window` are the most common. See [examples/core.md](examples/core.md).

---

### Pattern 8: Splash Screens and Always-On-Top Windows

Create a splash screen as a frameless, always-on-top window that closes after the main window loads.

```javascript
const splash = new BrowserWindow({
  width: 400,
  height: 300,
  frame: false,
  alwaysOnTop: true,
  transparent: true,
  skipTaskbar: true,
  resizable: false,
});
splash.loadFile("splash.html");

mainWindow.once("ready-to-show", () => {
  splash.destroy();
  mainWindow.show();
});
```

**Key point:** Use `skipTaskbar: true` so the splash doesn't appear in the taskbar. Show the main window only after `ready-to-show` fires (content is rendered). See [examples/core.md](examples/core.md) for kiosk mode.

---

### Pattern 9: Kiosk Mode

Kiosk mode makes the window fullscreen with no way for the user to exit via standard OS controls.

```javascript
const kiosk = new BrowserWindow({
  kiosk: true,
  // alwaysOnTop: true, // optional: stay above other apps
});
// Exit kiosk programmatically
kiosk.setKiosk(false);
```

**Key point:** Kiosk mode disables window controls, Alt+F4 on Windows, and Cmd+Q on macOS. Provide an in-app exit mechanism (admin button, keyboard shortcut via IPC) or the user cannot close the app.

</patterns>

---

<decision_framework>

## Decision Framework

### Window Chrome Strategy

```
Need custom branding in the title bar?
+-- YES --> titleBarStyle: 'hidden' + titleBarOverlay (Windows/Linux)
|           + custom HTML/CSS title bar with app-region: drag
+-- NO  --> Keep default frame: true

Need fully frameless (no controls at all)?
+-- YES --> frame: false + implement ALL window controls in HTML
+-- NO  --> Use titleBarStyle: 'hidden' (keeps native controls)

Need transparency?
+-- Fully transparent (overlay widget)? --> transparent: true + frame: false
+-- macOS frosted glass? --> vibrancy: 'sidebar' (or other type)
+-- Windows 11 material? --> backgroundMaterial: 'mica' | 'acrylic'
```

### Title Bar Options by Platform

| Option                         | macOS                             | Windows                           | Linux                             |
| ------------------------------ | --------------------------------- | --------------------------------- | --------------------------------- |
| `titleBarStyle: 'hidden'`      | Hides title, keeps traffic lights | Hides title bar entirely          | Hides title bar entirely          |
| `titleBarStyle: 'hiddenInset'` | Traffic lights inset further      | N/A (same as hidden)              | N/A (same as hidden)              |
| `titleBarOverlay`              | Not needed (traffic lights stay)  | Adds native min/max/close buttons | Adds native min/max/close buttons |
| `trafficLightPosition`         | Custom traffic light position     | N/A                               | N/A                               |
| `frame: false`                 | No chrome at all                  | No chrome at all                  | No chrome at all                  |

### System Tray vs Dock Badge

```
Need background presence after window close?
+-- YES --> System tray (Tray) + tray.setContextMenu()
+-- NO  --> Just show/hide the main window

Need notification count on app icon?
+-- macOS? --> app.setBadgeCount() or app.dock.setBadge()
+-- Linux/Unity? --> app.setBadgeCount()
+-- Windows? --> Third-party taskbar overlay
```

</decision_framework>

---

**Detailed resources:**

- [examples/core.md](examples/core.md) - Custom title bars, drag regions, tray, menus, badges, transparent windows, splash screens, kiosk mode
- [examples/window-state.md](examples/window-state.md) - Window state persistence with display validation
- [reference.md](reference.md) - Quick-reference tables, vibrancy values, platform support matrix

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Losing the `Tray` reference (no module-level variable) -- tray icon disappears silently when garbage collected
- Missing `app-region: no-drag` on buttons/inputs inside a drag region -- they become unclickable with no visible indication
- Using `transparent: true` with `backgroundMaterial` on Windows -- breaks material rendering; use `backgroundColor: '#00000000'` instead
- Using `frame: false` without implementing window controls -- users cannot minimize, maximize, or close the window
- Missing `user-select: none` on drag regions -- dragging accidentally selects title bar text

**Medium Priority Issues:**

- Not providing a macOS-specific first menu item (app name menu) -- menu bar looks wrong on macOS
- Missing platform checks for macOS-only APIs (`vibrancy`, `trafficLightPosition`, `dock.setBadge`)
- Not using template images for macOS tray icons -- icon does not adapt to dark/light mode
- Saving window state on `closed` instead of `close` -- window is already destroyed, `getBounds()` fails
- Not validating restored window bounds against current displays -- window appears off-screen after display changes

**Gotchas & Edge Cases:**

- `titleBarOverlay` is not needed on macOS -- traffic lights stay visible automatically with `titleBarStyle: 'hidden'`
- `titleBarStyle: 'hiddenInset'` and `customButtonsOnHover` are macOS-only -- they behave like `'hidden'` on other platforms
- Tray `click` event does not fire on macOS when a context menu is set -- macOS always shows the context menu on any click
- `app.setBadgeCount()` requires notification permissions on macOS and a `.desktop` file on Linux
- `backgroundMaterial` requires Windows 11 22H2 or later -- it silently does nothing on older Windows versions
- `vibrancy` values like `appearance-based` are deprecated -- prefer `sidebar`, `under-window`, `content`
- Kiosk mode disables standard OS exit shortcuts (Alt+F4, Cmd+Q) -- provide an in-app exit mechanism
- Right-clicking a drag region triggers the system window menu on some platforms -- never use custom context menus on drag regions
- `setAlwaysOnTop(true, 'screen-saver')` places the window above macOS fullscreen apps but is discouraged by Apple for non-screen-saver use
- On Linux, tray support depends on the desktop environment -- GNOME requires an extension; KDE and XFCE support it natively

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST keep a module-level reference to `Tray` objects -- garbage collection silently destroys the tray icon with no error)**

**(You MUST use `app-region: no-drag` on ALL interactive elements (buttons, inputs, links) inside a drag region -- draggable areas swallow all pointer events)**

**(You MUST add `user-select: none` to draggable title bar regions -- dragging conflicts with text selection)**

**(You MUST NOT use `transparent: true` with `backgroundMaterial` on Windows -- set `backgroundColor: '#00000000'` instead to allow the DWM material to show through)**

**Failure to follow these rules will cause invisible tray icons, unclickable buttons, broken transparency, and poor cross-platform behavior.**

</critical_reminders>
