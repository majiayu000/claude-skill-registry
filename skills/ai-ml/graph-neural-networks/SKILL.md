---
name: graph-neural-networks
description: Implement graph neural networks with PyTorch Geometric for node, edge, and graph tasks
---

# Graph Neural Networks

## Architecture Selection

| Architecture | Best For | Key Property | Complexity |
|-------------|----------|--------------|------------|
| **GCN** | Homogeneous graphs, semi-supervised | Spectral convolution, fixed aggregation | Low |
| **GAT** | Graphs with varying neighbor importance | Learned attention weights | Medium |
| **GraphSAGE** | Large graphs, inductive learning | Sampling + aggregation, works on unseen nodes | Medium |
| **GIN** | Graph classification, WL-test expressiveness | Injective aggregation, maximally powerful | Medium |
| **HGT** | Heterogeneous graphs, multiple relations | Type-aware attention | High |
| **TransE/RotatE** | Knowledge graph link prediction | Translation/rotation in embedding space | Low |

| Task | Recommended | Reason |
|------|-------------|--------|
| **Node classification** | GAT or GraphSAGE | Attention captures varying neighbor relevance |
| **Link prediction** | GraphSAGE + dot product | Inductive; generalizes to unseen nodes |
| **Graph classification** | GIN + global pooling | Most expressive message passing for graph-level |
| **Heterogeneous** | HGT or `to_hetero` wrapper | Handles multiple node/edge types natively |
| **Knowledge graph** | RotatE | Handles symmetric, antisymmetric, composition |

## Core Layer Implementations

### GCN, GAT, GraphSAGE

```python
import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv, GATConv, SAGEConv, global_mean_pool
from torch_geometric.data import Data

class GCN(torch.nn.Module):
    """2-layer GCN for node classification."""
    def __init__(self, in_ch: int, hidden: int, out_ch: int, dropout: float = 0.5):
        super().__init__()
        self.conv1 = GCNConv(in_ch, hidden)
        self.conv2 = GCNConv(hidden, out_ch)
        self.dropout = dropout

    def forward(self, x, edge_index):
        x = F.dropout(F.relu(self.conv1(x, edge_index)), p=self.dropout, training=self.training)
        return self.conv2(x, edge_index)       # Raw logits; apply softmax externally

class GAT(torch.nn.Module):
    """Multi-head GAT for node classification."""
    def __init__(self, in_ch: int, hidden: int, out_ch: int, heads: int = 8, dropout: float = 0.6):
        super().__init__()
        self.conv1 = GATConv(in_ch, hidden, heads=heads, dropout=dropout)
        self.conv2 = GATConv(hidden * heads, out_ch, heads=1, concat=False, dropout=dropout)
        self.dropout = dropout

    def forward(self, x, edge_index):
        x = F.dropout(x, p=self.dropout, training=self.training)
        x = F.elu(self.conv1(x, edge_index))
        x = F.dropout(x, p=self.dropout, training=self.training)
        return self.conv2(x, edge_index)

class GraphSAGE(torch.nn.Module):
    """GraphSAGE with mean aggregation for inductive learning."""
    def __init__(self, in_ch: int, hidden: int, out_ch: int, num_layers: int = 3):
        super().__init__()
        self.convs = torch.nn.ModuleList()
        self.convs.append(SAGEConv(in_ch, hidden))
        for _ in range(num_layers - 2):
            self.convs.append(SAGEConv(hidden, hidden))
        self.convs.append(SAGEConv(hidden, out_ch))

    def forward(self, x, edge_index):
        for conv in self.convs[:-1]:
            x = F.dropout(F.relu(conv(x, edge_index)), p=0.5, training=self.training)
        return self.convs[-1](x, edge_index)
```

## Message Passing Framework

```python
from torch_geometric.nn import MessagePassing
from torch_geometric.utils import add_self_loops, degree

class CustomMP(MessagePassing):
    """Custom message passing: demonstrates the propagate framework."""
    def __init__(self, in_channels: int, out_channels: int):
        super().__init__(aggr="add")               # "add", "mean", "max"
        self.lin = torch.nn.Linear(in_channels, out_channels)

    def forward(self, x, edge_index):
        edge_index, _ = add_self_loops(edge_index, num_nodes=x.size(0))
        x = self.lin(x)
        row, col = edge_index
        deg = degree(col, x.size(0), dtype=x.dtype)
        deg_inv_sqrt = deg.pow(-0.5)
        deg_inv_sqrt[deg_inv_sqrt == float("inf")] = 0
        norm = deg_inv_sqrt[row] * deg_inv_sqrt[col]
        return self.propagate(edge_index, x=x, norm=norm)

    def message(self, x_j, norm):
        return norm.view(-1, 1) * x_j              # Scale neighbor features
```

## Knowledge Graph Embeddings

