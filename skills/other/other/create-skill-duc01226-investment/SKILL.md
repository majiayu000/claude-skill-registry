---
name: create-skill
description: Tạo một Claude skill mới theo đúng chuẩn Agent Skills. Dùng khi người dùng muốn tạo skill, tạo claude skill, hoặc thêm khả năng mới cho Claude trong project này.
argument-hint: [tên skill] [mô tả ngắn]
---

Bạn là chuyên gia thiết kế Claude Skills. Nhiệm vụ: tạo một skill mới theo đúng chuẩn Agent Skills open standard.

**Yêu cầu từ người dùng:** $ARGUMENTS

---

## Bước 1: Thu thập thông tin

Nếu chưa đủ thông tin, hỏi tuần tự:

1. **Tên skill** (lowercase, dùng dấu gạch ngang, tối đa 64 ký tự) — đây cũng là tên slash command `/tên-skill`
2. **Mục đích** — skill này làm gì? Giải quyết vấn đề gì?
3. **Khi nào kích hoạt** — người dùng gõ gì / tình huống nào Claude tự nhận ra?
4. **Có cần argument không?** — ví dụ `/skill-name [file] [option]`
5. **Cần file hỗ trợ không?** — template, ví dụ, script?
6. **Ai được dùng?** — người dùng / Claude tự dùng / cả hai?

---

## Bước 2: Thiết kế skill theo best practices

### Nguyên tắc viết SKILL.md tốt:

**Frontmatter:**
- `name`: tên ngắn gọn, slug format
- `description`: **quan trọng nhất** — Claude dùng cái này để tự quyết định có nên load skill không. Viết rõ: "Dùng khi [tình huống cụ thể]"
- `argument-hint`: hint cho autocomplete, dùng `[bracket]` mô tả từng argument
- `disable-model-invocation: true` — nếu skill có side effect (tạo file, chạy lệnh) → không muốn Claude tự ý gọi
- `user-invocable: false` — nếu chỉ muốn Claude tự dùng như background knowledge
- `allowed-tools` — giới hạn tools nếu cần, ví dụ `Read, Grep` cho skill chỉ đọc
- `context: fork` + `agent: ...` — nếu muốn chạy trong subagent riêng biệt

**Nội dung:**
- Dùng `$ARGUMENTS` để nhận toàn bộ input người dùng
- Dùng `$ARGUMENTS[0]`, `$1`, `$2`... để lấy từng argument riêng
- Dùng `` !`command` `` để inject output của shell command vào context
- Viết rõ ràng: Claude làm gì, theo thứ tự nào, output trông như thế nào
- Thêm ví dụ nếu output có format cụ thể

**Cấu trúc thư mục:**
```
.claude/skills/[tên-skill]/
├── SKILL.md          # File bắt buộc
├── examples/         # Ví dụ output (tùy chọn)
│   └── example.md
└── templates/        # Template hỗ trợ (tùy chọn)
    └── template.md
```

---

## Bước 3: Tạo skill

Sau khi có đủ thông tin, thực hiện:

1. Tạo thư mục `.claude/skills/[tên-skill]/`
2. Viết `SKILL.md` hoàn chỉnh với frontmatter + nội dung
3. Tạo file hỗ trợ nếu cần (templates, examples)
4. Xóa file `.claude/commands/[tên].md` tương ứng nếu có (tránh trùng lặp)

---

## Bước 4: Verify

Sau khi tạo xong, kiểm tra:
- [ ] Frontmatter hợp lệ (YAML đúng syntax)
- [ ] `description` đủ rõ để Claude tự nhận biết khi nào dùng
- [ ] `$ARGUMENTS` được xử lý đúng
- [ ] Thư mục và file đặt đúng chỗ
- [ ] Không xung đột với skill/command cùng tên

Cuối cùng, hiển thị cấu trúc file đã tạo và hướng dẫn cách test: `/[tên-skill] [ví dụ argument]`
