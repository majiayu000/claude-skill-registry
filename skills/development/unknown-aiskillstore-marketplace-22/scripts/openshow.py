#!/usr/bin/env python3
"""
OpenShow — 将 Markdown / Word / HTML / URL 转换为单个可播放 HTML 幻灯片
"""

import argparse
import base64
import io
import json
import mimetypes
import os
import re
import sys
import textwrap
import urllib.parse
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple

from bs4 import BeautifulSoup, NavigableString, Tag

# ---------------------------------------------------------------------------
# 依赖适配
# ---------------------------------------------------------------------------
try:
    import markdown
except ImportError:
    markdown = None  # type: ignore

try:
    import requests
except ImportError:
    requests = None  # type: ignore

try:
    import docx
except ImportError:
    docx = None  # type: ignore


# ---------------------------------------------------------------------------
# 数据模型
# ---------------------------------------------------------------------------
@dataclass
class Block:
    type: str  # heading, paragraph, image, list, code, quote, other
    html: str
    level: int = 0  # for heading
    text: str = ""


@dataclass
class Slide:
    blocks: List[Block] = field(default_factory=list)
    layout: str = "text"
    idx: int = 0


# ---------------------------------------------------------------------------
# 内容提取
# ---------------------------------------------------------------------------
def _read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def _to_data_uri(src: str, base_path: Optional[str] = None) -> str:
    """将本地图片或远程图片转为 data URI，失败则返回原 src。"""
    if src.startswith("data:"):
        return src

    # 远程 URL
    if src.startswith("http://") or src.startswith("https://"):
        if requests is None:
            return src
        try:
            r = requests.get(src, timeout=15)
            r.raise_for_status()
            mime = r.headers.get("Content-Type", mimetypes.guess_type(src)[0] or "image/png")
            b64 = base64.b64encode(r.content).decode("ascii")
            return f"data:{mime};base64,{b64}"
        except Exception:
            return src

    # 本地路径
    if base_path:
        local = Path(base_path).parent / src
        if not local.exists():
            local = Path(src)
        if local.exists():
            mime = mimetypes.guess_type(str(local))[0] or "application/octet-stream"
            with open(local, "rb") as f:
                b64 = base64.b64encode(f.read()).decode("ascii")
            return f"data:{mime};base64,{b64}"
    return src


def _soup_to_blocks(soup: BeautifulSoup, base_path: Optional[str] = None) -> List[Block]:
    """将 BeautifulSoup 中的正文元素提取为 Block 列表。"""
    blocks: List[Block] = []

    # 清理导航/广告
    for tag_name in ["script", "style", "nav", "footer", "header", "aside", "noscript"]:
        for t in soup.find_all(tag_name):
            t.decompose()

    # 先把所有图片转 data-uri
    for img in soup.find_all("img"):
        src = img.get("src") or ""
        if src:
            img["src"] = _to_data_uri(src, base_path)

    # 块级元素名单
    BLOCK_TAGS = {"h1", "h2", "h3", "h4", "h5", "h6", "p", "div", "ul", "ol", "pre", "img", "blockquote", "table"}

    def _is_block_tag(node) -> bool:
        return isinstance(node, Tag) and node.name in BLOCK_TAGS

    def _walk(node):
        if isinstance(node, NavigableString):
            txt = str(node).strip()
            if txt:
                blocks.append(Block(type="paragraph", html=f"<p>{txt}</p>", text=txt))
            return
        if not isinstance(node, Tag):
            return
        name = node.name
        if name in ("h1", "h2", "h3", "h4", "h5", "h6"):
            level = int(name[1])
            text = node.get_text(strip=True)
            blocks.append(Block(type="heading", html=str(node), level=level, text=text))
        elif name == "img":
            blocks.append(Block(type="image", html=str(node)))
        elif name in ("ul", "ol"):
            text = node.get_text(strip=True)
            blocks.append(Block(type="list", html=str(node), text=text))
        elif name == "pre":
            text = node.get_text(strip=True)
            blocks.append(Block(type="code", html=str(node), text=text))
        elif name == "blockquote":
            text = node.get_text(strip=True)
            blocks.append(Block(type="quote", html=str(node), text=text))
        elif name in ("p", "div", "span", "a", "strong", "em", "b", "i"):
            # 如果内部含有块级子元素，递归处理；否则整体作为段落
            has_block_child = any(_is_block_child(c) for c in node.children)
            if has_block_child:
                for child in node.children:
                    _walk(child)
            else:
                text = node.get_text(strip=True)
                if text:
                    inner = "".join(str(c) for c in node.contents)
                    blocks.append(Block(type="paragraph", html=f"<p>{inner}</p>", text=text))
        elif name in ("section", "article", "main", "figure", "figcaption"):
            for child in node.children:
                _walk(child)
        else:
            # 其他标签若含有块级子元素，递归；否则作为 other
            has_block_child = any(_is_block_child(c) for c in node.children)
            if has_block_child:
                for child in node.children:
                    _walk(child)
            else:
                text = node.get_text(strip=True)
                if text:
                    blocks.append(Block(type="other", html=str(node), text=text))

    def _is_block_child(child) -> bool:
        return isinstance(child, Tag) and child.name in BLOCK_TAGS

    body = soup.find("body") or soup
    for child in body.children:
        _walk(child)

    # 合并相邻的同类型短段落
    merged: List[Block] = []
    for b in blocks:
        if b.type == "paragraph" and merged and merged[-1].type == "paragraph":
            merged[-1].html = f"<p>{merged[-1].text}<br><br>{b.text}</p>"
            merged[-1].text += "\n\n" + b.text
        else:
            merged.append(b)
    return merged


