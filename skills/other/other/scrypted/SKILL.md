---
name: scrypted
description: "Build Scrypted plugins for home automation. Create camera integrations, automations, and smart home bridges. Use for HomeKit, Google Home, and Alexa integrations."
---

# Scrypted Skill

Complete guide for Scrypted - the home video integration platform.

## Quick Reference

### Key Features
| Feature | Description |
|---------|-------------|
| **HKSV** | HomeKit Secure Video with local processing |
| **Google Home** | Camera streaming to Google ecosystem |
| **Alexa** | Camera streaming to Amazon ecosystem |
| **NVR** | Built-in recording and playback |
| **AI Detection** | Object detection (person, car, animal) |

### Access Points
```
http://<scrypted-ip>:10443  # Web interface
https://<scrypted-ip>:10443 # HTTPS
```

---

## 1. Installation

### Docker Installation (Recommended)
```yaml
services:
  scrypted:
    image: koush/scrypted:latest
    container_name: scrypted
    restart: unless-stopped
    network_mode: host
    volumes:
      - ./volume:/server/volume
      - /var/run/dbus:/var/run/dbus
      - /var/run/avahi-daemon/socket:/var/run/avahi-daemon/socket
    devices:
      # For hardware transcoding
      - /dev/dri:/dev/dri
      # For Coral TPU
      # - /dev/bus/usb:/dev/bus/usb
    environment:
      - SCRYPTED_WEBHOOK_UPDATE_AUTHORIZATION=Bearer YOUR_TOKEN
      - SCRYPTED_WEBHOOK_UPDATE=http://localhost:10444/v1/update
```

### Docker Compose with GPU
```yaml
services:
  scrypted:
    image: koush/scrypted:latest
    container_name: scrypted
    restart: unless-stopped
    network_mode: host
    volumes:
      - ./volume:/server/volume
    devices:
      - /dev/dri:/dev/dri  # Intel/AMD GPU
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

### Raspberry Pi
```bash
# Install via script
curl -s https://raw.githubusercontent.com/koush/scrypted/main/install/docker/install-scrypted-docker-compose.sh | bash
```

### npm Installation
```bash
# Install Node.js 18+
npm install -g @scrypted/server

# Run
npx scrypted serve
```

---

## 2. Initial Setup

### First Login
1. Navigate to `https://<ip>:10443`
2. Accept self-signed certificate warning
3. Create admin account
4. Complete setup wizard

### Add Camera
1. Click "+" to add device
2. Select camera brand or "Generic RTSP"
3. Enter camera URL and credentials
4. Configure detection and recording options

### Generic RTSP Camera
```
# RTSP URL format
rtsp://username:password@192.168.1.100:554/stream1

# Common paths:
# Hikvision: /Streaming/Channels/101
# Dahua: /cam/realmonitor?channel=1&subtype=0
# Amcrest: /cam/realmonitor?channel=1&subtype=0
# Reolink: /h264Preview_01_main
```

---

## 3. HomeKit Secure Video (HKSV)

### Enable HomeKit Plugin
1. Plugins > HomeKit
2. Install "HomeKit" plugin
3. Scan QR code with Apple Home app

### Configure HKSV
1. Select camera in Scrypted
2. Enable "HomeKit Secure Video" extension
3. In Apple Home: Camera settings > Recording Options
4. Enable "Stream & Allow Recording"

### HKSV Requirements
- Apple Home Hub (HomePod/Apple TV)
- iCloud+ subscription (50GB minimum)
- Supported resolution (1080p max for HKSV)

### Optimize for HKSV
```yaml
# Camera settings in Scrypted
Video Codec: H.264
Resolution: 1920x1080 (or lower)
Framerate: 30 fps
Bitrate: 2000-4000 kbps
Audio: AAC (if supported)
```

---

## 4. Google Home Integration

### Install Google Home Plugin
1. Plugins > Install "Google Home"
2. Link account in Google Home app
3. Add Scrypted as linked service

### Configure Cameras
1. Enable "Google Home" extension on camera
2. Camera appears in Google Home app
3. View on Nest displays and TV

### Supported Features
- Live streaming
- Talk back (2-way audio)
- Event notifications
- Doorbell announcements

---

## 5. Alexa Integration

### Install Alexa Plugin
1. Plugins > Install "Alexa"
2. Link in Alexa app
3. Discover devices

### Configure Cameras
1. Enable "Alexa" extension on camera
2. View on Echo Show devices
3. Enable doorbell announcements

---

## 6. NVR (Recording)

### Enable NVR Plugin
1. Plugins > Install "NVR"
2. Configure storage location
3. Set retention policies

### Storage Configuration
```yaml
# In Scrypted NVR settings
Storage Path: /server/volume/recordings
Retention Days: 7
Pre-Event Buffer: 10 seconds
Post-Event Buffer: 10 seconds
```

### Recording Modes
| Mode | Description |
|------|-------------|
| **Continuous** | Record everything |
| **Event** | Record on motion/detection |
| **Smart** | Record on AI detection (person, car, etc.) |

