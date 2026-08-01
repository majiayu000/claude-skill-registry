---
name: voiceover
description: '|------|------|------|'
---

---
name: voiceover
description: 使用 edge-tts 生成多语言配音（中文/英文）。当需要为视频生成语音旁白、基于时间线同步配音时使用。支持语速调整、多种声音选择和配音验证。
argument-hint: [配音文案或时间线文件] [语言: zh/en]
---

# 配音生成技能

## 技术选型

| 方案 | 优点 | 缺点 |
|------|------|------|
| edge-tts | 免费、音质好、多语言支持 | 需要网络 |
| Azure TTS | 更多声音选择、更稳定 | 需要付费 |

**推荐**: edge-tts

## 声音选择

### 中文声音列表 (zh-CN)

| 声音 ID | 性别 | 风格 | 适用场景 |
|---------|------|------|----------|
| zh-CN-XiaoxiaoNeural | 女 | 温暖亲切 | 产品介绍、教程 |
| zh-CN-YunxiNeural | 男 | 专业稳重 | 企业宣传、正式场合 |
| zh-CN-YunjianNeural | 男 | 激情活力 | 科技发布、激励视频 |
| zh-CN-XiaoyiNeural | 女 | 年轻活泼 | 创意内容、轻松主题 |
| zh-CN-YunyangNeural | 男 | 新闻播报 | 资讯类、严肃主题 |

### 英文声音列表 (en-US)

| 声音 ID | 性别 | 风格 | 适用场景 |
|---------|------|------|----------|
| en-US-GuyNeural | 男 | 专业稳重 | 企业宣传、产品介绍 |
| en-US-JennyNeural | 女 | 温暖友好 | 教程、客户服务 |
| en-US-AriaNeural | 女 | 清晰专业 | 新闻、正式场合 |
| en-US-DavisNeural | 男 | 年轻活力 | 科技内容、创意视频 |
| en-US-JasonNeural | 男 | 激情活力 | 发布会、激励视频 |
| en-US-SaraNeural | 女 | 年轻活泼 | 社交媒体、轻松主题 |

### 声音选择建议

**中文视频:**

| 视频类型 | 推荐声音 |
|----------|----------|
| 产品演示 | XiaoxiaoNeural (女) |
| 公司介绍 | YunxiNeural (男) 或 XiaoxiaoNeural |
| 科技历程 | **YunjianNeural (男)** - 有激情感 |
| 教程类 | XiaoxiaoNeural (女) |
| 发布会风格 | YunjianNeural (男) |

**英文视频:**

| 视频类型 | 推荐声音 |
|----------|----------|
| 产品演示 | GuyNeural (男) 或 JennyNeural (女) |
| 公司介绍 | GuyNeural (男) 或 AriaNeural (女) |
| 科技历程 | **JasonNeural (男)** - 有激情感 |
| 教程类 | JennyNeural (女) |
| 发布会风格 | JasonNeural (男) 或 DavisNeural (男) |

## 时间线计算

### 核心公式

```python
# 最终视频时间 = 录屏事件时间 + 偏移量
DEMO_START = OPENING_DURATION + FEATURES_DURATION
final_time = recording_time + DEMO_START
```

### 图文视频时间线

对于图文展示型视频，时间线由分镜直接定义：

```python
# 场景时间配置
SCENES = {
    "opening": {"start": 0, "duration": 8},
    "scene_1": {"start": 8, "duration": 14},
    "scene_2": {"start": 22, "duration": 16},
    # ...
}

# 配音定义 - 直接基于场景时间
VOICEOVER_SEGMENTS = [
    (0.5, 7.5, "片头配音..."),      # 场景 opening 内
    (8.5, 21.5, "场景1配音..."),    # 场景 scene_1 内
    (22.5, 37.5, "场景2配音..."),   # 场景 scene_2 内
]
```

## 配音验证机制 (重要)

