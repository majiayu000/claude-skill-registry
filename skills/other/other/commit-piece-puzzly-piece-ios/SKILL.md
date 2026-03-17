---
name: commit
version: 3.1.0
description: 원자적 커밋 생성
user-invocable: true
---

# Commit 스킬

현재 변경사항을 분석하고 논리적 단위로 나누어 원자적 커밋을 생성합니다.
프로젝트 구조를 자동으로 감지하여 적절한 그룹화 규칙을 적용합니다.

## 실행 단계

### 1. 프로젝트 타입 감지

디렉토리 구조를 확인하여 프로젝트 타입을 판별합니다:

```bash
# 프로젝트 타입 확인
ls *.xcodeproj *.xcworkspace Package.swift 2>/dev/null
```

**프로젝트 타입 결정**:

| 조건 | 타입 | 설명 |
|------|------|------|
| `*.xcodeproj` 또는 `*.xcworkspace` 존재 | `ios-xcode` | Xcode iOS 프로젝트 |
| `Package.swift` 존재 | `ios-spm` | Swift Package Manager 프로젝트 |
| 그 외 | `default` | 일반 프로젝트 |

### 2. 사전 확인

```bash
# 현재 브랜치 확인
git branch --show-current

# 변경사항 확인
git status --short

# 변경 파일 통계
git diff --stat
```

**체크리스트**:
- [ ] 변경된 파일이 1개 이상 존재하는가?
- [ ] 현재 브랜치가 무엇인가? (main/develop/feature)

### 3. 브랜치 확인 및 이슈 ID 추출

**IF** 현재 브랜치가 `main`:
→ 안내 후 종료:
```text
main 브랜치에서는 직접 커밋할 수 없습니다.
`/start-branch`를 실행하여 작업 브랜치를 먼저 생성하세요.
```

**ELSE** feature/fix 브랜치:
1. 브랜치명에서 이슈 ID 추출
   ```bash
   BRANCH=$(git branch --show-current)
   # 예: feat/PC-1813 → PC-1813
   ISSUE_ID=$(echo "$BRANCH" | grep -oE 'PC-[0-9]+' || echo "")
   ```
2. 추출된 이슈 ID 저장 (커밋 메시지에 사용)

### 4. 변경사항 분석 및 그룹화

**파일 읽기**: 변경된 파일 목록을 기반으로 관련 파일들을 읽어 변경 내용 파악

**그룹화 기준** (프로젝트 타입별):

#### IF 프로젝트 타입 = `ios-xcode` 또는 `ios-spm`:

**iOS SwiftUI 그룹화 우선순위**:

1. **Models** (`Models/`, `*Model.swift`) - 데이터 모델, DTO
2. **ViewModels** (`ViewModels/`, `*ViewModel.swift`) - ObservableObject
3. **Views** (`Views/`, `*View.swift`) - SwiftUI 뷰
4. **Services** (`Services/`, `*Service.swift`) - 네트워크, 영속성
5. **Extensions** (`Extensions/`, `*+Extension.swift`) - Swift 확장
6. **Resources** (`Assets.xcassets`, `Info.plist`, `*.strings`) - 리소스
7. **Tests** (`Tests/`, `*Tests.swift`) - XCTest 파일
8. **설정 파일** (루트 - `Package.swift`, `.swiftlint.yml`, `*.xcconfig`)

#### ELSE (default):

- 첫 번째 디렉토리 기준으로 그룹화
- 루트 파일은 별도 그룹

**공통 규칙**:

1. **파일 타입 간 의존성**:
   - `*View.swift`, `*ViewModel.swift`, `*Model.swift`는 같은 기능이라면 함께 커밋

2. **원자성 규칙**:
   - 한 커밋당 3-5개 파일 권장 (최대 8개)
   - 변경 파일이 12개 초과이거나 성격이 2개 이상(코드/설정/문서) 섞이면 반드시 분할 커밋

3. **설정 파일 분리**:
   - 설정 파일 변경은 항상 별도 커밋

### 5. 커밋 메시지 생성

각 그룹마다:
1. **Type 결정** (대문자 시작): Feature, Fix, Build, Chore, Refactor
2. **설명 작성**: 무엇을 왜 변경했는지 (한글, 50자 이내)

**커밋 메시지 형식**:

**이슈 ID 있음 (일반적인 경우)**:
```text
[PC-XXXX] Type: 설명
```

**이슈 ID 없음** (스킬 파일 등 프로젝트 외부):
```text
Type: 설명
```

**Type 기준**:

| Type | 용도 |
|------|------|
| `Feature` | 새 기능 |
| `Fix` | 버그 수정 |
| `Build` | 빌드 시스템, 의존성 변경 |
| `Chore` | 유지보수 작업 |
| `Refactor` | 동작 변경 없는 코드 구조 개선 |


**중요**: 브랜치에서 이슈 ID가 추출되면 **반드시** 커밋 메시지에 포함해야 합니다.

**예시**:
- `[PC-1342] Feature: StoreMain 프로모션 상품 UI 구현`
- `[PC-1342] Fix: Description 하단 패딩 수정`
- `[PC-1342] Build: SVG 이미지 url 로드를 위한 서드파티 의존성 추가`

### 6. 순차적 커밋 실행

각 그룹마다 순차적으로:

```bash
# 해당 그룹 파일들만 스테이징
git add <파일1> <파일2> <파일3>

# 커밋 (Co-Authored-By 없이)
git commit -m "[PC-XXXX] Type: 설명"

# 커밋 성공 확인
git log -1 --oneline
```

**주의**: Piece-iOS 프로젝트는 Co-Authored-By를 사용하지 않습니다.

### 7. 최종 확인 및 요약

```bash
# 생성된 커밋 목록 확인
git log --oneline -n <생성된 커밋 수>

# 남은 변경사항 확인
git status
```

**사용자에게 보고**:
1. 생성된 커밋 목록 (커밋 메시지 포함)
2. 각 커밋에 포함된 파일 목록
3. 다음 단계 안내

## 엣지 케이스 처리

### Case 1: 변경사항이 없을 때
→ "변경사항이 없습니다." 메시지 출력 후 종료

### Case 2: main 브랜치에서 실행
→ "/start-branch를 먼저 실행하세요" 안내 후 종료

### Case 3: 변경사항이 너무 많을 때 (50개 이상 파일)
→ 사용자에게 경고 후 자동 그룹화 또는 수동 선택

### Case 4: 스테이징된 파일이 이미 있을 때
→ 사용자에게 처리 방법 확인
