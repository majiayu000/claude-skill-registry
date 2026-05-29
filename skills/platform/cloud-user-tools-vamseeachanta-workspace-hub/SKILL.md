---
name: cloud-user-tools
description: Flow Nexus user management and system utilities. Use for profile management, storage operations, real-time subscriptions, and platform administration.
version: 1.0.0
category: cloud
type: skill
capabilities:
  - profile_management
  - storage_operations
  - realtime_subscriptions
  - system_monitoring
  - seraphina_consultation
  - notification_management
tools:
  - mcp__flow-nexus__user_profile
  - mcp__flow-nexus__user_update_profile
  - mcp__flow-nexus__user_stats
  - mcp__flow-nexus__storage_upload
  - mcp__flow-nexus__storage_delete
  - mcp__flow-nexus__storage_list
  - mcp__flow-nexus__storage_get_url
  - mcp__flow-nexus__realtime_subscribe
  - mcp__flow-nexus__realtime_unsubscribe
  - mcp__flow-nexus__realtime_list
  - mcp__flow-nexus__seraphina_chat
  - mcp__flow-nexus__system_health
  - mcp__flow-nexus__audit_log
  - mcp__flow-nexus__execution_stream_subscribe
  - mcp__flow-nexus__execution_stream_status
  - mcp__flow-nexus__execution_files_list
  - mcp__flow-nexus__execution_file_get
related_skills:
  - cloud-auth
  - cloud-payments
  - cloud-sandbox
---

# Cloud User Tools

> Manage user profiles, file storage, real-time subscriptions, and access platform utilities in Flow Nexus.

## Quick Start

```javascript
// Update profile
await mcp__flow-nexus__user_update_profile({
  user_id: "user_id",
  updates: {
    full_name: "Developer Name",
    bio: "AI Developer",
    github_username: "username"
  }
});

// Upload file to storage
await mcp__flow-nexus__storage_upload({
  bucket: "private",
  path: "projects/config.json",
  content: JSON.stringify({ key: "value" }),
  content_type: "application/json"
});

// Subscribe to real-time updates
await mcp__flow-nexus__realtime_subscribe({
  table: "tasks",
  event: "INSERT",
  filter: "status=eq.pending"
});

// Consult Queen Seraphina
const advice = await mcp__flow-nexus__seraphina_chat({
  message: "How should I architect my distributed system?",
  enable_tools: true
});
```

## When to Use

- Managing user profiles and account settings
- Uploading and organizing files in cloud storage
- Setting up real-time notifications and subscriptions
- Monitoring system health and diagnostics
- Consulting Queen Seraphina for guidance
- Tracking execution streams and output files
- Reviewing audit logs for security

## Prerequisites

- Flow Nexus account with active session
- MCP server `flow-nexus` configured
- Appropriate permissions for storage operations

## Core Concepts

### Storage Buckets

| Bucket | Access | Purpose |
|--------|--------|---------|
| **private** | User-only | Personal files, configs |
| **public** | Anyone | Shared assets, downloads |
| **shared** | Team | Collaboration files |
| **temp** | Auto-expire | Transient data |

### Real-time Events

| Event | Description |
|-------|-------------|
| `INSERT` | New record created |
| `UPDATE` | Record modified |
| `DELETE` | Record removed |
| `*` | All events |

### Queen Seraphina

AI assistant providing:
- Architectural guidance
- Best practices advice
- Complex decision support
- Tool execution (when enabled)

## MCP Tools Reference

### Profile Management

```javascript
// Get profile
mcp__flow-nexus__user_profile({
  user_id: "user_id"
})
// Returns: { id, email, full_name, bio, tier, created_at }

// Update profile
mcp__flow-nexus__user_update_profile({
  user_id: "user_id",
  updates: {
    full_name: "New Name",
    bio: "Developer bio",
    github_username: "username",
    website: "https://example.com"
  }
})

// Get statistics
mcp__flow-nexus__user_stats({
  user_id: "user_id"
})
// Returns: { apps_published, credits_earned, challenges_completed }
```

### Storage Operations

```javascript
// Upload file
mcp__flow-nexus__storage_upload({
  bucket: "private",           // private, public, shared, temp
  path: "folder/file.json",
  content: "file content",
  content_type: "application/json"
})

// List files
mcp__flow-nexus__storage_list({
  bucket: "private",
  path: "folder/",             // Path prefix
  limit: 100                   // Max 1000
})
// Returns: { files: [{ name, size, created_at }] }

// Get public URL
mcp__flow-nexus__storage_get_url({
  bucket: "public",
  path: "assets/image.png",
  expires_in: 3600             // Seconds
})
// Returns: { url, expires_at }

// Delete file
mcp__flow-nexus__storage_delete({
  bucket: "private",
  path: "folder/file.json"
})
```

### Real-time Subscriptions

