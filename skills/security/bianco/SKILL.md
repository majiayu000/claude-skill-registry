---
name: bianco-pyramid-of-pain
description: Apply David Bianco's threat hunting frameworks including the Pyramid of Pain and Threat Hunting Maturity Model. Emphasizes prioritizing detection by adversary cost and building mature hunting programs. Use when designing detection strategies or assessing hunting capability.
---

# David Bianco — Threat Hunting Frameworks

## Overview

David Bianco is a SANS instructor with 20+ years in information security, primarily in detection and response. He created two foundational frameworks: the **Pyramid of Pain** (2013), which prioritizes indicators by adversary impact, and the **Threat Hunting Maturity Model**, which guides organizations in building hunting capability.

## References

- **Pyramid of Pain**: Original 2013 blog post, SANS documentation
- **Threat Hunting Maturity Model**: SANS whitepaper
- **Profile**: https://www.sans.org/profiles/david-bianco

## Core Philosophy

> "The more pain you cause adversaries, the more effective your detection."

> "Hunting is not about finding evil—it's about finding evil that your automated defenses missed."

Bianco's insight: not all indicators are equal. Detecting hash values is trivial for adversaries to evade; detecting their tactics, techniques, and procedures (TTPs) forces them to fundamentally change how they operate.

## The Pyramid of Pain

```
                    /\
                   /  \
                  / TT \      ← TTPs: Tough! Adversary must change behavior
                 /  Ps  \
                /--------\
               /  Tools   \   ← Tools: Annoying. Must find/create new tools
              /------------\
             / Network/Host \  ← Artifacts: Irritating. Must reconfigure
            /   Artifacts    \
           /------------------\
          /   Domain Names     \ ← Domains: Simple. Register new ones
         /----------------------\
        /     IP Addresses       \ ← IPs: Easy. Change infrastructure
       /--------------------------\
      /       Hash Values          \ ← Hashes: Trivial. Recompile
     /------------------------------\
```

### Level Details

| Level | Indicator Type | Adversary Pain | Detection Value |
|-------|---------------|----------------|-----------------|
| **1** | Hash Values | Trivial | Low |
| **2** | IP Addresses | Easy | Low |
| **3** | Domain Names | Simple | Medium |
| **4** | Network/Host Artifacts | Annoying | Medium |
| **5** | Tools | Challenging | High |
| **6** | TTPs | Tough! | Highest |

## Threat Hunting Maturity Model

```
Level 0: Initial
├── Relies primarily on automated alerting
├── Little to no routine data collection
└── Hunting: None

Level 1: Minimal  
├── Incorporates threat intelligence indicators
├── Moderate data collection
└── Hunting: IOC searches only

Level 2: Procedural
├── Follows procedures from others
├── High/very high data collection
└── Hunting: Follows published playbooks

Level 3: Innovative
├── Creates new procedures
├── High/very high data collection
└── Hunting: Creates original hypotheses

Level 4: Leading
├── Automates successful hunts
├── Very high data collection
└── Hunting: Continuous, automated
```

## When Implementing

### Always

- Prioritize TTP-based detections over IOC matching
- Measure detection effectiveness by adversary pain
- Document and share successful hunt methodologies
- Automate proven hunts into continuous detection
- Assess your organization's hunting maturity honestly

### Never

- Rely solely on hash-based detection
- Treat all indicators as equally valuable
- Hunt without a hypothesis
- Fail to document findings
- Ignore organizational maturity constraints

### Prefer

- Behavioral detection over signature matching
- Hypothesis-driven hunts over random searching
- Automated continuous hunting over periodic campaigns
- TTP mapping over IOC collection
- Detection as code over manual rule creation

## Implementation Patterns

### Pyramid-Aware Detection Strategy

