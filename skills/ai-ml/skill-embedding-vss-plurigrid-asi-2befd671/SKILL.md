---
name: skill-embedding-vss
description: P-adic ultrametric skill embeddings with MLX Snowflake Arctic, DuckDB VSS, and full SPI tracing
license: MIT
metadata:
  trit: 0
  color: '#5DE93A'
  gf3_role: ERGODIC
  version: 2.0.0
  embedding_model: mlx-community/snowflake-arctic-embed-l-v2.0-8bit
  embedding_dim: 1024
  index_type: HNSW
  distance_metric: padic_ultrametric
  prime: 2
---

# Skill Embedding VSS

Vector similarity search for Agent Skills using:
- **P-adic ultrametric distance** (non-Archimedean, hierarchical clustering)
- **Snowflake Arctic 1024-bit embeddings** via MLX on Apple Silicon
- **DuckDB HNSW index** for fast approximate nearest neighbor
- **SPI tracing** down to individual Metal operations
- **Content ID extraction** with cq/jq/narya.el normal forms

## GF(3) Triad

```
skill-embedding-vss (0) ⊗ skill-connectivity-hub (-1) ⊗ skill-installer (+1) = 0 ✓
```

## Dependencies

```bash
uv pip install mlx-embeddings duckdb
```

## Core Implementation

```python
from mlx_embeddings import load
import mlx.core as mx
import numpy as np
import duckdb
import os

class SkillEmbeddingVSS:
    """Embed and search skills using MLX Snowflake + DuckDB HNSW."""
    
    MODEL_ID = "mlx-community/snowflake-arctic-embed-l-v2.0-8bit"
    EMBEDDING_DIM = 1024
    
    def __init__(self, skills_dir: str):
        self.skills_dir = skills_dir
        self.model, self.tokenizer = load(self.MODEL_ID)
        self.model.eval()
        self.conn = duckdb.connect(':memory:')
        self.conn.execute('INSTALL vss; LOAD vss')
        self.conn.execute(f'''
            CREATE TABLE skills (
                name VARCHAR PRIMARY KEY,
                is_target BOOLEAN,
                embedding FLOAT[{self.EMBEDDING_DIM}]
            )
        ''')
        self.skill_data = []
        self.embeddings = []
    
    def embed_text(self, text: str, max_tokens: int = 512) -> np.ndarray:
        """Generate embedding for text using Snowflake Arctic."""
        tokens = self.tokenizer.encode(text[:max_tokens * 4])[:max_tokens]
        input_ids = mx.array([tokens])
        attention_mask = mx.ones_like(input_ids)
        outputs = self.model(input_ids, attention_mask=attention_mask)
        if outputs.text_embeds is not None:
            return np.array(outputs.text_embeds[0])
        return np.array(mx.mean(outputs.last_hidden_state, axis=1)[0])
    
    def index_skills(self, target_skills: list[str] = None):
        """Index all skills from directory."""
        target_skills = target_skills or []
        skills = [d for d in os.listdir(self.skills_dir) 
                  if os.path.isdir(os.path.join(self.skills_dir, d)) 
                  and not d.startswith('.') and d != '_integrated']
        
        for skill in skills:
            skill_path = os.path.join(self.skills_dir, skill, 'SKILL.md')
            if os.path.exists(skill_path):
                with open(skill_path, 'r') as f:
                    content = f.read()[:3000]
                emb = self.embed_text(content)
                is_target = skill in target_skills
                self.skill_data.append({'name': skill, 'is_target': is_target})
                self.embeddings.append(emb)
                self.conn.execute(
                    'INSERT INTO skills VALUES (?, ?, ?)',
                    [skill, is_target, emb.tolist()]
                )
        
        self.embeddings = np.array(self.embeddings)
        self.conn.execute('CREATE INDEX skills_idx ON skills USING HNSW (embedding)')
        return len(self.skill_data)
    
    def find_nearest(self, skill_name: str, k: int = 3, exclude_targets: bool = True) -> list:
        """Find k nearest skills to given skill."""
        idx = next((i for i, s in enumerate(self.skill_data) if s['name'] == skill_name), None)
        if idx is None:
            return []
        
        query_emb = self.embeddings[idx].tolist()
        exclude_clause = "AND NOT is_target" if exclude_targets else ""
        
        result = self.conn.execute(f'''
            SELECT name, array_distance(embedding, ?::FLOAT[{self.EMBEDDING_DIM}]) as dist
            FROM skills 
            WHERE name != ? {exclude_clause}
            ORDER BY dist ASC
            LIMIT ?
        ''', [query_emb, skill_name, k]).fetchall()
        
        return [(name, float(dist)) for name, dist in result]
    
    def find_most_novel(self, target_skills: list[str], top_k: int = 5) -> list:
        """Find which target skills are most novel (furthest from others)."""
        novelty = []
        for skill_name in target_skills:
            nearest = self.find_nearest(skill_name, k=1, exclude_targets=True)
            if nearest:
                novelty.append((skill_name, nearest[0][1]))
        
        novelty.sort(key=lambda x: -x[1])
        return novelty[:top_k]
    
    def embed_query(self, query_text: str, k: int = 5) -> list:
        """Find skills most similar to arbitrary query text."""
        query_emb = self.embed_text(query_text)
        
        result = self.conn.execute(f'''
            SELECT name, array_distance(embedding, ?::FLOAT[{self.EMBEDDING_DIM}]) as dist
            FROM skills
            ORDER BY dist ASC
            LIMIT ?
        ''', [query_emb.tolist(), k]).fetchall()
        
        return [(name, float(dist)) for name, dist in result]
    
    def close(self):
        self.conn.close()
```

