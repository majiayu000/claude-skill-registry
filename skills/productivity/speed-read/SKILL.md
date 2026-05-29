---
name: speed-read
description: Display text using RSVP speed reading. Use when presenting explanations, summaries, or any text the user should read quickly. Launches speed-read script with the provided text.
---
<!-- @agent-architect owns this file. Delegate changes, don't edit directly. -->

<purpose>
Display text using RSVP (Rapid Serial Visual Presentation) for 400-900+ WPM reading. Use when presenting explanations, summaries, or substantial text benefiting from focused reading.
</purpose>

<execution>
TMPFILE=$(mktemp /tmp/speed-read-XXXXXX.txt)
echo "$CONTENT" > "$TMPFILE"
speed-read "$TMPFILE"
rm "$TMPFILE"
</execution>

<controls>
SPACE/p: pause/resume | q/ESC: quit | +/-: adjust speed | r: restart
</controls>

<notes>
Default 400 WPM, adjustable with --wpm flag. Remove markdown formatting (plain text works best). Keep text concise. Requires ANSI-capable terminal.
</notes>
