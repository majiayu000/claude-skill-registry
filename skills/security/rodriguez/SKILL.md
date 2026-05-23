---
name: rodriguez-threat-hunter-playbook
description: Apply Roberto Rodriguez's threat hunting methodology with the Threat Hunter Playbook and HELK. Emphasizes documented hunts, open source infrastructure, and data-driven hunting. Use when building hunting programs or developing hunt playbooks.
---

# Roberto Rodriguez — Threat Hunter Playbook

## Overview

Roberto Rodriguez is a Principal Threat Researcher at Microsoft and creator of the Threat Hunter Playbook and HELK (Hunting ELK). His work democratized threat hunting by providing open-source infrastructure, documented methodologies, and reproducible hunt procedures.

## References

- **Threat Hunter Playbook**: https://threathunterplaybook.com/
- **HELK**: https://github.com/Cyb3rWard0g/HELK
- **GitHub**: https://github.com/Cyb3rWard0g
- **Open Threat Research**: https://github.com/OTRF

## Core Philosophy

> "Share knowledge, not just indicators."

> "If you can't reproduce it, you can't improve it."

> "The best defense is an educated community."

Rodriguez believes that threat hunting knowledge should be open, reproducible, and accessible. His playbooks document not just what to hunt, but how to think about hunting.

## Key Contributions

### Threat Hunter Playbook
Community-driven library of documented hunts mapped to ATT&CK, with queries, notebooks, and methodology.

### HELK (Hunting ELK)
Open source hunting platform combining Elasticsearch, Logstash, Kibana with Jupyter notebooks for interactive analysis.

### Mordor Datasets
Pre-recorded attack datasets for testing detections without needing a lab.

## When Implementing

### Always

- Document every hunt with methodology
- Map hunts to ATT&CK techniques
- Use Jupyter notebooks for reproducibility
- Share successful hunts with the team
- Test detections with Mordor datasets
- Build on community playbooks

### Never

- Hunt without a hypothesis
- Keep successful methodologies private
- Deploy without testing against known attacks
- Ignore the importance of data quality
- Skip documentation of findings

### Prefer

- Interactive notebooks over static queries
- Reproducible hunts over one-time searches
- Community playbooks as starting points
- Data-driven hypotheses over intuition
- Open source tools over vendor lock-in

## Implementation Patterns

### Hunt Playbook Structure