```python
# detection_strategy.py
# Prioritize detections by Pyramid of Pain level

from dataclasses import dataclass
from enum import IntEnum
from typing import List, Optional

class PyramidLevel(IntEnum):
    """Pyramid of Pain levels - higher = more valuable"""
    HASH_VALUES = 1
    IP_ADDRESSES = 2
    DOMAIN_NAMES = 3
    ARTIFACTS = 4      # Network/Host artifacts
    TOOLS = 5
    TTPS = 6

@dataclass
class Detection:
    """A detection rule with pyramid classification"""
    name: str
    description: str
    level: PyramidLevel
    mitre_technique: Optional[str]
    query: str
    false_positive_rate: float
    
    @property
    def adversary_pain(self) -> str:
        pain_map = {
            PyramidLevel.HASH_VALUES: "Trivial - recompile",
            PyramidLevel.IP_ADDRESSES: "Easy - change infrastructure",
            PyramidLevel.DOMAIN_NAMES: "Simple - register new domains",
            PyramidLevel.ARTIFACTS: "Annoying - reconfigure tools",
            PyramidLevel.TOOLS: "Challenging - find/create new tools",
            PyramidLevel.TTPS: "Tough - must change tradecraft"
        }
        return pain_map[self.level]
    
    @property
    def priority_score(self) -> float:
        """Higher score = better detection to invest in"""
        # Weight by pyramid level, penalize false positives
        return (self.level.value * 10) * (1 - self.false_positive_rate)


class DetectionPortfolio:
    """Manage detections with pyramid awareness"""
    
    def __init__(self):
        self.detections: List[Detection] = []
    
    def add(self, detection: Detection):
        self.detections.append(detection)
    
    def coverage_by_level(self) -> dict:
        """Assess coverage at each pyramid level"""
        coverage = {level: [] for level in PyramidLevel}
        for det in self.detections:
            coverage[det.level].append(det.name)
        return coverage
    
    def maturity_assessment(self) -> str:
        """Assess detection maturity based on pyramid distribution"""
        coverage = self.coverage_by_level()
        
        ttp_count = len(coverage[PyramidLevel.TTPS])
        tool_count = len(coverage[PyramidLevel.TOOLS])
        ioc_count = (len(coverage[PyramidLevel.HASH_VALUES]) + 
                     len(coverage[PyramidLevel.IP_ADDRESSES]) +
                     len(coverage[PyramidLevel.DOMAIN_NAMES]))
        
        total = len(self.detections)
        if total == 0:
            return "No detections - Level 0"
        
        ttp_ratio = (ttp_count + tool_count) / total
        
        if ttp_ratio > 0.5:
            return "Mature - Strong TTP focus"
        elif ttp_ratio > 0.25:
            return "Developing - Building TTP coverage"
        else:
            return "Immature - Over-reliant on IOCs"
    
    def improvement_recommendations(self) -> List[str]:
        """Suggest where to invest detection effort"""
        coverage = self.coverage_by_level()
        recommendations = []
        
        if len(coverage[PyramidLevel.TTPS]) < 10:
            recommendations.append(
                "Priority: Add more TTP-based detections. "
                "These cause maximum adversary pain."
            )
        
        if len(coverage[PyramidLevel.TOOLS]) < 5:
            recommendations.append(
                "Add tool-based detections for common attack frameworks "
                "(Cobalt Strike, Mimikatz, etc.)"
            )
        
        ioc_count = (len(coverage[PyramidLevel.HASH_VALUES]) + 
                     len(coverage[PyramidLevel.IP_ADDRESSES]))
        if ioc_count > len(self.detections) * 0.5:
            recommendations.append(
                "Warning: Over 50% of detections are low-value IOCs. "
                "Consider retiring stale IOC rules."
            )
        
        return recommendations


# Example: TTP-level detection
ttp_detection = Detection(
    name="Suspicious PowerShell Download Cradle",
    description="Detects PowerShell download and execute patterns",
    level=PyramidLevel.TTPS,
    mitre_technique="T1059.001",
    query="""
        process_name:powershell.exe AND 
        (command_line:*DownloadString* OR 
         command_line:*IEX* OR 
         command_line:*Invoke-Expression*)
    """,
    false_positive_rate=0.05
)

# Example: Hash-level detection (low value)
hash_detection = Detection(
    name="Known Malware Hash",
    description="Matches specific malware sample hash",
    level=PyramidLevel.HASH_VALUES,
    mitre_technique=None,
    query="file_hash:e99a18c428cb38d5f260853678922e03",
    false_positive_rate=0.001
)
```

### Hunting Maturity Assessment

```python
# maturity_model.py
# Assess and improve threat hunting maturity

from dataclasses import dataclass
from enum import IntEnum
from typing import List

class HuntingMaturityLevel(IntEnum):
    INITIAL = 0      # Relies on automated alerts
    MINIMAL = 1      # IOC searches
    PROCEDURAL = 2   # Follows playbooks
    INNOVATIVE = 3   # Creates new procedures
    LEADING = 4      # Automates hunts

@dataclass
class MaturityAssessment:
    """Evaluate hunting program maturity"""
    
    # Data Collection
    has_endpoint_telemetry: bool
    has_network_telemetry: bool
    has_cloud_telemetry: bool
    data_retention_days: int
    
    # Hunting Practice
    has_dedicated_hunters: bool
    hunts_per_month: int
    uses_threat_intel: bool
    documents_hunts: bool
    automates_successful_hunts: bool
    creates_original_hypotheses: bool
    
    # Infrastructure
    has_hunting_platform: bool
    has_playbook_library: bool
    measures_hunt_effectiveness: bool
    
    def calculate_level(self) -> HuntingMaturityLevel:
        """Determine maturity level"""
        
        # Level 4: Leading
        if (self.automates_successful_hunts and 
            self.creates_original_hypotheses and
            self.measures_hunt_effectiveness and
            self.hunts_per_month >= 8):
            return HuntingMaturityLevel.LEADING
        
        # Level 3: Innovative
        if (self.creates_original_hypotheses and
            self.documents_hunts and
            self.hunts_per_month >= 4):
            return HuntingMaturityLevel.INNOVATIVE
        
        # Level 2: Procedural
        if (self.has_playbook_library and
            self.has_dedicated_hunters and
            self.hunts_per_month >= 2):
            return HuntingMaturityLevel.PROCEDURAL
        
        # Level 1: Minimal
        if self.uses_threat_intel:
            return HuntingMaturityLevel.MINIMAL
        
        # Level 0: Initial
        return HuntingMaturityLevel.INITIAL
    
    def roadmap_to_next_level(self) -> List[str]:
        """What's needed to advance"""
        current = self.calculate_level()
        
        if current == HuntingMaturityLevel.INITIAL:
            return [
                "Implement threat intelligence feeds",
                "Begin IOC-based hunting",
                "Ensure basic telemetry collection",
                "Identify potential hunting analysts"
            ]
        
        elif current == HuntingMaturityLevel.MINIMAL:
            return [
                "Develop or adopt hunting playbooks",
                "Dedicate analyst time to hunting",
                "Increase data collection coverage",
                "Hunt at least 2x per month"
            ]
        
        elif current == HuntingMaturityLevel.PROCEDURAL:
            return [
                "Train hunters to create original hypotheses",
                "Document all hunt findings",
                "Begin measuring hunt effectiveness",
                "Increase hunt frequency to 4x/month"
            ]
        
        elif current == HuntingMaturityLevel.INNOVATIVE:
            return [
                "Automate successful hunts into detections",
                "Build metrics dashboard for hunting",
                "Share methodologies with community",
                "Achieve continuous hunting capability"
            ]
        
        return ["You've achieved hunting mastery! 🏆"]
```

