---
name: openclaw-runtime-monitor
description: Real-time security monitoring for OpenClaw including file system access monitoring, credential access detection, anomaly identification, and automated incident response.
---

# OpenClaw Runtime Monitoring Skill

This skill provides comprehensive real-time security monitoring for OpenClaw, detecting unauthorized access, credential theft attempts, and security anomalies.

## When to Activate

- OpenClaw security audit
- Suspicious activity detection
- Security incident response
- Continuous monitoring setup
- After credential encryption implementation

## Monitoring Components

### 1. File System Access Monitoring

#### Real-time File Monitoring

```bash
# Monitor ~/.clawdbot/ directory access
sudo fs_usage | grep clawdbot &
FS_USAGE_PID=$!

# Alternative: Use fswatch for continuous monitoring
fswatch -o ~/.clawdbot/ | while read event; do
  echo "$(date): File system event in ~/.clawdbot/: $event" >> /var/log/openclaw-fs-monitor.log
done &
FSWATCH_PID=$!

# Monitor credential file access specifically
sudo lsof +D ~/.clawdbot/credentials/ 2>/dev/null | grep -v "PID" | while read line; do
  echo "$(date): Credential file access detected: $line" >> /var/log/openclaw-credential-access.log
  # Send alert
  osascript -e 'display notification "Credential file access detected!" with title "OpenClaw Security Alert"'
done &
LSOF_PID=$!
```

#### File Integrity Monitoring

```bash
#!/bin/bash
# file-integrity-monitor.sh

CLAWDBOT_DIR="$HOME/.clawdbot"
INTEGRITY_LOG="/var/log/openclaw-integrity.log"
HASH_FILE="/tmp/openclaw-file-hashes"

# Calculate initial file hashes
echo "$(date): Initializing file integrity monitoring..." >> $INTEGRITY_LOG
find "$CLAWDBOT_DIR" -type f -exec sha256sum {} \; > "$HASH_FILE" 2>/dev/null

# Monitor for changes
while true; do
  sleep 30  # Check every 30 seconds
  
  # Calculate current hashes
  find "$CLAWDBOT_DIR" -type f -exec sha256sum {} \; > /tmp/current-hashes 2>/dev/null
  
  # Compare with baseline
  if ! diff -q "$HASH_FILE" /tmp/current-hashes > /dev/null; then
    echo "$(date): FILE INTEGRITY BREACH DETECTED!" >> $INTEGRITY_LOG
    diff "$HASH_FILE" /tmp/current-hashes >> $INTEGRITY_LOG
    
    # Send critical alert
    osascript -e 'display notification "File integrity breach detected in OpenClaw!" with title "CRITICAL SECURITY ALERT"'
    
    # Update baseline
    cp /tmp/current-hashes "$HASH_FILE"
  fi
done &
```

### 2. Credential Access Detection

#### Keychain Access Monitoring

```bash
# Monitor Keychain access for OpenClaw credentials
log stream --predicate 'subsystem == "com.apple.security" AND (process == "openclaw" OR process == "clawdbot")' | while read line; do
  if echo "$line" | grep -q "keychain\|credential"; then
    echo "$(date): Keychain access detected: $line" >> /var/log/openclaw-keychain-monitor.log
  fi
done &
KEYCHAIN_PID=$!

# Monitor securityd logs for credential access
log stream --predicate 'subsystem == "com.apple.securityd"' | grep -i "openclaw\|clawdbot" >> /var/log/openclaw-securityd.log &
SECURITYD_PID=$!
```

#### Process Monitoring for Credential Theft

```bash
#!/bin/bash
# credential-theft-monitor.sh

# Monitor processes trying to access OpenClaw credentials
while true; do
  # Check for suspicious processes reading credential files
  ps aux | grep -E "(cat|less|more|vim|nano|emacs)" | grep -v grep | while read line; do
    if echo "$line" | grep -q "clawdbot\|oauth\.json\|\.env.*claw"; then
      PID=$(echo "$line" | awk '{print $2}')
      CMD=$(echo "$line" | awk '{print $11}')
      USER=$(echo "$line" | awk '{print $1}')
      
      echo "$(date): SUSPICIOUS CREDENTIAL ACCESS - PID: $PID, CMD: $CMD, USER: $USER" >> /var/log/openclaw-credential-theft.log
      
      # Alert user
      osascript -e "display notification \"Suspicious credential access detected: $CMD accessing OpenClaw credentials\" with title \"SECURITY ALERT\""
      
      # Optional: Kill suspicious process
      # kill -9 $PID
    fi
  done
  
  sleep 10
done &
THEFT_MONITOR_PID=$!
```

### 3. Anomaly Detection

#### Network Anomaly Detection

