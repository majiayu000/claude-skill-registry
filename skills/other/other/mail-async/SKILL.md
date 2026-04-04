---
name: mail-async
description: Durable asynchronous messaging channel for inter-agent communication. Implements write-once read-many filesystem mail using atomic writes and directory-based mailboxes.
---

# Mail Async

Filesystem-backed durable messaging for multi-agent orchestration. Every message is a JSON file written atomically into a per-agent mailbox directory. Messages are never lost -- the write-then-rename pattern guarantees that a reader sees either a complete message or no message, never a partial write.

## Purpose

Mail is the high-bandwidth, durable communication channel in the Gastown chipset -- the PCIe equivalent. It carries work assignments from the mayor, completion reports from polecats, merge notifications from the refinery, and coordination messages between any pair of agents. Because messages persist on disk, they survive process crashes, agent restarts, and network disconnections.

## Filesystem Contract

```
.chipset/state/mail/{agent-id}/{timestamp}-{from-agent}.json
```

Each agent has a dedicated mailbox directory. Incoming messages are named with the creation timestamp and sender ID, guaranteeing unique filenames and natural chronological ordering when listing the directory.

**Example paths:**

```
.chipset/state/mail/polecat-alpha/2026-03-05T10-30-00Z-mayor-a1b2c.json
.chipset/state/mail/polecat-alpha/2026-03-05T10-31-00Z-witness-d3e4f.json
.chipset/state/mail/mayor-a1b2c/2026-03-05T10-32-00Z-polecat-alpha.json
```

## Message Format

```json
{
  "from": "mayor-a1b2c",
  "to": "polecat-alpha",
  "type": "work_assignment",
  "subject": "Bead gt-abc12 assigned to your rig",
  "body": "Implement the auth middleware as specified in the convoy plan. Priority P1.",
  "timestamp": "2026-03-05T10:30:00Z",
  "read": false,
  "priority": "normal"
}
```

### Field Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `from` | string | yes | Sender agent ID |
| `to` | string | yes | Recipient agent ID |
| `type` | string | yes | Message type (see Message Types below) |
| `subject` | string | yes | Short summary for logs and listings |
| `body` | string | yes | Full message content |
| `timestamp` | string | yes | ISO 8601 creation timestamp |
| `read` | boolean | yes | Whether recipient has processed this message |
| `priority` | string | yes | `urgent`, `normal`, or `low` |

### Message Types

| Type | Sender | Recipient | Purpose |
|------|--------|-----------|---------|
| `work_assignment` | mayor | polecat | New bead assigned via hook |
| `completion_report` | polecat | mayor | Bead work completed |
| `merge_notification` | refinery | mayor | Merge result (success or conflict) |
| `health_escalation` | witness | mayor | Agent stall detected |
| `coordination` | any | any | General-purpose coordination |

## Sending a Message

The send protocol uses atomic writes to guarantee durability.

### Protocol

1. **Construct** the message JSON with all required fields
2. **Generate** the filename: `{ISO-timestamp}-{from-agent}.json` (replace colons with dashes in timestamp for filesystem compatibility)
3. **Serialize** with sorted keys for git-friendly output
4. **Write** to a temporary file in the recipient's mailbox: `.chipset/state/mail/{to}/.msg.tmp`
5. **Fsync** the temporary file to ensure data reaches disk
6. **Rename** the temporary file to the final path (atomic on POSIX)

### Pseudocode

```typescript
async function sendMail(message: MailMessage): Promise<void> {
  const mailDir = join(stateDir, 'mail', message.to);
  await mkdir(mailDir, { recursive: true });

  const safestamp = message.timestamp.replace(/:/g, '-');
  const filename = `${safestamp}-${message.from}.json`;
  const filePath = join(mailDir, filename);

  const content = serializeSorted(message);
  const tmpPath = join(mailDir, '.msg.tmp');

  const fd = await open(tmpPath, 'w');
  try {
    await fd.writeFile(content, 'utf-8');
    await fd.sync();
  } finally {
    await fd.close();
  }
  await rename(tmpPath, filePath);
}
```

