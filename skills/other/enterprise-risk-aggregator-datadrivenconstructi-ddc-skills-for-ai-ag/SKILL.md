---
slug: "enterprise-risk-aggregator"
display_name: "Enterprise Risk Aggregator"
description: "Aggregate and analyze risks across construction project portfolio. Identify correlated risks, systemic exposures, and portfolio-level risk mitigation strategies."
---

# Enterprise Risk Aggregator

## Overview

Aggregate individual project risks into a portfolio-level view. Identify correlated risks across projects, calculate enterprise risk exposure, and develop portfolio-wide mitigation strategies.

## Risk Aggregation Framework

```
┌─────────────────────────────────────────────────────────────────┐
│                ENTERPRISE RISK AGGREGATION                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  PROJECT RISKS           CORRELATION            PORTFOLIO VIEW  │
│  ─────────────           ───────────            ──────────────  │
│                                                                  │
│  Project A:              Market risks ←→        Total Exposure: │
│  • Material cost ↗       affect all             $45M            │
│  • Labor shortage        projects               ─────────────── │
│                                    ↓            Risk Categories:│
│  Project B:              Weather impacts        • Market: 35%   │
│  • Weather delay         multiple sites         • Schedule: 25% │
│  • Permit issue                    ↓            • Safety: 15%   │
│                          Supply chain           • Regulatory:15%│
│  Project C:              affects                • Technical:10% │
│  • Subcontractor ↗       entire region          ─────────────── │
│  • Design change                                Top 5 Risks:    │
│                                                 1. Steel prices │
│                                                 2. Labor market │
│                                                 3. Supply chain │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Technical Implementation

```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Set
from datetime import datetime, timedelta
from enum import Enum
import statistics
import math

class RiskCategory(Enum):
    MARKET = "market"
    SCHEDULE = "schedule"
    SAFETY = "safety"
    REGULATORY = "regulatory"
    TECHNICAL = "technical"
    FINANCIAL = "financial"
    ENVIRONMENTAL = "environmental"
    SUPPLY_CHAIN = "supply_chain"
    LABOR = "labor"
    WEATHER = "weather"

