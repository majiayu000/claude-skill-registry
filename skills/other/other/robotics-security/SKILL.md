---
name: robotics-security
description: >
  Security hardening and best practices for robotic systems, covering SROS2 DDS security, network
  segmentation, secrets management, secure boot, and the physical-cyber safety intersection. Use
  this skill when securing ROS2 communications, configuring DDS encryption and access control,
  hardening robot onboard computers, managing certificates and credentials, setting up network
  segmentation for robot fleets, or addressing the unique security challenges where cyber
  vulnerabilities become physical safety risks. Trigger whenever the user mentions SROS2, DDS
  security, robot security, robot hardening, ROS2 encryption, ROS2 access control, robot
  network security, secure robot deployment, robot certificates, keystore generation, robot
  firewall, e-stop security, safety controller isolation, or IEC 62443 for robotics.
---

# Robotics Security Skill

## When to Use This Skill
- Enabling SROS2 encryption and access control on ROS2 topics/services
- Generating keystores, certificates, and security policies for DDS
- Hardening robot onboard computers (SSH, firewalls, minimal packages)
- Setting up network segmentation between robot control/data/management planes
- Managing secrets and credentials across a robot fleet
- Securing Docker containers running ROS2 nodes
- Designing e-stop and safety systems that survive cyber compromise
- Auditing a robot system for security vulnerabilities
- Implementing secure boot and firmware verification
- Addressing IEC 62443 requirements for industrial robot deployments

## The Robot Attack Surface

Robots are unique: cyber vulnerabilities become **physical** threats.

```
  NETWORK                    MIDDLEWARE                   APPLICATION
  ┌────────────────┐        ┌────────────────┐           ┌────────────────┐
  │ Open DDS ports │───────▶│ Unauthenticated│──────────▶│ Hardcoded      │
  │ (7400-7500)    │        │ /cmd_vel pub   │           │ credentials    │
  │ Unsegmented LAN│        │ No msg signing │           │ Unvalidated cmd│
  └────────────────┘        └────────────────┘           └────────────────┘
  PHYSICAL                   FIRMWARE                     SUPPLY CHAIN
  ┌────────────────┐        ┌────────────────┐           ┌────────────────┐
  │ USB/debug ports│───────▶│ Unsigned       │──────────▶│ Compromised    │
  │ Serial consoles│        │ firmware OTA   │           │ ROS packages   │
  │ Exposed SBCs   │        │ No secure boot │           │ Unverified imgs│
  └────────────────┘        └────────────────┘           └────────────────┘
```

| Vector | Impact |
|--------|--------|
| Unauthenticated `/cmd_vel` | Robot moves unexpectedly — injury/damage |
| Sensor spoofing (`/scan`, `/camera/image`) | Robot collides, wrong decisions |
| Open DDS multicast discovery | Full topic graph enumeration by passive listener |
| USB/serial physical access | Root shell, firmware flash, data exfiltration |
| Unsigned firmware update | Persistent backdoor in motor controllers |

## SROS2: DDS Security

SROS2 wraps DDS Security to provide authentication, encryption, and access control at the DDS layer.

### Keystore Generation and Certificate Setup

```bash
export ROS_SECURITY_KEYSTORE=~/sros2_keystore
ros2 security create_keystore ${ROS_SECURITY_KEYSTORE}

# Generate per-node enclaves (use exact fully-qualified node names)
ros2 security create_enclave ${ROS_SECURITY_KEYSTORE} /my_robot/camera_driver
ros2 security create_enclave ${ROS_SECURITY_KEYSTORE} /my_robot/navigation
ros2 security create_enclave ${ROS_SECURITY_KEYSTORE} /my_robot/motor_controller
ros2 security create_enclave ${ROS_SECURITY_KEYSTORE} /my_robot/teleop

# Result:
# sros2_keystore/
# ├── enclaves/my_robot/{camera_driver,navigation,...}/
# │   ├── cert.pem, key.pem          # Node identity
# │   ├── governance.p7s              # Signed governance
# │   └── permissions.p7s             # Signed permissions
# ├── public/ca.cert.pem              # CA certificate
# └── private/ca.key.pem              # CA private key — PROTECT THIS
```

### Security Policy XML

