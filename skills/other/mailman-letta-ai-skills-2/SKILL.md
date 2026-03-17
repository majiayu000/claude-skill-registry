---
name: mailman
description: Guidance for setting up mailing list servers with Postfix and Mailman3. This skill should be used when configuring email infrastructure, integrating Mailman3 with Postfix MTA, creating mailing lists, or troubleshooting mail delivery issues.
---

# Mailman - Mailing List Server Setup

## Overview

This skill provides guidance for setting up and configuring mailing list servers using Postfix (MTA) and Mailman3. It covers proper integration patterns, configuration best practices, and verification strategies to avoid common pitfalls.

## Approach

### Phase 1: Documentation Review

Before making any configuration changes:

1. Read Mailman3's official documentation on Postfix integration
2. Understand the `[mta]` section configuration in `mailman.cfg`
3. Identify the native integration mechanisms (postfix_lmtp, postfix_domains)
4. Review existing configuration files to understand current state

### Phase 2: Configuration Architecture

The proper integration between Postfix and Mailman3 involves:

1. **Mailman3 MTA Configuration** (`mailman.cfg`):
   - Configure `[mta]` section with proper `incoming` and `outgoing` settings
   - Set `postfix_map_exe` for automatic alias generation
   - Configure LMTP listener settings

2. **Postfix Integration**:
   - Configure `main.cf` to use mailman-generated transport maps
   - Set up virtual alias maps pointing to mailman's generated files
   - Avoid creating custom transport definitions when native integration exists

3. **LMTP Delivery**:
   - Verify LMTP port configuration (default: 8024)
   - Ensure Postfix can communicate with Mailman's LMTP server

### Phase 3: Implementation Order

Execute configuration in this order:

1. Configure Mailman3's `mailman.cfg` for MTA integration
2. Restart Mailman3 services to apply configuration
3. Verify Mailman generates transport/alias files
4. Configure Postfix to use Mailman-generated maps
5. Reload Postfix configuration
6. Create mailing lists
7. Test mail delivery

## Verification Strategies

### Pre-Implementation Verification

- Check if services are running: `systemctl status mailman3` and `systemctl status postfix`
- Verify LMTP port is listening: `ss -tlnp | grep 8024`
- Check Mailman's configured MTA: `mailman conf | grep -A10 '\[mta\]'`

### Configuration Verification

- Validate Postfix configuration: `postfix check`
- Test Postfix configuration syntax before reload
- Verify Mailman-generated files are populated (not empty)
- Check file permissions on transport maps

### Post-Implementation Verification

- Send test emails and verify delivery
- Check mail logs: `journalctl -u postfix` and `journalctl -u mailman3`
- Verify list creation persisted in database
- Test service survival after restart

### Database Verification

- Verify list creation persisted: check with `mailman lists` command
- Understand Mailman3's transaction model for list operations
- Ensure database commits occur properly

## Common Pitfalls

### 1. Empty Alias/Transport Files

**Symptom**: Mailman-generated postfix files (postfix_lmtp, postfix_domains) are empty.

**Cause**: Improper `[mta]` section configuration in `mailman.cfg`.

**Investigation**: Check `[mta]` configuration settings rather than creating workaround scripts.

### 2. Custom Transport Instead of Native Integration

**Anti-pattern**: Creating custom `mailman:` transport in `master.cf` and manual alias scripts.

**Problem**: Duplicates built-in functionality, breaks when lists change, requires manual intervention.

**Solution**: Use Mailman3's native `postfix_map_exe` configuration for automatic alias generation.

### 3. List Creation Not Persisting

**Symptom**: List created via API/CLI but doesn't appear after service restart.

**Cause**: Database transaction not committed properly.

**Investigation**: Check Mailman's transaction handling, verify database configuration.

### 4. Malformed Configuration Sections

**Anti-pattern**: Adding non-standard sections like `[styles]` or `[style.legacy-default]` with settings that don't follow Mailman3's schema.

**Problem**: Settings like `subscription_policy` should be set on lists, not as style definitions.

**Solution**: Consult official schema documentation before adding configuration sections.

### 5. LMTP Port Mismatch

**Symptom**: Mail delivery fails with connection refused.

**Cause**: Postfix configured to connect to wrong LMTP port.

**Verification**: Check Mailman's actual LMTP port vs Postfix transport configuration.

### 6. Missing Automatic Synchronization

**Symptom**: New lists don't receive mail without manual intervention.

**Cause**: Missing `postfix_maps` configuration for automatic regeneration.

**Solution**: Configure Mailman to automatically update Postfix maps when lists change.

## Debugging Workflow

When mail delivery fails:

1. **Trace the mail path**: Check Postfix logs for delivery attempts
2. **Verify transport lookup**: `postmap -q listname@domain /path/to/transport`
3. **Test LMTP directly**: `telnet localhost 8024`
4. **Check Mailman logs**: Look for LMTP connection errors
5. **Verify list exists**: `mailman lists -d domain`

## Key Configuration Files

| File | Purpose |
|------|---------|
| `/etc/mailman3/mailman.cfg` | Main Mailman3 configuration |
| `/etc/postfix/main.cf` | Postfix main configuration |
| `/etc/postfix/master.cf` | Postfix service definitions |
| `/var/lib/mailman3/data/postfix_lmtp` | Mailman-generated LMTP transport map |
| `/var/lib/mailman3/data/postfix_domains` | Mailman-generated relay domains |

## Testing Checklist

Before declaring success:

- [ ] Services running and enabled
- [ ] LMTP port accessible
- [ ] Transport maps populated (not empty)
- [ ] Test email delivered to list
- [ ] List archives accessible
- [ ] Configuration survives service restart
- [ ] New list creation triggers automatic map update
