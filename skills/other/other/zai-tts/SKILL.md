---
name: zai-tts
description: Text-to-speech conversion using GLM-TTS service via the `uvx zai-tts` command for generating audio from text. Use when (1) User requests audio/voice output with the "tts" trigger or keyword. (2) Content needs to be spoken rather than read (multitasking, accessibility, podcast, driving, cooking). (3) Using pre-cloned voices for speech.
---

# Zai-TTS

Generate high-quality text-to-speech audio using GLM-TTS service via the `uvx zai-tts` command.
Before using this skill, you need to configure the environment variables `ZAI_AUDIO_USERID` and `ZAI_AUDIO_TOKEN`,
which can be obtained by login `audio.z.ai` and executing `localStorage['auth-storage']` in the console via F12 Developer Tools.

## Usage
```shell
uvx zai-tts -t "{msg}" -o {tempdir}/{filename}.wav
uvx zai-tts -f path/to/file.txt -o {tempdir}/{filename}.wav
```

## Changing speed, volume
```shell
uvx zai-tts -t "{msg}" -o {tempdir}/{filename}.wav --speed 1.5
uvx zai-tts -t "{msg}" -o {tempdir}/{filename}.wav --speed 1.5 --volume 2
```

## Changing the voice
```shell
uvx zai-tts -t "{msg}" -o {tempdir}/{filename}.wav --voice system_002
```

## Available voices
`system_001`: Lila.  A cheerful, standard-pronunciation female voice
`system_002`: Chloe. A gentle, elegant, intelligent female voice
`system_003`: Ethan. A sunny, standard-pronunciation male voice

Retrieve all available voices using shell commands:
```shell
uvx zai-tts -l
```
If you want to use custom voices, please complete voice cloning on the website `audio.z.ai` first.