### 自动化验证函数

```python
def validate_voiceover(segments, total_duration):
    """
    验证配音时间线
    返回: (是否通过, 问题列表)
    """
    issues = []

    for i, seg in enumerate(segments):
        # 检查1: 配音是否超出场景时长
        actual_end = seg["start_time"] + seg["actual_duration"]
        if seg["actual_duration"] > seg["target_duration"] + 0.5:
            issues.append({
                "type": "duration_exceeded",
                "segment": i,
                "message": f"片段{i}: 实际({seg['actual_duration']:.1f}s) > 目标({seg['target_duration']:.1f}s)",
                "severity": "warning"
            })

        # 检查2: 配音是否与下一段重叠
        if i < len(segments) - 1:
            next_start = segments[i+1]["start_time"]
            if actual_end > next_start:
                issues.append({
                    "type": "overlap",
                    "segment": i,
                    "message": f"片段{i}和{i+1}重叠: {actual_end:.1f}s > {next_start:.1f}s",
                    "severity": "error"
                })

    # 检查3: 最后一段是否超出视频时长
    last_seg = segments[-1]
    last_end = last_seg["start_time"] + last_seg["actual_duration"]
    if last_end > total_duration + 1:
        issues.append({
            "type": "exceeds_video",
            "message": f"配音结束({last_end:.1f}s) > 视频时长({total_duration}s)",
            "severity": "error"
        })

    # 检查4: 空白间隙
    for i in range(len(segments) - 1):
        current_end = segments[i]["start_time"] + segments[i]["actual_duration"]
        next_start = segments[i+1]["start_time"]
        gap = next_start - current_end
        if gap > 3:
            issues.append({
                "type": "large_gap",
                "segment": i,
                "message": f"片段{i}和{i+1}之间有{gap:.1f}s空白",
                "severity": "warning"
            })

    passed = not any(issue["severity"] == "error" for issue in issues)
    return passed, issues
```

### 验证报告输出

```python
def print_validation_report(segments, total_duration):
    """打印配音验证报告"""
    passed, issues = validate_voiceover(segments, total_duration)

    print("╔" + "═" * 58 + "╗")
    print("║" + "配音验证报告".center(54) + "║")
    print("╠" + "═" * 58 + "╣")
    print("║ 片段 │ 开始   │ 目标时长 │ 实际时长 │ 状态       ║")
    print("╠" + "═" * 58 + "╣")

    for i, seg in enumerate(segments):
        status = "✅ OK" if seg["actual_duration"] <= seg["target_duration"] + 0.5 else "⚠️ 超时"
        print(f"║  {i:2d}  │ {seg['start_time']:5.1f}s │  {seg['target_duration']:5.1f}s  │  {seg['actual_duration']:5.1f}s  │ {status:10s} ║")

    print("╠" + "═" * 58 + "╣")

    if passed:
        print("║ ✅ 验证通过                                            ║")
    else:
        print("║ ❌ 验证失败，请检查以下问题:                            ║")
        for issue in issues:
            if issue["severity"] == "error":
                print(f"║   ❌ {issue['message'][:50]:50s} ║")

    print("╚" + "═" * 58 + "╝")

    return passed
```

## 完整配音脚本模板 (V2 - 多语言版)