### TTP-Based Hunt Design

```python
# ttp_hunt.py
# Design hunts that target TTPs (maximum pain)

from dataclasses import dataclass
from typing import List, Dict

@dataclass
class TTPHunt:
    """A hunt targeting specific adversary TTPs"""
    
    name: str
    hypothesis: str
    mitre_tactic: str
    mitre_techniques: List[str]
    
    # Data requirements
    required_telemetry: List[str]
    
    # Hunt queries
    queries: Dict[str, str]  # platform -> query
    
    # Expected findings
    expected_benign: List[str]
    indicators_of_compromise: List[str]
    
    # Documentation
    references: List[str]
    
    def to_playbook(self) -> str:
        """Generate hunt playbook"""
        playbook = f"""
# Hunt Playbook: {self.name}

## Hypothesis
{self.hypothesis}

## MITRE ATT&CK Mapping
- **Tactic**: {self.mitre_tactic}
- **Techniques**: {', '.join(self.mitre_techniques)}

## Required Telemetry
{chr(10).join(f'- {t}' for t in self.required_telemetry)}

## Hunt Queries

"""
        for platform, query in self.queries.items():
            playbook += f"### {platform}\n```\n{query}\n```\n\n"
        
        playbook += f"""
## Expected Benign Activity
{chr(10).join(f'- {b}' for b in self.expected_benign)}

## Indicators of Compromise
{chr(10).join(f'- {i}' for i in self.indicators_of_compromise)}

## References
{chr(10).join(f'- {r}' for r in self.references)}
"""
        return playbook


# Example: Credential Dumping Hunt (TTP-level)
credential_dump_hunt = TTPHunt(
    name="LSASS Memory Access",
    hypothesis="Adversaries are accessing LSASS memory to dump credentials",
    mitre_tactic="Credential Access",
    mitre_techniques=["T1003.001"],
    required_telemetry=[
        "Process creation with command line",
        "Process access events (Sysmon Event 10)",
        "Memory read operations"
    ],
    queries={
        "Splunk": """
            index=windows sourcetype=sysmon EventCode=10
            TargetImage="*lsass.exe"
            NOT SourceImage IN ("*\\\\MsMpEng.exe", "*\\\\csrss.exe")
            | stats count by SourceImage, SourceProcessGUID
            | where count > 1
        """,
        "Elastic": """
            event.code:10 AND 
            process.target.name:lsass.exe AND
            NOT process.name:(MsMpEng.exe OR csrss.exe)
        """
    },
    expected_benign=[
        "Windows Defender (MsMpEng.exe)",
        "Antivirus products",
        "Crash dump utilities"
    ],
    indicators_of_compromise=[
        "procdump.exe accessing lsass.exe",
        "mimikatz.exe or renamed variants",
        "comsvcs.dll MiniDump export",
        "Unknown processes accessing lsass.exe"
    ],
    references=[
        "https://attack.mitre.org/techniques/T1003/001/",
        "https://www.microsoft.com/security/blog/credential-theft/"
    ]
)
```

## Mental Model

Bianco approaches threat hunting by asking:

1. **What pyramid level is this?** Prioritize TTP-based detection
2. **What pain does this cause?** Measure detection value by adversary impact
3. **What's our maturity level?** Match hunting to organizational capability
4. **Can we automate this?** Successful hunts become continuous detection
5. **What did we learn?** Every hunt improves the program

## Signature Bianco Moves

- Pyramid of Pain for indicator prioritization
- Maturity model for program development
- TTP focus over IOC collection
- Hypothesis-driven hunting
- Automation of proven hunts
- Continuous improvement mindset
