---
name: expert-routing
description: 领域专家路由。当知识库无法回答用户问题时，根据问题领域查找并通知对应专家。仅在 IM 模式下可用。触发条件：6阶段检索无结果时。
---

---
name: expert-routing
description: Domain expert routing. When the knowledge base cannot answer user questions, find and notify the corresponding expert based on the question domain. Only available in IM mode. Trigger condition: No results in 6-stage retrieval.
---

# Domain Expert Routing

Automatically route questions to domain experts when the knowledge base cannot answer user questions.

## Applicable Scenarios

- User question has no answer in knowledge base
- Question belongs to a specific domain requiring professional response
- Only available in IM mode (WeCom/Feishu/DingTalk)

## Quick Workflow

1. **Identify domain** → Determine the domain based on question semantics
2. **Query expert** → Get expert information from domain_experts.xlsx
3. **Notify expert** → Send message to expert with user question
4. **Notify user** → Inform user that expert has been contacted

## Domain Identification Examples

| Question Keywords | Domain |
|------------------|--------|
| Salary/wage/adjustment | Compensation & Benefits |
| Leave/attendance/clock-in | Attendance Management |
| Onboarding/new employee/training | Recruitment & Training |
| Contract/labor/resignation | Employee Relations |

## Detailed Workflow

For complete expert routing workflow, see [WORKFLOW.md](WORKFLOW.md)