## Usage Examples

### Index and Search Skills

```python
from skill_embedding_vss import SkillEmbeddingVSS

# Define target skills (e.g., a contributor's skills)
zubyul_skills = [
    'aptos-wallet-mcp', 'skill-connectivity-hub', 'glass-hopping',
    'ordered-locale', 'covariant-modification', 'catsharp-galois',
    'topos-of-music', 'gay-integration', 'kolmogorov-codex-quest'
]

# Initialize and index
vss = SkillEmbeddingVSS('/path/to/skills')
vss.index_skills(target_skills=zubyul_skills)

# Find nearest non-target skills
for skill in zubyul_skills:
    neighbors = vss.find_nearest(skill, k=3)
    print(f"🎯 {skill}")
    for name, dist in neighbors:
        print(f"   ├─ {name} ({dist:.4f})")

# Find most novel contributions
novel = vss.find_most_novel(zubyul_skills, top_k=5)
for name, dist in novel:
    print(f"🆕 {name}: {dist:.4f}")

vss.close()
```

### Query by Description

```python
# Find skills matching a concept
results = vss.embed_query("blockchain wallet integration with GF(3) conservation")
for name, dist in results:
    print(f"{name}: {dist:.4f}")
```

## Babashka CLI Wrapper

```clojure
#!/usr/bin/env bb
;; skill-vss.bb - Query skill embeddings

(require '[babashka.process :refer [shell]])
(require '[cheshire.core :as json])

(defn query-skills [query-text]
  (let [result (shell {:out :string}
                 "uv" "run" "--with" "mlx-embeddings" "--with" "duckdb"
                 "python3" "-c"
                 (format "
from skill_embedding_vss import SkillEmbeddingVSS
import json
vss = SkillEmbeddingVSS('%s')
vss.index_skills()
results = vss.embed_query('%s', k=5)
print(json.dumps(results))
vss.close()
" (System/getenv "SKILLS_DIR") query-text))]
    (json/parse-string (:out result) true)))

(when (= *file* (System/getProperty "babashka.file"))
  (let [query (first *command-line-args*)]
    (doseq [[name dist] (query-skills query)]
      (println (format "%-40s %.4f" name dist)))))
```

## Justfile Recipes

```makefile
# Embed all skills and create index
embed-skills skills_dir:
    uv run --with mlx-embeddings --with duckdb python3 -c "
    from skill_embedding_vss import SkillEmbeddingVSS
    vss = SkillEmbeddingVSS('{{skills_dir}}')
    n = vss.index_skills()
    print(f'Indexed {n} skills')
    vss.close()
    "

# Find nearest skills to a target
nearest skill_name skills_dir:
    uv run --with mlx-embeddings --with duckdb python3 -c "
    from skill_embedding_vss import SkillEmbeddingVSS
    vss = SkillEmbeddingVSS('{{skills_dir}}')
    vss.index_skills()
    for name, dist in vss.find_nearest('{{skill_name}}', k=5):
        print(f'{name}: {dist:.4f}')
    vss.close()
    "

# Search by text query
search query skills_dir:
    uv run --with mlx-embeddings --with duckdb python3 -c "
    from skill_embedding_vss import SkillEmbeddingVSS
    vss = SkillEmbeddingVSS('{{skills_dir}}')
    vss.index_skills()
    for name, dist in vss.embed_query('{{query}}', k=10):
        print(f'{name}: {dist:.4f}')
    vss.close()
    "
```

