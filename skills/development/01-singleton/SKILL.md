# 01-singleton

Status: ACTIVE  
AppliesTo: v10  
Type: Policy

---

## 1. 목적

Unity용 Singleton **정책**을 정의한다.  
이 스킬은 **싱글톤 계열 정책 묶음**이며, 정확히 5개의 타입을 제공한다.

---

## 2. 범위

### 포함

- **SceneSingleton\<T\>** - Scene-Placed / Persistent (자동 생성 없음)
- **MonoSingleton\<T\>** - [Obsolete] SceneSingleton 래퍼 (호환성용)
- **AutoSingleton\<T\>** - AutoCreate / Persistent (Instance 접근 시 자동 생성)
- **ResSingleton\<T\>** - Resources / Persistent (Resources.Load로 생성)
- **SimpleSingleton\<T\>** - Pure C# / Lazy 기반 / 스레드 안전 (Unity 오브젝트 의존 없음)
- 공통 규약 (중복 처리, 영속성, 네임스페이스, 스레드)
- API 시그니처 정본
- 확장 정책

### 제외

- Scene 종속형 Singleton (별도 스킬로 분리)
- 실제 C# 구현 코드
- 위 5개 외 다른 singleton 타입

---

## 3. 용어 정의

| 용어 | 정의 |
|------|------|
| Persistent Singleton | `DontDestroyOnLoad`로 씬 전환에도 유지되는 싱글톤 |
| Scene Singleton | 특정 씬 내에서만 유효한 싱글톤 (이 스킬에서 제외) |
| Scene-Placed Singleton | 씬 배치 또는 명시적 등록으로만 인스턴스 생성 (SceneSingleton) |
| AutoCreate Singleton | Instance 접근 시 인스턴스가 없으면 자동 생성 (AutoSingleton) |
| Resources Singleton | Resources.Load로 프리팹을 로드하여 생성 (ResSingleton) |

---

## 4. 공통 규약 (Common Rules)

모든 타입에 적용되는 기본 규칙이다. 타입별 섹션에서 더 엄격하게 정의할 수 있으나, 완화는 금지.

### 4.1 네이밍 규약 (정본)

제공 타입 이름은 **정확히 5개만** 사용:

| 타입 이름 | 용도 |
|-----------|------|
| `SceneSingleton<T>` | Scene-Placed / Persistent (자동 생성 없음) |
| `MonoSingleton<T>` | **[Obsolete]** SceneSingleton 래퍼 (호환성용) |
| `AutoSingleton<T>` | AutoCreate / Persistent |
| `ResSingleton<T>` | Resources / Persistent |
| `SimpleSingleton<T>` | Pure C# / Lazy / Thread-safe |

- **위 이름 외 "더 긴 이름/다른 접두사/접미사" 금지**
- 네임스페이스: **`namespace Devian`** 고정

### 4.2 영속성 (Persistence)

- Singleton은 기본적으로 **Persistent**이며 `DontDestroyOnLoad(gameObject)` 적용 전제
- 씬 전환 시에도 인스턴스 유지

### 4.3 중복 인스턴스 처리 (정본)

```
Awake()에서 기존 인스턴스(_instance)가 있고 자기 자신이 아니면:
  → 새로 뜬 쪽(this)을 Destroy (기존 유지)
```

- 기존 인스턴스 우선 정책
- **"둘 다 살려두기" 금지**

### 4.4 스레드 규약 (정본)

- Unity 오브젝트 생성/파괴/Resources.Load/Instantiate는 **메인 스레드에서만 허용**
- **메인 스레드가 아닐 경우: throw (정본)**
- `Awake()`, `Register()`, `Create()`, `Load()` 등은 메인 스레드에서만 동작

### 4.5 씬 종속형 제외

- 씬 종속형 singleton은 이 스킬 범위 밖
- 별도 스킬(예: `02-scene-singleton`)로 분리

### 4.6 멀티스레드 경계

