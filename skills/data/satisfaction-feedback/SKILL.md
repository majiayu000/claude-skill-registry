---
name: satisfaction-feedback
description: 处理用户满意度反馈。用户回复"满意"/"不满意"时，更新 FAQ 使用计数或记录 BADCASE。触发词：满意/不满意/解决了/���解决/谢谢。
---

---
name: satisfaction-feedback
description: Handle user satisfaction feedback. When users respond with "satisfied"/"unsatisfied", update FAQ usage count or record BADCASE. Trigger words: satisfied/unsatisfied/resolved/not resolved/thanks/满意/不满意/解决了/没解决/谢谢.
---

# Satisfaction Feedback Processing

Process user satisfaction feedback and update FAQ or record issues based on the answer source.

## Trigger Words

**Satisfied**: satisfied, resolved, thanks, understood, ok, got it, clear, I see, 满意, 解决了, 谢谢, 明白了, 好的, 懂了, 清楚了, 知道了
**Unsatisfied**: unsatisfied, not resolved, wrong, incorrect, doesn't work, 不满意, 没解决, 不对, 错了, 不行

## Processing Logic

Process feedback based on **answer source from previous round** (metadata `answer_source`):

| Answer Source | Satisfied Feedback | Unsatisfied Feedback |
|--------------|-------------------|---------------------|
| FAQ | Increment usage count | Remove entry + Record BADCASE |
| Knowledge base file | Add to FAQ | Record BADCASE |

## Key Principles

1. **Use file locks**: Must use `SharedKBAccess` file locks when updating FAQ.md and BADCASE.md
2. **Concurrency safety**: Avoid data conflicts when multiple users operate simultaneously
3. **Status update**: Set session_status to "resolved" after satisfied feedback

## Detailed Operations

For FAQ add/delete/modify operation details, see [FAQ_OPERATIONS.md](FAQ_OPERATIONS.md)
