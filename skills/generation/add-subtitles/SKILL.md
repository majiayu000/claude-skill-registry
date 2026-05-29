---
name: add-subtitles
description: Adds SRT formatted subtitles to a video file when you want a video to have subtitles.
---

# Add Subtitles

## Instructions

This assumes you have created subtitles or have downloaded subtitles in SRT format. If you don't have subtitles then you can use the transcribe-srt skill to create SRT formatted subtitles.

Once you have subtitles, you can call `ffmpeg -n -i "{INPUT FILE}.webm" -i "{INPUT FILE}.srt" -s 720x480 -c:s mov_text "{INPUT FILE}.mp4"`. This will output the "{INPUT FILE}.mp4" file with the "{INPUT FILE}.srt" subtitles.

Typically the video files will be stored in ~/Videos.

## Examples

```
Can you please add the subtitles ~/Videos/my_video.srt to ~/Videos/my_video.webm?
```

Then you would call `ffmpeg -n -i "~/Videos/my_video.webm" -i "~/Videos/my_video.srt" -s 720x480 -c:s mov_text "~/Videos/my_video.mp4"`.
