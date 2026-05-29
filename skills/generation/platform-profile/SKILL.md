---
name: platform-profile
description: 채용 플랫폼별 맞춤 프로필 생성이 필요할 때
---

# 플랫폼별 프로필 생성

## 개요

`my_career_data.md` 원본 데이터를 기반으로 각 채용 플랫폼의 형식과 글자 수 제한에 맞춘 프로필/경력 콘텐츠를 생성합니다.

## 지원 플랫폼

| 플랫폼 | 코드 | 프로필 제한 | 경력 제한 | 특징 |
|--------|------|------------|----------|------|
| 리멤버 | `remember` | ~500자 | ~1000자/회사 | 명함 기반, 기본/구직용 분리 |
| 원티드 | `wanted` | ~300자 | 프로젝트 단위 | 개발자 채용 특화 |
| 사람인 | `saramin` | ~500자 | 자기소개서 형식 | 전통적 이력서 |
| 잡코리아 | `jobkorea` | ~500자 | 자기소개서 형식 | 사람인과 유사 |
| 링크드인 | `linkedin` | ~2600자 | 경험별 상세 | 영문/국문 버전 |

## 파라미터

| 파라미터 | 필수 | 기본값 | 설명 |
|---------|------|--------|------|
| `platform` | Y | - | remember, wanted, saramin, jobkorea, linkedin |
| `type` | N | all | profile, career, all |
| `mode` | N | basic | basic(네트워킹), jobseek(구직용) |

## 출력 경로

```
docs/career/platforms/{platform}/
├── profile-basic.md       # 기본 프로필 (mode=basic)
├── profile-jobseek.md     # 구직용 프로필 (mode=jobseek)
└── careers/
    ├── guhada.md          # 구하다 경력
    ├── interpark.md       # 인터파크 경력
    └── korealit.md        # 한국문헌정보기술 경력
```

## 실행 단계

### Step 1: 원본 데이터 읽기
```
docs/career/my_career_data.md
```
- Professional Summary 섹션 추출
- 경력 사항 섹션 추출
- 프로젝트별 STAR+I 내용 추출

### Step 2: 플랫폼 특성 적용

#### 리멤버 (remember)
- **프로필**: 헤드라인 + 핵심 가치 + 대표 성과 1-2개
- **경력**: 회사 소개 + 역할 + 주요 성과 bullet points
- **톤**: 기본용(차분), 구직용(적극적)

#### 원티드 (wanted)
- **프로필**: 한 줄 소개 + 핵심 역량 3가지
- **경력**: 프로젝트 단위 기술 (성과 중심)
- **톤**: 개발자 친화적, 기술 키워드 강조

#### 사람인/잡코리아 (saramin/jobkorea)
- **프로필**: 자기소개 형식 (지원동기 포함 가능)
- **경력**: 전통적 업무 기술서 형식
- **톤**: 정중한 비즈니스 톤

#### 링크드인 (linkedin)
- **About**: 스토리텔링 형식, 상세한 경력 요약
- **Experience**: 각 회사별 상세 기술
- **언어**: 국문(about-kr.md), 영문(about-en.md)

### Step 3: 글자 수 최적화
- 플랫폼별 제한에 맞춰 내용 축약/확장
- 핵심 성과 우선순위 적용
- 글자 수 체크 섹션 추가

### Step 4: 파일 생성
- 해당 플랫폼 디렉토리에 파일 생성
- 메타 정보 (용도, 톤, 글자 수) 포함
- 복사-붙여넣기용 코드 블록 포함

### Step 5: git add
```bash
git add docs/career/platforms/{platform}/
```

## 사용 예시

```
# 리멤버 전체 (프로필 + 경력)
/platform-profile remember

# 원티드 프로필만
/platform-profile wanted profile

# 리멤버 구직용 프로필
/platform-profile remember profile jobseek

# 링크드인 전체
/platform-profile linkedin
```

## 플랫폼별 톤 가이드

### 기본용 (basic)
- 현 직장 재직 중 뉘앙스
- 네트워킹/명함 교환 목적
- "~에 관심이 있습니다", "~를 중요하게 생각합니다"

### 구직용 (jobseek)
- 적극적 구직 의사 표현
- 성과 강조, 수치 부각
- "~를 달성했습니다", "~를 개선했습니다"

## 체크리스트

### 생성 전
- [ ] `my_career_data.md` 최신 상태 확인
- [ ] 대상 플랫폼 파라미터 확인
- [ ] 모드(basic/jobseek) 선택

### 생성 후
- [ ] 글자 수 제한 준수 확인
- [ ] 복사-붙여넣기 테스트
- [ ] 플랫폼 톤에 맞는지 확인
- [ ] git add 완료

## 주의사항

- 원본 데이터(`my_career_data.md`)는 수정하지 않음
- 플랫폼 파일은 항상 원본 기반으로 재생성
- 플랫폼별 글자 수 초과 시 경고 표시
