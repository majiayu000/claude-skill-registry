---
name: docx-comment-reply
description: "Reply to comments (批注) in Word .docx/.doc files: extract comment context, draft replies, write threaded replies back, and validate OOXML."
---

# Word 批注回复（.docx/.doc）

这个 skill 解决的问题：把 Word 文档里的批注（comments）按“原文锚点上下文”整理出来，生成待回复清单，然后把回复以 **threaded replies** 的方式写回到新的 `.docx` 文件里（不改原文件）。

适用场景：专利/论文/合同/内部评审等需要“逐条回复批注”的文档。

## 输出物（约定）

在当前工作目录的 `outputs/` 下生成：
- `*_批注定位与上下文_*.md`：人可读的批注+锚点上下文报告
- `*_comment_context_*.json`：机器可读上下文（用于并行写回复/自动化）
- `*_replies_todo_*.json`：待回复模板（键=comment_id，值=空字符串）
- `*_批注已回复_*.docx`：写回批注回复后的最终交付文件

## 工作流（推荐）

### 1) 提取批注上下文

```powershell
python scripts/extract_comment_context.py --input "path\\to\\file.docx"
```

如果输入是 `.doc`，脚本会尝试用 LibreOffice `soffice` 转成 `.docx` 后继续。

### 2) 生成回复（由你/Claude 来写）

- 打开 `outputs\\*_批注定位与上下文_*.md`，逐条写回复。
- 把回复填进 `outputs\\*_replies_todo_*.json`（保持 JSON 结构不变）。

**回复口径（强约束）**
- 直接回答问题（别写“后续补充”但不说补什么）
- 必须贴合锚点原文（避免泛泛而谈）
- 不要用“老师您好/您好”类开头；口语化但专业

### 3) 写回批注回复并生成新 docx

```powershell
python scripts/apply_comment_replies.py `
  --unpacked "outputs\\<xxx>_unpacked_<timestamp>" `
  --replies "outputs\\<xxx>_replies_todo_<timestamp>.json" `
  --author "YourName" `
  --initials "YN"
```

### 4) 校验（必须）

脚本默认会在保存时做 schema + redlining 校验；如需单独验证：

```powershell
python ..\\docx\\ooxml\\scripts\\validate.py "outputs\\<unpacked_dir>" --original "outputs\\<out>.docx"
```

## 并行（XL 可选）

当批注数量较多（例如 ≥20 条）：
1. 先跑提取脚本得到 `comment_context.json`
2. 以 comment_id 分片给子代理写回复（每个子代理 prompt 末尾加 `$vibe`）
3. 合并为一个 replies JSON，再执行 `apply_comment_replies.py`

