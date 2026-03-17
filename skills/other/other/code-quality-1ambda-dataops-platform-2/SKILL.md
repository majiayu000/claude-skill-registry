# Code Quality Skill

디버깅, 리팩토링, 성능 분석 통합 가이드.

---

## 디버깅

### 접근법

1. **증상 수집**: 에러 메시지, 스택 트레이스
2. **가설 수립**: 가장 가능성 높은 원인 3개
3. **검증**: 각 가설 테스트
4. **수정 및 확인**: 테스트로 검증

### 도구

```bash
# Kotlin/Spring
./gradlew test --info

# Python
uv run pytest -v --tb=long

# TypeScript
pnpm test -- --verbose
```

---

## 리팩토링

### 원칙

1. **테스트 먼저**: 기존 동작 테스트로 보호
2. **작은 단계**: 한 번에 하나씩 변경
3. **자주 커밋**: 되돌릴 수 있게

### 체크리스트

- [ ] 기존 테스트 통과
- [ ] 새 테스트 추가 (필요시)
- [ ] 동작 변경 없음 확인
- [ ] 빌드 통과

---

## 성능

### 일반 패턴

| 문제 | 해결책 |
|------|--------|
| N+1 쿼리 | Batch fetch, JOIN |
| 메모리 누수 | 리소스 해제 확인 |
| 느린 루프 | 벌크 처리, 캐싱 |

### 프로파일링

```bash
# Python
python -m cProfile -o profile.out script.py

# JVM
./gradlew bootRun -Dspring.profiles.active=dev
# VisualVM 또는 JFR 사용
```
