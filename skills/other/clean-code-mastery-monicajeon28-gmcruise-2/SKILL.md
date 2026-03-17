---
name: clean-code-mastery
description: "**CLEAN CODE MASTERY**: '코드 작성', '함수 만들어', '구현해', '개발해', '리팩토링', '개선해', '설계해', '클린코드', '코드품질' 요청 시 자동 발동. *.ts/*.py/*.go/*.java 등 모든 코드 파일 작업 시 자동 적용. SOLID/DRY/KISS + OWASP 보안 패턴. 언어별 선택적 로드."
allowed-tools:
  - Read
  - Glob
  - Grep
---

# Clean Code Mastery Skill v3.0

**Proactive Code Guardian** - 코드 작업 시 자동으로 Clean Code + Secure Coding 원칙 적용

## 자동 발동 조건

이 스킬은 다음 상황에서 **자동으로 활성화**됩니다:

```yaml
Auto_Trigger_Conditions:
  File_Extensions:
    - ".ts, .tsx, .js, .jsx"  → TypeScript/JavaScript
    - ".py"                    → Python
    - ".go"                    → Go
    - ".rs"                    → Rust
    - ".java"                  → Java
    - ".cpp, .cc, .h, .hpp"   → C++
    - ".cs"                    → C#
    - ".kt, .kts"             → Kotlin
    - ".rb"                    → Ruby
    - ".php"                   → PHP
    - ".swift"                 → Swift

  Keywords:
    - "코드 리뷰", "code review"
    - "리팩토링", "refactor"
    - "클린 코드", "clean code"
    - "코드 품질", "code quality"
    - "보안 검토", "security review"

  Actions:
    - Write tool로 코드 파일 생성/수정 시
    - Edit tool로 코드 파일 수정 시
    - 코드 분석 요청 시
```

## 선택적 문서 로드 전략

**전체 문서를 로드하지 않습니다!** 상황에 따라 필요한 문서만 로드:

```yaml
Document_Loading_Strategy:
  Step_1_Detect_Language:
    - 파일 확장자 또는 코드 문법으로 언어 감지
    - 언어가 불명확하면 사용자에게 확인

  Step_2_Load_Required_Docs:
    Universal_Always_Load:
      - "core/principles.md"      # SOLID, DRY, KISS (항상)
      - "core/security.md"        # OWASP 보안 원칙 (항상)

    Language_Specific_Load:
      TypeScript: "languages/typescript.md"
      Python: "languages/python.md"
      Go: "languages/go.md"
      Rust: "languages/rust.md"
      Java: "languages/java.md"
      CPP: "languages/cpp.md"
      CSharp: "languages/csharp.md"
      Kotlin: "languages/kotlin.md"

    Context_Specific_Load:
      Code_Review: "contexts/review-checklist.md"
      Refactoring: "contexts/refactoring-patterns.md"
      New_Code: "contexts/best-practices.md"
      Security_Audit: "contexts/security-audit.md"
```

## 사용 방법

### 1. 자동 발동 (Proactive)
코드 파일 작업 시 자동으로 원칙 적용됨

### 2. 명시적 호출
```
"이 코드 클린코드 원칙으로 리뷰해줘"
"Python 보안 패턴 확인해줘"
"TypeScript 베스트 프랙티스 적용해줘"
```

### 3. 언어 지정 호출
```
"Go 언어 관점에서 분석해줘"
"Java security 패턴 검토해줘"
```

## 문서 구조

```
clean-code-mastery/
├── SKILL.md                    # 이 파일 (라우터)
├── core/
│   ├── principles.md           # SOLID, DRY, KISS, YAGNI (~200줄)
│   ├── security.md             # OWASP 보안 원칙 (~300줄)
│   ├── naming.md               # 네이밍 컨벤션 (~150줄)
│   └── error-handling.md       # 에러 처리 패턴 (~200줄)
├── languages/
│   ├── typescript.md           # TS/JS 패턴 + 보안 (~400줄)
│   ├── python.md               # Python 패턴 + 보안 (~400줄)
│   ├── go.md                   # Go 패턴 + 보안 (~350줄)
│   ├── rust.md                 # Rust 패턴 + 보안 (~350줄)
│   ├── java.md                 # Java 패턴 + 보안 (~400줄)
│   ├── cpp.md                  # C++ 패턴 + 보안 (~400줄)
│   ├── csharp.md               # C# 패턴 + 보안 (~350줄)
│   └── kotlin.md               # Kotlin 패턴 + 보안 (~300줄)
├── contexts/
│   ├── review-checklist.md     # 코드 리뷰 체크리스트 (~150줄)
│   ├── refactoring-patterns.md # 리팩토링 패턴 (~300줄)
│   └── security-audit.md       # 보안 감사 체크리스트 (~200줄)
└── quick-reference/
    ├── anti-patterns.md        # 안티패턴 카탈로그 (~200줄)
    └── metrics.md              # 코드 메트릭 기준 (~100줄)
```

## 핵심 원칙 요약 (항상 적용)

