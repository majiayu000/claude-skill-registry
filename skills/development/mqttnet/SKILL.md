---
name: mqttnet
description: |
  Manages MQTT broker connections and message publishing/subscription using MQTTnet 4.3.x.
  Use when: implementing MQTT-based device communication, creating IoT plugins, handling pub/sub messaging patterns
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# MQTTnet Skill

MQTTnet is used in VanDaemon for MQTT-based device communication, specifically for the ESP32 LED dimmer integration. The codebase uses MQTTnet 4.3.x with a managed client pattern running as a background service.

## Quick Start

### Basic Managed Client Setup

```csharp
// From MqttLedDimmerPlugin pattern
private readonly IMqttClient _mqttClient;
private MqttClientOptions _options = null!;

public async Task InitializeAsync(Dictionary<string, object> configuration, CancellationToken ct = default)
{
    var factory = new MqttFactory();
    _mqttClient = factory.CreateMqttClient();
    
    _options = new MqttClientOptionsBuilder()
        .WithTcpServer(configuration["MqttBroker"]?.ToString() ?? "localhost", 
                       Convert.ToInt32(configuration["MqttPort"] ?? 1883))
        .WithClientId($"vandaemon-{Guid.NewGuid():N}")
        .WithCleanSession(true)
        .Build();
    
    _mqttClient.ApplicationMessageReceivedAsync += HandleMessageAsync;
    await _mqttClient.ConnectAsync(_options, ct);
}
```

### Subscribe to Topics

```csharp
await _mqttClient.SubscribeAsync(new MqttTopicFilterBuilder()
    .WithTopic("vandaemon/leddimmer/+/status")
    .WithQualityOfServiceLevel(MqttQualityOfServiceLevel.AtLeastOnce)
    .Build(), cancellationToken);
```

### Publish Messages

```csharp
var message = new MqttApplicationMessageBuilder()
    .WithTopic($"vandaemon/leddimmer/{deviceId}/channel/{channel}/set")
    .WithPayload(brightness.ToString())
    .WithQualityOfServiceLevel(MqttQualityOfServiceLevel.AtLeastOnce)
    .WithRetainFlag(false)
    .Build();

await _mqttClient.PublishAsync(message, cancellationToken);
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| MqttFactory | Create client instances | `new MqttFactory().CreateMqttClient()` |
| MqttClientOptions | Connection configuration | `new MqttClientOptionsBuilder().WithTcpServer()` |
| Topic wildcards | `+` single level, `#` multi-level | `device/+/status`, `device/#` |
| QoS levels | 0=fire-forget, 1=at-least-once, 2=exactly-once | Use QoS 1 for state changes |
| Retain flag | Broker stores last message | Use for device status |

## Common Patterns

### Background Service Integration

**When:** Running MQTT client as a hosted service

```csharp
public class MqttLedDimmerService : BackgroundService
{
    private readonly MqttLedDimmerPlugin _plugin;
    
    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        await _plugin.InitializeAsync(_config, stoppingToken);
        
        while (!stoppingToken.IsCancellationRequested)
        {
            await _plugin.DiscoverDevicesAsync(stoppingToken);
            await Task.Delay(TimeSpan.FromSeconds(10), stoppingToken);
        }
    }
}
```

### Message Handler Pattern

**When:** Processing incoming MQTT messages

```csharp
private Task HandleMessageAsync(MqttApplicationMessageReceivedEventArgs e)
{
    var topic = e.ApplicationMessage.Topic;
    var payload = Encoding.UTF8.GetString(e.ApplicationMessage.PayloadSegment);
    
    // Parse topic: vandaemon/leddimmer/{deviceId}/channel/{N}/state
    var segments = topic.Split('/');
    if (segments.Length >= 5 && segments[3] == "channel")
    {
        var deviceId = segments[2];
        var channel = int.Parse(segments[4]);
        ProcessChannelState(deviceId, channel, payload);
    }
    
    return Task.CompletedTask;
}
```

## See Also

- [patterns](references/patterns.md) - Connection management, topic design, error handling
- [workflows](references/workflows.md) - Device discovery, state synchronization

## Related Skills

- See the **csharp** skill for async patterns and error handling
- See the **aspnet-core** skill for background service registration
- See the **serilog** skill for structured MQTT logging