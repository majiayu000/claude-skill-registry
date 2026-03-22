---
name: hour-meter
clawhub: tardis
description: Track elapsed time from a set epoch with tamper-evident locking. Like an analog Hobbs meter but digital. Use for tracking uptime, service hours, time since events, sobriety counters, project duration, equipment runtime. Supports create, lock (seal), check, verify against external hash, list, and export operations.
---

# Hour Meter (TARDIS on ClawHub)

Life event tracker with three modes, milestone notifications, and tamper-evident verification.

> **ClawHub Note:** This skill is published as **TARDIS** on ClawHub after the original `hour-meter` listing was lost due to a repository sync issue.

## Three Modes

### COUNT UP — Time since an event
```bash
# Quit smoking tracker
meter.py create smoke-free --start "2025-06-15T08:00:00Z" -d "Last cigarette"
meter.py milestone smoke-free -t hours -v 720 -m "🎉 30 days smoke-free!"
meter.py lock smoke-free  # → Gives you paper code to save
```

### COUNT DOWN — Time until an event
```bash
# Baby due date
meter.py create baby --start "2026-01-15" --end "2026-10-15" --mode down -d "Baby arriving!"
meter.py milestone baby -t percent -v 33 -m "👶 First trimester complete!"
```

### COUNT BETWEEN — Journey from start to end
```bash
# Career span
meter.py create career --start "1998-05-15" --end "2038-05-15" -d "40-year career"
meter.py milestone career -t percent -v 50 -m "📊 Halfway through career!"
meter.py career --meter career --rate 85 --raise-pct 2.5
```

## Tamper-Evident Persistence

When you lock a meter, you get a **paper code** — a short, checksummed code you can write on paper:

```
╔══════════════════════════════════════════════════════════════╗
║  PAPER CODE (write this down):                               ║
║     318B-3229-C523-2F9C-V                                    ║
╚══════════════════════════════════════════════════════════════╝
```

### Four Ways to Save (Non-Technical)

**1️⃣ PAPER** — Write the code on paper/sticky note
- 20 characters with dashes, easy to copy
- Built-in checksum catches typos when verifying
- Keep in wallet, safe, or taped to equipment

**2️⃣ PHOTO** — Screenshot or photograph the lock screen
- Store in camera roll, cloud photos
- Visual backup, no typing required

**3️⃣ WITNESS FILE** — Auto-saved to `~/.openclaw/meter-witness.txt`
- Append-only log of all locked meters
- Sync folder to Dropbox/iCloud/Google Drive for cloud backup
- Contains paper code + full hash + timestamp

**4️⃣ EMAIL TO SELF** — Click the mailto: link or copy the one-liner
- Opens your email client with pre-filled subject and body
- Or copy the compact message: `🔒 my-meter | Code: XXXX-XXXX-XXXX-XXXX-C | Locked: 2026-02-02`
- Send to yourself, search inbox later to verify

**5️⃣ SENDGRID EMAIL** — Auto-send verification email on lock
```bash
# Set your SendGrid API key
export SENDGRID_API_KEY=SG.xxxxx
export SENDGRID_FROM_EMAIL=verified@yourdomain.com

# Lock and email in one command
meter.py lock my-meter --email you@example.com
```
- Sends a beautifully formatted HTML email with paper code
- Requires a verified sender in SendGrid (see SendGrid docs)
- Great for automated workflows

### Verifying Later

```bash
# With paper code (catches typos!)
meter.py verify my-meter "318B-3229-C523-2F9C-V"

# → ✅ VERIFIED! Paper code matches.
# → ⚠️ CHECKSUM ERROR! (if you have a typo)
# → ❌ MISMATCH! (if tampered)
```

## Milestones

```bash
meter.py milestone <name> --type hours --value 1000 --message "1000 hours!"
meter.py milestone <name> --type percent --value 50 --message "Halfway!"
meter.py check-milestones  # JSON output for automation
```

### Email Milestone Notifications (v1.3.0)

Get milestone notifications sent directly to your email:

```bash
# Create meter with email notifications
meter.py create my-meter \
  --notify-email you@example.com \
  --from-email verified@yourdomain.com \
  -d "My tracked event"

# Add milestones as usual
meter.py milestone my-meter -t hours -v 24 -m "🎉 24 hours complete!"

# When check-milestones runs and a milestone fires, email is sent automatically
meter.py check-milestones
# → Triggers milestone AND sends email notification
```

**Email includes:**
- 🎯 Milestone message
- ⏱️ Current elapsed time
- 📝 Meter description

Requires `SENDGRID_API_KEY` environment variable.