def _extract_main_content(soup: BeautifulSoup) -> BeautifulSoup:
    """启发式提取正文容器（最大文本密度的 div/article/main/section）。"""
    candidates = []
    for tag in soup.find_all(["article", "main", "div", "section"]):
        text_len = len(tag.get_text(strip=True))
        link_text = sum(len(a.get_text(strip=True)) for a in tag.find_all("a"))
        score = text_len - link_text * 2
        if text_len > 200:
            candidates.append((score, tag))
    if candidates:
        candidates.sort(key=lambda x: x[0], reverse=True)
        return BeautifulSoup(str(candidates[0][1]), "html.parser")
    return soup


def parse_markdown(path: str) -> List[Block]:
    if markdown is None:
        raise RuntimeError("缺少依赖: markdown。请运行 pip install markdown")
    text = _read_text(path)
    html = markdown.markdown(text, extensions=["tables", "fenced_code"])
    soup = BeautifulSoup(html, "html.parser")
    return _soup_to_blocks(soup, base_path=path)


def parse_docx(path: str) -> List[Block]:
    if docx is None:
        raise RuntimeError("缺少依赖: python-docx。请运行 pip install python-docx")
    document = docx.Document(path)
    blocks: List[Block] = []
    for para in document.paragraphs:
        text = para.text.strip()
        if not text:
            continue
        style_name = para.style.name if para.style else ""
        if style_name.startswith("Heading"):
            level = 1
            try:
                level = int(style_name.replace("Heading", "").strip())
            except ValueError:
                level = 1
            blocks.append(
                Block(type="heading", html=f"<h{level}>{text}</h{level}>", level=level, text=text)
            )
        else:
            blocks.append(Block(type="paragraph", html=f"<p>{text}</p>", text=text))

    # 尝试提取图片
    try:
        import zipfile

        docx_zip = zipfile.ZipFile(path)
        media_files = [n for n in docx_zip.namelist() if n.startswith("word/media/")]
        for mf in media_files[:5]:
            data = docx_zip.read(mf)
            mime = mimetypes.guess_type(mf)[0] or "image/png"
            b64 = base64.b64encode(data).decode("ascii")
            blocks.append(Block(type="image", html=f'<img src="data:{mime};base64,{b64}" alt="">'))
    except Exception:
        pass
    return blocks


def parse_html(path: str) -> List[Block]:
    text = _read_text(path)
    soup = BeautifulSoup(text, "html.parser")
    main = _extract_main_content(soup)
    return _soup_to_blocks(main, base_path=path)


