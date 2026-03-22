---
name: "Unity Save System"
description: "Implementer un systeme de sauvegarde et persistence : /unity-save, /save, sauvegarde, save system, persistence, sauvegarder, charger une partie, save game, PlayerPrefs, serialisation, JSON save, cloud save, slot de sauvegarde"
---

# Unity Save System

## Ce que fait cette skill

Guider l'implementation d'un systeme de sauvegarde complet pour Unity 6+ : serialisation de l'etat de jeu, persistence fichier avec ecriture atomique, versioning des donnees sauvegardees, gestion multi-slots, auto-save, cloud saves (UGS), et encryption optionnelle. Couvre du simple PlayerPrefs jusqu'aux architectures hybrides local/cloud.

## Prerequis

- Unity 6.0+ (Awaitable API)
- **Recommande** : Newtonsoft.Json (`com.unity.nuget.newtonsoft-json`) pour serialisation avancee
- Aucune dependance stricte pour les cas simples (JsonUtility suffit)

## Demarrage rapide

1. **Choisir le format** : JsonUtility (simple) ou Newtonsoft.Json (polymorphisme, Dictionary)
2. **Creer l'interface** `ISaveable` sur chaque composant a sauvegarder
3. **Implementer** `SaveManager` avec ecriture atomique dans `Application.persistentDataPath`
4. **Brancher** l'auto-save (dirty flag + timer + `OnApplicationPause`)
5. **Tester** le cycle save/load avec un test EditMode (voir `/unity-test`)

## Arbre de decision

```
Que sauvegarder ?
|
+-- Preferences utilisateur (volume, langue, bindings) ?
|   +-- Peu de donnees (<1 KB) --> PlayerPrefs
|   +-- Plus structure ----------> JSON dans persistentDataPath
|
+-- Etat de jeu (progression, inventaire, position) ?
|   +-- Slot unique -----------> JSON + ISaveable pattern
|   +-- Multi-slots -----------> SaveManager avec index + slots nommes
|   +-- Donnees volumineuses (>10 MB) --> Format binaire (MemoryPack/MessagePack)
|
+-- Cloud sync ?
|   +-- Unity Gaming Services --> UGS Cloud Save
|   +-- Cross-platform natif --> Platform Toolkit (Unity 6.3+)
|   +-- Hybride (local + cloud) -> ISaveStorage abstraction (voir `references/save-advanced.md`)
|
+-- Sensible (anti-cheat) ?
    +-- Encryption AES + hash d'integrite (voir `references/save-advanced.md`)
```

## Guide etape par etape

### Etape 1 — Choisir le format de serialisation

| Critere | JsonUtility | Newtonsoft.Json | MemoryPack | MessagePack |
|---------|------------|-----------------|------------|-------------|
| Setup | Inclus Unity | Package Unity | NuGet | NuGet |
| Polymorphisme | Non | Oui (`TypeNameHandling`) | Oui | Oui |
| Dictionary | Non | Oui | Oui | Oui |
| Lisibilite | JSON | JSON | Binaire | Binaire |
| Performance | Rapide | Moyen | Tres rapide | Rapide |
| Taille | Moyen | Moyen | Petit | Petit |
| Recommandation | Prototypage | **Defaut recommande** | >10 MB donnees | Alternative binaire |

### Etape 2 — Creer ISaveable et SaveData

- Definir `ISaveable` : `SaveKey`, `CaptureState()`, `RestoreState(object)`
- Creer `SaveData` avec champ `version`, `Dictionary<string, object>`, metadata
- Voir `references/save-templates.md` pour le code complet (ISaveable, SaveData, SaveManager)

### Etape 3 — Implementer SaveManager

- Pattern singleton ou service locator (voir `/unity` architecture)
- Registry de `ISaveable` (Register/Unregister)
- `SaveAsync` : capturer tous les etats -> serialiser -> ecriture atomique (.tmp -> .save, .bak)
- `LoadAsync` : lire fichier -> deserialiser -> restaurer tous les etats
- Chemin : `Path.Combine(Application.persistentDataPath, "saves", slotName + ".save")`

### Etape 4 — Auto-save

- Dirty flag : chaque `ISaveable` signale ses changements
- Timer configurable (60-120s par defaut)
- Sauvegarder sur `OnApplicationPause(true)` et changement de scene
- Voir `references/save-advanced.md` section Auto-Save

### Etape 5 — Tester le cycle save/load

- Test EditMode : save -> clear state -> load -> assert state restored
- Test corruption : charger un fichier tronque -> verifier fallback .bak
- Test migration : charger une save v1 avec du code v2

## Regles strictes

### TOUJOURS

- **TOUJOURS** utiliser l'ecriture atomique (write .tmp, rename, keep .bak)
- **TOUJOURS** versionner les `SaveData` (champ `version` incremente a chaque changement de schema)
- **TOUJOURS** utiliser `Application.persistentDataPath` (jamais `dataPath` ou `streamingAssetsPath`)
- **TOUJOURS** sauvegarder sur `OnApplicationPause(true)` pour mobile
- **TOUJOURS** serialiser des POCOs (Plain Old C# Objects) — pas de types Unity
- **TOUJOURS** gerer le cas "pas de sauvegarde" (premier lancement)

### JAMAIS

- **JAMAIS** utiliser `BinaryFormatter` — faille de securite connue, deprecie
- **JAMAIS** stocker de references `MonoBehaviour`, `GameObject`, ou `ScriptableObject` dans les saves
- **JAMAIS** sauvegarder sur le thread principal de facon synchrone pour des fichiers >100 KB
- **JAMAIS** supprimer l'ancien fichier avant que le nouveau soit ecrit (corruption garantie en cas de crash)
- **JAMAIS** ignorer les exceptions d'I/O — toujours try/catch avec fallback

## Skills connexes

- `/unity-code-gen` — Generer le boilerplate ISaveable et SaveManager
- `/unity-test` — Tests EditMode pour valider le cycle save/load
- `/unity-debug` — Diagnostiquer les problemes de deserialisation
- `/addressables` — Sauvegarder les references d'assets par address string

## Troubleshooting

| Probleme | Cause probable | Solution |
|----------|---------------|----------|
| `FileNotFoundException` au load | Premier lancement, aucune save | Verifier `File.Exists()` avant load, retourner donnees par defaut |
| Donnees perdues apres mise a jour | Schema change sans migration | Ajouter champ `version` + chaine de migration v1->v2->vN |
| `JsonSerializationException` | Type polymorphe non reconnu | Newtonsoft : `TypeNameHandling.Auto` + `SerializationBinder` custom |
| Save corrompue (JSON tronque) | Crash pendant ecriture | Ecriture atomique (.tmp -> rename) + fallback sur .bak |
| `UnauthorizedAccessException` | Chemin non autorise (Android scope) | Utiliser uniquement `persistentDataPath` |
| PlayerPrefs disparaissent (iOS) | Nettoyage systeme ou reinstallation | Migrer vers fichier pour donnees importantes |
| Save trop volumineuse (>50 MB) | Serialisation JSON de gros volumes | Passer a MemoryPack/MessagePack, compresser (GZip) |
| Desync cloud/local | Conflit de versions | Implementer conflict resolution (timestamp ou version counter) |