```python
class TransE(torch.nn.Module):
    """TransE: h + r ~ t in embedding space."""
    def __init__(self, n_ent: int, n_rel: int, dim: int = 128, margin: float = 1.0):
        super().__init__()
        self.ent = torch.nn.Embedding(n_ent, dim)
        self.rel = torch.nn.Embedding(n_rel, dim)
        self.margin = margin
        torch.nn.init.xavier_uniform_(self.ent.weight)
        torch.nn.init.xavier_uniform_(self.rel.weight)

    def score(self, h, r, t):
        return torch.norm(self.ent(h) + self.rel(r) - self.ent(t), p=2, dim=-1)

    def forward(self, pos_h, pos_r, pos_t, neg_h, neg_r, neg_t):
        return F.relu(self.margin + self.score(pos_h, pos_r, pos_t) - self.score(neg_h, neg_r, neg_t)).mean()

class RotatE(torch.nn.Module):
    """RotatE: h * r ~ t via complex rotation."""
    def __init__(self, n_ent: int, n_rel: int, dim: int = 128, margin: float = 6.0):
        super().__init__()
        self.ent_re = torch.nn.Embedding(n_ent, dim)
        self.ent_im = torch.nn.Embedding(n_ent, dim)
        self.rel_phase = torch.nn.Embedding(n_rel, dim)
        self.margin = margin

    def score(self, h_idx, r_idx, t_idx):
        h_re, h_im = self.ent_re(h_idx), self.ent_im(h_idx)
        t_re, t_im = self.ent_re(t_idx), self.ent_im(t_idx)
        r_re, r_im = torch.cos(self.rel_phase(r_idx)), torch.sin(self.rel_phase(r_idx))
        diff_re = (h_re * r_re - h_im * r_im) - t_re
        diff_im = (h_re * r_im + h_im * r_re) - t_im
        return torch.sqrt(diff_re**2 + diff_im**2 + 1e-9).sum(dim=-1)
```

## Heterogeneous Graph Handling

```python
from torch_geometric.data import HeteroData
from torch_geometric.nn import to_hetero

def build_hetero_data():
    data = HeteroData()
    data["user"].x = torch.randn(1000, 64)
    data["item"].x = torch.randn(5000, 128)
    data["user", "buys", "item"].edge_index = torch.randint(0, 1000, (2, 10000))
    data["user", "rates", "item"].edge_index = torch.randint(0, 1000, (2, 20000))
    return data

def create_hetero_model(data: HeteroData, hidden: int = 64, out: int = 32):
    model = GraphSAGE(in_ch=-1, hidden=hidden, out_ch=out, num_layers=2)
    return to_hetero(model, data.metadata(), aggr="sum")  # Separate weights per type
```

## Mini-Batch Training with NeighborLoader

```python
from torch_geometric.loader import NeighborLoader

def train_node_classification(data: Data, model, epochs: int = 50, lr: float = 0.01):
    loader = NeighborLoader(
        data, num_neighbors=[25, 10],              # 25 1-hop, 10 2-hop
        batch_size=512, input_nodes=data.train_mask, shuffle=True,
    )
    optimizer = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=5e-4)
    model.train()
    for epoch in range(epochs):
        for batch in loader:
            optimizer.zero_grad()
            out = model(batch.x, batch.edge_index)
            loss = F.cross_entropy(out[:batch.batch_size], batch.y[:batch.batch_size])
            loss.backward()
            optimizer.step()
    return model
```

## Link Prediction Pipeline

```python
from torch_geometric.transforms import RandomLinkSplit
from torch_geometric.utils import negative_sampling

def setup_link_prediction(data: Data):
    transform = RandomLinkSplit(num_val=0.1, num_test=0.1,
        add_negative_train_samples=True, neg_sampling_ratio=1.0)
    return transform(data)                         # (train, val, test)

def link_prediction_loss(model, data):
    z = model(data.x, data.edge_index)
    src, dst = data.edge_label_index
    pos_score = (z[src] * z[dst]).sum(dim=-1)
    neg_edge = negative_sampling(data.edge_index, num_nodes=data.num_nodes, num_neg_samples=src.size(0))
    neg_score = (z[neg_edge[0]] * z[neg_edge[1]]).sum(dim=-1)
    scores = torch.cat([pos_score, neg_score])
    labels = torch.cat([torch.ones(pos_score.size(0)), torch.zeros(neg_score.size(0))])
    return F.binary_cross_entropy_with_logits(scores, labels.to(scores.device))
```

## Gotchas

- **Over-smoothing**: Stacking >3 GNN layers causes embeddings to converge; use skip connections, JumpingKnowledge, or DropEdge
- **Neighbor explosion**: Without sampling, a 3-layer GNN on a power-law graph pulls millions of nodes; always use NeighborLoader for >100K nodes
- **Self-loops**: GCN requires self-loops (`add_self_loops=True`); forgetting this drops accuracy 5-15%
- **Feature scaling**: GNN layers are sensitive to feature scale; use BatchNorm or LayerNorm between layers
- **to_hetero lazy init**: Must call model with a real batch to trigger lazy init when using `in_channels=-1`
- **Negative sampling leakage**: Negatives must not include val/test edges; `RandomLinkSplit` handles this automatically
- **TransE symmetric relations**: TransE cannot model symmetric relations; use RotatE or DistMult for undirected graphs
- **GPU memory**: Large adjacency matrices don't fit on GPU; use `SparseTensor` from `torch_sparse` for >500K edges