```javascript
// Subscribe to table changes
mcp__flow-nexus__realtime_subscribe({
  table: "tasks",              // Table name
  event: "INSERT",             // INSERT, UPDATE, DELETE, *
  filter: "status=eq.pending"  // Optional filter
})
// Returns: { subscription_id }

// List subscriptions
mcp__flow-nexus__realtime_list()
// Returns: { subscriptions: [{ id, table, event }] }

// Unsubscribe
mcp__flow-nexus__realtime_unsubscribe({
  subscription_id: "subscription_id"
})
```

### Execution Streams

```javascript
// Subscribe to execution stream
mcp__flow-nexus__execution_stream_subscribe({
  stream_type: "claude-code",   // claude-code, claude-flow-swarm, github-integration
  sandbox_id: "sandbox_id",
  deployment_id: "deployment_id"
})

// Check stream status
mcp__flow-nexus__execution_stream_status({
  stream_id: "stream_id"
})

// List execution files
mcp__flow-nexus__execution_files_list({
  stream_id: "stream_id",
  created_by: "claude-code",    // claude-code, claude-flow, git-clone, user
  file_type: "js"
})

// Get file content
mcp__flow-nexus__execution_file_get({
  file_id: "file_id",
  file_path: "/path/to/file"
})
```

### Queen Seraphina

```javascript
mcp__flow-nexus__seraphina_chat({
  message: "Your question or request",
  conversation_history: [       // Optional previous messages
    { role: "user", content: "Previous question" },
    { role: "assistant", content: "Previous answer" }
  ],
  enable_tools: true            // Allow tool execution
})
// Returns: { response, tools_used }
```

### System Utilities

```javascript
// Check system health
mcp__flow-nexus__system_health()
// Returns: { status, services: { api, database, storage } }

// Get audit logs
mcp__flow-nexus__audit_log({
  user_id: "user_id",           // Optional filter
  limit: 100                    // Max 1000
})
// Returns: { events: [{ timestamp, action, user, details }] }
```

## Usage Examples

### Example 1: Complete Profile Setup

```javascript
// Get current profile
const profile = await mcp__flow-nexus__user_profile({
  user_id: "your_user_id"
});

console.log(`Current profile: ${profile.full_name}`);

// Update with complete information
await mcp__flow-nexus__user_update_profile({
  user_id: "your_user_id",
  updates: {
    full_name: "Alex Developer",
    bio: "Full-stack developer specializing in AI and distributed systems",
    github_username: "alexdev",
    twitter_username: "alexdev",
    website: "https://alexdev.io",
    location: "San Francisco, CA",
    company: "Tech Startup",
    preferences: {
      theme: "dark",
      notifications: true,
      newsletter: true
    }
  }
});

// Get user statistics
const stats = await mcp__flow-nexus__user_stats({
  user_id: "your_user_id"
});

console.log(`
Profile Statistics:
- Apps Published: ${stats.apps_published}
- Credits Earned: ${stats.credits_earned}
- Challenges Completed: ${stats.challenges_completed}
`);
```

### Example 2: File Storage Management

```javascript
// Upload project configuration
await mcp__flow-nexus__storage_upload({
  bucket: "private",
  path: "projects/my-app/config.json",
  content: JSON.stringify({
    name: "My Application",
    version: "1.0.0",
    settings: {
      debug: false,
      maxConnections: 100
    }
  }, null, 2),
  content_type: "application/json"
});

// Upload public asset
await mcp__flow-nexus__storage_upload({
  bucket: "public",
  path: "assets/logo.svg",
  content: '<svg>...</svg>',
  content_type: "image/svg+xml"
});

// Get public URL for sharing
const logoUrl = await mcp__flow-nexus__storage_get_url({
  bucket: "public",
  path: "assets/logo.svg",
  expires_in: 86400  // 24 hours
});

console.log(`Share this URL: ${logoUrl.url}`);

// List all project files
const files = await mcp__flow-nexus__storage_list({
  bucket: "private",
  path: "projects/my-app/",
  limit: 50
});

console.log("Project files:");
for (const file of files.files) {
  console.log(`- ${file.name} (${file.size} bytes)`);
}

// Clean up old files
await mcp__flow-nexus__storage_delete({
  bucket: "private",
  path: "projects/old-project/config.json"
});
```

### Example 3: Real-time Notifications

```javascript
// Subscribe to task updates
const taskSub = await mcp__flow-nexus__realtime_subscribe({
  table: "tasks",
  event: "*",
  filter: "user_id=eq.your_user_id"
});

console.log(`Subscribed to tasks: ${taskSub.subscription_id}`);

// Subscribe to workflow completions
const workflowSub = await mcp__flow-nexus__realtime_subscribe({
  table: "workflow_executions",
  event: "UPDATE",
  filter: "status=eq.completed"
});

// Subscribe to new messages
const messageSub = await mcp__flow-nexus__realtime_subscribe({
  table: "messages",
  event: "INSERT"
});

// List all active subscriptions
const subscriptions = await mcp__flow-nexus__realtime_list();

console.log("Active subscriptions:");
for (const sub of subscriptions.subscriptions) {
  console.log(`- ${sub.table}: ${sub.event}`);
}

// Unsubscribe when done
await mcp__flow-nexus__realtime_unsubscribe({
  subscription_id: taskSub.subscription_id
});
```

