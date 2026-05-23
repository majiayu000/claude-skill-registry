---
name: server-log-health-check
description: Quick health check of IQRight server pipeline. Shows packet reception, lookups, LoRa responses, and MQTT publishing status. Use when checking if the server is working or after deploying.
---

# Server Log Health Check

Perform a 4-stage pipeline health check on the CaptureLora.py server logs.

## Step 1: Locate and Assess Active Log

The server logs are at `logs/IQRight_Daemon.debug` with rotated backups at `logs/IQRight_Daemon.debug.MMDDYY`.

- Check file sizes with `du -h logs/IQRight_Daemon.debug*`
- Read the last 50 lines of the active log to see current state
- Extract first/last timestamps to show the date range covered

## Step 2: Run Pipeline Health Check

Count packets at each of the 4 pipeline stages. Use Grep for each:

1. **LoRa Reception**: pattern `Received data from scanner` in `logs/IQRight_Daemon.debug`
2. **Data Lookups**: pattern `Using local results|Using API results` in `logs/IQRight_Daemon.debug`
3. **LoRa Responses**: pattern `Sent DATA to scanner|Sent CMD` in `logs/IQRight_Daemon.debug`
4. **MQTT Successes**: pattern `MQTT-TX.*SUCCESS` in `logs/IQRight_Daemon.debug`
5. **MQTT Failures**: pattern `MQTT-TX.*FAILED` in `logs/IQRight_Daemon.debug`

Present these 5 numbers in a clear table.

## Step 3: Check Adaptive Logging State

Look for state transitions to understand operational timeline:
- `SWITCHING TO ACTIVE MODE` = operation started (HELLO received)
- `SWITCHING TO IDLE MODE` = operation ended (15 min no packets)
- `Server started in IDLE mode` = server restart

## Step 4: Recent Errors

Find the last 15 ERROR lines to identify current issues. Categorize by type:
- **LoRa errors**: "Error in sendDataScanner", "create_packet"
- **API errors**: "Connection reset", "timed out", "Client error"
- **MQTT errors**: "MQTT-TX.*FAILED"
- **Data errors**: "Couldn't find Code", "Invalid DATA packet"

## Step 5: Summary Report

Report:
- **Time range**: First and last log entry timestamps
- **Operational state**: IDLE or ACTIVE, last state change
- **Pipeline status**: All 4 stages working? Where are gaps?
- **Error count**: Total errors, top 3 types
- **Recommendation**: Is the server healthy? What needs attention?

Reference: See `docs/LOG_ANALYSIS_SKILLS.md` for detailed patterns and baselines.