def parse_text(path: str) -> List[Block]:
    text = _read_text(path)
    blocks: List[Block] = []
    # 简单按空行分块，每段作为一个 paragraph
    for para in text.split("\n\n"):
        para = para.strip()
        if not para:
            continue
        # 若整行是标题格式（# 开头），作为 heading
        if para.startswith("# "):
            blocks.append(Block(type="heading", html=f"<h1>{para[2:]}</h1>", level=1, text=para[2:]))
        elif para.startswith("## "):
            blocks.append(Block(type="heading", html=f"<h2>{para[3:]}</h2>", level=2, text=para[3:]))
        elif para.startswith("### "):
            blocks.append(Block(type="heading", html=f"<h3>{para[4:]}</h3>", level=3, text=para[4:]))
        else:
            blocks.append(Block(type="paragraph", html=f"<p>{para}</p>", text=para))
    return blocks


def parse_url(url: str) -> List[Block]:
    if requests is None:
        raise RuntimeError("缺少依赖: requests。请运行 pip install requests")
    headers = {"User-Agent": "Mozilla/5.0 (compatible; OpenShow/1.0)"}
    try:
        r = requests.get(url, headers=headers, timeout=20)
        r.raise_for_status()
    except Exception:
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        r = requests.get(url, headers=headers, timeout=20, verify=False)
        r.raise_for_status()
    r.encoding = r.apparent_encoding or "utf-8"
    soup = BeautifulSoup(r.text, "html.parser")
    main = _extract_main_content(soup)
    for img in main.find_all("img"):
        src = img.get("src") or ""
        if src and not src.startswith(("http://", "https://", "data:")):
            img["src"] = urllib.parse.urljoin(url, src)
    return _soup_to_blocks(main, base_path=None)


def parse_pdf(path: str) -> List[Block]:
    try:
        import fitz  # PyMuPDF
    except ImportError:
        raise RuntimeError("缺少依赖: PyMuPDF。请运行 pip install pymupdf")

    doc = fitz.open(path)
    blocks: List[Block] = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap(dpi=150)
        img_bytes = pix.tobytes("png")
        b64 = base64.b64encode(img_bytes).decode("ascii")
        blocks.append(
            Block(
                type="image",
                html=f'<img src="data:image/png;base64,{b64}" alt="Page {page_num + 1}">',
                text=f"Page {page_num + 1}",
            )
        )
    return blocks


def parse_input(src: str) -> Tuple[List[Block], str]:
    """返回 blocks 和来源标题（用于文件名）。"""
    src = src.strip()
    # 处理 file:// 前缀
    if src.startswith("file://"):
        src = src[7:]

    if src.startswith(("http://", "https://")):
        title = urllib.parse.urlparse(src).netloc.replace(".", "_")
        return parse_url(src), title

    p = Path(src)
    if not p.exists():
        raise FileNotFoundError(f"文件不存在: {src}")

    suffix = p.suffix.lower()
    title = p.stem
    if suffix in (".md", ".markdown"):
        return parse_markdown(str(p)), title
    elif suffix == ".docx":
        return parse_docx(str(p)), title
    elif suffix in (".html", ".htm"):
        return parse_html(str(p)), title
    elif suffix == ".pdf":
        return parse_pdf(str(p)), title
    elif suffix == ".txt":
        return parse_text(str(p)), title
    else:
        return parse_markdown(str(p)), title


# ---------------------------------------------------------------------------
# 分页算法
# ---------------------------------------------------------------------------
def _count_words(blocks: List[Block]) -> int:
    return sum(len(b.text) for b in blocks)


def _count_images(blocks: List[Block]) -> int:
    return sum(1 for b in blocks if b.type == "image")


def _split_long_paragraphs(blocks: List[Block], max_words: int = 300) -> List[Block]:
    """将超过 max_words 的单个 paragraph 按句子拆分。"""
    result: List[Block] = []
    for b in blocks:
        if b.type == "paragraph" and len(b.text) > max_words:
            # 按句子分割（中文句号、英文句号、换行等）
            pattern = r"(?<=[。！？.!?])\s*|\n"
            sentences = re.split(pattern, b.text)
            sentences = [s.strip() for s in sentences if s.strip()]
            chunk_text = ""
            chunk_html = ""
            for s in sentences:
                if chunk_text and len(chunk_text) + len(s) > max_words:
                    result.append(Block(type="paragraph", html=f"<p>{chunk_html}</p>", text=chunk_text))
                    chunk_text = s
                    chunk_html = s
                else:
                    if chunk_text:
                        chunk_text += "\n\n" + s
                        chunk_html += "<br><br>" + s
                    else:
                        chunk_text = s
                        chunk_html = s
            if chunk_text:
                result.append(Block(type="paragraph", html=f"<p>{chunk_html}</p>", text=chunk_text))
        else:
            result.append(b)
    return result


