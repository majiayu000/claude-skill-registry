---
name: wispr-dictionary
description: Add words to the Wispr Flow dictionary. Use when the user wants to add a word, phrase, or snippet to Wispr Flow for voice dictation.
user-invocable: true
---

# Wispr Flow Dictionary

Add entries to the Wispr Flow personal dictionary for improved voice dictation recognition.

## Usage

```bash
# Add a word/phrase to recognize
wispr-add-dictionary "METR"

# Add with replacement (what you say -> what gets typed)
wispr-add-dictionary "teh" "the"

# Add a snippet/text expansion
wispr-add-dictionary -s "shrug" "¯\_(ツ)_/¯"

# Add without refreshing the UI
wispr-add-dictionary --no-refresh "word"
```

## How It Works

1. Adds the entry directly to the Wispr Flow SQLite database at `~/Library/Application Support/Wispr Flow/flow.sqlite`
2. Switches to the Dictionary tab in Wispr Flow (via AppleScript accessibility)
3. Clicks the refresh button to sync

## Requirements

**On host (macOS):**
- Wispr Flow must be running
- The Hub window must be open (will error if closed)
- Accessibility permissions for Terminal/shell to control System Events

**From dev containers:**
- The `url-listener` must be running on the host
- Uses `host.docker.internal` to forward requests to the host

## Entry Types

- **Dictionary word**: Just a phrase - helps Wispr recognize the word correctly
- **Replacement**: Maps what you say to what gets typed (e.g., common typos, abbreviations)
- **Snippet** (`-s`): Text expansion triggered by a keyword

## Notes

- Entries are added to your personal dictionary (not team dictionary)
- The refresh happens without bringing Wispr Flow to the foreground
- Deleting entries from the database does not delete them from Wispr servers
