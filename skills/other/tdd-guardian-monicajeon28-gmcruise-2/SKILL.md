---
name: tdd-guardian
description: "**TDD GUARDIAN**: '테스트 작성', '테스트 만들어', 'TDD', '단위 테스트', '통합 테스트', '커버리지', 'mock', '모킹' 요청 시 자동 발동. *.test.ts/*.spec.ts/test_*.py 파일 작업 시 자동 적용. Fake Test 탐지, 80% 커버리지 게이트. Jest/Vitest/PyTest/JUnit 템플릿."
allowed-tools:
  - Read
  - Glob
  - Grep
---

# TDD Guardian v2.0 - Test-Driven Development Enforcer

**Proactive TDD Enforcer** - 테스트 작업 시 자동으로 TDD 원칙 적용

## 자동 발동 조건

이 스킬은 다음 상황에서 **자동으로 활성화**됩니다:

```yaml
Auto_Trigger_Conditions:
  File_Patterns:
    - "*.test.ts, *.test.tsx, *.test.js"
    - "*.spec.ts, *.spec.tsx, *.spec.js"
    - "__tests__/**, test/**, tests/**"
    - "*_test.py, test_*.py"           # Python
    - "*_test.go"                       # Go
    - "*Test.java, *Spec.java"          # Java

  Keywords_KO:
    - "테스트 작성, 테스트 만들어, 테스트 추가"
    - "단위 테스트, 통합 테스트, E2E 테스트"
    - "TDD, 테스트 주도, 테스트 먼저"
    - "커버리지, 테스트 커버리지"
    - "테스트 코드, 테스트 케이스"
    - "mock, 모킹, 스텁"

  Keywords_EN:
    - "write test, create test, add test"
    - "unit test, integration test, e2e test"
    - "TDD, test driven, test first"
    - "coverage, test coverage"

  Code_Patterns:
    - "describe(, it(, test(, expect("
    - "jest., vitest., pytest"
    - "beforeEach, afterEach, beforeAll"
```

## 선택적 문서 로드 전략

**전체 문서를 로드하지 않습니다!** 상황에 따라 필요한 문서만 로드:

```yaml
Document_Loading_Strategy:
  Step_1_Detect_Framework:
    - 파일 확장자, import 문, 설정 파일로 테스트 프레임워크 감지
    - 불명확하면 package.json의 devDependencies 확인

  Step_2_Load_Required_Docs:
    Universal_Always_Load:
      - "core/tdd-workflow.md"       # TDD 3단계 사이클 (항상)
      - "core/real-assertions.md"    # Real Assertion 규칙 (항상)

    Framework_Specific_Load:
      Jest: "frameworks/jest.md"           # Jest 설정, 매처, 모킹
      Vitest: "frameworks/vitest.md"       # Vitest 설정, 매처
      Mocha: "frameworks/mocha.md"         # Mocha + Chai
      PyTest: "frameworks/pytest.md"       # Python PyTest
      GoTest: "frameworks/gotest.md"       # Go testing package
      RSpec: "frameworks/rspec.md"         # Ruby RSpec
      JUnit: "frameworks/junit.md"         # Java JUnit5
      XCTest: "frameworks/xctest.md"       # Swift XCTest

    Context_Specific_Load:
      Unit_Test: "templates/unit-test.md"
      Integration_Test: "templates/integration-test.md"
      React_Test: "templates/react-test.md"
      Fake_Detection: "patterns/fake-test-detector.md"
      Coverage_Check: "core/coverage-thresholds.md"

  Quick_Reference:
    Checklist: "quick-reference/checklist.md"
    Anti_Patterns: "quick-reference/anti-patterns.md"
```

## 2025 테스트 프레임워크 선택 가이드

