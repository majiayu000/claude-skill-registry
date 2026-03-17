---
name: unity3d
description: |
  USE FOR: Building 2D and 3D games, simulations, AR/VR experiences, and interactive applications using the Unity game engine with C# scripting. Use when you need a visual editor, asset store, and cross-platform deployment to PC, consoles, mobile, and web.
  DO NOT USE FOR: Business applications, web APIs, or CRUD apps (use ASP.NET Core or Blazor), command-line tools, or projects that require fully open-source tooling (Unity is proprietary).
license: MIT
metadata:
  displayName: Unity3D
  author: "Tyler-R-Kendrick"
  version: "1.0.0"
compatibility:
  - claude
  - copilot
  - cursor
references:
  - title: "Unity Documentation"
    url: "https://docs.unity3d.com/Manual/index.html"
  - title: "Unity Official Site"
    url: "https://unity.com/"
  - title: "Unity Scripting API Reference"
    url: "https://docs.unity3d.com/ScriptReference/index.html"
---

# Unity3D

## Overview

Unity is a cross-platform game engine and development environment that uses C# as its primary scripting language. It supports 2D and 3D game development, AR/VR, simulation, and interactive media. Unity provides a visual editor, scene hierarchy, inspector, animation system, physics engine, and an asset store. Games and applications built with Unity can be deployed to Windows, macOS, Linux, iOS, Android, WebGL, PlayStation, Xbox, Nintendo Switch, and more. Unity scripts are C# classes that inherit from `MonoBehaviour` and use lifecycle methods (`Awake`, `Start`, `Update`, `FixedUpdate`, `OnDestroy`) to define behavior.

## MonoBehaviour Lifecycle and Player Controller

The `MonoBehaviour` class provides lifecycle hooks. Use `Update` for frame-dependent logic and `FixedUpdate` for physics.

```csharp
using UnityEngine;

namespace MyGame
{
    [RequireComponent(typeof(Rigidbody))]
    [RequireComponent(typeof(CapsuleCollider))]
    public class PlayerController : MonoBehaviour
    {
        [Header("Movement")]
        [SerializeField] private float moveSpeed = 6f;
        [SerializeField] private float jumpForce = 8f;
        [SerializeField] private float groundCheckDistance = 0.3f;

        [Header("Camera")]
        [SerializeField] private Transform cameraTransform;
        [SerializeField] private float mouseSensitivity = 2f;

        private Rigidbody _rb;
        private bool _isGrounded;
        private float _verticalRotation;

        private void Awake()
        {
            _rb = GetComponent<Rigidbody>();
            _rb.freezeRotation = true;
            Cursor.lockState = CursorLockMode.Locked;
        }

        private void Update()
        {
            HandleMouseLook();
            CheckGrounded();

            if (_isGrounded && Input.GetButtonDown("Jump"))
            {
                _rb.AddForce(Vector3.up * jumpForce, ForceMode.Impulse);
            }
        }

        private void FixedUpdate()
        {
            float horizontal = Input.GetAxisRaw("Horizontal");
            float vertical = Input.GetAxisRaw("Vertical");

            Vector3 direction = transform.forward * vertical + transform.right * horizontal;
            direction = direction.normalized * moveSpeed;
            direction.y = _rb.linearVelocity.y;

            _rb.linearVelocity = direction;
        }

        private void HandleMouseLook()
        {
            float mouseX = Input.GetAxis("Mouse X") * mouseSensitivity;
            float mouseY = Input.GetAxis("Mouse Y") * mouseSensitivity;

            _verticalRotation -= mouseY;
            _verticalRotation = Mathf.Clamp(_verticalRotation, -90f, 90f);

            cameraTransform.localRotation = Quaternion.Euler(_verticalRotation, 0f, 0f);
            transform.Rotate(Vector3.up * mouseX);
        }

        private void CheckGrounded()
        {
            _isGrounded = Physics.Raycast(
                transform.position, Vector3.down, groundCheckDistance);
        }
    }
}
```

## Scriptable Objects for Data