**Governance** — domain-wide security behavior:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<dds xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
     xsi:noNamespaceSchemaLocation="omg_shared_ca_governance.xsd">
  <domain_access_rules>
    <domain_rule>
      <domains><id_range><min>0</min><max>230</max></id_range></domains>
      <allow_unauthenticated_participants>false</allow_unauthenticated_participants>
      <enable_join_access_control>true</enable_join_access_control>
      <discovery_protection_kind>ENCRYPT</discovery_protection_kind>
      <liveliness_protection_kind>ENCRYPT</liveliness_protection_kind>
      <rtps_protection_kind>ENCRYPT</rtps_protection_kind>
      <topic_access_rules>
        <topic_rule>
          <topic_expression>*</topic_expression>
          <enable_discovery_protection>true</enable_discovery_protection>
          <enable_read_access_control>true</enable_read_access_control>
          <enable_write_access_control>true</enable_write_access_control>
          <metadata_protection_kind>ENCRYPT</metadata_protection_kind>
          <data_protection_kind>ENCRYPT</data_protection_kind>
        </topic_rule>
      </topic_access_rules>
    </domain_rule>
  </domain_access_rules>
</dds>
```

**Permissions** — per-enclave publish/subscribe rules:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<dds xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
     xsi:noNamespaceSchemaLocation="omg_shared_ca_permissions.xsd">
  <permissions>
    <grant name="/my_robot/motor_controller">
      <subject_name>CN=/my_robot/motor_controller</subject_name>
      <validity><not_before>2024-01-01T00:00:00</not_before>
                <not_after>2026-01-01T00:00:00</not_after></validity>
      <allow_rule>
        <domains><id>0</id></domains>
        <publish><topics><topic>rt/joint_states</topic></topics></publish>
        <subscribe><topics><topic>rt/cmd_vel</topic></topics></subscribe>
      </allow_rule>
      <default>DENY</default>
    </grant>
    <grant name="/my_robot/teleop">
      <subject_name>CN=/my_robot/teleop</subject_name>
      <validity><not_before>2024-01-01T00:00:00</not_before>
                <not_after>2026-01-01T00:00:00</not_after></validity>
      <allow_rule>
        <domains><id>0</id></domains>
        <publish><topics><topic>rt/cmd_vel</topic></topics></publish>
        <subscribe><topics><topic>rt/joy</topic></topics></subscribe>
      </allow_rule>
      <default>DENY</default>
    </grant>
  </permissions>
</dds>
```

### Enabling Security in Launch Files

```python
import os
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    security_env = {
        'ROS_SECURITY_KEYSTORE': os.path.expanduser('~/sros2_keystore'),
        'ROS_SECURITY_ENABLE': 'true',
        'ROS_SECURITY_STRATEGY': 'Enforce',  # Enforce=reject unauth, Permissive=warn only
    }
    return LaunchDescription([
        Node(package='my_robot_drivers', executable='motor_controller',
             name='motor_controller', namespace='my_robot',
             additional_env=security_env),
        Node(package='my_robot_nav', executable='navigation',
             name='navigation', namespace='my_robot',
             additional_env=security_env),
    ])
```

Always use `Enforce` in production. `Permissive` logs violations but allows them — debugging aid only.

### Per-Topic Access Control

Design with **least privilege**:

| Node | Publishes | Subscribes | Rationale |
|------|-----------|------------|-----------|
| `motor_controller` | `/joint_states` | `/cmd_vel` | Driver acts on velocity only |
| `navigation` | `/cmd_vel`, `/path` | `/scan`, `/odom`, `/map` | Nav reads sensors, writes commands |
| `camera_driver` | `/camera/image_raw` | (none) | Pure source — no subscriptions |
| `teleop` | `/cmd_vel` | `/joy` | Joystick passthrough — minimal surface |

A compromised `camera_driver` **cannot** publish to `/cmd_vel` — permissions deny it at the DDS layer.

## Network Hardening

### Network Segmentation

