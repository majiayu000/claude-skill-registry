---
name: iaud-project-guide
description: i-AUD Developer Kit 프로젝트 가이드. 프로젝트 구조, 폴더 설명, 개발 환경 설정, VS Code 확장 명령어에 대해 안내합니다. "i-AUD란?", "프로젝트 구조", "폴더 설명", "개발 환경", "AUD 명령어" 등을 물어볼 때 사용하세요.
---

# i-AUD Developer Kit 프로젝트 가이드

## 1. 프로젝트 개요

### i-AUD란?
- **AUD Platform**은 업무시스템 화면 개발을 위한 통합 UI 개발 플랫폼입니다
- BI 툴, 리포팅 툴, 시각화 분석 툴, UI/UX 툴의 기능을 하나로 통합
- **i-AUD**는 AUD Platform의 핵심 도구로 WYSIWYG 방식의 웹 애플리케이션 개발 환경 제공
- TypeScript(JavaScript) 단일 언어로 클라이언트/서버 개발 가능

### i-AUD Developer Kit이란?
VS Code에서 i-AUD 보고서 및 스크립트를 개발할 수 있는 공식 확장(extension) 도구입니다.

**주요 기능:**
- 보고서 다운로드/업로드
- TypeScript 기반 클라이언트/서버 스크립트 개발
- 자동 빌드 및 배포
- 보고서 컨트롤 코드 자동 생성

---

## 2. 프로젝트 폴더 구조

```
i-AUD-Developer-Kit/
├── .vscode/
│   └── settings.json          # AUD 서버 연결 설정
├── src/
│   ├── com/                    # 서버 스크립트용 API (Rhino JavaScript)
│   │   └── matrix/
│   │       ├── script/         # Matrix, Connection, RecordSet 등
│   │       ├── olap/           # OLAP 관련 API
│   │       └── Excel/          # Excel 처리 API
│   ├── aud/                    # 클라이언트 스크립트용 API
│   │   ├── control/            # UI 컨트롤 (Button, Grid, Chart 등)
│   │   ├── common/             # 공통 유틸리티 (UserInfo, ReportInfo 등)
│   │   ├── data/               # 데이터 관련 (DataSet, DataTable 등)
│   │   └── enums/              # 열거형 타입들
│   └── reports/                # 샘플 보고서 및 개발 보고서
│       ├── samples/            # 샘플 보고서 모음
│       │   ├── MX_GRID/        # MX-GRID 컴포넌트 샘플
│       │   ├── OLAP/           # OLAP 그리드 샘플
│       │   └── ETC/            # 기타 샘플들
│       └── [보고서폴더]/       # 실제 개발 보고서들
├── out/                        # TypeScript 빌드 출력
└── node_modules/               # npm 패키지
```

---

## 3. 보고서(프로그램) 폴더 구조

각 보고서 폴더는 다음과 같은 구조를 가집니다:

```
[보고서명]/
├── .aud.json                   # 프로그램 메타 정보 (ReportCode, FolderCode 등)
├── [보고서명].mtsd             # 화면 UI 배치, 데이터소스, 서비스 정의 (JSON)
├── [보고서명].script.ts        # 클라이언트 스크립트 (TypeScript)
├── [보고서명].script.js        # 클라이언트 스크립트 (JavaScript)
├── DataSource/                 # 데이터 조회 SQL 파일들
│   └── *.sql
└── ServerScript/               # 서버 스크립트 (Rhino 엔진 사용)
    ├── *.ts                    # TypeScript 서버 스크립트
    └── *.sql                   # SQL 파일
```

### 파일 설명

| 파일 | 설명 |
|------|------|
| `.aud.json` | 프로그램 상세 저장 정보 (ReportCode, ReportName, FolderCode 등) |
| `*.mtsd` | 화면 UI 배치, 데이터 소스, 서비스가 포함된 JSON 문서 (최종 output) |
| `*.script.ts` | 클라이언트 스크립트 소스 (.ts 우선 탐색) |
| `DataSource/*.sql` | DB 조회용 SQL 파일들 |
| `ServerScript/*.ts` | 서버 스크립트 (개별 파일이 서비스가 됨) |

---

## 4. 개발 환경 설정

### 4.1 설정 파일 (.vscode/settings.json)

```json
{
    "aud.config": {
        "SourcePath": "D:\\aud_report\\src\\reports\\",
        "OutputPath": "D:\\aud_report\\out\\reports\\",
        "ServiceURL": "http://server.com:8080",
        "UserName": "{계정명}",
        "ApiKey": "{API 키}",
        "AutoBuild": false,
        "MX_GRID_BACKUP": true,
        "MX_GRID_JSON_PRETTY": true,
        "QueryResultLimit": 100,
        "QueryResultFileName": "QueryResult.txt"
    }
}
```

### 4.2 TypeScript 빌드 설정

```bash
# 패키지 설치
npm install

# TypeScript watch 모드 실행 (자동 빌드)
tsc --w
```

---

## 5. VS Code 명령어 (Command Palette)

| 명령어 | 단축키 | 설명 |
|--------|--------|------|
| `AUD: Download Report` | - | 서버에서 프로그램 다운로드 |
| `AUD: Download Folder` | - | 특정 폴더 하위 모든 보고서 다운로드 |
| `AUD: Pull Report` | - | 서버 최신 정보로 업데이트 |
| `AUD: Publish Script` | `Ctrl+Alt+S` | 스크립트를 서버에 배포 |
| `AUD: Run Designer` | `Ctrl+Alt+D` | 브라우저로 프로그램 실행 |
| `AUD: Deploy Report` | - | 디자인 정보 포함 전체 배포 |
| `AUD: Generate Starter Code` | - | TypeScript 기본 구조 생성 |
| `AUD: Execute Query` | `Ctrl+F5` | 선택한 SQL 실행 |
| `AUD: Generate Control Variables` | - | 보고서 내 컨트롤 변수 선언 생성 |

---

## 6. 개발 워크플로우

1. **i-AUD Designer**에서 새 보고서 생성 및 컴포넌트 배치
2. **VS Code**에서 `AUD: Download Report`로 다운로드
3. `.script.js` → `.script.ts`로 확장자 변경
4. `AUD: Generate Starter Code`로 기본 구조 생성
5. `tsc --w`로 TypeScript watch 모드 실행
6. 스크립트 개발 후 `AUD: Publish Script` (Ctrl+Alt+S)로 배포
7. `AUD: Run Designer` (Ctrl+Alt+D)로 테스트

---

## 7. API 참조 위치

- **클라이언트 API**: `types/aud/` 폴더의 TypeScript 인터페이스 참조
- **서버 API**: `types/com/` 폴더의 TypeScript 인터페이스 참조
- **샘플 코드**: `src/reports/samples/` 폴더의 예제 참조
