---
name: rebuild
description: Apply Nix configuration changes. Use when modifying .nix files, after flake updates, or when user asks to rebuild/apply dotfiles changes.
---
<!-- @agent-architect owns this file. Delegate changes, don't edit directly. -->

<announcement>
"I'm using the rebuild skill to apply configuration changes."
</announcement>

<context>
Session-context hook provides User and OS at session start. Use this to determine rebuild strategy:
- NixOS: Use nixosConfigurations with username from session
- Non-NixOS: Use homeConfigurations with username@arch-linux format
</context>

<prerequisite>
Nix reads from git index, not working tree. Stage all modified files before rebuilding: `git add specific-file.nix` for each changed file. Never use `git add -A` or `git add .` (may stage unrelated parallel work).
</prerequisite>

<simple_rebuild>
Primary method: `./bin/rebuild` (or `~/bin/rebuild`).
Auto-detects platform and user dynamically. Sources nix-daemon.sh if needed. Handles backup naming.

NixOS: Runs `sudo nixos-rebuild switch --flake ~/.dotfiles#$(whoami)`
Non-NixOS: Runs `home-manager switch --flake ~/.dotfiles#$(whoami)@$(arch)-linux`
</simple_rebuild>

<nix_not_found>
If `nix: command not found`: source the daemon profile first.
`. /nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh`
Then retry the rebuild command.
</nix_not_found>

<dry_run>
Validate configuration before applying. Substitute USER with actual username from session:

NixOS: `nix build ~/.dotfiles#nixosConfigurations.USER.config.system.build.toplevel --dry-run`
Non-NixOS: `home-manager build --flake ~/.dotfiles#USER@x86_64-linux --dry-run`

Dry-run catches syntax errors, missing imports, and evaluation failures without modifying the system.
</dry_run>

<platform_difference>
NixOS: Full system rebuild with `sudo nixos-rebuild switch --flake`. Requires sudo. Affects system services, kernel, boot. Home-manager is integrated as a module.

Home-manager standalone: User-level only with `home-manager switch --flake`. No sudo needed. Affects user packages, dotfiles, services.

Detection: Check `/etc/os-release` for `ID=nixos`, or use OS from session-context. The bin/rebuild script handles this automatically.
</platform_difference>

<workflow>
1. Make .nix file changes
2. Stage changed files: `git add path/to/changed.nix`
3. Dry-run to validate: use command from <dry_run> with correct username
4. If dry-run passes, apply: `./bin/rebuild`
5. Verify changes took effect

On NixOS: May need to ask user to run rebuild (requires sudo).
On home-manager standalone: Execute directly, no sudo needed.
</workflow>

<troubleshooting>
Build fails with import error: Check file exists and is staged (`git status`).
Attribute not found: Verify module is imported in appropriate home.nix or configuration.nix. Check flake has matching config for username.
Unfree package error: Check NIXPKGS_ALLOW_UNFREE=1 is set (bin/rebuild does this).
Rate limit errors: Install home-manager locally: `nix profile install nixpkgs#home-manager`.
Wrong user config: Check session-context User field matches flake configuration name.
</troubleshooting>

<post_rebuild>
After rebuild, verify changes applied. Test it and check services are running, dotfiles updated, packages installed as expected.
If issues arise, review rebuild output for errors. Re-run dry-run to catch config problems.
</post_rebuild>