#!/usr/bin/env python3
"""free-stock-media-search — query FREE image/video/GIF APIs, return one normalized list.

Zero deps (stdlib only). No-key sources work out of the box; key-gated sources
(Pexels, Pixabay, GIPHY, KLIPY) activate only if their env var is set. Output is
a normalized record list, easy to rank or filter across sources.

Each record: source, title, url (human page/asset), thumb, dl (direct downloadable
media URL or None), page_url, author, license, w, h, type.

Usage:
  webmedia.py "1950s street scene" --type image --count 8 --json
  webmedia.py "rocket launch" --type video --source nasa,internetarchive
  webmedia.py "car factory 1930s" --source nokey --download --out ./downloads
"""
import argparse, json, os, re, sys, urllib.parse, urllib.request, concurrent.futures as cf

UA = {"User-Agent": "free-stock-media-search/1.0 (+https://github.com/connerkward/free-stock-media-search)"}
TIMEOUT = 12

def _get(url, headers=None):
    req = urllib.request.Request(url, headers={**UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return json.load(r)

def rec(**k):
    k.setdefault("type","image"); k.setdefault("license",""); k.setdefault("author","")
    k.setdefault("w",None); k.setdefault("h",None); k.setdefault("dl",None)
    return k

# ---- no-key adapters ----------------------------------------------------
def openverse(q, typ, n):
    if typ=="video": return []
    d=_get(f"https://api.openverse.org/v1/images/?q={urllib.parse.quote(q)}&page_size={n}")
    return [rec(source="openverse", title=it.get("title",""), url=it.get("url"), dl=it.get("url"),
        thumb=it.get("thumbnail") or it.get("url"), page_url=it.get("foreign_landing_url"),
        author=it.get("creator",""), license=f"{it.get('license','')} {it.get('license_version','')}".strip(),
        w=it.get("width"), h=it.get("height"), type="image") for it in d.get("results",[])]

def internetarchive(q, typ, n):
    mt = "movies" if typ=="video" else "image"
    qq = urllib.parse.quote(f'({q}) AND mediatype:({mt})')
    d=_get(f"https://archive.org/advancedsearch.php?q={qq}&rows={n}&output=json"
           "&fl[]=identifier&fl[]=title&fl[]=year&fl[]=creator&sort[]=downloads+desc")
    out=[]
    for doc in d.get("response",{}).get("docs",[]):
        ident=doc.get("identifier")
        out.append(rec(source="internetarchive", title=doc.get("title",""),
            url=f"https://archive.org/details/{ident}",
            thumb=f"https://archive.org/services/img/{ident}",
            # real image/video file resolved lazily from item metadata on --download
            # (services/img is just the item icon — not the content). See _ia_*_file.
            dl=None,
            page_url=f"https://archive.org/details/{ident}", ident=ident,
            author=(doc.get("creator") if isinstance(doc.get("creator"),str) else ""),
            license="see item", type=("video" if typ=="video" else "image")))
    return out

def _ia_video_file(ident):
    """Resolve an Internet Archive item to a single playable mp4 derivative."""
    try:
        m=_get(f"https://archive.org/metadata/{ident}")
        files=m.get("files",[])
        mp4=[f for f in files if (f.get("name","").lower().endswith(".mp4"))]
        mp4.sort(key=lambda f: float(f.get("size",0) or 0))  # smallest derivative = a clip-ish file
        if mp4:
            return f"https://archive.org/download/{ident}/{urllib.parse.quote(mp4[0]['name'])}"
    except Exception:
        pass
    return None

def _ia_image_file(ident):
    """Resolve an Internet Archive item to a real content image (not the item icon)."""
    try:
        m=_get(f"https://archive.org/metadata/{ident}")
        imgs=[f for f in m.get("files",[])
              if f.get("name","").lower().endswith((".jpg",".jpeg",".png"))
              and "thumb" not in f.get("name","").lower()
              and f.get("source")!="thumbnail"]
        if imgs:
            CAP=15_000_000  # avoid 100MB+ archival scans; prefer largest under the cap
            sz=lambda f: float(f.get("size",0) or 0)
            under=[f for f in imgs if sz(f)<=CAP]
            pick=max(under,key=sz) if under else min(imgs,key=sz)
            return f"https://archive.org/download/{ident}/{urllib.parse.quote(pick['name'])}"
    except Exception:
        pass
    return None

def nasa(q, typ, n):
    mt = "video" if typ=="video" else "image"
    d=_get(f"https://images-api.nasa.gov/search?q={urllib.parse.quote(q)}&media_type={mt}")
    out=[]
    for it in d.get("collection",{}).get("items",[])[:n]:
        data=(it.get("data") or [{}])[0]; links=it.get("links") or [{}]
        out.append(rec(source="nasa", title=data.get("title",""), url=it.get("href"),
            thumb=links[0].get("href"), dl=(links[0].get("href") if mt=="image" else None),
            page_url=f"https://images.nasa.gov/details/{data.get('nasa_id','')}",
            author=data.get("photographer") or data.get("center",""),
            license="public domain (NASA)", type=mt))
    return out

def wikimedia(q, typ, n):
    if typ=="video": return []
    qq=urllib.parse.quote(q)
    url=("https://commons.wikimedia.org/w/api.php?action=query&generator=search"
         f"&gsrsearch={qq}&gsrnamespace=6&gsrlimit={n*2}&prop=imageinfo"
         "&iiprop=url|size|mediatype|extmetadata&iiurlwidth=800&format=json")
    d=_get(url); out=[]
    for p in (d.get("query",{}).get("pages",{}) or {}).values():
        ii=(p.get("imageinfo") or [{}])[0]; em=ii.get("extmetadata",{}) or {}
        # skip PDFs/DjVu/office docs (magazines, newspapers, books) — photos only
        if ii.get("mediatype") not in ("BITMAP","DRAWING"): continue
        if len(out)>=n: break
        out.append(rec(source="wikimedia", title=p.get("title","").replace("File:",""),
            # prefer the jpg rendition for dl — originals can be .tif/.svg the browser can't show
            url=ii.get("url"), dl=ii.get("thumburl") or ii.get("url"), thumb=ii.get("thumburl") or ii.get("url"),
            page_url=ii.get("descriptionurl"),
            author=re.sub("<[^>]+>","",(em.get("Artist",{}) or {}).get("value",""))[:120],
            license=(em.get("LicenseShortName",{}) or {}).get("value",""),
            w=ii.get("width"), h=ii.get("height"), type="image"))
    return out

def loc(q, typ, n):
    if typ=="video": return []
    d=_get(f"https://www.loc.gov/photos/?q={urllib.parse.quote(q)}&fo=json&c={n}")
    out=[]
    for it in (d.get("results") or [])[:n]:
        imgs=[u for u in (it.get("image_url") or []) if re.search(r"\.(jpg|jpeg|png)", u)]
        if not imgs: continue
        out.append(rec(source="loc", title=(it.get("title") or "")[:120],
            url=imgs[-1], dl=imgs[-1], thumb=imgs[0], page_url=it.get("id") or it.get("url"),
            license="see item (LoC)", type="image"))
    return out

# ---- key-gated adapters (free keys) -------------------------------------
def pexels(q, typ, n):
    key=os.environ.get("PEXELS_API_KEY")
    if not key: return []
    if typ=="video":
        d=_get(f"https://api.pexels.com/videos/search?query={urllib.parse.quote(q)}&per_page={n}",
               headers={"Authorization":key}); out=[]
        for v in d.get("videos",[]):
            files=sorted(v.get("video_files",[]), key=lambda f:(f.get("width") or 0))
            mid=files[len(files)//2] if files else {}
            out.append(rec(source="pexels", title=(v.get("user") or {}).get("name",""),
                url=v.get("url"), dl=mid.get("link"), thumb=v.get("image"), page_url=v.get("url"),
                author=(v.get("user") or {}).get("name",""), license="Pexels (free)",
                w=v.get("width"), h=v.get("height"), type="video"))
        return out
    d=_get(f"https://api.pexels.com/v1/search?query={urllib.parse.quote(q)}&per_page={n}",
           headers={"Authorization":key})
    return [rec(source="pexels", title=p.get("alt",""), url=(p.get("src") or {}).get("large2x"),
        dl=(p.get("src") or {}).get("large2x"), thumb=(p.get("src") or {}).get("medium"),
        page_url=p.get("url"), author=p.get("photographer",""), license="Pexels (free)",
        w=p.get("width"), h=p.get("height"), type="image") for p in d.get("photos",[])]

def pixabay(q, typ, n):
    key=os.environ.get("PIXABAY_API_KEY")
    if not key: return []
    base="https://pixabay.com/api/videos/" if typ=="video" else "https://pixabay.com/api/"
    d=_get(f"{base}?key={key}&q={urllib.parse.quote(q)}&per_page={max(3,n)}"); out=[]
    for h in d.get("hits",[])[:n]:
        if typ=="video":
            v=(h.get("videos") or {}).get("medium",{})
            out.append(rec(source="pixabay", title=h.get("tags",""), url=v.get("url"), dl=v.get("url"),
                thumb=f"https://i.vimeocdn.com/video/{h.get('picture_id','')}_295x166.jpg",
                page_url=h.get("pageURL"), author=h.get("user",""), license="Pixabay (free)", type="video"))
        else:
            out.append(rec(source="pixabay", title=h.get("tags",""), url=h.get("largeImageURL"),
                dl=h.get("largeImageURL"), thumb=h.get("previewURL"), page_url=h.get("pageURL"),
                author=h.get("user",""), license="Pixabay (free)",
                w=h.get("imageWidth"), h=h.get("imageHeight"), type="image"))
    return out

# ---- GIF adapters (free keys; only fire for --type gif) -----------------
def giphy(q, typ, n):
    key=os.environ.get("GIPHY_API_KEY")
    if not key or typ!="gif": return []
    d=_get(f"https://api.giphy.com/v1/gifs/search?api_key={key}&q={urllib.parse.quote(q)}&limit={n}&rating=pg-13")
    out=[]
    for g in d.get("data",[]):
        im=g.get("images",{}) or {}
        out.append(rec(source="giphy", title=g.get("title",""),
            url=(im.get("original",{}) or {}).get("url"), dl=(im.get("original",{}) or {}).get("url"),
            thumb=(im.get("fixed_height_small",{}) or {}).get("url"), page_url=g.get("url"),
            license="GIPHY", type="gif"))
    return out

def klipy(q, typ, n):
    key=os.environ.get("KLIPY_API_KEY")
    if not key or typ!="gif": return []
    # KLIPY exposes a /v2/search (unverified — assumes Tenor-compatible /v2/search). Thumb key is mediumgif.
    d=_get(f"https://api.klipy.com/v2/search?q={urllib.parse.quote(q)}&key={key}&limit={n}")
    out=[]
    for g in (d.get("results") or []):
        mf=g.get("media_formats") or {}
        url=(mf.get("gif",{}) or {}).get("url")
        thumb=(mf.get("nanogif") or mf.get("tinygif") or mf.get("mediumgif") or mf.get("gif") or {}).get("url")
        out.append(rec(source="klipy", title=g.get("content_description") or g.get("title",""),
            url=url, dl=url, thumb=thumb, page_url=g.get("itemurl"), license="KLIPY", type="gif"))
    return out

NOKEY={"openverse":openverse,"internetarchive":internetarchive,"nasa":nasa,"wikimedia":wikimedia,"loc":loc}
KEYED={"pexels":pexels,"pixabay":pixabay}
GIF={"klipy":klipy,"giphy":giphy}   # gif sources, used only for --type gif (tenor removed: Google EOL'd the API 2026-06-30)
ALL={**NOKEY,**KEYED}
REG={**ALL,**GIF}   # full dispatch registry

def run(q, typ, n, sources):
    res, errs = [], {}
    with cf.ThreadPoolExecutor(max_workers=len(sources)) as ex:
        futs={ex.submit(REG[s], q, typ, n): s for s in sources if s in REG}
        for f in cf.as_completed(futs):
            s=futs[f]
            try: res.extend(f.result())
            except Exception as e: errs[s]=str(e)[:80]
    return res, errs

def _ext(url, typ):
    m=re.search(r"\.(jpg|jpeg|png|gif|webp|mp4|webm|ogv)(?:\?|$)", (url or "").lower())
    return "."+m.group(1) if m else (".mp4" if typ=="video" else ".jpg")

def _safe_name(name):
    """Sanitize a filename component derived from API data: no path separators,
    no '..', no control chars, bounded length."""
    name=re.sub(r"[^A-Za-z0-9._-]", "_", name).replace("..", "_")
    return name.lstrip(".")[:100] or "file"

def download(records, out, typ):
    os.makedirs(out, exist_ok=True)
    saved=[]
    for i,r in enumerate(records):
        dl=r.get("dl")
        if not dl and r["source"]=="internetarchive" and r.get("ident"):
            dl=(_ia_video_file(r["ident"]) if typ=="video" else _ia_image_file(r["ident"])); r["dl"]=dl
        if not dl: continue
        if urllib.parse.urlparse(dl).scheme not in ("http","https"):
            r["download_error"]="skipped non-http(s) URL"; continue
        fn=_safe_name(f"{i:02d}_{r['source']}{_ext(dl, r['type'])}")
        path=os.path.join(out, fn)
        try:
            req=urllib.request.Request(dl, headers=UA)
            with urllib.request.urlopen(req, timeout=30) as resp, open(path,"wb") as fh:
                fh.write(resp.read())
            r["file"]=fn; saved.append(r)
        except Exception as e:
            r["download_error"]=str(e)[:60]
    with open(os.path.join(out,"attribution.json"),"w") as fh:
        json.dump(records, fh, indent=1)
    return saved

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("--type",default="image",choices=["image","video","gif"])
    ap.add_argument("--count",type=int,default=6)
    ap.add_argument("--source",default="all")
    ap.add_argument("--json",action="store_true")
    ap.add_argument("--download",action="store_true")
    ap.add_argument("--out",default="./downloads")
    a=ap.parse_args()
    if a.type=="gif":
        sources = list(GIF) if a.source=="all" else [s.strip() for s in a.source.split(",")]
    else:
        sources = list(ALL) if a.source=="all" else list(NOKEY) if a.source=="nokey" else [s.strip() for s in a.source.split(",")]
    res,errs=run(a.query,a.type,a.count,sources)
    if a.download:
        saved=download(res,a.out,a.type)
        print(f"  downloaded {len(saved)}/{len(res)} {a.type} → {a.out}  (attribution.json written)")
        if errs: print(f"  source errors: {errs}")
        return
    if a.json:
        print(json.dumps({"query":a.query,"type":a.type,"count":len(res),"errors":errs,"results":res},indent=1)); return
    print(f"\n  {len(res)} {a.type} results for {a.query!r}  (sources: {','.join(sorted({r['source'] for r in res}))})")
    if errs: print(f"  skipped: {errs}")
    for r in res:
        print(f"  [{r['source']:14}] {(r['title'] or '')[:48]:48}  {r['license'][:20]}")
        print(f"     {r['url']}")

if __name__=="__main__": main()
