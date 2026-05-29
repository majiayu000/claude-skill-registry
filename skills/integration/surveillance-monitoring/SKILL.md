---
name: surveillance-monitoring
description: Monitor Ubiquiti Protect surveillance cameras and events. Track camera status, review recordings and alerts, and monitor system health.
---

# Surveillance Monitoring Skill

Monitor your Protect surveillance system including cameras, events, and system health.

## What this skill does

This skill enables you to:
- Monitor all surveillance cameras and their status
- Review recent surveillance events and alerts
- Analyze motion detection and recording status
- Monitor Protect system health and storage
- Track camera connectivity
- Identify offline or underperforming cameras
- Generate surveillance reports

## When to use this skill

Use this skill when you need to:
- Check camera status and connectivity
- Review surveillance events
- Verify recording is active
- Monitor system storage usage
- Troubleshoot camera issues
- Verify coverage for specific areas
- Generate surveillance reports
- Audit event history

## Available Tools

- `get_protect_devices` - List and monitor cameras
- `get_protect_events` - Review surveillance events and alerts
- `get_protect_info` - Monitor system status and health
- `get_network_devices` - Get camera network information

## Typical Workflows

### Camera System Health Check
1. Use `get_protect_devices` to list all cameras
2. Check status and connectivity for each
3. Use `get_protect_info` for system health
4. Monitor storage usage
5. Identify any offline cameras

### Event Review
1. Use `get_protect_events` to get recent events
2. Filter by event type (motion, person, etc.)
3. Review event timeline
4. Verify recording occurred
5. Identify patterns or trends

### Coverage Verification
1. Use `get_protect_devices` to list cameras
2. Verify coverage for critical areas
3. Check camera angles and placement
4. Identify coverage gaps
5. Plan additional camera deployment

## Example Questions

- "Show all cameras and their status"
- "Are there any offline cameras?"
- "Review recent surveillance events"
- "Show motion detection events from today"
- "What's the Protect system storage usage?"
- "Verify camera coverage of all areas"
- "Generate a surveillance audit report"
- "Check camera connectivity and performance"

## Response Format

When using this skill, I provide:
- Camera status and connectivity information
- Event summaries with timestamps
- Recording status verification
- Storage usage and capacity
- System health metrics
- Coverage analysis
- Specific actionable alerts
- Recommendations for improvements

## Best Practices

- Check camera status regularly
- Review events daily for security incidents
- Monitor storage capacity proactively
- Verify coverage for critical areas
- Plan camera maintenance during off-hours
- Archive important events
- Test recovery procedures
- Document camera locations and coverage
- Maintain backup recordings
- Review and update retention policies