> Log 같은 시스템에서 "어떤 스레드에서든 호출"을 원하면,  
> 그것은 **singleton 템플릿이 아니라 sink/pump 설계**로 해결한다.  
> 예: `Log.Info()`는 큐에 메시지를 넣고, 메인 스레드의 pump가 처리.

---

## 5. 타입 A: SceneSingleton\<T\> (Scene-Placed / Persistent)

### 5.1 목적

자동 생성 없이 **씬 배치 또는 명시적 등록**으로만 인스턴스를 관리한다.  
Instance가 없으면 예외를 발생시켜 개발자가 누락을 즉시 인지하도록 한다.

### 5.2 필수 규약 (정본)

| 항목 | 규칙 |
|------|------|
| **자동 생성** | **금지** - Instance는 생성하지 않는다 |
| **Resources.Load** | **금지** |
| **Instance 없을 때** | **throw** (`InvalidOperationException`) |
| **허용되는 생성 방식** | 씬 배치 또는 명시적 Register 호출 |
| **중복 처리** | 신규 Destroy, 기존 유지 |
| **영속성** | 등록된(유효한) 인스턴스에 DontDestroyOnLoad 적용 |
| **메인 스레드 강제** | Register() 호출 시 `UnityMainThread.EnsureOrThrow()` |

### 5.3 Instance 실패 정책 (정본)

```csharp
public static T Instance
{
    get
    {
        if (s_instance == null)
            throw new InvalidOperationException(
                $"[{typeof(T).Name}] Instance not found. " +
                "SceneSingleton requires scene placement or explicit Register() call.");
        return s_instance;
    }
}
```

### 5.4 API 시그니처 (정본)

```csharp
namespace Devian
{
    public abstract class SceneSingleton<T> : MonoBehaviour where T : SceneSingleton<T>
    {
        /// <summary>인스턴스 존재 여부</summary>
        public static bool HasInstance { get; }

        /// <summary>싱글톤 인스턴스 (없으면 throw)</summary>
        /// <exception cref="InvalidOperationException">인스턴스가 존재하지 않을 때</exception>
        public static T Instance { get; }

        /// <summary>명시적 인스턴스 등록 (메인 스레드 전용, 자동 생성 아님)</summary>
        /// <remarks>Register()에서 UnityMainThread.EnsureOrThrow() 호출</remarks>
        public static void Register(T instance);
    }
}
```

---

## 5.5. MonoSingleton\<T\> (Obsolete - SceneSingleton 래퍼)

### 목적

**[Obsolete]** `SceneSingleton<T>` 또는 `AutoSingleton<T>`를 대신 사용하라.

MonoSingleton은 기존 코드 호환성을 위해 유지되며, `SceneSingleton<T>`의 얇은 래퍼이다.

```csharp
namespace Devian
{
    [Obsolete("Use SceneSingleton<T> or AutoSingleton<T> instead.")]
    public abstract class MonoSingleton<T> : SceneSingleton<T> where T : MonoSingleton<T>
    {
        // All functionality inherited from SceneSingleton<T>
    }
}
```

- 모든 기능은 `SceneSingleton<T>`에서 상속
- 신규 코드에서는 `SceneSingleton<T>` 또는 `AutoSingleton<T>` 직접 사용 권장

---

## 6. 타입 B: AutoSingleton\<T\> (AutoCreate / Persistent)

### 6.1 목적

사용자는 `T.Instance` 접근 시 인스턴스가 없으면 **자동 생성**된다.  
단, Unity 제약으로 인해 **자동 생성은 메인 스레드에서만** 허용한다.

### 6.2 Instance 동작 순서 (정본)

Instance 로직은 **반드시 아래 순서**를 따른다:

```
1. _instance가 있으면 → 반환
2. 없으면 씬에서 기존 인스턴스 탐색 후 채택
   - FindObjectOfType<T>(includeInactive: true) 또는 동등한 방식
   - 활성/비활성 오브젝트 모두 탐색
3. 그래도 없으면 → 새 GameObject 생성 + AddComponent<T>()
4. 첫 인스턴스에 DontDestroyOnLoad 적용
```