```
┌───────────────────┬──────────────────┬────────────────────────┐
│   CONTROL PLANE   │   DATA PLANE     │   MANAGEMENT PLANE     │
│   VLAN 10         │   VLAN 20        │   VLAN 30              │
│   10.10.10.0/24   │   10.10.20.0/24  │   10.10.30.0/24        │
├───────────────────┼──────────────────┼────────────────────────┤
│ /cmd_vel, /odom   │ /camera/image    │ SSH, Prometheus         │
│ /joint_states     │ /pointcloud      │ Log collection          │
│ /e_stop           │ /map, /rosbag    │ Fleet mgmt API          │
├───────────────────┼──────────────────┼────────────────────────┤
│ LOW LATENCY       │ HIGH BANDWIDTH   │ RESTRICTED ACCESS       │
│ QoS: RELIABLE     │ QoS: BEST_EFFORT │ Jump host / VPN + 2FA  │
└───────────────────┴──────────────────┴────────────────────────┘
```

Management plane is **never** reachable from data plane. Control plane traffic never transits WiFi.

### Firewall Rules for ROS2/DDS

```bash
#!/bin/bash
# firewall_ros2.sh — adapt interface names to your hardware
iptables -F && iptables -X

# Default: drop inbound, allow outbound
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

iptables -A INPUT -i lo -j ACCEPT                                    # Loopback (intra-process DDS)
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT      # Existing connections
iptables -A INPUT -p udp --dport 7400:7500 -s 10.10.10.0/24 -j ACCEPT  # DDS discovery — control VLAN
iptables -A INPUT -p udp --dport 7500:7700 -s 10.10.10.0/24 -j ACCEPT  # DDS user traffic
iptables -A INPUT -p tcp --dport 22 -s 10.10.30.0/24 -j ACCEPT         # SSH — mgmt VLAN only
iptables -A INPUT -i wlan0 -d 239.255.0.0/16 -j DROP                   # Block multicast on WiFi
iptables -A INPUT -j LOG --log-prefix "DROPPED: " --log-level 4
iptables -A INPUT -j DROP
iptables-save > /etc/iptables/rules.v4
```

### VLAN Configuration for Robot Networks

```yaml
# /etc/netplan/01-robot-vlans.yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    eth0: {dhcp4: false}
  vlans:
    vlan10:
      id: 10
      link: eth0
      addresses: [10.10.10.5/24]
    vlan20:
      id: 20
      link: eth0
      addresses: [10.10.20.5/24]
    vlan30:
      id: 30
      link: eth0
      addresses: [10.10.30.5/24]
      routes: [{to: default, via: 10.10.30.1}]
```

### Disabling DDS Multicast in Production

Multicast auto-discovery exposes the full topic graph. Use unicast peer lists.

```xml
<!-- cyclonedds_secure.xml -->
<CycloneDDS>
  <Domain>
    <General><AllowMulticast>false</AllowMulticast></General>
    <Discovery>
      <Peers>
        <Peer address="10.10.10.1"/>
        <Peer address="10.10.10.2"/>
        <Peer address="10.10.10.3"/>
      </Peers>
      <ParticipantIndex>auto</ParticipantIndex>
    </Discovery>
  </Domain>
</CycloneDDS>
```

```bash
export CYCLONEDDS_URI=file:///etc/ros2/cyclonedds_secure.xml
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
```

FastDDS equivalent — set `initialPeersList` with explicit unicast locators and omit multicast locators in the participant profile. Use `FASTRTPS_DEFAULT_PROFILES_FILE` env var to load.

## SSH and Host Hardening

### SSH Key-Only Auth, Disable Root Login

```ini
# /etc/ssh/sshd_config
Port 2222
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
AuthorizedKeysFile .ssh/authorized_keys
MaxAuthTries 3
ClientAliveInterval 300
ClientAliveCountMax 2
AllowUsers robot-admin
X11Forwarding no
AllowTcpForwarding no
PermitTunnel no
```

```bash
sudo systemctl restart sshd
# Per-robot key pair (on management workstation)
ssh-keygen -t ed25519 -f ~/.ssh/robot_$(hostname) -C "admin@$(hostname)"
ssh-copy-id -i ~/.ssh/robot_$(hostname).pub -p 2222 robot-admin@10.10.30.5
```

### fail2ban for Robot Computers

```ini
# /etc/fail2ban/jail.local
[sshd]
enabled = true
port = 2222
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600
findtime = 600
```

