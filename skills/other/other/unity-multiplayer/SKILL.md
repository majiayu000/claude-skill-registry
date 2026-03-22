---
name: "Unity Multiplayer"
description: "Developpement multijoueur avec Netcode for GameObjects. Setup reseau, NetworkBehaviour, synchronisation d'etat, RPCs, lobby et relay. Triggers: /netcode, /multiplayer, 'NetworkBehaviour', 'NetworkVariable', 'ServerRpc', 'ClientRpc', 'lobby', 'multijoueur', 'Netcode for GameObjects', 'mode host', 'dedicated server'."
---

# Unity Multiplayer — Netcode for GameObjects (NGO)

## Ce que fait cette skill

Guider le developpement multijoueur avec **Netcode for GameObjects** (NGO).
Couvre le setup reseau, la creation de NetworkBehaviours, la synchronisation
d'etat via NetworkVariables, la communication par RPCs (ServerRpc / ClientRpc),
et l'integration Unity Gaming Services (Lobby + Relay).

Scope: NGO uniquement. Pas DOTS Netcode, pas Mirror, pas Photon.

## Prerequis

- Package `com.unity.netcode.gameobjects` (>= 1.5.0)
- Un GameObject `NetworkManager` dans la scene
- Unity Transport (`com.unity.transport`) comme couche transport
- (Optionnel) Compte Unity Gaming Services pour Lobby / Relay

## Demarrage rapide

1. **Installer le package** — Window > Package Manager > `Netcode for GameObjects`
2. **Ajouter NetworkManager** — GameObject vide avec composant `NetworkManager`
3. **Configurer le transport** — Ajouter `UnityTransport` sur le meme GameObject, l'assigner dans NetworkManager
4. **Creer le player prefab** — Prefab avec `NetworkObject` + votre `NetworkBehaviour`
5. **Assigner le prefab** dans NetworkManager > Player Prefab
6. **Tester en mode host** — `NetworkManager.Singleton.StartHost()`

## Arbre de decision

```
Architecture reseau...
+-- Prototype / local coop ?
|   +-- -> Host mode (client + server sur meme machine)
+-- Jeu en ligne casual (2-8 joueurs) ?
|   +-- -> Host mode + Unity Relay (pas besoin de serveur dedie)
+-- Jeu competitif / anti-cheat important ?
|   +-- -> Dedicated server (autoritative)
+-- Besoin de matchmaking ?
    +-- -> Unity Lobby + Relay
```

## Packages complementaires (Unity 6+)

### Multiplayer Center (`Window > Multiplayer Center`)

Point d'entree recommande par Unity pour configurer un projet multiplayer :
- Recommande les packages a installer selon le type de jeu (casual, competitif, MMO)
- Configure automatiquement le `NetworkManager` et le transport
- Propose des templates de projet multiplayer pre-configures
- Guide vers les bons Gaming Services (Lobby, Relay, Matchmaker)

Utiliser le Multiplayer Center au lieu de configurer manuellement quand on demarre un projet from scratch.

### Dedicated Server package (`com.unity.dedicated-server`)

Pour les jeux avec serveur dedie (pas host mode) :
- **Multiplayer Roles** : marquer du contenu comme `Client`, `Server`, ou `ClientAndServer` dans Build Profiles
- **Content Selection** : le build pipeline strip automatiquement les assets non pertinents pour le role (textures, audio, UI pour le serveur)
- **Impact** : builds serveur 50-80% plus legers
- **Setup** : Installer le package → configurer les roles dans Build Profiles → assigner les roles aux composants/GameObjects

Pertinent uniquement pour les jeux qui shippent un binaire serveur separe. Pas necessaire en mode host.

## Guide etape par etape

### Step 1 — Setup NetworkManager

```csharp
// Demarrer une session:
NetworkManager.Singleton.StartHost();   // host mode
NetworkManager.Singleton.StartServer(); // dedicated
NetworkManager.Singleton.StartClient(); // client
```

### Step 2 — Creer un NetworkBehaviour