def _split_blocks(blocks: List[Block], max_words: int = 300, max_images: int = 3, max_items: int = 6) -> List[List[Block]]:
    """把一组长内容块按容量拆分成多页。"""
    pages: List[List[Block]] = []
    current: List[Block] = []
    cur_words = 0
    cur_images = 0
    cur_items = 0

    for b in blocks:
        w = len(b.text)
        img = 1 if b.type == "image" else 0
        if current and (cur_words + w > max_words or cur_images + img > max_images or cur_items >= max_items):
            pages.append(current)
            current = [b]
            cur_words = w
            cur_images = img
            cur_items = 1
        else:
            current.append(b)
            cur_words += w
            cur_images += img
            cur_items += 1
    if current:
        pages.append(current)
    return pages


def paginate(blocks: List[Block], title: str = "Deck") -> List[Slide]:
    """
    先按 heading 分节，再对每节做容量拆分，最后选 layout。
    """
    if not blocks:
        return []

    # 先拆分超长段落
    blocks = _split_long_paragraphs(blocks)

    # 按 heading 分 section
    sections: List[List[Block]] = []
    current_sec: List[Block] = []
    for b in blocks:
        if b.type == "heading" and b.level <= 3 and current_sec:
            sections.append(current_sec)
            current_sec = [b]
        else:
            current_sec.append(b)
    if current_sec:
        sections.append(current_sec)

    # 若第一节没有 H1 标题，补一个封面
    has_cover = False
    if sections and sections[0] and sections[0][0].type == "heading" and sections[0][0].level == 1:
        has_cover = True
    elif sections and sections[0]:
        # 在最前面插入一个封面 section
        sections.insert(0, [Block(type="heading", html=f"<h1>{title}</h1>", level=1, text=title)])
        has_cover = True

    slides: List[Slide] = []
    for sec in sections:
        pages = _split_blocks(sec)
        for page_blocks in pages:
            slides.append(Slide(blocks=page_blocks))

    # 后处理：避免标题独自占页（除非是最后一页）
    i = 0
    while i < len(slides) - 1:
        s = slides[i]
        if len(s.blocks) == 1 and s.blocks[0].type == "heading":
            if slides[i + 1].blocks:
                s.blocks.append(slides[i + 1].blocks.pop(0))
                if not slides[i + 1].blocks:
                    slides.pop(i + 1)
                    continue
        i += 1

    # 布局判定
    for idx, slide in enumerate(slides):
        page_blocks = slide.blocks
        is_first_slide = idx == 0
        is_last_slide = idx == len(slides) - 1

        headings = [b for b in page_blocks if b.type == "heading"]
        images = [b for b in page_blocks if b.type == "image"]
        lists = [b for b in page_blocks if b.type == "list"]

        if is_first_slide and headings and headings[0].level == 1:
            slide.layout = "cover"
        elif is_last_slide and len(slides) > 2:
            slide.layout = "closing"
        elif images and len([b for b in page_blocks if b.type in ("paragraph", "list", "code")]) > 0:
            slide.layout = "split"
        elif lists and not images:
            slide.layout = "list"
        elif len(page_blocks) == 1 and page_blocks[0].type == "image":
            slide.layout = "image"
        else:
            slide.layout = "text"

    if not slides:
        slides.append(Slide(blocks=[Block(type="paragraph", html="<p>无内容</p>", text="无内容")], layout="text"))

    for i, s in enumerate(slides):
        s.idx = i
    return slides


