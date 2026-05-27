---
name: codebase-search
description: 코드 검색 전 코드베이스 문서를 참고하여 프로젝트 구조와 컨텍스트를 파악합니다. 코드 검색, 파일 탐색, 구현 위치 파악, 프로젝트 이해가 필요할 때 사용하세요.
allowed-tools: Read, Grep, Glob
---

# Codebase Search Skill

코드베이스를 검색하거나 탐색하기 전에 `.codebase/` 디렉토리의 문서를 먼저 참조하여 프로젝트 컨텍스트를 파악합니다.

## 지침

### 1단계: 코드베이스 문서 확인
코드 검색을 시작하기 전에 반드시 `.codebase/` 디렉토리의 문서를 먼저 읽으세요:

```bash
# 사용 가능한 문서 목록 확인
ls -la .codebase/
```

### 2단계: 관련 문서 읽기
검색하려는 내용과 관련된 문서를 읽으세요:

| 문서 | 용도 |
|------|------|
| `.codebase/ARCHITECTURE.md` | 전체 아키텍처, 레이어 구조, 의존성 흐름 |
| `.codebase/DIRECTORY.md` | 디렉토리 구조 및 각 폴더의 역할 |
| `.codebase/API.md` | API 엔드포인트 목록 및 라우팅 구조 |
| `.codebase/DATABASE.md` | 데이터베이스 스키마, 엔티티 관계 |
| `.codebase/MODULES.md` | 주요 모듈/서비스 설명 |
| `.codebase/PATTERNS.md` | 코드 패턴, 컨벤션, 네이밍 규칙 |

### 3단계: 컨텍스트 기반 검색
문서에서 파악한 정보를 바탕으로 효율적인 검색 수행:

1. 관련 디렉토리 범위 좁히기
2. 적절한 파일 패턴 사용
3. 코드 패턴/네이밍 컨벤션 활용

## 검색 우선순위

1. **먼저**: `.codebase/` 문서 확인
2. **다음**: 문서에서 파악한 위치로 직접 이동
3. **마지막**: 필요시 Grep/Glob으로 추가 검색

## 예시

### 인증 관련 코드 찾기
```markdown
1. .codebase/MODULES.md 읽기 → "auth" 모듈 위치 파악
2. .codebase/API.md 읽기 → 인증 관련 엔드포인트 확인
3. 해당 디렉토리로 직접 이동하여 코드 읽기
```

### 데이터베이스 엔티티 찾기
```markdown
1. .codebase/DATABASE.md 읽기 → 엔티티 목록 및 관계 파악
2. .codebase/DIRECTORY.md 읽기 → 엔티티 파일 위치 확인
3. 해당 파일 직접 읽기
```

## 주의사항

- `.codebase/` 문서가 없거나 오래된 경우, `codebase-update` 스킬을 먼저 실행하세요
- 문서와 실제 코드가 불일치할 수 있으니, 문서는 참고용으로만 사용하세요
- 검색 결과가 예상과 다르면 문서 업데이트가 필요할 수 있습니다
