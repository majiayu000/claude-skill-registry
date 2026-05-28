---
name: wpf-drawingcontext-rendering
description: 'WPF DrawingContext를 사용한 고성능 렌더링 패턴 (Shape 대비 10-50배 성능 향상)'
---

# WPF DrawingContext 고성능 렌더링

WPF에서 대량의 도형을 렌더링할 때 DrawingContext를 사용하여 Shape 객체 대비 10-50배 성능 향상을 달성하는 패턴입니다.

## 1. 핵심 개념

### Shape 방식 vs DrawingContext 방식

| 항목 | Shape (Polygon, Rectangle 등) | DrawingContext |
|------|------------------------------|----------------|
| **상속 클래스** | Canvas | FrameworkElement |
| **Visual 개수** | 도형 수만큼 생성 (n개) | 1개 |
| **레이아웃 계산** | O(n) Measure/Arrange | O(1) |
| **메모리 사용** | 매우 많음 (WPF 객체 오버헤드) | 매우 적음 (데이터만) |
| **성능** | 기준점 | **10-50배 빠름** |
| **적합한 경우** | 소수의 인터랙티브 도형 (수십~수백 개) | 대량의 정적 도형 (수천~수만 개) |

### 왜 DrawingContext가 빠른가?

1. **단일 Visual**: FrameworkElement 1개만 Visual Tree에 등록
2. **레이아웃 생략**: Measure/Arrange 계산 전혀 불필요
3. **배치 렌더링**: GPU에 단일 배치로 전달
4. **메모리 효율**: 도형 메타데이터만 저장

---

## 2. 기본 구현 패턴

### 2.1 DrawingContext 기반 커스텀 컨트롤

```csharp
namespace MyApp.Controls;

using System.Windows;
using System.Windows.Media;

public sealed class HighPerformanceCanvas : FrameworkElement
{
    // 1. 도형 데이터를 저장하는 구조체 (가벼움)
    // 1. Struct for storing shape data (lightweight)
    private readonly record struct ShapeData(
        Point Position,
        double Width,
        double Height,
        Brush Fill);

    // 2. 렌더링 데이터만 메모리에 저장
    // 2. Only rendering data stored in memory
    private readonly List<ShapeData> _shapes = [];

    // 3. 최적화된 Pen (Freeze 적용)
    // 3. Optimized Pen (Freeze applied)
    private readonly Pen _pen = new(Brushes.Black, 1);

    public HighPerformanceCanvas()
    {
        // Pen을 Freeze하여 성능 최적화
        // Freeze Pen for performance optimization
        _pen.Freeze();
    }

    // 4. 도형 추가 메서드
    // 4. Shape addition method
    public void AddShape(Point position, double width, double height, Color color)
    {
        var brush = new SolidColorBrush(color);
        brush.Freeze();  // Freeze로 성능 최적화
                         // Freeze for performance optimization

        _shapes.Add(new ShapeData(position, width, height, brush));
    }

    // 5. 렌더링 트리거 (데이터 추가 완료 후 한 번만 호출)
    // 5. Trigger rendering (call once after data addition is complete)
    public void Render()
    {
        InvalidateVisual();
    }

    // 6. 실제 렌더링 - OnRender에서 직접 그리기
    // 6. Actual rendering - direct drawing in OnRender
    protected override void OnRender(DrawingContext dc)
    {
        base.OnRender(dc);

        foreach (var shape in _shapes)
        {
            dc.DrawRectangle(
                shape.Fill,
                _pen,
                new Rect(shape.Position, new Size(shape.Width, shape.Height)));
        }
    }

    // 7. 도형 초기화
    // 7. Clear shapes
    public void Clear()
    {
        _shapes.Clear();
        InvalidateVisual();
    }
}
```

---

## 3. 복잡한 도형 (StreamGeometry 사용)

삼각형, 다각형 등 복잡한 도형은 StreamGeometry를 사용합니다.

### 3.1 삼각형 렌더링 예제

```csharp
namespace MyApp.Controls;

using System.Windows;
using System.Windows.Media;

public sealed class TriangleCanvas : FrameworkElement
{
    private readonly record struct TriangleData(
        Point Point1, Point Point2, Point Point3, Brush Fill);

    private readonly List<TriangleData> _triangles = [];
    private readonly Pen _pen = new(Brushes.Black, 1);

    public TriangleCanvas()
    {
        _pen.Freeze();
    }

    public void AddTriangle(Point p1, Point p2, Point p3, Color color)
    {
        var brush = new SolidColorBrush(color);
        brush.Freeze();

        _triangles.Add(new TriangleData(p1, p2, p3, brush));
    }

    public void Render()
    {
        InvalidateVisual();
    }

    protected override void OnRender(DrawingContext dc)
    {
        base.OnRender(dc);

        foreach (var triangle in _triangles)
        {
            // StreamGeometry를 사용한 경량 기하학 생성
            // Create lightweight geometry using StreamGeometry
            var geometry = new StreamGeometry();

            using (var ctx = geometry.Open())
            {
                ctx.BeginFigure(triangle.Point1, isFilled: true, isClosed: true);
                ctx.LineTo(triangle.Point2, isStroked: true, isSmoothJoin: false);
                ctx.LineTo(triangle.Point3, isStroked: true, isSmoothJoin: false);
            }

            geometry.Freeze();  // 불변 처리로 최적화
                                // Optimize by making immutable

            dc.DrawGeometry(triangle.Fill, _pen, geometry);
        }
    }

    public void Clear()
    {
        _triangles.Clear();
        InvalidateVisual();
    }
}
```

