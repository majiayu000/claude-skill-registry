---
description: Camera, GPIO, and hardware integration for Raspberry Pi 5. Use for camera testing, hardware diagnostics, GPIO troubleshooting, and sensor issues.
auto-activation-keywords:
  - camera
  - gpio
  - hardware
  - sensor
  - raspberry
  - pi5
  - capture
  - diagnostic
  - usb
  - device
  - peripheral
---

# Hardware Integration Skill

Complete reference for camera, GPIO, USB, and hardware integration on Raspberry Pi 5 for the PhotoBooth application.

## Quick Reference

- **Camera**: iPad via getUserMedia (browser-based capture)
- **Printer**: Canon Selphy CP1500 via USB/CUPS
- **Network**: Wi-Fi AP mode (hostapd)
- **Storage**: 256GB microSD

## Raspberry Pi 5 Specifications

| Component | Specification |
|-----------|---------------|
| CPU | Broadcom BCM2712, Quad-core Cortex-A76 @ 2.4GHz |
| RAM | 8GB LPDDR4X |
| USB | 2x USB 3.0, 2x USB 2.0 |
| GPIO | 40-pin header, 26 GPIO pins |
| Network | Gigabit Ethernet, Wi-Fi 5 (802.11ac), Bluetooth 5.0 |

## Camera Integration

The PhotoBooth uses iPad Air as the camera device via browser's getUserMedia API.

### Camera Constraints (Frontend)
```typescript
const constraints: MediaStreamConstraints = {
  video: {
    facingMode: 'user',           // Front camera for selfies
    width: { ideal: 1920 },       // Full HD
    height: { ideal: 1080 },
    frameRate: { ideal: 30 }
  },
  audio: false
};
```

### Camera Testing
```bash
# On iPad (Safari DevTools):
# Check getUserMedia support
navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => console.log('Camera OK'))
  .catch(err => console.error('Camera Error:', err));
```

## USB Device Management

### List USB Devices
```bash
# List all USB devices
lsusb

# Detailed info
lsusb -v | grep -A 10 "Canon"

# Check USB device tree
lsusb -t
```

### USB Troubleshooting
```bash
# Check kernel messages for USB
dmesg | grep -i usb | tail -20

# Reset USB bus (if device not responding)
sudo usbreset /dev/bus/usb/001/002  # Replace with actual device
```

## Network (Wi-Fi AP Mode)

### Configuration Files
- `/etc/hostapd/hostapd.conf` - AP configuration
- `/etc/dnsmasq.conf` - DHCP configuration
- `/etc/dhcpcd.conf` - Static IP for wlan0

### hostapd Configuration
```conf
interface=wlan0
driver=nl80211
ssid=photobooth
hw_mode=g
channel=7
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=photobooth-1998
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
```

### Network Testing
```bash
# Check Wi-Fi AP status
sudo systemctl status hostapd

# List connected clients
iw dev wlan0 station dump

# Check IP assignments
cat /var/lib/misc/dnsmasq.leases
```

## System Diagnostics

### Temperature Monitoring
```bash
# CPU temperature
vcgencmd measure_temp

# Continuous monitoring
watch -n 1 vcgencmd measure_temp
```

### Memory and CPU
```bash
# Memory usage
free -h

# CPU usage
top -bn1 | head -20

# Disk usage
df -h
```

### Service Status
```bash
# Check all PhotoBooth services
sudo systemctl status hostapd
sudo systemctl status dnsmasq
sudo systemctl status cups
sudo systemctl status photobooth-backend
sudo systemctl status photobooth-frontend
```

## Common Issues & Solutions

### Issue: Camera not accessible from browser
**Cause**: HTTPS required for getUserMedia on non-localhost
**Solution**:
1. Use self-signed certificate for HTTPS
2. Or add exception in Safari settings
3. Or use localhost with port forwarding

### Issue: USB device not detected
**Cause**: Power issues or driver problems
**Solution**:
```bash
# Check USB power
vcgencmd get_throttled

# Reload USB driver
sudo modprobe -r usb_storage && sudo modprobe usb_storage

# Check dmesg for errors
dmesg | tail -50
```

### Issue: Wi-Fi AP not starting
**Cause**: Interface conflict or config error
**Solution**:
```bash
# Check for conflicts
sudo rfkill list

# Unblock if blocked
sudo rfkill unblock wifi

# Restart hostapd
sudo systemctl restart hostapd
```

### Issue: High CPU temperature
**Cause**: Inadequate cooling or high load
**Solution**:
```bash
# Check temperature
vcgencmd measure_temp

# If > 80°C, reduce CPU frequency temporarily
echo 1500000 | sudo tee /sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq
```

## Hardware Test Script

Create `/home/pi/scripts/test-hardware.sh`:
```bash
#!/bin/bash
echo "=== PhotoBooth Hardware Diagnostics ==="
echo ""
echo "CPU Temperature: $(vcgencmd measure_temp)"
echo "Memory: $(free -h | grep Mem | awk '{print $3"/"$2}')"
echo "Disk: $(df -h / | tail -1 | awk '{print $3"/"$2" ("$5" used)"}')"
echo ""
echo "=== USB Devices ==="
lsusb | grep -v "hub" || echo "No non-hub USB devices"
echo ""
echo "=== Network ==="
echo "Wi-Fi AP: $(systemctl is-active hostapd)"
echo "DHCP: $(systemctl is-active dnsmasq)"
echo "Connected clients: $(iw dev wlan0 station dump 2>/dev/null | grep Station | wc -l)"
echo ""
echo "=== Services ==="
echo "CUPS: $(systemctl is-active cups)"
echo "Backend: $(systemctl is-active photobooth-backend 2>/dev/null || echo 'not configured')"
echo ""
echo "=== Diagnostics Complete ==="
```

## Related Documentation

- `docs/DEPLOYMENT.md` - Full deployment guide
- `docs/ERROR_CODES.md` - Hardware error codes (PRINTER_*, STORAGE_*)
- `docs/use-cases/UC-205-health-check.md` - Health monitoring
