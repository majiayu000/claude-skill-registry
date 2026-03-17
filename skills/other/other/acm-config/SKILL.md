---
name: acm-config
description: Use when the user wants to customize Claudikins Automatic Context Manager behavior, configure trigger threshold, snooze duration, summary length, or runs '/acm:config'. Interactively asks questions and saves preferences to config file.
---

# Claudikins Automatic Context Manager Interactive Configuration

You are helping the user configure Claudikins Automatic Context Manager. This skill guides you through an interactive configuration process where you ask the user questions and save their preferences to `~/.claude/claudikins-acm.conf`.

## Configuration Flow

Follow this conversational flow to configure Claudikins Automatic Context Manager:

### 1. Welcome & Current Settings

First, check if a config file exists and show current settings:

```bash
# Check for existing config
if [ -f ~/.claude/claudikins-acm.conf ]; then
    echo "Current Claudikins Automatic Context Manager Configuration:"
    cat ~/.claude/claudikins-acm.conf
else
    echo "No configuration found. Let's set up Claudikins Automatic Context Manager!"
fi
```

### 2. Ask Configuration Questions

Ask the user about each setting in a friendly, conversational way:

**Context Trigger Threshold:**
- Question: "At what context percentage should the handoff dialog appear?"
- Default: 60
- Valid range: 50-90
- Explain: "This controls when Claudikins alerts you. Lower = more frequent alerts, higher = fewer alerts but less context headroom."

**Snooze Duration:**
- Question: "How long should the snooze duration be (in minutes)?"
- Default: 5
- Valid range: 1-60
- Explain: "When you click 'SNOOZE', how long should Claudikins wait before asking again?"

**Summary Token Length:**
- Question: "How detailed should handoff summaries be (in tokens)?"
- Default: 500
- Valid range: 200-2000
- Explain: "Larger = more detailed summaries but takes longer to generate. 500 is usually perfect."

**Dialog Style:**
- Question: "Which dialog style do you prefer?"
- Options: "vibrant" (colorful, current default) or "minimal" (subtle colors)
- Default: vibrant
- Explain: "Vibrant uses bright orange/pink colors. Minimal uses muted tones."

### 3. Validate Input

For each answer:
- Ensure values are within valid ranges
- If invalid, explain why and ask again
- Provide examples of good values

### 4. Save Configuration

After all questions are answered, create the config file:

```bash
cat > ~/.claude/claudikins-acm.conf << EOF
# Claudikins Automatic Context Manager Configuration
# Generated on $(date)

# Context trigger threshold (50-90)
THRESHOLD=${threshold_value}

# Snooze duration in seconds
SNOOZE_DURATION=$((snooze_minutes * 60))

# Summary token length (200-2000)
SUMMARY_TOKENS=${summary_tokens}

# Dialog style (vibrant|minimal)
DIALOG_STYLE="${dialog_style}"
EOF
```

### 5. Apply Changes

After saving, offer to reload the configuration:

```bash
# Source the new config
source ~/.claude/claudikins-acm.conf
echo "Configuration saved to ~/.claude/claudikins-acm.conf"
echo ""
echo "Note: Changes will take effect in new sessions or after running:"
echo "  source ~/.claude/claudikins-acm.conf"
```

### 6. Show Summary

Display a friendly summary of what was configured:

```
╔═══════════════════════════════════════════╗
║   Claudikins Automatic Context Manager Configuration Saved!     ║
╚═══════════════════════════════════════════╝

✓ Trigger threshold: 60%
✓ Snooze duration: 5 minutes
✓ Summary length: 500 tokens
✓ Dialog style: vibrant

Your changes will take effect in new sessions.
```

## Tone & Style

- Be conversational and friendly
- Explain technical terms in simple language
- Show enthusiasm about customization
- Use the Claudikins branding colors (orange, pink, cyan) in output
- No emoji (matches Claudikins' clean aesthetic)

## Example Interaction

```
USER: /acm:config

ASSISTANT: Let's configure Claudikins Automatic Context Manager! I'll ask you a few questions about your preferences.

Current settings not found. Let's set up fresh!

First question: At what context percentage should the handoff dialog appear?

The default is 60%, which means you'll get alerted when your session is 60% full.
This gives you plenty of headroom. You can set it anywhere from 50% to 90%.

What would you like? (Press enter for 60%)
```

## Additional Commands

If the user wants to:
- **View current config**: Show the contents of `~/.claude/claudikins-acm.conf`
- **Reset to defaults**: Delete the config file and recreate with defaults
- **Edit manually**: Open the config file in their editor

## Error Handling

- If config file cannot be written, check permissions on `~/.claude/`
- If values are out of range, explain valid ranges and ask again
- If user cancels (Ctrl+C), save partial configuration if any values were set

## Integration Notes

The config file will be sourced by:
- `install.sh` during installation (if exists)
- `handoff-prompt.sh` at runtime
- `statusline-command.sh` for threshold value

Format is simple bash variables that can be sourced directly.