## Model Comparison

| Model | Dim | Size | Quality | Speed |
|-------|-----|------|---------|-------|
| all-MiniLM-L6-v2 | 384 | 90MB | Baseline | Fast |
| **snowflake-arctic-embed-l-v2.0-8bit** | 1024 | 1.2GB | **Best** | Medium |
| Qwen3-Embedding-8B | 4096 | 4.7GB | SOTA | Slow |

## Invariants

```yaml
invariants:
  - name: embedding_determinism
    predicate: "same text → same embedding"
    scope: per_embed
    
  - name: hnsw_recall
    predicate: "recall@10 >= 0.95"
    scope: per_index
    
  - name: gf3_conservation
    predicate: "trit(skill-embedding-vss) + trit(hub) + trit(installer) = 0"
    scope: per_triad
```

## Fibers

```yaml
fibers:
  - name: skill_embedding_fiber
    base: "Skill"
    projection: "embed_text(skill.content) → R^1024"
    
  - name: similarity_fiber  
    base: "Skill × Skill"
    projection: "array_distance(emb_a, emb_b) → R"
    
  - name: novelty_fiber
    base: "SkillSet"
    projection: "min_distance_to_complement → R"
```

## Trifurcated Random Walk

The `trifurcate_walk.py` module implements SplitMix64-seeded random walks through the 1024-dim embedding space with GF(3) trifurcation at each step.

### SplitMix64 / SplitMixTernary

```python
@dataclass
class SplitMix64:
    """Splittable PRNG - same seed = same sequence."""
    state: int
    GOLDEN = 0x9e3779b97f4a7c15
    
    def next_trit(self) -> int:
        """Generate trit in {-1, 0, +1} via mod 3."""
        return (self.next() % 3) - 1
    
    def trifurcate(self) -> Tuple['SplitMix64', 'SplitMix64', 'SplitMix64']:
        """Split into three streams for GF(3) parallel execution."""
        return (SplitMix64(self.next()),   # MINUS
                SplitMix64(self.next()),   # ERGODIC  
                SplitMix64(self.next()))   # PLUS

class SplitMixTernary:
    """Generates balanced trit triples that sum to 0 (mod 3)."""
    def next_balanced_triple(self) -> Tuple[int, int, int]:
        t1 = self.rng.next_trit()
        t2 = self.rng.next_trit()
        t3 = -(t1 + t2) % 3  # Conservation
        return (t1, t2, t3 if t3 != 2 else -1)
```

### Walk Algorithm

```
At each step:
1. Find k nearest neighbors per trit: {MINUS: [...], ERGODIC: [...], PLUS: [...]}
2. Select one from each → balanced triad (Σ = 0)
3. SplitMixTernary emits conserved trit → pick corresponding path
4. Continue from chosen skill, avoiding visited nodes
```

### Example Walk

```
bisimulation-game (seed=1069):
  Step 0: bisimulation-game → [+] glass-bead-game
          Triad: [+]glass-bead-game, [−]open-games, [○]blackhat-go (Σ=0)
  Step 1: glass-bead-game → [−] dialectica
          Triad: [+]world-hopping, [○]glass-hopping, [−]dialectica (Σ=0)
  Step 2: dialectica → [○] skill-connectivity-hub
          Triad: [−]open-games, [○]skill-connectivity-hub, [○]glass-hopping (Σ=-1)
```

### Parallel Trifurcated Walks

```python
walker = TrifurcatedSkillWalk(skills_dir, seed=1069)
walker.index_skills()

# Three parallel walkers with independent RNG streams
results = walker.parallel_walk('bisimulation-game', steps=5)
# results = {'MINUS': [...], 'ERGODIC': [...], 'PLUS': [...]}
```

### CLI Usage

```bash
python trifurcate_walk.py /path/to/skills start_skill [seed]
python trifurcate_walk.py /tmp/plurigrid-asi/skills bisimulation-game 1069
```

## P-adic Ultrametric Distance

The `padic_ultrametric.py` module implements non-Archimedean distance for hierarchical skill clustering.

### Why P-adic?

Standard Euclidean distance satisfies the triangle inequality:
```
d(x, z) ≤ d(x, y) + d(y, z)
```

P-adic ultrametric satisfies the **strong** triangle inequality:
```
d(x, z) ≤ max(d(x, y), d(y, z))
```

