---
name: hyprland-debug
description: Debug Hyprland/Wayland issues. Use when theme switching fails, windows disappear, services crash, or displays malfunction.
---
<!-- @agent-architect owns this file. Delegate changes, don't edit directly. -->

<announcement>
"I'm using the hyprland-debug skill to diagnose Wayland/Hyprland issues."
</announcement>

<diagnosis_order>
1. Check Hyprland logs for errors (DRM conflicts, modesetting)
2. Check for process accumulation (multiple swaybg, waybar instances)
3. Check service logs for Wayland connection errors
4. Verify HYPRLAND_INSTANCE_SIGNATURE is current
5. Check monitor-related daemons for state-change loops
</diagnosis_order>

<log_locations>
Hyprland logs: /run/user/$(id -u)/hypr/*/hyprland.log
Hyprland socket: $XDG_RUNTIME_DIR/hypr/$HYPRLAND_INSTANCE_SIGNATURE/
User service logs: journalctl --user -u SERVICE
</log_locations>

<common_causes>
Windows disappearing: Multiple background daemons (swaybg) causing DRM page-flip conflicts.
Repeated modesetting: Monitor daemon applying config without checking current state.
Service crashes: Wayland connection lost during restart - often from upstream DRM issues.
Broken socket errors: Stale HYPRLAND_INSTANCE_SIGNATURE from crash/logout.
</common_causes>

<anti_patterns>
Restarting services with file watchers: Check logs for "reload listener" - if present, service auto-reloads.
Gentle kills for background daemons: Use SIGKILL + delay for clean replacement.
Monitor config without state check: Always check current state before hyprctl keyword commands.
SIGUSR2 for waybar theme changes: Doesn't re-fetch @imported CSS files - need full restart.
Modifying nix-managed configs: Symlinks to /nix/store are immutable - can't trigger inotify.
PartOf= for Wayland services: Causes services to stop during home-manager reload.
</anti_patterns>

<service_reload_methods>
Check bin/omarchy/ scripts for current implementations. General patterns:
- hyprctl keyword: Safe for Hyprland config changes without reload
- swaync-client -rs: CSS reload without service restart
- File watchers: Many services auto-reload on file change
- Full restart: Only when other methods don't work
</service_reload_methods>

<stale_session_fix>
Shell startup script in shell/fish/conf.d/ handles stale HYPRLAND_INSTANCE_SIGNATURE. Tests actual hyprctl connectivity and updates to working instance. tmux update-environment includes Wayland vars.
</stale_session_fix>

<verification>
After any fix: verify single instance of daemons with pgrep -c. Check Hyprland logs for new errors. Confirm services responding. Test the original failing operation.
</verification>
