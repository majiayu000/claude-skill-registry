<div align="center">

<!-- Animated Hero Banner -->
<h1>
  <img src="https://raw.githubusercontent.com/lumacoder/open-show/main/assets/logo.svg" width="80" alt="OpenShow Logo">
  <br>
  OpenShow
</h1>

<p align="center">
  <strong>Turn any document into a cinematic HTML slideshow</strong>
  <br>
  <em>Markdown · Word · PDF · Text · HTML · URLs → Single-file playable deck</em>
</p>

<p align="center">
  <a href="https://github.com/lumacoder/open-show/stargazers"><img src="https://img.shields.io/github/stars/lumacoder/open-show?style=for-the-badge&logo=github&color=ffd700&labelColor=1a1a1a" alt="Stars"></a>
  <a href="https://github.com/lumacoder/open-show/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-00d26a?style=for-the-badge&labelColor=1a1a1a" alt="License"></a>
  <a href="#"><img src="https://img.shields.io/badge/Python-3.9%2B-3776ab?style=for-the-badge&logo=python&labelColor=1a1a1a" alt="Python"></a>
  <a href="#"><img src="https://img.shields.io/badge/Zero%20CDN-Offline%20Ready-ff6b6b?style=for-the-badge&labelColor=1a1a1a" alt="Zero CDN"></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/%E2%86%90_%E2%86%92-Keyboard_Navigation-3b82f6?style=flat-square&labelColor=1a1a1a">
  <img src="https://img.shields.io/badge/F-Fullscreen-f59e0b?style=flat-square&labelColor=1a1a1a">
  <img src="https://img.shields.io/badge/T-Timer-10b981?style=flat-square&labelColor=1a1a1a">
  <img src="https://img.shields.io/badge/%E2%86%94%EF%B8%8E-Touch_Swipe-ec4899?style=flat-square&labelColor=1a1a1a">
</p>

<br>

<!-- Cinematic Preview Placeholder - replace with actual GIF when available -->
<p align="center">
  <img src="https://user-images.githubusercontent.com/placeholder/openshow-demo.gif" alt="OpenShow Demo" width="720">
</p>

<p align="center">
  <a href="#-quick-start"><strong>⚡ Quick Start</strong></a> ·
  <a href="#-features"><strong>✨ Features</strong></a> ·
  <a href="#-supported-formats"><strong>📁 Formats</strong></a> ·
  <a href="#-installation"><strong>🔧 Install</strong></a> ·
  <a href="#-command-line"><strong>⌨️ CLI</strong></a> ·
  <a href="#-architecture"><strong>🏗️ Architecture</strong></a>
</p>

</div>

---

## ⚡ Quick Start

```bash
# Clone & setup
git clone https://github.com/lumacoder/open-show.git
cd open-show
python3 -m pip install markdown python-docx requests beautifulsoup4 pymupdf

# Convert a URL to slideshow
python3 scripts/openshow.py -i "https://example.com" -o ~/openshow_outputs --open

# Convert a PDF to slideshow
python3 scripts/openshow.py -i "presentation.pdf" -o ~/openshow_outputs --open
```

> 💡 **Pro tip**: Add `--openclaw` instead of `--open` to launch directly in OpenClaw browser.

---

## ✨ Features

<div align="center">

| 🎬 **Cinematic Experience** | 📱 **Any Screen** | 🔒 **Fully Offline** |
|:---|:---|:---|
| Smooth `cubic-bezier` slide transitions with hardware acceleration | Responsive from mobile to projector. Touch, keyboard, click-zone navigation | Zero external CDN. All CSS, JS, and images inlined into a single HTML file |

</div>

### What makes OpenShow different

- **🧠 Smart Pagination** — Content-aware splitting by headings, word count, image density, and block count. No wall-of-text slides.
- **🎨 Auto Layout Engine** — Dynamically selects `cover`, `text`, `list`, `split`, `image`, or `closing` layouts per slide.
- **⏱️ Built-in Timer** — Auto-starting presentation timer with pause/resume. Press `T` to toggle.
- **🖼️ Image Inlining** — Remote and local images are automatically converted to `data URI` for true offline portability.
- **🚀 One-Command Open** — Generate and immediately launch with `--open` (system browser) or `--openclaw` (OpenClaw).

---

## 📁 Supported Formats

<div align="center">

| Format | Extension | Parser | Dependency |
|:---:|:---:|:---|:---|
| **Markdown** | `.md`, `.markdown` | Full markdown + tables + fenced code | `markdown` |
| **Microsoft Word** | `.docx` | Paragraphs, headings, embedded images | `python-docx` |
| **PDF** | `.pdf` | Per-page rasterization to PNG | `pymupdf` |
| **Plain Text** | `.txt` | Paragraph blocks + `#` heading detection | None |
| **HTML** | `.html`, `.htm` | Heuristic main-content extraction | `beautifulsoup4` |
| **Web URL** | `http://`, `https://` | Fetch + clean + extract body | `requests`, `beautifulsoup4` |