```bash
sudo apt install fail2ban -y && sudo systemctl enable --now fail2ban
```

### Unattended Security Updates

```bash
sudo apt install unattended-upgrades -y
sudo dpkg-reconfigure -plow unattended-upgrades
# Key settings in /etc/apt/apt.conf.d/50unattended-upgrades:
#   Allowed-Origins: "${distro_id}:${distro_codename}-security"
#   Automatic-Reboot: "false"   # NEVER auto-reboot a running robot
```

### Minimal Installed Packages

```bash
# Remove unnecessary packages from robot computers
sudo apt purge -y avahi-daemon cups snapd modemmanager bluetooth bluez
sudo apt autoremove -y
```

## Secrets Management

### No Hardcoded Credentials

```python
# BAD:
class FleetClient:
    def __init__(self):
        self.api_key = "sk-live-abc123xyz789"
```

```python
# GOOD:
import os
class FleetClient:
    def __init__(self):
        self.api_key = os.environ['FLEET_API_KEY']
```

```yaml
# BAD: credentials in params.yaml tracked by git
fleet_manager:
  ros__parameters:
    aws_secret_key: "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
```

```yaml
# GOOD: reference environment variables
fleet_manager:
  ros__parameters:
    aws_secret_key: "$(env AWS_SECRET_KEY)"
```

### Environment-Based Secrets for ROS2 Nodes

```ini
# /etc/systemd/system/robot-nav.service
[Service]
User=robot
Group=robot
EnvironmentFile=/etc/robot/secrets.env
ExecStart=/opt/ros/humble/bin/ros2 launch my_robot nav.launch.py
Restart=always
```

```bash
# /etc/robot/secrets.env
FLEET_API_KEY=sk-live-actual-key-here
ROS_SECURITY_KEYSTORE=/opt/robot/sros2_keystore

# Lock it down
sudo chown root:robot /etc/robot/secrets.env
sudo chmod 640 /etc/robot/secrets.env
```

### Certificate Rotation Patterns

```bash
#!/bin/bash
# rotate_certs.sh — run via cron monthly
set -euo pipefail
KEYSTORE="/opt/robot/sros2_keystore"
cp -r "${KEYSTORE}" "${KEYSTORE}_backup_$(date +%Y%m%d)"

for enclave in motor_controller navigation camera_driver teleop; do
    ros2 security create_enclave "${KEYSTORE}" "/my_robot/${enclave}"
done
sudo systemctl restart robot-*.service
echo "Certificates rotated at $(date)"
```

```bash
# /etc/cron.d/robot-cert-rotation
0 3 1 * * root /opt/robot/scripts/rotate_certs.sh >> /var/log/cert-rotation.log 2>&1
```

### File Permissions for Keystores

```bash
sudo chown -R root:robot /opt/robot/sros2_keystore
sudo find /opt/robot/sros2_keystore -type d -exec chmod 750 {} \;
sudo find /opt/robot/sros2_keystore -type f -exec chmod 640 {} \;
# CA private key — root only
sudo chmod 600 /opt/robot/sros2_keystore/private/ca.key.pem
sudo chown root:root /opt/robot/sros2_keystore/private/ca.key.pem
```

## Container Security

### Non-Root Containers

```dockerfile
FROM ros:humble-ros-base AS runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    ros-humble-nav2-bringup && rm -rf /var/lib/apt/lists/*
RUN groupadd -g 1000 robot && useradd -u 1000 -g robot -m -s /bin/false robot
COPY --from=builder /opt/ros2_ws/install /opt/ros2_ws/install
USER robot:robot
ENTRYPOINT ["/ros_entrypoint.sh"]
CMD ["ros2", "launch", "my_robot", "nav.launch.py"]
```

### Minimal Runtime Images

```dockerfile
FROM ros:humble-desktop AS builder
WORKDIR /opt/ros2_ws
COPY src/ src/
RUN . /opt/ros/humble/setup.sh && \
    colcon build --cmake-args -DCMAKE_BUILD_TYPE=Release --merge-install

FROM ros:humble-ros-core AS runtime
COPY --from=builder /opt/ros2_ws/install /opt/ros2_ws/install
# Remove shell and package manager — prevents interactive exploitation
RUN rm -f /bin/sh /bin/bash /bin/dash && apt-get purge -y --auto-remove apt
```