# ---------------------------------------------------------------------------
# HTML 模板与渲染
# ---------------------------------------------------------------------------
CSS = """
:root {
  --bg: #0f0f0f;
  --fg: #f0f0f0;
  --muted: #a0a0a0;
  --accent: #3b82f6;
  --font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  --mono: "SF Mono", "Fira Code", Consolas, "Courier New", monospace;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body {
  width: 100%; height: 100%;
  overflow: hidden;
  background: var(--bg);
  color: var(--fg);
  font-family: var(--font-family);
  font-size: clamp(16px, 1.6vw, 28px);
  line-height: 1.6;
  touch-action: none;
  -webkit-font-smoothing: antialiased;
}
#deck {
  position: relative;
  width: 100%; height: 100%;
}
.slide {
  position: absolute;
  inset: 0;
  width: 100%; height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 6vh 8vw;
  opacity: 0;
  pointer-events: none;
  transform: translateX(100%);
  transition: transform 0.5s cubic-bezier(0.22, 1, 0.36, 1), opacity 0.5s ease;
  overflow: hidden;
  will-change: transform, opacity;
  backface-visibility: hidden;
}
.slide.active {
  opacity: 1;
  pointer-events: auto;
  transform: translateX(0);
}
.slide.prev {
  opacity: 0;
  transform: translateX(-100%);
}
.slide-inner {
  width: 100%;
  max-width: 1400px;
  display: flex;
  flex-direction: column;
  gap: 1.2em;
}
h1, h2, h3, h4, h5, h6 {
  line-height: 1.25;
  font-weight: 700;
}
h1 { font-size: clamp(2rem, 5vw, 4rem); }
h2 { font-size: clamp(1.5rem, 3.5vw, 2.8rem); }
h3 { font-size: clamp(1.2rem, 2.5vw, 2rem); }
p { opacity: 0.95; max-width: 70ch; }
ul, ol { padding-left: 1.5em; }
li { margin: 0.4em 0; }
a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }
img {
  max-width: 100%;
  max-height: 60vh;
  object-fit: contain;
  border-radius: 8px;
  box-shadow: 0 10px 40px rgba(0,0,0,0.35);
}
pre, code {
  font-family: var(--mono);
  background: rgba(255,255,255,0.06);
  border-radius: 6px;
}
pre {
  padding: 1em;
  overflow: auto;
  max-height: 55vh;
  font-size: 0.85em;
}

.watermark {
  position: absolute;
  bottom: 3.5vh;
  right: 3vw;
  width: clamp(48px, 6vw, 84px);
  height: clamp(48px, 6vw, 84px);
  color: rgba(255,255,255,0.04);
  pointer-events: none;
  z-index: 1;
  transition: color 0.5s ease;
}
.slide.active .watermark {
  color: rgba(255,255,255,0.07);
}
blockquote {
  border-left: 4px solid var(--accent);
  padding-left: 1em;
  color: var(--muted);
  font-style: italic;
}

/* layouts */
[data-layout="cover"] .slide-inner {
  align-items: center;
  text-align: center;
  gap: 0.8em;
}
[data-layout="cover"] h1 {
  font-size: clamp(2.4rem, 6vw, 5rem);
  letter-spacing: -0.02em;
}
[data-layout="cover"] .subtitle {
  color: var(--muted);
  font-size: clamp(1rem, 2vw, 1.6rem);
}
[data-layout="closing"] .slide-inner {
  align-items: center;
  text-align: center;
}
[data-layout="split"] .slide-inner {
  display: grid;
  grid-template-columns: 1fr 1fr;
  align-items: center;
  gap: 3vw;
}
[data-layout="split"].img-top .slide-inner {
  grid-template-columns: 1fr;
  grid-template-rows: auto 1fr;
  text-align: center;
}
[data-layout="list"] .slide-inner {
  align-items: flex-start;
  text-align: left;
}
[data-layout="list"] ul, [data-layout="list"] ol {
  font-size: clamp(1.1rem, 2.2vw, 1.8rem);
}
[data-layout="image"] .slide-inner {
  align-items: center;
  justify-content: center;
}
[data-layout="image"] img {
  max-height: 72vh;
}
[data-layout="text"] .slide-inner {
  align-items: flex-start;
  text-align: left;
}

/* timer */
#timer {
  position: fixed;
  top: 18px;
  left: 22px;
  z-index: 999;
  font-variant-numeric: tabular-nums;
  font-size: 0.85rem;
  color: var(--muted);
  background: rgba(0,0,0,0.4);
  padding: 6px 12px;
  border-radius: 999px;
  backdrop-filter: blur(4px);
  cursor: pointer;
  user-select: none;
  transition: opacity 0.3s;
}
#timer.hidden { opacity: 0; pointer-events: none; }
#timer.paused { color: #f59e0b; }

/* progress */
#progress {
  position: fixed;
  bottom: 18px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  align-items: center;
  gap: 10px;
  z-index: 999;
  padding: 6px 14px;
  background: rgba(0,0,0,0.4);
  border-radius: 999px;
  backdrop-filter: blur(4px);
}
.dot {
  width: 8px; height: 8px;
  border-radius: 50%;
  background: rgba(255,255,255,0.25);
  transition: background 0.3s;
}
.dot.active { background: var(--accent); }
#page-num {
  position: fixed;
  bottom: 18px;
  right: 22px;
  font-size: 0.75rem;
  color: var(--muted);
  z-index: 999;
}

/* touch hints / click zones */
.zone {
  position: fixed;
  top: 0; bottom: 0;
  width: 20%;
  z-index: 99;
  cursor: pointer;
}
.zone:hover { background: rgba(255,255,255,0.02); }
.zone-left { left: 0; }
.zone-right { right: 0; width: 80%; }

/* mobile */
@media (max-width: 768px) {
  .slide { padding: 5vh 6vw; }
  [data-layout="split"] .slide-inner { grid-template-columns: 1fr; text-align: center; }
  img { max-height: 40vh; }
  #timer { font-size: 0.75rem; top: 10px; left: 10px; }
}
""".strip()