</div>

---

## 🔧 Installation

### Prerequisites

```bash
python3 --version  # >= 3.9
```

### Install dependencies

```bash
python3 -m pip install markdown python-docx requests beautifulsoup4 pymupdf
```

### Optional: OpenClaw integration

If you have [OpenClaw](https://openclaw.ai) installed, use `--openclaw` for instant browser launch.

---

## ⌨️ Command Line

```
usage: openshow.py [-h] -i INPUT [-o OUTPUT] [--open] [--openclaw]

OpenShow — 将文档/网页转为可播放 HTML 幻灯片

options:
  -h, --help           show this help message and exit
  -i, --input INPUT    输入文件路径或 URL
  -o, --output OUTPUT  输出目录（默认当前目录）
  --open               生成后用系统默认浏览器自动打开
  --openclaw           生成后用 openclaw browser 打开
```

### Common recipes

```bash
# Markdown article → deck
python3 scripts/openshow.py -i article.md -o ~/openshow_outputs --open

# Word report → deck
python3 scripts/openshow.py -i report.docx -o ~/openshow_outputs --open

# PDF slides → HTML deck
python3 scripts/openshow.py -i deck.pdf -o ~/openshow_outputs --open

# Plain text notes → deck
python3 scripts/openshow.py -i notes.txt -o ~/openshow_outputs --open

# Web article → deck
python3 scripts/openshow.py -i "https://blog.example.com/post" -o ~/openshow_outputs --openclaw
```

---

## 🎮 Controls

<div align="center">

| Action | Desktop | Mobile |
|:---|:---|:---|
| Next slide | `→` `↓` `Space` `PageDown` | Swipe left · Tap right 2/3 |
| Previous slide | `←` `↑` `PageUp` | Swipe right · Tap left 1/3 |
| Toggle fullscreen | `F` | Rotate device |
| Toggle timer | `T` | — |
| Pause timer | Click top-left timer | — |

</div>

---

## 🏗️ Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────────┐     ┌─────────────┐
│   INPUT     │────▶│   PARSER    │────▶│  BLOCK PIPELINE │────▶│  PAGINATE   │
│ (md/pdf/..) │     │(format spec)│     │(clean · inline) │     │(smart split)│
└─────────────┘     └─────────────┘     └─────────────────┘     └──────┬──────┘
                                                                        │
                                                                        ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────────┐     ┌─────────────┐
│  SINGLE     │◀────│   RENDER    │◀────│  LAYOUT ENGINE  │◀────│   SLIDES    │
│  HTML FILE  │     │(css+js inline)│    │(auto layout pick)│    │(page list)  │
└─────────────┘     └─────────────┘     └─────────────────┘     └─────────────┘
```

### Design principles

1. **Single file output** — One `.html` file contains everything. Email it, host it on a static bucket, or open it from your Downloads folder.
2. **Content-first pagination** — We split by semantic headings first, then by capacity constraints (words, images, blocks).
3. **Layout polymorphism** — The engine picks the best layout for each slide based on its content fingerprint.
4. **Zero config** — No YAML frontmatter, no template selection, no manual tweaking. Pass a file, get a deck.

---

## 📸 Gallery

<div align="center">
  <table>
    <tr>
      <td align="center"><b>Cover Layout</b></td>
      <td align="center"><b>Split Layout</b></td>
      <td align="center"><b>List Layout</b></td>
    </tr>
    <tr>
      <td><img src="https://via.placeholder.com/300x200/1a1a1a/3b82f6?text=Cover" alt="Cover"></td>
      <td><img src="https://via.placeholder.com/300x200/1a1a1a/f59e0b?text=Split" alt="Split"></td>
      <td><img src="https://via.placeholder.com/300x200/1a1a1a/10b981?text=List" alt="List"></td>
    </tr>
  </table>
</div>

> 🎨 *Replace placeholder images with real screenshots once you generate your first decks.*

---

## 🛣️ Roadmap

- [x] Markdown support
- [x] Word (.docx) support
- [x] PDF support
- [x] Plain text support
- [x] HTML & URL support
- [x] OpenClaw browser integration
- [ ] PPTX support (stretch goal)
- [ ] Custom theme / skin injection
- [ ] Speaker notes mode
- [ ] Export to video (MP4/WebM)

---

## 🤝 Contributing

PRs are welcome! Areas we'd love help with:

- Better PDF text extraction (OCR for scanned pages)
- Additional layout templates
- Theme / CSS customization system
- Performance optimization for giant documents

---

## 📜 License

MIT © [lumacoder](https://github.com/lumacoder)

---

<div align="center">

⭐ **Star this repo if OpenShow saved you from making slides by hand!**

</div>