### Image Scanning and Signing

```bash
trivy image --severity HIGH,CRITICAL my-robot/navigation:latest
cosign sign --key cosign.key my-registry.io/my-robot/navigation:v1.2.3
cosign verify --key cosign.pub my-registry.io/my-robot/navigation:v1.2.3 || exit 1
```

### Read-Only Root Filesystem

```yaml
# docker-compose.yml
services:
  motor_controller:
    image: my-robot/motor-controller:v1.0.0
    user: "1000:1000"
    read_only: true
    tmpfs: ["/tmp:size=64M", "/var/log/ros:size=32M"]
    volumes:
      - type: bind
        source: /opt/robot/sros2_keystore/enclaves/my_robot/motor_controller
        target: /keystore
        read_only: true
    security_opt: ["no-new-privileges:true"]
    cap_drop: [ALL]
    environment:
      ROS_SECURITY_KEYSTORE: /keystore
      ROS_SECURITY_ENABLE: "true"
      ROS_SECURITY_STRATEGY: Enforce
```

## Physical-Cyber Safety Intersection

Cyber attacks on robots cause **physical harm**. Standard IT security is necessary but not sufficient.

### E-Stop Independence

The emergency stop **must** function with all software, network, and main compute completely dead.

```
  ┌──────────┐     HARDWIRED      ┌─────────────────┐
  │ Physical  │ ─────────────────▶│ Safety Relay /   │──▶ Motor power cut
  │ E-Stop    │  Direct circuit    │ Safety PLC       │   via contactor
  │ Button    │  NO software       └─────────────────┘
  └──────────┘
  ┌──────────┐     OPTIONAL
  │ Software  │ ───(notifies)───▶ Can trigger relay, but NOT sole path
  │ E-Stop    │
  └──────────┘
  Main compute crash ──X──▶ Cannot prevent hardware e-stop
  Network failure    ──X──▶ Cannot prevent hardware e-stop
```

Design rules: hardwired circuit disconnects motor power; software triggers the relay but is never the only path; wireless e-stops use dedicated radio, not WiFi.

### Safety Controller Isolation

```
┌──────────────────────────────┬───────────────────────────────┐
│ MAIN COMPUTE (Jetson/x86)    │ SAFETY CONTROLLER (STM32/MCU) │
│ Ubuntu + ROS2                │ Bare-metal firmware            │
│ Nav, Perception, Planning    │                               │
│             ──── CAN/UART ──▶│ Validates:                    │
│                cmd_vel        │ - Max velocity                │
│                               │ - Max acceleration            │
│             ◀── joint_fb ────│ - Workspace limits            │
│                               │ - Watchdog timeout            │
│ If compromised, safety       │ Rejects out-of-bounds cmds    │
│ controller STILL enforces    │ Runs on separate hardware     │
│ physical limits.             │ Does NOT run ROS2 or Linux    │
└──────────────────────────────┴───────────────────────────────┘
```

### Command Velocity Validation and Rate Limiting

Enforce at the driver level — last line of defense before actuators:

