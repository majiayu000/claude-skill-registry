---
name: arxiv
description: 使用 arXiv 进行论文检索与获取：按关键词搜索、按 arXiv ID 获取摘要、下载论文 PDF。适用于做文献调研时快速定位论文、提取摘要、批量下载。
---

# arXiv

使用本技能完成三类任务：

- 搜索：按关键词/语法查询返回论文列表
- 摘要：按 arXiv ID 获取摘要
- 下载：按 arXiv ID 下载 PDF

使用附带脚本：`scripts/arxiv_cli.py`。

## 快速开始

先运行帮助信息；把脚本当黑盒使用。

```bash
python scripts/arxiv_cli.py --help
```

## 搜索（关键词 / 查询语法）

```bash
python scripts/arxiv_cli.py search \
  --query "speech enhancement on-device" \
  --max-results 10 \
  --sort-by relevance \
  --sort-order descending
```

查询字符串会透传给 arXiv（经 `arxiv.py` 封装）。常用示例：

- `all:whisper AND cat:cs.CL`
- `ti:"streaming ASR" AND (cat:cs.CL OR cat:eess.AS)`

需要机器可读输出时，输出 JSON：

```bash
python scripts/arxiv_cli.py search --query "all:tiny asr" --max-results 5 --json
```

## 获取摘要（按 arXiv ID）

```bash
python scripts/arxiv_cli.py abstract --id 2401.01234
```

支持版本号（例如 `2401.01234v2`）。

## 下载 PDF（按 arXiv ID）

写入目录：

```bash
python scripts/arxiv_cli.py download --id 2401.01234 --outdir ./papers
```

写入指定文件：

```bash
python scripts/arxiv_cli.py download --id 2401.01234 --outfile "./papers/2401.01234.pdf"
```

## 注意事项

- 依赖包：`pip install arxiv`
- 避免高并发；必要时用 `search` 的 `--delay-seconds` 控制请求间隔
