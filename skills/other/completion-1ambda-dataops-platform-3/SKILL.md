# Completion Skill

구현 완료 선언 전 검증하는 통합 프로세스.

## 적용 시점

"구현 완료", "done", "finished" 선언 전 자동 적용.

---

## 필수 Gate 조건

### 1. 코드 존재 검증

```bash
# 새로 만든 클래스/함수가 실제로 존재하는지 확인
grep -r "class ClassName" src/
grep -r "def function_name" src/
```

### 2. 테스트 통과

```bash
# 프로젝트별 테스트 실행
./gradlew clean build     # Kotlin/Spring
uv run pytest             # Python
pnpm test                 # React/TypeScript
```

### 3. API-CLI Parity (CLI 프로젝트만)

| CLI 커맨드 | API 메서드 |
|------------|-----------|
| `dli xxx list` | `XxxAPI.list_xxxs()` |
| `dli xxx get` | `XxxAPI.get()` |
| `dli xxx run` | `XxxAPI.run()` |

### 4. Export 확인 (라이브러리)

```bash
grep "XxxAPI" src/dli/__init__.py  # Python
grep "export.*Xxx" src/index.ts    # TypeScript
```

---

## 완료 선언 형식

```markdown
## 구현 완료

**새로 작성한 파일:**
- `src/xxx.py:10-50` (+40 lines)

**테스트 결과:**
- `pytest tests/ → 15 passed`

**검증:**
- `grep -r "class XxxAPI" src/` ✓
```

---

## Phase 관리 (다단계 기능)

Phase 1/2 구분이 있으면:
1. Phase 1 완료 시 "Phase 1 완료" (not "구현 완료")
2. Phase 2 항목 목록 제시
3. 전체 완료 시에만 "구현 완료"
