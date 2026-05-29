---
name: sync-platforms
description: 채용 플랫폼 프로필 일괄 동기화가 필요할 때
---

# 플랫폼 일괄 동기화

## 개요

`my_career_data.md` 원본 데이터가 변경되었을 때, 모든 채용 플랫폼(리멤버, 원티드, 사람인, 잡코리아, 링크드인)의 프로필/경력 파일을 한 번에 업데이트합니다.

## 대상 플랫폼

| 플랫폼 | 파일 수 | 경로 |
|--------|--------|------|
| 리멤버 | 5개 | `platforms/remember/` |
| 원티드 | 2개+ | `platforms/wanted/` |
| 사람인 | 2개 | `platforms/saramin/` |
| 잡코리아 | 2개 | `platforms/jobkorea/` |
| 링크드인 | 5개+ | `platforms/linkedin/` |

## 실행 단계

### Step 1: 변경사항 확인
```bash
git diff docs/career/my_career_data.md
```
- 변경된 섹션 식별 (프로필/경력/프로젝트)
- 영향받는 플랫폼 파일 목록 생성

### Step 2: 플랫폼별 동기화

각 플랫폼에 대해 `/platform-profile` 스킬 실행:

```
/platform-profile remember all
/platform-profile wanted all
/platform-profile saramin all
/platform-profile jobkorea all
/platform-profile linkedin all
```

### Step 3: 변경 리포트 생성

```
## 동기화 결과

### 변경된 원본 내용
- Professional Summary: 수정됨
- 구하다 프로젝트: Seeding 성과 추가

### 업데이트된 파일
| 플랫폼 | 파일 | 상태 |
|--------|------|------|
| remember | profile-basic.md | 업데이트 |
| remember | profile-jobseek.md | 업데이트 |
| remember | careers/guhada.md | 업데이트 |
| wanted | profile.md | 업데이트 |
| ... | ... | ... |

### 글자 수 검증
| 플랫폼 | 파일 | 현재 | 제한 | 상태 |
|--------|------|------|------|------|
| remember | profile-basic.md | 230자 | 500자 | OK |
| remember | profile-jobseek.md | 520자 | 500자 | 초과 |
```

### Step 4: git add
```bash
git add docs/career/platforms/
```

## 사용 예시

```
# 전체 플랫폼 동기화
/sync-platforms

# 특정 플랫폼만 동기화 (내부적으로 /platform-profile 호출)
/sync-platforms remember
/sync-platforms linkedin
```

## 동기화 우선순위

1. **리멤버** - 가장 자주 사용, 최우선 동기화
2. **원티드** - 개발자 채용 주요 플랫폼
3. **링크드인** - 글로벌 네트워킹
4. **사람인/잡코리아** - 범용 채용 플랫폼

## 체크리스트

### 동기화 전
- [ ] `my_career_data.md` 변경사항 확인
- [ ] 변경된 섹션 식별

### 동기화 후
- [ ] 모든 플랫폼 파일 업데이트 확인
- [ ] 글자 수 제한 준수 확인
- [ ] 초과 파일 수동 조정
- [ ] git add 완료
- [ ] 변경 리포트 확인

## 주의사항

- 원본 데이터(`my_career_data.md`)는 수정하지 않음
- 글자 수 초과 시 경고만 표시, 자동 축약하지 않음
- 플랫폼별 톤/형식은 `/platform-profile` 스킬 기준 적용
- 새 플랫폼 추가 시 이 스킬과 `/platform-profile` 모두 업데이트 필요
