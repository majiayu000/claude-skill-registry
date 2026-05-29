---
name: terminal
description: >
  Command line, npm, git, and shell basics. Activated when Claude runs Bash commands.
  Demystifies the terminal for non-technical users.
---

# Terminal & Command Line — CodeSensei Teaching Module

## The Terminal
- **Analogy:** The terminal is like texting your computer. Instead of clicking buttons, you type instructions and it responds. It's not scarier than that.
- **Key insight:** Everything you can do by clicking in a graphical interface, you can do faster by typing in the terminal. Developers prefer typing because it's faster and scriptable.

## Essential Commands
Teach these as they appear in the user's session:

### Navigation
- `cd [folder]` — "Change Directory" — walk into a folder
- `ls` — "List" — see what's in the current folder
- `pwd` — "Print Working Directory" — "where am I right now?"
- **Analogy:** You're in a building. `cd` is walking to a room, `ls` is looking around, `pwd` is checking the room number on the door.

### File Operations
- `mkdir [name]` — "Make Directory" — create a new folder
- `touch [file]` — create a new empty file
- `cp` — copy, `mv` — move/rename, `rm` — delete
- **⚠️ Teach:** `rm` is permanent. There's no trash can.

### npm (Node Package Manager)
- **Analogy:** An app store for code. Other developers built tools and shared them. `npm install` downloads those tools into your project.
- `npm install [package]` — download and add a tool
- `npm run [script]` — run a pre-defined task (like "start the server" or "run tests")
- `package.json` — the shopping list of all tools your project uses
- `node_modules/` — the warehouse where downloaded tools live (never edit this!)

### git (Version Control)
- **Analogy:** A time machine for your code. Every "commit" is a save point you can go back to.
- `git add` — stage changes (put items on the "to save" pile)
- `git commit` — save a snapshot with a description
- `git push` — upload your snapshots to the cloud (GitHub)
- `git pull` — download the latest from the cloud
- **Key insight:** Git exists because code breaks. It lets you undo mistakes by going back to when things worked.

### Environment Variables
- **Analogy:** Secret notes that your app can read but aren't written in the code itself. Like a password you whisper instead of writing on a whiteboard.
- `.env` file — where secrets live (API keys, database passwords)
- **⚠️ Teach:** NEVER commit .env files to git. That's like posting your passwords publicly.

## Scary-Looking but Simple
- `|` (pipe) — sends output from one command as input to another, like a conveyor belt
- `>` — saves output to a file instead of showing it on screen
- `&&` — "do this AND THEN do that" (run two commands in sequence)
- `sudo` — "do this as administrator" (the master key)