| 단계 | 설명 |
|------|------|
| Step 1 | 캐시된 인스턴스 확인 |
| Step 2 | 씬 탐색 (Find-first) - 비활성 포함 |
| Step 3 | 자동 생성 (메인 스레드 강제) |
| Step 4 | 영속성 적용 |

### 6.3 필수 규약 (정본)

| 항목 | 규칙 |
|------|------|
| **메인 스레드 강제** | Step 2~3 진입 시 `InitIfNeeded()` → `EnsureOrThrow()`로 메인 스레드 강제, 아니면 **throw** |
| **Resources.Load** | **금지** |
| **중복 처리** | 신규 Destroy, 기존 유지 |
| **종료 중 재생성** | **금지** (throw) |

### 6.4 스레드 규칙 (정본)

```csharp
// 정본: InitIfNeeded MUST be called first to prevent false negatives during early initialization
UnityMainThread.InitIfNeeded();
UnityMainThread.EnsureOrThrow($"{typeof(T).Name}.Instance");
```

- `InitIfNeeded()`가 먼저 호출되어 초기화 타이밍 문제 방지
- 이미 인스턴스가 존재하면 메인 스레드 체크 스킵 (fast path)
- **단, Unity 객체 접근이 섞이므로 권장하지 않음**

### 6.5 종료 중 재생성 금지 (정본)

```csharp
private static bool _isQuitting = false;

private void OnApplicationQuit()
{
    _isQuitting = true;
}

public static T Instance
{
    get
    {
        if (_isQuitting)
            throw new InvalidOperationException(
                $"[{typeof(T).Name}] Cannot access singleton during application quit.");
        // ... 나머지 로직
    }
}
```

- **종료 중 Instance 호출 시: throw (정본)**

### 6.6 API 시그니처 (정본)

```csharp
namespace Devian
{
    public class AutoSingleton<T> : MonoBehaviour where T : AutoSingleton<T>
    {
        /// <summary>인스턴스 존재 여부</summary>
        public static bool HasInstance { get; }

        /// <summary>
        /// 싱글톤 인스턴스 (없으면 자동 생성)
        /// - 메인 스레드가 아니면 throw
        /// - 종료 중이면 throw
        /// </summary>
        public static T Instance { get; }
    }
}
```

---

## 7. 타입 C: ResSingleton\<T\> (Resources / Persistent)

### 7.1 목적

**Resources.Load**로 프리팹을 로드해 생성하는 singleton을 제공한다.  
**이 타입에서만 Resources 사용을 허용한다.** (MonoSingleton/AutoSingleton은 금지)

### 7.2 필수 규약 (정본)

| 항목 | 규칙 |
|------|------|
| **생성 방식** | `Load(string resourcePath)` 명시적 호출 (정본) |
| **경로 자동 유추** | **금지** (리플렉션/타입명 조합 등 금지) |
| **Instance 없을 때** | **throw** (사용자가 Load를 먼저 호출해야 함) |
| **메인 스레드 강제** | Load 호출 시 메인 스레드가 아니면 **throw** |
| **프리팹에 T 없음** | **throw** (리소스/프리팹 구성 오류) |
| **중복 처리** | 이미 있으면 기존 반환 (추가 로드 무시) |

### 7.3 Load 동작 순서 (정본)

```
1. 메인 스레드 확인 → 아니면 throw
2. _instance가 이미 있으면 → 기존 인스턴스 반환 (추가 로드 무시)
3. Resources.Load<GameObject>(resourcePath)로 프리팹 로드
4. prefab == null이면 throw (리소스 없음)
5. Instantiate(prefab) 후 GetComponent<T>()
6. component == null이면 throw (프리팹에 T 없음)
7. DontDestroyOnLoad 적용
8. _instance에 할당 후 반환
```

### 7.4 Instance 정책 (정본)