```csharp
using Unity.Netcode;
using UnityEngine;

public class PlayerController : NetworkBehaviour
{
    [SerializeField] private float speed = 5f;

    // NetworkVariable — synchronise automatiquement server -> clients
    private NetworkVariable<int> score = new(0,
        NetworkVariableReadPermission.Everyone,
        NetworkVariableWritePermission.Server);

    public override void OnNetworkSpawn()
    {
        if (IsOwner)
        {
            // Setup specifique au joueur local
        }
        score.OnValueChanged += OnScoreChanged;
    }

    public override void OnNetworkDespawn()
    {
        score.OnValueChanged -= OnScoreChanged;
    }

    private void Update()
    {
        if (!IsOwner) return; // Seul le owner controle son personnage

        var input = new Vector3(Input.GetAxis("Horizontal"), 0, Input.GetAxis("Vertical"));
        transform.position += input * (speed * Time.deltaTime);
    }

    // Server RPC — appele par le client, execute sur le server
    [ServerRpc]
    public void AddScoreServerRpc(int points)
    {
        score.Value += points;
    }

    private void OnScoreChanged(int oldValue, int newValue)
    {
        Debug.Log($"Score: {oldValue} -> {newValue}");
    }
}
```

### Step 3 — Setup Lobby + Relay (optionnel, pour jeu en ligne)

Code complet Lobby + Relay dans `references/netcode-patterns.md`.

Workflow :
1. `UnityServices.InitializeAsync()` + `SignInAnonymouslyAsync()`
2. Host : `RelayService.Instance.CreateAllocationAsync()` → get join code → `StartHost()`
3. Client : `RelayService.Instance.JoinAllocationAsync(joinCode)` → `StartClient()`

## Regles strictes

**TOUJOURS:**
- Verifier `IsOwner` avant de traiter l'input joueur
- Verifier `IsServer` avant de modifier l'etat autoritatif
- Utiliser `NetworkVariable` pour l'etat synchronise (pas de champs classiques)
- Suffixer les RPCs : methodes en `ServerRpc` et `ClientRpc`
- Implementer `OnNetworkSpawn` / `OnNetworkDespawn` (pas Start/OnDestroy pour la logique reseau)
- Desabonner les callbacks `OnValueChanged` dans `OnNetworkDespawn`

**JAMAIS:**
- D'`Instantiate` direct en multi — utiliser `NetworkObject.Spawn()` (server only)
- De logique client qui modifie l'etat server directement
- De `NetworkVariable<string>` ou types reference sans custom serialization
- De `Update()` couteux sur des objets non-owner sans raison

**PREFERER:**
- `NetworkVariable` pour l'etat continu (position, health, score)
- `ServerRpc` pour les actions ponctuelles (tirer, acheter, interagir)
- `ClientRpc` pour les feedbacks visuels/audio (explosions, sons)

## Skills connexes

- `/unity-code-gen` — generer des NetworkBehaviour types
- `/unity-build-config` — configuration de build pour dedicated server
- `/unity-test` — tester avec plusieurs instances en parallele
- Bug reseau difficile a tracer ? Utiliser `/unity-debug` (Unity Debug)

## Troubleshooting

| Probleme | Solution |
|----------|----------|
| "NetworkObject is not spawned" | Verifier que le prefab a un composant NetworkObject et est spawne via NetworkManager |
| ServerRpc pas appele | Verifier le suffixe `ServerRpc` dans le nom de methode et que l'appelant est le owner (ou `RequireOwnership = false`) |
| Desync d'etat | Utiliser NetworkVariable au lieu de variables locales. Verifier les read/write permissions |
| Latence visible | Implementer client-side prediction (voir references/netcode-advanced.md) |
| "Object already spawned" | Ne pas appeler Spawn() sur un objet deja spawne. Verifier le flow de spawn |
| Client ne se connecte pas | Verifier l'adresse/port dans UnityTransport. En Relay, verifier le join code |
| NetworkVariable pas mise a jour | Seul le server (ou owner selon WritePermission) peut ecrire. Verifier les permissions |