```yaml
Framework_Comparison:
  Vitest:
    권장_상황: "새 프로젝트, Vite 기반"
    장점:
      - "Jest보다 30-70% 빠름"
      - "ESM 네이티브 지원"
      - "설정 없이 바로 사용 (zero-config)"
      - "Jest 호환 API (jest.* → vi.*)"
      - "브라우저 UI 디버깅"
    메모리: "Jest 1.2GB vs Vitest 800MB (50K 라인 기준)"
    마이그레이션: "85-90% Jest 테스트 수정 없이 작동"

  Jest:
    권장_상황: "기존 프로젝트, React Native"
    장점:
      - "안정적, 10년+ 커뮤니티"
      - "레퍼런스/튜토리얼 풍부"
      - "스냅샷 테스팅 원조"
    주의: "ESM 설정 복잡, 싱글 스레드 기본"

  선택_기준:
    새_프로젝트: "Vitest 권장"
    기존_Jest_프로젝트: "유지 (마이그레이션 비용 고려)"
    React_Native: "Jest 필수"
    Vite_프로젝트: "Vitest 필수"
```

## Quick Reference

### 5 Core Principles

```yaml
1. Test First: "코드 작성 전 반드시 실패하는 테스트부터"
2. Real Assertions: "toBeDefined/toBeTruthy 단독 사용 금지"
3. Edge Coverage: "Happy + Error + Boundary + Async 필수"
4. No Fake Tests: "15+ 패턴의 Fake Test 탐지 및 거부"
5. Coverage Gate: "80% line, 70% branch 미달 시 진행 금지"
```

### Instant Checklist

```markdown
## 테스트 작성 전 체크
- [ ] 요구사항에서 테스트 케이스 도출했는가?
- [ ] Happy/Error/Boundary/Async 케이스 포함했는가?

## 테스트 작성 후 체크
- [ ] 모든 assertion이 구체적 값을 검증하는가?
- [ ] toBeDefined/toBeTruthy 단독 사용 없는가?
- [ ] 테스트 제목과 내용이 일치하는가?
- [ ] Mock이 과도하지 않은가?
- [ ] Edge case가 포함되었는가?

## 최종 검증
- [ ] 모든 테스트 통과?
- [ ] Line coverage >= 80%?
- [ ] Branch coverage >= 70%?
```

## 문서 구조

```
tdd-guardian/
├── SKILL.md                          # 이 파일 (라우터)
├── core/
│   ├── tdd-workflow.md               # Red-Green-Refactor 사이클
│   ├── real-assertions.md            # Real Assertion 규칙
│   ├── edge-coverage.md              # Edge Case 커버리지
│   └── coverage-thresholds.md        # 커버리지 임계값
├── frameworks/
│   ├── jest.md                       # Jest 설정, 매처, 모킹
│   ├── vitest.md                     # Vitest 설정, 매처
│   ├── pytest.md                     # Python PyTest
│   ├── gotest.md                     # Go testing package
│   └── junit.md                      # Java JUnit5
├── templates/
│   ├── unit-test.md                  # NestJS Service/Controller 템플릿
│   ├── integration-test.md           # E2E 테스트 템플릿
│   └── react-test.md                 # React Component/Hook 템플릿
├── patterns/
│   ├── fake-test-detector.md         # 15+ Fake Test 패턴
│   └── mock-guidelines.md            # Mock 사용 가이드
└── quick-reference/
    ├── checklist.md                  # 빠른 체크리스트
    └── anti-patterns.md              # 20+ Anti-Pattern
```

## 사용 방법

### 1. 자동 발동 (Proactive)
테스트 파일 작업 시 자동으로 원칙 적용됨

### 2. 명시적 호출
```
"이 테스트 TDD 원칙으로 리뷰해줘"
"Fake test 패턴 검사해줘"
"커버리지 80% 확인해줘"
```

### 3. 템플릿 요청
```
"NestJS Service 단위 테스트 템플릿"
"React Hook 테스트 템플릿"
"E2E 테스트 템플릿"
```

---

**Version**: 2.0.0
**Quality Target**: 95%
**Related Skills**: clean-code-mastery, code-reviewer
