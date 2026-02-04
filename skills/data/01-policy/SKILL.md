# devian-unity-samples — Policy

> **도메인:** devian-upm-samples
> **정책 문서 버전:** v4

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
Devian.Samples.<TemplateName>
Devian.Samples.<TemplateName>.Editor
```

예시:
- `Devian.Samples.Network`
- `Devian.Samples.Network.Editor`

> **주의**: 위는 asmdef의 `name`(어셈블리명)이다. 코드의 namespace와 혼동하지 않는다.

### 3.4 namespace (Hard Rule)

**모든 샘플 코드는 단일 네임스페이스 `Devian`을 사용한다.**

```csharp
namespace Devian
```

> asmdef의 `rootNamespace`도 `"Devian"`으로 설정한다.

### 3.4.1 Protocol handlers 구현 정책 (Hard Rule)

**어셈블리 제약:**
`Devian.Protocol.*` 어셈블리에서 생성된 `*_Handlers.g.cs`는 **다른 asmdef(샘플 asmdef 포함)에서 partial로 확장할 수 없다.**
(C#의 partial class는 동일 어셈블리 내에서만 동작)

**따라서 샘플에서 수신 처리 예시는 아래 방법으로 구현한다:**

1. **Stub 상속 (권장):** `Devian.Protocol.{Group}.{ProtocolName}.Stub`를 샘플 어셈블리에서 상속 구현
   - 예: `class SampleGame2CStub : Game2C.Stub`
   - 샘플이 자체 어셈블리에서 자유롭게 구현 가능

2. **(참고) 프로토콜 패키지 내부:** partial 확장은 프로토콜 패키지 내부에서만 가능 (샘플 범위 밖)

**금지 (Hard):**
- 샘플에서 `partial class *_Handlers` 형태로 확장 시도 금지 (컴파일 불가, 오해 유발)
- 샘플에서 `namespace Devian.Protocol.*` 사용 금지 (Stub 상속 시에도 `namespace Devian` 사용)

### 3.5 금지 프리픽스 (네임스페이스)

샘플 코드에서 다음 네임스페이스 사용 금지:

- `Devian.Network.*`
- `Devian.Protocol.*` (샘플 어셈블리에서 사용 불가 — 3.4.1 참조)
- `Devian.Domain.*`
- `Devian.Core.*`
- `Devian.Templates.*` (샘플 코드 namespace로 사용 금지)
- `Devian.Samples.*` (샘플 코드 namespace로 사용 금지 — asmdef name으로만 사용)

> 어셈블리명(asmdef name)은 `Devian.Samples.*`를 사용하지만, namespace는 `Devian` 단일만 사용한다.

---

## 4. 경로 정책

### 4.1 Template 원본 (upm)

```
framework-cs/upm/com.devian.samples/
├── package.json
├── Samples~/
│   ├── Network/
│   │   ├── Runtime/
│   │   │   ├── [asmdef: Devian.Samples.Network]
│   │   │   └── *.cs
│   │   ├── Editor/
│   │   │   ├── [asmdef: Devian.Samples.Network.Editor]
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
Assets/Samples/Devian Samples/0.1.0/Network/
├── README.md
└── Runtime/
    ├── [asmdef: Devian.Samples.Network]
    ├── GameNetworkClientSample.cs
    ├── GameNetworkClient.cs
    └── GameNetworkClient_Stub.cs   (Game2C.Stub 상속 구현)
```

---

## 7. 새 템플릿 추가 방법

1. `Samples~/` 아래에 새 폴더 생성
2. Runtime/, Editor/ 폴더 및 asmdef/코드 추가
3. `package.json`의 `samples` 배열에 항목 추가
4. `skills/devian-unity-samples/`에 새 스킬 문서 추가

---

## 8. FAIL 조건

- [ ] 샘플 패키지에 `Devian.Network.*`/`Devian.Protocol.*` namespace 코드가 존재
- [ ] 샘플에서 `partial class *_Handlers` 확장 시도 (컴파일 불가)
- [ ] package.json name이 `com.devian.samples`가 아님
- [ ] Samples~ 폴더가 없거나 비어있음
- [ ] samples 메타데이터가 package.json에 없음
