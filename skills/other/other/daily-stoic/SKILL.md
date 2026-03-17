---
category: Lifestyle
id: daily-stoic
name: Daily Stoic
description: Send daily Stoic philosophy quotes from "The Daily Stoic" by Ryan Holiday.
---

# Daily Stoic

Deliver daily Stoic wisdom from "The Daily Stoic" by Ryan Holiday. Each day has a title, opening quote, and reflection.

## Quick Start

```bash
# Get today's stoic message
python3 {baseDir}/scripts/get-stoic.py

# Get specific date (MM-DD format)
python3 {baseDir}/scripts/get-stoic.py 02-03

# Output formats
python3 {baseDir}/scripts/get-stoic.py --format text    # Plain text (default)
python3 {baseDir}/scripts/get-stoic.py --format json    # JSON
python3 {baseDir}/scripts/get-stoic.py --format html    # Email-ready HTML
python3 {baseDir}/scripts/get-stoic.py --format telegram # Telegram markdown
```

## Send via Clawdbot

### Telegram
```bash
# Use Clawdbot's message tool with telegram format
MESSAGE=$(python3 {baseDir}/scripts/get-stoic.py --format telegram)
# Then send via Clawdbot message action
```

### Email (via gog skill)
```bash
# Generate HTML email
HTML=$(python3 {baseDir}/scripts/get-stoic.py --format html)

# Send via gog gmail
gog gmail send --to recipient@email.com --subject "Daily Stoic - $(date +%B\ %d)" --body-html="$HTML"
```

## Cron Setup

Schedule daily delivery at 7am:
```
0 7 * * * python3 /path/to/scripts/get-stoic.py --format telegram | send-to-telegram
```

Or use Clawdbot cron with text:
```
"Send today's Daily Stoic quote via Telegram and email to the configured recipients"
```

## Data

- **366 entries** (includes Feb 29)
- Each entry: `date_label`, `title`, `quote`, `source`, `reflection`
- Data file: `assets/stoic-daily.json`

## Example Output

**February 3rd — THE SOURCE OF YOUR ANXIETY**

_"When I see an anxious person, I ask myself, what do they want?"_
—EPICTETUS, DISCOURSES, 2.13.1

The anxious father, worried about his children. What does he want? A world that is always safe...

## Customization

Edit the HTML template in `assets/email-template.html` to match your brand.
