---
name: mitre-attack-framework
description: Apply the MITRE ATT&CK framework for threat intelligence and detection. Provides a universal taxonomy of adversary tactics, techniques, and procedures (TTPs). Use when mapping threats, building detections, or assessing defensive coverage.
---

# MITRE ATT&CK Framework

## Overview

MITRE ATT&CK (Adversarial Tactics, Techniques, and Common Knowledge) is a globally-accessible knowledge base of adversary behavior based on real-world observations. Created by MITRE Corporation, it has become the universal language for describing how adversaries operate.

## References

- **Website**: https://attack.mitre.org/
- **Navigator**: https://mitre-attack.github.io/attack-navigator/
- **GitHub**: https://github.com/mitre-attack

## Core Philosophy

> "Know your adversary."

> "You can't defend against what you don't understand."

ATT&CK shifts the focus from IOCs (what attackers use) to TTPs (how attackers behave). This behavioral focus provides more durable detection strategies.

## The ATT&CK Matrix Structure

```
Enterprise ATT&CK Matrix

TACTICS (The "Why" - Adversary Goals)
├── Reconnaissance        ← Gather information
├── Resource Development  ← Build infrastructure  
├── Initial Access        ← Get into the network
├── Execution             ← Run malicious code
├── Persistence           ← Maintain foothold
├── Privilege Escalation  ← Get higher privileges
├── Defense Evasion       ← Avoid detection
├── Credential Access     ← Steal credentials
├── Discovery             ← Learn the environment
├── Lateral Movement      ← Move through network
├── Collection            ← Gather target data
├── Command and Control   ← Communicate with implants
├── Exfiltration          ← Steal data
└── Impact                ← Damage or disrupt

TECHNIQUES (The "How" - Methods Used)
└── Each tactic contains multiple techniques
    └── Techniques may have sub-techniques
        └── Example: T1059.001 (PowerShell) under T1059 (Command and Scripting Interpreter)
```

## Key Components

| Component | Description | Example |
|-----------|-------------|---------|
| **Tactics** | Adversary goals | Credential Access |
| **Techniques** | How goals are achieved | OS Credential Dumping (T1003) |
| **Sub-techniques** | Specific implementations | LSASS Memory (T1003.001) |
| **Procedures** | Real-world examples | APT28 uses Mimikatz |
| **Mitigations** | How to prevent | Credential Guard |
| **Detections** | How to find | Monitor LSASS access |

## When Implementing

### Always

- Map detections to ATT&CK techniques
- Assess coverage across all tactics
- Use ATT&CK Navigator for visualization
- Reference technique IDs in alerts
- Track adversary groups and their TTPs
- Update mapping as ATT&CK evolves

### Never

- Assume full coverage from a few detections
- Ignore techniques without current detections
- Treat ATT&CK as a compliance checklist
- Map inaccurately to inflate coverage
- Forget sub-techniques in analysis

### Prefer

- Behavioral detection over signature matching
- Coverage breadth over depth initially
- Technique-based hunting hypotheses
- ATT&CK-aligned threat intelligence
- Continuous coverage assessment

## Implementation Patterns

### ATT&CK Coverage Assessment

