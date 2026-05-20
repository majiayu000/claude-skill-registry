---
name: port-scanner
description: 扫描网络端口以检查可用性和检测运行的服务。
metadata:
  short-description: 扫描网络端口
source:
  repository: https://github.com/python/cpython
  license: PSF
---

# Port Scanner Tool

## Description
Scan network ports to check availability, detect running services, and find open ports.

## Trigger
- `/port` command
- User needs to check ports
- User wants to scan network

## Usage

```bash
# Check single port
python scripts/port_scanner.py localhost 8080

# Scan port range
python scripts/port_scanner.py 192.168.1.1 --range 80-443

# Scan common ports
python scripts/port_scanner.py example.com --common

# Check if port is available
python scripts/port_scanner.py localhost 3000 --available
```

## Tags
`port`, `network`, `scan`, `tcp`, `security`

## Compatibility
- Codex: ✅
- Claude Code: ✅
