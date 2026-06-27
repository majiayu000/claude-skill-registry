# web-media-getter

*web-media-getter is a Claude Code skill that runs one query across free image/video/GIF APIs and returns a single license-tagged list of results.*

![License: MIT](https://img.shields.io/badge/license-MIT-blue) ![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-3776ab) ![Zero deps](https://img.shields.io/badge/deps-stdlib%20only-46d39a) ![Media: images · video · gifs](https://img.shields.io/badge/media-📷%20images%20·%20🎬%20video%20·%20🎞️%20gifs-111)

Search a pile of free media APIs with **one query** and get back a single,
license-tagged list of images, videos, and GIFs — optionally downloaded with
their attribution. It's one Python file, no dependencies to install, and it runs
anywhere `python3` does.

![web-media-getter: one apollo-moon-landing query returning results badged by source — internet archive, openverse, wikimedia, loc, nasa](docs/example-output.png)

*One query → five free sources fanned out at once, each result badged by source and license.*

## 🤔 Why

When you need a *real* photo or a piece of archival footage — a hero image, a
texture, 1930s factory film, a reaction GIF — you usually end up tab-hopping
across NASA, Wikimedia, the Internet Archive, and a couple of stock sites, each
with its own search box and its own licensing fine print. This collapses all of
that into one command and hands the licensing back to you with every result.

## 📦 Install

You only need Python 3.8+ (already on most Macs and Linux machines). Grab the
single script:

```bash
curl -O https://raw.githubusercontent.com/connerkward/web-media-getter-skill/main/webmedia.py
python3 webmedia.py "your query"
```

That's the whole install — no `pip install`, no virtualenv, nothing to keep
updated.

### 🪟 On Windows

The script is pure standard library, so it runs on Windows too — you just need
Python, which isn't preinstalled there. Easiest path (PowerShell):

```powershell
winget install Python.Python.3      # one time, if you don't have Python
curl.exe -O https://raw.githubusercontent.com/connerkward/web-media-getter-skill/main/webmedia.py
python webmedia.py "your query"
```

Two Windows gotchas: the command is `python` (not `python3`), and use `curl.exe`
explicitly so PowerShell doesn't intercept `curl` as an alias. Everything else —
sources, downloads, attribution — works identically.

> 🤖 Using this with Claude Code or another AI agent? Install it as a skill and
> let the agent drive it — see **[docs/agents.md](docs/agents.md)**.

## 🚀 Use it

```
webmedia.py QUERY [--type image|video|gif] [--count N] [--source LIST|all|nokey]
                  [--download] [--out DIR]
```

```bash
# Images across every free source
python3 webmedia.py "apollo moon landing" --source all --count 8

# Historical footage from the Internet Archive
python3 webmedia.py "car factory 1930s" --type video --source internetarchive --count 5

# Reaction GIFs (needs a KLIPY or GIPHY key — see Sources)
python3 webmedia.py "thumbs up" --type gif --count 6

# Download the results and write attribution alongside them
python3 webmedia.py "saturn v" --source nasa --download --out ./downloads
```

- `--source` defaults to `all`; use `nokey` for the keyless sources only, or a
  comma list like `wikimedia,pexels`.
- `--download` saves each file into `--out` and drops an `attribution.json` next
  to them, so where each file came from travels with it.

## Three media types, one interface

| Type | Flag | Sources |
|---|---|---|
| 📷 **Images** | `--type image` (default) | openverse · wikimedia · internet archive · loc · nasa · pexels · pixabay |
| 🎬 **Videos** | `--type video` | internet archive · nasa · pexels · pixabay |
| 🎞️ **GIFs** | `--type gif` | klipy · giphy |

## 🗂️ Sources

The five no-key sources work the moment you run the script. The rest take a free
API key — set the matching environment variable and they switch on automatically.

| Source | Type | Free key needed | Get one | Env var |
|---|---|---|---|---|
| [Openverse](https://openverse.org) | images | — | — | — |
| [Internet Archive](https://archive.org) | images, video | — | — | — |
| [NASA Image Library](https://images.nasa.gov) | images, video | — | — | — |
| [Wikimedia Commons](https://commons.wikimedia.org) | images | — | — | — |
| [Library of Congress](https://www.loc.gov/photos/) | images | — | — | — |
| [Pexels](https://www.pexels.com) | images, video | ✓ | [pexels.com/api](https://www.pexels.com/api/) | `PEXELS_API_KEY` |
| [Pixabay](https://pixabay.com) | images, video | ✓ | [pixabay.com/api/docs](https://pixabay.com/api/docs/) | `PIXABAY_API_KEY` |
| [KLIPY](https://klipy.com) | GIFs | ✓ | [klipy.com/developers](https://klipy.com/developers) | `KLIPY_API_KEY` |
| [GIPHY](https://giphy.com) | GIFs | ✓ | [developers.giphy.com](https://developers.giphy.com/) | `GIPHY_API_KEY` |

## ⚖️ Attribution & licensing

The tool reports a license for every result, but **you check the terms before you
use anything.** A quick guide to what comes back:

- **NASA** — generally public domain.
- **Wikimedia / Openverse** — per-item CC or public-domain licenses; CC-BY and
  CC-BY-SA require credit.
- **Internet Archive / Library of Congress** — varies per item ("see item").
- **Pexels / Pixabay** — their own free licenses.
- **GIF platforms** — expect platform attribution in anything you ship.

`--download` always writes `attribution.json` so the provenance is recorded
whether or not you read it at the time.

## License

[MIT](LICENSE) © Conner K Ward. The tool is MIT; fetched media is licensed by its
source — see above.

---

🧭 **[ckw-skills](https://github.com/connerkward/ckw-skills)** — part of Conner K. Ward's collection of Claude Code skills & MCP servers.