---

## 4. 성능 측정이 포함된 패턴

### 4.1 비동기 렌더링 + 성능 측정

```csharp
namespace MyApp.Controls;

using System.Diagnostics;
using System.Windows;
using System.Windows.Media;
using System.Windows.Threading;

public sealed class BenchmarkCanvas : FrameworkElement
{
    private readonly record struct RectData(Rect Bounds, Brush Fill);

    private readonly List<RectData> _items = [];
    private readonly Pen _pen = new(Brushes.Black, 1);

    public BenchmarkCanvas()
    {
        _pen.Freeze();
    }

    /// <summary>
    /// 대량의 도형을 렌더링하고 소요 시간을 반환합니다.
    /// Renders a large number of shapes and returns the elapsed time.
    /// </summary>
    public async Task<TimeSpan> DrawItemsAsync(int count)
    {
        _items.Clear();

        double width = ActualWidth > 0 ? ActualWidth : 400;
        double height = ActualHeight > 0 ? ActualHeight : 400;

        var random = new Random();

        // 1단계: 데이터만 생성 (측정 전)
        // Step 1: Generate data only (before measurement)
        for (int i = 0; i < count; i++)
        {
            double x = random.NextDouble() * (width - 20);
            double y = random.NextDouble() * (height - 20);
            double size = 10 + random.NextDouble() * 20;

            var brush = new SolidColorBrush(Color.FromRgb(
                (byte)random.Next(256),
                (byte)random.Next(256),
                (byte)random.Next(256)));
            brush.Freeze();

            _items.Add(new RectData(new Rect(x, y, size, size), brush));

            // UI Hang 방지를 위해 주기적으로 양보
            // Yield periodically to prevent UI hang
            if (i % 100 == 0)
            {
                await Dispatcher.InvokeAsync(() => { }, DispatcherPriority.Background);
            }
        }

        // 2단계: 렌더링만 측정 (한 번만 호출)
        // Step 2: Measure rendering only (call once)
        var stopwatch = Stopwatch.StartNew();
        InvalidateVisual();
        await Dispatcher.InvokeAsync(() => { }, DispatcherPriority.Render);
        stopwatch.Stop();

        return stopwatch.Elapsed;
    }

    protected override void OnRender(DrawingContext dc)
    {
        base.OnRender(dc);

        foreach (var item in _items)
        {
            dc.DrawRectangle(item.Fill, _pen, item.Bounds);
        }
    }

    public void Clear()
    {
        _items.Clear();
        InvalidateVisual();
    }
}
```

---

## 5. 핵심 최적화 기법

### 5.1 Freeze() - 불변 객체화

```csharp
// ✅ Pen 최적화
private readonly Pen _pen = new(Brushes.Black, 1);
public MyControl()
{
    _pen.Freeze();  // WPF가 내부 최적화 가능
}

// ✅ Brush 최적화
var brush = new SolidColorBrush(Color.FromRgb(255, 0, 0));
brush.Freeze();  // 메모리에서 공유 가능

// ✅ Geometry 최적화
var geometry = new StreamGeometry();
// ... geometry 구성 ...
geometry.Freeze();  // 렌더링 파이프라인 최적화
```

### 5.2 record struct 사용

```csharp
// ✅ 값 타입 (stack allocation) → 메모리 효율적
private readonly record struct ShapeData(
    Point Position,
    Size Size,
    Brush Fill);

// 자동 Equals, GetHashCode 생성
// 불변 의미론 강화
```

### 5.3 StreamGeometry vs PathGeometry

```csharp
// ✅ StreamGeometry - 경량, 쓰기 전용
var geometry = new StreamGeometry();
using (var ctx = geometry.Open())
{
    ctx.BeginFigure(startPoint, true, true);
    ctx.LineTo(point2, true, false);
}

// ❌ PathGeometry - 상대적으로 무거움
var geometry = new PathGeometry();
var figure = new PathFigure { StartPoint = startPoint };
figure.Segments.Add(new LineSegment(point2, true));
```

---

## 6. InvalidateVisual() 호출 시 주의사항

### ⚠️ O(n²) 복잡도 발생 패턴

