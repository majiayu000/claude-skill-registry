---
name: experiments
description: |
  A/B tests, feature flags, gradual rollout experiments cho PikaRobot.
  TRIGGERS: "experiment", "A/B test", "feature flag", "gradual rollout", "thử nghiệm".
  NOT FOR: Full feature specs (→2_Define/), metrics tracking (→4_Measure/).
---
# Experiments

## Overview
Quản lý Experiments cho dự án PikaRobot.

## Core Principles
1. **Clarity** — Mọi output phải clear và actionable
2. **Evidence-Based** — Dựa trên data, không phải opinion
3. **Iterative** — Improve qua mỗi iteration
4. **Documented** — Mọi decision và rationale được ghi lại

## Best Practices

| Practice | Why | How | Anti-pattern |
|----------|-----|-----|-------------|
| Template First | Consistency + speed | Dùng template_output.md làm starting point | Blank page mỗi lần |
| Review Before Ship | Quality check | Peer review hoặc self-review sau 24h | Ship mà không review |
| Learn from Cases | Improve over time | Check problem-solving-use-cases/ trước khi bắt đầu | Lặp lại sai lầm cũ |

## Decision Framework
```
Khi cần ra quyết định trong area này:
1. Check existing cases (references/problem-solving-use-cases/)
2. Apply relevant framework (references/knowledge-base/)
3. Document decision + rationale
4. Set success criteria
5. Review sau 2-4 tuần
```

## Checklist
- [ ] Objective rõ ràng
- [ ] Template selected
- [ ] Past cases reviewed
- [ ] Output reviewed trước khi finalize
- [ ] Decision documented
- [ ] Follow-up scheduled

## Common Mistakes
- ❌ Bắt đầu từ zero mà không check existing work
- ❌ Không document decisions
- ❌ Skip review step
- ✅ Luôn build on existing knowledge

## References
→ `references/knowledge-base/` — Frameworks, guides
→ `references/problem-solving-use-cases/` — Real cases
→ `template_output.md` — Output template (nếu có)
