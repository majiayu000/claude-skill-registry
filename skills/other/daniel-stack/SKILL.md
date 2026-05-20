---
name: daniel-stack
description: Firebase, Photon, Agora, and React/Unity integration patterns for metaverse development. Use when working with backend services, realtime networking, or voice/video.
license: MIT
---

# Stack Reference: Firebase, Photon, Agora

## When to Use

Activate this skill when:

- Working with Firebase (Firestore, Auth, Functions, Storage, Hosting)
- Implementing Photon networking (PUN2 or Fusion)
- Integrating Agora voice/video
- Setting up security rules or custom claims
- Optimizing Cloud Functions (cold starts, concurrency)
- Debugging realtime connectivity issues
- React ↔ Unity ↔ Firebase communication patterns

## Reference Documentation

**Primary Reference:** `docs/stack-reference-firebase-photon-agora.md`

## Quick Reference

### Firebase Auth - Custom Claims

```javascript
// Set claims (Admin SDK in Cloud Function)
await admin.auth().setCustomUserClaims(userId, {
  groups: ['disruptiveAdmin', 'space_123_owners'],
});

// Client: Force refresh to get new claims
await user.getIdToken(true);
const token = await user.getIdTokenResult();
const isAdmin = token.claims.groups?.includes('disruptiveAdmin');
```

### Security Rules Pattern

```javascript
function isDisruptiveAdmin() {
  return (
    request.auth != null &&
    request.auth.token.groups != null &&
    request.auth.token.groups.hasAny(['disruptiveAdmin'])
  );
}

function isSpaceOwner(spaceId) {
  return request.auth.token.groups.hasAny(['space_' + spaceId + '_owners']);
}
```

### Cloud Functions V2 - Optimization

```javascript
const { onCall } = require('firebase-functions/v2/https');

exports.myFunction = onCall(
  {
    minInstances: 1, // Eliminate cold starts
    concurrency: 80, // Handle concurrent requests
    memory: '256MiB',
    region: 'europe-west1',
  },
  async (request) => {
    // ...
  }
);
```

### Firestore Queries

```javascript
// Pagination with cursors
const first = db.collection('spaces').orderBy('createdAt').limit(25);

const next = db.collection('spaces').orderBy('createdAt').startAfter(lastDoc).limit(25);
```

### Photon PUN2 - Connection

```csharp
public class NetworkManager : MonoBehaviourPunCallbacks
{
    void Start() => PhotonNetwork.ConnectUsingSettings();

    public override void OnConnectedToMaster()
        => PhotonNetwork.JoinRandomRoom();

    public override void OnJoinRandomFailed(short code, string msg)
        => PhotonNetwork.CreateRoom(null, new RoomOptions { MaxPlayers = 10 });

    public override void OnJoinedRoom()
        => PhotonNetwork.Instantiate("Player", Vector3.zero, Quaternion.identity);
}
```

### Photon RPCs

```csharp
[PunRPC]
public void ReceiveMessage(string sender, string msg)
{
    chatUI.AddMessage($"{sender}: {msg}");
}

public void Send(string msg)
{
    photonView.RPC("ReceiveMessage", RpcTarget.All,
                   PhotonNetwork.LocalPlayer.NickName, msg);
}
```

### Agora React Hooks

```tsx
import { useJoin, useLocalMicrophoneTrack, usePublish, useRemoteUsers } from 'agora-rtc-react';

function VoiceChat({ channelName, token }) {
  useJoin({ appid: APP_ID, channel: channelName, token });

  const { localMicrophoneTrack } = useLocalMicrophoneTrack();
  usePublish([localMicrophoneTrack]);

  const remoteUsers = useRemoteUsers();
  // ...
}
```

### Agora Token Server (Cloud Function)

```javascript
const { RtcTokenBuilder, RtcRole } = require('agora-access-token');

exports.getAgoraToken = onCall(async (request) => {
  const token = RtcTokenBuilder.buildTokenWithUid(
    APP_ID,
    APP_CERTIFICATE,
    request.data.channelName,
    0,
    RtcRole.PUBLISHER,
    Math.floor(Date.now() / 1000) + 3600
  );
  return { token };
});
```

### Unity ↔ React ↔ Firebase Pattern

**React handles Firebase, Unity communicates via bridge:**

```javascript
// React
const handleRequestData = async (id) => {
  const doc = await getDoc(doc(db, 'spaces', id));
  sendMessage('GameController', 'ReceiveData', JSON.stringify(doc.data()));
};
addEventListener('RequestData', handleRequestData);
```

```csharp
// Unity
[DllImport("__Internal")]
private static extern void RequestData(string id);

public void ReceiveData(string json) {
    var data = JsonUtility.FromJson<SpaceData>(json);
}
```

## Key Limitations

| Service            | Limitation                  | Workaround               |
| ------------------ | --------------------------- | ------------------------ |
| Firebase Unity SDK | No WebGL support            | Use React bridge         |
| Photon WebGL       | TCP only (higher latency)   | Use Fusion Shared Auth   |
| Agora WebGL        | Community SDK (beta)        | Test thoroughly          |
| Custom Claims      | 1000 bytes max              | Keep claims minimal      |
| Custom Claims      | Propagates on token refresh | Force `getIdToken(true)` |
| Firestore offline  | IndexedDB disconnects       | SDK 7.2.1+ improved      |

## Emulator Commands

```bash
# Start all emulators
firebase emulators:start

# Start with seed data
firebase emulators:start --import=./seed-data

# Export data
firebase emulators:export ./seed-data
```

## Deployment Commands

```bash
firebase deploy --only hosting
firebase deploy --only functions
firebase deploy --only firestore:rules
firebase deploy --only storage
```

## Project-Specific Collections

```
/users/{userId}           # User profiles
  /private/{docId}        # Sensitive data
/spaces/{spaceId}         # Virtual spaces
  /objects/{objectId}
  /chatMessages/{msgId}
  /portals/{portalId}
  /mediaScreens/{id}
/groups/{groupId}
/brands/{brandId}
/events/{eventId}
/webglBuilds/{buildId}
```

## Common Issues

| Issue                   | Solution                 |
| ----------------------- | ------------------------ |
| Claims not updating     | `user.getIdToken(true)`  |
| Cold start latency      | Set `minInstances: 1`    |
| CORS on Storage         | Configure with gsutil    |
| Photon region mismatch  | Use Fixed Region         |
| No audio WebGL          | Require user click first |
| Security rules blocking | Test with emulator       |

## Related Skills

- `daniel-unity` - Unity WebGL/WebGPU reference
- `frontend-development` - React/TypeScript patterns
- `backend-development` - Server patterns
