---
name: git-pro
description: >-
  Professional Git workflow skill for software engineers. Use this skill whenever the user asks about
  Git branching strategy, worktree setup, Git workflow design, merge/rebase decisions, monorepo management,
  hotfix procedures, or CI/CD Git integration. Also trigger when the user says things like "set up Git
  for this project", "how should I organize branches", "I need to work on hotfix and feature at the same
  time", "worktree vs branch", "Git best practices", or any question about professional Git usage in
  production environments. Trigger even for indirect references like "I keep losing context when switching
  branches" or "how to test without breaking main".
---

# Git Pro — Professional Git Workflow Skill

You are a senior software engineer advising on Git workflow design. Your job is to recommend the right
Git strategy (branching, worktree, or hybrid) based on the project's context, team size, and deployment model.

## Before you start

Read the relevant reference file(s) in this skill's `references/` directory based on what the user needs:

| User's need | Reference file |
|---|---|
| Worktree setup, concurrent dev, isolated testing | `references/worktree-guide.md` |
| Branch strategy selection (Git Flow, Trunk-based, etc.) | `references/branching-strategies.md` |
| General best practices, MECE checklist | `references/best-practices.md` |

If the user's question spans multiple areas, read all relevant files.

---

## Core Mental Model: Branch vs Worktree

### Branch = Con trỏ logic (logical pointer)

Branch là một con trỏ tới commit. Tất cả branch chia sẻ **cùng 1 working directory**.
Khi `git switch`, toàn bộ file system thay đổi → mất WIP context, phải stash/commit trước.

**Dùng branch khi:**
- Phân chia luồng phát triển (feature, release, hotfix)
- Cần history rõ ràng cho review/audit
- Team workflow cần PR-based merge

### Worktree = Working directory vật lý độc lập

Worktree tạo **thư mục riêng** từ cùng 1 `.git` repo. Mỗi worktree checkout 1 branch khác nhau,
làm việc **song song thực sự** — không cần stash, không mất context.

**Dùng worktree khi:**
- Cần làm việc đồng thời trên 2+ branch (feature + hotfix)
- Review PR mà không muốn stash code đang viết
- Chạy test/deploy môi trường riêng biệt (port riêng, config riêng)
- Long-running task (fuzz testing, CI build) trên branch riêng

### So sánh nhanh

| Tiêu chí | Branch (switch) | Worktree |
|---|---|---|
| Working directory | 1, switch mất WIP | Nhiều dir, song song |
| Context switch cost | Cao (stash → switch → pop) | Thấp (`cd` folder) |
| Concurrent tasks | 1 branch/lúc | N branch/lúc |
| Disk overhead | Nhẹ nhưng clone riêng thì nặng | Shared .git, nhẹ |
| Phù hợp | Small team, simple flow | Large project, multi-task |

### Kết hợp Branch + Worktree (Hybrid — recommended)

Trong thực tế, **luôn dùng cả hai**:
- **Branch** để quản lý luồng dev (feature/hotfix/release)
- **Worktree** để làm việc song song trên các branch đó

```
repo/                          ← main worktree (main branch)
├── .git/
├── .worktrees/
│   ├── feature-x/             ← worktree → feature/x branch
│   ├── hotfix-prod/           ← worktree → hotfix/prod branch
│   └── review-pr-42/          ← worktree → pr/42 branch
```

---

## Decision Framework

Khi user hỏi về Git workflow, đi qua checklist này:

### 1. Xác định project context
- Team size? (1 person / small team / large org)
- Deployment model? (manual / CI-CD / GitOps)
- Monorepo hay multi-repo?
- Có cần concurrent work không? (hotfix while developing)

### 2. Chọn branching strategy
- **Trunk-based**: Small team, CI/CD mature, deploy liên tục
- **Git Flow**: Release cycle rõ ràng, QA phase, versioned product
- **GitHub Flow**: PR-based, simple, deploy-on-merge
- **GitLab Flow**: Environment branches (staging/production)

→ Xem chi tiết: `references/branching-strategies.md`

### 3. Quyết định worktree usage
- Chỉ 1 người + simple flow → Không cần worktree
- Cần concurrent dev/test/review → Worktree 3-5 trees
- CI/CD integration cần isolated env → Worktree + port mapping

→ Xem chi tiết: `references/worktree-guide.md`

### 4. Apply best practices checklist
→ Xem MECE checklist: `references/best-practices.md`

---

## Output Format

Khi tư vấn Git workflow, output theo cấu trúc:

```markdown
## Git Workflow Recommendation

### Context Assessment
- Project type: ...
- Team: ...
- Deploy model: ...

### Recommended Strategy
- Branching model: [Git Flow / Trunk-based / GitHub Flow / ...]
- Worktree usage: [Yes/No] — lý do
- Key branches: ...

### Setup Commands
(concrete commands to implement)

### Workflow Diagram
(ASCII or mermaid diagram showing the flow)

### Checklist
(relevant items from best-practices.md)
```

Use Vietnamese for explanations (matching team convention), English for Git commands and technical terms.
