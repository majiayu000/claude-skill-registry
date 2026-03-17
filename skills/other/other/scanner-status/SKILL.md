---
name: scanner-status
description: Check the connectivity and health of a specific scanner node. Shows last activity, handshake history, error rate, and data quality. Use when verifying a scanner is connected or diagnosing scanner issues.
argument-hint: [scanner-node-id]
---

# Scanner Status

Check the status of scanner node `$ARGUMENTS` in `logs/IQRight_Daemon.debug`.

Scanner node IDs are in the range 100-199 (e.g., 102 = Gym Side scanner).

## Step 1: Last Activity

Search for the most recent packets from this scanner:
- Pattern: `Received data from scanner $ARGUMENTS`
- Pattern: `HELLO.*src=$ARGUMENTS` or `HELLO from.*node $ARGUMENTS`

Extract:
- **Last DATA packet**: timestamp, sequence number, code scanned
- **Last HELLO**: timestamp (indicates scanner restart)
- **TTL value**: 3 = direct connection, 2 = via repeater (1 hop), 1 = 2 hops

## Step 2: HELLO Handshake History

Search for handshake events for this scanner:
- `HELLO from SCANNER node $ARGUMENTS` - Scanner initiated handshake
- `HELLO_ACK sent successfully to node $ARGUMENTS` - Server responded OK
- `Failed to send HELLO_ACK to node $ARGUMENTS` - Handshake failed

Count total HELLOs vs total DATA packets:
- **Healthy ratio**: < 1 HELLO per 10 DATA packets
- **Warning**: > 1 HELLO per 5 DATA packets (scanner restarting too often)
- **Critical**: > 1:1 ratio (scanner may be crash-looping)

## Step 3: Data Quality

Count for this scanner:
- Total DATA packets received
- Successful lookups (lines after `Received data from scanner $ARGUMENTS` that lead to `Using local results` or `Using API results`)
- Failed lookups (`Couldn't find Code` or `No data found for code`)
- Responses sent back (`Sent DATA to scanner $ARGUMENTS`)
- Failed sends (`FAILED to send.*Scanner.*$ARGUMENTS`)

Calculate success rates.

## Step 4: Error Analysis

Search for errors mentioning this scanner:
- `scanner $ARGUMENTS` combined with `ERROR` or `FAILED`
- Check for corrupted QR codes (PATTERN-001: `31` prefix, null bytes, doubled codes)

## Step 5: Report

```
Scanner $ARGUMENTS Status
========================
Last Activity:    {timestamp} ({time ago})
Connection:       DIRECT (TTL=3) | VIA REPEATER (TTL=2)
Handshake:        Last HELLO at {time}, {count} total ({status})

Pipeline:
  Packets received:    {N}
  Lookups succeeded:   {N}/{total} ({pct}%)
  Responses sent:      {N}/{total} ({pct}%)
  MQTT published:      {N}

Errors:
  {list of errors with counts}

Health: HEALTHY | DEGRADED | CRITICAL
Recommendation: {action items}
```

Reference: See `docs/LOG_ANALYSIS_SKILLS.md` section 2 for packet signatures and section 6 for thresholds.