Use `ScriptableObject` to define data assets that can be edited in the Unity Inspector and shared across objects.

```csharp
using UnityEngine;

namespace MyGame.Data
{
    [CreateAssetMenu(fileName = "NewWeapon", menuName = "Game/Weapon Data")]
    public class WeaponData : ScriptableObject
    {
        [Header("Weapon Info")]
        public string weaponName;
        public Sprite icon;
        public GameObject prefab;

        [Header("Stats")]
        [Range(1, 100)] public int damage = 10;
        [Range(0.1f, 5f)] public float fireRate = 0.5f;
        [Range(1, 100)] public int maxAmmo = 30;
        [Range(5f, 200f)] public float range = 50f;

        [Header("Effects")]
        public AudioClip fireSound;
        public ParticleSystem muzzleFlash;
    }

    public class WeaponSystem : MonoBehaviour
    {
        [SerializeField] private WeaponData currentWeapon;
        private int _currentAmmo;
        private float _nextFireTime;

        private void Start()
        {
            _currentAmmo = currentWeapon.maxAmmo;
        }

        public void Fire()
        {
            if (Time.time < _nextFireTime || _currentAmmo <= 0) return;

            _nextFireTime = Time.time + currentWeapon.fireRate;
            _currentAmmo--;

            if (Physics.Raycast(transform.position, transform.forward,
                out RaycastHit hit, currentWeapon.range))
            {
                if (hit.collider.TryGetComponent<IDamageable>(out var target))
                {
                    target.TakeDamage(currentWeapon.damage);
                }
            }

            if (currentWeapon.fireSound != null)
                AudioSource.PlayClipAtPoint(currentWeapon.fireSound, transform.position);
        }

        public void Reload()
        {
            _currentAmmo = currentWeapon.maxAmmo;
        }
    }

    public interface IDamageable
    {
        void TakeDamage(int amount);
    }
}
```

## Object Pooling

Avoid runtime `Instantiate`/`Destroy` overhead with an object pool for frequently spawned objects.

```csharp
using System.Collections.Generic;
using UnityEngine;

namespace MyGame.Systems
{
    public class ObjectPool : MonoBehaviour
    {
        [SerializeField] private GameObject prefab;
        [SerializeField] private int initialSize = 20;
        [SerializeField] private Transform poolParent;

        private readonly Queue<GameObject> _available = new();

        private void Awake()
        {
            for (int i = 0; i < initialSize; i++)
            {
                var obj = Instantiate(prefab, poolParent);
                obj.SetActive(false);
                _available.Enqueue(obj);
            }
        }

        public GameObject Get(Vector3 position, Quaternion rotation)
        {
            GameObject obj;
            if (_available.Count > 0)
            {
                obj = _available.Dequeue();
            }
            else
            {
                obj = Instantiate(prefab, poolParent);
            }

            obj.transform.SetPositionAndRotation(position, rotation);
            obj.SetActive(true);
            return obj;
        }

        public void Return(GameObject obj)
        {
            obj.SetActive(false);
            _available.Enqueue(obj);
        }
    }
}
```

## Coroutines and Async Patterns

Unity supports both coroutines (via `IEnumerator`) and modern async/await patterns for asynchronous operations.

```csharp
using System.Collections;
using System.Threading;
using System.Threading.Tasks;
using UnityEngine;
using UnityEngine.Networking;

namespace MyGame.Networking
{
    public class DataLoader : MonoBehaviour
    {
        private CancellationTokenSource _cts;

        private void OnEnable()
        {
            _cts = new CancellationTokenSource();
        }

        private void OnDisable()
        {
            _cts?.Cancel();
            _cts?.Dispose();
        }

        // Coroutine approach
        public IEnumerator LoadTextureCoroutine(string url, System.Action<Texture2D> callback)
        {
            using var request = UnityWebRequestTexture.GetTexture(url);
            yield return request.SendWebRequest();

            if (request.result == UnityWebRequest.Result.Success)
            {
                var texture = DownloadHandlerTexture.GetContent(request);
                callback?.Invoke(texture);
            }
            else
            {
                Debug.LogError($"Failed to load texture: {request.error}");
            }
        }

        // Async/await approach
        public async Task<string> LoadJsonAsync(string url)
        {
            using var request = UnityWebRequest.Get(url);
            var operation = request.SendWebRequest();

            while (!operation.isDone)
            {
                _cts.Token.ThrowIfCancellationRequested();
                await Task.Yield();
            }

            if (request.result != UnityWebRequest.Result.Success)
                throw new System.Exception($"Request failed: {request.error}");

            return request.downloadHandler.text;
        }
    }
}
```