JS = """
(function(){
  const slides = Array.from(document.querySelectorAll('.slide'));
  let idx = 0;

  function update(){
    slides.forEach((s,i)=>{
      s.classList.remove('active','prev');
      if(i===idx){ s.classList.add('active'); }
      else if(i<idx){ s.classList.add('prev'); }
    });
    document.querySelectorAll('.dot').forEach((d,i)=>{
      d.classList.toggle('active', i===idx);
    });
    document.getElementById('page-text').textContent = (idx+1) + ' / ' + slides.length;
  }

  function next(){ if(idx < slides.length-1){ idx++; update(); } }
  function prev(){ if(idx > 0){ idx--; update(); } }

  // keyboard
  document.addEventListener('keydown', e=>{
    if(e.key==='ArrowRight' || e.key==='ArrowDown' || e.key===' ' || e.key==='PageDown'){
      e.preventDefault();
      next();
    } else if(e.key==='ArrowLeft' || e.key==='ArrowUp' || e.key==='PageUp'){
      e.preventDefault();
      prev();
    } else if(e.key==='f' || e.key==='F'){
      e.preventDefault();
      if(!document.fullscreenElement) document.documentElement.requestFullscreen().catch(()=>{});
      else document.exitFullscreen().catch(()=>{});
    } else if(e.key==='t' || e.key==='T'){
      e.preventDefault();
      document.getElementById('timer').classList.toggle('hidden');
    }
  });

  // click zones
  document.querySelector('.zone-left').addEventListener('click', prev);
  document.querySelector('.zone-right').addEventListener('click', next);

  // touch swipe
  let startX = 0;
  document.addEventListener('touchstart', e=>{
    startX = e.touches[0].clientX;
  }, {passive: true});
  document.addEventListener('touchend', e=>{
    const endX = e.changedTouches[0].clientX;
    const diff = startX - endX;
    if(Math.abs(diff) > 40){ diff > 0 ? next() : prev(); }
  }, {passive: true});

  // prevent link jumps in deck mode
  document.body.addEventListener('click', e=>{
    const a = e.target.closest('a');
    if(a){
      const href = a.getAttribute('href') || '';
      if(!href.startsWith('#')){
        e.preventDefault();
      }
    }
  });

  // timer
  const timerEl = document.getElementById('timer');
  let seconds = 0, paused = false, timerStarted = false;
  function fmt(n){ return n.toString().padStart(2,'0'); }
  function updateTimer(){
    const m = Math.floor(seconds/60), s = seconds%60;
    timerEl.textContent = fmt(m) + ':' + fmt(s);
  }
  setInterval(()=>{
    if(!paused && timerStarted){
      seconds++;
      updateTimer();
    }
  }, 1000);
  timerEl.addEventListener('click', ()=>{
    paused = !paused;
    timerEl.classList.toggle('paused', paused);
  });
  // start timer on first interaction or after 1s
  setTimeout(()=>{ timerStarted = true; }, 1000);

  update();
})();
""".strip()


