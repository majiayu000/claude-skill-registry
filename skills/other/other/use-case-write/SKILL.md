---
name: use-case-write
description: Write a well-structured use-case document for PMTL_VN following the project's writing standards. Use when documenting a new feature's write-path, business flow, or risky operation.
argument-hint: <module-name> <use-case-description>
---

# Use-Case Writer (Viết Kịch bản Nghiệp vụ)

Viết use-case document cho: **$ARGUMENTS**

## Bước 1: Thu thập context

Đọc các file sau trước khi viết:
1. `design/baseline/writing-standards.md` — chuẩn viết của project
2. `design/<module>/contracts.md` — contracts của module liên quan
3. `design/<module>/module-map.md` — ownership và boundaries
4. File use-case gần nhất trong `design/<module>/use-cases/` — để follow style
5. `design/tracking/audit-policy.md` — audit events bắt buộc

## Bước 2: Hỏi nếu cần thêm thông tin

Nếu description chưa đủ rõ, hỏi:
- Actor là ai? (member / admin / super-admin / system)
- Preconditions là gì?
- Happy path cụ thể là gì?
- Failure cases quan trọng nhất là gì?

## Bước 3: Viết use-case theo template

Output phải là Markdown file tại:
`design/<module>/use-cases/<verb>-<object>.md`

---

## Template bắt buộc

```markdown
# Use-Case: <Verb> <Object>

## Owner module
`<module-name>` — [link contracts.md]

## Actor
- `<role>` — mô tả actor

## Preconditions (Điều kiện tiên quyết)
- ...

## Canonical records affected (Collections bị ảnh hưởng)
- `<collection>` — owned by `<module>` — write / read-only

## Happy path (Luồng thành công)

1. **Validate input** — Zod schema `<SchemaName>` check [list fields]
2. **Authorize** — `<policy-check>` (role gate + business rule)
3. **Check preconditions** — [specific invariants]
4. **Execute canonical write** — `<repository-method>()` on `<collection>`
5. **Audit** — `auditService.append(actor, '<module>.<action>', entityId, metadata)`
6. **Side effects** — [sync inline / outbox event `<event.type>`]
7. **Return** — `<ResponseDto>` via mapper

## Failure cases (Các trường hợp thất bại)

| Condition | Error code | HTTP | Recovery |
|---|---|---|---|
| ... | `invalid_body` | 400 | ... |
| ... | `forbidden` | 403 | ... |
| ... | `not_found` | 404 | ... |

## Audit events (Sự kiện audit bắt buộc)

| Action | Actor | Trigger |
|---|---|---|
| `<module>.<action>` | actorUserId | [describe when] |

## Rate-limit requirement
- [ ] Cần rate-limit: Yes / No
- Scope: per-IP / per-account / both
- Limit: <N> requests per <window>

## Outbox event (nếu có side effect quan trọng)
- Event type: `<module>.<entity>.<action>`
- Subscriber: `<downstream-module>`
- Mode: outbox-required (phase 2+) / sync-inline (phase 1)
- Xem: `tracking/outbox-event-taxonomy.md`

## Recovery path (nếu có derived data)
- Nếu <derived-field> drift: recompute từ <source-collection>
- Recovery API: `POST /api/admin/<module>/recompute-<field>` (nếu cần)

## Notes for AI/codegen
- [các rule cụ thể mà AI dễ implement sai]
```

---

## Tiêu chí chất lượng

Use-case đạt chuẩn khi:
- [ ] Happy path đủ chi tiết để code mà không cần hỏi thêm
- [ ] Tất cả failure cases quan trọng được list với error code cụ thể
- [ ] Audit events rõ ràng — không phải "maybe audit"
- [ ] Side effects rõ: sync hay outbox, event type cụ thể
- [ ] Không mơ hồ về ownership — collection nào owned by ai
- [ ] Không có logic mà chỉ TypeScript type enforce — phải runtime validate
- [ ] Nếu có derived data → có recovery path

## Output

Sau khi viết, hỏi:
"Anh muốn em tạo file này tại `design/<module>/use-cases/<name>.md` không?"

Sau khi confirm, tạo file và báo cáo:
- Path đã tạo
- Audit events cần implement
- Outbox events cần thêm vào taxonomy nếu có event mới
