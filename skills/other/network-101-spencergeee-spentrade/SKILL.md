---
name: Network 101
description: This skill should be used when the user asks to "set up a web server", "configure HTTP or HTTPS", "perform SNMP enumeration", "configure SMB shares", "test network services", or needs guidance on configuring and testing network services for penetration testing labs.
metadata:
  author: zebbern
  version: 4.1.0-fractal
---

# Network 101

## Purpose

Configure and test common network services (HTTP, HTTPS, SNMP, SMB) for penetration testing lab environments. Enable hands-on practice with service enumeration, log analysis, and security testing against properly configured target systems.

## Inputs/Prerequisites

- Windows Server or Linux system for hosting services
- Kali Linux or similar for testing
- Administrative access to target system
- Basic networking knowledge (IP addressing, ports)
- Firewall access for port configuration

## Outputs/Deliverables

- Configured HTTP/HTTPS web server
- SNMP service with accessible communities
- SMB file shares with various permission levels
- Captured logs for analysis
- Documented enumeration results

## Core Workflow

## 🧠 Knowledge Modules (Fractal Skills)

### 1. [1. Configure HTTP Server (Port 80)](./sub-skills/1-configure-http-server-port-80.md)
### 2. [2. Configure HTTPS Server (Port 443)](./sub-skills/2-configure-https-server-port-443.md)
### 3. [3. Configure SNMP Service (Port 161)](./sub-skills/3-configure-snmp-service-port-161.md)
### 4. [4. Configure SMB Service (Port 445)](./sub-skills/4-configure-smb-service-port-445.md)
### 5. [5. Analyze Service Logs](./sub-skills/5-analyze-service-logs.md)
### 6. [Essential Ports](./sub-skills/essential-ports.md)
### 7. [Service Verification Commands](./sub-skills/service-verification-commands.md)
### 8. [Common Enumeration Tools](./sub-skills/common-enumeration-tools.md)
### 9. [Example 1: Complete HTTP Lab Setup](./sub-skills/example-1-complete-http-lab-setup.md)
### 10. [Example 2: SNMP Testing Setup](./sub-skills/example-2-snmp-testing-setup.md)
### 11. [Example 3: SMB Anonymous Access](./sub-skills/example-3-smb-anonymous-access.md)