```python
# velocity_safety_gate.py
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class VelocitySafetyGate(Node):
    def __init__(self):
        super().__init__('velocity_safety_gate')
        self.declare_parameter('max_linear_vel', 1.0)   # m/s
        self.declare_parameter('max_angular_vel', 2.0)   # rad/s
        self.declare_parameter('max_linear_accel', 0.5)  # m/s^2
        self.declare_parameter('cmd_timeout_sec', 0.5)
        self.declare_parameter('max_cmd_rate_hz', 50.0)

        self.max_lin = self.get_parameter('max_linear_vel').value
        self.max_ang = self.get_parameter('max_angular_vel').value
        self.max_acc = self.get_parameter('max_linear_accel').value
        self.timeout = self.get_parameter('cmd_timeout_sec').value
        self.min_period = 1.0 / self.get_parameter('max_cmd_rate_hz').value

        self.last_cmd_time = self.get_clock().now()
        self.last_linear = 0.0
        self.last_pub_sec = 0.0

        self.sub = self.create_subscription(Twist, 'cmd_vel_raw', self.on_cmd, 10)
        self.pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.create_timer(0.1, self.watchdog_check)

    def on_cmd(self, msg: Twist):
        now = self.get_clock().now()
        now_sec = now.nanoseconds / 1e9
        if (now_sec - self.last_pub_sec) < self.min_period:
            return  # Rate limit exceeded — drop

        msg.linear.x = max(-self.max_lin, min(self.max_lin, msg.linear.x))
        msg.angular.z = max(-self.max_ang, min(self.max_ang, msg.angular.z))

        dt = (now - self.last_cmd_time).nanoseconds / 1e9
        if dt > 0:
            accel = abs(msg.linear.x - self.last_linear) / dt
            if accel > self.max_acc:
                sign = 1.0 if msg.linear.x > self.last_linear else -1.0
                msg.linear.x = self.last_linear + sign * self.max_acc * dt

        self.pub.publish(msg)
        self.last_cmd_time = now
        self.last_linear = msg.linear.x
        self.last_pub_sec = now_sec

    def watchdog_check(self):
        elapsed = (self.get_clock().now() - self.last_cmd_time).nanoseconds / 1e9
        if elapsed > self.timeout:
            self.pub.publish(Twist())  # No command → zero velocity
```

### Watchdog Independence from Application Software

```python
# Hardware watchdog — kernel resets system if not fed
import os

class HardwareWatchdog:
    """Uses /dev/watchdog. If not fed within timeout, kernel triggers reset."""
    def __init__(self):
        self.fd = os.open('/dev/watchdog', os.O_WRONLY)  # Starts countdown
    def feed(self):
        os.write(self.fd, b'\x00')  # Reset countdown
    def close(self):
        os.write(self.fd, b'V')     # Magic close — disarm gracefully
        os.close(self.fd)
```

```bash
# /etc/watchdog.conf
watchdog-device = /dev/watchdog
watchdog-timeout = 15
interval = 5
pidfile = /var/run/robot-safety-monitor.pid
max-load-1 = 24
```

## Secure Boot and Firmware

### Read-Only Root Filesystem with Overlay

```bash
# /etc/fstab
/dev/mmcblk0p2  /        ext4  ro,noatime,errors=remount-ro  0 1
tmpfs           /tmp     tmpfs nosuid,nodev,size=128M         0 0
tmpfs           /var/log tmpfs nosuid,nodev,size=128M         0 0
/dev/mmcblk0p3  /data    ext4  rw,noatime,nosuid,nodev       0 2
```

```bash
# Alternative: overlayroot — all writes go to tmpfs, lost on reboot
sudo apt install overlayroot -y
# /etc/overlayroot.conf → overlayroot="tmpfs:swap=1"
```

### Signed Container Images

```bash
#!/bin/bash
set -euo pipefail
IMAGE="registry.myrobot.io/robot/navigation"
TAG="v$(cat VERSION)-$(git rev-parse --short HEAD)"
docker build -t "${IMAGE}:${TAG}" -f Dockerfile.prod .
trivy image --exit-code 1 --severity CRITICAL "${IMAGE}:${TAG}"
docker push "${IMAGE}:${TAG}"
cosign sign --key env://COSIGN_PRIVATE_KEY "${IMAGE}:${TAG}"
syft "${IMAGE}:${TAG}" -o spdx-json > sbom.json
cosign attach sbom --sbom sbom.json "${IMAGE}:${TAG}"
```

### TPM-Based Disk Encryption

```bash
# LUKS + TPM2 for unattended encrypted boot
sudo cryptsetup luksFormat /dev/mmcblk0p3
sudo cryptsetup luksOpen /dev/mmcblk0p3 robot-data
sudo systemd-cryptenroll /dev/mmcblk0p3 --tpm2-device=auto --tpm2-pcrs=0+7
# Disk decrypts only on original hardware with unmodified firmware
```

### Firmware Update Verification

```python
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
import subprocess

def verify_and_flash(firmware: Path, signature: Path, pubkey_path: Path):
    pubkey = serialization.load_pem_public_key(pubkey_path.read_bytes())
    try:
        pubkey.verify(signature.read_bytes(), firmware.read_bytes(),
                      ec.ECDSA(hashes.SHA256()))
    except Exception:
        raise SecurityError("Firmware signature verification FAILED — aborting")
    subprocess.run(['flash-tool', '--write', str(firmware)], check=True)
```