```python
# attack_coverage.py
# Assess and visualize ATT&CK coverage

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set
from enum import Enum
import json

class CoverageLevel(Enum):
    NONE = 0
    MINIMAL = 1      # Basic detection exists
    PARTIAL = 2      # Some variants covered
    SUBSTANTIAL = 3  # Most variants covered
    COMPREHENSIVE = 4 # Full coverage with validation

@dataclass
class Technique:
    """ATT&CK Technique representation"""
    id: str                          # e.g., "T1003.001"
    name: str                        # e.g., "LSASS Memory"
    tactic: str                      # e.g., "Credential Access"
    platforms: List[str]             # e.g., ["Windows"]
    data_sources: List[str]          # Required telemetry
    
    # Coverage tracking
    detections: List[str] = field(default_factory=list)
    coverage_level: CoverageLevel = CoverageLevel.NONE
    last_validated: Optional[str] = None
    
    @property
    def is_sub_technique(self) -> bool:
        return "." in self.id

@dataclass
class Detection:
    """A detection rule mapped to ATT&CK"""
    name: str
    techniques: List[str]           # ATT&CK technique IDs
    query: str
    platform: str                   # SIEM/EDR platform
    false_positive_rate: float
    validated: bool = False

class ATTACKCoverageAnalyzer:
    """Analyze detection coverage against ATT&CK"""
    
    def __init__(self):
        self.techniques: Dict[str, Technique] = {}
        self.detections: List[Detection] = []
        self.tactics = [
            "Reconnaissance", "Resource Development", "Initial Access",
            "Execution", "Persistence", "Privilege Escalation",
            "Defense Evasion", "Credential Access", "Discovery",
            "Lateral Movement", "Collection", "Command and Control",
            "Exfiltration", "Impact"
        ]
    
    def load_attack_data(self, attack_json_path: str):
        """Load ATT&CK STIX data"""
        # In practice, load from MITRE's STIX bundle
        pass
    
    def add_detection(self, detection: Detection):
        """Add detection and update coverage"""
        self.detections.append(detection)
        
        for tech_id in detection.techniques:
            if tech_id in self.techniques:
                self.techniques[tech_id].detections.append(detection.name)
                self._update_coverage_level(tech_id)
    
    def _update_coverage_level(self, tech_id: str):
        """Recalculate coverage level for technique"""
        tech = self.techniques[tech_id]
        detection_count = len(tech.detections)
        
        if detection_count == 0:
            tech.coverage_level = CoverageLevel.NONE
        elif detection_count == 1:
            tech.coverage_level = CoverageLevel.MINIMAL
        elif detection_count < 3:
            tech.coverage_level = CoverageLevel.PARTIAL
        elif detection_count < 5:
            tech.coverage_level = CoverageLevel.SUBSTANTIAL
        else:
            tech.coverage_level = CoverageLevel.COMPREHENSIVE
    
    def coverage_by_tactic(self) -> Dict[str, dict]:
        """Get coverage statistics per tactic"""
        results = {}
        
        for tactic in self.tactics:
            tactic_techs = [t for t in self.techniques.values() 
                          if t.tactic == tactic]
            
            if not tactic_techs:
                continue
            
            covered = sum(1 for t in tactic_techs 
                         if t.coverage_level != CoverageLevel.NONE)
            
            results[tactic] = {
                'total_techniques': len(tactic_techs),
                'covered': covered,
                'coverage_percent': (covered / len(tactic_techs)) * 100,
                'gaps': [t.id for t in tactic_techs 
                        if t.coverage_level == CoverageLevel.NONE]
            }
        
        return results
    
    def identify_gaps(self) -> List[Technique]:
        """Find techniques with no detection coverage"""
        return [t for t in self.techniques.values() 
                if t.coverage_level == CoverageLevel.NONE]
    
    def prioritize_gaps(self) -> List[Technique]:
        """Prioritize gaps by adversary usage"""
        gaps = self.identify_gaps()
        
        # Prioritize by:
        # 1. Commonly used by threat groups
        # 2. Data sources already available
        # 3. Tactic importance
        
        high_priority_tactics = [
            "Initial Access", "Execution", "Persistence",
            "Credential Access", "Lateral Movement"
        ]
        
        prioritized = sorted(
            gaps,
            key=lambda t: (
                t.tactic in high_priority_tactics,  # Prioritize key tactics
                len(t.data_sources)                  # Easier to detect
            ),
            reverse=True
        )
        
        return prioritized
    
    def generate_navigator_layer(self) -> dict:
        """Generate ATT&CK Navigator layer JSON"""
        layer = {
            "name": "Detection Coverage",
            "version": "4.4",
            "domain": "enterprise-attack",
            "description": "Current detection coverage",
            "techniques": []
        }
        
        color_map = {
            CoverageLevel.NONE: "#ffffff",
            CoverageLevel.MINIMAL: "#ffcccc",
            CoverageLevel.PARTIAL: "#ffff99",
            CoverageLevel.SUBSTANTIAL: "#99ff99",
            CoverageLevel.COMPREHENSIVE: "#00ff00"
        }
        
        for tech in self.techniques.values():
            layer["techniques"].append({
                "techniqueID": tech.id,
                "color": color_map[tech.coverage_level],
                "comment": f"Detections: {len(tech.detections)}"
            })
        
        return layer
```

