---
name: "cwicr-value-engineering"
description: "Perform value engineering analysis using CWICR data. Identify cost-saving alternatives while maintaining function and quality."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "🗄️", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---
# CWICR Value Engineering

## Business Case

### Problem Statement
Projects often exceed budget:
- Where can costs be reduced?
- What alternatives exist?
- How to maintain quality?
- Document VE decisions

### Solution
Systematic value engineering using CWICR data to identify cost-effective alternatives, analyze trade-offs, and document decisions.

### Business Value
- **Cost savings** - Identify reduction opportunities
- **Quality maintenance** - Function-based analysis
- **Documentation** - VE proposal records
- **Client value** - Optimize value for cost

## Technical Implementation

```python
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import date
from enum import Enum


class VECategory(Enum):
    """Value engineering categories."""
    MATERIAL = "material"
    METHOD = "method"
    DESIGN = "design"
    SPECIFICATION = "specification"
    SYSTEM = "system"


class VEStatus(Enum):
    """VE proposal status."""
    PROPOSED = "proposed"
    UNDER_REVIEW = "under_review"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    IMPLEMENTED = "implemented"


@dataclass
class VEProposal:
    """Value engineering proposal."""
    proposal_id: str
    title: str
    category: VECategory
    description: str
    original_item: str
    proposed_item: str
    original_cost: float
    proposed_cost: float
    savings: float
    savings_percent: float
    function_impact: str
    quality_impact: str
    schedule_impact: int
    risk_assessment: str
    status: VEStatus


@dataclass
class VEAnalysis:
    """Complete VE analysis."""
    project_name: str
    total_original_cost: float
    total_proposed_cost: float
    total_savings: float
    savings_percent: float
    proposals: List[VEProposal]
    accepted_savings: float
    pending_savings: float


class CWICRValueEngineering:
    """Value engineering analysis using CWICR data."""

    def __init__(self, cwicr_data: pd.DataFrame):
        self.cost_data = cwicr_data
        self._index_data()
        self._proposals: Dict[str, VEProposal] = {}

    def _index_data(self):
        """Index cost data."""
        if 'work_item_code' in self.cost_data.columns:
            self._code_index = self.cost_data.set_index('work_item_code')
        else:
            self._code_index = None

    def get_item_cost(self, code: str, quantity: float = 1) -> Tuple[float, Dict[str, float]]:
        """Get item cost breakdown."""
        if self._code_index is None or code not in self._code_index.index:
            return (0, {})

        item = self._code_index.loc[code]
        labor = float(item.get('labor_cost', 0) or 0) * quantity
        material = float(item.get('material_cost', 0) or 0) * quantity
        equipment = float(item.get('equipment_cost', 0) or 0) * quantity

        return (labor + material + equipment, {
            'labor': labor,
            'material': material,
            'equipment': equipment
        })

    def find_alternatives(self,
                          work_item_code: str,
                          quantity: float,
                          max_cost_increase: float = 0) -> List[Dict[str, Any]]:
        """Find alternative work items that could replace original."""

        original_cost, _ = self.get_item_cost(work_item_code, quantity)

        if self._code_index is None:
            return []

        # Get original item category
        if work_item_code in self._code_index.index:
            original = self._code_index.loc[work_item_code]
            category = str(original.get('category', '')).lower()
        else:
            return []

        alternatives = []

        for code, row in self._code_index.iterrows():
            if code == work_item_code:
                continue

            # Match by category prefix or similar category
            item_category = str(row.get('category', '')).lower()

            if category[:4] in item_category or item_category[:4] in category:
                alt_cost, breakdown = self.get_item_cost(code, quantity)

                if alt_cost <= original_cost * (1 + max_cost_increase):
                    savings = original_cost - alt_cost

                    alternatives.append({
                        'code': code,
                        'description': str(row.get('description', code)),
                        'cost': round(alt_cost, 2),
                        'savings': round(savings, 2),
                        'savings_pct': round(savings / original_cost * 100, 1) if original_cost > 0 else 0,
                        'breakdown': breakdown
                    })

        # Sort by savings
        return sorted(alternatives, key=lambda x: x['savings'], reverse=True)[:10]

    def create_proposal(self,
                        proposal_id: str,
                        title: str,
                        category: VECategory,
                        description: str,
                        original_item: str,
                        proposed_item: str,
                        quantity: float,
                        function_impact: str = "Equivalent",
                        quality_impact: str = "Equivalent",
                        schedule_impact: int = 0,
                        risk_assessment: str = "Low") -> VEProposal:
        """Create VE proposal."""

        original_cost, _ = self.get_item_cost(original_item, quantity)
        proposed_cost, _ = self.get_item_cost(proposed_item, quantity)

        savings = original_cost - proposed_cost
        savings_pct = (savings / original_cost * 100) if original_cost > 0 else 0

        proposal = VEProposal(
            proposal_id=proposal_id,
            title=title,
            category=category,
            description=description,
            original_item=original_item,
            proposed_item=proposed_item,
            original_cost=round(original_cost, 2),
            proposed_cost=round(proposed_cost, 2),
            savings=round(savings, 2),
            savings_percent=round(savings_pct, 1),
            function_impact=function_impact,
            quality_impact=quality_impact,
            schedule_impact=schedule_impact,
            risk_assessment=risk_assessment,
            status=VEStatus.PROPOSED
        )

        self._proposals[proposal_id] = proposal
        return proposal

    def update_status(self, proposal_id: str, status: VEStatus):
        """Update proposal status."""
        if proposal_id in self._proposals:
            self._proposals[proposal_id].status = status

    def identify_high_cost_items(self,
                                   items: List[Dict[str, Any]],
                                   top_n: int = 20,
                                   min_percentage: float = 2.0) -> List[Dict[str, Any]]:
        """Identify high-cost items for VE focus."""

        item_costs = []
        total_cost = 0

        for item in items:
            code = item.get('work_item_code', item.get('code'))
            qty = item.get('quantity', 0)
            cost, breakdown = self.get_item_cost(code, qty)

            item_costs.append({
                'code': code,
                'quantity': qty,
                'cost': cost,
                'breakdown': breakdown
            })
            total_cost += cost

        # Add percentage and sort
        for item in item_costs:
            item['percentage'] = round(item['cost'] / total_cost * 100, 2) if total_cost > 0 else 0

        # Filter and sort
        significant = [i for i in item_costs if i['percentage'] >= min_percentage]
        significant.sort(key=lambda x: x['cost'], reverse=True)

        return significant[:top_n]

    def analyze_material_alternatives(self,
                                       material_type: str,
                                       quantity: float) -> Dict[str, Any]:
        """Analyze alternative materials by type."""

        if self._code_index is None:
            return {}

        matches = []

        for code, row in self._code_index.iterrows():
            desc = str(row.get('description', '')).lower()
            if material_type.lower() in desc:
                cost, breakdown = self.get_item_cost(code, quantity)
                matches.append({
                    'code': code,
                    'description': str(row.get('description', code)),
                    'cost': cost,
                    'material_cost': breakdown.get('material', 0),
                    'unit': str(row.get('unit', 'unit'))
                })

        if not matches:
            return {}

        matches.sort(key=lambda x: x['cost'])

        cheapest = matches[0]
        most_expensive = matches[-1]

        return {
            'material_type': material_type,
            'quantity': quantity,
            'options_found': len(matches),
            'cheapest': cheapest,
            'most_expensive': most_expensive,
            'potential_savings': round(most_expensive['cost'] - cheapest['cost'], 2),
            'all_options': matches
        }

    def generate_ve_analysis(self, project_name: str) -> VEAnalysis:
        """Generate complete VE analysis."""

        proposals = list(self._proposals.values())

        total_original = sum(p.original_cost for p in proposals)
        total_proposed = sum(p.proposed_cost for p in proposals)
        total_savings = sum(p.savings for p in proposals)

        accepted_savings = sum(
            p.savings for p in proposals
            if p.status in [VEStatus.ACCEPTED, VEStatus.IMPLEMENTED]
        )

        pending_savings = sum(
            p.savings for p in proposals
            if p.status in [VEStatus.PROPOSED, VEStatus.UNDER_REVIEW]
        )

        return VEAnalysis(
            project_name=project_name,
            total_original_cost=round(total_original, 2),
            total_proposed_cost=round(total_proposed, 2),
            total_savings=round(total_savings, 2),
            savings_percent=round(total_savings / total_original * 100, 1) if total_original > 0 else 0,
            proposals=proposals,
            accepted_savings=round(accepted_savings, 2),
            pending_savings=round(pending_savings, 2)
        )

    def export_ve_report(self,
                          analysis: VEAnalysis,
                          output_path: str) -> str:
        """Export VE analysis to Excel."""

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Summary
            summary_df = pd.DataFrame([{
                'Project': analysis.project_name,
                'Total Original Cost': analysis.total_original_cost,
                'Total Proposed Cost': analysis.total_proposed_cost,
                'Total Savings': analysis.total_savings,
                'Savings %': analysis.savings_percent,
                'Accepted Savings': analysis.accepted_savings,
                'Pending Savings': analysis.pending_savings
            }])
            summary_df.to_excel(writer, sheet_name='Summary', index=False)

            # Proposals
            proposals_df = pd.DataFrame([
                {
                    'ID': p.proposal_id,
                    'Title': p.title,
                    'Category': p.category.value,
                    'Original Item': p.original_item,
                    'Proposed Item': p.proposed_item,
                    'Original Cost': p.original_cost,
                    'Proposed Cost': p.proposed_cost,
                    'Savings': p.savings,
                    'Savings %': p.savings_percent,
                    'Function Impact': p.function_impact,
                    'Quality Impact': p.quality_impact,
                    'Schedule Days': p.schedule_impact,
                    'Risk': p.risk_assessment,
                    'Status': p.status.value
                }
                for p in analysis.proposals
            ])
            proposals_df.to_excel(writer, sheet_name='Proposals', index=False)

        return output_path
```

