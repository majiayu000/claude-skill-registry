---
name: react-unity-hooks
description: React-Unity WebGL event hooks patterns. Use when working with Unity messaging or creating new event hooks.
license: MIT
---

# React-Unity Event Hooks

## When to Use

Activate when:

- Creating new Unity event hooks
- Debugging React↔Unity communication
- Adding new Unity interactions
- Fixing event timing issues

## Architecture

```
React → Unity:  sendMessage() → ReactIncomingEvent.HandleEvent(name, data)
Unity → React:  SendToReact() → window.dispatchReactUnityEvent(name, data)
```

## Hook Location

`packages/webgl/src/hooks/unityEvents/`

## Core Hooks

### Send to Unity

```javascript
// useSendUnityEvent.js - Base pattern
import { useUnityContext } from 'react-unity-webgl';

export const useSendUnityEvent = () => {
  const { sendMessage, isLoaded } = useUnityContext();

  const sendEvent = useCallback(
    (eventName, data) => {
      if (!isLoaded || !window.isPlayerInstantiated) {
        console.warn('Unity not ready');
        return;
      }

      // ReactIncomingEvent is the Unity C# class
      sendMessage(
        'ReactIncomingEvent',
        'HandleEvent',
        JSON.stringify({
          eventName,
          data: JSON.stringify(data), // Double-encode for Unity parsing
        })
      );
    },
    [sendMessage, isLoaded]
  );

  return { sendEvent };
};
```

### Listen from Unity

```javascript
// useListenForUnityEvent.js - Base pattern
import { useUnityContext } from 'react-unity-webgl';

export const useListenForUnityEvent = (eventName, callback) => {
  const { addEventListener, removeEventListener } = useUnityContext();

  useEffect(() => {
    const handler = (data) => {
      try {
        const parsed = typeof data === 'string' ? JSON.parse(data) : data;
        callback(parsed);
      } catch (e) {
        callback(data); // Raw string fallback
      }
    };

    addEventListener(eventName, handler);
    return () => removeEventListener(eventName, handler);
  }, [eventName, callback, addEventListener, removeEventListener]);
};
```

## Hook Categories

| Category    | Hooks                                                        | Pattern                              |
| ----------- | ------------------------------------------------------------ | ------------------------------------ |
| Send        | `usePlacePrefab`, `usePlacePortal`                           | `useSendUnityEvent`                  |
| Lifecycle   | `useUnityOnFirstSceneLoaded`, `useUnityOnPlayerInstantiated` | `useListenForUnityEvent`             |
| Interaction | `useUnityOnPortalClick`, `useUnityOnNameplateClick`          | `useListenForUnityEvent`             |
| Media       | `useUnityOnPlayVideo`, `useMediaScreenVideoPlayer`           | `useListenForUnityEvent` + Firestore |
| Data Fetch  | `useSpaceObjects`, `useSpacePortals`                         | Firestore + send to Unity            |

## Creating New Hooks

### Send-to-Unity Hook

```javascript
// hooks/unityEvents/usePlaceNewObject.js
import { useCallback } from 'react';
import { useSendUnityEvent } from './useSendUnityEvent';

export const usePlaceNewObject = () => {
  const { sendEvent } = useSendUnityEvent();

  const placeObject = useCallback(
    (objectData) => {
      sendEvent('PlaceNewObject', {
        id: objectData.id,
        position: objectData.position,
        rotation: objectData.rotation,
        // ... other fields
      });
    },
    [sendEvent]
  );

  return { placeObject };
};
```

### Listen-from-Unity Hook

```javascript
// hooks/unityEvents/useUnityOnObjectClick.js
import { useCallback } from 'react';
import { useListenForUnityEvent } from './useListenForUnityEvent';

export const useUnityOnObjectClick = (onObjectClick) => {
  const handleClick = useCallback(
    (data) => {
      // data comes from Unity: { objectId: string, clickPosition: Vector3 }
      if (onObjectClick) {
        onObjectClick(data);
      }
    },
    [onObjectClick]
  );

  useListenForUnityEvent('ObjectClicked', handleClick);
};
```

## Known Issues

| Issue                     | Location                                    | Severity |
| ------------------------- | ------------------------------------------- | -------- |
| Event name trailing space | `useUnityOnRequestForMedia`                 | HIGH     |
| `alert()` in production   | `useUnityOnRequestForMedia`                 | HIGH     |
| Double JSON encoding      | All send patterns                           | MEDIUM   |
| Magic number delays       | `useHLSStream`, `useMediaScreenVideoPlayer` | MEDIUM   |

## Best Practices

### DO

```javascript
// Check Unity readiness
if (!isLoaded || !window.isPlayerInstantiated) return;

// Use constants for event names
const EVENTS = {
  PLACE_OBJECT: 'PlaceObject',
  OBJECT_CLICKED: 'ObjectClicked',
};

// Clean up listeners
useEffect(() => {
  return () => removeEventListener(eventName, handler);
}, []);
```

### DON'T

```javascript
// No trailing spaces in event names
sendEvent('MyEvent '); // BAD - will never match

// No alert() in hooks
alert('Debug message'); // BAD - use Logger

// No hardcoded delays without constants
setTimeout(fn, 500); // BAD - use named constant
```

## Unity C# Side

```csharp
// ReactIncomingEvent.cs
public class ReactIncomingEvent : MonoBehaviour
{
    public void HandleEvent(string jsonData)
    {
        var wrapper = JsonUtility.FromJson<EventWrapper>(jsonData);
        var data = JsonUtility.FromJson<T>(wrapper.data);
        // Process event...
    }
}

// SendToReact via JSLib
[DllImport("__Internal")]
private static extern void SendToReact(string eventName, string data);
```

## Related Skills

- `daniel-unity` - Unity WebGL build patterns
- `frontend-development` - React hook patterns
