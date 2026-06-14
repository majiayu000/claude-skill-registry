---
name: deepline-plays-feedback
description: 'Send Deepline SDK/V2 CLI feedback or bug reports, including environment info and the current Claude/Cowork session transcript. Use when the user asks to report a Deepline bug, share a failing run, or send feedback from a V2 SDK workflow.'
disable-model-invocation: false
---

# Deepline Plays Feedback

Send feedback or a bug report to Deepline support from the V2 SDK CLI.

## Steps

1. **Get feedback text.** Use the argument if provided, such as `/deepline-plays-feedback plays run failed after upload`. Otherwise ask the user for the message to send.

2. **Confirm.** Ask before sending because the report includes the feedback text, environment info collected by the CLI, and a session transcript. If the user cancels, stop.

3. **Send the feedback text.** The V2 SDK command is `feedback send`; the text is positional:

   ```bash
   deepline feedback send "{feedback text}" --json
   ```

4. **Send the session transcript.** Try the normal Claude transcript location first:

   ```bash
   deepline sessions send --current-session --json
   ```

   If that reports no session files and `~/mnt/.claude/projects` exists, the run is likely in Cowork. Bridge the mounted transcript directory, then retry. If `--current-session` still cannot resolve a session, send the newest mounted transcript directly:

   ```bash
   if [ -d "$HOME/mnt/.claude/projects" ]; then
     mkdir -p "$HOME/.claude"
     ln -sfn "$HOME/mnt/.claude/projects" "$HOME/.claude/projects" 2>/dev/null || true
     deepline sessions send --current-session --json || deepline sessions send --file "$(ls -t "$HOME"/mnt/.claude/projects/*/*.jsonl | head -1)" --json
   fi
   ```

5. **Avoid stale command shapes.** Do not use the legacy `provide-feedback` command, a `--text` flag for feedback, or the old singular session form; those target older or unsupported CLI surfaces.

6. Tell the user it was sent.
