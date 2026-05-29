---
name: "local-dev-context"
description: "Local development environment context management"
---

# Local Development Context

로컬 개발 환경 맥락 통합 (파일시스템, 설정, 문서, 히스토리) → 에러 없는 코딩

## Overview

**해결 문제**:
- 반복적 환경 설정 에러
- 프로젝트별 특수 설정 누락
- 팀 내부 문서 미활용
- 과거 해결 사례 재검색

**핵심 기능**:
- 로컬 파일시스템 자동 스캔 (3초 이내)
- 기술 스택 자동 감지 (Node.js/Python/Go/Rust)
- MCP 도구 통합 (Notion/Drive/Gmail)
- 컨텍스트 기반 에러 진단

## Activation Triggers

### 자동 활성화
1. **에러 메시지**: `ModuleNotFoundError`, `npm ERR!`, `docker: Error`
2. **프로젝트 정보 요청**: "프로젝트 구조 파악해줘"
3. **개발 작업 시작**: "API 엔드포인트 추가하려는데"
4. **명시적 요청**: "로컬 환경 스캔해줘"

## Core Workflow

### Phase 1: 자동 컨텍스트 수집 (30초)
```bash
view /home/claude         # 작업 디렉토리
ls -la                    # 숨김 파일
view README.md            # 프로젝트 개요
git log -1 --oneline      # Git 상태
```

### Phase 2: 기술 스택 감지
| 파일 | 감지 결과 |
|------|----------|
| package.json | Node.js/npm |
| requirements.txt | Python |
| go.mod | Go |
| Cargo.toml | Rust |
| docker-compose.yml | Docker |

### Phase 3: MCP 통합 검색
Notion/Google Drive/Gmail에서 관련 문서 검색

### Phase 4: 인사이트 제공
에러 진단 + 해결책 제시

## Usage Patterns

### 에러 해결
```
"ModuleNotFoundError: No module named 'numpy'"
→ 환경 스캔 + pip install numpy 제안
```

### 프로젝트 온보딩
```
"프로젝트 처음인데 뭐부터 시작하지?"
→ README + 구조 분석 + 시작 가이드 제공
```

### 설정 확인
```
"배포하려고 하는데 설정 확인해줘"
→ .env, docker-compose, CI/CD 검토
```

## References

- `references/stack-detection.md` - 기술 스택 감지 상세
- `references/mcp-integration.md` - MCP 도구 연동
- `references/error-patterns.md` - 에러 패턴 DB
- `references/troubleshooting.md` - 트러블슈팅 가이드
