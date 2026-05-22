---
name: roth-detection-engineering
description: Apply Florian Roth's detection engineering methodology with YARA and Sigma rules. Emphasizes portable detection logic, community sharing, and signature quality. Use when creating detection rules that work across platforms.
---

# Florian Roth — Detection Engineering

## Overview

Florian Roth is CTO of Nextron Systems and creator of some of the most influential detection tools in security: the Sigma rule format, extensive YARA rule sets, and the THOR APT scanner. His work has made detection logic portable, shareable, and accessible to the community.

## References

- **Sigma**: https://sigmahq.io/
- **YARA**: https://virustotal.github.io/yara/
- **GitHub**: https://github.com/Neo23x0
- **Twitter**: @cyb3rops

## Core Philosophy

> "Detection should be shareable."

> "One rule format to rule them all."

> "The community is stronger together."

Roth's insight: detection logic shouldn't be locked to a single SIEM. Sigma allows defenders to write once and deploy everywhere, accelerating community-wide defense.

## Key Contributions

### Sigma Rules
Generic signature format for SIEM systems. Write detection logic once, convert to any SIEM query language.

### YARA Rules
Binary pattern matching for malware detection. Extensive rule sets for threat hunting.

### THOR Scanner
APT scanner that brings professional detection capabilities to incident response.

## When Implementing

### Always

- Write Sigma rules for portability
- Include MITRE ATT&CK tags
- Document false positives
- Test rules before deployment
- Share rules with the community
- Version control your rules

### Never

- Hard-code SIEM-specific syntax in shared rules
- Deploy untested rules to production
- Ignore false positive rates
- Keep effective rules private
- Skip metadata (author, date, references)

### Prefer

- Sigma over SIEM-specific queries
- Behavioral patterns over exact strings
- Community rules as starting points
- Layered detection (multiple rules per technique)
- Regular rule review and tuning

## Implementation Patterns

### Sigma Rule Anatomy

```yaml
# sigma_rule_template.yml
# Complete Sigma rule with all recommended fields

title: Suspicious PowerShell Download Cradle
id: 3b6ab547-8ec2-4991-b9d2-2b06702a48d7    # UUID
status: experimental    # test | stable | deprecated
description: |
    Detects PowerShell download cradle patterns commonly used
    for malware delivery and living-off-the-land attacks.

references:
    - https://attack.mitre.org/techniques/T1059/001/
    - https://lolbas-project.github.io/

author: Florian Roth (Nextron Systems)
date: 2024/01/15
modified: 2024/02/20

tags:
    - attack.execution
    - attack.t1059.001
    - attack.defense_evasion
    - attack.t1140

logsource:
    category: process_creation
    product: windows

detection:
    selection_img:
        - Image|endswith: '\powershell.exe'
        - Image|endswith: '\pwsh.exe'
        - OriginalFileName:
            - 'PowerShell.EXE'
            - 'pwsh.dll'
    
    selection_commands:
        CommandLine|contains:
            - 'IEX'
            - 'Invoke-Expression'
            - 'DownloadString'
            - 'DownloadFile'
            - 'DownloadData'
            - 'Net.WebClient'
            - 'Start-BitsTransfer'
            - 'Invoke-WebRequest'
            - 'iwr '
            - 'curl '
            - 'wget '
    
    filter_legitimate:
        CommandLine|contains:
            - 'chocolatey'
            - 'update-help'
            - 'Microsoft.PowerShell'
    
    condition: all of selection_* and not filter_legitimate

falsepositives:
    - Legitimate administration scripts
    - Software deployment tools
    - Package managers (Chocolatey, etc.)

level: medium

fields:
    - CommandLine
    - ParentCommandLine
    - User
    - ComputerName
```

### YARA Rule Anatomy

```yara
/*
    YARA Rule: Cobalt Strike Beacon
    Author: Florian Roth
    Date: 2024-01-15
    Reference: https://www.cobaltstrike.com/
    
    Detects Cobalt Strike beacon payloads in memory or files
*/

rule CobaltStrike_Beacon_Encoded
{
    meta:
        description = "Detects Cobalt Strike beacon"
        author = "Florian Roth"
        date = "2024-01-15"
        reference = "https://attack.mitre.org/software/S0154/"
        hash1 = "abc123..."
        score = 80
        
    strings:
        // XOR encoded config
        $config_start = { 00 01 00 01 00 02 }
        
        // Sleep mask
        $sleep_mask = { 48 89 5C 24 08 48 89 6C 24 10 }
        
        // Named pipe pattern
        $pipe = "\\\\.\\pipe\\msagent_" ascii wide
        
        // Default watermark (change for specific actors)
        $watermark = { 01 00 00 00 [4] 00 00 00 00 }
        
        // Reflective loader
        $reflective = "ReflectiveLoader" ascii
        
    condition:
        uint16(0) == 0x5A4D and    // MZ header
        filesize < 1MB and
        (
            ($config_start and $watermark) or
            ($sleep_mask and $pipe) or
            ($reflective and $pipe)
        )
}

rule Mimikatz_Memory_Strings
{
    meta:
        description = "Detects Mimikatz in memory"
        author = "Florian Roth"
        reference = "https://attack.mitre.org/software/S0002/"
        
    strings:
        $s1 = "sekurlsa::logonpasswords" ascii wide nocase
        $s2 = "sekurlsa::wdigest" ascii wide nocase
        $s3 = "sekurlsa::kerberos" ascii wide nocase
        $s4 = "lsadump::sam" ascii wide nocase
        $s5 = "lsadump::dcsync" ascii wide nocase
        $s6 = "privilege::debug" ascii wide nocase
        
        $author = "gentilkiwi" ascii wide
        $tool = "mimikatz" ascii wide nocase
        
    condition:
        3 of ($s*) or
        ($author and $tool)
}
```

