---
name: appstore-connect
description: Use when working with App Store Connect, TestFlight builds, beta testers, beta groups, or checking build review status. Covers iOS app management, TestFlight distribution, and beta testing workflows.
---

# App Store Connect

Comprehensive App Store Connect integration for iOS app management and TestFlight beta testing.

## Quick Reference

| Operation | Tool | Requires Approval |
|-----------|------|-------------------|
| List apps | `appstore_list_apps` | No |
| List builds | `testflight_list_builds` | No |
| Check build status | `testflight_check_build_status` | No |
| Get build details | `testflight_get_build` | No |
| Submit for review | `testflight_submit_for_review` | Yes |
| Get review status | `testflight_get_review_status` | No |
| List testers | `testflight_list_testers` | No |
| Add tester | `testflight_add_tester` | Yes |
| Remove tester | `testflight_remove_tester` | Yes |
| List groups | `testflight_list_groups` | No |
| Create group | `testflight_create_group` | Yes |
| Delete group | `testflight_delete_group` | Yes |
| Add build to group | `testflight_add_build_to_group` | Yes |
| Add testers to group | `testflight_add_testers_to_group` | Yes |
| Remove testers from group | `testflight_remove_testers_from_group` | Yes |

## Common Workflows

### Check Latest Build Status
```
# Quick status check for an app
testflight_check_build_status(app_id="6746294071")

# Or list recent builds with details
testflight_list_builds(app_id="6746294071", limit=5)
```

### Submit Build for Beta Review
```
# 1. Find the build ID
testflight_list_builds(app_id="6746294071", limit=1)

# 2. Submit for review (requires approval)
testflight_submit_for_review(build_id="abc123")

# 3. Check status later
testflight_get_review_status(build_id="abc123")
```

### Manage Beta Testers
```
# List all testers
testflight_list_testers()

# Add a new tester
testflight_add_tester(
    email="tester@example.com",
    first_name="John",
    last_name="Doe",
    group_ids="group-id-1,group-id-2"
)

# Find tester by email
testflight_list_testers(email="tester@example.com")
```

### Manage Beta Groups
```
# List all groups for an app
testflight_list_groups(app_id="6746294071")

# Create external beta group
testflight_create_group(
    app_id="6746294071",
    name="Beta Testers",
    is_internal=False,
    public_link_enabled=True
)

# Add build to group (makes it available to testers)
testflight_add_build_to_group(group_id="group-123", build_ids="build-456")

# Add testers to group
testflight_add_testers_to_group(group_id="group-123", tester_ids="tester-1,tester-2")
```

## Beta Review States

| State | Meaning |
|-------|---------|
| `WAITING_FOR_REVIEW` | Submitted, awaiting Apple review |
| `IN_REVIEW` | Currently being reviewed |
| `APPROVED` | Approved for TestFlight distribution |
| `REJECTED` | Rejected, check App Store Connect for details |

## Processing States

| State | Meaning |
|-------|---------|
| `PROCESSING` | Build is being processed |
| `FAILED` | Processing failed |
| `INVALID` | Build is invalid |
| `VALID` | Ready for distribution |

## Authentication

Uses App Store Connect API with JWT authentication. Required environment variables:
- `APPSTORE_KEY_ID` - API Key ID
- `APPSTORE_ISSUER_ID` - Issuer ID
- `APPSTORE_KEY_PATH` - Path to .p8 private key file

## Rate Limits

App Store Connect API has rate limits. For bulk operations:
- Space requests when adding many testers
- Use pagination for large result sets (limit parameter)

## Common Issues

**"Build already submitted"**: A build can only have one active review submission. Wait for current review or use a new build.

**"Tester already exists"**: Use `testflight_list_testers(email="...")` to find existing tester ID, then add to groups.

**"Group not found"**: Use `testflight_list_groups()` to get valid group IDs.
