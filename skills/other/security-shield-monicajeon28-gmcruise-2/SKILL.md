---
name: security-shield
description: "**SECURITY SHIELD**: '보안', '인증', '로그인', '비밀번호', 'JWT', '토큰', '암호화', '취약점', 'SQL 인젝션', 'XSS', '보안 검사' 요청 시 자동 발동. .env/auth/**/guard/** 파일 작업 시 자동 적용. 하드코딩 시크릿 탐지(40+ 패턴), OWASP Top 10 검증."
allowed-tools:
  - Read
  - Glob
  - Grep
---

# Security Shield v2.0 - AI Security Vulnerability Prevention

**Proactive Security Guardian** - 보안 관련 코드 작업 시 자동으로 보안 원칙 적용

## Base Knowledge (clean-code-mastery 참조)

> **OWASP 기본, SQL Injection, XSS 방지, 세션 보안의 기본 내용은**
> **`clean-code-mastery/core/security.md`를 참조하세요.**
>
> 이 스킬은 **하드코딩 시크릿 탐지**, **JWT 고급 패턴**, **NestJS/React 보안 템플릿**에 집중합니다.

## 자동 발동 조건

```yaml
Auto_Trigger_Conditions:
  File_Patterns:
    - ".env, .env.*, *.env"
    - "**/auth/**, **/security/**"
    - "*.config.ts, *.config.js"
    - "**/middleware/**, **/guard/**"

  Keywords_KO:
    - "인증, 인가, 로그인, 로그아웃"
    - "보안, 시큐리티, 취약점, 해킹"
    - "비밀번호, 패스워드, 암호화, 복호화"
    - "토큰, 세션, 쿠키, JWT"
    - "권한, 역할, RBAC, 접근 제어"
    - "API 키, 시크릿, 환경변수"
    - "SQL 인젝션, XSS, CSRF"
    - "보안 검사, 보안 리뷰, 취약점 분석"

  Keywords_EN:
    - "auth, authentication, authorization, login"
    - "security, secure, vulnerability, hack"
    - "password, encrypt, decrypt, hash"
    - "token, session, cookie, JWT"
    - "permission, role, RBAC, access control"
    - "api key, secret, env, environment"
    - "injection, XSS, CSRF, OWASP"

  Code_Patterns:
    - "bcrypt, argon2, crypto"
    - "jwt.sign, jwt.verify"
    - "createHash, pbkdf2"
    - "@UseGuards, @Roles, AuthGuard"
```

## 선택적 문서 로드 전략

**전체 문서를 로드하지 않습니다!** 상황에 따라 필요한 문서만 로드:

```yaml
Document_Loading_Strategy:
  Step_1_Detect_Language_Framework:
    - 파일 확장자, import 문으로 언어/프레임워크 감지
    - 불명확하면 package.json/requirements.txt/go.mod 확인

  Step_2_Load_Required_Docs:
    Universal_Always_Load:
      - "core/secrets-detection.md"      # 시크릿 탐지 (항상)
      - "quick-reference/checklist.md"   # 보안 체크리스트 (항상)

    Language_Specific_Load:
      TypeScript: "languages/typescript-security.md"  # Node.js, Express, NestJS
      Python: "languages/python-security.md"          # Django, FastAPI, Flask
      Go: "languages/go-security.md"                  # Go 보안 패턴
      Java: "languages/java-security.md"              # Spring Security
      CSharp: "languages/csharp-security.md"          # ASP.NET Core
      Ruby: "languages/ruby-security.md"              # Rails 보안
      PHP: "languages/php-security.md"                # Laravel 보안
      Rust: "languages/rust-security.md"              # Rust 보안

    Framework_Specific_Load:
      NestJS: "templates/nestjs-auth.md"
      Express: "templates/express-auth.md"
      React: "templates/react-security.md"
      Django: "templates/django-auth.md"
      Spring: "templates/spring-security.md"

    Context_Specific_Load:
      JWT_Work: "patterns/jwt-security.md"
      OAuth_Work: "patterns/oauth-security.md"
      Input_Validation: "patterns/validation.md"
      API_Security: "patterns/api-security.md"
```

## Quick Reference

### 5 Core Security Principles

```yaml
1. Defense in Depth: "여러 겹의 보안 레이어"
2. Least Privilege: "최소 권한 원칙"
3. Fail Secure: "에러 시 접근 거부"
4. Input Validation: "모든 입력은 검증 후 사용"
5. Output Encoding: "모든 출력은 컨텍스트에 맞게 인코딩"
```

### Instant Security Checklist

```markdown
## 코드 작성 시 필수 확인

### 시크릿 관리
- [ ] 코드에 API 키, 비밀번호, 토큰 없음?
- [ ] 환경변수 또는 Secret Manager 사용?
- [ ] .env 파일이 .gitignore에 있음?

### 입력 검증
- [ ] 모든 사용자 입력에 검증 있음?
- [ ] DTO에 class-validator 데코레이터?
- [ ] SQL은 parameterized query 사용?

### 인증/인가
- [ ] 모든 보호 엔드포인트에 Guard 적용?
- [ ] 역할 기반 접근 제어(RBAC) 구현?
- [ ] 비밀번호는 bcrypt/argon2로 해시?
```

## 문서 구조

```
security-shield/
├── SKILL.md                          # 이 파일 (라우터)
├── core/
│   ├── secrets-detection.md          # 40+ 시크릿 탐지 패턴
│   └── owasp-advanced.md             # OWASP 고급 패턴
├── languages/
│   ├── typescript-security.md        # Node.js, Express, NestJS
│   ├── python-security.md            # Django, FastAPI, Flask
│   ├── go-security.md                # Go 보안 패턴
│   └── java-security.md              # Spring Security
├── templates/
│   ├── nestjs-auth.md                # NestJS 인증 템플릿
│   └── react-security.md             # React 보안 템플릿
├── patterns/
│   ├── jwt-security.md               # JWT 보안 패턴
│   └── validation.md                 # 입력 검증 패턴
└── quick-reference/
    └── checklist.md                  # 보안 체크리스트
```

## 사용 방법

### 1. 자동 발동 (Proactive)
인증/보안 관련 코드 작업 시 자동으로 원칙 적용됨

### 2. 명시적 호출
```
"이 코드 보안 검사해줘"
"하드코딩된 시크릿 있는지 확인해줘"
"JWT 보안 패턴 적용해줘"
```

---

**Version**: 2.0.0
**Quality Target**: 95%
**Related Skills**: clean-code-mastery, code-reviewer