def _render_slide_content(slide: Slide) -> str:
    """把 Slide 的 blocks 渲染成 HTML，同时做 layout 微调。"""
    if slide.layout == "cover":
        parts = []
        for b in slide.blocks:
            if b.type == "heading" and b.level == 1:
                parts.append(f'<h1>{b.text}</h1>')
            elif b.type == "heading":
                parts.append(f'<div class="subtitle">{b.text}</div>')
            else:
                parts.append(b.html)
        return "\n".join(parts)

    if slide.layout == "split":
        images = [b.html for b in slide.blocks if b.type == "image"]
        texts = [b.html for b in slide.blocks if b.type != "image"]
        if len(images) == 1:
            return f"""<div>{"".join(images)}</div>
<div>{"".join(texts)}</div>"""
        else:
            slide.layout = "split img-top"
            return f"""<div>{"".join(images)}</div>
<div>{"".join(texts)}</div>"""

    if slide.layout == "image":
        return "\n".join(b.html for b in slide.blocks)

    if slide.layout == "list":
        heading = ""
        body = []
        for b in slide.blocks:
            if b.type == "heading":
                heading = b.html
            else:
                body.append(b.html)
        return f"{heading}\n<div>{''.join(body)}</div>"

    # text / closing / default
    return "\n".join(b.html for b in slide.blocks)


def build_html(slides: List[Slide], title: str = "OpenShow", logo_svg: str = "") -> str:
    dots = "\n".join(f'<div class="dot{" active" if i == 0 else ""}"></div>' for i in range(len(slides)))
    slide_html = "\n".join(
        f'<section class="slide" data-layout="{s.layout}"><div class="watermark">{logo_svg}</div><div class="slide-inner">{_render_slide_content(s)}</div></section>'
        for s in slides
    )

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
{CSS}
</style>
</head>
<body>
<div id="deck">
{slide_html}
</div>
<div class="zone zone-left"></div>
<div class="zone zone-right"></div>
<div id="timer">00:00</div>
<div id="progress">
{dots}
</div>
<div id="page-num"><span id="page-text">1 / {len(slides)}</span></div>
<script>
{JS}
</script>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="OpenShow — 将文档/网页转为可播放 HTML 幻灯片")
    parser.add_argument("-i", "--input", required=True, help="输入文件路径或 URL")
    parser.add_argument("-o", "--output", default=".", help="输出目录（默认当前目录）")
    parser.add_argument("--open", action="store_true", help="生成后用系统默认浏览器自动打开")
    parser.add_argument("--openclaw", action="store_true", help="生成后用 openclaw browser 打开")
    args = parser.parse_args()

    blocks, title = parse_input(args.input)
    slides = paginate(blocks, title=title)

    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"openshow_{title}_{ts}.html"
    out_path = out_dir / filename

    logo_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="60" cy="60" r="54" opacity="0.25"/>
  <circle cx="60" cy="60" r="36" opacity="0.18"/>
  <polygon points="48,45 48,75 81,60" fill="currentColor" stroke="none" opacity="0.35"/>
</svg>"""
    html = build_html(slides, title=title, logo_svg=logo_svg)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"生成完成：{out_path.resolve()}")
    print(f"共 {len(slides)} 页幻灯片")

    file_url = f"file://{out_path.resolve()}"
    if args.openclaw:
        import subprocess
        try:
            subprocess.run(["openclaw", "browser", "open", file_url], check=False)
            print(f"已通过 openclaw 打开：{file_url}")
        except Exception as e:
            print(f"openclaw 打开失败：{e}")
    elif args.open:
        import webbrowser
        try:
            webbrowser.open(file_url)
            print(f"已用系统默认浏览器打开：{file_url}")
        except Exception as e:
            print(f"浏览器打开失败：{e}")


if __name__ == "__main__":
    main()