## Receiving Messages

### Polling

Agents poll their mailbox directory on each state cycle. Polling returns all JSON files sorted by filename (which is sorted by timestamp due to the naming convention).

```typescript
async function checkMail(agentId: string): Promise<MailMessage[]> {
  const mailDir = join(stateDir, 'mail', agentId);
  let files: string[];
  try {
    files = (await readdir(mailDir)).filter(f => f.endsWith('.json')).sort();
  } catch {
    return []; // No mailbox yet
  }

  const messages: MailMessage[] = [];
  for (const file of files) {
    const msg = await readJson<MailMessage>(join(mailDir, file));
    if (msg) messages.push(msg);
  }
  return messages;
}
```

### Reading Unread Messages

Filter by `read === false` to get only unprocessed messages:

```typescript
const unread = (await checkMail(agentId)).filter(m => !m.read);
```

### Marking as Read

Update the `read` field atomically by rewriting the message file:

```typescript
async function markRead(agentId: string, filename: string): Promise<void> {
  const filePath = join(stateDir, 'mail', agentId, filename);
  const msg = await readJson<MailMessage>(filePath);
  if (!msg || msg.read) return;

  msg.read = true;
  await atomicWrite(filePath, serializeSorted(msg));
}
```

## Archival

Messages older than 24 hours are moved to an archive subdirectory to keep the active mailbox small and fast to scan.

```
.chipset/state/mail/{agent-id}/archive/{filename}
```

### Archival Protocol

1. List all files in the agent's mailbox
2. For each file, parse the timestamp from the filename
3. If the timestamp is more than 24 hours old, move the file to `archive/`
4. Archive moves use rename (atomic, no data loss)

```typescript
async function archiveOldMail(agentId: string): Promise<number> {
  const mailDir = join(stateDir, 'mail', agentId);
  const archiveDir = join(mailDir, 'archive');
  const cutoff = Date.now() - 24 * 60 * 60 * 1000;
  let archived = 0;

  const files = (await readdir(mailDir)).filter(f => f.endsWith('.json'));
  for (const file of files) {
    const tsStr = file.split('-').slice(0, 3).join('-').replace(/T/, 'T');
    const fileTime = new Date(tsStr).getTime();
    if (fileTime < cutoff) {
      await mkdir(archiveDir, { recursive: true });
      await rename(join(mailDir, file), join(archiveDir, file));
      archived++;
    }
  }
  return archived;
}
```

## Cross-Channel Integration

Mail integrates with other communication channels in a defined flow:

1. **Hook set** (hook-persistence): Mayor assigns work via hook
2. **Mail sent** (mail-async): Mayor sends `work_assignment` message with details
3. **GUPP activation**: Agent picks up hook, reads mail for context
4. **Work execution**: Agent processes the bead
5. **Mail sent** (mail-async): Agent sends `completion_report` to mayor
6. **Hook cleared** (hook-persistence): Work item retired

If an agent stalls during step 4, the witness detects via nudge (nudge-sync) and escalates to the mayor via `health_escalation` mail.

## Error Handling

| Condition | Behavior |
|-----------|----------|
| Recipient mailbox doesn't exist | Created automatically on first send |
| Corrupt JSON in mailbox | Logged as warning, skipped during polling |
| Disk full during write | OS error propagated, temp file left for cleanup |
| Concurrent writes to same mailbox | Safe -- each message has a unique filename |
| Agent terminated with unread mail | Mail persists; available if agent restarts |

## Constraints

- **Filesystem only:** No sockets, no tmux, no network. All communication through JSON files
- **Write-once:** Message content is immutable after creation. Only the `read` field changes
- **No guaranteed delivery order:** Recipients poll; order depends on filesystem listing
- **No acknowledgment protocol:** Sender does not get confirmation of receipt. Use mail replies for coordination
- **24-hour retention:** Active mailbox keeps messages for 24 hours before archival
