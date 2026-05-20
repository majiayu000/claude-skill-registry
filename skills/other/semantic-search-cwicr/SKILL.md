---
name: "semantic-search-cwicr"
description: "Semantic search in DDC CWICR construction database using vector embeddings. Find similar work items and resources for cost estimation."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "🗄️", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"], "env": ["QDRANT_URL"]}, "primaryEnv": "QDRANT_URL"}}
---
# Semantic Search in DDC CWICR Database

## Business Case

### Problem Statement
Construction cost estimation requires finding relevant work items from large databases. Traditional keyword search fails when:
- Users describe work in natural language
- Terminology varies across regions and languages
- Similar work items have different naming conventions

### Solution
DDC CWICR database provides pre-computed embeddings (OpenAI text-embedding-3-large, 3072 dimensions) enabling semantic similarity search across 55,719 work items in 9 languages.

### Business Value
- **90% faster** work item lookup compared to manual search
- **Multi-language** support: Arabic, Chinese, German, English, Spanish, French, Hindi, Portuguese, Russian
- **Higher accuracy** by finding semantically similar items, not just keyword matches

## Technical Implementation

### Prerequisites
```bash
pip install qdrant-client openai pandas
```

### Database Setup
```bash
# Download Qdrant snapshot
wget https://github.com/datadrivenconstruction/OpenConstructionEstimate-DDC-CWICR/releases/download/v0.1.0/qdrant_snapshot_en.tar.gz

# Start Qdrant with Docker
docker run -p 6333:6333 -v $(pwd)/qdrant_storage:/qdrant/storage qdrant/qdrant
```

### Python Implementation

```python
import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
import openai

class CWICRSemanticSearch:
    def __init__(self, qdrant_host: str = "localhost", port: int = 6333):
        self.client = QdrantClient(host=qdrant_host, port=port)
        self.collection_name = "ddc_cwicr_en"
        self.embedding_model = "text-embedding-3-large"
        self.embedding_dim = 3072

    def get_embedding(self, text: str) -> list:
        """Generate embedding for search query."""
        response = openai.embeddings.create(
            model=self.embedding_model,
            input=text
        )
        return response.data[0].embedding

    def search_work_items(self, query: str, limit: int = 10,
                          min_score: float = 0.7) -> pd.DataFrame:
        """Search for similar work items."""
        query_vector = self.get_embedding(query)

        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit,
            score_threshold=min_score
        )

        items = []
        for result in results:
            item = result.payload
            item['similarity_score'] = result.score
            items.append(item)

        return pd.DataFrame(items)

    def search_by_category(self, query: str, category: str,
                           limit: int = 10) -> pd.DataFrame:
        """Search within specific category."""
        query_vector = self.get_embedding(query)

        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            query_filter={
                "must": [{"key": "category", "match": {"value": category}}]
            },
            limit=limit
        )

        return pd.DataFrame([{**r.payload, 'score': r.score} for r in results])

    def estimate_cost(self, work_items: pd.DataFrame,
                      quantities: dict) -> dict:
        """Calculate cost from matched work items."""
        total_cost = 0
        breakdown = []

        for _, item in work_items.iterrows():
            if item['work_item_code'] in quantities:
                qty = quantities[item['work_item_code']]
                cost = qty * item.get('unit_price', 0)
                total_cost += cost
                breakdown.append({
                    'item': item['description'],
                    'quantity': qty,
                    'unit_price': item.get('unit_price', 0),
                    'total': cost
                })

        return {
            'total_cost': total_cost,
            'breakdown': breakdown,
            'currency': 'Regional default'
        }
```

## Usage Examples

### Basic Search
```python
search = CWICRSemanticSearch()

# Natural language query
results = search.search_work_items("brick masonry wall construction")
print(results[['description', 'unit', 'unit_price', 'similarity_score']])
```

### Cost Estimation
```python
# Find work items for foundation work
foundation_items = search.search_work_items(
    "reinforced concrete foundation excavation and pouring",
    limit=20
)

# Estimate with quantities
quantities = {
    'CONC-001': 150,  # cubic meters
    'EXCV-002': 200,  # cubic meters
}
estimate = search.estimate_cost(foundation_items, quantities)
print(f"Estimated Cost: ${estimate['total_cost']:,.2f}")
```

## Database Schema

| Field | Type | Description |
|-------|------|-------------|
| work_item_code | string | Unique identifier |
| description | string | Work item description |
| unit | string | Measurement unit |
| labor_norm | float | Labor hours per unit |
| material_cost | float | Material cost per unit |
| equipment_cost | float | Equipment cost per unit |
| unit_price | float | Total price per unit |
| category | string | Work category |
| embedding | vector[3072] | Pre-computed embedding |

## Best Practices

1. **Use specific queries** - "reinforced concrete slab 200mm" beats "concrete"
2. **Filter by category** - Narrow results to relevant work types
3. **Check similarity scores** - Scores below 0.7 may need manual verification
4. **Combine with QTO** - Use BIM quantities for automated estimation

## Resources

- **GitHub**: [OpenConstructionEstimate-DDC-CWICR](https://github.com/datadrivenconstruction/OpenConstructionEstimate-DDC-CWICR)
- **Releases**: [v0.1.0 Database Downloads](https://github.com/datadrivenconstruction/OpenConstructionEstimate-DDC-CWICR/releases)
- **Qdrant Docs**: https://qdrant.tech/documentation/
