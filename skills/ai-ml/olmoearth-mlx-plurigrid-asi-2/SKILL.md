---
name: olmoearth-mlx
description: "OlmoEarth MLX: Spatio-Temporal Earth Intelligence"
version: 1.0.0
---

# OlmoEarth MLX: Spatio-Temporal Earth Intelligence

**Trit**: +1 (PLUS - world creation via planetary observation)  
**Foundation**: AI2 OlmoEarth + Apple MLX + GeoACSet + Dune.xyz Geographic WEV

## Overview

OlmoEarth is AI2's open spatio-temporal foundation model for planetary intelligence, trained on:
- Sentinel-2 L2A (12 bands, 10-60m resolution)
- Sentinel-1 SAR (VV, VH polarization)
- Landsat (historical continuity)
- WorldCover (11 land cover classes)
- OpenStreetMap raster
- SRTM elevation
- WRI Canopy Height Map

This skill enables:
1. **Geographic embedding** of crypto wallet activity from Dune.xyz
2. **Impact area identification** for Protocol Labs infrastructure
3. **GeoACSet materialization** for categorical spatial reasoning

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     OLMOEARTH-MLX PIPELINE                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Dune.xyz Query ─┬─► IP Geolocation ─┬─► OlmoEarth Embedding            │
│                  │                   │                                  │
│  Wallet Activity ┘   Region Bounds  ─┘   FlexiVit Encoder               │
│                                              │                          │
│                                              ▼                          │
│                              ┌───────────────────────────────────┐      │
│                              │     GeoACSet Materialization      │      │
│                              │   Regions → Districts → Parcels   │      │
│                              │        with GF(3) trits           │      │
│                              └───────────────────────────────────┘      │
│                                              │                          │
│                                              ▼                          │
│                              ┌───────────────────────────────────┐      │
│                              │     Tenderloin WEV Integration    │      │
│                              │   Geographic Value Extraction     │      │
│                              └───────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────────────┘
```

## OlmoEarth Model Specs

| Model | Encoder Params | Decoder Params | Embed Dim | Depth |
|-------|----------------|----------------|-----------|-------|
| Nano  | 5.8M          | 3.7M           | 192       | 12    |
| Tiny  | 22M           | 14M            | 384       | 12    |
| Base  | 86M           | 55M            | 768       | 12    |
| Large | 307M          | 197M           | 1024      | 24    |

### Supported Modalities

```python
MODALITIES = {
    "SENTINEL2_L2A": {
        "bands": ["B02", "B03", "B04", "B05", "B06", "B07", 
                  "B08", "B8A", "B11", "B12", "SCL", "CLD"],
        "gsd": [10, 10, 10, 20, 20, 20, 10, 20, 20, 20, 20, 20],
        "temporal": True
    },
    "SENTINEL1": {
        "bands": ["VV", "VH"],
        "gsd": [10, 10],
        "temporal": True
    },
    "WORLDCOVER": {
        "bands": ["LC"],
        "classes": 11,  # Tree, Shrub, Grass, Crop, Built, Bare, Snow, Water, Wetland, Mangrove, Moss
        "gsd": [10],
        "temporal": False
    },
    "SRTM": {
        "bands": ["elevation"],
        "gsd": [30],
        "temporal": False
    }
}
```

## MLX Inference

```python
# olmoearth_mlx.py - Apple Silicon optimized inference

import mlx.core as mx
import mlx.nn as nn
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

@dataclass
class OlmoEarthConfig:
    """OlmoEarth model configuration for MLX."""
    embed_dim: int = 768
    depth: int = 12
    num_heads: int = 12
    patch_size: int = 4
    num_modalities: int = 8
    temporal_tokens: int = 4

class FlexiVitEncoder(nn.Module):
    """FlexiVit encoder for OlmoEarth on MLX."""
    
    def __init__(self, config: OlmoEarthConfig):
        super().__init__()
        self.config = config
        
        # Patch embeddings per modality
        self.patch_embed = nn.Linear(
            config.patch_size * config.patch_size * 12,  # Max bands
            config.embed_dim
        )
        
        # Positional encoding
        self.pos_embed = mx.zeros((1, 256, config.embed_dim))
        
        # Transformer blocks
        self.blocks = [
            TransformerBlock(config.embed_dim, config.num_heads)
            for _ in range(config.depth)
        ]
        
        self.norm = nn.LayerNorm(config.embed_dim)
    
    def __call__(self, x: mx.array, timestamps: mx.array) -> mx.array:
        # Patchify and embed
        x = self.patch_embed(x)
        x = x + self.pos_embed[:, :x.shape[1], :]
        
        # Transform
        for block in self.blocks:
            x = block(x)
        
        return self.norm(x)

