---
name: mtv-rewind
description: "Watch classic MTV music videos from the 80s, 90s, and 2000s right inside Telegram. Use when: user wants to watch MTV, music videos, retro TV, or says anything like 'play MTV', 'I want my MTV', or 'what's on'. NOT for: searching specific songs, playing audio-only music, or streaming modern live TV. No API key needed."
homepage: https://wantmymtv.xyz
metadata:
  {
    "openpaw":
      { "emoji": "📺", "category": "entertainment", "channels": ["telegram", "discord", "web"] },
  }
---

# MTV Rewind

Stream classic MTV music videos — 80s, 90s, 2000s — right inside your chat.

## When to Use

✅ **USE this skill when:**

- "Play MTV"
- "I want my MTV"
- "Put on some music videos"
- "What's on MTV?"
- "Play 80s/90s/2000s music videos"
- "I need background vibes"
- User wants retro music video content

## When NOT to Use

❌ **DON'T use this skill when:**

- User wants a specific song → use spotify-player skill
- User wants audio only → use spotify-player or music skills
- User wants modern/current music videos → this is retro content only
- User wants live broadcast TV → this is curated retro MTV content

## Channels

Available channels to filter by era:

| Channel   | Parameter | What You Get                                   |
| --------- | --------- | ---------------------------------------------- |
| **All**   | `all`     | Mix of everything — 80s, 90s, 2000s            |
| **80s**   | `80s`     | Peak MTV era — hair metal, new wave, synth pop |
| **90s**   | `90s`     | Grunge, hip-hop golden age, TRL era            |
| **2000s** | `2000s`   | Pop-punk, crunk, early YouTube era             |

## How to Respond

### Telegram (Primary)

Send a message with an inline Web App button that opens the MTV Rewind player. Use Telegram's `reply_markup` with an `InlineKeyboardButton` containing a `web_app` URL:

**Player URL format:**

```
https://wantmymtv.xyz/embed.html?channel={channel}
```

**Response format — always include:**

1. A short Paw-style message about what's playing
2. An inline keyboard button that opens the player

**Example response structure:**

For "play MTV" or "put on some videos":

- Message: "MTV Rewind is on. All eras, no commercials, no skips. Just vibes."
- Button: `[📺 Watch MTV Rewind]` → opens `https://wantmymtv.xyz/embed.html?channel=all`

For "play 80s MTV":

- Message: "1985 called. They want you back. Here's the good stuff."
- Button: `[📺 Watch 80s MTV]` → opens `https://wantmymtv.xyz/embed.html?channel=80s`

For "play 90s MTV":

- Message: "TRL energy. Grunge. Hip-hop. The decade that broke everything. Enjoy."
- Button: `[📺 Watch 90s MTV]` → opens `https://wantmymtv.xyz/embed.html?channel=90s`

For "play 2000s MTV":

- Message: "Low-rise jeans and pop-punk. You asked for it."
- Button: `[📺 Watch 2000s MTV]` → opens `https://wantmymtv.xyz/embed.html?channel=2000s`

### Discord / Web

Send the embed URL directly as a clickable link with a short description:

```
📺 MTV Rewind — https://wantmymtv.xyz/embed.html?channel=all
```

## Personality Notes

Paw should treat this like a jukebox moment. Keep responses short, nostalgic, and a little smug — like a cat who has impeccable taste in music. Don't over-explain. Drop the link and let the music speak.

Good tone:

- "You have taste. Here."
- "Serving visuals. You're welcome."
- "The algorithm could never."

Bad tone:

- "Sure! Here's a link to watch MTV Rewind music videos from the retro era!"
- "I've found a music video streaming service for you!"

## Direct URLs

- All channels: https://wantmymtv.xyz/embed.html?channel=all
- 80s: https://wantmymtv.xyz/embed.html?channel=80s
- 90s: https://wantmymtv.xyz/embed.html?channel=90s
- 2000s: https://wantmymtv.xyz/embed.html?channel=2000s
- Main site: https://wantmymtv.xyz
