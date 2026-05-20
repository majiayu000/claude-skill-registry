---
name: content-hash-cache-pattern
description: "Use when caching expensive file processing results. SHA-256 content-hash keying with frozen CacheEntry and service layer wrapper."
license: MIT
metadata:
  author: shimo4228
  version: "1.0"
  extracted: "2026-02-10"
---

# Content-Hash File Cache Pattern
# コンテンツハッシュキャッシュパターン

**Extracted / 抽出日:** 2026-02-10
**Context / コンテキスト:** ファイル処理結果をSHA-256ハッシュでキャッシュし、サービス層でラップするパターン

---

## Problem / 課題

ファイル処理（PDF解析、テキスト抽出等）は時間がかかるが、同じファイルの再処理は無駄：

```python
# WRONG: 毎回フルパイプライン実行
def process_file(path: Path) -> Result:
    return expensive_extraction(path)  # Always re-runs

# WRONG: パスベースキャッシュ（ファイル移動で無効化）
cache = {"/path/to/file.pdf": result}  # Path changes → cache miss

# WRONG: 既存関数にキャッシュパラメータ追加（SRP違反）
def extract_text(path, *, cache_enabled=False, cache_dir=None):
    if cache_enabled:  # Extraction function now has cache responsibility
        ...
```

---

## Solution / 解決策

### 1. Content-Hash Based Cache Key

ファイルパスではなくファイル内容のSHA-256ハッシュをキーに使う：

```python
import hashlib
from pathlib import Path

_HASH_CHUNK_SIZE = 65536  # 64KB chunks for large files

def compute_file_hash(path: Path) -> str:
    """SHA-256 of file contents (chunked for large files)."""
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {path}")
    sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(_HASH_CHUNK_SIZE)
            if not chunk:
                break
            sha256.update(chunk)
    return sha256.hexdigest()
```

**利点:** ファイル移動・リネームでもキャッシュヒット、内容変更で自動無効化

### 2. Frozen Dataclass for Cache Entry

```python
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class CacheEntry:
    file_hash: str
    source_path: str
    document: ExtractedDocument  # The cached result
```

### 3. JSON Serialization of Frozen Dataclasses

`dataclasses.asdict()` はネストしたfrozen dataclassで問題が起きるため、手動マッピング：

```python
import json
from typing import Any

def _serialize_entry(entry: CacheEntry) -> dict[str, Any]:
    """Manual mapping for full control over serialized format."""
    doc = entry.document
    return {
        "file_hash": entry.file_hash,
        "source_path": entry.source_path,
        "document": {
            "text": doc.text,
            "chunks": list(doc.chunks),  # tuple → list for JSON
            "file_type": doc.file_type,
            # ... other fields
        },
    }

def _deserialize_entry(data: dict[str, Any]) -> CacheEntry:
    doc_data = data["document"]
    document = ExtractedDocument(
        text=doc_data["text"],
        chunks=tuple(doc_data["chunks"]),  # list → tuple
        file_type=doc_data["file_type"],
    )
    return CacheEntry(
        file_hash=data["file_hash"],
        source_path=data["source_path"],
        document=document,
    )
```

### 4. Service Layer Wrapper (SRP)

**純粋な処理関数を変更せず**、サービス層でキャッシュロジックをラップ：

```python
# service.py — cache wrapper
def extract_with_cache(file_path: Path, *, config: AppConfig) -> ExtractedDocument:
    """Service layer: cache check → extraction → cache write."""
    if not config.cache_enabled:
        return extract_text(file_path)  # Pure function, no cache knowledge

    cache_dir = Path(config.cache_dir)
    file_hash = compute_file_hash(file_path)

    # Check cache
    cached = read_cache(cache_dir, file_hash)
    if cached is not None:
        logger.info("Cache hit: %s (hash=%s)", file_path.name, file_hash[:12])
        return cached.document

    # Cache miss → extract → store
    logger.info("Cache miss: %s (hash=%s)", file_path.name, file_hash[:12])
    doc = extract_text(file_path)
    entry = CacheEntry(file_hash=file_hash, source_path=str(file_path), document=doc)
    write_cache(cache_dir, entry)
    return doc
```

### 5. Graceful Corruption Handling

```python
def read_cache(cache_dir: Path, file_hash: str) -> CacheEntry | None:
    cache_file = cache_dir / f"{file_hash}.json"
    if not cache_file.is_file():
        return None
    try:
        raw = cache_file.read_text(encoding="utf-8")
        data = json.loads(raw)
        return _deserialize_entry(data)
    except (json.JSONDecodeError, ValueError, KeyError):
        logger.warning("Corrupted cache entry: %s", cache_file)
        return None  # Treat corruption as cache miss
```

---

## Key Design Choices / 設計上のポイント

| Choice / 選択 | Reason / 理由 |
|-------|--------|
| SHA-256 content hash | Path-independent, auto-invalidates on content change |
| `{hash}.json` file naming | O(1) lookup, no index file needed |
| Service layer wrapper | SRP: extraction stays pure, cache is separate concern |
| Manual JSON serialization | Full control over frozen dataclass serialization |
| Corruption → None | Graceful degradation, re-extracts on next run |
| `cache_dir.mkdir(parents=True)` | Lazy directory creation on first write |

---

## When to Use / 使用すべき場面

- ファイル処理パイプライン（PDF解析、画像処理、テキスト抽出）
- 処理コストが高く、同一ファイルの再処理が頻繁な場合
- CLI ツールで `--cache/--no-cache` オプションが必要な場合
- 既存の純粋関数にキャッシュを追加する場合（SRP維持）

## When NOT to Use / 使用すべきでない場面

- リアルタイム更新が必要なデータ（常に最新が必要）
- キャッシュエントリが非常に大きい場合（メモリ/ディスク圧迫）
- 処理結果がファイル内容以外のパラメータに依存する場合（設定変更でキャッシュ無効化が必要）

---

## Related Patterns / 関連パターン

- `python-immutable-accumulator.md` — frozen dataclass + slotsパターン
- `backward-compatible-frozen-extension.md` — frozen dataclass拡張
- `cost-aware-llm-pipeline.md` — LLMパイプラインでのキャッシュ活用