```python
# playbook.py
# Threat Hunter Playbook structure

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class DataSource:
    """Required data for the hunt"""
    name: str
    category: str              # e.g., "Process Monitoring"
    platforms: List[str]       # e.g., ["Windows"]
    collection_method: str     # e.g., "Sysmon Event 1"
    fields_required: List[str]

@dataclass
class AnalyticStep:
    """Single step in hunt analytics"""
    step_number: int
    description: str
    query: str
    query_language: str        # e.g., "KQL", "SPL", "SQL"
    expected_output: str
    interpretation: str

@dataclass
class HuntPlaybook:
    """Complete hunt playbook - Rodriguez style"""
    
    # Metadata
    id: str
    title: str
    description: str
    author: str
    created: datetime
    modified: datetime
    
    # ATT&CK Mapping
    tactics: List[str]
    techniques: List[str]
    
    # Hunt Details
    hypothesis: str
    technical_context: str     # Background on the technique
    
    # Requirements
    data_sources: List[DataSource]
    platforms: List[str]
    
    # Analytics
    analytics: List[AnalyticStep]
    
    # Validation
    mordor_datasets: List[str]  # Datasets for testing
    
    # Results
    expected_benign: List[str]
    known_bypasses: List[str]
    
    # References
    references: List[str]
    
    def to_jupyter_notebook(self) -> dict:
        """Export playbook as Jupyter notebook"""
        cells = []
        
        # Title cell
        cells.append({
            "cell_type": "markdown",
            "source": [
                f"# {self.title}\n",
                f"\n",
                f"**Author:** {self.author}\n",
                f"**Created:** {self.created}\n",
                f"\n",
                f"## ATT&CK Mapping\n",
                f"- **Tactics:** {', '.join(self.tactics)}\n",
                f"- **Techniques:** {', '.join(self.techniques)}\n"
            ]
        })
        
        # Hypothesis cell
        cells.append({
            "cell_type": "markdown",
            "source": [
                "## Hypothesis\n",
                f"\n{self.hypothesis}\n",
                "\n## Technical Context\n",
                f"\n{self.technical_context}\n"
            ]
        })
        
        # Analytics cells
        for analytic in self.analytics:
            # Description
            cells.append({
                "cell_type": "markdown",
                "source": [
                    f"### Step {analytic.step_number}: {analytic.description}\n",
                    f"\n{analytic.interpretation}\n"
                ]
            })
            
            # Query
            cells.append({
                "cell_type": "code",
                "source": [analytic.query]
            })
        
        return {
            "cells": cells,
            "metadata": {
                "kernelspec": {
                    "display_name": "PySpark",
                    "language": "python",
                    "name": "pyspark"
                }
            },
            "nbformat": 4,
            "nbformat_minor": 4
        }
    
    def validate_with_mordor(self) -> dict:
        """Instructions for validating with Mordor datasets"""
        return {
            "datasets": self.mordor_datasets,
            "instructions": [
                "1. Download Mordor dataset from https://mordordatasets.com/",
                "2. Import into your SIEM/hunting platform",
                f"3. Run analytics from this playbook",
                "4. Verify detection of simulated attack",
                "5. Document any required tuning"
            ]
        }


# Example playbook: Credential Dumping via LSASS
lsass_playbook = HuntPlaybook(
    id="WIN-190625024610",
    title="Credential Dumping via LSASS Memory Access",
    description="Detect credential dumping by monitoring processes "
                "that access LSASS memory",
    author="Roberto Rodriguez @Cyb3rWard0g",
    created=datetime(2024, 1, 15),
    modified=datetime(2024, 2, 20),
    
    tactics=["Credential Access"],
    techniques=["T1003.001"],
    
    hypothesis="Adversaries might be accessing LSASS process memory "
               "to extract credentials",
    
    technical_context="""
    The Local Security Authority Subsystem Service (LSASS) stores 
    credentials in memory for single sign-on. Attackers commonly 
    target LSASS using tools like Mimikatz, procdump, or comsvcs.dll.
    
    Windows Event ID 10 (Sysmon) captures process access events,
    including when a process reads another process's memory.
    """,
    
    data_sources=[
        DataSource(
            name="Process Access",
            category="Process Monitoring",
            platforms=["Windows"],
            collection_method="Sysmon Event ID 10",
            fields_required=[
                "SourceProcessGUID",
                "SourceImage",
                "TargetImage",
                "GrantedAccess"
            ]
        )
    ],
    
    platforms=["Windows"],
    
    analytics=[
        AnalyticStep(
            step_number=1,
            description="Find processes accessing LSASS",
            query="""
SELECT 
    SourceImage,
    TargetImage,
    GrantedAccess,
    COUNT(*) as AccessCount
FROM sysmon_events
WHERE EventCode = 10
    AND TargetImage LIKE '%lsass.exe'
    AND SourceImage NOT LIKE '%MsMpEng.exe'
    AND SourceImage NOT LIKE '%csrss.exe'
GROUP BY SourceImage, TargetImage, GrantedAccess
ORDER BY AccessCount DESC
            """,
            query_language="SQL (Spark)",
            expected_output="List of processes accessing LSASS with counts",
            interpretation="Look for unusual processes or high access counts"
        ),
        AnalyticStep(
            step_number=2,
            description="Analyze granted access rights",
            query="""
SELECT 
    SourceImage,
    GrantedAccess,
    CASE 
        WHEN GrantedAccess IN ('0x1010', '0x1410', '0x1438', '0x143a')
        THEN 'SUSPICIOUS - Memory Read Access'
        ELSE 'Likely Benign'
    END as Assessment
FROM sysmon_events
WHERE EventCode = 10
    AND TargetImage LIKE '%lsass.exe'
            """,
            query_language="SQL (Spark)",
            expected_output="Access rights analysis",
            interpretation="Memory read access (0x1010, 0x1410) indicates "
                          "potential credential dumping"
        )
    ],
    
    mordor_datasets=[
        "https://mordordatasets.com/notebooks/small/windows/06_credential_access/"
    ],
    
    expected_benign=[
        "Windows Defender (MsMpEng.exe)",
        "Client Server Runtime (csrss.exe)",
        "System process",
        "Antivirus products"
    ],
    
    known_bypasses=[
        "Direct syscalls (bypass Sysmon hooking)",
        "Targeting SAM/SECURITY registry instead",
        "Using MiniDumpWriteDump variations"
    ],
    
    references=[
        "https://attack.mitre.org/techniques/T1003/001/",
        "https://github.com/gentilkiwi/mimikatz",
        "https://threathunterplaybook.com/notebooks/windows/06_credential_access/"
    ]
)
```