class TransformerBlock(nn.Module):
    def __init__(self, dim: int, num_heads: int):
        super().__init__()
        self.attn = nn.MultiHeadAttention(dim, num_heads)
        self.mlp = nn.Sequential(
            nn.Linear(dim, dim * 4),
            nn.GELU(),
            nn.Linear(dim * 4, dim)
        )
        self.norm1 = nn.LayerNorm(dim)
        self.norm2 = nn.LayerNorm(dim)
    
    def __call__(self, x: mx.array) -> mx.array:
        x = x + self.attn(self.norm1(x), self.norm1(x), self.norm1(x))
        x = x + self.mlp(self.norm2(x))
        return x
```

## Dune.xyz Geographic Mapping

### Trackable Interactions

| Query | Geographic Signal | GeoACSet Mapping |
|-------|-------------------|------------------|
| Filecoin Storage Deals | Provider location | Region → District |
| FVM Contract Deploys | Creator wallet region | District → Parcel |
| Bridge Transactions | Source/dest chains | Region ↔ Region |
| Grant Disbursements | Recipient geography | Parcel → Building |

### SQL Queries (Dune)

```sql
-- Filecoin storage provider geographic distribution
SELECT 
    provider_id,
    COALESCE(ip_geolocation.country, 'Unknown') as country,
    COALESCE(ip_geolocation.region, 'Unknown') as region,
    COUNT(*) as deals,
    SUM(piece_size) as total_bytes
FROM filecoin.storage_deals sd
LEFT JOIN ip_geolocation ON sd.provider_ip = ip_geolocation.ip
WHERE deal_timestamp > NOW() - INTERVAL '30 days'
GROUP BY 1, 2, 3
ORDER BY deals DESC;

-- FVM contract geographic heat map
SELECT 
    DATE_TRUNC('day', block_timestamp) as day,
    creator_country,
    creator_region,
    COUNT(DISTINCT contract_address) as contracts,
    SUM(gas_used) as total_gas
FROM filecoin.fvm_contracts
WHERE block_timestamp > NOW() - INTERVAL '90 days'
GROUP BY 1, 2, 3;

-- Cross-chain bridge flows by geography
SELECT
    source_chain,
    dest_chain,
    sender_region,
    receiver_region,
    SUM(amount_usd) as volume_usd,
    COUNT(*) as tx_count
FROM bridge_transactions
WHERE timestamp > NOW() - INTERVAL '7 days'
  AND (source_chain = 'filecoin' OR dest_chain = 'filecoin')
GROUP BY 1, 2, 3, 4;
```

## GeoACSet Materialization

```julia
# GeoACSet schema for crypto-geographic data
@present SchCryptoGeo(FreeSchema) begin
    # Objects
    Region::Ob
    District::Ob
    Wallet::Ob
    Transaction::Ob
    EarthTile::Ob
    
    # Morphisms
    region_of::Hom(District, Region)
    district_of::Hom(Wallet, District)
    sender::Hom(Transaction, Wallet)
    receiver::Hom(Transaction, Wallet)
    tile_of::Hom(Wallet, EarthTile)
    
    # Attributes
    lat::Attr(Region, Float64)
    lon::Attr(Region, Float64)
    embedding::Attr(EarthTile, Vector{Float32})  # OlmoEarth embedding
    trit::Attr(Transaction, Int)  # GF(3) classification
end

@acset_type CryptoGeoACSet(SchCryptoGeo)

# Materialization from Dune query results
function materialize_crypto_geo(dune_results::DataFrame)::CryptoGeoACSet
    acset = CryptoGeoACSet()
    
    # Add regions
    for row in eachrow(unique(dune_results, :region))
        add_part!(acset, :Region; 
            lat=row.lat, 
            lon=row.lon
        )
    end
    
    # Add districts within regions
    for row in eachrow(unique(dune_results, [:region, :district]))
        region_id = findfirst(r -> r == row.region, acset[:Region])
        add_part!(acset, :District; region_of=region_id)
    end
    
    # Add wallets with earth tile embeddings
    for row in eachrow(unique(dune_results, :wallet))
        district_id = findfirst(d -> d == row.district, acset[:District])
        tile_embedding = get_olmoearth_embedding(row.lat, row.lon)
        tile_id = add_part!(acset, :EarthTile; embedding=tile_embedding)
        add_part!(acset, :Wallet; district_of=district_id, tile_of=tile_id)
    end
    
    return acset
end
```

## Impact Area Identification

### Protocol Labs Infrastructure Zones

```python
PL_IMPACT_ZONES = {
    "high_density": [
        {"name": "SF Bay Area", "lat": 37.7749, "lon": -122.4194, "radius_km": 100},
        {"name": "Greater NYC", "lat": 40.7128, "lon": -74.0060, "radius_km": 80},
        {"name": "Singapore", "lat": 1.3521, "lon": 103.8198, "radius_km": 50},
    ],
    "emerging": [
        {"name": "Shenzhen", "lat": 22.5431, "lon": 114.0579, "radius_km": 60},
        {"name": "Berlin", "lat": 52.5200, "lon": 13.4050, "radius_km": 40},
        {"name": "Bangalore", "lat": 12.9716, "lon": 77.5946, "radius_km": 50},
    ],
    "frontier": [
        {"name": "Lagos", "lat": 6.5244, "lon": 3.3792, "radius_km": 30},
        {"name": "São Paulo", "lat": -23.5505, "lon": -46.6333, "radius_km": 60},
        {"name": "Jakarta", "lat": -6.2088, "lon": 106.8456, "radius_km": 40},
    ]
}