## Audit and Monitoring

### Security Logging for ROS2

```python
# topic_auditor.py — logs publications on sensitive topics
import rclpy, json, time
from rclpy.node import Node
from geometry_msgs.msg import Twist

class TopicAuditor(Node):
    def __init__(self):
        super().__init__('topic_auditor')
        self.log = open('/var/log/ros2_audit.jsonl', 'a')
        self.create_subscription(Twist, '/cmd_vel', self.audit_cmd_vel, 10)

    def audit_cmd_vel(self, msg: Twist):
        record = {'ts': time.time(), 'topic': '/cmd_vel',
                  'lin_x': msg.linear.x, 'ang_z': msg.angular.z}
        self.log.write(json.dumps(record) + '\n')
        self.log.flush()
        if abs(msg.linear.x) > 0.8 or abs(msg.angular.z) > 1.5:
            self.get_logger().warn(f'HIGH VEL: lin={msg.linear.x:.2f} ang={msg.angular.z:.2f}')
```

### Intrusion Detection on Command Topics

```python
# cmd_vel_anomaly_detector.py
import numpy as np
from collections import deque
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class CmdVelAnomalyDetector(Node):
    def __init__(self):
        super().__init__('cmd_vel_anomaly_detector')
        self.window = deque(maxlen=100)
        self.alert_pub = self.create_publisher(Twist, '/security/cmd_vel_alert', 10)
        self.create_subscription(Twist, '/cmd_vel', self.on_cmd, 10)

    def on_cmd(self, msg: Twist):
        self.window.append((msg.linear.x, msg.angular.z))
        if len(self.window) < 20:
            return
        vels = np.array(list(self.window))
        z_scores = np.abs((np.array([msg.linear.x, msg.angular.z]) - vels.mean(0)) / (vels.std(0) + 1e-6))
        if np.any(z_scores > 3.0):
            self.get_logger().error(f'ANOMALY: lin={msg.linear.x:.3f} ang={msg.angular.z:.3f} z={z_scores}')
            self.alert_pub.publish(msg)
```

### auditd Rules for Robot Systems

```bash
# /etc/audit/rules.d/robot-security.rules
-w /opt/robot/sros2_keystore/ -p rwxa -k robot_keystore
-w /etc/robot/ -p wa -k robot_config
-w /home/robot-admin/.ssh/ -p wa -k ssh_keys
-w /opt/robot/firmware/ -p rwxa -k firmware_access
-w /etc/systemd/system/robot- -p wa -k robot_services
-a always,exit -F arch=b64 -F euid=0 -S execve -k root_commands
-w /dev/bus/usb/ -p rwxa -k usb_access
-w /etc/netplan/ -p wa -k network_config
-w /etc/iptables/ -p wa -k firewall_config
-w /usr/bin/docker -p x -k docker_exec
```

```bash
sudo auditctl -R /etc/audit/rules.d/robot-security.rules
sudo systemctl enable --now auditd
sudo ausearch -k robot_keystore --start today
```

## Robotics Security Anti-Patterns

### 1. Unauthenticated /cmd_vel

**Problem:** Default ROS2 lets any DDS participant publish to `/cmd_vel`. One command from any machine on the LAN moves the robot.

```bash
# BAD: anyone on the network can do this
ros2 topic pub /cmd_vel geometry_msgs/Twist "{linear: {x: 999.0}}"
```

**Fix:** SROS2 with `Enforce`. Restrict `/cmd_vel` publish to authorized enclaves. Velocity safety gate as secondary check.

```bash
# GOOD: unauthorized publish rejected at DDS layer
export ROS_SECURITY_ENABLE=true
export ROS_SECURITY_STRATEGY=Enforce
```

### 2. Shared SSH Keys Across Robot Fleet

**Problem:** One key compromised = entire fleet compromised.

```bash
# BAD: same key for all robots
ssh-copy-id -i ~/.ssh/fleet_key.pub robot@robot-001
ssh-copy-id -i ~/.ssh/fleet_key.pub robot@robot-002
```

