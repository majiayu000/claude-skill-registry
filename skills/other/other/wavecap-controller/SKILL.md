---
name: wavecap-controller
description: Control WaveCap-SDR server via MCP tools. Use when the user wants to tune frequencies, start/stop captures, manage channels, or control P25 trunking systems.
---

# WaveCap-SDR Controller

Control the WaveCap-SDR server using MCP (Model Context Protocol) tools. This skill enables AI-assisted radio tuning, capture management, and trunking system control.

## Prerequisites

1. **WaveCap-SDR server running** at `http://localhost:8087`
2. **MCP enabled** in `wavecapsdr.yaml`:
   ```yaml
   mcp:
     enabled: true
     api_key: your-secret-key
   ```
3. **Environment variable** set: `export WAVECAP_MCP_KEY=your-secret-key`

## Available MCP Tools

### Device Management

| Tool | Description |
|------|-------------|
| `list_devices` | List available SDR devices with capabilities |
| `refresh_devices` | Rescan for connected devices |
| `get_device_health` | Check SDRplay API service health |

### Capture Control

| Tool | Description |
|------|-------------|
| `list_captures` | List active RF captures |
| `create_capture` | Create new capture (device, freq, sample_rate, gain) |
| `get_capture` | Get capture details |
| `start_capture` | Start a capture |
| `stop_capture` | Stop a capture |
| `update_capture` | Update capture settings |

### Channel Control

| Tool | Description |
|------|-------------|
| `list_channels` | List channels for a capture |
| `create_channel` | Create demodulation channel (mode, offset, squelch) |
| `update_channel` | Update channel settings |
| `delete_channel` | Remove a channel |
| `get_channel_metrics` | Get RSSI, SNR, S-meter readings |

### P25 Trunking

| Tool | Description |
|------|-------------|
| `list_trunking_systems` | List configured trunking systems |
| `start_trunking` | Start a trunking system |
| `stop_trunking` | Stop a trunking system |
| `get_active_calls` | Get active voice calls |
| `get_talkgroups` | List talkgroups with aliases |

### Utilities

| Tool | Description |
|------|-------------|
| `get_recipes` | List available capture recipes |
| `identify_frequency` | Identify radio service by frequency |
| `get_system_health` | Overall system health check |

## Usage Examples

### Tune to NOAA Weather Radio

```
User: "Tune to NOAA weather on 162.475 MHz"

Steps:
1. Call create_capture with center_hz=162475000, sample_rate=250000
2. Call create_channel with offset_hz=0, mode="nbfm", name="NOAA Weather"
3. Call start_capture
```

### Monitor Marine VHF Channel 16

```
User: "Listen to marine distress channel"

Steps:
1. Call create_capture with center_hz=156800000, sample_rate=250000
2. Call create_channel with offset_hz=0, mode="nbfm", name="Ch 16 Distress"
3. Call start_capture
```

### Check Signal Quality

```
User: "How's the signal on my current channel?"

Steps:
1. Call list_captures to get capture ID
2. Call list_channels to get channel ID
3. Call get_channel_metrics to get RSSI, SNR, S-meter
```

### Start P25 Trunking

```
User: "Start monitoring the SA-GRN trunking system"

Steps:
1. Call list_trunking_systems to find system ID
2. Call start_trunking with system_id
3. Call get_active_calls to see current activity
```

## Frequency Reference

Common frequencies:
- **NOAA Weather**: 162.400-162.550 MHz (NBFM)
- **Marine VHF Ch 16**: 156.800 MHz (NBFM)
- **Aviation Guard**: 121.500 MHz (AM)
- **FRS/GMRS**: 462.5625-467.7125 MHz (NBFM)
- **2m Ham Calling**: 146.520 MHz (NBFM)

## Demodulation Modes

- `nbfm` - Narrowband FM (12.5-25 kHz, public safety, ham, marine)
- `wbfm` - Wideband FM (200 kHz, broadcast radio)
- `am` - Amplitude Modulation (aviation, shortwave)
- `usb` / `lsb` - Single Sideband (ham, marine HF)
- `p25` - P25 Phase 1 digital voice
- `dmr` - DMR digital voice
- `raw` - Raw IQ samples

## Troubleshooting

### MCP Connection Failed

1. Verify server is running: `curl http://localhost:8087/api/v1/health`
2. Check MCP is enabled in config
3. Verify API key matches environment variable

### No Devices Found

1. Call `refresh_devices` to rescan
2. Check `get_device_health` for SDRplay issues
3. Verify SDR is connected via USB

### Poor Signal Quality

1. Use `get_channel_metrics` to check SNR
2. Increase gain via `update_capture`
3. Adjust squelch via `update_channel`
