# devian-unity-samples — Policy

> **도메인:** devian-upm-samples  
> **정책 문서 버전:** v3

---

## 1. Templates 정의

**Templates**는 `com.devian.samples` UPM 패키지의 **Samples~** 폴더에 포함된 샘플 코드다.

- Unity Package Manager에서 "Import" 버튼으로 설치
- 설치 후 `Assets/Samples/`로 복사되어 프로젝트 소유가 됨
- 자유롭게 수정/삭제/확장 가능

---

## 2. 핵심 원칙

| 원칙 | 설명 |
|------|------|
| **단일 패키지** | 모든 템플릿은 `com.devian.samples` 패키지에 포함 |
| **Samples~ 방식** | Unity의 표준 샘플 제공 방식 사용 |
| **프로젝트 소유** | 설치 후 Assets/Samples/에 복사되어 프로젝트가 소유 |
| **충돌 방지** | `Devian` + `.Network.*`, `Devian` + `.Protocol.*`, `Devian` + `.Domain.*` 네임스페이스 사용 금지 |

---

## 3. 네이밍 규칙

### 3.1 UPM 패키지명

```
com.devian.samples
```

단일 패키지에 모든 템플릿이 Samples~로 포함됨.

### 3.2 샘플 폴더명

```
Samples~/<TemplateName>/
```

예시:
- `Samples~/Network/`
- `Samples~/Game/`

### 3.3 asmdef 이름 (어셈블리명)

```
`Devian` + `.Templates.<TemplateName>`
`Devian` + `.Templates.<TemplateName>.Editor`
```

예시:
- `Devian` + `.Templates.Network`
- `Devian` + `.Templates.Network.Editor`

> **주의**: 위는 asmdef의 `name`(어셈블리명)이다. 코드의 namespace와 혼동하지 않는다.

### 3.4 namespace (Hard Rule)

**모든 샘플 코드는 단일 네임스페이스 `Devian`을 사용한다.**

```csharp
namespace Devian
```

> asmdef의 `rootNamespace`도 `"Devian"`으로 설정한다.

### 3.5 금지 프리픽스 (네임스페이스)

샘플 코드에서 다음 네임스페이스 사용 금지:

- `Devian` + `.Network.*`
- `Devian` + `.Protocol.*`
- `Devian` + `.Domain.*`
- `Devian` + `.Core.*`
- `Devian` + `.Templates.*`

> 어셈블리명(asmdef name)은 `Devian` + `.Templates.*`를 사용하지만, namespace는 `Devian` 단일만 사용한다.

---

## 4. 경로 정책

### 4.1 Template 원본 (upm)

```
framework-cs/upm/com.devian.samples/
├── package.json
├── Samples~/
│   ├── Network/
│   │   ├── Runtime/
│   │   │   ├── `[asmdef: Devian` + `.Templates.Network]`
│   │   │   └── *.cs
│   │   ├── Editor/
│   │   │   ├── `[asmdef: Devian` + `.Templates.Network.Editor]`
│   │   │   └── *.cs
│   │   └── README.md
│   └── (다른 템플릿들...)
└── README.md
```

### 4.2 빌드 출력 (packageDir)

```
{upmConfig.packageDir}/com.devian.samples/
```

### 4.3 설치 후 위치 (Unity 프로젝트)

```
Assets/Samples/Devian Templates/{version}/{TemplateName}/
```

---

## 5. package.json 구조

```json
{
  "name": "com.devian.samples",
  "version": "0.1.0",
  "displayName": "Devian Templates",
  "description": "Templates for Devian framework.",
  "unity": "2021.3",
  "samples": [
    {
      "displayName": "Network",
      "description": "WebSocket client template.",
      "path": "Samples~/Network"
    }
  ]
}
```

---

## 6. 사용법

### 6.1 Unity에서 설치

1. Window → Package Manager
2. `Devian Templates` 패키지 선택
3. Samples 섹션에서 원하는 템플릿 "Import" 클릭

### 6.2 설치 후 위치

```
Assets/Samples/Devian Templates/0.1.0/Network/
├── Runtime/
│   ├── `[asmdef: Devian` + `.Templates.Network]`
│   └── EchoWsClientSample.cs
└── Editor/
    ├── `[asmdef: Devian` + `.Templates.Network.Editor]`
    └── EchoWsClientSampleEditor.cs
```

---

## 7. 새 템플릿 추가 방법

1. `Samples~/` 아래에 새 폴더 생성
2. Runtime/, Editor/ 폴더 및 asmdef/코드 추가
3. `package.json`의 `samples` 배열에 항목 추가
4. `skills/devian-unity-samples/`에 새 스킬 문서 추가

---

## 8. FAIL 조건

- [ ] Templates 패키지에 Devian.Network.*/Devian.Protocol.* asmdef가 존재
- [ ] package.json name이 `com.devian.samples`가 아님
- [ ] Samples~ 폴더가 없거나 비어있음
- [ ] samples 메타데이터가 package.json에 없음
