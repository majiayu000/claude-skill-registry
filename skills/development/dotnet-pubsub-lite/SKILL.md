---
name: dotnet-pubsub-lite
description: 'Pub-Sub 핵심 패턴 (Channels)'
---

# Pub-Sub 핵심

## 1. Channel 기본

```csharp
using System.Threading.Channels;

var channel = Channel.CreateUnbounded<Message>();

// Producer
await channel.Writer.WriteAsync(message);

// Consumer
await foreach (var msg in channel.Reader.ReadAllAsync(ct))
{
    await HandleMessage(msg);
}

// 완료 신호
channel.Writer.Complete();
```

## 2. Bounded Channel

```csharp
// 배압 제어
var channel = Channel.CreateBounded<Message>(new BoundedChannelOptions(100)
{
    FullMode = BoundedChannelFullMode.Wait
});
```

## 3. DI 등록

```csharp
services.AddSingleton(Channel.CreateUnbounded<Message>());
services.AddSingleton(sp => sp.GetRequiredService<Channel<Message>>().Reader);
services.AddSingleton(sp => sp.GetRequiredService<Channel<Message>>().Writer);
```

## 4. Channels vs Rx.NET

| 특성 | Channels | Rx.NET |
|------|----------|--------|
| 용도 | Producer-Consumer | 이벤트 스트림 |
| 배압 | 내장 | 별도 구현 |
| 의존성 | BCL | NuGet |

> 상세 내용: `/dotnet-pubsub` skill 참조
