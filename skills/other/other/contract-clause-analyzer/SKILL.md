---
name: "contract-clause-analyzer"
description: "Analyze construction contract clauses. Identify risks, obligations, and key terms using NLP."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "📋", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---
# Contract Clause Analyzer

## Business Case

### Problem Statement
Contract review is time-consuming and error-prone:
- Important clauses missed
- Risk provisions overlooked
- Inconsistent interpretation
- Long review cycles

### Solution
AI-assisted contract clause analysis that identifies key provisions, flags risks, and extracts critical terms.

## Technical Implementation

```python
import pandas as pd
from datetime import datetime, date
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from enum import Enum
import re


class ClauseType(Enum):
    SCOPE = "scope"
    PAYMENT = "payment"
    SCHEDULE = "schedule"
    CHANGE_ORDER = "change_order"
    TERMINATION = "termination"
    INDEMNIFICATION = "indemnification"
    INSURANCE = "insurance"
    WARRANTY = "warranty"
    DISPUTE = "dispute"
    LIABILITY = "liability"
    FORCE_MAJEURE = "force_majeure"
    SAFETY = "safety"
    COMPLIANCE = "compliance"
    OTHER = "other"


class RiskLevel(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


@dataclass
class ContractClause:
    clause_id: str
    section: str
    title: str
    text: str
    clause_type: ClauseType
    risk_level: RiskLevel
    key_terms: List[str] = field(default_factory=list)
    obligations: List[str] = field(default_factory=list)
    deadlines: List[str] = field(default_factory=list)
    amounts: List[str] = field(default_factory=list)
    notes: str = ""


@dataclass
class AnalysisResult:
    contract_name: str
    analyzed_date: datetime
    total_clauses: int
    clauses: List[ContractClause]
    risk_summary: Dict[str, int]
    key_dates: List[Dict[str, str]]
    key_amounts: List[Dict[str, str]]


class ContractClauseAnalyzer:
    """Analyze construction contract clauses."""

    RISK_KEYWORDS = {
        'high': ['indemnify', 'sole discretion', 'waive', 'forfeit', 'liquidated damages',
                 'consequential', 'unlimited liability', 'hold harmless', 'no limit'],
        'medium': ['shall', 'must', 'required', 'obligated', 'responsible', 'liable',
                   'penalty', 'default', 'breach'],
        'low': ['may', 'should', 'reasonable', 'mutual', 'consent', 'approval']
    }

    CLAUSE_PATTERNS = {
        ClauseType.PAYMENT: ['payment', 'invoice', 'retainage', 'progress payment'],
        ClauseType.SCHEDULE: ['schedule', 'completion date', 'milestone', 'time is of the essence'],
        ClauseType.CHANGE_ORDER: ['change order', 'modification', 'additional work', 'variation'],
        ClauseType.TERMINATION: ['termination', 'terminate', 'cancellation'],
        ClauseType.INDEMNIFICATION: ['indemnif', 'hold harmless', 'defend'],
        ClauseType.INSURANCE: ['insurance', 'coverage', 'policy', 'insured'],
        ClauseType.WARRANTY: ['warranty', 'guarantee', 'defect', 'workmanship'],
        ClauseType.DISPUTE: ['dispute', 'arbitration', 'mediation', 'litigation'],
        ClauseType.LIABILITY: ['liability', 'damages', 'limitation'],
        ClauseType.FORCE_MAJEURE: ['force majeure', 'act of god', 'unforeseen'],
    }

    def __init__(self):
        self.clauses: List[ContractClause] = []

    def analyze_text(self, contract_name: str, text: str) -> AnalysisResult:
        """Analyze contract text."""
        self.clauses = []

        # Split into sections/clauses
        sections = self._split_into_sections(text)

        for i, section in enumerate(sections):
            clause = self._analyze_clause(f"CL-{i+1:03d}", section)
            self.clauses.append(clause)

        # Generate summary
        risk_summary = {
            'high': sum(1 for c in self.clauses if c.risk_level == RiskLevel.HIGH),
            'medium': sum(1 for c in self.clauses if c.risk_level == RiskLevel.MEDIUM),
            'low': sum(1 for c in self.clauses if c.risk_level == RiskLevel.LOW)
        }

        key_dates = []
        key_amounts = []
        for clause in self.clauses:
            for d in clause.deadlines:
                key_dates.append({'clause': clause.clause_id, 'date': d})
            for a in clause.amounts:
                key_amounts.append({'clause': clause.clause_id, 'amount': a})

        return AnalysisResult(
            contract_name=contract_name,
            analyzed_date=datetime.now(),
            total_clauses=len(self.clauses),
            clauses=self.clauses,
            risk_summary=risk_summary,
            key_dates=key_dates,
            key_amounts=key_amounts
        )

    def _split_into_sections(self, text: str) -> List[Dict[str, str]]:
        """Split contract into sections."""
        sections = []
        # Simple split by numbered sections
        pattern = r'(\d+\.[\d\.]*\s+[A-Z][^\.]+)'
        parts = re.split(pattern, text)

        current_title = ""
        for i, part in enumerate(parts):
            if re.match(r'\d+\.[\d\.]*\s+[A-Z]', part):
                current_title = part.strip()
            elif part.strip() and current_title:
                sections.append({
                    'title': current_title,
                    'text': part.strip()
                })
                current_title = ""

        # If no sections found, treat whole text as one
        if not sections and text.strip():
            sections.append({'title': 'Contract Text', 'text': text.strip()})

        return sections

    def _analyze_clause(self, clause_id: str, section: Dict[str, str]) -> ContractClause:
        """Analyze single clause."""
        text = section.get('text', '')
        title = section.get('title', '')
        text_lower = text.lower()

        # Determine clause type
        clause_type = self._determine_type(text_lower)

        # Assess risk level
        risk_level = self._assess_risk(text_lower)

        # Extract key terms
        key_terms = self._extract_key_terms(text)

        # Extract obligations
        obligations = self._extract_obligations(text)

        # Extract dates
        deadlines = self._extract_dates(text)

        # Extract amounts
        amounts = self._extract_amounts(text)

        return ContractClause(
            clause_id=clause_id,
            section=clause_id,
            title=title,
            text=text[:500] + "..." if len(text) > 500 else text,
            clause_type=clause_type,
            risk_level=risk_level,
            key_terms=key_terms,
            obligations=obligations,
            deadlines=deadlines,
            amounts=amounts
        )

    def _determine_type(self, text: str) -> ClauseType:
        """Determine clause type from content."""
        for clause_type, keywords in self.CLAUSE_PATTERNS.items():
            if any(kw in text for kw in keywords):
                return clause_type
        return ClauseType.OTHER

    def _assess_risk(self, text: str) -> RiskLevel:
        """Assess risk level of clause."""
        high_count = sum(1 for kw in self.RISK_KEYWORDS['high'] if kw in text)
        medium_count = sum(1 for kw in self.RISK_KEYWORDS['medium'] if kw in text)

        if high_count >= 2:
            return RiskLevel.HIGH
        elif high_count >= 1 or medium_count >= 3:
            return RiskLevel.MEDIUM
        elif medium_count >= 1:
            return RiskLevel.LOW
        return RiskLevel.INFO

    def _extract_key_terms(self, text: str) -> List[str]:
        """Extract key defined terms."""
        # Look for quoted terms or capitalized multi-word phrases
        patterns = [
            r'"([^"]+)"',
            r"'([^']+)'",
            r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\b'
        ]
        terms = []
        for pattern in patterns:
            matches = re.findall(pattern, text)
            terms.extend(matches[:5])
        return list(set(terms))[:10]

    def _extract_obligations(self, text: str) -> List[str]:
        """Extract obligation statements."""
        patterns = [
            r'(?:contractor|owner|party)\s+shall\s+([^\.]+)',
            r'(?:contractor|owner|party)\s+must\s+([^\.]+)',
            r'(?:contractor|owner|party)\s+is\s+(?:required|obligated)\s+to\s+([^\.]+)'
        ]
        obligations = []
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            obligations.extend(matches[:3])
        return obligations[:5]

    def _extract_dates(self, text: str) -> List[str]:
        """Extract date references."""
        patterns = [
            r'\b\d{1,2}/\d{1,2}/\d{2,4}\b',
            r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b',
            r'\b\d+\s+(?:calendar|working|business)\s+days\b',
            r'\bwithin\s+\d+\s+days\b'
        ]
        dates = []
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            dates.extend(matches)
        return dates[:5]

    def _extract_amounts(self, text: str) -> List[str]:
        """Extract monetary amounts."""
        patterns = [
            r'\$[\d,]+(?:\.\d{2})?',
            r'\b\d+(?:,\d{3})*(?:\.\d{2})?\s*(?:dollars|USD)\b',
            r'\b\d+(?:\.\d+)?%\b'
        ]
        amounts = []
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            amounts.extend(matches)
        return amounts[:5]

    def get_high_risk_clauses(self) -> List[ContractClause]:
        """Get all high-risk clauses."""
        return [c for c in self.clauses if c.risk_level == RiskLevel.HIGH]

    def export_analysis(self, result: AnalysisResult, output_path: str):
        """Export analysis to Excel."""
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Summary
            summary_df = pd.DataFrame([{
                'Contract': result.contract_name,
                'Analyzed': result.analyzed_date,
                'Total Clauses': result.total_clauses,
                'High Risk': result.risk_summary['high'],
                'Medium Risk': result.risk_summary['medium'],
                'Low Risk': result.risk_summary['low']
            }])
            summary_df.to_excel(writer, sheet_name='Summary', index=False)

            # Clauses
            clause_data = [{
                'ID': c.clause_id,
                'Title': c.title[:50],
                'Type': c.clause_type.value,
                'Risk': c.risk_level.value,
                'Key Terms': ', '.join(c.key_terms[:3]),
                'Obligations': len(c.obligations),
                'Dates': ', '.join(c.deadlines[:2]),
                'Amounts': ', '.join(c.amounts[:2])
            } for c in result.clauses]
            pd.DataFrame(clause_data).to_excel(writer, sheet_name='Clauses', index=False)

        return output_path
```

## Quick Start

```python
analyzer = ContractClauseAnalyzer()

# Analyze contract text
contract_text = open("contract.txt").read()
result = analyzer.analyze_text("Construction Contract", contract_text)

print(f"High risk clauses: {result.risk_summary['high']}")

# Get risky clauses
high_risk = analyzer.get_high_risk_clauses()
for clause in high_risk:
    print(f"{clause.clause_id}: {clause.title}")
```

## Resources
- **DDC Book**: Chapter 5 - Contract Management
