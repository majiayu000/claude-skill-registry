---
name: error-report
description: Generate a categorized error summary from server logs. Shows what's failing, frequency, severity, and recommendations. Use when troubleshooting system failures or before go-live checks.
---

# Error Report

Analyze all ERROR messages in the IQRight server logs.

## Step 1: Error Count

Count total ERROR lines in `logs/IQRight_Daemon.debug` and any rotated logs.

## Step 2: Categorize by Type

Search for ERROR lines and group by message pattern. The known error categories are:

### LoRa Errors
- `Error in sendDataScanner` - Failed to send response to scanner
- `'LoRaTransceiver' object has no attribute 'create_packet'` - Method name bug (should be `create_data_packet`)
- `Failed to send DATA` / `FAILED to send data to Scanner` - LoRa TX failure

### API Errors
- `Connection reset by peer` - API server unreachable
- `Server disconnected` - API connection dropped mid-request
- `API call timed out` - API timeout exceeded
- `Client error during API call` - General HTTP client error
- `API getUserAccess request failed on getting secrets` - Credential retrieval failure

### MQTT Errors
- `MQTT-TX.*FAILED.*Status=7` - Broker connection lost during publish
- `MQTT ERROR publishing data` - Data publish failed after all retries
- `MQTT ERROR publishing command ACK` - Command ACK publish failed

### Data/Lookup Errors
- `Couldn't find Code: {code} locally` - Code not in local database
- `No data found for code {code}` - Neither API nor local found the code
- `Invalid DATA packet format` - Corrupted LoRa payload structure
- `Invalid UTF-8 String` - Binary corruption in packet payload

### Handshake Errors
- `Failed to send HELLO_ACK` - Could not respond to scanner handshake
- `Invalid HELLO packet format` - Malformed HELLO payload

## Step 3: Severity Classification

**CRITICAL** (blocks user-facing operations):
- LoRa send failures (scanner gets no response)
- MQTT publish failures (web UI gets no data)
- `create_packet` attribute errors (code bug)

**WARNING** (degrades but doesn't block):
- API connection failures (local fallback works)
- QR code corruption / lookup failures (~10% expected)
- MQTT Status=7 with successful retry

**INFO** (normal/expected):
- `own_packet_looped` discards (repeater forwarding back - normal)
- Duplicate packet discards (normal if < 5% of traffic)

## Step 4: Recent Examples

Show the last 10-15 ERROR lines with timestamps and full messages.

## Step 5: Summary

Present a report with:
- Total error count and percentage of log lines
- Top 5 error types ranked by frequency
- Severity of each type
- Whether each is a known pattern (reference PATTERN-001 through PATTERN-004) or new
- Actionable recommendations for each critical/warning error

Reference: See `docs/LOG_ANALYSIS_SKILLS.md` section 5 for known bugs and section 6 for alerting thresholds.