```csharp
public static T Instance
{
    get
    {
        if (_instance == null)
            throw new InvalidOperationException(
                $"[{typeof(T).Name}] Instance not found. " +
                "Call Load(resourcePath) first to create the singleton.");
        return _instance;
    }
}
```

- **Instance는 존재하지 않으면 throw**
- 사용자가 `Load(path)`를 먼저 호출해야 함
- Instance가 내부적으로 마지막 경로를 기억하고 로드하는 방식은 **금지** (상태/추측 발생)

### 7.5 API 시그니처 (정본)

```csharp
namespace Devian
{
    public class ResSingleton<T> : MonoBehaviour where T : ResSingleton<T>
    {
        /// <summary>인스턴스 존재 여부</summary>
        public static bool HasInstance { get; }

        /// <summary>싱글톤 인스턴스 (없으면 throw, Load 선행 필요)</summary>
        /// <exception cref="InvalidOperationException">인스턴스가 존재하지 않을 때</exception>
        public static T Instance { get; }

        /// <summary>
        /// Resources에서 프리팹 로드 후 인스턴스 생성 (메인 스레드 전용)
        /// - 이미 인스턴스가 있으면 기존 반환
        /// - 프리팹이 없거나 T 컴포넌트가 없으면 throw
        /// </summary>
        /// <param name="resourcePath">Resources 폴더 내 프리팹 경로</param>
        public static T Load(string resourcePath);
    }
}
```

### 7.6 금지사항 (ResSingleton 내부)

| 금지 항목 | 이유 |
|-----------|------|
| resourcePath 없이 자동 경로 유추 | 리플렉션/타입명 조합 등은 예측 불가능한 동작 유발 |
| MonoSingleton/AutoSingleton에 Resources 허용 역수입 | SSOT 위반 |

---

## 8. 타입 D: SimpleSingleton\<T\> (Pure C# / Lazy)

### 8.1 목적

Unity API에 의존하지 않는 **순수 C# 싱글톤** 베이스를 제공한다.
`Lazy<T>`를 사용하여 스레드 안전하고, MonoBehaviour/씬 생명주기와 무관하게 동작한다.

사용처:
- Unity 오브젝트/씬 의존 없는 서비스
- 캐시/매퍼/레지스트리 등 순수 데이터 관리 클래스

### 8.2 필수 규약 (정본)

| 항목 | 규칙 |
|------|------|
| **제약** | `where T : SimpleSingleton<T>, new()` |
| **Unity API** | **금지** (MonoBehaviour, UnityEngine.Object 상속 금지) |
| **생성 시점** | `Instance` 최초 접근 시 1회 생성 |
| **스레드 안전성** | `Lazy<T>` (isThreadSafe: true)로 보장 |
| **외부 생성** | **금지** (protected 생성자) |

### 8.3 API 시그니처 (정본)

```csharp
namespace Devian
{
    public abstract class SimpleSingleton<T>
        where T : SimpleSingleton<T>, new()
    {
        /// <summary>싱글톤 인스턴스 (최초 접근 시 생성)</summary>
        public static T Instance { get; }
        
        protected SimpleSingleton() { }
    }
}
```

### 8.4 금지사항

| 금지 항목 | 이유 |
|-----------|------|
| MonoBehaviour 상속 | Unity 생명주기 의존성 발생 |
| public 생성자 | 외부에서 직접 생성 허용 방지 |
| Reset/Dispose 등 추가 API | 이 스킬 범위 밖 (필요시 별도 확장) |

### 8.5 SimpleSingleton 안전 규약 (정본)

**금지:**

| 금지 항목 | 이유 |
|-----------|------|
| 생성자(ctor)에서 `Instance` 호출 | 초기화 순서 미보장, 무한 재귀 위험 |
| 정적 필드 초기화 / 정적 생성자(static ctor)에서 `Instance` 호출 | 타입 로딩 시점 문제, Unity Editor ScriptableSingleton 충돌 |
| `[InitializeOnLoad]`, `[InitializeOnLoadMethod]`에서 즉시 `Instance` 호출 | 에디터 로딩 완료 전 접근 시 경고/에러 발생 |