```csharp
// ❌ 나쁜 예: 루프 내 InvalidateVisual() 호출
for (int i = 0; i < count; i++)
{
    _items.Add(data);
    if (i % 10 == 0)
    {
        InvalidateVisual();  // OnRender가 전체 _items를 순회!
    }
}
// 결과: 10개 + 20개 + ... + n개 = O(n²)
// Result: 10 + 20 + ... + n = O(n²)
```

### ✅ 올바른 패턴: 마지막에 한 번만

```csharp
// ✅ 좋은 예: 데이터 수집 후 한 번만 렌더링
for (int i = 0; i < count; i++)
{
    _items.Add(data);
}

// 마지막에 한 번만 렌더링
// Render only once at the end
InvalidateVisual();
```

**성능 차이**:
- 나쁜 패턴: 10,000개 데이터 시 **수초**
- 올바른 패턴: 10,000개 데이터 시 **수십ms**

---

## 7. MVVM 패턴과 통합

### 7.1 ViewModel - 델리게이트 패턴

ViewModel이 View 타입을 직접 참조하지 않으면서도 렌더링 메서드를 호출하는 패턴:

```csharp
namespace MyApp.ViewModels;

using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;

public sealed partial class RenderViewModel : ObservableObject
{
    // View 타입 참조 없이 델리게이트만 저장
    // Store only delegates without View type reference
    private Func<int, Task<TimeSpan>>? _drawItems;
    private Action? _clearCanvas;

    [ObservableProperty]
    private bool _isRendering;

    [ObservableProperty]
    private string _elapsedTime = "대기 중... / Waiting...";

    // View에서 필요한 메서드 주입
    // Inject required methods from View
    public void SetRenderActions(
        Func<int, Task<TimeSpan>> drawItems,
        Action clearCanvas)
    {
        _drawItems = drawItems;
        _clearCanvas = clearCanvas;
    }

    [RelayCommand]
    private async Task RenderAsync()
    {
        if (_drawItems is null)
        {
            return;
        }

        IsRendering = true;
        _clearCanvas?.Invoke();

        var elapsed = await _drawItems(10000);
        ElapsedTime = $"{elapsed.TotalMilliseconds:F2} ms";

        IsRendering = false;
    }
}
```

### 7.2 View - 델리게이트 연결

```csharp
namespace MyApp.Views;

using System.Windows;
using MyApp.ViewModels;

public partial class MainWindow : Window
{
    public MainWindow()
    {
        InitializeComponent();

        Loaded += (_, _) =>
        {
            if (DataContext is RenderViewModel vm)
            {
                vm.SetRenderActions(
                    MyCanvas.DrawItemsAsync,
                    MyCanvas.Clear);
            }
        };
    }
}
```

---

## 8. Shape 방식과의 비교 (참고용)

Shape 방식이 필요한 경우도 있습니다:

```csharp
// Shape 방식 - 인터랙션이 필요한 소수의 도형에 적합
// Shape approach - suitable for few shapes requiring interaction
public sealed class ShapeBasedPanel : Canvas
{
    public void AddInteractiveShape()
    {
        var polygon = new Polygon
        {
            Points = [new Point(0, 0), new Point(50, 0), new Point(25, 50)],
            Fill = Brushes.Blue,
            Stroke = Brushes.Black,
            StrokeThickness = 1
        };

        // 개별 도형에 이벤트 연결 가능
        // Can attach events to individual shapes
        polygon.MouseEnter += (s, e) => polygon.Fill = Brushes.Red;
        polygon.MouseLeave += (s, e) => polygon.Fill = Brushes.Blue;

        Children.Add(polygon);
    }
}
```

**Shape 방식 선택 기준**:
- 도형 수가 수십~수백 개 이하
- 개별 도형에 마우스 이벤트가 필요한 경우
- 드래그 앤 드롭 기능이 필요한 경우

---

## 9. 성능 비교 결과 예시

**10,000개 삼각형 기준**:

| 방식 | 예상 시간 | 비고 |
|------|----------|------|
| Shape (Polygon) | 500-2000ms | Visual Tree 오버헤드 |
| DrawingContext | 20-50ms | 직접 그리기 |
| **성능 비율** | **10-50배** | 환경에 따라 변동 |

---

## 10. 체크리스트

- [ ] FrameworkElement 상속 (Canvas 대신)
- [ ] Pen, Brush에 Freeze() 적용
- [ ] 도형 데이터는 record struct로 저장
- [ ] 복잡한 도형은 StreamGeometry 사용
- [ ] InvalidateVisual()은 데이터 추가 완료 후 **한 번만** 호출
- [ ] 대량 데이터 생성 시 Dispatcher.InvokeAsync로 UI 양보
- [ ] ViewModel은 View 타입 참조 없이 델리게이트 패턴 사용

---

## 11. 참고 문서

- [DrawingContext - Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/api/system.windows.media.drawingcontext)
- [StreamGeometry - Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/api/system.windows.media.streamgeometry)
- [Optimizing WPF Performance - Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/optimizing-performance-2d-graphics-and-imaging)