```python
#!/usr/bin/env python3
"""
配音生成脚本 V2 - 包含验证机制 + 多语言支持
"""

import asyncio
import subprocess
from pathlib import Path
import json
import re

# ========== 配置 ==========
LANGUAGE = "zh"  # "zh" 或 "en"
VOICE = "zh-CN-YunjianNeural"  # 科技感男声
# 英文示例: VOICE = "en-US-JasonNeural"
OUTPUT_DIR = Path("public/audio")
TOTAL_DURATION = 85  # 视频总时长

# 配音段落定义 (开始时间, 结束时间, 配音文字)
VOICEOVER_SEGMENTS = [
    (0.5, 7.5, "配音内容1"),
    (8.5, 21.5, "配音内容2"),
    # ...
]

# ========== 工具函数 ==========
def get_audio_duration(file_path):
    """获取音频时长"""
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(file_path)],
        capture_output=True, text=True
    )
    return float(result.stdout.strip())

def validate_voiceover(segments, total_duration):
    """验证配音时间线"""
    issues = []

    for i, seg in enumerate(segments):
        # 检查时长
        if seg["actual_duration"] > seg["target_duration"] + 0.5:
            issues.append(f"⚠️ 片段{i}: 超时 {seg['actual_duration'] - seg['target_duration']:.1f}s")

        # 检查重叠
        if i < len(segments) - 1:
            actual_end = seg["start_time"] + seg["actual_duration"]
            next_start = segments[i+1]["start_time"]
            if actual_end > next_start:
                issues.append(f"❌ 片段{i}和{i+1}重叠")

    return len([i for i in issues if i.startswith("❌")]) == 0, issues

# ========== 多语言支持函数 ==========
def calculate_natural_duration(text, language):
    """计算文本自然朗读时长"""
    if language == "zh":
        # 中文: 约 4 字/秒
        char_count = len(re.sub(r'[^\u4e00-\u9fff]', '', text))
        return char_count / 4.0
    else:
        # 英文: 约 150 词/分钟 = 2.5 词/秒
        word_count = len(text.split())
        return word_count / 2.5

# ========== 生成函数 ==========
async def generate_segment(index, start, end, text):
    """生成单个配音片段（支持多语言）"""
    import edge_tts

    output_file = OUTPUT_DIR / f"vo_{index:02d}.mp3"
    duration_target = end - start

    # 计算语速（多语言支持）
    natural_duration = calculate_natural_duration(text, LANGUAGE)

    if natural_duration > duration_target:
        rate_adjust = min(35, int((natural_duration / duration_target - 1) * 100))
        rate = f"+{rate_adjust}%"
    elif natural_duration < duration_target * 0.7:
        rate_adjust = min(15, int((1 - natural_duration / duration_target) * 50))
        rate = f"-{rate_adjust}%"
    else:
        rate = "+0%"

    # 生成配音
    communicate = edge_tts.Communicate(text=text, voice=VOICE, rate=rate)
    await communicate.save(str(output_file))

    actual_duration = get_audio_duration(output_file)

    return {
        "index": index,
        "file": output_file.name,
        "start_time": start,
        "target_duration": duration_target,
        "actual_duration": actual_duration,
        "text": text[:20] + "...",
        "rate": rate,
        "language": LANGUAGE,
    }

def merge_audio(segments):
    """合并音频"""
    filter_parts = []
    inputs = []

    for i, seg in enumerate(segments):
        inputs.extend(["-i", str(OUTPUT_DIR / seg["file"])])
        delay_ms = int(seg["start_time"] * 1000)
        filter_parts.append(f"[{i}:a]adelay={delay_ms}|{delay_ms}[a{i}];")

    mix_inputs = "".join([f"[a{i}]" for i in range(len(segments))])
    filter_parts.append(f"{mix_inputs}amix=inputs={len(segments)}:duration=longest[out]")

    output_file = OUTPUT_DIR / "synced_voiceover.mp3"

    subprocess.run([
        "ffmpeg", "-y", *inputs,
        "-filter_complex", "".join(filter_parts),
        "-map", "[out]",
        "-t", str(TOTAL_DURATION),
        str(output_file)
    ], capture_output=True)

    return output_file

# ========== 主函数 ==========
async def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 50)
    print(f"配音生成 - 声音: {VOICE}")
    print("=" * 50)

    # 1. 生成配音
    print("\n[1/3] 生成配音片段...")
    segments = []
    for i, (start, end, text) in enumerate(VOICEOVER_SEGMENTS):
        seg = await generate_segment(i, start, end, text)
        segments.append(seg)
        print(f"  ✓ 片段{i}: {seg['actual_duration']:.1f}s (目标: {seg['target_duration']:.1f}s) 语速: {seg['rate']}")

    # 2. 验证
    print("\n[2/3] 验证配音...")
    passed, issues = validate_voiceover(segments, TOTAL_DURATION)

    if issues:
        for issue in issues:
            print(f"  {issue}")

    if not passed:
        print("\n❌ 验证失败，请检查配音时间线")
        return
    else:
        print("  ✅ 验证通过")

    # 3. 合并
    print("\n[3/3] 合并音频...")
    output = merge_audio(segments)
    final_duration = get_audio_duration(output)
    print(f"  ✓ 输出: {output}")
    print(f"  ✓ 时长: {final_duration:.1f}s")

    # 保存元数据
    metadata = {
        "voice": VOICE,
        "total_duration": TOTAL_DURATION,
        "segments": segments,
    }
    with open(OUTPUT_DIR / "voiceover_metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 50)
    print("配音生成完成!")
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(main())
```