**권장 패턴:**

- 무거운 초기화는 생성자 대신 `Init()` 같은 명시적 메서드로 분리
- 호출 타이밍은 게임 시작 이후(예: Start/Awake 이후) 또는 사용자 액션 이후로 지연
- 에디터 초기화가 필요하면 `EditorApplication.delayCall`을 사용해 "에디터 로딩 완료 후" 실행

**가드 구현:**

- `UNITY_EDITOR || DEVELOPMENT_BUILD` 조건부로 StackTrace 기반 검사
- Instance 최초 생성 시 1회만 실행 (Lazy 람다 내부)
- **System/Unity 내부 프레임은 제외** (System.*, Microsoft.*, UnityEngine.*, UnityEditor.* 어셈블리)
- **사용자/에디터 스크립트의 ctor/static-init만 탐지**
- InitializeOnLoad/InitializeOnLoadMethod attribute도 reflection으로 감지 (UNITY_EDITOR에서)
- 생성자/정적 생성자/InitializeOnLoad에서 호출 감지 시 `InvalidOperationException` 발생

> **Note**: SimpleSingleton은 수기 코드이며, 생성기는 `Generated/` 폴더만 다룬다.

---

## 9. 확장 정책 (추가 Singleton 타입)

### 8.1 확장 규칙

이 스킬(01-singleton-template)은 **싱글톤 템플릿 묶음**이며, 추가 타입은 이 문서에 섹션으로 추가한다.

| 규칙 | 설명 |
|------|------|
| 공통 규약 준수 | 섹션 4의 공통 규약을 반드시 준수 |
| 완화 금지 | 공통 규약보다 느슨한 정책은 불가 |
| 이름 규칙 | 타입 이름은 짧게, 기존 3종 이름은 변경 금지 |
| Scene Singleton | 별도 스킬로 분리 (예: `02-scene-singleton`) |

### 8.2 신규 타입 추가 시 필수 정의 항목

| 항목 | 설명 |
|------|------|
| 생성 방식 | 자동/수동/리소스, 허용 방식 |
| 중복 처리 | 공통 규약 준수 여부 |
| 영속성 | Persistent/Scene-bound |
| 스레드 규칙 | 메인 스레드 강제 여부, 예외 처리 |

---

## 9. DoD 체크리스트

### 네이밍/구조

- [x] `SceneSingleton<T>`, `MonoSingleton<T>`, `AutoSingleton<T>`, `ResSingleton<T>`, `SimpleSingleton<T>` 이름이 SSOT로 명시
- [x] `MonoSingleton<T>`이 [Obsolete]로 표시되고 SceneSingleton 래퍼임이 명시
- [x] 네임스페이스 `Devian` 고정 규약이 명시
- [x] "씬 종속형은 별도 스킬"이 명시

### SceneSingleton (신규)

- [x] 자동 생성 금지가 명시
- [x] Resources.Load 금지가 명시
- [x] Instance 없으면 throw가 명시
- [x] Register()에서 메인 스레드 강제가 명시

### MonoSingleton

- [x] [Obsolete] 표시 및 SceneSingleton 래퍼임이 명시
- [x] 모든 기능이 SceneSingleton에서 상속됨이 명시

### AutoSingleton

- [x] Find-first → Create 순서가 명시
- [x] 메인 스레드 강제 (InitIfNeeded() → EnsureOrThrow())가 명시
- [x] Resources.Load 금지가 명시
- [x] 종료 중 재생성 방지 (throw)가 명시

### ResSingleton

- [x] Resources.Load 허용 범위가 ResSingleton만으로 제한
- [x] `Load(string resourcePath)` 정본 API가 명시
- [x] 프리팹에 T가 없으면 throw가 명시
- [x] Instance 정책 (Load 선행 필요, 없으면 throw)이 명시
- [x] 경로 자동 유추 금지가 명시

