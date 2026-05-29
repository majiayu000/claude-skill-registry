---
name: tidal-search
description: Search for artists, albums, or tracks on Tidal. Use when the user wants to find music, look up an artist, search for a song or album.
allowed-tools: Bash, Read, Grep
argument-hint: "<artist|album|track> <query>"
---

# Tidal Search

Search for artists, albums, or tracks on Tidal and display results as a formatted table.

## Commands

### search artist
- **Usage**: `tidal-cli --json search artist "<query>"`
- **Arguments**: query (string)
- **Output**: `[{id, name}]`

### search album
- **Usage**: `tidal-cli --json search album "<query>"`
- **Arguments**: query (string)
- **Output**: `[{id, name, artist, year}]`

### search track
- **Usage**: `tidal-cli --json search track "<query>"`
- **Arguments**: query (string)
- **Output**: `[{id, name, artist}]`

## Instructions

1. Parse `$ARGUMENTS`:
   - First word: search type (`artist`, `album`, or `track`)
   - Remaining words: the search query
   - If no arguments or missing search type, show usage: `/tidal-search <artist|album|track> <query>`
   - If no query provided after the type, ask the user to provide a search term

2. Run the appropriate command based on search type:
   - **artist**: `tidal-cli --json search artist "<query>"`
   - **album**: `tidal-cli --json search album "<query>"`
   - **track**: `tidal-cli --json search track "<query>"`

3. Parse the JSON array output and format as a markdown table:
   - **artist**: columns `ID` and `Name`
   - **album**: columns `ID`, `Name`, `Artist`, and `Year`
   - **track**: columns `ID`, `Name`, and `Artist`

4. If the result array is empty, display: "No results found for `<type>: <query>`."

## Error Handling

- If exit code is non-zero, read stderr:
  - `"Error: Not authenticated"` → "You need to authenticate first. Run `/tidal-auth` to log in."
  - `"Error: Unable to connect to Tidal"` → "Network error: unable to reach Tidal. Check your internet connection."
  - Any other error → display the raw error message with label "Error:"
