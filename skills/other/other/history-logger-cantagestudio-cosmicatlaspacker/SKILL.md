---
name: history-logger
description: "[Task Mgmt] A Skill that logs completed tasks to Docs/History/History_yyMMdd.md as a Markdown table in Korean. Use this when a task or subtask has been completed and the user wants to record the completion time, task title, and a short Korean retrospective line into the History file for that date. (user)"
---

# History Logger

Log completed tasks to `Docs/History/History_yyMMdd.md`.

## Format

| 시간 | 태스크 제목 | 회고 |
|------|------------|------|
| HH:mm | Task title (Korean) | Retrospective (Korean) |

## Workflow

1. Get completion time (HH:mm)
2. Get task title in Korean
3. Get retrospective summary in Korean
4. Check if `Docs/History/History_yyMMdd.md` exists
   - If not: create file with table header
   - If exists: append new row
5. Show added row to user

## Example

| 14:30 | 로그인 기능 구현 | JWT 인증 추가, 토큰 갱신 로직 구현 완료 |