### Sigma to SIEM Conversion

```python
# sigma_converter.py
# Convert Sigma rules to various SIEM formats

from dataclasses import dataclass
from typing import Dict, List, Optional
import yaml
import re

@dataclass
class SigmaRule:
    """Parsed Sigma rule"""
    title: str
    id: str
    status: str
    description: str
    logsource: Dict
    detection: Dict
    level: str
    tags: List[str]
    falsepositives: List[str]
    
    @classmethod
    def from_yaml(cls, yaml_content: str) -> 'SigmaRule':
        data = yaml.safe_load(yaml_content)
        return cls(
            title=data.get('title', ''),
            id=data.get('id', ''),
            status=data.get('status', 'experimental'),
            description=data.get('description', ''),
            logsource=data.get('logsource', {}),
            detection=data.get('detection', {}),
            level=data.get('level', 'medium'),
            tags=data.get('tags', []),
            falsepositives=data.get('falsepositives', [])
        )


class SigmaConverter:
    """Convert Sigma rules to SIEM queries"""
    
    def __init__(self, rule: SigmaRule):
        self.rule = rule
    
    def to_splunk(self) -> str:
        """Convert to Splunk SPL"""
        query_parts = []
        
        # Add index based on logsource
        if self.rule.logsource.get('product') == 'windows':
            query_parts.append('index=windows')
        
        # Process detection selections
        detection = self.rule.detection
        condition = detection.get('condition', '')
        
        for key, value in detection.items():
            if key == 'condition':
                continue
            
            if isinstance(value, dict):
                field_queries = self._convert_selection_splunk(value)
                query_parts.append(f"({' OR '.join(field_queries)})")
        
        # Combine with condition logic
        query = ' '.join(query_parts)
        
        # Add table formatting
        query += f"\n| table _time, ComputerName, User, CommandLine"
        
        return query
    
    def _convert_selection_splunk(self, selection: Dict) -> List[str]:
        """Convert selection to Splunk query parts"""
        queries = []
        
        for field, value in selection.items():
            # Handle modifiers
            if '|' in field:
                field_name, modifier = field.split('|')
                
                if modifier == 'endswith':
                    if isinstance(value, list):
                        queries.extend([f'{field_name}="*{v}"' for v in value])
                    else:
                        queries.append(f'{field_name}="*{value}"')
                        
                elif modifier == 'contains':
                    if isinstance(value, list):
                        queries.extend([f'{field_name}="*{v}*"' for v in value])
                    else:
                        queries.append(f'{field_name}="*{value}*"')
                        
                elif modifier == 'startswith':
                    if isinstance(value, list):
                        queries.extend([f'{field_name}="{v}*"' for v in value])
                    else:
                        queries.append(f'{field_name}="{value}*"')
            else:
                if isinstance(value, list):
                    queries.extend([f'{field}="{v}"' for v in value])
                else:
                    queries.append(f'{field}="{value}"')
        
        return queries
    
    def to_elastic(self) -> str:
        """Convert to Elastic Query DSL / KQL"""
        query_parts = []
        
        detection = self.rule.detection
        
        for key, value in detection.items():
            if key == 'condition':
                continue
            
            if isinstance(value, dict):
                field_queries = self._convert_selection_elastic(value)
                query_parts.append(f"({' OR '.join(field_queries)})")
        
        return ' AND '.join(query_parts)
    
    def _convert_selection_elastic(self, selection: Dict) -> List[str]:
        """Convert selection to Elastic query parts"""
        queries = []
        
        for field, value in selection.items():
            field_name = field.split('|')[0] if '|' in field else field
            
            # Map Windows fields to ECS
            field_map = {
                'Image': 'process.executable',
                'CommandLine': 'process.command_line',
                'ParentImage': 'process.parent.executable',
                'User': 'user.name',
                'ComputerName': 'host.name'
            }
            field_name = field_map.get(field_name, field_name)
            
            if '|' in field:
                modifier = field.split('|')[1]
                
                if modifier == 'contains':
                    if isinstance(value, list):
                        queries.extend([f'{field_name}:*{v}*' for v in value])
                    else:
                        queries.append(f'{field_name}:*{value}*')
            else:
                if isinstance(value, list):
                    queries.extend([f'{field_name}:"{v}"' for v in value])
                else:
                    queries.append(f'{field_name}:"{value}"')
        
        return queries
    
    def to_qradar(self) -> str:
        """Convert to QRadar AQL"""
        # QRadar-specific conversion
        pass
    
    def to_sentinel(self) -> str:
        """Convert to Microsoft Sentinel KQL"""
        query_parts = []
        
        # Start with appropriate table
        if self.rule.logsource.get('category') == 'process_creation':
            query_parts.append("SecurityEvent")
            query_parts.append("| where EventID == 4688")
        
        # Add field filters
        detection = self.rule.detection
        for key, value in detection.items():
            if key == 'condition':
                continue
            
            if isinstance(value, dict):
                for field, val in value.items():
                    field_name = field.split('|')[0]
                    
                    # Sentinel field mapping
                    sentinel_fields = {
                        'CommandLine': 'CommandLine',
                        'Image': 'NewProcessName',
                        'User': 'SubjectUserName'
                    }
                    sentinel_field = sentinel_fields.get(field_name, field_name)
                    
                    if '|contains' in field:
                        if isinstance(val, list):
                            conditions = ' or '.join(
                                [f'{sentinel_field} contains "{v}"' for v in val]
                            )
                            query_parts.append(f"| where {conditions}")
        
        return '\n'.join(query_parts)
```

