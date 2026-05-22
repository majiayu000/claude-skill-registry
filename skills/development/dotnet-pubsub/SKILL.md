---
name: dotnet-pubsub
description: '.NET Pub-Sub 패턴 (System.Reactive, Channels)'
---

# .NET Pub-Sub 패턴

이벤트 기반 비동기 통신을 위한 Pub-Sub 패턴 가이드입니다.

## 1. 핵심 API

| API | 용도 | NuGet |
|-----|------|-------|
| `System.Reactive` (Rx.NET) | 반응형 이벤트 스트림 | System.Reactive |
| `System.Threading.Channels` | 비동기 Producer-Consumer | BCL |
| `IObservable<T>` | 관찰 가능한 시퀀스 | BCL |

---

## 2. System.Threading.Channels

### 2.1 기본 사용법

```csharp
using System.Threading.Channels;

public sealed class MessageProcessor
{
    private readonly Channel<Message> _channel =
        Channel.CreateUnbounded<Message>();

    // Producer - 메시지 전송
    public async Task SendAsync(Message message)
    {
        await _channel.Writer.WriteAsync(message);
    }

    // Consumer - 메시지 처리
    public async Task ProcessAsync(CancellationToken ct)
    {
        await foreach (var message in _channel.Reader.ReadAllAsync(ct))
        {
            await HandleMessage(message);
        }
    }

    // 채널 완료 신호
    public void Complete() => _channel.Writer.Complete();
}
```

### 2.2 Bounded Channel (배압 제어)

```csharp
// 버퍼 크기 제한으로 배압 제어
var options = new BoundedChannelOptions(capacity: 100)
{
    FullMode = BoundedChannelFullMode.Wait, // 가득 차면 대기
    SingleReader = true,
    SingleWriter = false
};

var channel = Channel.CreateBounded<Message>(options);

// Writer는 공간이 생길 때까지 대기
await channel.Writer.WriteAsync(message);
```

### 2.3 다중 Consumer 패턴

```csharp
public sealed class WorkerPool
{
    private readonly Channel<WorkItem> _channel;
    private readonly int _workerCount;

    public WorkerPool(int workerCount = 4)
    {
        _workerCount = workerCount;
        _channel = Channel.CreateUnbounded<WorkItem>();
    }

    public async Task StartAsync(CancellationToken ct)
    {
        var workers = Enumerable.Range(0, _workerCount)
            .Select(_ => ProcessAsync(ct));

        await Task.WhenAll(workers);
    }

    private async Task ProcessAsync(CancellationToken ct)
    {
        await foreach (var item in _channel.Reader.ReadAllAsync(ct))
        {
            await ProcessItem(item);
        }
    }

    public ValueTask EnqueueAsync(WorkItem item) =>
        _channel.Writer.WriteAsync(item);
}
```

---

## 3. System.Reactive (Rx.NET)

### 3.1 EventAggregator 패턴

```csharp
using System.Reactive.Linq;
using System.Reactive.Subjects;

public sealed class EventAggregator : IDisposable
{
    private readonly Subject<object> _subject = new();

    // 특정 타입 이벤트 구독
    public IObservable<T> GetEvent<T>() =>
        _subject.OfType<T>().AsObservable();

    // 이벤트 발행
    public void Publish<T>(T @event) =>
        _subject.OnNext(@event!);

    public void Dispose() => _subject.Dispose();
}
```

### 3.2 사용 예시

```csharp
// 이벤트 정의
public record UserLoggedIn(string UserId);
public record OrderPlaced(int OrderId);

// 구독
var aggregator = new EventAggregator();

aggregator.GetEvent<UserLoggedIn>()
    .Subscribe(e => Console.WriteLine($"User logged in: {e.UserId}"));

aggregator.GetEvent<OrderPlaced>()
    .Where(e => e.OrderId > 100)
    .Subscribe(e => Console.WriteLine($"Large order: {e.OrderId}"));

// 발행
aggregator.Publish(new UserLoggedIn("user123"));
aggregator.Publish(new OrderPlaced(150));
```

### 3.3 Rx 연산자

```csharp
// 디바운스 - 연속 이벤트 중 마지막만 처리
searchInput
    .Throttle(TimeSpan.FromMilliseconds(300))
    .DistinctUntilChanged()
    .Subscribe(query => Search(query));

// 버퍼 - 일정 기간 이벤트 모아서 처리
events
    .Buffer(TimeSpan.FromSeconds(5))
    .Subscribe(batch => ProcessBatch(batch));

// 재시도 - 실패 시 재시도
observable
    .Retry(3)
    .Subscribe(
        onNext: data => Process(data),
        onError: ex => LogError(ex)
    );
```

---

## 4. 비교: Channels vs Rx

| 특성 | Channels | Rx.NET |
|------|----------|--------|
| 용도 | Producer-Consumer | 이벤트 스트림 |
| 배압 제어 | 내장 (Bounded) | 별도 구현 |
| 연산자 | 기본적 | 풍부함 |
| 학습 곡선 | 낮음 | 높음 |
| 의존성 | BCL | NuGet |

---

## 5. DI 통합

```csharp
// Program.cs
services.AddSingleton(Channel.CreateUnbounded<Message>());
services.AddSingleton(sp => sp.GetRequiredService<Channel<Message>>().Reader);
services.AddSingleton(sp => sp.GetRequiredService<Channel<Message>>().Writer);

// Producer
public sealed class Producer(ChannelWriter<Message> writer)
{
    public ValueTask SendAsync(Message msg) => writer.WriteAsync(msg);
}

// Consumer
public sealed class Consumer(ChannelReader<Message> reader)
{
    public async Task ProcessAsync(CancellationToken ct)
    {
        await foreach (var msg in reader.ReadAllAsync(ct))
        {
            await Handle(msg);
        }
    }
}
```

---

## 6. 필수 NuGet 패키지

```xml
<ItemGroup>
  <PackageReference Include="System.Reactive" Version="6.0.*" />
</ItemGroup>
```

---

## 7. 주의사항

### ⚠️ 메모리 누수

```csharp
// 구독 해제 필수
var subscription = observable.Subscribe(handler);

// 사용 완료 후
subscription.Dispose();
```

### ⚠️ 스레드 안전성

- Channels는 기본적으로 스레드 안전
- Subject는 스레드 안전하지 않음 (필요시 Synchronize() 사용)

### ⚠️ 배압 처리

```csharp
// Bounded Channel로 메모리 폭발 방지
var channel = Channel.CreateBounded<Message>(new BoundedChannelOptions(1000)
{
    FullMode = BoundedChannelFullMode.DropOldest // 오래된 메시지 버림
});
```

---

## 8. 참고 문서

- [Channels](https://learn.microsoft.com/en-us/dotnet/core/extensions/channels)
- [System.Reactive](https://github.com/dotnet/reactive)

