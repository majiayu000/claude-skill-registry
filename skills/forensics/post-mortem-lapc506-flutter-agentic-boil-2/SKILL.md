# 📋 Skill: Post-Mortem Process

## 📋 Metadata

| Atributo | Valor |
|----------|-------|
| **ID** | `sre-post-mortem` |
| **Nivel** | 🔴 Avanzado |
| **Versión** | 1.0.0 |
| **Keywords** | `post-mortem`, `postmortem`, `incident-review`, `blameless`, `lessons-learned`, `root-cause-analysis` |
| **Referencia** | [Google SRE - Postmortem Culture](https://sre.google/workbook/postmortem-culture/), [Blameless Postmortems](https://www.blameless.com/blog/blameless-postmortem) |

## 🔑 Keywords para Invocación

- `post-mortem`
- `postmortem`
- `incident-review`
- `blameless`
- `lessons-learned`
- `root-cause-analysis`
- `incident-analysis`
- `@skill:post-mortem`

### Ejemplos de Prompts

```
Crea un post-mortem para el incidente de ayer
```

```
Implementa proceso de post-mortem blameless
```

```
Genera template de post-mortem con timeline y action items
```

```
@skill:post-mortem - Proceso completo de análisis de incidentes
```

## 📖 Descripción

Un post-mortem es un análisis estructurado y blameless de un incidente que busca entender qué pasó, por qué pasó, y cómo prevenir que vuelva a ocurrir. Este skill cubre la metodología completa de post-mortems, templates, mejores prácticas, y herramientas para facilitar el proceso.

### ✅ Cuándo Usar Este Skill

- Después de incidentes críticos (SEV1, SEV2)
- Cuando se consume error budget significativo
- Incidentes que afectan múltiples usuarios
- Incidentes que requieren escalación
- Para cumplir con compliance requirements
- Cuando hay patrones recurrentes de incidentes

### ❌ Cuándo NO Usar Este Skill

- Incidentes menores sin impacto (SEV4)
- Problemas resueltos en < 5 minutos sin impacto
- Incidentes de mantenimiento planificados
- Cuando no hay tiempo para análisis adecuado

## 🏗️ Proceso de Post-Mortem

```
┌─────────────────┐
│ Incident Occurs │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Incident Resolved│
└────────┬────────┘
         │
         │ (Within 24-48 hours)
         ▼
┌─────────────────┐
│ Schedule Meeting │
│ (All Stakeholders)│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Collect Data    │
│ - Logs          │
│ - Metrics       │
│ - Timeline      │
│ - Testimonies   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Write Draft     │
│ Post-Mortem     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Review Meeting  │
│ (Blameless)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Finalize &      │
│ Publish         │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Track Action    │
│ Items           │
└─────────────────┘
```

## 💻 Implementación

### 1. Post-Mortem Template

```markdown
# Post-Mortem: [Incident Title]

**Incident ID:** [INC-YYYYMMDD-HHMMSS]  
**Date:** [Date]  
**Duration:** [Start Time] - [End Time] (X minutes/hours)  
**Severity:** [SEV1/SEV2/SEV3]  
**Affected Services:** [Service names]  
**On-Call Engineer:** [Name]  
**Post-Mortem Lead:** [Name]  
**Status:** [Draft/Review/Final]

---

## Executive Summary

[2-3 sentence summary for leadership. What happened, impact, and resolution.]

**TL;DR:** [One sentence summary]

---

## Impact

### User Impact
- **Users Affected:** [Number or percentage]
- **Geographic Impact:** [Regions affected]
- **Feature Impact:** [Which features were unavailable]

### Business Impact
- **Revenue Impact:** [If applicable, estimated $]
- **SLA Breach:** [Yes/No - which SLA]
- **Error Budget Consumption:** [X% of monthly budget]
- **Customer Complaints:** [Number]

### Technical Impact
- **Services Down:** [List]
- **Data Loss:** [Yes/No - details]
- **Performance Degradation:** [Metrics]

---

## Timeline

| Time (UTC) | Event | Actor | Notes |
|------------|-------|-------|-------|
| 10:00 AM | Alert fired: HighErrorRate | Prometheus | Error rate > 5% |
| 10:02 AM | On-call engineer acknowledged | Engineer A | PagerDuty notification |
| 10:05 AM | Initial investigation started | Engineer A | Checking logs |
| 10:10 AM | Identified pattern in logs | Engineer A | Database connection errors |
| 10:15 AM | Root cause identified | Engineer A | Connection pool exhaustion |
| 10:20 AM | Mitigation deployed | Engineer B | Increased pool size |
| 10:25 AM | Service restored | System | Metrics normalized |
| 10:30 AM | Incident resolved | Engineer A | All systems healthy |

**Key Milestones:**
- **Detection Time:** 10:00 AM
- **Response Time:** 2 minutes
- **Time to Identify:** 15 minutes
- **Time to Mitigate:** 20 minutes
- **Time to Resolve:** 30 minutes
- **Total Downtime:** 30 minutes

---

## Root Cause Analysis

### Primary Root Cause

[Detailed explanation of what caused the incident. Use the "5 Whys" technique if applicable.]

**What Happened:**
[Description of the immediate cause]

**Why It Happened:**
[Underlying technical reason]

**Why That Happened:**
[Deeper systemic reason]

### Contributing Factors

1. **[Factor 1]**
   - **Impact:** [How it contributed]
   - **Why it existed:** [Systemic reason]

2. **[Factor 2]**
   - **Impact:** [How it contributed]
   - **Why it existed:** [Systemic reason]

3. **[Factor 3]**
   - **Impact:** [How it contributed]
   - **Why it existed:** [Systemic reason]

### Detection Gaps

- [What we should have detected earlier]
- [Why we didn't detect it]
- [What monitoring/metrics were missing]

---

## Resolution

### Immediate Actions Taken

1. **[Action 1]**
   - **Who:** [Name]
   - **When:** [Time]
   - **Result:** [Outcome]

2. **[Action 2]**
   - **Who:** [Name]
   - **When:** [Time]
   - **Result:** [Outcome]

### Long-term Fix

[What was done to permanently resolve the issue]

---

## Action Items

### Immediate (Next 24 hours)
- [ ] **Item 1** - Owner: [Name] - Due: [Date]
  - Description: [Details]
- [ ] **Item 2** - Owner: [Name] - Due: [Date]
  - Description: [Details]

### Short-term (Next week)
- [ ] **Item 1** - Owner: [Name] - Due: [Date]
  - Description: [Details]
- [ ] **Item 2** - Owner: [Name] - Due: [Date]
  - Description: [Details]

### Long-term (Next month)
- [ ] **Item 1** - Owner: [Name] - Due: [Date]
  - Description: [Details]
- [ ] **Item 2** - Owner: [Name] - Due: [Date]
  - Description: [Details]

**Action Item Tracking:**
- Total Items: [X]
- Completed: [Y]
- In Progress: [Z]
- Not Started: [W]

---

## Lessons Learned

### What Went Well ✅

1. **[Positive aspect 1]**
   - **Why it helped:** [Explanation]
   - **How to replicate:** [Actionable steps]

2. **[Positive aspect 2]**
   - **Why it helped:** [Explanation]
   - **How to replicate:** [Actionable steps]

### What Could Be Improved 🔄

1. **[Improvement 1]**
   - **Current state:** [What happened]
   - **Desired state:** [What should happen]
   - **How to improve:** [Actionable steps]

2. **[Improvement 2]**
   - **Current state:** [What happened]
   - **Desired state:** [What should happen]
   - **How to improve:** [Actionable steps]

### Surprises 🤔

- [Unexpected behavior or findings]
- [Things we learned about the system]

---

## Prevention

### How to Prevent This Incident

1. **[Prevention measure 1]**
   - **Type:** [Monitoring/Process/Code/Infrastructure]
   - **Priority:** [High/Medium/Low]
   - **Effort:** [Small/Medium/Large]

2. **[Prevention measure 2]**
   - **Type:** [Monitoring/Process/Code/Infrastructure]
   - **Priority:** [High/Medium/Low]
   - **Effort:** [Small/Medium/Large]

### Similar Incidents

- [Link to related post-mortems]
- [Patterns identified]

---

## Follow-up

### Post-Mortem Review

- **Scheduled Date:** [Date]
- **Participants:** [Names]
- **Status:** [Scheduled/Completed]

### Action Item Review

- **Next Review Date:** [Date]
- **Owner:** [Name]
- **Last Updated:** [Date]

### Communication

- **Internal:** [Who was notified]
- **External:** [Customer communication if applicable]
- **Status Updates:** [Where updates were posted]

---

## Metrics

### Incident Metrics

- **MTTR (Mean Time To Resolution):** [X minutes]
- **MTTD (Mean Time To Detection):** [X minutes]
- **MTTI (Mean Time To Identify):** [X minutes]
- **MTTM (Mean Time To Mitigate):** [X minutes]

### Historical Comparison

- **Similar incidents in last 6 months:** [Number]
- **Trend:** [Improving/Stable/Worsening]

---

## Appendix

### Logs & Evidence

- [Links to relevant logs]
- [Screenshots of dashboards]
- [Metrics graphs]

### Related Documentation

- [Runbooks used]
- [Related post-mortems]
- [Design documents]

### Team Feedback

- [Quotes from team members]
- [Additional context]

---

**Document Version:** 1.0  
**Last Updated:** [Date]  
**Next Review:** [Date]
```

### 2. Post-Mortem Automation Script

```python
# postmortem/generator.py
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict
from enum import Enum
import json

class IncidentSeverity(Enum):
    SEV1 = "critical"  # Service down
    SEV2 = "high"      # Major degradation
    SEV3 = "medium"    # Minor issues
    SEV4 = "low"       # Informational

@dataclass
class TimelineEvent:
    time: datetime
    event: str
    actor: str
    notes: Optional[str] = None

@dataclass
class ActionItem:
    id: str
    description: str
    owner: str
    due_date: datetime
    priority: str  # immediate, short-term, long-term
    status: str = "not-started"  # not-started, in-progress, completed
    completed_date: Optional[datetime] = None

@dataclass
class PostMortem:
    incident_id: str
    title: str
    date: datetime
    start_time: datetime
    end_time: datetime
    duration_minutes: int
    severity: IncidentSeverity
    affected_services: List[str]
    on_call_engineer: str
    post_mortem_lead: str
    status: str = "draft"  # draft, review, final
    
    # Impact
    users_affected: Optional[int] = None
    revenue_impact: Optional[float] = None
    sla_breach: bool = False
    error_budget_consumption: Optional[float] = None
    
    # Content
    executive_summary: str = ""
    root_cause: str = ""
    contributing_factors: List[str] = field(default_factory=list)
    resolution: str = ""
    timeline: List[TimelineEvent] = field(default_factory=list)
    action_items: List[ActionItem] = field(default_factory=list)
    lessons_learned: Dict[str, List[str]] = field(default_factory=dict)
    
    # Metrics
    mttr_minutes: Optional[int] = None
    mttd_minutes: Optional[int] = None
    mtti_minutes: Optional[int] = None
    mttm_minutes: Optional[int] = None

class PostMortemGenerator:
    def __init__(self):
        self.template_path = "templates/postmortem.md"
    
    def generate(self, postmortem: PostMortem) -> str:
        """Generate post-mortem document from data structure"""
        with open(self.template_path, 'r') as f:
            template = f.read()
        
        # Replace template variables
        content = template.replace("{{INCIDENT_ID}}", postmortem.incident_id)
        content = content.replace("{{TITLE}}", postmortem.title)
        content = content.replace("{{DATE}}", postmortem.date.strftime("%Y-%m-%d"))
        content = content.replace("{{DURATION}}", f"{postmortem.duration_minutes} minutes")
        content = content.replace("{{SEVERITY}}", postmortem.severity.value)
        content = content.replace("{{AFFECTED_SERVICES}}", ", ".join(postmortem.affected_services))
        content = content.replace("{{EXECUTIVE_SUMMARY}}", postmortem.executive_summary)
        content = content.replace("{{ROOT_CAUSE}}", postmortem.root_cause)
        content = content.replace("{{RESOLUTION}}", postmortem.resolution)
        
        # Generate timeline table
        timeline_table = self._generate_timeline_table(postmortem.timeline)
        content = content.replace("{{TIMELINE}}", timeline_table)
        
        # Generate action items
        action_items = self._generate_action_items(postmortem.action_items)
        content = content.replace("{{ACTION_ITEMS}}", action_items)
        
        return content
    
    def _generate_timeline_table(self, events: List[TimelineEvent]) -> str:
        """Generate markdown table from timeline events"""
        rows = ["| Time | Event | Actor | Notes |", "|------|-------|-------|-------|"]
        for event in sorted(events, key=lambda e: e.time):
            rows.append(f"| {event.time.strftime('%H:%M %p')} | {event.event} | {event.actor} | {event.notes or ''} |")
        return "\n".join(rows)
    
    def _generate_action_items(self, items: List[ActionItem]) -> str:
        """Generate action items list"""
        sections = {
            "immediate": [],
            "short-term": [],
            "long-term": []
        }
        
        for item in items:
            sections[item.priority].append(item)
        
        output = []
        for priority, title in [("immediate", "Immediate (Next 24 hours)"),
                                ("short-term", "Short-term (Next week)"),
                                ("long-term", "Long-term (Next month)")]:
            if sections[priority]:
                output.append(f"### {title}")
                for item in sections[priority]:
                    status_icon = "✅" if item.status == "completed" else "⏳" if item.status == "in-progress" else "📋"
                    output.append(f"- {status_icon} **{item.description}** - Owner: {item.owner} - Due: {item.due_date.strftime('%Y-%m-%d')}")
        
        return "\n".join(output)
    
    def export_json(self, postmortem: PostMortem) -> str:
        """Export post-mortem as JSON"""
        data = {
            "incident_id": postmortem.incident_id,
            "title": postmortem.title,
            "date": postmortem.date.isoformat(),
            "severity": postmortem.severity.value,
            "affected_services": postmortem.affected_services,
            "timeline": [
                {
                    "time": event.time.isoformat(),
                    "event": event.event,
                    "actor": event.actor,
                    "notes": event.notes
                }
                for event in postmortem.timeline
            ],
            "action_items": [
                {
                    "id": item.id,
                    "description": item.description,
                    "owner": item.owner,
                    "due_date": item.due_date.isoformat(),
                    "priority": item.priority,
                    "status": item.status
                }
                for item in postmortem.action_items
            ]
        }
        return json.dumps(data, indent=2)

# Example usage
if __name__ == "__main__":
    generator = PostMortemGenerator()
    
    postmortem = PostMortem(
        incident_id="INC-20240115-1000",
        title="Database Connection Pool Exhaustion",
        date=datetime(2024, 1, 15),
        start_time=datetime(2024, 1, 15, 10, 0),
        end_time=datetime(2024, 1, 15, 10, 30),
        duration_minutes=30,
        severity=IncidentSeverity.SEV2,
        affected_services=["user-service", "payment-service"],
        on_call_engineer="engineer@example.com",
        post_mortem_lead="lead@example.com",
        executive_summary="Database connection pool was exhausted due to unclosed connections.",
        root_cause="Connection leaks in payment processing code",
        timeline=[
            TimelineEvent(datetime(2024, 1, 15, 10, 0), "Alert fired", "Prometheus"),
            TimelineEvent(datetime(2024, 1, 15, 10, 2), "Engineer acknowledged", "Engineer A"),
            TimelineEvent(datetime(2024, 1, 15, 10, 30), "Incident resolved", "Engineer A"),
        ],
        action_items=[
            ActionItem("AI-001", "Fix connection leaks", "dev@example.com", datetime(2024, 1, 16), "immediate"),
            ActionItem("AI-002", "Add connection pool monitoring", "sre@example.com", datetime(2024, 1, 22), "short-term"),
        ]
    )
    
    markdown = generator.generate(postmortem)
    print(markdown)
```

### 3. Blameless Post-Mortem Guidelines

```markdown
# Blameless Post-Mortem Guidelines

## Principles

### 1. Focus on Systems, Not People
- **DO:** "The deployment process didn't catch the configuration error"
- **DON'T:** "John forgot to check the configuration"

### 2. Assume Good Intentions
- Everyone was trying to do the right thing
- Mistakes happen in complex systems
- Focus on how the system allowed the mistake

### 3. Learn, Don't Blame
- Goal is improvement, not punishment
- Understand why decisions were made
- Identify systemic issues

### 4. Be Specific and Factual
- Use data and evidence
- Avoid speculation
- Document what actually happened

## Language Guidelines

### ✅ Good Language
- "The system failed to..."
- "The process didn't catch..."
- "The monitoring didn't alert on..."
- "We discovered that..."
- "The design allowed..."

### ❌ Blaming Language
- "X person made a mistake"
- "X team should have..."
- "X person forgot to..."
- "X person didn't follow procedure"
- "X person's fault"

## Meeting Structure

1. **Set Ground Rules** (5 min)
   - Remind everyone: blameless culture
   - Focus on learning
   - No finger-pointing

2. **Timeline Construction** (20 min)
   - Build timeline together
   - Everyone adds their perspective
   - No judgment, just facts

3. **Root Cause Discussion** (30 min)
   - Use "5 Whys" technique
   - Ask "why" until you reach systemic cause
   - Focus on processes, not people

4. **Action Items** (15 min)
   - Identify improvements
   - Assign owners
   - Set deadlines

5. **Wrap-up** (5 min)
   - Thank everyone
   - Remind about follow-up
   - Schedule review meeting
```

### 4. Post-Mortem Checklist

```markdown
# Post-Mortem Checklist

## Before the Meeting
- [ ] Incident is fully resolved
- [ ] All stakeholders notified
- [ ] Meeting scheduled (within 24-48 hours)
- [ ] Data collected:
  - [ ] Logs from all services
  - [ ] Metrics and dashboards
  - [ ] Timeline of events
  - [ ] Chat logs (Slack, etc.)
  - [ ] Deployment history
- [ ] Draft template prepared
- [ ] Meeting room/video link set up

## During the Meeting
- [ ] Ground rules established (blameless)
- [ ] Timeline constructed
- [ ] Root cause identified
- [ ] Contributing factors discussed
- [ ] Action items created
- [ ] Lessons learned captured
- [ ] Next steps agreed upon

## After the Meeting
- [ ] Post-mortem document finalized
- [ ] Action items assigned and tracked
- [ ] Post-mortem published (internal wiki/docs)
- [ ] Team notified of publication
- [ ] Follow-up review scheduled
- [ ] Related teams notified if applicable
```

### 5. Post-Mortem Metrics Dashboard

```yaml
# grafana/postmortem-dashboard.json
{
  "dashboard": {
    "title": "Post-Mortem Metrics",
    "panels": [
      {
        "title": "MTTR by Severity",
        "targets": [
          {
            "expr": "avg(postmortem_mttr_minutes) by (severity)",
            "legendFormat": "{{severity}}"
          }
        ],
        "type": "graph"
      },
      {
        "title": "Action Items Completion Rate",
        "targets": [
          {
            "expr": "sum(postmortem_action_items_completed) / sum(postmortem_action_items_total) * 100",
            "legendFormat": "Completion Rate"
          }
        ],
        "type": "stat"
      },
      {
        "title": "Post-Mortems by Month",
        "targets": [
          {
            "expr": "count(postmortem_total) by (month)",
            "legendFormat": "{{month}}"
          }
        ],
        "type": "graph"
      },
      {
        "title": "Top Contributing Factors",
        "targets": [
          {
            "expr": "topk(10, count(postmortem_contributing_factor) by (factor))",
            "legendFormat": "{{factor}}"
          }
        ],
        "type": "table"
      }
    ]
  }
}
```

## 🎯 Mejores Prácticas

### 1. Timing

✅ **DO:**
- Schedule within 24-48 hours of incident
- While memories are fresh
- Before people move on to other work

❌ **DON'T:**
- Wait more than a week
- Schedule during high-stress periods
- Rush the process

### 2. Participation

✅ **DO:**
- Include all stakeholders
- Include people who made decisions
- Invite people who can provide context
- Keep group size manageable (5-10 people)

❌ **DON'T:**
- Exclude people who were involved
- Make it a blame session
- Include people who weren't involved

### 3. Documentation

✅ **DO:**
- Write clearly and concisely
- Use data and evidence
- Include timeline with timestamps
- Make action items specific and trackable
- Publish where everyone can access

❌ **DON'T:**
- Use vague language
- Skip important details
- Make action items vague
- Hide post-mortems

### 4. Follow-up

✅ **DO:**
- Track action items to completion
- Review post-mortems periodically
- Share learnings across teams
- Update runbooks based on learnings
- Measure improvement over time

❌ **DON'T:**
- Create action items and forget them
- Let post-mortems sit unread
- Keep learnings siloed
- Repeat the same mistakes

## 🚨 Troubleshooting

### Post-Mortem Not Happening

1. **Make it mandatory** for SEV1/SEV2 incidents
2. **Automate scheduling** after incident resolution
3. **Track compliance** as a metric
4. **Make it easy** with templates and tools

### Blame Culture

1. **Set ground rules** at start of every meeting
2. **Call out blaming language** when it happens
3. **Focus on systems** in all discussions
4. **Lead by example** from management

### Action Items Not Completed

1. **Assign clear owners** with deadlines
2. **Track in project management** tool
3. **Review in team meetings**
4. **Escalate if overdue**

### Low-Quality Post-Mortems

1. **Provide training** on post-mortem process
2. **Review and provide feedback**
3. **Share examples** of good post-mortems
4. **Make templates** more detailed

## 📚 Recursos Adicionales

- [Google SRE - Postmortem Culture](https://sre.google/workbook/postmortem-culture/)
- [Blameless Postmortems](https://www.blameless.com/blog/blameless-postmortem)
- [Atlassian Post-Mortem Guide](https://www.atlassian.com/incident-management/handbook/postmortems)
- [Post-Mortem Templates Collection](https://github.com/dastergon/awesome-sre#post-mortem)

---

**Versión:** 1.0.0  
**Última actualización:** Diciembre 2025  
**Total líneas:** 800+

