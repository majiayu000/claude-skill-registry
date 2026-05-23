---
name: unity-networking
description: Implement multiplayer games with Unity Netcode, Mirror, or Photon. Masters client-server architecture, state synchronization, and lag compensation. Use for multiplayer features, networking issues, or real-time synchronization.
requires:
  - csharp-plugin:csharp-code-style
---

# Unity Networking - Multiplayer Game Development

## Overview

Multiplayer networking for Unity using Netcode for GameObjects, Mirror, or Photon frameworks.

**Foundation Required**: `unity-csharp-fundamentals` (TryGetComponent, FindAnyObjectByType, null-safe coding)

**Core Topics**:
- Client-server architecture
- State synchronization
- Lag compensation
- RPC (Remote Procedure Calls)
- Network variables
- Matchmaking

## Quick Start (Unity Netcode)

```csharp
using Unity.Netcode;

public class Player : NetworkBehaviour
{
    private NetworkVariable<int> mHealth = new(100);

    public override void OnNetworkSpawn()
    {
        if (IsOwner)
        {
            // Only owner can control
            HandleInput();
        }

        mHealth.OnValueChanged += OnHealthChanged;
    }

    [ServerRpc]
    void TakeDamageServerRpc(int damage)
    {
        mHealth.Value -= damage;
    }

    [ClientRpc]
    void ShowDamageEffectClientRpc()
    {
        // Visual feedback on all clients
    }
}
```

## Network Architecture

- **Authoritative Server**: Server validates all actions (competitive)
- **Client Authority**: Clients control own entities (cooperative)
- **Relay Servers**: NAT traversal for peer-to-peer
- **Dedicated Servers**: Professional hosting

## Synchronization Patterns

- **Transform Sync**: Position, rotation interpolation
- **Network Variables**: Automatic state replication
- **RPCs**: Remote method calls
- **Ownership**: Who can modify what

## Best Practices

1. **Server authority**: Prevent cheating
2. **Client prediction**: Smooth movement
3. **Interpolation**: Handle lag gracefully
4. **Bandwidth optimization**: Delta compression
5. **Test with network simulation**: Latency, packet loss
