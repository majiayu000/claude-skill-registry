# Bootstrap Resource Object

## 0. 목적

씬과 무관하게 Devian BootstrapRoot를 DDOL로 보장한다.

---

## 1. 구성

- **DevianBootstrap** (static): BeforeSceneLoad에서 BootstrapRoot prefab 로드/Instantiate + DDOL 보장
- **DevianBootstrapRoot** (MonoBehaviour): BootstrapRoot prefab의 루트 컴포넌트, DevianSettings 참조 보유

---

## 2. Files (SSOT)

- `framework-cs/upm/com.devian.foundation/Runtime/Unity/Bootstrap/DevianBootstrap.cs`
- `framework-cs/upm/com.devian.foundation/Runtime/Unity/Bootstrap/DevianBootstrapRoot.cs`
- `framework-cs/upm/com.devian.foundation/Editor/Settings/DevianSettingsMenu.cs`

---

## 3. 경로 (SSOT)

| 에셋 | 프로젝트 경로 | Resources.Load 경로 |
|------|---------------|---------------------|
| DevianSettings | `Assets/Resources/Devian/DevianSettings.asset` | `Devian/DevianSettings` |
| BootstrapRoot Prefab | `Assets/Resources/Devian/BootstrapRoot.prefab` | `Devian/BootstrapRoot` |

---

## 4. BootstrapRoot 구조

BootstrapRoot는 **registry prefab**이다:
- 여기에 `BootSingleton<T>` 컴포넌트들을 붙여서 자동 등록
- 사용자는 자신의 초기화 MonoBehaviour 스크립트를 붙여서, 원하는 로딩/초기화/등록을 직접 코딩

프레임워크는 "부팅 완료"를 강제/대기하지 않는다. 개발자 코드가 부팅 흐름을 책임진다.

---

## 5. DevianBootstrap

BeforeSceneLoad에서 자동 실행되는 정적 클래스.

```csharp
public static class DevianBootstrap
{
    // BootstrapRoot 존재 보장 + DDOL + Settings 주입
    public static DevianBootstrapRoot Ensure();

    // Settings 캐시 접근
    public static DevianSettings Settings { get; }
}
```

**Ensure() 동작:**
1. 이미 존재하는 DevianBootstrapRoot를 FindAnyObjectByType으로 찾음
2. 없으면 Resources에서 `Devian/BootstrapRoot` prefab 로드 후 Instantiate
3. prefab이 없으면 fallback으로 코드로 생성 (테스트/최소 실행 보장)
4. DontDestroyOnLoad 적용
5. Settings 주입 (없으면 Resources에서 로드)

---

## 6. DevianBootstrapRoot

```csharp
public sealed class DevianBootstrapRoot : MonoBehaviour
{
    [SerializeField] private DevianSettings? _settings;
    public DevianSettings? Settings => _settings;
    public void SetSettings(DevianSettings? settings) { _settings = settings; }
}
```

---

## 7. Editor 메뉴

**메뉴: Devian/Create Bootstrap**

이 메뉴는 다음을 생성/보수한다:
1. DevianSettings (`Assets/Resources/Devian/DevianSettings.asset`)
2. BootstrapRoot Prefab (`Assets/Resources/Devian/BootstrapRoot.prefab`)

**BootstrapRoot Prefab 기본 구성:**
- DevianBootstrapRoot (Settings 참조 연결)
- SceneTransManager

사용자는 BootstrapRoot.prefab에 초기화 스크립트를 추가로 부착해, 원하는 순서/로딩/등록을 직접 코딩할 수 있다.

---

## 8. 테스트 규약

PlayMode 테스트는 SetUp에서 `DevianBootstrap.Ensure()` 호출로 BootstrapRoot 존재를 보장한다.

---

## 9. Reference

- Parent: `skills/devian-unity/30-unity-components/SKILL.md`
- DevianSettings: `skills/devian-unity/30-unity-components/23-devian-settings/SKILL.md`
- SceneTransManager: `skills/devian-unity/30-unity-components/15-scene-trans-manager/SKILL.md`
- Singleton: `skills/devian-unity/30-unity-components/31-singleton/SKILL.md`
