---
name: nixos
description: Resolve NixOS issues using research and sequential thinking
---

Use nix-pro and nixos MCP to resolve the following issues with the current NixOS installation.

- Do not, under any circumstances, decrypt the SOPS secrets.yaml file. See the
  @CLAUDE.md file for extensive notes on this important security consideration.

- Use Web Search and Perplexity as need for research and discovering resources.

- Use sequential-thinking when appropriate to break down tasks further.

- Use context7 whenever code examples might help.

- Each time before you intend to build or switch to a new configuration, use
  `touch` a create a file named `/etc/nixos/.nixos-build`. Remove this file
  when the build or the switch is completed. If you see that this file already
  exists, wait for up to ten minutes, checking every 10 seconds during that
  time to see if the file has been removed. This way, multiple nixos jobs can
  be working with the system at the same time, but only one will be building
  or switching at any given time.