### Technique-Based Detection

```python
# technique_detection.py
# Build detections aligned to ATT&CK techniques

from dataclasses import dataclass
from typing import List, Dict

@dataclass
class ATTACKDetection:
    """Detection rule with full ATT&CK context"""
    
    # ATT&CK mapping
    technique_id: str
    technique_name: str
    tactic: str
    
    # Detection details
    name: str
    description: str
    query: str
    platform: str
    
    # Quality metrics
    severity: str
    confidence: str
    false_positive_guidance: str
    
    # Data requirements
    data_sources: List[str]
    
    # Response
    recommended_response: List[str]
    
    def to_sigma(self) -> str:
        """Export as Sigma rule"""
        return f"""
title: {self.name}
id: {self.technique_id.lower().replace('.', '-')}-detection
status: experimental
description: {self.description}
references:
    - https://attack.mitre.org/techniques/{self.technique_id}/
author: Security Team
date: 2024/01/01
tags:
    - attack.{self.tactic.lower().replace(' ', '_')}
    - attack.{self.technique_id.lower()}
logsource:
    category: process_creation
    product: windows
detection:
    selection:
        # Detection logic here
    condition: selection
falsepositives:
    - {self.false_positive_guidance}
level: {self.severity.lower()}
"""


# Example: T1003.001 - LSASS Memory
lsass_detection = ATTACKDetection(
    technique_id="T1003.001",
    technique_name="LSASS Memory",
    tactic="Credential Access",
    name="LSASS Memory Access via Suspicious Process",
    description="Detects processes accessing LSASS memory, "
                "commonly used for credential dumping",
    query="""
        event.code:10 AND 
        winlog.event_data.TargetImage:*lsass.exe AND
        NOT winlog.event_data.SourceImage:(
            *MsMpEng.exe OR *csrss.exe OR *wininit.exe
        )
    """,
    platform="Elastic SIEM",
    severity="High",
    confidence="Medium",
    false_positive_guidance="Security tools may legitimately access LSASS",
    data_sources=["Process: Process Access (Sysmon EID 10)"],
    recommended_response=[
        "Isolate affected host",
        "Capture memory dump for analysis",
        "Reset potentially compromised credentials",
        "Hunt for lateral movement"
    ]
)
```

### Threat Group Tracking