### SimpleSingleton

- [x] `SimpleSingleton<T>` 이름/경로/네임스페이스가 SSOT로 명시
- [x] Pure C# / Lazy 기반 / 스레드 안전이 명시
- [x] Unity API 금지가 명시

---

## 10. 파일 위치 및 소유권 (정본)

이 스킬의 C# 코드는 **고정 유틸(수기 코드)** 영역에 속하며, 생성기가 건드리지 않는다.

### 소유권 정책 (SSOT: 03-ssot)

| 영역 | 정책 |
|------|------|
| `Runtime/_Shared/` | 고정 유틸(수기) — 생성기 clean/generate 금지 |
| `Runtime/Singleton/` | 고정 유틸(수기) — 생성기 clean/generate 금지 |
| `Runtime/Pool/` | 고정 유틸(수기) — 생성기 clean/generate 금지 |
| `Runtime/PoolFactories/` | 고정 유틸(수기) — 생성기 clean/generate 금지 |
| `Runtime/Generated/**` | 생성기 관리 영역 (Generated Only) |
| `Editor/Generated/**` | 생성기 관리 영역 (Generated Only) |

### 파일 위치 (고정)

```
com.devian.foundation/Runtime/Unity/
├── _Shared/
│   └── UnityMainThread.cs     (공용 내부 헬퍼)
└── Singleton/
    ├── SceneSingleton.cs      (Scene-Placed, 자동 생성 없음)
    ├── MonoSingleton.cs       ([Obsolete] SceneSingleton 래퍼)
    ├── AutoSingleton.cs
    ├── ResSingleton.cs
    └── SimpleSingleton.cs
```

### 빌드 파이프라인 동작

1. 빌더는 `framework-cs/upm/{pkg}`를 staging에 복사
2. 최종적으로 `apps/UnityExample/Packages/{pkg}`로 **package-level clean+copy sync**
3. 생성기는 UPM에서 `Runtime/Generated/**`, `Editor/Generated/**`만 clean+generate (Generated Only)

> **Note:** Singleton 폴더는 수기 코드 영역이므로 생성기가 생성/삭제하지 않음

### 파일 규칙

| 파일 | 타입 | 네임스페이스 |
|------|------|-------------|
| `SceneSingleton.cs` | `SceneSingleton<T>` | `Devian` |
| `MonoSingleton.cs` | `MonoSingleton<T>` [Obsolete] | `Devian` |
| `AutoSingleton.cs` | `AutoSingleton<T>` | `Devian` |
| `ResSingleton.cs` | `ResSingleton<T>` | `Devian` |
| `SimpleSingleton.cs` | `SimpleSingleton<T>` | `Devian` |

### 공용 헬퍼 (Pool과 공유)

- `_Shared/UnityMainThread.cs` - 메인 스레드 검증 헬퍼
- 호출 형태: `UnityMainThread.EnsureOrThrow(string context)`
- Singleton은 이 공용 헬퍼를 참조한다

### 중복 인스턴스 Destroy 정본

```csharp
// 정본: 중복 인스턴스 처리 시
UnityEngine.Object.Destroy(gameObject);
```

- `00-unity-object-destruction/SKILL.md` 규약을 따른다
- `delete` 키워드 사용 금지 (C#에 없음)
- 컴포넌트가 아닌 `gameObject`를 Destroy

### 주의사항

- 제공 singleton 타입은 5종이며, 공용 헬퍼는 `_Shared/`에 위치
- **`Singleton/UnityMainThread.cs`는 생성하지 않음** (공용 `_Shared/` 사용)
- `Runtime/Templates/` 레거시 경로가 존재하면 FAIL

---

## 11. Reference

- Parent: `skills/devian-unity/30-unity-components/SKILL.md`
- Related: `skills/devian/03-ssot/SKILL.md` (Foundation Package SSOT)
- Related: `skills/devian-unity/30-unity-components/00-unity-object-destruction/SKILL.md` (Destroy 규약)