class RiskLevel(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

class CorrelationType(Enum):
    POSITIVE = "positive"      # Risks tend to occur together
    NEGATIVE = "negative"      # One risk may offset another
    INDEPENDENT = "independent"

@dataclass
class ProjectRisk:
    id: str
    project_id: str
    project_name: str
    category: RiskCategory
    description: str
    probability: float  # 0-1
    impact: float       # Dollar amount
    score: float = 0.0  # P x I
    level: RiskLevel = RiskLevel.MEDIUM
    status: str = "open"
    mitigation: str = ""
    triggers: List[str] = field(default_factory=list)

    def __post_init__(self):
        self.score = self.probability * self.impact
        if self.score > 5000000:
            self.level = RiskLevel.CRITICAL
        elif self.score > 1000000:
            self.level = RiskLevel.HIGH
        elif self.score > 250000:
            self.level = RiskLevel.MEDIUM
        else:
            self.level = RiskLevel.LOW

@dataclass
class RiskCorrelation:
    risk1_id: str
    risk2_id: str
    correlation_type: CorrelationType
    strength: float  # 0-1
    shared_triggers: List[str]
    notes: str = ""

@dataclass
class AggregatedRisk:
    category: RiskCategory
    total_exposure: float
    expected_loss: float
    worst_case: float
    risk_count: int
    projects_affected: int
    mitigation_cost: float
    residual_exposure: float

@dataclass
class PortfolioRiskProfile:
    report_date: datetime
    total_projects: int
    total_risks: int
    total_exposure: float
    expected_loss: float
    var_95: float  # Value at Risk at 95% confidence
    by_category: Dict[str, AggregatedRisk]
    top_risks: List[ProjectRisk]
    correlations: List[RiskCorrelation]
    systemic_risks: List[str]

class EnterpriseRiskAggregator:
    """Aggregate risks across project portfolio."""

    # Common triggers that create correlation
    SYSTEMIC_TRIGGERS = [
        "steel_price_increase",
        "labor_shortage",
        "supply_chain_disruption",
        "interest_rate_change",
        "regulatory_change",
        "weather_event",
        "economic_downturn",
        "pandemic",
        "trade_restrictions"
    ]

    def __init__(self, portfolio_name: str):
        self.portfolio_name = portfolio_name
        self.risks: Dict[str, ProjectRisk] = {}
        self.correlations: List[RiskCorrelation] = []
        self.projects: Set[str] = set()

    def add_risk(self, project_id: str, project_name: str,
                category: RiskCategory, description: str,
                probability: float, impact: float,
                triggers: List[str] = None,
                mitigation: str = "") -> ProjectRisk:
        """Add project risk to portfolio."""
        risk_id = f"RISK-{project_id}-{len(self.risks)+1:04d}"

        risk = ProjectRisk(
            id=risk_id,
            project_id=project_id,
            project_name=project_name,
            category=category,
            description=description,
            probability=probability,
            impact=impact,
            triggers=triggers or [],
            mitigation=mitigation
        )

        self.risks[risk_id] = risk
        self.projects.add(project_id)

        return risk

    def import_project_risks(self, project_id: str, project_name: str,
                            risks: List[Dict]) -> int:
        """Import risks from project risk register."""
        count = 0
        for r in risks:
            self.add_risk(
                project_id=project_id,
                project_name=project_name,
                category=RiskCategory(r['category']),
                description=r['description'],
                probability=r['probability'],
                impact=r['impact'],
                triggers=r.get('triggers', []),
                mitigation=r.get('mitigation', '')
            )
            count += 1
        return count

    def detect_correlations(self) -> List[RiskCorrelation]:
        """Automatically detect correlated risks."""
        self.correlations = []
        risks = list(self.risks.values())

        for i, risk1 in enumerate(risks):
            for risk2 in risks[i+1:]:
                # Check for shared triggers
                shared = set(risk1.triggers) & set(risk2.triggers)

                if shared:
                    # Calculate correlation strength
                    total_triggers = len(set(risk1.triggers) | set(risk2.triggers))
                    strength = len(shared) / total_triggers if total_triggers > 0 else 0

                    correlation = RiskCorrelation(
                        risk1_id=risk1.id,
                        risk2_id=risk2.id,
                        correlation_type=CorrelationType.POSITIVE,
                        strength=strength,
                        shared_triggers=list(shared)
                    )
                    self.correlations.append(correlation)

                # Check for same category across projects
                elif (risk1.category == risk2.category and
                      risk1.project_id != risk2.project_id):
                    correlation = RiskCorrelation(
                        risk1_id=risk1.id,
                        risk2_id=risk2.id,
                        correlation_type=CorrelationType.POSITIVE,
                        strength=0.3,  # Weak assumed correlation
                        shared_triggers=[],
                        notes=f"Same category: {risk1.category.value}"
                    )
                    self.correlations.append(correlation)

        return self.correlations

    def identify_systemic_risks(self) -> List[Dict]:
        """Identify systemic risks affecting multiple projects."""
        systemic = []

        # Count triggers across all risks
        trigger_count: Dict[str, Set[str]] = {}
        for risk in self.risks.values():
            for trigger in risk.triggers:
                if trigger not in trigger_count:
                    trigger_count[trigger] = set()
                trigger_count[trigger].add(risk.project_id)

        # Systemic if affects multiple projects
        for trigger, projects in trigger_count.items():
            if len(projects) > 1:
                # Calculate total exposure
                affected_risks = [r for r in self.risks.values()
                                 if trigger in r.triggers]
                total_exposure = sum(r.score for r in affected_risks)

                systemic.append({
                    "trigger": trigger,
                    "projects_affected": len(projects),
                    "risks_affected": len(affected_risks),
                    "total_exposure": total_exposure,
                    "is_systemic": trigger in self.SYSTEMIC_TRIGGERS
                })

        return sorted(systemic, key=lambda x: -x['total_exposure'])

    def aggregate_by_category(self) -> Dict[RiskCategory, AggregatedRisk]:
        """Aggregate risks by category."""
        by_category = {}

        for category in RiskCategory:
            cat_risks = [r for r in self.risks.values() if r.category == category]

            if not cat_risks:
                continue

            projects = set(r.project_id for r in cat_risks)

            # Simple aggregation (no correlation adjustment)
            total_exposure = sum(r.impact for r in cat_risks)
            expected_loss = sum(r.score for r in cat_risks)

            # Worst case assuming all materialize
            worst_case = total_exposure

            by_category[category] = AggregatedRisk(
                category=category,
                total_exposure=total_exposure,
                expected_loss=expected_loss,
                worst_case=worst_case,
                risk_count=len(cat_risks),
                projects_affected=len(projects),
                mitigation_cost=0,
                residual_exposure=expected_loss
            )

        return by_category

    def calculate_var(self, confidence: float = 0.95,
                     simulations: int = 10000) -> float:
        """Calculate Value at Risk using Monte Carlo simulation."""
        import random

        losses = []
        risks = list(self.risks.values())

        for _ in range(simulations):
            sim_loss = 0
            for risk in risks:
                if random.random() < risk.probability:
                    sim_loss += risk.impact
            losses.append(sim_loss)

        losses.sort()
        var_index = int(simulations * confidence)
        return losses[var_index]

    def generate_portfolio_profile(self) -> PortfolioRiskProfile:
        """Generate comprehensive portfolio risk profile."""
        if not self.correlations:
            self.detect_correlations()

        total_exposure = sum(r.impact for r in self.risks.values())
        expected_loss = sum(r.score for r in self.risks.values())

        by_category = self.aggregate_by_category()

        # Top risks by score
        top_risks = sorted(self.risks.values(), key=lambda x: -x.score)[:10]

        # Systemic risks
        systemic = self.identify_systemic_risks()
        systemic_triggers = [s['trigger'] for s in systemic if s['is_systemic']]

        # VaR calculation
        var_95 = self.calculate_var(0.95)

        return PortfolioRiskProfile(
            report_date=datetime.now(),
            total_projects=len(self.projects),
            total_risks=len(self.risks),
            total_exposure=total_exposure,
            expected_loss=expected_loss,
            var_95=var_95,
            by_category={k.value: v for k, v in by_category.items()},
            top_risks=top_risks,
            correlations=self.correlations,
            systemic_risks=systemic_triggers
        )

    def suggest_mitigation_priorities(self) -> List[Dict]:
        """Suggest prioritized mitigation actions."""
        priorities = []

        # Systemic risks first
        systemic = self.identify_systemic_risks()
        for s in systemic[:5]:
            if s['is_systemic']:
                priorities.append({
                    "priority": 1,
                    "type": "systemic",
                    "target": s['trigger'],
                    "exposure": s['total_exposure'],
                    "projects": s['projects_affected'],
                    "recommendation": f"Portfolio-wide mitigation for {s['trigger']}"
                })

        # High-correlation risks
        high_corr = [c for c in self.correlations if c.strength > 0.5]
        for corr in high_corr[:5]:
            r1 = self.risks.get(corr.risk1_id)
            r2 = self.risks.get(corr.risk2_id)
            if r1 and r2:
                priorities.append({
                    "priority": 2,
                    "type": "correlated",
                    "target": f"{r1.description[:30]} / {r2.description[:30]}",
                    "exposure": r1.score + r2.score,
                    "projects": 2,
                    "recommendation": f"Joint mitigation via {corr.shared_triggers}"
                })

        # Individual high-impact risks
        top_risks = sorted(self.risks.values(), key=lambda x: -x.score)[:10]
        for risk in top_risks:
            if not any(p['target'].startswith(risk.description[:20]) for p in priorities):
                priorities.append({
                    "priority": 3,
                    "type": "individual",
                    "target": risk.description[:50],
                    "exposure": risk.score,
                    "projects": 1,
                    "recommendation": risk.mitigation or "Develop mitigation plan"
                })

        return sorted(priorities, key=lambda x: (x['priority'], -x['exposure']))

    def generate_report(self) -> str:
        """Generate enterprise risk report."""
        profile = self.generate_portfolio_profile()

        lines = [
            "# Enterprise Risk Aggregation Report",
            "",
            f"**Portfolio:** {self.portfolio_name}",
            f"**Report Date:** {profile.report_date.strftime('%Y-%m-%d')}",
            "",
            "## Executive Summary",
            "",
            f"| Metric | Value |",
            f"|--------|-------|",
            f"| Total Projects | {profile.total_projects} |",
            f"| Total Risks | {profile.total_risks} |",
            f"| Total Exposure | ${profile.total_exposure:,.0f} |",
            f"| Expected Loss | ${profile.expected_loss:,.0f} |",
            f"| VaR (95%) | ${profile.var_95:,.0f} |",
            "",
            "## Risk Distribution by Category",
            "",
            "| Category | Risks | Projects | Expected Loss | % of Total |",
            "|----------|-------|----------|---------------|------------|"
        ]

        for cat, agg in profile.by_category.items():
            pct = (agg.expected_loss / profile.expected_loss * 100) if profile.expected_loss > 0 else 0
            lines.append(
                f"| {cat} | {agg.risk_count} | {agg.projects_affected} | "
                f"${agg.expected_loss:,.0f} | {pct:.1f}% |"
            )

        # Systemic risks
        if profile.systemic_risks:
            lines.extend([
                "",
                "## Systemic Risks (Portfolio-Wide)",
                ""
            ])
            for trigger in profile.systemic_risks[:5]:
                lines.append(f"- **{trigger}**")

        # Top individual risks
        lines.extend([
            "",
            "## Top 10 Individual Risks",
            "",
            "| Project | Risk | Prob | Impact | Score |",
            "|---------|------|------|--------|-------|"
        ])

        for risk in profile.top_risks:
            lines.append(
                f"| {risk.project_name} | {risk.description[:30]} | "
                f"{risk.probability:.0%} | ${risk.impact:,.0f} | ${risk.score:,.0f} |"
            )

        # Correlations
        high_corr = [c for c in profile.correlations if c.strength > 0.3]
        if high_corr:
            lines.extend([
                "",
                f"## Risk Correlations ({len(high_corr)} significant)",
                "",
                "| Strength | Shared Triggers |",
                "|----------|-----------------|"
            ])
            for c in high_corr[:10]:
                lines.append(
                    f"| {c.strength:.0%} | {', '.join(c.shared_triggers[:3])} |"
                )

        return "\n".join(lines)
```

## Quick Start

```python
# Initialize aggregator
aggregator = EnterpriseRiskAggregator("Regional Portfolio")

# Add risks from Project A
aggregator.add_risk(
    "PRJ-A", "Downtown Tower",
    RiskCategory.MARKET, "Steel price increase",
    probability=0.7, impact=2000000,
    triggers=["steel_price_increase", "trade_restrictions"]
)
aggregator.add_risk(
    "PRJ-A", "Downtown Tower",
    RiskCategory.LABOR, "Skilled labor shortage",
    probability=0.5, impact=1500000,
    triggers=["labor_shortage"]
)

# Add risks from Project B
aggregator.add_risk(
    "PRJ-B", "Hospital Wing",
    RiskCategory.MARKET, "Material cost escalation",
    probability=0.6, impact=1800000,
    triggers=["steel_price_increase", "supply_chain_disruption"]
)
aggregator.add_risk(
    "PRJ-B", "Hospital Wing",
    RiskCategory.SCHEDULE, "Weather delays",
    probability=0.4, impact=500000,
    triggers=["weather_event"]
)

# Detect correlations
correlations = aggregator.detect_correlations()
print(f"Found {len(correlations)} correlated risk pairs")

# Identify systemic risks
systemic = aggregator.identify_systemic_risks()
for s in systemic[:3]:
    print(f"Systemic: {s['trigger']} affects {s['projects_affected']} projects")

# Generate portfolio profile
profile = aggregator.generate_portfolio_profile()
print(f"Total Exposure: ${profile.total_exposure:,.0f}")
print(f"VaR (95%): ${profile.var_95:,.0f}")

# Get mitigation priorities
priorities = aggregator.suggest_mitigation_priorities()
for p in priorities[:5]:
    print(f"Priority {p['priority']}: {p['recommendation']}")

# Generate report
print(aggregator.generate_report())
```

## Requirements

```bash
pip install (no external dependencies)
```