### View Recordings
1. Select camera > Timeline
2. Use timeline scrubber
3. Download clips as needed

---

## 7. Object Detection

### Built-in Detection
- Motion detection (basic)
- Uses camera's built-in analytics when available

### OpenCV Plugin
```yaml
# Install OpenCV plugin for AI detection
Plugins > OpenCV

# Detects:
- Person
- Car/Vehicle
- Animal
- Face
```

### Coral TPU Plugin
```yaml
# For Google Coral TPU acceleration
Plugins > TensorFlow Lite

# Docker device mapping
devices:
  - /dev/bus/usb:/dev/bus/usb  # USB Coral
  - /dev/apex_0:/dev/apex_0     # PCIe Coral
```

### OpenVINO Plugin (Intel)
```yaml
# For Intel CPU/GPU acceleration
Plugins > OpenVINO

# Best for Intel NUC, 6th gen+ processors
```

### Detection Zones
1. Select camera > Detection
2. Draw zones on camera view
3. Configure objects to detect per zone
4. Set sensitivity and thresholds

---

## 8. Two-Way Audio

### Requirements
- Camera with audio input
- Speaker/microphone support
- Compatible platform (HomeKit, Google, Alexa)

### Configuration
1. Enable audio on camera
2. Configure audio codec (AAC preferred)
3. Test in platform app

### Doorbell Configuration
```yaml
# Enable doorbell button detection
1. Camera settings > Doorbell
2. Map button press event
3. Configure chime behavior
```

---

## 9. Advanced Configuration

### Multiple Streams
```yaml
# Configure separate streams for different purposes
Main Stream: rtsp://....:554/stream1 (high quality, recording)
Sub Stream: rtsp://....:554/stream2 (low quality, detection)

# In camera settings
Recording Stream: Main
Detection Stream: Sub
Remote Stream: Sub
```

### Rebroadcast Plugin
```yaml
# Create reliable RTSP streams
Plugins > Rebroadcast

# Provides:
- RTSP re-streaming
- HLS output
- WebRTC output
- MPEG-DASH output
```

### Script Plugin
```javascript
// Custom automation script example
const camera = device;

camera.on('motionDetected', async () => {
  console.log('Motion detected!');
  // Trigger other actions
});
```

### Webhooks
```yaml
# Configure webhook notifications
1. Camera > Webhooks
2. Add webhook URL
3. Select events to trigger

# Webhook payload includes:
- Event type
- Camera ID
- Timestamp
- Thumbnail (optional)
```

---

## 10. Troubleshooting

### Common Issues

**Camera not connecting:**
```bash
# Test RTSP stream
ffprobe rtsp://user:pass@192.168.1.100:554/stream1

# Check Scrypted logs
docker logs scrypted

# Verify network connectivity
ping 192.168.1.100
```

**Poor streaming quality:**
```yaml
# Optimize camera settings
- Reduce resolution to 1080p
- Lower bitrate (2-4 Mbps)
- Use H.264 (not H.265)
- Enable hardware transcoding
```

**HomeKit issues:**
```bash
# Reset HomeKit pairing
1. Remove bridge from Apple Home
2. Scrypted > HomeKit plugin > Reset
3. Re-pair with QR code

# Check mDNS
avahi-browse -rt _hap._tcp
```

**High CPU usage:**
```yaml
# Enable hardware transcoding
1. Verify GPU passthrough in Docker
2. Install appropriate plugin (Intel/NVIDIA/AMD)
3. Select hardware transcoder in camera settings

# Reduce detection resolution
- Use sub-stream for detection
- Lower detection FPS
```

### Logs
```bash
# Docker logs
docker logs -f scrypted

# Scrypted console
# Web UI > Console tab

# Enable debug logging
# Settings > Logging > Debug
```

---

## 11. Performance Optimization

### Hardware Transcoding
```yaml
# Intel Quick Sync
devices:
  - /dev/dri:/dev/dri

# NVIDIA
deploy:
  resources:
    reservations:
      devices:
        - driver: nvidia
          count: 1
          capabilities: [gpu]
```

### Memory Management
```yaml
# Docker memory limits
deploy:
  resources:
    limits:
      memory: 4G
```

### Network Optimization
1. Use **wired connection** for Scrypted server
2. Place cameras on **dedicated VLAN**
3. Use **PoE** for reliable camera power
4. Configure **QoS** for video traffic

---

## Best Practices

1. **Use sub-streams** for detection (saves CPU)
2. **Enable hardware transcoding** when available
3. **Use HKSV** for Apple users (end-to-end encrypted)
4. **Set retention policies** to manage storage
5. **Configure zones** to reduce false positives
6. **Regular backups** of Scrypted configuration
7. **Update plugins** regularly for fixes and features
8. **Monitor resources** - cameras can be CPU intensive
9. **Use Coral TPU** for best AI detection performance
10. **Separate network** for cameras (security/performance)
