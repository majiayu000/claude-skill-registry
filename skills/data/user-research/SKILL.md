---
name: discovery.user_research
phase: discovery
roles:
  - Product Designer
  - Product Manager
description: Plan and structure moderated or unmoderated user research sessions that target the given persona and objectives.
variables:
  required:
    - name: persona
      description: Primary persona or role for the research participants.
    - name: research_method
      description: Method such as interview, contextual inquiry, or usability test.
    - name: key_questions
      description: Comma-separated list of core learning goals to explore.
  optional:
    - name: product_area
      description: Feature, workflow, or journey under investigation.
    - name: success_metric
      description: North-star metric the research should influence.
outputs:
  - Research brief summarizing goals, hypotheses, and logistics.
  - Discussion guide with sections, timings, and probes.
  - Capture template for observations, quotes, and insights.
---

# Purpose
Provide a consistent prompt that quickly produces a research-ready briefing pack aligned with the broader discovery strategy.

# Pre-run Checklist
- ✅ Confirm recruiting pipeline or panel availability for the target persona.
- ✅ Align with stakeholders on the primary learning goals.
- ✅ Gather existing artifacts (journey maps, past studies) to inform prompts.

# Invocation Guidance
```bash
codex run --skill discovery.user_research \
  --vars "persona={{persona}}" \
         "research_method={{research_method}}" \
         "key_questions={{key_questions}}" \
         "product_area={{product_area}}" \
         "success_metric={{success_metric}}"
```

# Recommended Input Attachments
- Screens, prototypes, or scripts relevant to the study.
- Current hypotheses or assumptions document.

# Claude Workflow Outline
1. Summarize the research context, including method and product area.
2. Generate a research brief capturing purpose, hypotheses, participant criteria, logistics, and success measures.
3. Create a timed discussion guide with introduction, warm-up, core tasks, and wrap-up.
4. Provide an observation log template with slots for verbatim quotes and insights mapped to key questions.
5. Suggest follow-up synthesis rituals and share-outs.

# Output Template
```
# Research Brief
## Purpose
...

## Hypotheses & Key Questions
- Hypothesis:
- Key Question:

## Participant Criteria
- Role / Persona:
- Experience Level:
- Recruitment Notes:

## Logistics
- Method:
- Tools:
- Timeline:

---
# Discussion Guide
| Section | Time | Moderator Notes |
| --- | --- | --- |
| Introduction | 5 min | ... |

---
# Observation Log Template
| Participant | Scenario | Observation | Quote | Insight Tag |
| --- | --- | --- | --- | --- |
```

# Follow-up Actions
- Create tasks in your research tracker for recruiting, incentives, and scheduling.
- Set up a synthesis workshop with cross-functional partners.
- Archive recordings and notes in the shared research repository.
