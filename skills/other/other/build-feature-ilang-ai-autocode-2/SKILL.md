---
name: build-feature
description: Build one feature at a time. Complete it fully before moving to the next.
---

# Build Feature

For each feature in the plan:
1. Write the code
2. Silently run auto-quality checks (activate auto-quality skill)
3. Verify it works
4. Tell user what was completed: "登录功能做好了。用户可以注册、登录、登出。"
5. Move to next feature

Rules:
- ONE feature at a time. Never work on two simultaneously.
- Each feature must work independently before integrating
- If a feature is too big, break it down further (activate plan-breakdown)
- Show progress after each feature: "第3步完成，还剩2步。"