## 语速控制

### 多语言语速计算

```python
def calculate_natural_duration(text, language="zh"):
    """计算文本自然朗读时长"""
    import re

    if language == "zh":
        # 中文: 约 4 字/秒
        char_count = len(re.sub(r'[^\u4e00-\u9fff]', '', text))
        return char_count / 4.0
    else:
        # 英文: 约 150 词/分钟 = 2.5 词/秒
        word_count = len(text.split())
        return word_count / 2.5

def calculate_rate(text, target_duration, language="zh"):
    """计算语速调整"""
    natural_duration = calculate_natural_duration(text, language)

    if natural_duration > target_duration:
        adjustment = min(35, int((natural_duration / target_duration - 1) * 100))
        return f"+{adjustment}%"
    elif natural_duration < target_duration * 0.7:
        adjustment = min(15, int((1 - natural_duration / target_duration) * 50))
        return f"-{adjustment}%"
    return "+0%"
```

### 语速参考

| 语言 | 自然语速 | 最快可调 | 最慢可调 |
|------|----------|----------|----------|
| 中文 | 4 字/秒 | +35% (5.4字/秒) | -15% (3.4字/秒) |
| 英文 | 150 词/分 | +35% (200词/分) | -15% (130词/分) |

### 建议

| 情况 | 处理方式 |
|------|----------|
| 配音太长 | 先精简文字，再考虑加速 |
| 配音太短 | 稍微减速，或延长画面 |
| 语速 > +35% | 必须精简文字 |

## FFmpeg 音频合并

### adelay 滤镜

```bash
# 单个音频延迟 5 秒
ffmpeg -i input.mp3 -af "adelay=5000|5000" output.mp3

# 多音频按时间点合并
ffmpeg -i vo_01.mp3 -i vo_02.mp3 -i vo_03.mp3 \
  -filter_complex \
  "[0:a]adelay=1000|1000[a0];\
   [1:a]adelay=5500|5500[a1];\
   [2:a]adelay=10500|10500[a2];\
   [a0][a1][a2]amix=inputs=3:duration=longest[out]" \
  -map "[out]" output.mp3
```

## 音量标准化

```bash
# 标准化到 -16 LUFS（广播标准）
ffmpeg -i input.mp4 -af "loudnorm=I=-16:TP=-1.5:LRA=11" -c:v copy output.mp4
```

## 常见问题

| 问题 | 解决方案 |
|------|----------|
| 配音和画面不同步 | 检查时间偏移计算 |
| 配音语速过快 | 精简文字或降低 rate |
| 配音段重叠 | 调整开始时间或缩短文字 |
| 空白间隙过大 | 添加过渡说明填补 |
| 音量不一致 | 使用 FFmpeg loudnorm |
| 网络失败 | 添加重试机制 |