### Example 4: Consulting Queen Seraphina

```javascript
// Ask for architectural guidance
const advice = await mcp__flow-nexus__seraphina_chat({
  message: "I need to design a real-time collaborative editing system. What architecture would you recommend?",
  enable_tools: false
});

console.log("Seraphina's advice:", advice.response);

// Follow-up with context
const followUp = await mcp__flow-nexus__seraphina_chat({
  message: "How should I handle conflict resolution in that architecture?",
  conversation_history: [
    { role: "user", content: "I need to design a real-time collaborative editing system..." },
    { role: "assistant", content: advice.response }
  ],
  enable_tools: false
});

// Ask for help with tool execution
const withTools = await mcp__flow-nexus__seraphina_chat({
  message: "Create a mesh swarm with 5 agents for my project",
  enable_tools: true
});

console.log("Tools used:", withTools.tools_used);
```

### Example 5: Execution Stream Monitoring

```javascript
// Subscribe to Claude Code execution
const stream = await mcp__flow-nexus__execution_stream_subscribe({
  stream_type: "claude-code",
  sandbox_id: "active_sandbox_id"
});

// Check stream status
const status = await mcp__flow-nexus__execution_stream_status({
  stream_id: stream.stream_id
});

console.log(`Stream status: ${status.status}`);
console.log(`Output lines: ${status.output_lines}`);

// List files created during execution
const files = await mcp__flow-nexus__execution_files_list({
  stream_id: stream.stream_id,
  created_by: "claude-code"
});

console.log("Files created:");
for (const file of files.files) {
  console.log(`- ${file.path} (${file.type})`);
}

// Get specific file content
const fileContent = await mcp__flow-nexus__execution_file_get({
  file_id: files.files[0].id
});

console.log("File content:", fileContent.content);
```

### Example 6: System Monitoring and Audit

```javascript
// Check system health
const health = await mcp__flow-nexus__system_health();

console.log(`System Status: ${health.status}`);
console.log("Services:");
for (const [service, status] of Object.entries(health.services)) {
  console.log(`- ${service}: ${status}`);
}

// Review audit logs
const auditLogs = await mcp__flow-nexus__audit_log({
  user_id: "your_user_id",
  limit: 50
});

console.log("Recent Activity:");
for (const event of auditLogs.events) {
  console.log(`${event.timestamp}: ${event.action} - ${event.details}`);
}
```

## Execution Checklist

- [ ] Complete profile setup with all relevant information
- [ ] Organize storage with proper bucket selection
- [ ] Set up real-time subscriptions for important events
- [ ] Monitor execution streams during development
- [ ] Consult Seraphina for complex decisions
- [ ] Review audit logs periodically
- [ ] Clean up unused subscriptions and files

## Best Practices

1. **Profile Completeness**: Fill out all profile fields for better discoverability
2. **Bucket Selection**: Use appropriate buckets for access control
3. **File Organization**: Create clear folder structures in storage
4. **Subscription Hygiene**: Unsubscribe when monitoring is complete
5. **Seraphina Usage**: Provide context for better advice
6. **Audit Review**: Check logs regularly for security

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `profile_not_found` | Invalid user_id | Verify user_id |
| `storage_upload_failed` | Invalid bucket or path | Check bucket name and path format |
| `subscription_failed` | Invalid table or filter | Verify table exists and filter syntax |
| `seraphina_unavailable` | Service temporarily down | Retry later |
| `file_not_found` | Invalid file_id or path | Use storage_list to find valid files |

## Metrics & Success Criteria

- **Profile Completeness**: 100% of fields filled
- **Storage Organization**: Clear folder structure
- **Active Subscriptions**: Minimal unused subscriptions
- **Response Time**: <2s for storage operations

## Integration Points

### With Authentication

```javascript
// Profile updates require authentication
const auth = await mcp__flow-nexus__auth_status({ detailed: true });
if (auth.authenticated) {
  await mcp__flow-nexus__user_update_profile({ user_id: auth.user_id, ... });
}
```

### With Sandboxes

```javascript
// Monitor sandbox execution
await mcp__flow-nexus__execution_stream_subscribe({
  stream_type: "claude-code",
  sandbox_id: sandbox.sandbox_id
});
```

### Related Skills

- [cloud-auth](../cloud-auth/SKILL.md) - Authentication
- [cloud-payments](../cloud-payments/SKILL.md) - Credits
- [cloud-sandbox](../cloud-sandbox/SKILL.md) - Execution environments

## References

- [Flow Nexus User Guide](https://flow-nexus.ruv.io/docs/user)
- [Storage Documentation](https://flow-nexus.ruv.io/docs/storage)

## Version History

- **1.0.0** (2026-01-02): Initial release - converted from flow-nexus-user-tools agent
