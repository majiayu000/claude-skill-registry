---
name: openrgb
description: Advanced OpenRGB integration for ambient computing — SDK server automation, remote display surfaces, presence indicators, notification channels, and event-driven effects using openrgb-python. Use when building RGB as an ambient interface layer, presence/notification systems, multi-host lighting coordination, or system-event-driven effects.
compatibility: Requires OpenRGB with SDK server enabled, openrgb-python (pip). Network features require hosts reachable over TCP. Linux recommended; partial Windows/macOS support.
metadata:
  author: zk
  version: "0.2"
---

# OpenRGB Ambient

*RGB as ambient interface — not decoration, but information substrate.*

## Overview

OpenRGB exposes a network-based SDK (default port 6742) that turns RGB hardware into a programmable ambient display. This skill covers the advanced integration layer: SDK server automation, remote display surfaces, presence indicators, ambient notification channels, and event-driven effects via the `openrgb-python` library.

The core insight: every RGB device on your network is an addressable pixel in a distributed ambient display. OpenRGB's SDK makes them programmable. This skill makes them meaningful.

## Architecture Patterns

### Single Host

Simplest case — one machine runs OpenRGB server and the ambient daemon:

```
┌──────────────────────┐
│  Event Sources       │
│  systemd·git·idle    │
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│  ambient-rgbd        │
│  event → color       │
│  OpenRGB SDK client  │
└──────────┬───────────┘
           │ localhost:6742
           ▼
┌──────────────────────┐
│  OpenRGB Server      │
│  RGB devices         │
└──────────────────────┘
```

### Collector → Display (recommended for multi-host)

Separate the event collection from the display surface. A headless collector aggregates events from across the network and pushes color state to a dedicated display host over the SDK.

```
  workstation(s)              collector (headless)
  ┌──────────────┐            ┌──────────────────────┐
  │ local events │            │ network-wide events   │
  │ git·build·   │            │ systemd·docker·       │
  │ idle         │            │ inference·sensors     │
  └──────┬───────┘            └──────────┬───────────┘
         │ (push to collector             │
         │  or direct to display)         │
         └──────────┐    ┌───────────────┘
                    ▼    ▼
              ┌──────────────┐
              │  collector   │  ambient-rgbd
              │  event →     │  (aggregation + state)
              │  color       │
              └──────┬───────┘
                     │ OpenRGB SDK (TCP :6742)
                     ▼
              ┌──────────────┐
              │  display     │  OpenRGB server
              │  host        │  (RGB hardware)
              └──────────────┘
```

The display host runs `openrgb --server` and owns the hardware. The collector runs the ambient daemon and connects as an SDK client. Workstations can push events to the collector or connect directly to the display for low-latency local feedback.

## Server Setup

### Starting the SDK Server

```bash
# Foreground (testing)
openrgb --server --server-port 6742

# With auto-start on boot, use your init system (systemd, etc.)
# The --server flag enables the SDK listener; --noautoconnect is for CLI-only use
```

### Linux systemd Service

```ini
# /etc/systemd/system/openrgb-server.service
[Unit]
Description=OpenRGB SDK Server
After=network.target

[Service]
ExecStart=/usr/bin/openrgb --server --server-port 6742
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

### NixOS Declarative

```nix
services.hardware.openrgb = {
  enable = true;
  package = pkgs.openrgb-with-all-plugins;
  motherboard = "amd"; # or "intel"
  server.port = 6742;
};
boot.kernelModules = [ "i2c-dev" ];
hardware.i2c.enable = true;
```

### Firewall Considerations

The SDK server listens on TCP. For remote access, open the port only to trusted networks:

```bash
# iptables example — restrict to a VPN/mesh interface
iptables -A INPUT -i tailscale0 -p tcp --dport 6742 -j ACCEPT
iptables -A INPUT -p tcp --dport 6742 -j DROP
```

## Python SDK Patterns

### Connection

```python
from openrgb import OpenRGBClient
from openrgb.utils import RGBColor, DeviceType

# Local server
client = OpenRGBClient()

# Remote server (display host)
client = OpenRGBClient("192.168.1.50", 6742, name="ambient-engine")
```

### Display Client with Reconnect

```python
from openrgb import OpenRGBClient
from openrgb.utils import RGBColor

