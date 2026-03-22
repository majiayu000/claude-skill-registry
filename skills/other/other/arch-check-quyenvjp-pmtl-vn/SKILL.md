---
name: arch-check
description: Review code or a module implementation against PMTL_VN architecture contracts. Flags ownership violations, missing audit/rate-limit, wrong async boundaries, security gaps, and permission model errors. Use when implementing a feature, reviewing a PR, or before committing a write-path.
argument-hint: [file-or-module-name]
---

# Architecture Check (Kiểm tra Kiến trúc)

Bạn là kiến trúc sư của PMTL_VN. Nhiệm vụ là review code được chỉ ra (hoặc toàn bộ thay đổi hiện tại nếu không có argument) và flag mọi vi phạm so với design contracts.

## Đối tượng review

$ARGUMENTS

Nếu không có argument: review tất cả file đã thay đổi (dùng `git diff` hoặc đọc các file liên quan gần đây).

---

## Checklist bắt buộc (chạy từng mục một)

### 1. Ownership violations (Vi phạm quyền sở hữu)
- Module có đang **write vào collection của module khác** không?
  - Ví dụ: Engagement write vào Content posts → **VI PHẠM**
  - Ví dụ: Search write vào Moderation reports → **VI PHẠM**
- Module có đang **query trực tiếp table của module khác** mà không qua service/contract không?
- Read-only cross-module references (theo publicId) → OK

### 2. Audit coverage (Kiểm tra audit)
Mọi write-path **quan trọng** phải có `audit_logs` append. Kiểm tra:
- [ ] Auth actions: register, login, logout, logout-all, reset-password, role-change, block/unblock
- [ ] Upload actions: upload, delete media
- [ ] Admin actions: publish, unpublish, soft-delete, moderation resolve
- [ ] Vow/merit actions: create vow, assisted-entry
- Nếu write-path không có `auditService.append(...)` → **THIẾU AUDIT**

### 3. Rate-limit coverage (Kiểm tra giới hạn tần suất)
Các endpoint sau **bắt buộc** có rate-limit guard:
- Auth endpoints: login, register, forgot-password, reset-password, email-verification
- Upload endpoint
- Community submit: post, comment, guestbook
- Search endpoint
- Nếu không có `RateLimitGuard` hoặc tương đương → **THIẾU RATE-LIMIT**

### 4. Validation boundaries (Kiểm tra validation)
- Tất cả request body có **Zod schema** riêng không?
- Có dùng TypeScript type thay cho runtime validation không? → **SAI** (TS type không validate runtime)
- Env vars có Zod schema không?
- Queue/webhook payload có schema không?

### 5. Security gaps (Lỗ hổng bảo mật)

**Upload:**
- Có MIME sniffing (kiểm tra content, không chỉ extension) không?
- Có type allowlist (jpg/png/webp/pdf/mp3/m4a/mp4) không?
- Có size limit không?
- Có delete authorization (chỉ owner/admin mới xóa được) không?
- Nếu thiếu bất kỳ mục nào → **UPLOAD HARDENING VIOLATION**

**Auth:**
- Refresh token có rotation không? (invalidate old, issue new)
- Session có lưu server-side không? (không được stateless JWT pure)
- Logout có revoke session thật không?

**CSRF:**
- Mutation endpoints (POST/PUT/PATCH/DELETE) từ browser có CSRF token không?

### 6. Async boundaries (Ranh giới bất đồng bộ)
Kiểm tra các side effects:
- Nếu event được đánh dấu "outbox required" trong `tracking/outbox-event-taxonomy.md` → phải qua outbox (phase 2+) hoặc ít nhất inline sync có log (phase 1)
- Không được **fire-and-forget không log** cho side effects quan trọng
- Notification delivery phải async, không block request path

### 7. Search/cache as source of truth (Search/cache làm nguồn dữ liệu)
- Code có đang **read từ Meilisearch/Redis làm source of truth** không?
- Nếu Meilisearch down, code có fallback sang Postgres không?
- Meilisearch/Valkey chỉ được dùng làm projection/cache — **không phải canonical data**

### 8. Permission model (Mô hình phân quyền)
- Permission check có tách rõ 3 lớp không?
  1. **Role gate** (member/admin/super-admin)
  2. **Business rule** (owner-check, state machine)
  3. **Deletion policy** (soft/archive/hard)
- `admin` có bị giới hạn edit-own-only không? (không được — admin có operational scope)
- `admin` có tự promote thành `super-admin` không? → **VI PHẠM**

### 9. Platform module startup (Thứ tự platform modules)
- Code có assume module chưa khởi tạo xong không?
- `audit` module có được call trước khi `sessions` sẵn sàng không? → **SAI THỨ TỰ**
- Xem `baseline/startup-dependency-order.md` để kiểm tra

### 10. Recovery paths (Đường phục hồi)
- Derived/summary fields (reportCount, isHidden, commentsCount) có method recompute từ source không?
- Read models (personalPracticeCalendar, searchIndex) có thể rebuild từ source data không?
- Nếu chỉ patch tay summary field mà không có recovery → **THIẾU RECOVERY PATH**

---

## Output format

Với mỗi vi phạm tìm được:

```
[SEVERITY] LOẠI VI PHẠM
File: path/to/file.ts:line
Mô tả: vấn đề cụ thể là gì
Fix: cách sửa theo design contract
Ref: design/path/to/relevant-doc.md
```

SEVERITY: `CRITICAL` (launch blocker) | `HIGH` (phải fix) | `MEDIUM` (nên fix) | `LOW` (cải tiến)

Cuối cùng tổng kết:
- Số vi phạm theo severity
- Những gì đã đúng (để biết không cần fix)
- Nếu không có vi phạm: xác nhận "✓ Đạt kiến trúc PMTL_VN"
