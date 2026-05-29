---
name: videocut:剪辑
description: 执行视频剪辑。根据确认的删除任务执行FFmpeg剪辑。触发词：执行剪辑、开始剪、确认剪辑
---

<!--
input: delete_segments.json（审核网页导出）
output: 剪辑后视频
pos: 执行 skill，用户在审核网页确认后调用

架构守护者：一旦我被修改，请同步更新：
1. ../README.md 的 Skill 清单
2. /CLAUDE.md 路由表
-->

# 剪辑

> 用户在审核网页一次性确认好 → 执行剪辑 → 完成

## 快速使用

```
用户: 确认，执行剪辑
用户: 全删
用户: 保留静音3和5，其他都删
```

## 前置条件

需要先执行 `/videocut:剪口播v2` 生成删除任务 TodoList

## 流程

```
前置：用户在审核网页（/videocut:剪口播v2）一次性确认所有删除
    ↓
1. 读取 delete_segments.json（网页导出）
    ↓
2. 计算保留时间段
    ↓
3. 生成 FFmpeg filter_complex
    ↓
4. 执行剪辑
    ↓
5. 完成
```

**核心原则**：所有审核在前置阶段完成，剪辑阶段只执行，不再循环。

## 进度 TodoList

启动时创建：

```
- [ ] 读取 delete_segments.json
- [ ] 计算保留时间段
- [ ] 执行 FFmpeg 剪辑
- [ ] 验证输出视频
```

---

## 一、读取删除任务

从审核网页导出的 `delete_segments.json` 读取：

```json
[
  {"start": 0, "end": 20.2},
  {"start": 29.06, "end": 36.4}
]
```

**直接使用时间戳**，网页已确保精确边界。

---

## 二、FFmpeg 命令

**必须用 `filter_complex + trim`**，不能用 concat demuxer（口播片段多且短，必须帧级别精确）。

```bash
ffmpeg -y -i "file:input.mp4" \
  -filter_complex "$FILTER" \
  -map "[outv]" -map "[outa]" \
  -c:v libx264 -preset fast -crf 18 \
  -c:a aac -b:a 192k \
  "file:output.mp4"
```

### filter_complex 格式

```
[0:v]trim=start=0:end=1.36,setpts=PTS-STARTPTS[v0];
[0:a]atrim=start=0:end=1.36,asetpts=PTS-STARTPTS[a0];
[0:v]trim=start=2.54:end=10.5,setpts=PTS-STARTPTS[v1];
[0:a]atrim=start=2.54:end=10.5,asetpts=PTS-STARTPTS[a1];
...
[v0][v1]...concat=n=N:v=1:a=0[outv];
[a0][a1]...concat=n=N:v=0:a=1[outa]
```

**注意**：文件名含冒号需加 `file:` 前缀。

---

## 三、输出文件

```
output.mp4    # 剪辑后视频
```

