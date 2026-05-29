---
name: transcribe-srt
description: Transcribes SRT formatted subtitles given a video or audio content file. Use when you want subtitles for a file that doesn't have any.
---

# Transcribe SRT

## Dependencies

This skill depends on having `whisper-cli` available in your `$PATH`. It may also depend on `ffmpeg` being available if the input file isn't directly processable by `whisper-cli`. Finally, we will depend on `python` or `python3` being available to execute the script `wsp2srt.py` as a part of this skill.

## Instructions

If the input file type is not processable by `whisper-cli` then first call `ffmpeg -i "{INPUT FILE}" "{INPUT FILE}.wav"`. This will output a .wav file that `whisper-cli` can understand.

Then call `whisper-cli -m ~/whisper.cpp/models/ggml-large-v3-turbo.bin -vm ~/whisper.cpp/models/ggml-silero-v6.2.0.bin -f "{INPUT FILE}.wav" > almost_srt.txt`. If you think the input file is mostly spoken in a language other than English, then add `-l {language}` to the command.

Finally, call `python wsp2srt.py almost_srt.txt "{INPUT FILE}.srt"` to save the SRT subtitles to a file that is similarly named as the input.

## Examples

```
Can you transcribe subtitles for Videos/my_awesome_video.webm
```

Then call
```
ffmpeg -i "Videos/my_awesome_video.webm" "Videos/my_awesome_video.wav"
whisper-cli -m large-v3-turbo -vm silero-v6.2.0 -f "Videos/my_awesome_video.wav" > almost_srt.txt
python wsp2srt.py almost_srt.txt "Videos/my_awesome_video.srt"
```
