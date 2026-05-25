---
name: audio
description: TTS + 词级对齐
expected_outputs:
  - "**/*.mp3"
---

# audio · TTS + 词级对齐

NextFrame audio 流程(TTS 合成 → WhisperX 字级对齐 → karaoke.html)。

## 推进状态机

第一步必做:
```
Bash("nf-guide audio")      # 读 state machine
```

核心命令:
- `Bash("nf-tts batch <batch.json> --dir <out_dir>")` · 批次合成 mp3 + timeline.json + srt
- `Bash("nf-tts <text> -v <voice>")` · 单条合成

voice 选:
- edge 免费: zh-CN-XiaoxiaoNeural(晓晓) / YunxiNeural(云希) / YunyangNeural(云扬)
- volcengine 付费(seed-tts-2.0): 需 `-b volcengine`

## 产物

- mp3 音频
- timeline.json(whisperx 词级时间戳 · 卡拉 OK 字幕同步)
- srt 字幕
