---
name: videocut:字幕
description: 字幕生成与烧录。转录→词典纠错→审核→烧录。触发词：加字幕、生成字幕、字幕
---

# 字幕

> 转录 → 纠错 → 审核 → 匹配 → 烧录

## 流程

```
1. 转录视频（本地 FunASR）
    ↓
2. 词典纠错 + 分句
    ↓
3. 输出字幕稿（纯文本，一句一行）
    ↓
【用户审核修改】
    ↓
4. 用户给回修改后的文本
    ↓
5. 我匹配时间戳 → 生成 SRT
    ↓
6. 烧录字幕（FFmpeg）
```

---

## 转录

使用 `剪口播/scripts/transcribe_local.py` 脚本：

```bash
python 剪口播/scripts/transcribe_local.py video.mp4 --output=transcript.json
```

输出 JSON 包含：
- `full_text`: 完整文本
- `chars`: 字符级时间戳

**优点**：
- 中文识别准确
- 字符级时间戳，分句精确
- 与剪口播共用同一脚本

### ⚠️ 脚本位置规则

**字幕相关脚本必须放在 `字幕/scripts/` 文件夹中**：
- `generate_subtitle_draft.py` - 从转录结果生成分句字幕稿
- `generate_srt.py` - 生成SRT字幕文件
- 禁止在其他文件夹创建临时脚本

**原因**：保持项目结构清晰，便于复用和维护

---

## 分句逻辑

从字符级时间戳生成字幕句：

```javascript
/**
 * 将字符数组分割为字幕句
 * @param {Array} chars - 字符数组 [{char, start, end}, ...]
 * @param {number} maxLen - 每行最大字数，默认 15
 * @param {number} pauseThreshold - 停顿阈值（秒），默认 0.5
 */
function splitToSubtitles(chars, maxLen = 15, pauseThreshold = 0.5) {
  const subtitles = [];
  let current = { text: '', start: 0, end: 0 };

  for (let i = 0; i < chars.length; i++) {
    const char = chars[i];
    const prevEnd = i > 0 ? chars[i - 1].end : 0;
    const gap = char.start - prevEnd;

    // 分句条件：标点 / 停顿 / 超长
    const isPunc = /[，。？！、：；]/.test(char.char);
    const isPause = gap >= pauseThreshold;
    const isTooLong = current.text.length >= maxLen;

    if ((isPunc || isPause || isTooLong) && current.text.length > 0) {
      // 如果是标点，加上标点再分句
      if (isPunc) {
        current.text += char.char;
        current.end = char.end;
      }
      subtitles.push({ ...current });
      current = { text: '', start: char.start, end: char.end };
      if (isPunc) continue;
    }

    if (current.text.length === 0) {
      current.start = char.start;
    }
    current.text += char.char;
    current.end = char.end;
  }

  // 最后一句
  if (current.text.length > 0) {
    subtitles.push(current);
  }

  return subtitles;
}
```

---

## 字幕规范

| 规则 | 说明 |
|------|------|
| 一屏一行 | 不换行，不堆叠 |
| ≤15字/行 | 超过15字必须拆分（4:3竖屏） |
| 句尾无标点 | `你好` 不是 `你好。` |
| 句中保留标点 | `先点这里，再点那里` |

---

## 词典纠错

读取 `词典.txt`，每行一个正确写法：

```
skills
Claude
iPhone
```

自动识别变体：`claude` → `Claude`

---

## 字幕稿格式

**我给用户的**（纯文本，≤15字/行）：

```
今天给大家分享一个技巧
很多人可能不知道
其实这个功能
藏在设置里面
你只要点击这里
就能看到了
```

**用户修改后给回我**，我再匹配时间戳生成 SRT。

---

## SRT 生成

```javascript
/**
 * 生成 SRT 格式字幕
 */
function generateSRT(subtitles) {
  return subtitles.map((sub, i) => {
    const start = formatTime(sub.start);
    const end = formatTime(sub.end);
    // 去掉句尾标点
    const text = sub.text.replace(/[，。？！、：；]$/, '');
    return `${i + 1}\n${start} --> ${end}\n${text}\n`;
  }).join('\n');
}

function formatTime(seconds) {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = Math.floor(seconds % 60);
  const ms = Math.floor((seconds % 1) * 1000);
  return `${pad(h)}:${pad(m)}:${pad(s)},${pad(ms, 3)}`;
}

function pad(n, len = 2) {
  return String(n).padStart(len, '0');
}
```

---

## 样式

默认：24号白字、黑色描边、底部居中

**可选样式：**
| 样式 | 说明 |
|------|------|
| 默认 | 白字黑边 |
| 黄字 | 黄字黑边（醒目） |

用户可说：
- "字大一点" → 32号
- "放顶部" → 顶部居中
- "黄色字幕" → 黄字黑边

---

## 烧录命令

```bash
ffmpeg -i video.mp4 -vf "subtitles=video.srt:force_style='FontSize=24,FontName=PingFang SC,OutlineColour=&H000000&,Outline=2,MarginV=30'" -c:a copy output.mp4
```

---

## 输出

```
01-xxx_字幕稿.txt   # 纯文本，用户编辑
01-xxx.srt          # 字幕文件
01-xxx-字幕.mp4     # 带字幕视频
```