### HELK-Style Hunting Platform

```python
# helk_hunt.py
# Hunting with HELK-style infrastructure

from dataclasses import dataclass
from typing import List, Dict, Any
import pandas as pd

@dataclass
class HuntingPlatform:
    """HELK-inspired hunting infrastructure"""
    
    elasticsearch_url: str
    spark_master: str
    jupyter_url: str
    
    def query_elastic(self, query: Dict) -> pd.DataFrame:
        """Query Elasticsearch and return DataFrame"""
        from elasticsearch import Elasticsearch
        
        es = Elasticsearch([self.elasticsearch_url])
        
        response = es.search(
            index="logs-*",
            body=query,
            size=10000
        )
        
        hits = response['hits']['hits']
        return pd.DataFrame([hit['_source'] for hit in hits])
    
    def hunt_with_spark(self, sql_query: str) -> pd.DataFrame:
        """Execute Spark SQL for large-scale hunting"""
        from pyspark.sql import SparkSession
        
        spark = SparkSession.builder \
            .master(self.spark_master) \
            .appName("ThreatHunting") \
            .getOrCreate()
        
        result = spark.sql(sql_query)
        return result.toPandas()


class InteractiveHunt:
    """Jupyter notebook-based interactive hunt"""
    
    def __init__(self, platform: HuntingPlatform):
        self.platform = platform
        self.findings = []
        self.timeline = []
    
    def search(self, query: str, time_range: str = "24h") -> pd.DataFrame:
        """Execute search and track in timeline"""
        self.timeline.append({
            'action': 'search',
            'query': query,
            'time_range': time_range
        })
        
        # Execute query
        elastic_query = {
            "query": {
                "bool": {
                    "must": [
                        {"query_string": {"query": query}},
                        {"range": {"@timestamp": {"gte": f"now-{time_range}"}}}
                    ]
                }
            }
        }
        
        return self.platform.query_elastic(elastic_query)
    
    def filter_noise(self, df: pd.DataFrame, 
                     column: str, 
                     exclude: List[str]) -> pd.DataFrame:
        """Filter known benign activity"""
        self.timeline.append({
            'action': 'filter',
            'column': column,
            'excluded': exclude
        })
        
        mask = ~df[column].isin(exclude)
        return df[mask]
    
    def pivot(self, df: pd.DataFrame, 
              pivot_field: str, 
              pivot_value: Any) -> pd.DataFrame:
        """Pivot investigation to related events"""
        self.timeline.append({
            'action': 'pivot',
            'field': pivot_field,
            'value': pivot_value
        })
        
        query = f'{pivot_field}:"{pivot_value}"'
        return self.search(query, time_range="7d")
    
    def mark_finding(self, description: str, 
                     evidence: pd.DataFrame,
                     severity: str):
        """Document a finding"""
        self.findings.append({
            'description': description,
            'evidence_count': len(evidence),
            'severity': severity,
            'evidence_sample': evidence.head(5).to_dict()
        })
    
    def generate_report(self) -> str:
        """Generate hunt report"""
        report = "# Hunt Report\n\n"
        
        report += "## Investigation Timeline\n\n"
        for i, step in enumerate(self.timeline, 1):
            report += f"{i}. **{step['action'].title()}**: "
            if step['action'] == 'search':
                report += f"Query: `{step['query']}`\n"
            elif step['action'] == 'filter':
                report += f"Excluded {len(step['excluded'])} values from {step['column']}\n"
            elif step['action'] == 'pivot':
                report += f"Pivoted on {step['field']}={step['value']}\n"
        
        report += "\n## Findings\n\n"
        for i, finding in enumerate(self.findings, 1):
            report += f"### Finding {i}: {finding['description']}\n"
            report += f"- **Severity**: {finding['severity']}\n"
            report += f"- **Evidence Count**: {finding['evidence_count']}\n\n"
        
        return report
```