```bash
#!/bin/bash
# network-anomaly-detector.sh

# Monitor OpenClaw network connections
while true; do
  # Check for unusual network connections
  OPENCLAW_CONNECTIONS=$(lsof -i :18789 2>/dev/null | grep -v "PID")
  EXPECTED_CONNECTIONS=1  # Expected: OpenClaw gateway
  
  if [ -n "$OPENCLAW_CONNECTIONS" ]; then
    CONNECTION_COUNT=$(echo "$OPENCLAW_CONNECTIONS" | wc -l)
    if [ "$CONNECTION_COUNT" -gt "$EXPECTED_CONNECTIONS" ]; then
      echo "$(date): UNUSUAL NETWORK ACTIVITY - $CONNECTION_COUNT connections on port 18789" >> /var/log/openclaw-network-anomaly.log
      echo "$OPENCLAW_CONNECTIONS" >> /var/log/openclaw-network-anomaly.log
      
      osascript -e 'display notification "Unusual network activity detected on OpenClaw!" with title "Network Anomaly Alert"'
    fi
  fi
  
  # Check for connections to unexpected ports
  UNEXPECTED_PORTS=$(lsof -i -P | grep "openclaw\|clawdbot" | grep -v ":18789")
  if [ -n "$UNEXPECTED_PORTS" ]; then
    echo "$(date): OPENCLAW CONNECTING TO UNEXPECTED PORTS:" >> /var/log/openclaw-network-anomaly.log
    echo "$UNEXPECTED_PORTS" >> /var/log/openclaw-network-anomaly.log
    
    osascript -e 'display notification "OpenClaw connecting to unexpected ports!" with title "Network Anomaly Alert"'
  fi
  
  sleep 30
done &
NETWORK_MONITOR_PID=$!
```

#### Process Anomaly Detection

```bash
#!/bin/bash
# process-anomaly-detector.sh

# Monitor for suspicious OpenClaw processes
while true; do
  # Check for OpenClaw processes with unusual arguments
  SUSPICIOUS_PROCESSES=$(ps aux | grep -E "(openclaw|clawdbot)" | grep -E "(sh|bash|python|perl|nc|netcat|curl|wget)" | grep -v grep)
  
  if [ -n "$SUSPICIOUS_PROCESSES" ]; then
    echo "$(date): SUSPICIOUS OPENCLAW PROCESSES DETECTED:" >> /var/log/openclaw-process-anomaly.log
    echo "$SUSPICIOUS_PROCESSES" >> /var/log/openclaw-process-anomaly.log
    
    osascript -e 'display notification "Suspicious OpenClaw processes detected!" with title "Process Anomaly Alert"'
  fi
  
  # Check for processes trying to inject into OpenClaw
  INJECTION_ATTEMPTS=$(ps aux | grep -E "(gdb|lldb|strace|dtruss)" | grep -E "(openclaw|clawdbot)" | grep -v grep)
  
  if [ -n "$INJECTION_ATTEMPTS" ]; then
    echo "$(date): PROCESS INJECTION ATTEMPT DETECTED:" >> /var/log/openclaw-process-anomaly.log
    echo "$INJECTION_ATTEMPTS" >> /var/log/openclaw-process-anomaly.log
    
    osascript -e 'display notification "Process injection attempt detected!" with title "CRITICAL SECURITY ALERT"'
  fi
  
  sleep 15
done &
PROCESS_MONITOR_PID=$!
```

### 4. Automated Incident Response

#### Incident Response Script

```bash
#!/bin/bash
# openclaw-incident-response.sh

INCIDENT_LOG="/var/log/openclaw-incidents.log"
DATE=$(date +%Y-%m-%d_%H:%M:%S)

log_incident() {
  echo "[$DATE] INCIDENT: $1" >> $INCIDENT_LOG
  osascript -e "display notification \"$1\" with title \"OpenClaw Incident Response\""
}

# Function to isolate OpenClaw
isolate_openclaw() {
  log_incident "Isolating OpenClaw - stopping all processes"
  
  # Stop OpenClaw gateway
  pkill -f openclaw-gateway 2>/dev/null
  pkill -f clawdbot 2>/dev/null
  
  # Block network access
  sudo pfctl -f /dev/stdin << EOF
block drop in on any from any to any port 18789
EOF
  
  log_incident "OpenClaw isolated - processes stopped and network blocked"
}

# Function to preserve evidence
preserve_evidence() {
  EVIDENCE_DIR="/tmp/openclaw-evidence-$(date +%Y%m%d%H%M%S)"
  mkdir -p "$EVIDENCE_DIR"
  
  # Copy logs
  cp /var/log/openclaw-*.log "$EVIDENCE_DIR/" 2>/dev/null
  
  # Copy configuration files
  cp -r ~/.clawdbot "$EVIDENCE_DIR/" 2>/dev/null
  
  # Capture process information
  ps aux | grep -E "(openclaw|clawdbot)" > "$EVIDENCE_DIR/processes.txt" 2>/dev/null
  
  # Capture network connections
  lsof -i :18789 > "$EVIDENCE_DIR/network-connections.txt" 2>/dev/null
  
  log_incident "Evidence preserved in $EVIDENCE_DIR"
}

# Function to analyze breach
analyze_breach() {
  log_incident "Analyzing security breach..."
  
  # Check for credential access
  if [ -f /var/log/openclaw-credential-access.log ]; then
    RECENT_ACCESS=$(tail -10 /var/log/openclaw-credential-access.log)
    if [ -n "$RECENT_ACCESS" ]; then
      log_incident "Recent credential access detected: $RECENT_ACCESS"
    fi
  fi
  
  # Check for file integrity breaches
  if [ -f /var/log/openclaw-integrity.log ]; then
    RECENT_BREACHES=$(tail -10 /var/log/openclaw-integrity.log | grep "BREACH")
    if [ -n "$RECENT_BREACHES" ]; then
      log_incident "Recent integrity breaches: $RECENT_BREACHES"
    fi
  fi
  
  # Check for network anomalies
  if [ -f /var/log/openclaw-network-anomaly.log ]; then
    RECENT_ANOMALIES=$(tail -10 /var/log/openclaw-network-anomaly.log)
    if [ -n "$RECENT_ANOMALIES" ]; then
      log_incident "Recent network anomalies: $RECENT_ANOMALIES"
    fi
  fi
}

# Main incident response logic
case "$1" in
  "isolate")
    isolate_openclaw
    ;;
  "preserve")
    preserve_evidence
    ;;
  "analyze")
    analyze_breach
    ;;
  "full")
    isolate_openclaw
    preserve_evidence
    analyze_breach
    ;;
  *)
    echo "Usage: $0 {isolate|preserve|analyze|full}"
    exit 1
    ;;
esac
```

