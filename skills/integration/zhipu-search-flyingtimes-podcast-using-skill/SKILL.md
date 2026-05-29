---
name: zhipu-search
description: 根据用户给出的搜索关键语句，调用zhipu的搜索引擎得到搜索结果。
allowed-tools: Read, Grep, Glob, Write, Search
---

# zhipu-search

## Instructions
1、所有的运行中输出的临时程序、文件、代码统一放到当前项目根目录下的output/
4、根据用户给出的搜索关键语句{original}，先进行一次分析，如果包含有关时间的搜索条件，例如今天、昨天、明天、后天、下礼拜等，先获取当前日期并根据当前日期计算准确日期后，按照计算好的日期来构建新的搜索查询语句{modify}。
5、调用zhipu的搜索引擎,搜索{modify}得到搜索结果，并给出来源信息和url。
```
cd .claude/skills/zhipu-search && uv run zhipu_searcher.py "你的问题"
```