def classify_impact_zone(lat: float, lon: float) -> Tuple[str, str, float]:
    """Classify a coordinate into PL impact zone."""
    from math import radians, sin, cos, sqrt, atan2
    
    def haversine(lat1, lon1, lat2, lon2):
        R = 6371  # Earth radius in km
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
        return 2 * R * atan2(sqrt(a), sqrt(1-a))
    
    for zone_type, zones in PL_IMPACT_ZONES.items():
        for zone in zones:
            dist = haversine(lat, lon, zone["lat"], zone["lon"])
            if dist <= zone["radius_km"]:
                return zone_type, zone["name"], dist
    
    return "global", "Other", float("inf")
```

## GF(3) Geographic Classification

| Trit | Zone Type | WEV Signal | Strategy |
|------|-----------|------------|----------|
| +1 | high_density | Infrastructure concentration | Long storage deals |
| 0 | emerging | Growth potential | Bridge liquidity |
| -1 | frontier | Adoption catalyst | Grant allocation |

## Tenderloin Integration

```python
# Connect OlmoEarth embeddings to Tenderloin WEV
def geo_wev_extraction(
    dune_query: str,
    olmoearth_model: FlexiVitEncoder,
    geoacset: CryptoGeoACSet
) -> List[Dict]:
    """Extract geographic WEV from Dune data with OlmoEarth embeddings."""
    
    # Execute Dune query
    results = execute_dune_query(dune_query)
    
    wev_events = []
    for row in results:
        # Get OlmoEarth embedding for location
        embedding = olmoearth_model.embed(row.lat, row.lon)
        
        # Classify impact zone
        zone_type, zone_name, dist = classify_impact_zone(row.lat, row.lon)
        
        # Map to GF(3) trit
        trit = {"high_density": 1, "emerging": 0, "frontier": -1}.get(zone_type, 0)
        
        wev_events.append({
            "source": "dune_geo",
            "lat": row.lat,
            "lon": row.lon,
            "zone": zone_name,
            "trit": trit,
            "embedding": embedding.tolist(),
            "value": row.volume_usd,
            "category": "geographic"
        })
    
    return wev_events
```

## Usage

```bash
# Install OlmoEarth
pip install olmoearth-pretrain

# Run geographic WEV extraction
python -c "
from olmoearth_mlx import OlmoEarthMLX
from tenderloin.fund_wallets import WalletFundingEngine

# Load model
model = OlmoEarthMLX.load('olmoearth-base')

# Query Dune for geographic data
geo_wev = model.extract_geographic_wev(
    query='filecoin_storage_providers_by_region',
    timeframe='30d'
)

# Fund wallets based on geographic WEV
engine = WalletFundingEngine()
for event in geo_wev:
    engine.ingest_wev(event['category'], event['value'], trit=event['trit'])
"
```

## Canonical Triads

```
olmoearth-mlx (+1) ⊗ geoacset (0) ⊗ dune-geographic (-1) = 0 ✓
tenderloin (+1) ⊗ prediction-markets (0) ⊗ olmoearth-mlx (-1) = 0 ✓
```

## References

- [OlmoEarth arXiv Paper](https://arxiv.org/abs/2411.xxxxx)
- [allenai/olmoearth_pretrain](https://github.com/allenai/olmoearth_pretrain)
- [bmorphism/GeoACSets.jl](https://github.com/bmorphism/GeoACSets.jl)
- [Dune Analytics](https://dune.com)
- [Filecoin Data Portal](https://filecoindataportal.xyz)



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Autodiff
- **jax** [○] via bicomodule
  - Hub for autodiff/ML

### Bibliography References

- `general`: 734 citations in bib.duckdb



## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 8. Degeneracy

**Concepts**: redundancy, fallback, multiple strategies, robustness

### GF(3) Balanced Triad

```
olmoearth-mlx (+) + SDF.Ch8 (−) + [balancer] (○) = 0
```

**Skill Trit**: 1 (PLUS - generation)

### Secondary Chapters

- Ch6: Layering
- Ch10: Adventure Game Example

### Connection Pattern

Degeneracy provides fallbacks. This skill offers redundant strategies.
## Cat# Integration

This skill maps to **Cat# = Comod(P)** as a bicomodule in the equipment structure:

```
Trit: 0 (ERGODIC)
Home: Prof
Poly Op: ⊗
Kan Role: Adj
Color: #26D826
```

### GF(3) Naturality

The skill participates in triads satisfying:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

This ensures compositional coherence in the Cat# equipment structure.