### Milestone Notifications: Heartbeat vs Cron

**Recommended: HEARTBEAT** (~30 min resolution)
- Add to `HEARTBEAT.md`: `Run meter.py check-milestones and notify triggered`
- Batches with other periodic checks
- Cost-efficient: shares token usage with other heartbeat tasks
- Good for most use cases (quit tracking, career milestones, etc.)

### Milestone Messages

Milestones post their message text to the configured notification channel when triggered:

```bash
# Posts the message when milestone fires
meter.py milestone my-meter -t hours -v 24 -m "🎉 24 hours complete!"
```

Configure in HEARTBEAT.md:
```markdown
- Run meter.py check-milestones and post triggered milestone messages to the configured channel
```

> **Advanced:** Milestone messages prefixed with `ACTION:` can optionally be treated as agent instructions by your heartbeat config. This is an opt-in feature — see README.md for security considerations.

**Alternative: CRON** (precise timing)
- Use when exact timing matters (e.g., countdown to event)
- ⚠️ **Cost warning:** Cron at 1-minute intervals = 1,440 API calls/day = expensive!
- If using cron, keep intervals ≥15 minutes to manage costs
- Best for one-shot reminders, not continuous monitoring

**Rule of thumb:** If 30-minute resolution is acceptable, use heartbeat. Save cron for precision timing.

## Quick Reference

```bash
meter.py create <name> [--start T] [--end T] [--mode up|down|between] [-d DESC]
meter.py lock <name>                # Seal + get paper code
meter.py verify <name> <code>       # Verify paper code
meter.py check <name>               # Status + progress
meter.py milestone <name> -t hours|percent -v N -m "..."
meter.py check-milestones           # All milestones (JSON)
meter.py witness [--show] [--path]  # Witness file
meter.py list                       # All meters
meter.py career [--meter M] [--rate R] [--raise-pct P]
meter.py export [name]              # JSON export
```

## SendGrid Email Webhook Server

Receive real-time notifications when recipients open, click, bounce, or unsubscribe from your meter verification emails.

### Setup

```bash
# Start webhook server with Discord webhook (recommended)
python sendgrid_webhook.py --port 8089 --discord-webhook https://discord.com/api/webhooks/xxx/yyy

# Or process events manually (for agent to post)
python sendgrid_webhook.py --process-events
python sendgrid_webhook.py --process-events --json
```

### Discord Webhook Setup (Recommended)

1. In your Discord channel, go to **Settings > Integrations > Webhooks**
2. Click **New Webhook**, copy the URL
3. Pass to `--discord-webhook` or set `DISCORD_WEBHOOK_URL` env var

### SendGrid Setup

1. Go to **SendGrid > Settings > Mail Settings > Event Webhook**
2. Click **"Create new webhook"** (or edit existing)
3. Set HTTP POST URL to: `https://your-domain.com/webhooks/sendgrid`
4. Select all event types under **Actions to be posted**:
   - **Engagement data:** Opened, Clicked, Unsubscribed, Spam Reports, Group Unsubscribes, Group Resubscribes
   - **Deliverability Data:** Processed, Dropped, Deferred, Bounced, Delivered
   - **Account Data:** Account Status Change
5. Click **"Test Integration"** to verify - this fires all event types to your webhook
6. **Important:** Click **Save** to enable the webhook!
7. (Optional) Enable **Signed Event Webhook** for security and set `SENDGRID_WEBHOOK_PUBLIC_KEY`

![SendGrid Webhook Setup](docs/sendgrid-webhook-setup.png)

### Event Types

| Event | Emoji | Description |
|-------|-------|-------------|
| delivered | ✅ | Email reached recipient |
| open | 👀 | Recipient opened email |
| click | 🔗 | Recipient clicked a link |
| bounce | ⚠️ | Email bounced |
| unsubscribe | 🔕 | Recipient unsubscribed |
| spamreport | 🚨 | Marked as spam |

### Environment Variables

```bash
SENDGRID_WEBHOOK_PUBLIC_KEY    # For signature verification (optional)
SENDGRID_WEBHOOK_MAX_AGE_SECONDS  # Max timestamp age (default: 300)
WEBHOOK_PORT                   # Server port (default: 8089)
DISCORD_WEBHOOK_URL            # Discord webhook URL
WEBHOOK_LOG_FILE               # Log file path
```

## The 80,000 Hours Concept

Career as finite inventory: 40 years × 2,000 hrs/year = 80,000 hours.

```bash
meter.py career --hours-worked 56000 --rate 85 --raise-pct 2.5
# → 12.3 years remaining, $2.4M earning potential
```
