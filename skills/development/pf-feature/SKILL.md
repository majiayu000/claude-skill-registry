---
name: pf-feature
description: 기능 개발 전체 플로우. "기능 개발", "새 기능", "feature" 요청 시 사용.
allowed-tools: Read, Write, Bash, Glob, Grep
---

# PF 기능 개발 플로우

$ARGUMENTS 기능을 체계적으로 개발합니다.

---

## 개발 플로우

```
1. 요구사항 분석
   ↓
2. 브랜치 생성
   ↓
3. 설계 & 계획
   ↓
4. 구현
   ↓
5. 테스트
   ↓
6. 코드 리뷰 준비
   ↓
7. PR 생성
```

---

## 1단계: 요구사항 분석

### 체크리스트
- [ ] 기능의 목적이 명확한가?
- [ ] 사용자 시나리오가 정의되었는가?
- [ ] 성공 기준이 있는가?
- [ ] 의존성이 있는 다른 기능이 있는가?
- [ ] 디자인/기획 문서가 있는가?

### 질문할 것
```
- 이 기능의 주요 사용자는 누구인가?
- 예외 상황은 어떻게 처리하나?
- 성능 요구사항이 있는가?
- 접근성 요구사항이 있는가?
```

---

## 2단계: 브랜치 생성

```bash
# 브랜치 네이밍 규칙
# feature/이슈번호-간단한설명
git checkout -b feature/123-user-profile

# 또는 이슈 없이
git checkout -b feature/add-dark-mode
```

---

## 3단계: 설계 & 계획

### 컴포넌트 설계

```
기능: 사용자 프로필 페이지

컴포넌트 구조:
pages/profile/
├── index.tsx           # 페이지 진입점
├── components/
│   ├── ProfileHeader.tsx
│   ├── ProfileForm.tsx
│   └── AvatarUpload.tsx
├── hooks/
│   └── useProfile.ts
└── types.ts

필요한 API:
- GET /users/me
- PUT /users/me
- POST /users/avatar

상태 관리:
- useProfileStore (Zustand)
- 또는 로컬 상태로 충분
```

### 작업 분해

```
[ ] 1. 타입 정의 (types.ts)
[ ] 2. API 서비스 함수 (services/profile.service.ts)
[ ] 3. ProfileHeader 컴포넌트
[ ] 4. ProfileForm 컴포넌트
[ ] 5. AvatarUpload 컴포넌트
[ ] 6. 페이지 조합
[ ] 7. 라우트 추가
[ ] 8. 테스트 작성
```

---

## 4단계: 구현

### 순서

1. **타입 정의**
```tsx
// types.ts
export interface UserProfile {
  id: number;
  name: string;
  email: string;
  avatar?: string;
}

export interface UpdateProfileDto {
  name?: string;
  email?: string;
}
```

2. **API 서비스**
```tsx
// services/profile.service.ts
export const profileService = {
  getProfile: () => apiClient.get<UserProfile>("/users/me"),
  updateProfile: (data: UpdateProfileDto) =>
    apiClient.put<UserProfile>("/users/me", data),
  uploadAvatar: (file: File) =>
    apiClient.upload<{ url: string }>("/users/avatar", file),
};
```

3. **컴포넌트 구현**
```tsx
// 기본 구조 먼저, 스타일은 나중에
function ProfileForm({ profile, onSubmit }) {
  // 1. 상태 및 로직
  // 2. 핸들러
  // 3. 렌더링
}
```

4. **페이지 조합**
```tsx
// pages/profile/index.tsx
export default function ProfilePage() {
  const { data: profile, isLoading } = useProfile();

  if (isLoading) return <ProfileSkeleton />;

  return (
    <div className="container mx-auto py-8">
      <ProfileHeader profile={profile} />
      <ProfileForm profile={profile} />
    </div>
  );
}
```

5. **라우트 추가**
```tsx
// routes/index.tsx
const ProfilePage = lazy(() => import("@/pages/profile"));

<Route path="/profile" element={<ProfilePage />} />
```

---

## 5단계: 테스트

### 실행

```bash
# 개발 서버로 수동 테스트
pnpm --filter 앱이름 dev

# 린트
pnpm lint

# 타입 체크
pnpm tsc --noEmit
```

### 테스트 작성 (권장)

```bash
# 컴포넌트 테스트 생성
/pf-test-component ProfileForm
```

---

## 6단계: 코드 리뷰 준비

### 자체 점검

```bash
# 코드 리뷰 스킬 사용
/pf-code-review src/pages/profile
```

### 체크리스트
- [ ] 타입 에러 없음
- [ ] 린트 에러 없음
- [ ] 불필요한 console.log 제거
- [ ] 주석 정리
- [ ] 접근성 확인
- [ ] 반응형 확인

---

## 7단계: PR 생성

```bash
# 변경사항 커밋
git add .
git commit -m "feat: add user profile page

- Add profile page with header and form
- Add avatar upload functionality
- Add profile API service"

# 푸시
git push -u origin feature/123-user-profile

# PR 생성
gh pr create --title "feat: 사용자 프로필 페이지 추가" --body "
## 개요
사용자 프로필 조회/수정 페이지 구현

## 변경사항
- 프로필 페이지 UI
- 아바타 업로드 기능
- 프로필 수정 API 연동

## 테스트
- [ ] 프로필 조회 확인
- [ ] 프로필 수정 확인
- [ ] 아바타 업로드 확인
- [ ] 모바일 반응형 확인

## 스크린샷
(스크린샷 첨부)

## 관련 이슈
Closes #123
"
```

---

## 빠른 명령어 참고

```bash
# 새 앱 생성
pnpm turbo gen app

# 특정 앱 실행
pnpm --filter 앱이름 dev

# 빌드 테스트
pnpm --filter 앱이름 build

# 스토리북
pnpm storybook
```