class DisplayClient:
    """SDK client targeting a single display host, with reconnect."""

    def __init__(self, host: str = "localhost", port: int = 6742):
        self.host = host
        self.port = port
        self.client: OpenRGBClient | None = None

    def connect(self) -> bool:
        try:
            self.client = OpenRGBClient(self.host, self.port, name="ambient-rgbd")
            return True
        except (ConnectionRefusedError, OSError):
            self.client = None
            return False

    def ensure_connected(self) -> bool:
        if self.client is None:
            return self.connect()
        return True

    def set_color(self, color: RGBColor):
        if self.ensure_connected():
            self.client.set_color(color)

    def set_device(self, index: int, color: RGBColor):
        if self.ensure_connected():
            self.client.devices[index].set_color(color)

    def load_profile(self, name: str):
        if self.ensure_connected():
            self.client.load_profile(name)

    def off(self):
        self.set_color(RGBColor(0, 0, 0))
```

### Multi-Display Pool

When multiple hosts have RGB hardware:

```python
class DisplayPool:
    """Manage connections to multiple display hosts."""

    def __init__(self, hosts: dict[str, str], port: int = 6742):
        self.displays: dict[str, DisplayClient] = {}
        for name, ip in hosts.items():
            self.displays[name] = DisplayClient(ip, port)

    def set_all(self, color: RGBColor):
        for d in self.displays.values():
            d.set_color(color)

    def set_host(self, name: str, color: RGBColor):
        if name in self.displays:
            self.displays[name].set_color(color)

    def off(self):
        self.set_all(RGBColor(0, 0, 0))
```

## Palette Abstraction

The ambient system uses semantic color roles, not hardcoded hex values. Define a palette as a dict mapping role names to hex strings, then load it once:

```python
from openrgb.utils import RGBColor

def load_palette(palette: dict[str, str]) -> dict[str, RGBColor]:
    """Convert a hex palette dict into RGBColor objects."""
    return {k: RGBColor.fromHEX(v) for k, v in palette.items()}
```

### Example Palettes

```python
CATPPUCCIN_MOCHA = {
    "green": "#a6e3a1", "mauve": "#cba6f7", "yellow": "#f9e2af",
    "peach": "#fab387", "red": "#f38ba8", "sapphire": "#74c7ec",
    "blue": "#89b4fa", "base": "#1e1e2e", "crust": "#11111b",
}

DRACULA = {
    "green": "#50fa7b", "mauve": "#bd93f9", "yellow": "#f1fa8c",
    "peach": "#ffb86c", "red": "#ff5555", "sapphire": "#8be9fd",
    "blue": "#6272a4", "base": "#282a36", "crust": "#191a21",
}

NORD = {
    "green": "#a3be8c", "mauve": "#b48ead", "yellow": "#ebcb8b",
    "peach": "#d08770", "red": "#bf616a", "sapphire": "#88c0d0",
    "blue": "#5e81ac", "base": "#2e3440", "crust": "#242933",
}

PAL = load_palette(CATPPUCCIN_MOCHA)  # swap freely
```

All code below references `PAL["green"]`, `PAL["red"]`, etc. — the palette is the only thing you change to retheme the entire ambient system.

## Presence Indicators

Use RGB to signal machine state, user presence, or workload.

### Semantic State → Palette Role

States map to palette role names, not hex values. The active palette resolves the actual color.

| State | Palette Role | Meaning |
|-------|-------------|---------|
| Available | `green` | Active, accepting input |
| Focused | `mauve` | Deep work, do not disturb |
| Away | `yellow` | Stepped away |
| Building | `peach` | Compilation / heavy workload |
| Error | `red` | Something needs attention |
| Sleeping | `crust` | Machine idle / suspended |
| Inference | `sapphire` | LLM inference running |

### Presence Detection

```python
import subprocess

def get_presence_state() -> str:
    """Determine current presence from system signals. Adapt to your environment."""

    # Screen locked / idle (freedesktop screensaver D-Bus)
    idle = subprocess.run(
        ["busctl", "--user", "get-property",
         "org.freedesktop.ScreenSaver", "/org/freedesktop/ScreenSaver",
         "org.freedesktop.ScreenSaver", "GetActive"],
        capture_output=True, text=True
    )
    if "true" in idle.stdout:
        return "away"

    # High CPU load (build running)
    load = float(open("/proc/loadavg").read().split()[0])
    if load > 4.0:
        return "building"

    # Active network connections on a known service port (e.g. LLM inference)
    # Adapt the port to whatever service you want to monitor
    active = subprocess.run(
        ["ss", "-tn", "sport", "=", ":1234"],
        capture_output=True, text=True
    )
    if active.stdout.strip().count("\n") > 1:
        return "inference"

    return "available"