### Mordor Dataset Integration

```python
# mordor_testing.py
# Test detections with Mordor attack datasets

from dataclasses import dataclass
from typing import List, Dict, Optional
import requests
import json

@dataclass
class MordorDataset:
    """Mordor attack dataset reference"""
    
    id: str
    name: str
    description: str
    attack_technique: str
    platform: str
    
    download_url: str
    file_format: str      # "json", "csv"
    
    # Expected indicators
    expected_processes: List[str]
    expected_files: List[str]
    expected_network: List[str]
    
    def download(self, output_path: str):
        """Download dataset"""
        response = requests.get(self.download_url)
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        return output_path
    
    def load_events(self) -> List[Dict]:
        """Load events from dataset"""
        response = requests.get(self.download_url)
        response.raise_for_status()
        
        if self.file_format == 'json':
            return response.json()
        else:
            # Handle other formats
            pass


class DetectionValidator:
    """Validate detections against Mordor datasets"""
    
    def __init__(self):
        self.results = []
    
    def test_detection(self, 
                       detection_query: str,
                       dataset: MordorDataset,
                       query_executor) -> dict:
        """Test if detection finds attack in Mordor data"""
        
        # Load Mordor dataset into test environment
        events = dataset.load_events()
        
        # Index events
        for event in events:
            query_executor.index(event)
        
        # Run detection
        matches = query_executor.search(detection_query)
        
        # Assess results
        result = {
            'dataset': dataset.id,
            'technique': dataset.attack_technique,
            'total_events': len(events),
            'matches': len(matches),
            'detected': len(matches) > 0,
            'expected_processes_found': self._check_indicators(
                matches, 'process.name', dataset.expected_processes
            )
        }
        
        self.results.append(result)
        return result
    
    def _check_indicators(self, 
                          matches: List[Dict], 
                          field: str,
                          expected: List[str]) -> List[str]:
        """Check which expected indicators were found"""
        found = []
        for match in matches:
            value = match.get(field)
            if value in expected:
                found.append(value)
        return list(set(found))
    
    def coverage_report(self) -> str:
        """Generate detection coverage report"""
        report = "# Detection Validation Report\n\n"
        
        detected = sum(1 for r in self.results if r['detected'])
        total = len(self.results)
        
        report += f"**Overall Detection Rate**: {detected}/{total} "
        report += f"({detected/total*100:.1f}%)\n\n"
        
        report += "## Results by Technique\n\n"
        for result in self.results:
            status = "✅" if result['detected'] else "❌"
            report += f"- {status} **{result['technique']}**: "
            report += f"{result['matches']} matches in {result['total_events']} events\n"
        
        return report
```

## Mental Model

Rodriguez approaches threat hunting by asking:

1. **Is this documented?** Can others reproduce this hunt?
2. **Is this mapped?** What ATT&CK technique does this address?
3. **Can I test this?** Do I have Mordor data to validate?
4. **Is this shareable?** Can the community benefit?
5. **Is this interactive?** Can I explore and pivot?

## Signature Rodriguez Moves

- Jupyter notebooks for reproducible hunts
- Mordor datasets for validation
- ATT&CK mapping for all playbooks
- Open source hunting infrastructure (HELK)
- Community playbook contribution
- Data-driven hypothesis generation
