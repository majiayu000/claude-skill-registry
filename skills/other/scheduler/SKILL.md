---
name: scheduler
description: 'Use when asked to set, list, pause, update, or delete a personal reminder or lightweight local task that fires at a confirmed time or interval. Installs through the platform backend with per-platform mechanisms, writes a metadata record, and verifies both. Refuses destructive scheduled actions. Not for remote, credential, publish, or deploy operations.'
---

# Scheduler

## Contract

| Field | Bound contract |
|---|---|
| Trigger | The user asks to set a personal reminder or run a lightweight local task at a specific time or interval, or to list, pause, update, or delete an existing scheduled item. |
| Authority | Reversible-local, user-level scheduling only. A scheduled action that is itself destructive or irreversible is refused outright, not installed after confirmation. No admin elevation, no credentials, no remote mutation. Every mutation has a stated rollback path: remove the entry and its metadata record. |
| Side effect | Creates, pauses, unpauses, deletes, or updates one named local scheduled item per confirmed request. Never modifies unrelated system schedules. |
| Done | Every item exists in both the backend and the metadata record, and the user received a confirmation with name, action, human-readable time, and delivery method. |

## Inputs

- Action (required): the reminder message or the exact command to run.
- Schedule (required): an absolute time, a relative delay, or a recurrence pattern.
- **Delivery method** (required before install, asked when unspecified): notification, terminal output, or background command execution.
- Timezone (optional): defaults to the user's local timezone.
- Name (optional): defaults to a generated kebab-case name.

## Procedure

1. Parse intent, action, schedule, and delivery. Classify the request as reminder or task. When the classification is unclear, assume reminder and say so. Ask the one blocking question when anything is ambiguous: vague times ("tomorrow morning"), unclear timezone, or unclear action. Done when: intent, action, schedule, and delivery method are resolved or the blocking question is asked.
2. Normalize the schedule into a human-readable rule in local time. Whether an absolute timestamp, relative delay, or recurrence, express it in the user's local timezone unless stated otherwise. Confirm this normalized schedule with the user before installing anything. Done when: the normalized schedule is confirmed by the user.
3. Generate a stable kebab-case name and write the metadata record. Derive the name from the action ("review PRs" becomes `review-prs`); on collision, append a numeric suffix. Write the metadata record under `~/.odin/scheduler/` with the schema: name, type, backend path, normalized schedule, delivery, status. Done when: the metadata record is written.
4. Install through the platform backend with a stated mechanism per platform. Quoting and escaping rules for the action string are part of this step:
   - macOS: write a launchd plist to `~/Library/LaunchAgents/<name>.plist`. Notifications use `osascript`. The unload path is `launchctl unload ~/Library/LaunchAgents/<name>.plist`.
   - Linux: write a systemd user timer unit plus service unit to `~/.config/systemd/user/`. Verify with `systemctl --user list-timers`. When systemd is unavailable, fall back to a crontab line installed with `crontab -l | { cat; echo "<line>"; } | crontab -`. Notifications use `notify-send` with terminal output as fallback.
   - Windows: create a Task Scheduler task using `schtasks /create`. Notifications use a PowerShell toast.
   One-shot entries are self-cleaning: after firing, the backend entry and metadata record are removed. Done when: the entry is installed in the backend.
5. Verify the entry exists in the backend and the metadata record matches. Check the backend listing for the entry. Compare the backend entry's schedule and command against the metadata record. Confirm to the user with name, action, human-readable time, and delivery method. Done when: the backend entry and metadata record are both verified and the confirmation is shown.

## Failure and recovery

- Ambiguous input: ask the one blocking question and stop. Nothing is scheduled.
- Mechanism unavailable or outside authority: state the limitation and the nearest local alternative. Wait for the user's decision. No install.
- Backend install failure: remove any partially created entry and its metadata record. Report the failure. Never claim the item is scheduled.
- Destructive action: refuse under authority. Do not install. Ask the user to confirm the exact action if they want to proceed, but do not schedule it.
- Rollback for every mutation: delete the OS scheduler entry and its metadata record under `~/.odin/scheduler/`. Any failure before install leaves the system unchanged.

## Output

One of: a confirmation block (name, action, human-readable trigger in local time, delivery method); a list report (name, type, schedule, delivery, status per item); a state transition (paused, active, updated, deleted) with the updated record; or a terminal `blocked` classification naming the exact unresolved question or failing step.