### Clean Code 핵심
- **SRP**: 하나의 클래스/함수는 하나의 책임만
- **DRY**: 코드 중복 금지
- **KISS**: 단순하게 유지
- **함수 크기**: 20줄 이하
- **파라미터**: 3개 이하

### Security 핵심
- **Input Validation**: 모든 입력 검증
- **Output Encoding**: 모든 출력 인코딩
- **Parameterized Queries**: SQL 인젝션 방지
- **No Secrets in Code**: 코드에 비밀번호 금지

## 점수 기준 (100점 만점)

| 항목 | 배점 |
|------|------|
| 네이밍 컨벤션 | 10 |
| SOLID 준수 | 15 |
| 에러 처리 | 10 |
| 코드 스멜 없음 | 15 |
| 언어 관용구 | 10 |
| 문서화 | 5 |
| 테스트 커버리지 | 5 |
| **보안 패턴** | **20** |
| 입력 검증 | 5 |
| 출력 인코딩 | 5 |

## 2025 린팅/포맷팅 도구 가이드

```yaml
Linting_Tools:
  Biome:
    설명: "ESLint + Prettier를 대체하는 올인원 도구"
    장점:
      - "ESLint보다 15-20배 빠름"
      - "설정 간단 (biome.json 하나로 끝)"
      - "린팅 + 포맷팅 통합"
      - "97% Prettier 호환"
    타입_지원: "85% typescript-eslint 커버리지 (Biome 2.0+)"
    권장: "새 프로젝트, 빠른 피드백 원할 때"
    설치: "npm install --save-dev --save-exact @biomejs/biome"

  ESLint_Enterprise:
    설명: "AIRUDA Enterprise Grade 설정 (우수사례)"
    경로: "C:\\Users\\lpian\\OneDrive\\문서\\tsconfig\\eslint.config.mjs"
    특징:
      - "type-aware rules 전체 활성화"
      - "Brain 커스텀 룰 (불완전 구현 탐지, toast deps 감지)"
      - "no-explicit-any, no-unsafe-* 전부 error"
      - "React hooks exhaustive-deps 개선 버전"
      - "테스트 파일 별도 설정"
    권장: "엔터프라이즈 프로젝트, 팀 프로젝트, 타입 안전성 최대화"

  Oxlint:
    설명: "Rust 기반 초고속 린터"
    장점:
      - "ESLint보다 50-100배 빠름"
      - "520+ 룰"
      - "zero-config"
    주의: "포맷팅 없음, 타입 인식 룰 미지원"
    권장: "대규모 코드베이스 초기 린팅, CI 속도 개선"

  선택_가이드:
    새_프로젝트_개인: "Biome"
    새_프로젝트_팀: "ESLint Enterprise config"
    기존_프로젝트: "유지하되 설정 점진적 강화"
    CI_속도_최적화: "Oxlint 병렬 실행"
```

---

**이 스킬은 코드 작업 시 자동으로 활성화됩니다.**
**언어별 상세 가이드는 languages/ 폴더에서 선택적으로 로드됩니다.**

## 관련 스킬 통합

```yaml
Integration_Skills:
  project-architect:
    역할: "프로젝트 구조 설계"
    연동: "새 프로젝트 시작 시 자동 호출"
    
  tech-stack-advisor:
    역할: "기술 스택 선택"
    연동: "기술 결정 필요 시 참조"
    
  requirements-analyzer:
    역할: "요구사항 분석"
    연동: "기능 개발 전 분석"
    
  naming-convention-guard:
    역할: "네이밍 규칙"
    연동: "코드 작성 시 항상 함께 적용"
    
  code-smell-detector:
    역할: "코드 스멜 탐지"
    연동: "코드 리뷰 시 함께 실행"
    
  security-shield:
    역할: "보안 검증"
    연동: "인증/API 코드 작성 시"

Skill_Execution_Order:
  1. project-architect: "구조 먼저"
  2. requirements-analyzer: "요구사항 분석"
  3. tech-stack-advisor: "기술 선택"
  4. clean-code-mastery: "코드 작성"
  5. naming-convention-guard: "네이밍 검증"
  6. code-smell-detector: "스멜 탐지"
  7. security-shield: "보안 검증"
```

## 비개발자를 위한 핵심 원칙 요약

```yaml
For_Non_Developers:
  핵심_3가지:
    1_작게_만들기:
      규칙: "함수는 30줄 이하, 한 가지 일만"
      이유: "작아야 이해하기 쉽고, 테스트하기 쉬움"
      
    2_명확한_이름:
      규칙: "이름만 보고 역할을 알 수 있게"
      이유: "주석 없이도 코드가 문서가 됨"
      
    3_중복_제거:
      규칙: "같은 코드 2번 이상 쓰지 않기"
      이유: "수정할 때 한 곳만 고치면 됨"

  피해야_할_것:
    - 500줄 넘는 파일
    - 30줄 넘는 함수
    - 4단계 넘는 들여쓰기
    - 한 글자 변수명
    - 주석으로 설명해야 하는 코드
```

---

**Version**: 3.1.0
**Updated**: 스킬 통합 정보 추가
**Related Skills**: project-architect, naming-convention-guard, code-smell-detector
