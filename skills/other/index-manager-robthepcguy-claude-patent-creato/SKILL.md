---
name: index-manager
description: Manages MPEP index lifecycle including downloads, building, maintenance, and optimization.
---

# Index Manager Skill

Expert system for managing MPEP search index lifecycle: PDF downloads, index building, maintenance, updates, optimization.

**FOR CLAUDE:** All dependencies installed, system operational.
- Go directly to appropriate phase
- Scripts/tools in mcp_server/
- Use patent-creator CLI when available
- Only run diagnostics if operations fail

## When to Use

Building/rebuilding MPEP index, corruption/missing files, optimization, adding content, troubleshooting.

## Index Lifecycle

```
PDFs Not Present -> Download (2-5 min, 500MB)
  -> Extract & Parse (500MB data)
  -> Generate Embeddings (5-10 min GPU, 35-65 min CPU)
  -> Build FAISS + BM25 Indexes
  -> Index Ready (mcp_server/index/)
  -> Maintenance (Verify -> Optimize -> Update)
```

## Phase 1: PDF Management

**Check Status:**
```bash
ls pdfs/  # Should show mpep-*.pdf, consolidated_laws.pdf, consolidated_rules.pdf
```

**Download PDFs:**
```bash
patent-creator download-mpep
# Or: python install.py (Select "Download MPEP PDFs")
```

**Verify Integrity:**
```bash
python -c "
import fitz
from pathlib import Path
for pdf in Path('pdfs').glob('*.pdf'):
    try:
        doc = fitz.open(pdf)
        print(f'[OK] {pdf.name}: {len(doc)} pages')
        doc.close()
    except Exception as e:
        print(f'[X] {pdf.name}: ERROR - {e}')
"
```

## Phase 2: Index Building

```bash
patent-creator rebuild-index
# Or: python mcp_server/server.py --rebuild-index
```

**Timeline:**
- Load PDFs: 30s
- Extract text: 1-2 min
- Chunk text (500 tokens): 30s
- Generate embeddings: 5-10 min (GPU) or 35-65 min (CPU)
- Build FAISS/BM25: 1 min
- Save to disk: 10s

**Total:** 5-15 min (GPU) or 35-65 min (CPU)

**Custom Build:**
```python
from mcp_server.mpep_search import MPEPIndex
index = MPEPIndex(use_hyde=False)
index.build_index(
    chunk_size=500,
    overlap=50,
    batch_size=32  # Reduce to 16/8 if OOM
)
```

## Phase 3: Verification

```bash
# Check files
ls -lh mcp_server/index/
# Expected: mpep_index.faiss (~150MB), mpep_metadata.json (~80MB), mpep_bm25.pkl (~60MB)

# Verify health
patent-creator health
# Should show: [OK] MPEP Index: Ready (12,543 chunks)

# Manual test
python -c "
from mcp_server.mpep_search import MPEPIndex
index = MPEPIndex()
print(f'Chunks: {len(index.chunks)}')
results = index.search('claim definiteness', top_k=3)
print(f'Search results: {len(results)}')
"
```

## Phase 4: Maintenance

**When to Rebuild:**
- MPEP updates (quarterly check uspto.gov)
- Index corruption
- After adding new PDFs
- Performance degradation
- Machine migration

**Rebuild Process:**
```bash
# Backup (optional)
cp -r mcp_server/index mcp_server/index_backup_$(date +%Y%m%d)

# Rebuild
patent-creator rebuild-index

# Verify
patent-creator health

# Remove backup if successful
rm -rf mcp_server/index_backup_*
```

## Phase 5: Content Updates

```bash
# Download new PDF
wget https://www.uspto.gov/web/offices/pac/mpep/mpep-2900.pdf -O pdfs/mpep-2900.pdf

# Rebuild (includes new section)
patent-creator rebuild-index
```

**Note:** Incremental updates not supported. Full rebuild required.

## Troubleshooting

- OOM errors during build
- Build taking too long
- Corrupted index files
- Search returning no results

## Performance Tuning

- Embedding generation speed (GPU vs CPU)
- Search latency optimization
- Index size reduction
- Batch size tuning

## Quick Reference

| Command | Purpose |
|---------|---------|
| `patent-creator download-mpep` | Download MPEP PDFs |
| `patent-creator rebuild-index` | Build/rebuild search index |
| `patent-creator health` | Check index health |
| `ls -lh mcp_server/index/` | View index files |

**Best Practices:**
1. Backup before rebuild
2. Verify PDFs before building
3. Use GPU for 10x faster builds
4. Test after rebuild
5. Keep PDFs until verified
6. Weekly health checks