```

### Applying Presence

```python
STATE_ROLES = {
    "available": "green",
    "focused":   "mauve",
    "away":      "yellow",
    "building":  "peach",
    "error":     "red",
    "sleeping":  "crust",
    "inference": "sapphire",
}

def state_to_color(state: str, pal: dict[str, RGBColor]) -> RGBColor:
    role = STATE_ROLES.get(state)
    if role and role in pal:
        return pal[role]
    return RGBColor(0, 0, 0)
```

## Ambient Notifications

Flash or pulse RGB to signal events without interrupting flow.

### Notification Patterns

| Pattern | Implementation | Use Case |
|---------|---------------|----------|
| Flash | Set color → delay → restore | Transient alert (mail, message) |
| Pulse | Fade in → fade out → restore | Gentle notification |
| Sweep | Color wave across devices | Build complete, deploy success |
| Persist | Set and hold until cleared | Error state, needs attention |

### Flash Implementation

```python
import time
from openrgb import OpenRGBClient
from openrgb.utils import RGBColor

def flash(client: OpenRGBClient, color: RGBColor,
          duration: float = 0.3, count: int = 3):
    """Flash all devices. Non-destructive (restores prior state)."""
    snapshots = []
    for dev in client.devices:
        snapshots.append([led.color for led in dev.leds])

    for _ in range(count):
        client.set_color(color)
        time.sleep(duration)
        for dev, colors in zip(client.devices, snapshots):
            dev.set_colors(colors)
        time.sleep(duration)
```

### Systemd OnFailure Integration

Wire RGB alerts to service failures. The alert script connects to the display host (remote or local):

```ini
# /etc/systemd/system/rgb-alert@.service
[Unit]
Description=RGB alert for %i failure

[Service]
Type=oneshot
ExecStart=/usr/bin/python3 /opt/ambient/flash-alert.py
```

```python
# /opt/ambient/flash-alert.py
from openrgb import OpenRGBClient
from openrgb.utils import RGBColor
import time

DISPLAY_HOST = "192.168.1.50"  # your display host
c = OpenRGBClient(DISPLAY_HOST, 6742, name="rgb-alert")
alert = RGBColor.fromHEX("#ff5555")  # palette red
dark  = RGBColor.fromHEX("#282a36")  # palette base
for _ in range(5):
    c.set_color(alert); time.sleep(0.2)
    c.set_color(dark);  time.sleep(0.2)
```

Wire to any service: `systemd.services.my-service.unitConfig.OnFailure = "rgb-alert@%n.service"`

## Event-Driven Effects

### Git Hook

```bash
#!/usr/bin/env bash
# .git/hooks/post-commit
python3 -c "
from openrgb import OpenRGBClient
from openrgb.utils import RGBColor
import time
c = OpenRGBClient('${OPENRGB_HOST:-localhost}', 6742, name='git-hook')
c.set_color(RGBColor.fromHEX('#50fa7b'))  # palette green
time.sleep(1.5)
" &
```

Uses `$OPENRGB_HOST` env var so it works locally or pointed at a remote display.

### Build Status Wrapper

```python
"""Wrap any command — reflect build status in RGB."""
import subprocess, sys
from openrgb import OpenRGBClient
from openrgb.utils import RGBColor

def build_watch(cmd: list[str], pal: dict[str, RGBColor],
                host: str = "localhost", port: int = 6742):
    client = OpenRGBClient(host, port, name="build-watch")
    client.set_color(pal["peach"])   # building

    result = subprocess.run(cmd)

    if result.returncode == 0:
        client.set_color(pal["green"])  # success
    else:
        client.set_color(pal["red"])    # failure

    return result.returncode

if __name__ == "__main__":
    import os
    from ambient_palette import PAL  # your palette module
    host = os.environ.get("OPENRGB_HOST", "localhost")
    sys.exit(build_watch(sys.argv[1:], PAL, host=host))
```

Usage: `OPENRGB_HOST=192.168.1.50 python build_watch.py make -j8`

## Profile Management

OpenRGB profiles save/restore complete device state. Use them as named ambient modes.

```python
def apply_ambient_mode(client: OpenRGBClient, mode: str):
    """Apply a named ambient mode via OpenRGB profiles."""
    profiles = {
        "work":    "ambient-work",
        "chill":   "ambient-chill",
        "night":   "ambient-night",
        "off":     "ambient-off",
        "meeting": "ambient-meeting",
    }
    profile_name = profiles.get(mode)
    if profile_name:
        client.load_profile(profile_name)