## Quick Start

```python
# Load CWICR data
cwicr = pd.read_parquet("ddc_cwicr_en.parquet")

# Initialize VE analyzer
ve = CWICRValueEngineering(cwicr)

# Find alternatives for expensive item
alternatives = ve.find_alternatives(
    work_item_code="CONC-HIGH-001",
    quantity=100
)

for alt in alternatives[:3]:
    print(f"{alt['code']}: ${alt['savings']:,.2f} savings ({alt['savings_pct']}%)")
```

## Common Use Cases

### 1. Identify VE Opportunities
```python
items = [
    {'work_item_code': 'CONC-001', 'quantity': 200},
    {'work_item_code': 'STRL-002', 'quantity': 50}
]

high_cost = ve.identify_high_cost_items(items, top_n=10, min_percentage=5.0)
for item in high_cost:
    print(f"{item['code']}: ${item['cost']:,.2f} ({item['percentage']}%)")
```

### 2. Create VE Proposal
```python
proposal = ve.create_proposal(
    proposal_id="VE-001",
    title="Substitute concrete grade",
    category=VECategory.MATERIAL,
    description="Use C25 instead of C30 for non-structural elements",
    original_item="CONC-C30-001",
    proposed_item="CONC-C25-001",
    quantity=150,
    function_impact="Equivalent for intended use",
    quality_impact="Meets specification",
    risk_assessment="Low"
)

print(f"Potential Savings: ${proposal.savings:,.2f}")
```

### 3. Generate VE Report
```python
analysis = ve.generate_ve_analysis("Building Project")
ve.export_ve_report(analysis, "ve_analysis.xlsx")
```

## Resources
- **GitHub**: [OpenConstructionEstimate-DDC-CWICR](https://github.com/datadrivenconstruction/OpenConstructionEstimate-DDC-CWICR)
- **DDC Book**: Chapter 3.2 - Value Engineering