**Fix:** Unique key per robot. Use SSH CA with short-lived certificates.

```bash
# GOOD: SSH CA issues 8-hour certs per session
ssh-keygen -s /etc/ssh/ca_key -I "session-$(date +%s)" -n robot-admin -V +8h ~/.ssh/id_ed25519.pub
```

### 3. Running All Nodes as Root

**Problem:** Any compromised node = full root access to the system.

```bash
# BAD:
sudo ros2 launch my_robot bringup.launch.py
```

**Fix:** Run as unprivileged user. Use udev rules for hardware access instead of root.

```bash
# GOOD:
sudo -u robot ros2 launch my_robot bringup.launch.py
# /etc/udev/rules.d/99-robot.rules:
# SUBSYSTEM=="tty", ATTRS{idVendor}=="0403", MODE="0660", GROUP="robot"
```

### 4. No Network Segmentation

**Problem:** All traffic on one flat network. Compromised IP camera reaches motor controller.

**Fix:** VLAN segmentation with inter-VLAN firewall rules. See Network Hardening section.

```bash
# BAD: everything on 192.168.1.0/24

# GOOD: VLAN 10 control (wired), VLAN 20 data, VLAN 30 mgmt (jump host)
```

### 5. Hardcoded Credentials in Launch Files

**Problem:** Credentials in version control exposed to repo access, CI logs, Docker layers.

```yaml
# BAD: in params.yaml tracked by git
cloud_connector:
  ros__parameters:
    aws_access_key: "AKIAIOSFODNN7EXAMPLE"
```

**Fix:** Environment variables from protected files. Scan repos with `gitleaks`.

```bash
# GOOD: secrets injected at runtime via systemd EnvironmentFile
gitleaks detect --source . --verbose  # Pre-commit check
```

### 6. E-Stop Over Network

**Problem:** Software e-stop over ROS2 as the **only** safety mechanism. Network down = no stop.

```python
# BAD: sole e-stop is a ROS2 topic subscriber
self.create_subscription(Bool, '/e_stop', self.software_estop, 10)
```

**Fix:** Hardwired e-stop circuit. Software e-stop is an additional layer, never the sole path.

### 7. No Certificate Rotation

**Problem:** SROS2 certs generated once and never rotated. Compromised key = permanent access.

**Fix:** Monthly automated rotation via cron. Explicit validity periods in permissions XML. Emergency rotation capability via fleet management.

### 8. Disabling Security for Convenience

**Problem:** SROS2 disabled in production because "too hard" or "adds latency." Most common robotics security failure.

```bash
# BAD: "temporary" becomes permanent
export ROS_SECURITY_ENABLE=false
```

**Fix:** Security enabled in CI/CD from day one. Tests must pass with `Enforce`.

```bash
# GOOD: CI enforces security
export ROS_SECURITY_ENABLE=true
export ROS_SECURITY_STRATEGY=Enforce
ros2 launch my_robot test.launch.py  # Must pass with security on
```

## Robotics Security Checklist

1. **SROS2 enabled with `Enforce` strategy** — all nodes use encrypted, authenticated DDS
2. **Per-node enclaves with least-privilege permissions** — each node publishes/subscribes only to required topics
3. **Network segmented into control/data/management VLANs** — firewall rules between zones
4. **DDS multicast disabled** — unicast peer lists only, no auto-discovery on LAN
5. **SSH hardened** — key-only auth, non-default port, fail2ban, no root login
6. **No hardcoded credentials** — secrets from environment files with 640 permissions
7. **Certificates rotated on schedule** — automated monthly rotation, explicit validity periods
8. **Containers run as non-root** — USER directive, no-new-privileges, all capabilities dropped
9. **E-stop is hardware-independent** — hardwired circuit works with all software/network down
10. **Safety controller on separate hardware** — velocity/workspace limits enforced outside main compute
11. **Command velocity validated at driver level** — clamping, rate limiting, watchdog to zero
12. **auditd monitoring active** — keystore access, config changes, USB events, root commands logged
13. **Firmware updates signature-verified** — no unsigned code on motor controllers or safety MCUs
14. **Security tested in CI/CD** — SROS2 Enforce in integration tests, image scanning in pipeline
