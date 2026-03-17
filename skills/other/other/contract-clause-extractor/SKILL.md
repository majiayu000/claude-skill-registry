---
name: "contract-clause-extractor"
description: "Extract and analyze key clauses from construction contracts. Identify payment terms, change order procedures, dispute resolution, warranties, and risk allocation provisions."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "📝", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---
# Contract Clause Extractor

## Overview

Extract and analyze key clauses from construction contracts using NLP. Identify critical provisions for payment, changes, disputes, warranties, and risk allocation. Support contract review and compliance tracking.

## Key Clause Categories

```
┌─────────────────────────────────────────────────────────────────┐
│                 CONTRACT CLAUSE CATEGORIES                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Payment           Changes            Risk                       │
│  ───────           ───────            ────                       │
│  📅 Pay schedule   📝 CO process      ⚠️ Indemnification        │
│  💰 Retainage      ⏰ Notice period   🔒 Insurance              │
│  📋 Requirements   💵 Pricing         🏛️ Liability limits       │
│                                                                  │
│  Schedule          Disputes           Closeout                   │
│  ────────          ────────           ────────                   │
│  📆 Milestones     ⚖️ Resolution      ✅ Punch list             │
│  💸 Liquidated $   🏛️ Jurisdiction    📄 Warranties             │
│  ⏱️ Extensions     👤 Mediation       🔑 Final payment          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Technical Implementation

```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum
import re

class ClauseCategory(Enum):
    PAYMENT = "payment"
    CHANGE_ORDER = "change_order"
    SCHEDULE = "schedule"
    DISPUTE = "dispute"
    INSURANCE = "insurance"
    WARRANTY = "warranty"
    TERMINATION = "termination"
    INDEMNIFICATION = "indemnification"
    SAFETY = "safety"
    CLOSEOUT = "closeout"

