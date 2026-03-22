---
name: jira-sync
description: CHANGELOG 기반 Jira 티켓 상태를 Git 브랜치 상태에 맞게 동기화하는 로직을 가이드합니다.
allowed-tools: mcp__jira__jira_get_ticket, mcp__jira__jira_transition, mcp__jira__jira_update_field, mcp__jira__jira_list_transitions, mcp__jira__changelog_extract_tickets, mcp__jira__changelog_check_branches, Read, Bash
user-invocable: false
---

# Jira Sync Skill

## 목적

CHANGELOG.md의 티켓들을 Git 브랜치(main, staging, production) 상태에 맞춰 Jira 상태를 자동 동기화한다.

## Jira 상태 체계 (6개)

| 상태 | 의미 |
|------|------|
| 대기 | 미착수 또는 로컬 작업 중 |
| 진행 중 | 원격 Git에 올라갔으나 PR 없음 |
| 리뷰 중 | PR이 생성된 상태 |
| 리뷰 완료 | PR Approve 후 병합 완료 |
| 검토 완료 | QA 담당자가 확인 완료 |
| 완료 | Production 브랜치에 병합 |

## 상태 전이 규칙

### 규칙 1: main 또는 staging 병합 → 리뷰 완료

- **조건**: 티켓이 main 또는 staging 브랜치에 포함되어 있고, 현재 상태가 리뷰 완료 미만 (대기, 진행 중, 리뷰 중)
- **액션**: `jira_transition` → "리뷰 완료"

### 규칙 2: staging 배포 여부 → customfield 변경

- **조건**: 티켓이 staging 또는 production 브랜치에 포함됨 (main → staging → production 순서이므로 production은 staging을 거친 것)
- **액션**: `jira_update_field(customfield_10659, {id: "10678"})` (이미 설정되어 있으면 SKIP)

### 규칙 3: staging + 검토 완료 → SKIP

- **조건**: 티켓이 staging에 있고 현재 상태가 "검토 완료"
- **액션**: 건들지 않음

### 규칙 4: production 병합 → 완료

- **조건**: 티켓이 production 브랜치에 포함되고 현재 상태가 "완료"가 아님
- **액션**: `jira_transition` → "완료"

## 상태 순서 (전이 판단용)

대기 < 진행 중 < 리뷰 중 < 리뷰 완료 < 검토 완료 < 완료

"리뷰 완료 미만"은 상태가 {대기, 진행 중, 리뷰 중} 중 하나인 경우를 의미한다.

## Custom Field 정보

- 필드: `customfield_10659`
- 타입: select
- staging 병합 시 값: `{id: "10678"}`
