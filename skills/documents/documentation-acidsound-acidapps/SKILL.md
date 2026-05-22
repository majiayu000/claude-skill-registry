---
name: documentation
description: Generate and update project documentation following acidApps standards. Includes templates for README, USER_MANUAL, TERMINOLOGY, and CHANGELOG.
---

# 📝 Documentation Skill

프로젝트 문서 생성 및 갱신을 위한 가이드.

## 🎯 용도

- 새 프로젝트 문서 템플릿 제공
- 기존 문서 업데이트 가이드
- 다국어 문서 동기화

## 📋 필수 문서 목록

| 문서 | 용도 | 우선순위 |
|-----|------|---------|
| `README.md` | 프로젝트 개요, 시작 가이드 | 🔴 필수 |
| `USER_MANUAL.md` | 사용자 매뉴얼 | 🔴 필수 |
| `CHANGELOG.md` | 변경 이력 | 🟡 권장 |
| `TERMINOLOGY.md` | 용어 정의 | 🟡 권장 |
| `.agent/PROJECT_CONTEXT.md` | AI 에이전트용 프로젝트 정보 | 🟢 선택 |

## 📄 템플릿

### README.md

```markdown
# 🎹 [앱 이름]

**[앱 이름]**은 [한 줄 설명].

🎵 **[Live Demo](https://your-url.github.io/app/)**

## ✨ 주요 기능

- **기능 1**: 설명
- **기능 2**: 설명

## 🛠 기술 스택

- **Framework**: React 19 + Vite
- **Audio**: Web Audio API (AudioWorklet)

## 🚀 시작하기

\`\`\`bash
git clone https://github.com/user/app.git
cd app
npm install
npm run dev
\`\`\`

## 📖 문서

- [사용자 매뉴얼](./USER_MANUAL.md)
```

### USER_MANUAL.md

```markdown
# 📖 [앱 이름] 사용자 매뉴얼

## 🕹️ 인터페이스 구성

### 1. 헤더 영역
- **로고**: [기능]
- **디스플레이**: [표시 정보]

### 2. 메인 영역
- **패드/건반**: [사용법]

## 🎹 기본 조작

### 사운드 재생
1. [단계 1]
2. [단계 2]

## ⌨️ 키보드 단축키

| 키 | 동작 |
|----|------|
| Space | 재생/정지 |

## 🌐 시스템 요구사항

- **브라우저**: Chrome, Edge, Safari
```

### CHANGELOG.md

```markdown
# 📋 변경 이력

## [Unreleased]

### Added
- 새 기능

### Changed
- 변경 사항

### Fixed
- 버그 수정

---

## [1.0.0] - 2026-01-25

### Added
- 초기 릴리즈
```

### TERMINOLOGY.md

```markdown
# 📗 용어 정의

## 핵심 개념

| 용어 | 범위 | 정의 |
|------|------|------|
| **Project** | UI/Logic | 앱의 전체 상태 |
| **Pad** | UI/Logic | 개별 트리거 단위 |

## 파라미터

| 용어 | 범위 | 정의 |
|------|------|------|
| **Pitch** | Logic | 재생 속도/피치 |
```

## 📝 문서 갱신 워크플로우

### 1. 기능 추가 시

1. `USER_MANUAL.md`에 새 섹션 추가
2. `CHANGELOG.md`에 항목 추가
3. `README.md` 기능 목록 업데이트 (필요시)
4. 한국어 문서 동기화 (있는 경우)

### 2. UI 변경 시

1. 스크린샷 재생성 (`screenshot-generator` 스킬 참조)
2. `USER_MANUAL.md` 설명 업데이트
3. `README.md` 스크린샷 업데이트

### 3. API/구조 변경 시

1. `TERMINOLOGY.md` 용어 업데이트
2. `.agent/PROJECT_CONTEXT.md` 아키텍처 업데이트
3. 개발 문서 업데이트 (`docs/DEVELOPMENT.md`)

## 🌐 다국어 동기화

### 대상 파일

```
USER_MANUAL.md      → USER_MANUAL_ko.md
LEARNING_GUIDE.md   → LEARNING_GUIDE_ko.md (있는 경우)
```

### 동기화 체크리스트

- [ ] 섹션 구조 일치
- [ ] 헤더 번호/레벨 일치
- [ ] 스크린샷 경로 동일
- [ ] 키보드 단축키 표 동일

## 🔍 문서 검증

```bash
# 깨진 링크 확인
grep -rn "\[.*\](.*)" *.md | grep -v "http"

# 이미지 존재 확인
for img in $(grep -oh "assets/[^)]*" *.md); do
    [ -f "$img" ] || echo "Missing: $img"
done
```