## Monitoring Dashboard

### Real-time Status Script

```bash
#!/bin/bash
# openclaw-security-dashboard.sh

clear
echo "🔒 OpenClaw Security Monitoring Dashboard"
echo "=========================================="
echo "Last Updated: $(date)"
echo ""

# Check OpenClaw processes
echo "📊 OpenClaw Process Status:"
ps aux | grep -E "(openclaw|clawdbot)" | grep -v grep || echo "❌ No OpenClaw processes running"
echo ""

# Check credential security
echo "🔐 Credential Security:"
if [ -d ~/.clawdbot ]; then
  CREDENTIAL_FILES=$(find ~/.clawdbot/credentials -type f 2>/dev/null | wc -l)
  echo "📁 Credential files: $CREDENTIAL_FILES"
  
  # Check file permissions
  UNPROTECTED=$(find ~/.clawdbot/ -type f -not -perm 600 2>/dev/null | wc -l)
  if [ "$UNPROTECTED" -gt 0 ]; then
    echo "⚠️  $UNPROTECTED files have insecure permissions"
  else
    echo "✅ All files have secure permissions"
  fi
else
  echo "✅ No ~/.clawdbot directory found"
fi
echo ""

# Check network security
echo "🌐 Network Security:"
if lsof -i :18789 >/dev/null 2>&1; then
  CONNECTIONS=$(lsof -i :18789 | grep -v "PID" | wc -l)
  echo "🔗 Port 18789 connections: $CONNECTIONS"
else
  echo "✅ Port 18789 not listening"
fi
echo ""

# Recent security events
echo "🚨 Recent Security Events:"
if [ -f /var/log/openclaw-incidents.log ]; then
  tail -5 /var/log/openclaw-incidents.log | while read line; do
    echo "   $line"
  done
else
  echo "✅ No security incidents logged"
fi
echo ""

# Monitoring processes
echo "📡 Monitoring Status:"
if pgrep -f "file-integrity-monitor" >/dev/null; then
  echo "✅ File integrity monitor running"
else
  echo "❌ File integrity monitor not running"
fi

if pgrep -f "credential-theft-monitor" >/dev/null; then
  echo "✅ Credential theft monitor running"
else
  echo "❌ Credential theft monitor not running"
fi

if pgrep -f "network-anomaly-detector" >/dev/null; then
  echo "✅ Network anomaly detector running"
else
  echo "❌ Network anomaly detector not running"
fi

echo ""
echo "Press Ctrl+C to exit. Dashboard refreshes every 30 seconds."
```

## Installation and Setup

### Install Monitoring Dependencies

```bash
# Install fswatch for file monitoring
brew install fswatch

# Create log directories
sudo mkdir -p /var/log/openclaw-security
sudo chown $(whoami):staff /var/log/openclaw-security

# Create monitoring scripts directory
mkdir -p ~/openclaw-security-scripts
cd ~/openclaw-security-scripts

# Download and install monitoring scripts
# (Copy the scripts from above into this directory)
chmod +x *.sh
```

### Start Monitoring Services

```bash
#!/bin/bash
# start-openclaw-monitoring.sh

echo "🚀 Starting OpenClaw security monitoring..."

# Start file integrity monitoring
./file-integrity-monitor.sh &
echo "✅ File integrity monitor started (PID: $!)"

# Start credential theft monitoring
./credential-theft-monitor.sh &
echo "✅ Credential theft monitor started (PID: $!)"

# Start network anomaly detection
./network-anomaly-detector.sh &
echo "✅ Network anomaly detector started (PID: $!)"

# Start process anomaly detection
./process-anomaly-detector.sh &
echo "✅ Process anomaly detector started (PID: $!)"

echo ""
echo "🎉 OpenClaw security monitoring is now active!"
echo "📊 Run ./openclaw-security-dashboard.sh for real-time status"
```

This skill provides comprehensive runtime security monitoring for OpenClaw, detecting and responding to security threats in real-time.
