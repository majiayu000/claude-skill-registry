---
name: ipcam
title: "IP Camera - RTSP & ONVIF Control"
description: "ONVIF PTZ control + RTSP capture + camera discovery. Works with any ONVIF Profile S/T camera. Tested with TP-Link, Hikvision, Dahua, Reolink, Amcrest, Axis."
metadata:
  openclaw:
    emoji: "📹"
    version: "1.0.0"
    author: "tao"
    requires:
      bins: ["ffmpeg", "python3", "jq"]
      pip: ["onvif-zeep"]
    install:
      - id: "auto"
        kind: "script"
        label: "Run install.sh"
        instructions: "bash install.sh"
---

# IP Camera Skill

Control IP cameras via **RTSP** (snapshots, recording) and **ONVIF** (PTZ, presets, discovery).

Tested with TP-Link Tapo/Vigi. Works with Hikvision, Dahua, Reolink, Amcrest, Axis, and other ONVIF Profile S/T cameras.

## Setup

```bash
bash skills/ipcam/install.sh
```

Then either discover cameras automatically or configure manually:

```bash
# Auto-discover and add
ptz.py discover --add

# Or edit config
nano ~/.config/ipcam/config.json
```

### Config Format

```json
{
  "default": "front-door",
  "cameras": {
    "front-door": {
      "ip": "192.168.1.100",
      "username": "admin",
      "password": "secret",
      "rtsp_port": 554,
      "onvif_port": 2020,
      "rtsp_main_path": "stream1",
      "rtsp_sub_path": "stream2"
    }
  }
}
```

- `onvif_port`: 2020 (TP-Link), 80 (Hikvision/Dahua), 8000, 8080
- `rtsp_main_path` / `rtsp_sub_path`: auto-detect with `ptz.py stream-uri --save`
- Env overrides: `CAM_IP`, `CAM_USER`, `CAM_PASS`, `CAM_RTSP_PORT`, `CAM_ONVIF_PORT`

## Usage

### RTSP (`camera.sh`)

```bash
camera.sh snapshot                         # capture frame
camera.sh --cam cam2 snapshot /tmp/cam.jpg # specific camera
camera.sh record 15                        # record 15s clip
camera.sh stream-url sub                   # print sub-stream URL
camera.sh info                             # test connectivity
camera.sh list-cameras                     # list configured cameras
```

### PTZ (`ptz.py`)

```bash
ptz.py status                     # current position
ptz.py move left                  # pan left (speed 0.5, 0.5s)
ptz.py move zoomin 0.8 1.0        # zoom in, speed 0.8, 1s
ptz.py goto 0.5 -0.2 0.0          # absolute pan/tilt/zoom
ptz.py home                       # home position
ptz.py stop                       # stop movement
ptz.py preset list                # list presets
ptz.py preset goto 1              # go to preset 1
ptz.py preset set 2 "Door"        # save current pos as preset
```

### Discovery & Stream URI

```bash
ptz.py discover                   # scan network for ONVIF cameras
ptz.py discover --add             # scan and add to config
ptz.py stream-uri                 # query RTSP paths from ONVIF
ptz.py stream-uri --save          # save paths to config
```

Multi-camera: use `--cam <name>` with any command.

### Directions

`left`, `right`, `up`, `down`, `zoomin`, `zoomout`, `upleft`, `upright`, `downleft`, `downright`

## Troubleshooting

- **RTSP fails**: Check IP/port/firewall. Use `ptz.py stream-uri` to verify paths. Camera may limit concurrent RTSP connections (try closing other viewers).
- **ONVIF fails**: Verify ONVIF port and that ONVIF is enabled in camera web UI. Try common ports: 2020, 80, 8000, 8080.
- **No cameras found**: Ensure same subnet, ONVIF enabled, UDP multicast not blocked.
- **PTZ not working**: Not all cameras support PTZ. Check ONVIF Profile S support.
- **Auth error**: Check username/password. Special characters are URL-encoded automatically.
