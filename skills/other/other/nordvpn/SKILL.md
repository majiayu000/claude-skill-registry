---
name: nordvpn
description: Control NordVPN on Linux via the `nordvpn` CLI (connect/disconnect, choose country/city/group, read status, tweak settings, manage allowlist). Use for automation that needs region routing or temporary VPN tunneling.
homepage: https://nordvpn.com/
---

# NordVPN CLI Skill (Linux)

A ClawBot skill for controlling the **NordVPN Linux CLI** (`nordvpn`) to connect/disconnect, select locations, verify status, and adjust settings from automations and workflows.

## Assumptions / Compatibility

* Works with the official `nordvpn` CLI (example shown: **4.3.1 [snap]**).
* Requires the NordVPN daemon running (usually `nordvpnd`) and sufficient permissions.
* Some commands may require elevated privileges depending on distro + install method (snap vs deb).

## Installation

### Option A: Snap (common on Ubuntu)

```bash
sudo snap install nordvpn
nordvpn --version
```

### Option B: Distro package / repo (varies)

If you installed via Nord’s repo or a package manager, just verify:

```bash
which nordvpn
nordvpn --version
```

### Verify daemon is running

```bash
# systemd installs usually
systemctl status nordvpnd --no-pager || true

# snap installs may not expose systemd unit the same way
nordvpn status || true

# or may require the full patch to be specified like so
/snap/bin/nordvpn status || true
```

## Authentication / Login

NordVPN CLI typically requires logging in once per machine/user session.

```bash
nordvpn login
```

If the environment is headless, the CLI will guide you through the login flow (often via a browser link / code). After login, confirm:

```bash
nordvpn account
nordvpn status
```

**ClawBot guidance:** treat login as a manual prerequisite unless you explicitly automate the browser-based login flow.

## Quick Reference

### Status

```bash
nordvpn status
```

### Connect (best available)

```bash
nordvpn connect
# alias:
nordvpn c
```

### Connect to a country / city / group

```bash
# country
nordvpn connect Sweden

# city (must exist in `nordvpn cities <country>`)
nordvpn connect "Stockholm"

# group (must exist in `nordvpn groups`)
nordvpn connect P2P
```

### Disconnect

```bash
nordvpn disconnect
# alias:
nordvpn d
```

### List locations

```bash
nordvpn countries
nordvpn cities Sweden
nordvpn groups
```

### Settings (read + change)

```bash
nordvpn settings

# examples (options differ by version)
nordvpn set autoconnect on
nordvpn set killswitch on
nordvpn set threatprotectionlite on  # if supported
nordvpn set protocol nordlynx        # if supported
```

### Allowlist (bypass VPN for certain traffic)

```bash
# view help
nordvpn allowlist --help

# examples (subcommands differ by version)
nordvpn allowlist add port 22
nordvpn allowlist add subnet 192.168.0.0/16
nordvpn allowlist remove port 22
```

## Skill Design

### What this skill should do well

1. **Idempotent connection actions**

   * If already connected to the requested target, do nothing (or return “already connected”).
   * If connected elsewhere, optionally disconnect then connect to target.
2. **Reliable verification**

   * After connect/disconnect, always run `nordvpn status` and parse the result.
3. **Safe fallbacks**

   * If a requested city/country/group is invalid, provide closest alternatives by listing:

     * `nordvpn countries`
     * `nordvpn cities <country>`
     * `nordvpn groups`
4. **Human-in-the-loop login**

   * If `nordvpn` reports not logged in, return a structured response instructing to run `nordvpn login`.

### Recommended “actions” (API surface)

Implement these as the skill’s callable intents/tools:

* `status()` → returns parsed connection status
* `connect_best()` → connects to best available
* `connect_country(country)`
* `connect_city(city)` (optionally with `country` for disambiguation)
* `connect_group(group)`
* `disconnect()`
* `list_countries()`
* `list_cities(country)`
* `list_groups()`
* `get_settings()`
* `set_setting(key, value)`
* `allowlist_add(type, value)`
* `allowlist_remove(type, value)`

## Suggested Implementation Pattern (CLI orchestration)

### 1) Always start with status

```bash
nordvpn status
```

Parse fields commonly returned by the CLI, such as:

* Connection state (Connected/Disconnected)
* Current server / country / city
* IP, protocol, technology

### 2) Connect flow

**Goal:** connect to a target (country/city/group) with verification.

Pseudo-logic:

* Run `nordvpn status`
* If disconnected → connect directly
* If connected to different target → `nordvpn disconnect` then connect
* Run `nordvpn status` again and confirm connected

Commands:

```bash
nordvpn connect "<target>"
nordvpn status
```

### 3) Disconnect flow

```bash
nordvpn disconnect
nordvpn status
```

### 4) Resolve targets safely

If user asks for a city:

* Prefer `nordvpn cities <country>` when country is known
* Otherwise attempt connect; if it fails, list countries and search-like suggestions.

```bash
nordvpn countries
nordvpn cities "<country>"
nordvpn groups
```

## Common Errors & Handling

### Not logged in

Symptoms:

* CLI complains about authentication/account/login.

Handling:

* Return: “Login required. Run `nordvpn login` and repeat.”
* Optionally: run `nordvpn account` to confirm.

### Daemon not running / permission denied

Symptoms:

* Can’t connect, service errors, permission errors.

Handling:

* Check `systemctl status nordvpnd` (systemd installs)
* Confirm snap service health (snap installs vary)
* Ensure user belongs to the right group (some installs use a `nordvpn` group):

  ```bash
  groups
  getent group nordvpn || true
  ```

### Invalid location/group

Symptoms:

* “Unknown country/city/group” or connect fails immediately.

Handling:

* Provide available options:

  ```bash
  nordvpn countries
  nordvpn groups
  nordvpn cities "<country>"
  ```

## Practical Automation Recipes

### Ensure VPN is connected (any server)

```bash
nordvpn status | sed -n '1,10p'
nordvpn connect
nordvpn status | sed -n '1,15p'
```

### Reconnect to a specific country

```bash
nordvpn disconnect
nordvpn connect Sweden
nordvpn status
```

### Toggle killswitch (example)

```bash
nordvpn set killswitch on
nordvpn settings
```

## Notes

* Command options and setting keys can differ by NordVPN CLI version. Always rely on:

  ```bash
  nordvpn help
  nordvpn set --help
  nordvpn allowlist --help
  ```
* If you need stable machine-readable output, the NordVPN CLI does not consistently provide JSON; plan to parse human-readable status text defensively (line-based key/value extraction, tolerate missing fields).
