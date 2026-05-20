---
name: review-fix
version: 1.0.0
description: CodeRabbit PR 리뷰 코멘트 분석 및 수정 적용
user-invocable: true
---

# /review-fix

CodeRabbit이 PR에 남긴 리뷰 코멘트를 분석하고 수정사항을 적용하는 스킬입니다.

## 실행 단계

### 1. PR 정보 수집

사용자 입력 또는 현재 브랜치로부터 PR을 식별합니다.

**사용자 입력 패턴**:
- PR 번호: `/review-fix 123`
- PR URL: `/review-fix https://github.com/...`
- 인자 없음: 현재 브랜치의 PR 자동 조회

**현재 브랜치로 PR 조회**:
```bash
current_branch=$(git branch --show-current)
gh pr list --head "$current_branch" --json number,title,url --limit 1
```

**IF** PR을 찾을 수 없는 경우:
→ 사용자에게 PR 번호 또는 URL 입력 요청

---

### 2. 리뷰 코멘트 조회

gh CLI를 사용하여 PR의 모든 리뷰 코멘트를 가져옵니다.

```bash
gh api "repos/:owner/:repo/pulls/${PR_NUMBER}/comments" \
  --jq '.[] | {
    id: .id,
    user: .user.login,
    body: .body,
    path: .path,
    line: .line,
    created_at: .created_at,
    in_reply_to_id: .in_reply_to_id
  }'
```

**필터링**:
- CodeRabbit 봇의 코멘트만 추출 (user: "coderabbitai" 또는 설정된 봇 이름)
- 이미 답글이 달린 코멘트는 "해결됨"으로 분류 (선택적)

**IF** 코멘트가 없는 경우:
→ 사용자에게 "리뷰 코멘트가 없습니다" 보고 후 종료

---

### 3. 코멘트 분석 및 분류

CodeRabbit 코멘트를 파일별, 카테고리별로 정리합니다.

**분류 기준**:
- **Critical**: "must", "required", "bug", "error" 키워드 포함
- **Suggestion**: "consider", "recommend", "suggest" 키워드 포함
- **Nitpick**: "typo", "formatting", "style" 키워드 포함
- **Question**: "why", "how", "?" 포함

**출력 형식**:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 CodeRabbit 리뷰 코멘트 (총 N개)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔴 Critical (N개)
  • [파일명:라인] 코멘트 요약

🟡 Suggestion (N개)
  • [파일명:라인] 코멘트 요약

⚪ Nitpick (N개)
  • [파일명:라인] 코멘트 요약

❓ Question (N개)
  • [파일명:라인] 코멘트 요약

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### 4. 수정 대상 선택

사용자에게 어떤 코멘트를 수정할지 선택을 요청합니다.

**AskUserQuestion 사용**:
```
질문: "어떤 코멘트를 수정할까요?"
옵션:
  1. "모든 Critical" - Critical 코멘트만 수정
  2. "Critical + Suggestion" - Critical과 Suggestion 수정
  3. "전체 수정" - 모든 코멘트 수정
  4. "개별 선택" - 코멘트별로 선택
```

**IF** "개별 선택":
→ 각 코멘트를 순회하며 수정 여부 확인

---

### 5. 코드 수정 적용

선택된 코멘트에 대해 코드를 수정합니다.

**순서**:
1. 파일별로 그룹화
2. 각 파일의 해당 라인 Read
3. 코멘트 내용 분석 및 수정 방향 결정
4. Edit 또는 Write 도구로 수정

**수정 전 확인**:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔧 수정 적용 중...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 파일명:라인
📝 코멘트: {코멘트 내용}

현재 코드:
{코드 블록}

수정안:
{수정된 코드 블록}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**주의사항**:
- 한 번에 하나의 파일씩 수정
- 각 수정 후 결과 확인
- 불확실한 경우 사용자에게 확인 요청

---

### 6. 변경사항 커밋

수정이 완료되면 커밋을 생성합니다.

**중요**: Co-Authored-By를 **포함하지 않습니다**.

**커밋 명령어**:
```bash
git add <파일1> <파일2> ...
git commit -m "[TICKET-ID] Fix: CodeRabbit 리뷰 피드백 반영"
```

**커밋 메시지 형식**:
```text
[TICKET-ID] Fix: CodeRabbit 리뷰 피드백 반영
```

**IF** 여러 카테고리 수정 시:
→ 카테고리별로 별도 커밋 권장 (Critical, Suggestion 분리)
→ 각 커밋마다 Co-Authored-By **없이** 커밋

---

### 7. 푸시 및 완료

변경사항을 원격 저장소에 푸시합니다.

```bash
git push origin HEAD
```

**사용자에게 보고**:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 리뷰 피드백 수정 완료!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 수정 내역:
  • 파일 수정: N개
  • 코멘트 대응: N개
  • 커밋: N개

🔗 PR: {PR URL}

💡 다음 단계:
  • CodeRabbit이 자동으로 재검토합니다
  • 필요시 리뷰어에게 알림을 보내세요

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 엣지 케이스

### Case: PR이 draft 상태
→ 경고 후 진행 여부 확인

### Case: 충돌하는 수정사항
→ 충돌 파일 목록 표시, 수동 해결 안내

### Case: 이미 수정된 코드
→ 현재 코드와 코멘트 비교, 스킵 여부 확인

### Case: Question 타입 코멘트
→ 수정 대신 답글 작성 제안

### Case: CodeRabbit이 아닌 코멘트
→ 필터링하되, 옵션으로 "모든 코멘트 보기" 제공

### Case: 여러 PR이 있는 브랜치
→ 가장 최근 PR 자동 선택, 사용자에게 확인 요청

### Case: 파일이 삭제된 코멘트
→ "파일 없음" 표시, 스킵

---

## 옵션 (향후 확장)

### --dry-run
수정 미리보기만 표시 (실제 수정 없음)

### --category <type>
특정 카테고리만 수정 (critical, suggestion, nitpick, question)

### --file <path>
특정 파일의 코멘트만 수정

### --auto
자동으로 모든 Critical + Suggestion 수정 (확인 없이)

---

## 주의사항

1. **수정 전 백업**: 큰 변경사항은 워크트리 사용 권장
2. **테스트 필수**: 수정 후 빌드/테스트 확인
3. **리뷰어 소통**: 불명확한 코멘트는 리뷰어에게 질문
4. **분할 커밋**: 논리적 단위로 커밋 분리 (Critical/Suggestion 등)
