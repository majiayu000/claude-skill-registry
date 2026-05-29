---
name: document-task
description: Automatically documents conversations by appending to CLAUDE.local.research.md (Research) or CLAUDE.local.task.md (Task). Use when (1) User's CLAUDE.md instructs to invoke after main output, (2) User explicitly requests documentation, or (3) Documenting development work or research at conversation end. Always outputs in Korean (UTF-8).
---

# document-task

- This skill describes how to automatically document (organize) the conversation just before it ends.
  - If classified as **Research**, append to `CLAUDE.local.research.md`; if **Task**, append to `CLAUDE.local.task.md` using the specified format.
- The output language is always Korean, and files must be saved with UTF-8 encoding.

## Instructions

### 동작 순서 (구체적 절차)

#### 1) 기록 여부 판단 (Document / Skip)

아래의 판단 규칙을 적용해 기록 필요성이 높은 경우에만 문서에 추가합니다. 판단은 마지막 유저 메시지(의도)를 우선으로 하며, 추가 컨텍스트(대화 길이, 포함된 코드/파일/명령 등)를 반영합니다.

##### 기록할 것 (예시 신호 — 하나라도 해당하면 기록 권장)

- 새로운 요구사항/기능 요청/스펙 결정: "이 기능을 이렇게 구현하자", "API 계약은 X로 한다"
- 배포/마이그레이션/구성(인프라) 변경 지시나 결정: "이제 DB 마이그레이션을 포함해야 함"
- 코드·설계 수정 지시 또는 패치 요청(구체적 파일/라인/명령 포함)
- 테스트 케이스, 재현 방법, 버그 리포트(재현 단계/로그/증상)
- 명확한 CLI/스크립트/설치/운영 명령이 포함된 경우(예: `sudo apt ...`, `yarn build`)
- breaking change, 호환성 주의, 보안 관련 알림
- 사용자가 '이 내용을 문서화 해달라'고 직접 요청한 경우

##### 기록하지 않을 것 (무시 사례 — 예시)

- 단순 인사/잡담/간단 확인 질문: "안녕", "오늘 어때?"
- 단순 확인·재진술(clarifying) 질문: "그러니까 이건 ~라는 뜻이죠?" (사용자가 이해 확인 목적일 때)
- 아주 짧고 의미없는 반응(예: "좋아요", "응")
- 단순 오타 지적 후의 확인(사용자가 지적한 것이 실제로 문서 수정이 필요한 수준이 아닐 때)

##### 추가 규칙(수정/정정 처리)

- 사용자가 **이전 세션에서 기록된 항목**의 오류를 지적했을 때:
  - 사용자의 지적이 사실인 경우: 해당 마크다운 파일의 관련 부분을 **수정**(덮어쓰기/보정)합니다.
  - 지적이 사실이 아닌 경우: 파일을 변경하지 않습니다. (대화 내 근거를 간단히 메모할 수 있음)

---

#### 2) 분류: Research vs Task

- Research: 질문/정보 요청, 조사·레퍼런스 수집, 설계 검토 등
- Task: 구현·수정·버그 해결·코드 작성·명령 실행 요청 등
- 분류는 휴리스틱(키워드 + 의도)으로 결정하며 모호하면 Research로 보수적 기록.

---

#### 3) 대상 파일 결정

- Research → CLAUDE.local.research.md
- Task → CLAUDE.local.task.md
- 파일이 없으면 생성.

---

#### 4) 항목 식별자 (타임스탬프 + ID 사용)

- 각 항목은 아래 메타로 식별:
  - 작성일 (Asia/Seoul 기준, 예: `2025-11-10 15:23:05 (KST)`)
  - entry_id (에포크초 또는 에포크초 + 짧은 해시, 예: `1699659785`)
- 이 방식은 LLM 토큰 소모를 줄이고 충돌 가능성도 낮습니다.

---

#### 5) 코드 블록의 파일·라인 위치 탐색

- 코드 블록(`...`)이 포함된 경우, 대표적인 3~5줄을 추출
- Grep 도구로 저장소에서 부분/정확 매칭 시도:
  - 예: `Grep(pattern="extracted_lines", output_mode="content", -n=true)`
  - 찾으면 코드 위치를 `<파일 경로>:<시작행>-<끝행>` 형식으로 "특이사항" 섹션에 기록
  - 찾지 못하면 원문 코드 블록은 "질문 원본"에 포함하되, 위치 표기는 생략
- 디렉토리 범위는 프로젝트 루트(.)로 제한
- 여러 파일에서 발견될 경우, 가장 관련성 높은 파일 1~2개만 기록

---

#### 6) 기록 포맷 (번호 없음 — 타임스탬프/ID 사용)

- 항목은 아래 템플릿으로 append 합니다.
- 각 프롬프트 문서화 섹션 사이는 `{entry_id} 종료\n---`으로 구분합니다.
  - 혼선 방지를 위해, 위 용도 외에는 `---`는 절대 사용하지 않습니다.

```md
# 제목: {문서 제목 — 프롬프트의 핵심을 간결히}

- 작성일: {YYYY-MM-DD HH:MM:SS (KST)}
- entry_id: {epoch_seconds_or_short_id}

## 질문 원본

<user-prompt>
“{개발자가 입력한 프롬프트 원문(정확 복사)}”
</user-prompt>

## 답변

(assistant의 답변 — 최대한 자세하게. 별도로 요약하지 말것)

## 특이사항 (있는 경우)

- 코드 위치: <파일 경로>:<시작행>-<끝행> (가능한 경우만)
- 기타: (마이그레이션 필요, BREAKING CHANGE 등)

## {entry_id} 종료

...
```

#### 7) 출력/반환

- 성공 예: ✅ CLAUDE.local.research.md에 entry_id #1699659785 추가
- 기록 불필요: ℹ️ 기록 불필요 판단: 대화는 문서화 대상이 아님
- 오류: ⚠️ 파일 쓰기 실패: 권한 문제 또는 알 수 없는 이슈

## Resources

### Examples

완전한 Research 및 Task 항목 예시는 [references/example.md](references/example.md)를 참고하세요. 올바른 포맷팅과 구조를 확인할 수 있습니다.

### Template

새 항목을 작성할 때는 [assets/template.md](assets/template.md)를 포맷팅 템플릿으로 사용하세요.
