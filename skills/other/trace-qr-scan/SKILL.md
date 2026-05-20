---
name: trace-qr-scan
description: Trace a specific QR code through the entire server pipeline. Shows received, looked up, found, sent to scanner, published to MQTT. Use when debugging why a specific scan didn't work.
argument-hint: [qr-code]
---

# Trace QR Scan

Trace the QR code `$ARGUMENTS` through the entire data pipeline in `logs/IQRight_Daemon.debug`.

## Step 1: Search for the Code

Search the active log for all occurrences of the code. If no results, also try:
- Without leading `P` prefix
- With `31` prefix (known corruption pattern)
- Doubled/concatenated variant (e.g., `P1234567831P12345678`)

## Step 2: Trace Each Occurrence Through the Pipeline

For each match, extract context (30 lines after the match) and determine:

1. **Received?** - Look for `Received data from scanner {node}: Beacon={b}, Code={code}, Distance={d}`
   - Extract: source node, sequence number, TTL (3=direct, 2=via repeater)

2. **Looked up?** - Look for `Using local results` or `Using API results`
   - If `Couldn't find Code` appears, the code was not in the database (possibly corrupted)

3. **Found?** - Extract student info: name, grade, hierarchyID
   - Multi-student: count how many results returned

4. **Sent to scanner?** - Look for `Sent DATA to scanner {node}: {name}|{grade}|{id} [{index}/{total}]`
   - Multi-packet: `[1/4]` means packet 1 of 4

5. **Published to MQTT?** - Look for `MQTT-TX.*SUCCESS: Topic={topic}`
   - Verify topic format: `Class{hierarchyID}` for student data, `IQRSend` for commands
   - If `MQTT-TX.*FAILED`: note Status code (7 = connection lost)

## Step 3: Identify Where It Broke

If the trace breaks at any stage:
- **Not received**: LoRa signal/hardware issue
- **Not looked up**: Code pipeline bug
- **Not found**: Code not in DB, or corrupted (check for `31` prefix, null bytes, duplicated codes)
- **Not sent**: LoRa transmission failure (check `Error in sendDataScanner`)
- **Not published**: MQTT broker connection lost

## Output Format

Show the trace as a timeline:
```
Code: P22510583
Occurrences: 3

[1] 2025-12-17 15:21:30
  1. Received:  OK - Scanner 102, seq=4, TTL=3 (direct)
  2. Lookup:    OK - Local (API offline)
  3. Found:     OK - 2 students (Raphael Winata, Gabriel Winata)
  4. Sent:      OK - [1/2] and [2/2] to scanner 102
  5. Published: OK - Topic=Class89 and Topic=Class103

[2] 2025-12-17 10:49:26
  1. Received:  OK - Scanner 102, seq=38, TTL=2 (via repeater)
  2. Lookup:    FAILED - Corrupted code: "\x00\x00\x01\x0031P22510583"
  3. Found:     N/A
  4. Sent:      N/A
  5. Published: N/A
  DIAGNOSIS: QR scanner buffer corruption (PATTERN-001)
```

Reference: See `docs/LOG_ANALYSIS_SKILLS.md` sections 2-5 for pipeline stages and known patterns.