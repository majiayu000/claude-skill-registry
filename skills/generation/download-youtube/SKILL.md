---
name: download-youtube
description: Downloads videos from Youtube. Use when you have a youtube.com URL and you want the video/audio content to be downloaded.
---

# Download Youtube

## Instructions

When you want to download a video from a youtube.com URL, you may also have a hint at what to call that video.

You should call `cd ~/Videos/ && yt-dlp --embed-subs "{YOUTUBE URL}"` and check the output filename. The output filename is frequently overly verbose. If it is, you should rename the file to make it easier to read.

## Examples

```
Can you download youtube.com/watch?v=abc
```

Call `cd ~/Videos/ && yt-dlp --embed-subs "https://youtube.com/watch?v=abc"` using the bash tool. Once it's done, call `ls -lt ~/Videos/ | head` to check what the newly downloaded file is. Then rename it to something easier by calling `mv "~/Videos/Some Long Video - Author Is Great.webm" "~/Videos/some_long_video.webm"`
