---
name: powerskills-desktop
description: Windows desktop automation. Take full-screen or window screenshots, list/focus/minimize/maximize windows, send keystrokes, launch applications. Use when needing to capture the Windows screen, manage windows, send keyboard input, or start programs.
license: MIT
metadata:
  author: aloth
  cli: powerskills
  parent: powerskills
---

# PowerSkills — Desktop

Desktop automation: screenshots, window management, keystrokes, app launching.

## Requirements

- Windows with .NET Framework (System.Windows.Forms, System.Drawing)

## Actions

```powershell
.\powerskills.ps1 desktop <action> [--params]
```

| Action | Params | Description |
|--------|--------|-------------|
| `screenshot` | `--out-file path.png [--window "title"]` | Full screen or window capture |
| `windows` | | List all visible windows with title, PID, process name |
| `focus` | `--window "title"` | Bring window to foreground |
| `minimize` | `--window "title"` | Minimize window |
| `maximize` | `--window "title"` | Maximize window |
| `keys` | `--keys "{ENTER}" [--window "title"]` | Send keystrokes (SendKeys syntax) |
| `launch` | `--app notepad [--app-args "file.txt"] [--wait-ms 3000]` | Launch application |

## Examples

```powershell
# Full screen screenshot
.\powerskills.ps1 desktop screenshot --out-file screen.png

# Capture a specific window
.\powerskills.ps1 desktop screenshot --out-file outlook.png --window "Outlook"

# List all windows
.\powerskills.ps1 desktop windows

# Focus and type into Notepad
.\powerskills.ps1 desktop focus --window "Notepad"
.\powerskills.ps1 desktop keys --keys "Hello world{ENTER}" --window "Notepad"

# Launch an app
.\powerskills.ps1 desktop launch --app "notepad.exe" --app-args "C:\temp\notes.txt"
```

## SendKeys Syntax

| Key | Syntax |
|-----|--------|
| Enter | `{ENTER}` |
| Tab | `{TAB}` |
| Escape | `{ESC}` |
| Ctrl+C | `^c` |
| Alt+F4 | `%{F4}` |
| Shift+Tab | `+{TAB}` |

See [Microsoft SendKeys docs](https://learn.microsoft.com/en-us/dotnet/api/system.windows.forms.sendkeys) for full syntax.

## Output Fields

### windows
`title`, `pid`, `process`, `hwnd`

### screenshot
`saved`, `width`, `height`, `window` (if window capture)