### Rule Quality Framework

```python
# rule_quality.py
# Assess and improve detection rule quality

from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum

class QualityDimension(Enum):
    ACCURACY = "accuracy"           # Low false positives
    COVERAGE = "coverage"           # Catches variants
    PERFORMANCE = "performance"     # Query efficiency
    MAINTAINABILITY = "maintainability"  # Easy to update
    DOCUMENTATION = "documentation"  # Well documented

@dataclass
class RuleQualityScore:
    """Quality assessment for a detection rule"""
    
    rule_id: str
    
    # Scoring (0-100)
    accuracy_score: int
    coverage_score: int
    performance_score: int
    maintainability_score: int
    documentation_score: int
    
    # Evidence
    false_positive_rate: float
    true_positive_samples: int
    avg_query_time_ms: float
    
    # Recommendations
    improvements: List[str]
    
    @property
    def overall_score(self) -> float:
        weights = {
            'accuracy': 0.30,
            'coverage': 0.25,
            'performance': 0.15,
            'maintainability': 0.15,
            'documentation': 0.15
        }
        
        return (
            self.accuracy_score * weights['accuracy'] +
            self.coverage_score * weights['coverage'] +
            self.performance_score * weights['performance'] +
            self.maintainability_score * weights['maintainability'] +
            self.documentation_score * weights['documentation']
        )
    
    @property
    def grade(self) -> str:
        score = self.overall_score
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        return "F"


class RuleQualityAnalyzer:
    """Analyze and improve rule quality"""
    
    def analyze_sigma_rule(self, rule_content: str) -> RuleQualityScore:
        """Analyze a Sigma rule for quality"""
        import yaml
        rule = yaml.safe_load(rule_content)
        
        improvements = []
        
        # Documentation score
        doc_score = 100
        if not rule.get('description'):
            doc_score -= 30
            improvements.append("Add detailed description")
        if not rule.get('references'):
            doc_score -= 20
            improvements.append("Add references (ATT&CK, blog posts)")
        if not rule.get('author'):
            doc_score -= 10
            improvements.append("Add author information")
        if not rule.get('tags'):
            doc_score -= 20
            improvements.append("Add ATT&CK tags")
        if not rule.get('falsepositives'):
            doc_score -= 20
            improvements.append("Document known false positives")
        
        # Maintainability score
        maint_score = 100
        detection = rule.get('detection', {})
        
        # Check for overly specific patterns
        for key, value in detection.items():
            if isinstance(value, dict):
                for field, val in value.items():
                    if isinstance(val, str) and len(val) > 100:
                        maint_score -= 10
                        improvements.append(
                            f"Consider breaking up long pattern in {field}"
                        )
        
        # Check for filters
        if not any('filter' in k for k in detection.keys()):
            maint_score -= 20
            improvements.append("Add filter for known false positives")
        
        return RuleQualityScore(
            rule_id=rule.get('id', 'unknown'),
            accuracy_score=70,  # Requires testing to determine
            coverage_score=70,  # Requires testing
            performance_score=80,  # Requires benchmarking
            maintainability_score=maint_score,
            documentation_score=doc_score,
            false_positive_rate=0.0,  # Unknown
            true_positive_samples=0,  # Unknown
            avg_query_time_ms=0.0,  # Unknown
            improvements=improvements
        )
```

## Mental Model

Roth approaches detection engineering by asking:

1. **Is this portable?** Can it work across SIEMs?
2. **Is this documented?** Metadata, references, false positives
3. **Is this testable?** Can we validate it works?
4. **Is this shareable?** Can the community benefit?
5. **Is this maintainable?** Will it survive updates?

## Signature Roth Moves

- Sigma rules for portable detection
- YARA rules for binary/memory patterns
- Comprehensive rule metadata
- Community sharing and collaboration
- Detection-as-code in version control
- Continuous rule quality improvement