```python
# threat_groups.py
# Track adversary groups and their TTPs

from dataclasses import dataclass
from typing import List, Set, Dict

@dataclass
class ThreatGroup:
    """Known adversary group with TTPs"""
    
    id: str                          # e.g., "G0007"
    name: str                        # e.g., "APT28"
    aliases: List[str]               # e.g., ["Fancy Bear", "Sofacy"]
    
    # Attribution
    suspected_origin: str
    target_sectors: List[str]
    target_regions: List[str]
    
    # TTPs
    techniques: List[str]            # ATT&CK technique IDs
    
    # Intelligence
    first_seen: str
    last_seen: str
    active: bool
    
    def technique_overlap(self, other: 'ThreatGroup') -> Set[str]:
        """Find common techniques with another group"""
        return set(self.techniques) & set(other.techniques)
    
    def unique_techniques(self, all_groups: List['ThreatGroup']) -> Set[str]:
        """Find techniques unique to this group"""
        other_techniques = set()
        for group in all_groups:
            if group.id != self.id:
                other_techniques.update(group.techniques)
        
        return set(self.techniques) - other_techniques


class ThreatIntelligence:
    """Manage threat group intelligence"""
    
    def __init__(self):
        self.groups: Dict[str, ThreatGroup] = {}
    
    def relevant_groups(self, sector: str, region: str) -> List[ThreatGroup]:
        """Find groups targeting specific sector/region"""
        return [
            g for g in self.groups.values()
            if (sector in g.target_sectors or "All" in g.target_sectors) and
               (region in g.target_regions or "Global" in g.target_regions) and
               g.active
        ]
    
    def priority_techniques(self, sector: str, region: str) -> Dict[str, int]:
        """Rank techniques by threat relevance"""
        relevant = self.relevant_groups(sector, region)
        
        technique_counts = {}
        for group in relevant:
            for tech in group.techniques:
                technique_counts[tech] = technique_counts.get(tech, 0) + 1
        
        # Sort by frequency across relevant groups
        return dict(sorted(
            technique_counts.items(),
            key=lambda x: x[1],
            reverse=True
        ))
    
    def detection_priorities(self, 
                            sector: str, 
                            region: str,
                            current_coverage: Set[str]) -> List[str]:
        """Prioritize detections based on threat landscape"""
        priority_techs = self.priority_techniques(sector, region)
        
        # Find high-priority techniques without coverage
        gaps = [
            tech for tech, count in priority_techs.items()
            if tech not in current_coverage and count >= 2
        ]
        
        return gaps[:10]  # Top 10 priorities
```

### Hunt Hypothesis Generation

```python
# hypothesis_generator.py
# Generate hunt hypotheses from ATT&CK

from dataclasses import dataclass
from typing import List

@dataclass
class HuntHypothesis:
    """ATT&CK-based hunt hypothesis"""
    
    technique_id: str
    technique_name: str
    tactic: str
    
    hypothesis: str
    rationale: str
    
    data_requirements: List[str]
    hunt_query: str
    
    expected_findings: List[str]
    success_criteria: str


def generate_hypotheses(technique_id: str, 
                       technique_data: dict) -> List[HuntHypothesis]:
    """Generate hunt hypotheses for a technique"""
    
    hypotheses = []
    
    # Hypothesis 1: Direct technique detection
    hypotheses.append(HuntHypothesis(
        technique_id=technique_id,
        technique_name=technique_data['name'],
        tactic=technique_data['tactic'],
        hypothesis=f"Adversaries are using {technique_data['name']} "
                   f"in our environment",
        rationale=f"This technique is commonly used by threat groups "
                  f"targeting our sector",
        data_requirements=technique_data['data_sources'],
        hunt_query=technique_data.get('detection_query', ''),
        expected_findings=[
            "Legitimate use by IT/security tools",
            "Developer/admin testing",
            "Potential adversary activity"
        ],
        success_criteria="Identify all instances, triage findings, "
                        "create detection for confirmed malicious patterns"
    ))
    
    # Hypothesis 2: Technique chaining
    if technique_data.get('related_techniques'):
        hypotheses.append(HuntHypothesis(
            technique_id=technique_id,
            technique_name=technique_data['name'],
            tactic=technique_data['tactic'],
            hypothesis=f"Adversaries using {technique_data['name']} "
                       f"are also using related techniques",
            rationale="Techniques are often used in combination",
            data_requirements=technique_data['data_sources'],
            hunt_query="Correlated query across related techniques",
            expected_findings=["Attack chains", "Lateral movement paths"],
            success_criteria="Map complete attack chain if present"
        ))
    
    return hypotheses
```

## Mental Model

MITRE ATT&CK practitioners ask:

1. **What tactic is this?** Understand adversary goal
2. **What technique?** Identify specific method
3. **Do we detect this?** Assess coverage
4. **Who uses this?** Threat group attribution
5. **What's the gap?** Prioritize improvements

## Signature ATT&CK Moves

- Technique IDs in all detections and alerts
- Navigator layers for coverage visualization
- Threat group TTP tracking
- Gap analysis by tactic
- Hypothesis generation from techniques
- Continuous coverage assessment