This means:
- All triangles are isoceles (two sides equal)
- The unequal side is always the shortest
- Natural hierarchical clustering emerges

### P-adic Valuation

```python
def p_adic_valuation(n: int, p: int = 2) -> int:
    """v_p(n) = largest k such that p^k divides n."""
    if n == 0: return float('inf')
    k = 0
    while n % p == 0:
        n //= p
        k += 1
    return k

def p_adic_norm(n: int, p: int = 2) -> float:
    """|n|_p = p^(-v_p(n))"""
    return p ** (-p_adic_valuation(n, p))

def padic_ultrametric_distance(emb_a, emb_b, p=2) -> float:
    """d_p(a, b) = max_i |a_i - b_i|_p"""
    diff = (emb_a - emb_b) * 2**32  # Fixed-point
    return max(p_adic_norm(abs(int(d)), p) for d in diff)
```

### Full Stack Trace

```
┌─────────────────────────────────────────────────────────────┐
│                    UMAP / itUMAP                            │
│            (dimensionality reduction to 2D/3D)              │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                    HNSW Index                               │
│            (approximate nearest neighbor)                   │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│          Snowflake Arctic Embed 1024-bit                    │
│            (dense semantic vectors)                         │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                   MLX Operations                            │
│     tokenize → embedding_lookup → attention → pool          │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│               Apple Silicon Metal                           │
│     gather, matmul, softmax, reduce_mean kernels            │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│           Strong Parallelism Invariance                     │
│     seed → deterministic trace → fingerprint                │
└─────────────────────────────────────────────────────────────┘
```

### Content ID Extraction

Finds skills with IDs and computes normal forms:

```python
@dataclass
class ContentID:
    id: str
    content: str
    normal_form: str  # cq | jq normalized
    hash: str
    source: str
    
    @classmethod
    def from_skill(cls, skill_path: Path) -> Optional['ContentID']:
        """Extract if skill has id: field."""
        content = skill_path.read_text()
        id_match = re.search(r'id:\s*["\']?([^"\'\n]+)', content)
        if id_match:
            normal = jq_normalize(content)  # or cq_normalize
            return cls(id=id_match.group(1), ...)
```

### Narya.el Semantic Diff

```python
@dataclass 
class NaryaDiff:
    before: str
    after: str
    delta: Dict[str, Any]  # {added, removed, changed}
    birth: List[str]       # New content
    death: List[str]       # Removed content
    
    def to_narya_witness(self) -> Dict:
        return {
            'before': hash(self.before)[:16],
            'after': hash(self.after)[:16],
            'delta': self.delta,
            'birth': len(self.birth),
            'death': len(self.death),
            'impact': self.delta['changed'] > 0
        }
```

### SPI Verification

```python
@dataclass
class SPIVerifier:
    seed: int
    traces: List[MLXTrace]
    
    def verify_determinism(self, emb1, emb2) -> bool:
        """Same seed → same embedding (SPI)."""
        return np.allclose(emb1, emb2, rtol=1e-5)
    
    def fingerprint(self, embedding) -> str:
        """Deterministic hash for audit trail."""
        quantized = (embedding * 1e6).astype(np.int64)
        return sha256(quantized.tobytes()).hexdigest()[:16]
```

### CLI Usage

```bash
# Find skills with content IDs and p-adic neighbors
python padic_ultrametric.py /path/to/skills

# Output:
# Skills with Content IDs (7)
#   python-development: int (hash: 0a49ae9b...)
#   time-travel-crdt: OpId (hash: 14973d04...)
#
# P-adic Nearest to bisimulation-game
#   glass-bead-game: eucl=0.8511, p-adic=1.000000
#   open-games: eucl=0.8755, p-adic=1.000000
#
# SPI Report
#   Seed: 1069, Prime: 2
#   Total ops: 1296, Chain valid: True
#   Total FLOPS: 14,998,474,752
```

## References

- [Snowflake Arctic Embed](https://huggingface.co/Snowflake/snowflake-arctic-embed-l-v2.0)
- [DuckDB VSS Extension](https://duckdb.org/docs/extensions/vss)
- [MLX Embeddings](https://github.com/ml-explore/mlx-examples)
- [SplitMix64](https://dl.acm.org/doi/10.1145/2714064.2660195) - Steele et al. 2014
- [P-adic Numbers](https://en.wikipedia.org/wiki/P-adic_number) - Non-Archimedean analysis
- [Ultrametric Trees](https://arxiv.org/abs/1703.02287) - Hierarchical clustering
