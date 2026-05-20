---
name: raspberry-pi
cluster: iot
description: "Compact Linux board for IoT, prototyping, and edge computing"
tags: ["iot","raspberry"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "raspberry-pi iot"
---

# raspberry-pi

## Purpose
This skill enables the AI to interact with Raspberry Pi devices for IoT tasks, including remote management, hardware prototyping, and edge computing operations.

## When to Use
Use this skill for scenarios involving hardware setup, such as deploying sensors in a smart home, running lightweight servers for data processing, or testing embedded applications on a compact Linux board.

## Key Capabilities
- Establish SSH connections to execute commands on Raspberry Pi.
- Configure hardware settings, like GPIO pins, for physical interactions.
- Manage software installations and updates via apt.
- Monitor system resources and logs for edge computing tasks.
- Integrate with Python libraries for automation, e.g., RPi.GPIO for pin control.

## Usage Patterns
To accomplish tasks, first authenticate via SSH using environment variables like `$RASPI_HOST` and `$RASPI_SSH_KEY`. Then, run commands directly or invoke scripts. For repeated tasks, wrap commands in Python functions. Always check device connectivity before proceeding. For GPIO work, import relevant libraries and set pin modes explicitly.

## Common Commands/API
- Connect via SSH: `ssh pi@$RASPI_HOST -i $RASPI_SSH_KEY`
- Access configuration tool: `sudo raspi-config` (use options like "Boot Options" with flag `--expand-rootfs` for storage)
- Control GPIO pins in Python:
  ```python
  import RPi.GPIO as GPIO
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(17, GPIO.OUT)
  GPIO.output(17, GPIO.HIGH)
  ```
- Update and install packages: `sudo apt update && sudo apt install -y package-name` (e.g., `apache2` for a web server)
- Check system status: `vcgencmd measure_temp` to get CPU temperature, or `top` for resource usage.
- Config format for /boot/config.txt: Add lines like `dtparam=i2c_arm=on` to enable I2C, then reboot.

## Integration Notes
When integrating with other systems, set auth variables in your environment, e.g., `export RASPI_HOST=raspberrypi.local` and `export RASPI_SSH_KEY=/path/to/private.key`. For API-like interactions, use SSH wrappers in scripts. Ensure network compatibility; if behind a firewall, forward ports like 22 for SSH. For IoT ecosystems, pair with MQTT brokers by installing `mosquitto` and configuring via `/etc/mosquitto/mosquitto.conf` with lines like `listener 1883`.

## Error Handling
If SSH fails, verify connectivity with `ping $RASPI_HOST` and check key permissions (e.g., `chmod 600 $RASPI_SSH_KEY`). For GPIO errors, ensure RPi.GPIO is installed via `pip install RPi.GPIO` and handle exceptions like `GPIO.error` in code:
  ```python
  try:
      GPIO.setup(17, GPIO.OUT)
  except RuntimeError as e:
      print("Error: " + str(e) + " - Check user permissions")
  ```
For apt issues, use `apt --fix-broken install` to resolve dependencies. Always log errors with timestamps, e.g., via `echo "$(date): Error message" >> error.log`.

## Usage Examples
1. Set up and blink an LED on GPIO pin 17: First, SSH in with `ssh pi@$RASPI_HOST -i $RASPI_SSH_KEY`, then create a script file with `nano blink.py` and add:
   ```python
   import RPi.GPIO as GPIO
   import time
   GPIO.setmode(GPIO.BCM)
   GPIO.setup(17, GPIO.OUT)
   for _ in range(5):
       GPIO.output(17, True)
       time.sleep(1)
       GPIO.output(17, False)
       time.sleep(1)
   ```
   Run it with `python blink.py` to toggle the LED.

2. Deploy a basic web server for IoT monitoring: SSH into the device, update packages with `sudo apt update`, install Apache via `sudo apt install -y apache2`, then edit the default page at `/var/www/html/index.html` by adding content like `<h1>IoT Status: OK</h1>`. Access it via `http://$RASPI_HOST` in a browser, and monitor logs with `tail -f /var/log/apache2/access.log`.

## Graph Relationships
- Related to cluster: iot
- Connected skills: sensors (for GPIO integration), actuators (for hardware control), edge-computing (for resource monitoring)
