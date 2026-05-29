---
name: 哔哩哔哩字幕获取器
description: 从哔哩哔哩(B站)搜索视频、获取字幕并转换为 Markdown 格式。当用户需要搜索 B 站视频、下载视频字幕、批量获取字幕、分析视频内容时使用。支持关键词搜索、单视频处理、批量并发下载。
allowed-tools: [Bash, Read, Write, Glob]
---

# 哔哩哔哩字幕获取器

从 B 站搜索视频、批量下载字幕并转换为 Markdown 格式的专业工具。

## 核心功能

1. **关键词搜索** - 搜索 B 站视频并获取详细信息
2. **字幕下载** - 获取视频的中文字幕
3. **格式转换** - 自动转换为 Markdown 格式(时间戳 + 文本)
4. **批量处理** - 并发下载多个视频字幕(3并发)
5. **智能命名** - 使用视频标题作为文件名

## 使用场景识别

根据用户请求自动识别需要的功能:

- "搜索 Python 教程" → 执行视频搜索（根据用户需求拆分多个关键词）
- "下载 BV1xxx 的字幕" → 下载单个视频字幕
- "批量下载这些视频的字幕" → 批量下载
- "获取这个视频的文字内容" → 下载字幕并展示
- "分析这个视频讲了什么" → 下载字幕并总结

## 配置管理

### Cookie 配置

字幕 API 需要登录认证。配置文件位于:
```
~/.claude/skills/bilibili-subtitle-fetcher/config.txt
```

**格式**:
```
SESSDATA=你的SESSDATA值
bili_jct=你的bili_jct值
DedeUserID=你的用户ID
```

**获取方式**:
1. 登录 bilibili.com
2. 打开浏览器开发者工具(F12)
3. 进入 Application/存储 → Cookies
4. 复制以上三个值

**检查配置**:
如果下载失败,提示用户检查 Cookie 是否配置/过期。

### 输出目录

默认保存到:
```
~/.claude/skills/bilibili-subtitle-fetcher/subtitles/
```

如果用户指定其他目录,可以通过环境变量传递:
```bash
OUTPUT_DIR=/Users/xxx/Documents python3 bili_simple.py download BV号
```

## 高级功能

### 1. 字幕内容分析

下载后可以进行:
- 关键词提取
- 主题总结
- 时间轴分析
- 内容问答

### 2. 与其他 Skills 协作

- **cheap-summarizer**: 总结长字幕内容
- **文档处理**: 转换为其他格式(PDF、DOCX)
- **数据分析**: 提取关键词和统计信息

## 注意事项

1. **Cookie 有效期**: SESSDATA 约 30 天有效,过期需重新获取
2. **请求频率**: 已内置随机延迟,建议批量不超过 10 个视频
3. **字幕质量**: AI 生成的字幕可能有误差

## 技术细节

### API 接口
- 搜索: `api.bilibili.com/x/web-interface/search/type`
- 视频信息: `api.bilibili.com/x/web-interface/view`
- 字幕: `api.bilibili.com/x/player/v2`

### 并发控制
- 最大并发数: 3
- 随机延迟: 1-3 秒
- 超时设置: 10 秒

### 文件格式
- 输出格式: Markdown
- 编码: UTF-8
- 时间戳格式: mm:ss 或 hh:mm:ss

## 示例命令

```bash
# 搜索
python3 bili_simple.py search "关键词"

# 单个下载
python3 bili_simple.py download BV号

# 批量下载
python3 bili_simple.py batch BV1 BV2 BV3
```