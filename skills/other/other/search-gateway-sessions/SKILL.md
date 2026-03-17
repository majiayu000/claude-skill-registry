---
name: search-gateway-sessions
description: 과거 세션 대화를 검색하는 스킬. CLAUDE_GATEWAY_SESSION_MEMORY 환경변수가 local 또는 external일 때만 사용 가능. none이면 이 스킬을 선택하지 마라. 사용자가 과거/이전/기억/전에/아까 등을 언급하거나 회상을 요청할 때 활성화.
---

# Search Gateway Sessions Skill

과거 세션 대화를 검색합니다. 외부 의존성 없는 독립 스크립트.

## Activation Guard (필수 사전 체크)

**이 스킬을 실행하기 전에 반드시 환경변수를 확인하라:**

```bash
echo $CLAUDE_GATEWAY_SESSION_MEMORY
```

- 값이 비어있거나 `none` → **이 스킬을 실행하지 마라.**
- `local` 또는 `external` → 아래 Usage대로 실행하라.

## Files
- Script: `.claude/skills/search-gateway-sessions/scripts/search_gateway_sessions.py`
- 설정: 환경변수만 사용 (main.py가 .env를 로드하므로 이미 설정됨)
- 외부 모듈 임포트 없음 (hybrid_retriever, local_embeddings 불필요)

## Usage

```bash
python .claude/skills/search-gateway-sessions/scripts/search_gateway_sessions.py "검색어"
```

### Options
- `--top-k N`: 반환할 최대 결과 수 (기본값: 8)

```bash
python .claude/skills/search-gateway-sessions/scripts/search_gateway_sessions.py "검색어" --top-k 5
```

## 자동 검색 트리거 규칙

다음 상황에서 **자동으로** 이 스킬을 실행하라 (단, Activation Guard 통과 시에만):

1. 사용자가 "과거", "이전", "기억", "전에", "아까" 등의 키워드를 언급할 때
2. 사용자가 "내가 뭐했지", "뭐라고 했지", "찾아줘" 등 회상을 요청할 때
3. 사용자가 구체적인 날짜나 시간을 언급하며 과거 내용을 물을 때
4. 문맥상 현재 세션에 없는 정보를 참조하는 것으로 보일 때

## Agent Rules

- **Activation Guard를 통과하지 못하면 스크립트를 절대 실행하지 마라.**
- 검색 결과가 있으면 유사도 순으로 핵심 내용을 요약하여 사용자에게 전달한다.
- 검색 결과가 없으면 "관련 과거 대화를 찾지 못했습니다"라고 안내한다.
