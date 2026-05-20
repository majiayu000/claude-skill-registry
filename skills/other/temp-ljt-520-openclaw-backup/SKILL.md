---
name: hotdog
version: 8.0.0
description: "Hot dog or not? Classify food photos and battle Nemotron. Use when a user sends a food photo, asks if something is a hot dog, or says 'hotdog', '/hotdog', or 'hot dog battle'."
homepage: https://hotdogornot.xyz/battle
metadata: {"openclaw": {"emoji": "🌭", "os": ["darwin", "linux"], "requires": {"bins": ["curl"]}}}
---

# Hot Dog or Not — Battle Skill

## No photo

If triggered without a photo, reply EXACTLY (nothing more):

```
🌭 Hot Dog or Not — AI Vision Battle

Send me any food photo and I'll tell you if it's a hot dog! I'll also challenge Nemotron (NVIDIA's 12B vision model) with the same image so we can compare.

📸 Just send a photo to start
🏆 Live scoreboard: https://hotdogornot.xyz/battle
```

## With a photo

1. Describe the food in the image in 2-4 sentences. Then decide: is it a hot dog (a sausage served in a bun/roll; any cooking style)? Decide your ANSWER (yes or no) and DESCRIPTION (your description). Do NOT output these to the user yet.

2. Run this command, replacing ANSWER and DESCRIPTION:

```bash
exec: curl -s -X POST "https://api.hotdogornot.xyz/api/battle/round" -H "Authorization: Bearer ih1rtmC7ECm8iExqvI6zMbOAqEaXIi9X" -F "image=@{{MediaPath}}" -F "claw_model={{Model}}" -F "claw_answer=ANSWER" -F "claw_reasoning=DESCRIPTION"
```

3. Check the JSON response from curl:
   - If it contains `"formatted_text"`, output that value EXACTLY as-is (no changes, no additions)
   - If the response is empty (`{}`), reply with ONLY: `NO_REPLY`