class RiskLevel(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

@dataclass
class ExtractedClause:
    category: ClauseCategory
    article_number: str
    title: str
    full_text: str
    key_terms: List[str]
    dollar_amounts: List[float]
    time_periods: List[str]
    risk_level: RiskLevel
    notes: str = ""

@dataclass
class ContractSummary:
    contract_type: str
    parties: Dict[str, str]
    contract_value: float
    duration_days: int
    start_date: str
    key_dates: Dict[str, str]
    clauses_by_category: Dict[str, List[ExtractedClause]]
    risk_assessment: Dict[str, str]
    action_items: List[str]

class ContractClauseExtractor:
    """Extract key clauses from construction contracts."""

    # Patterns for clause identification
    CLAUSE_PATTERNS = {
        ClauseCategory.PAYMENT: [
            r"payment\s+(terms|schedule|application)",
            r"progress\s+payment",
            r"retainage|retention",
            r"pay\s+when\s+paid",
            r"pay\s+if\s+paid",
            r"final\s+payment",
        ],
        ClauseCategory.CHANGE_ORDER: [
            r"change\s+order",
            r"change\s+directive",
            r"modifications?\s+to\s+contract",
            r"extra\s+work",
            r"changes\s+in\s+the\s+work",
        ],
        ClauseCategory.SCHEDULE: [
            r"time\s+of\s+completion",
            r"liquidated\s+damages",
            r"delay|extension\s+of\s+time",
            r"substantial\s+completion",
            r"schedule\s+of\s+values",
            r"milestone",
        ],
        ClauseCategory.DISPUTE: [
            r"dispute\s+resolution",
            r"mediation",
            r"arbitration",
            r"claims?\s+procedures?",
            r"litigation",
            r"governing\s+law",
        ],
        ClauseCategory.INSURANCE: [
            r"insurance\s+requirements?",
            r"builder'?s?\s+risk",
            r"general\s+liability",
            r"professional\s+liability",
            r"workers'?\s+compensation",
        ],
        ClauseCategory.WARRANTY: [
            r"warranty|warranties",
            r"guarantee",
            r"correction\s+of\s+work",
            r"defect",
        ],
        ClauseCategory.INDEMNIFICATION: [
            r"indemnif",
            r"hold\s+harmless",
            r"defend",
            r"limitation\s+of\s+liability",
        ],
        ClauseCategory.TERMINATION: [
            r"termination",
            r"suspension\s+of\s+work",
            r"default",
            r"for\s+cause|for\s+convenience",
        ],
    }

    # Key terms to extract
    KEY_TERM_PATTERNS = {
        "dollar_amounts": r'\$[\d,]+(?:\.\d{2})?|\d+(?:,\d{3})*\s*dollars',
        "percentages": r'\d+(?:\.\d+)?%',
        "time_periods": r'\d+\s*(?:days?|weeks?|months?|years?|business\s+days?|calendar\s+days?)',
        "notice_periods": r'(?:within|not\s+(?:less|more)\s+than)\s+\d+\s*(?:days?|hours?)',
    }

    def __init__(self):
        self.extracted_clauses: List[ExtractedClause] = []

    def extract_clauses(self, contract_text: str) -> List[ExtractedClause]:
        """Extract all identifiable clauses from contract text."""
        self.extracted_clauses = []

        # Split into articles/sections
        sections = self._split_into_sections(contract_text)

        for section_num, section_text in sections.items():
            # Identify clause category
            category = self._identify_category(section_text)

            if category:
                clause = self._extract_clause_details(
                    category, section_num, section_text
                )
                self.extracted_clauses.append(clause)

        return self.extracted_clauses

    def _split_into_sections(self, text: str) -> Dict[str, str]:
        """Split contract into numbered sections."""
        sections = {}

        # Pattern for article/section headers
        header_pattern = r'(?:ARTICLE|SECTION|Article|Section)\s+(\d+(?:\.\d+)?)[:\.]?\s*([A-Z][A-Za-z\s]+)?'

        parts = re.split(header_pattern, text)

        current_num = "0"
        current_text = ""

        for i, part in enumerate(parts):
            if re.match(r'^\d+(?:\.\d+)?$', part.strip()):
                if current_text:
                    sections[current_num] = current_text
                current_num = part.strip()
                current_text = ""
            else:
                current_text += part

        if current_text:
            sections[current_num] = current_text

        return sections

    def _identify_category(self, text: str) -> Optional[ClauseCategory]:
        """Identify clause category from text."""
        text_lower = text.lower()

        for category, patterns in self.CLAUSE_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    return category

        return None

    def _extract_clause_details(self, category: ClauseCategory,
                               section_num: str, text: str) -> ExtractedClause:
        """Extract detailed information from clause."""
        # Extract title (first line or capitalized phrase)
        title_match = re.search(r'^([A-Z][A-Z\s]+)', text.strip())
        title = title_match.group(1).strip() if title_match else f"Section {section_num}"

        # Extract dollar amounts
        dollar_amounts = []
        for match in re.finditer(self.KEY_TERM_PATTERNS["dollar_amounts"], text):
            amount_str = match.group().replace('$', '').replace(',', '').replace('dollars', '').strip()
            try:
                dollar_amounts.append(float(amount_str))
            except ValueError:
                pass

        # Extract time periods
        time_periods = re.findall(self.KEY_TERM_PATTERNS["time_periods"], text, re.IGNORECASE)

        # Extract key terms
        key_terms = self._extract_key_terms(category, text)

        # Assess risk level
        risk_level = self._assess_risk(category, text)

        return ExtractedClause(
            category=category,
            article_number=section_num,
            title=title,
            full_text=text[:2000],  # Limit length
            key_terms=key_terms,
            dollar_amounts=dollar_amounts,
            time_periods=time_periods,
            risk_level=risk_level
        )

    def _extract_key_terms(self, category: ClauseCategory, text: str) -> List[str]:
        """Extract key terms relevant to clause category."""
        key_terms = []
        text_lower = text.lower()

        category_terms = {
            ClauseCategory.PAYMENT: ["net 30", "net 45", "net 60", "retainage", "pay when paid", "pay if paid", "lien waiver"],
            ClauseCategory.CHANGE_ORDER: ["written notice", "equitable adjustment", "constructive change", "time extension"],
            ClauseCategory.SCHEDULE: ["liquidated damages", "substantial completion", "final completion", "float", "concurrent delay"],
            ClauseCategory.DISPUTE: ["mediation", "arbitration", "binding", "non-binding", "venue", "jurisdiction"],
            ClauseCategory.INSURANCE: ["additional insured", "primary coverage", "waiver of subrogation", "occurrence form"],
            ClauseCategory.WARRANTY: ["one year", "two year", "workmanship", "materials", "manufacturer"],
            ClauseCategory.INDEMNIFICATION: ["broad form", "intermediate form", "limited form", "negligence", "gross negligence"],
        }

        for term in category_terms.get(category, []):
            if term in text_lower:
                key_terms.append(term)

        return key_terms

    def _assess_risk(self, category: ClauseCategory, text: str) -> RiskLevel:
        """Assess risk level of clause."""
        text_lower = text.lower()

        high_risk_indicators = [
            "sole discretion",
            "waive",
            "release",
            "indemnify and hold harmless",
            "consequential damages",
            "no limitation",
            "pay if paid",
            "broad form indemnification",
        ]

        medium_risk_indicators = [
            "may require",
            "reasonable",
            "mutual",
            "good faith",
        ]

        high_count = sum(1 for ind in high_risk_indicators if ind in text_lower)
        medium_count = sum(1 for ind in medium_risk_indicators if ind in text_lower)

        if high_count >= 2:
            return RiskLevel.HIGH
        elif high_count >= 1 or medium_count >= 2:
            return RiskLevel.MEDIUM
        return RiskLevel.LOW

    def generate_summary(self, contract_text: str) -> ContractSummary:
        """Generate comprehensive contract summary."""
        clauses = self.extract_clauses(contract_text)

        # Group clauses by category
        clauses_by_category = {}
        for clause in clauses:
            cat = clause.category.value
            if cat not in clauses_by_category:
                clauses_by_category[cat] = []
            clauses_by_category[cat].append(clause)

        # Extract parties
        parties = self._extract_parties(contract_text)

        # Extract contract value
        contract_value = self._extract_contract_value(contract_text)

        # Risk assessment
        risk_assessment = {}
        for clause in clauses:
            if clause.risk_level == RiskLevel.HIGH:
                risk_assessment[clause.title] = f"HIGH RISK: Review {clause.category.value} clause carefully"

        # Action items
        action_items = self._generate_action_items(clauses)

        return ContractSummary(
            contract_type=self._identify_contract_type(contract_text),
            parties=parties,
            contract_value=contract_value,
            duration_days=0,  # Would extract from schedule clause
            start_date="",
            key_dates={},
            clauses_by_category=clauses_by_category,
            risk_assessment=risk_assessment,
            action_items=action_items
        )

    def _extract_parties(self, text: str) -> Dict[str, str]:
        """Extract contract parties."""
        parties = {}

        patterns = [
            (r"Owner[:\s]+([A-Z][A-Za-z\s,\.]+?)(?:\n|,\s*(?:a|an))", "owner"),
            (r"Contractor[:\s]+([A-Z][A-Za-z\s,\.]+?)(?:\n|,\s*(?:a|an))", "contractor"),
            (r"between\s+([A-Z][A-Za-z\s,\.]+?)\s+\(\"Owner\"\)", "owner"),
            (r"and\s+([A-Z][A-Za-z\s,\.]+?)\s+\(\"Contractor\"\)", "contractor"),
        ]

        for pattern, party_type in patterns:
            match = re.search(pattern, text)
            if match and party_type not in parties:
                parties[party_type] = match.group(1).strip()

        return parties

    def _extract_contract_value(self, text: str) -> float:
        """Extract contract value/sum."""
        patterns = [
            r"contract\s+(?:sum|price|amount)[:\s]+\$?([\d,]+(?:\.\d{2})?)",
            r"total\s+(?:contract|price)[:\s]+\$?([\d,]+(?:\.\d{2})?)",
            r"\$?([\d,]+(?:\.\d{2})?)\s+(?:dollars\s+)?(?:and\s+no/100)",
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    return float(match.group(1).replace(',', ''))
                except ValueError:
                    continue

        return 0.0

    def _identify_contract_type(self, text: str) -> str:
        """Identify contract type."""
        text_lower = text.lower()

        if "stipulated sum" in text_lower or "lump sum" in text_lower:
            return "Stipulated Sum (Lump Sum)"
        elif "cost plus" in text_lower or "cost of the work" in text_lower:
            return "Cost Plus"
        elif "guaranteed maximum" in text_lower or "gmp" in text_lower:
            return "GMP (Guaranteed Maximum Price)"
        elif "unit price" in text_lower:
            return "Unit Price"
        elif "time and materials" in text_lower or "t&m" in text_lower:
            return "Time and Materials"

        return "Standard Form"

    def _generate_action_items(self, clauses: List[ExtractedClause]) -> List[str]:
        """Generate action items from clause analysis."""
        actions = []

        for clause in clauses:
            if clause.risk_level == RiskLevel.HIGH:
                actions.append(f"REVIEW: High-risk {clause.category.value} clause in Article {clause.article_number}")

            if clause.category == ClauseCategory.INSURANCE:
                actions.append("Verify insurance requirements meet specified limits")

            if clause.category == ClauseCategory.PAYMENT:
                if "pay when paid" in ' '.join(clause.key_terms).lower():
                    actions.append("ALERT: Pay-when-paid clause detected - assess cash flow risk")
                if clause.time_periods:
                    actions.append(f"Note payment terms: {', '.join(clause.time_periods)}")

        return list(set(actions))

    def generate_report(self, summary: ContractSummary) -> str:
        """Generate contract review report."""
        lines = [
            "# Contract Analysis Report",
            "",
            f"**Contract Type:** {summary.contract_type}",
            f"**Contract Value:** ${summary.contract_value:,.2f}" if summary.contract_value else "",
            "",
            "## Parties",
            ""
        ]

        for party_type, name in summary.parties.items():
            lines.append(f"- **{party_type.title()}:** {name}")

        lines.extend(["", "## Key Clauses Summary", ""])

        for category, clauses in summary.clauses_by_category.items():
            lines.append(f"### {category.replace('_', ' ').title()}")
            for clause in clauses:
                risk_indicator = "🔴" if clause.risk_level == RiskLevel.HIGH else "🟡" if clause.risk_level == RiskLevel.MEDIUM else "🟢"
                lines.append(f"- {risk_indicator} **Article {clause.article_number}**: {clause.title}")
                if clause.key_terms:
                    lines.append(f"  - Key terms: {', '.join(clause.key_terms)}")
            lines.append("")

        if summary.risk_assessment:
            lines.extend(["## Risk Assessment", ""])
            for item, note in summary.risk_assessment.items():
                lines.append(f"- ⚠️ {note}")
            lines.append("")

        if summary.action_items:
            lines.extend(["## Action Items", ""])
            for item in summary.action_items:
                lines.append(f"- [ ] {item}")

        return "\n".join(lines)
```

## Quick Start

```python
# Initialize extractor
extractor = ContractClauseExtractor()

# Sample contract text
contract_text = """
ARTICLE 5 - PAYMENT

5.1 The Contract Sum is Five Million Dollars ($5,000,000.00).

5.2 Progress payments shall be made monthly based on the Schedule of Values.
Retainage of ten percent (10%) shall be withheld from each payment.

5.3 Final payment shall be made within 30 days of substantial completion.

ARTICLE 7 - CHANGES IN THE WORK

7.1 The Owner may order changes in the Work within the general scope of the
Contract. Such changes shall be authorized by written Change Order.

7.2 Contractor shall provide written notice of any claim for additional cost
or time within 21 days of the event giving rise to such claim.

ARTICLE 12 - INDEMNIFICATION

12.1 Contractor shall indemnify and hold harmless the Owner from and against
all claims arising out of the Contractor's negligence.
"""

# Extract clauses
clauses = extractor.extract_clauses(contract_text)
for clause in clauses:
    print(f"{clause.category.value}: {clause.title} (Risk: {clause.risk_level.value})")

# Generate summary
summary = extractor.generate_summary(contract_text)
print(extractor.generate_report(summary))
```

## Requirements

```bash
pip install (no external dependencies)
```