```

Create profiles in OpenRGB GUI, save with `ambient-*` naming convention, then load programmatically.

## Daemon Skeleton

A minimal ambient daemon that ties presence, notifications, and display targeting together:

```python
"""ambient-rgbd — ambient RGB daemon."""
import os, time, signal
from openrgb import OpenRGBClient
from openrgb.utils import RGBColor

POLL_INTERVAL = int(os.environ.get("AMBIENT_POLL", "5"))
DISPLAY_HOST  = os.environ.get("OPENRGB_HOST", "localhost")
DISPLAY_PORT  = int(os.environ.get("OPENRGB_PORT", "6742"))

DEFAULT_PALETTE = {
    "green": "#a6e3a1", "mauve": "#cba6f7", "yellow": "#f9e2af",
    "peach": "#fab387", "red": "#f38ba8", "sapphire": "#74c7ec",
    "base": "#1e1e2e", "crust": "#11111b",
}

STATE_ROLES = {
    "available": "green", "focused": "mauve", "away": "yellow",
    "building": "peach", "error": "red", "inference": "sapphire",
}

class AmbientDaemon:
    def __init__(self, host: str = DISPLAY_HOST, port: int = DISPLAY_PORT,
                 palette: dict[str, str] | None = None):
        self.client = OpenRGBClient(host, port, name="ambient-rgbd")
        self.pal = {k: RGBColor.fromHEX(v)
                    for k, v in (palette or DEFAULT_PALETTE).items()}
        self.running = True
        self.current_state = None
        signal.signal(signal.SIGTERM, self._shutdown)
        signal.signal(signal.SIGINT, self._shutdown)

    def _shutdown(self, signum, frame):
        self.running = False

    def get_state(self) -> str:
        """Override with your presence detection logic."""
        return "available"

    def state_to_color(self, state: str) -> RGBColor:
        role = STATE_ROLES.get(state)
        if role and role in self.pal:
            return self.pal[role]
        return RGBColor(0, 0, 0)

    def run(self):
        while self.running:
            state = self.get_state()
            if state != self.current_state:
                self.client.set_color(self.state_to_color(state))
                self.current_state = state
            time.sleep(POLL_INTERVAL)
        self.client.set_color(RGBColor(0, 0, 0))

if __name__ == "__main__":
    AmbientDaemon().run()
```

Configure via environment:
```bash
OPENRGB_HOST=192.168.1.50 OPENRGB_PORT=6742 AMBIENT_POLL=5 python ambient-rgbd.py
```

## CLI Quick Reference

```bash
# Start SDK server
openrgb --server --server-port 6742

# List devices
openrgb --noautoconnect --list-devices

# Set all devices to a color
openrgb --noautoconnect --color ff5555

# Set specific device
openrgb --noautoconnect --device 0 --mode static --color 50fa7b

# Load a profile
openrgb --noautoconnect --profile ambient-work

# All off
openrgb --noautoconnect --mode static --color 000000
```

## Integration Points

| System | Integration | Pattern |
|--------|------------|---------|
| Wayland/X11 | Idle detection → presence | D-Bus screensaver signal → away state |
| systemd | Service failure → flash | `OnFailure=rgb-alert@%n.service` |
| VPN/mesh | Peer status → color coding | Poll peer status, map to palette roles |
| LLM servers | Inference activity → sapphire | Socket connection count on service port |
| Git | Commit/push → sweep | Post-commit hook |
| Build systems | Build status → peach/green/red | Wrapper script around build command |
| Docker | Container events → notification | `docker events` stream |
| Sensors | Temperature/load → gradient | Map numeric range to color interpolation |

## Related Skills

- [catppuccin-theming](../catppuccin-theming/SKILL.md) — One possible palette source
- [agent-steering](../agent-steering/SKILL.md) — Hook patterns for agent-triggered RGB events

## Resources

- [OpenRGB SDK documentation](https://openrgb.org/sdk.html)
- [openrgb-python docs](https://openrgb-python.readthedocs.io/en/latest/)
- [OpenRGB Effects Plugin](https://codeberg.org/OpenRGB/OpenRGBEffectsPlugin)
- [NixOS OpenRGB wiki](https://wiki.nixos.org/wiki/OpenRGB)
- [openrgb-python on PyPI](https://pypi.org/project/openrgb-python/)

---

*Every LED is an addressable pixel in a distributed ambient display.* 🌈
