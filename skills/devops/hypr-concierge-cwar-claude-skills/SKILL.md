---
name: hypr-concierge
description: Personal theme concierge for Hyprland desktop environments. Use when
  user wants to (1) change desktop theme/colors, (2) apply preset themes (Catppuccin/Dracula/Nord/Gruvbox/Rose
  Pine/Kanagawa/Tokyo Ni
---

---
name: hypr-concierge
description: Personal theme concierge for Hyprland desktop environments. Use when user wants to (1) change desktop theme/colors, (2) apply preset themes (Catppuccin/Dracula/Nord/Gruvbox/Rose Pine/Kanagawa/Tokyo Night), (3) create custom themes from mood/aesthetic descriptions, (4) create themes inspired by movies/art/feelings, (5) get theme recommendations based on mood, (6) learn what themes look/feel like, (7) save/restore/switch themes, (8) manage which apps get themed, or (9) find/change wallpapers. Triggers: "change theme", "apply catppuccin", "I want something cozy", "create a Hackers theme", "describe the themes", "what feels like...", "save my theme", "find wallpapers", "change wallpaper", "theme concierge".
---

# Hypr Concierge

Your personal theme concierge for Hyprland/Wayland desktop environments.

## Quick Start

1. Choose or define a theme (see [themes.md](references/themes.md) for presets)
2. Read [app-formats.md](references/app-formats.md) for target application's format
3. Edit config files in `~/dotfiles/{app}/.config/{app}/`
4. Run `cd ~/dotfiles && stow {app}` if new files created
5. Reload each application

## Workflow

### Apply Preset Theme

```
User: "Switch to Catppuccin"
```

1. Read `references/themes.md` → get Catppuccin Mocha colors
2. Read `references/app-formats.md` → get format for each app
3. Edit each config file with theme colors:
   - `~/dotfiles/hypr/.config/hypr/hyprland.conf`
   - `~/dotfiles/waybar/.config/waybar/style.css`
   - `~/dotfiles/rofi/.config/rofi/tokyo-night.rasi` (rename file if desired)
   - `~/dotfiles/mako/.config/mako/config`
   - `~/dotfiles/ghostty/.config/ghostty/config`
   - `~/dotfiles/tmux/.tmux.conf`
4. Reload apps: `hyprctl reload && makoctl reload && killall -SIGUSR2 waybar`
5. Suggest Neovim colorscheme plugin if applicable

### Describe Themes / Match Aesthetic

```
User: "Describe the available themes"
User: "I want something cozy and warm"
User: "What theme feels like a rainy day?"
```

1. Read `references/themes.md` → get aesthetic descriptions
2. For matching: compare user's mood/description to theme moods
3. Recommend 1-2 themes with explanation of why they fit
4. Offer to apply the recommended theme

### Create Custom Theme

```
User: "Create a theme with blue and orange accents"
```

1. Read `references/color-schema.md` → understand required color slots
2. Generate cohesive palette based on user's description
3. Apply using same process as preset themes

### Create Theme from Inspiration

```
User: "Create a theme inspired by the movie Hackers"
User: "I want a Blade Runner aesthetic"
User: "Make it feel like a forest at night"
```

1. Analyze the inspiration's visual language:
   - What are the dominant colors?
   - What's the mood/atmosphere?
   - What would "error" or "success" look like in that world?
2. Generate a cohesive palette following `references/color-schema.md`
3. Name the theme descriptively
4. Show the user the palette with rationale before applying
5. Save as a custom theme in `~/.config/hyprland-themes/saved/`

### Partial Theme Update

```
User: "Make waybar match my terminal colors"
```

1. Read the source config (e.g., ghostty) to extract current colors
2. Read target app's format from `references/app-formats.md`
3. Apply matching colors to target config only

### Save Current Theme

```
User: "Save my current theme as cozy-dark"
```

1. Read `references/theme-management.md` for save procedure
2. Create `~/.config/hyprland-themes/saved/{name}/` directory
3. Copy all current configs to the save directory
4. Create theme-info.txt with name, date, description
5. Update active-theme.txt

### List Saved Themes

```
User: "What themes do I have saved?"
```

1. List contents of `~/.config/hyprland-themes/saved/`
2. Read theme-info.txt from each
3. Indicate which is currently active

### Switch/Restore Theme

```
User: "Switch to my tokyo-night theme"
```

1. Verify theme exists in saved themes
2. Offer to save current theme first if it has unsaved changes
3. Copy saved configs back to dotfiles locations
4. Re-stow dotfiles and reload all applications
5. Update active-theme.txt

### List Themed Apps

```
User: "What apps can you theme?"
```

1. Read `references/themed-apps.md`
2. List all apps in the registry with their reload commands
3. Note any plugin-based apps (like Neovim)

### Add New App to Theming

```
User: "Add kitty terminal to my themed apps"
```

1. Ask user for config file location and reload command
2. Determine color format by reading their existing config
3. Add entry to `references/themed-apps.md`
4. Add detailed format instructions to `references/app-formats.md`
5. Include the new app in future theme operations

### Find Wallpapers for Theme

```
User: "Find wallpapers for my Hackers theme"
User: "I need a new wallpaper"
```

1. Search Wallhaven with theme-appropriate keywords (see `references/wallpapers.md`)
2. Collect wallpaper IDs and resolutions from results
3. Generate themed HTML preview page with thumbnails
4. Open preview in browser for user to browse visually
5. User selects wallpaper by ID
6. Download and apply selected wallpaper

### Apply Wallpaper

```
User: "Use wallpaper l3qo2r" or "Download that one"
```

1. Download full resolution from Wallhaven
2. Save to `~/Pictures/` with descriptive name
3. Update `~/dotfiles/hypr/.config/hypr/hyprpaper.conf`
4. Reload hyprpaper: `hyprctl hyprpaper reload`

## Themed Applications

| Application | Config Location | Reload Command |
|-------------|-----------------|----------------|
| Hyprland | `hypr/.config/hypr/hyprland.conf` | `hyprctl reload` |
| Hyprlock | `hypr/.config/hypr/hyprlock.conf` | (next lock) |
| Waybar | `waybar/.config/waybar/style.css` | `killall -SIGUSR2 waybar` |
| Rofi | `rofi/.config/rofi/*.rasi` | (next launch) |
| Mako | `mako/.config/mako/config` | `makoctl reload` |
| Ghostty | `ghostty/.config/ghostty/config` | Ctrl+Shift+, |
| Tmux | `tmux/.tmux.conf` | `tmux source ~/.tmux.conf` |

## Color Format Quick Reference

| App | Format | Example |
|-----|--------|---------|
| Hyprland | `rgba(HEXaa)` | `rgba(7aa2f7ee)` |
| Waybar | `#HEX` or `rgba(r,g,b,a)` | `#7aa2f7` or `rgba(122,162,247,0.9)` |
| Rofi | `#HEXaa` | `#7aa2f7e6` |
| Mako | `#HEX` | `#7aa2f7` |
| Ghostty | `#HEX` | `#7aa2f7` |
| Tmux | `#HEX` in strings | `"fg=#7aa2f7"` |

## Available Themes

Presets in `references/themes.md`:
- Tokyo Night (current default)
- Catppuccin Mocha
- Dracula
- Nord
- Gruvbox Dark
- Rose Pine
- Kanagawa

## Theme Management

Saved themes stored in `~/.config/hyprland-themes/saved/`

| Action | Quick Check |
|--------|-------------|
| List saved | `ls ~/.config/hyprland-themes/saved/` |
| Current theme | `cat ~/.config/hyprland-themes/active-theme.txt` |
| Theme details | `cat ~/.config/hyprland-themes/saved/{name}/theme-info.txt` |

See [theme-management.md](references/theme-management.md) for full save/restore procedures.

## References

- [Themed Apps](references/themed-apps.md) - Registry of apps to theme (add new apps here)
- [App Formats](references/app-formats.md) - Per-application config formats and examples
- [Themes](references/themes.md) - Preset theme palettes
- [Color Schema](references/color-schema.md) - Semantic color definitions
- [Theme Management](references/theme-management.md) - Save, restore, and switch themes
- [Wallpapers](references/wallpapers.md) - Wallpaper search, preview, and management