## Unity vs Other Game Engines

| Feature | Unity | Unreal Engine | Godot | MonoGame |
|---|---|---|---|---|
| Language | C# | C++ / Blueprints | GDScript / C# | C# |
| Editor | Full visual editor | Full visual editor | Full visual editor | None (code-only) |
| 2D support | Good | Limited | Excellent | Excellent |
| 3D support | Good | Excellent (AAA) | Good | Manual |
| Asset store | Largest ecosystem | Marketplace | Asset Library | None |
| Platform reach | 20+ platforms | 15+ platforms | 10+ platforms | 8+ platforms |
| Pricing | Free (revenue caps) | Free (5% royalty > $1M) | Free (MIT) | Free (MIT) |

## Best Practices

1. **Use `[SerializeField] private` instead of `public` fields for Inspector-exposed values** so that other scripts cannot directly modify the field, maintaining encapsulation; public fields bypass property setters, making it impossible to validate or react to changes at assignment time.

2. **Cache `GetComponent<T>()` results in `Awake()` and store them in private fields** rather than calling `GetComponent` every frame in `Update()`; each `GetComponent` call performs a runtime type lookup on the GameObject's component list, and calling it 60+ times per second across hundreds of objects creates measurable CPU overhead.

3. **Use `FixedUpdate()` for all physics-related code** (Rigidbody forces, raycasts for physics queries, collision checks) because `FixedUpdate` runs at a deterministic timestep synchronized with the physics engine; physics code in `Update()` produces frame-rate-dependent behavior that varies across devices.

4. **Implement object pooling for frequently instantiated/destroyed objects** (bullets, particles, UI popups) using a `Queue<GameObject>` pattern, because `Instantiate()` and `Destroy()` allocate and deallocate managed and native memory, triggering GC spikes that cause visible frame stutters on mobile.

5. **Use `ScriptableObject` assets for shared game data** (weapon stats, enemy configurations, dialog trees) instead of hardcoding values in MonoBehaviour fields or static variables, because ScriptableObjects are editable in the Inspector, shareable across prefabs, and do not require scene references.

6. **Cancel `CancellationTokenSource` in `OnDisable()` or `OnDestroy()` for all async operations** to prevent `MissingReferenceException` when a coroutine or Task completes after the GameObject has been destroyed; this is especially critical for scene transitions where objects are destroyed mid-operation.

7. **Use `[RequireComponent(typeof(T))]` attribute on MonoBehaviours that depend on specific components** (e.g., `Rigidbody`, `Collider`, `AudioSource`) so Unity automatically adds the required component when the script is attached and prevents accidental removal in the Inspector.

8. **Avoid string-based APIs like `GameObject.Find("PlayerObject")` and `SendMessage("TakeDamage")`** because they perform runtime string comparisons, bypass compile-time type checking, and silently fail if the name changes; use direct references via `[SerializeField]`, events, or interfaces instead.

9. **Separate game logic from MonoBehaviour by writing plain C# classes for state machines, AI, and calculations**, then composing them into MonoBehaviours; this enables unit testing with NUnit/xUnit without requiring a running Unity Editor or Play Mode test runner.

10. **Profile with the Unity Profiler (`Window > Analysis > Profiler`) before optimizing** and focus on the top three CPU or GPU bottlenecks per frame; premature optimization of code that consumes 0.1ms per frame wastes development time when the actual bottleneck is a 12ms shader or an unoptimized mesh.
