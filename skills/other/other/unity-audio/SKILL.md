---
name: "Unity Audio"
description: "Systeme audio complet Unity 6+ : SFX, musique, ambiance, spatialisation 3D, AudioMixer, pooling, Audio Random Container, Scriptable Audio Pipeline. Triggers: /unity-audio, /audio, audio, son, musique, AudioMixer, AudioSource, spatial audio, 3D sound, sound design, SFX"
---

# Unity Audio

## Ce que fait cette skill

Guide la conception et l'implementation d'un systeme audio complet dans Unity 6+. Couvre les SFX avec pooling, la musique avec crossfade, l'ambiance sonore, la spatialisation 3D, les Audio Random Containers (Unity 6+), les AudioMixer snapshots, et introduit le Scriptable Audio Pipeline (Unity 6.3+). Produit du code performant base sur des ScriptableObjects et le pattern event-driven.

## Prerequis

- Unity 6.0+ (6.3+ pour Scriptable Audio Pipeline)
- Package Audio par defaut (integre)
- Connaissance basique des AudioSource, AudioClip, AudioMixer
- Skill `/unity` chargee (architecture, patterns SO)

## Demarrage rapide

1. **Decrire le besoin** : type de son (SFX, musique, ambiance), contexte (2D/3D/VR)
2. **Suivre l'arbre de decision** pour choisir le pattern adapte
3. **Creer l'AudioManager** base sur ScriptableObject + pool de SoundEmitters
4. **Configurer les import settings** selon le type audio (voir `references/audio-optimization.md`)
5. **Tester** avec le Profiler Audio et ajuster les volumes via AudioMixer

## Arbre de decision

```
Type de son ?
|
+-- SFX ponctuel (tir, saut, UI click) ?
|   +-- Peu de variations --> AudioSource.PlayOneShot + pool
|   +-- Variations (footsteps, impacts) --> Audio Random Container (Unity 6+)
|
+-- Musique (BGM, themes) ?
|   +-- Un seul theme --> AudioSource loop
|   +-- Transitions entre themes --> Crossfade 2 sources
|   +-- Musique dynamique --> AudioMixer snapshots
|
+-- Ambiance (vent, foule, pluie) ?
|   +-- Globale --> AudioSource loop sur Camera/Manager
|   +-- Locale (zone) --> AudioSource 3D + trigger zone
|
+-- Son spatial 3D ?
|   +-- Standard --> spatialBlend = 1, Logarithmic rolloff
|   +-- VR/AR --> Spatializer plugin (Steam Audio, Resonance)
|
+-- Custom DSP / synthese ?
    +-- Unity 6.3+ --> Scriptable Audio Pipeline
```

## Guide etape par etape

### Etape 1 : Detecter l'AudioMixer existant

Verifier si un AudioMixer existe dans le projet. Sinon, en creer un avec les groupes :
- **Master** (volume global)
  - **SFX** (effets sonores)
  - **Music** (musique)
  - **Ambiance** (sons d'ambiance)
  - **UI** (sons d'interface)

Exposer les parametres de volume de chaque groupe (`SFXVolume`, `MusicVolume`, etc.).

### Etape 2 : Setup AudioManager SO

Creer le systeme base sur ScriptableObjects :
- `AudioCueSO` : contient les clips, plages de volume/pitch, groupe mixer cible
- `AudioCueEventChannelSO` : canal d'evenement pour decoupler les demandes de lecture
- `AudioManager` MonoBehaviour : ecoute le canal, gere le pool de SoundEmitters

Voir `references/audio-patterns.md` pour l'implementation complete (AudioCueSO, SoundEmitter, pool, crossfade).

### Etape 3 : Configurer les import settings

Pour chaque clip audio, appliquer les settings optimaux selon son type :
- **SFX courts** : Decompress On Load, Vorbis 70%, Force Mono
- **Musique** : Streaming, Vorbis 50%, Stereo
- **Ambiance** : Streaming, Vorbis 50%, Force Mono
- **UI** : Decompress On Load, PCM, Force Mono

Voir `references/audio-optimization.md` pour le tableau complet.

### Etape 4 : Implementer les patterns

Selon l'arbre de decision :
- **SFX** : pool de SoundEmitters avec auto-return
- **Musique** : crossfade entre 2 AudioSources via `Awaitable`
- **Ambiance** : AudioSource 3D avec trigger zones
- **Spatialisation** : configurer rolloff, min/max distance, doppler
- **AudioMixer Snapshots** : transitions d'ambiance (Combat, Pause, Underwater)

Voir `references/audio-advanced.md` pour les patterns Mixer snapshots, spatial 3D et Audio Random Container.

### Etape 5 : Tester et profiler

- Ouvrir **Window > Analysis > Audio Profiler**
- Verifier le nombre de voix actives (budget : 32 mobile, 64 desktop)
- Verifier la memoire audio dans le Profiler (onglet Memory > Audio)
- Tester les transitions de snapshots AudioMixer
- Valider la spatialisation 3D en scene avec Gizmos audio

## Regles strictes

**TOUJOURS :**
- Utiliser `PlayOneShot()` pour les SFX ponctuels (pas `Play()`)
- Passer par un pool de SoundEmitters (jamais `Instantiate` par son)
- Exposer les volumes via `AudioMixer.SetFloat()` (pas via `AudioSource.volume` direct)
- Configurer les import settings AVANT d'utiliser un clip en jeu
- Utiliser `AudioMixerGroup` sur chaque AudioSource pour le routing
- Convertir les volumes en dB : `Mathf.Log10(value) * 20f`
- Limiter les voix simultanees par categorie (max voices)

**JAMAIS :**
- `new AudioClip()` ou charger des clips a chaque frame
- `AudioSource.Play()` pour des SFX rapides et superposes
- Oublier de retourner un emitter au pool apres lecture
- Laisser un AudioSource en `Decompress On Load` pour un fichier > 500 Ko
- Utiliser `Destroy()` sur des GameObjects audio (recycler via pool)
- Ignorer le `spatialBlend` (defaut 0 = 2D, souvent oublie pour le 3D)

## Skills connexes

- `/unity-code-gen` : generer le code AudioManager, SoundEmitter, AudioCueSO
- `/proto` : prototype rapide avec audio placeholder
- `/perf-audit` : detecter les anti-patterns audio (memoire, voix)
- `/unity-test` : tester les systemes audio en EditMode

## Troubleshooting

| Probleme | Cause probable | Solution |
|----------|---------------|----------|
| Son ne joue pas | AudioSource desactivee ou volume a 0 | Verifier `enabled`, `volume`, `AudioMixerGroup` non mute |
| Son 3D inaudible | `spatialBlend = 0` (mode 2D) | Mettre `spatialBlend = 1` et verifier `maxDistance` |
| Clic/pop au debut du clip | Clip mal trimme ou decompression | Trimmer le silence, utiliser fade-in dans le clip |
| Latence SFX sur mobile | `Streaming` sur SFX courts | Passer en `Decompress On Load` pour clips < 1s |
| Memoire audio explose | Tous les clips en `Decompress On Load` | Streaming pour musique/ambiance, compresser |
| Crossfade brutal | Pas de courbe de transition | Utiliser `Mathf.SmoothStep` ou courbe logarithmique |
| AudioMixer.SetFloat echoue | Parametre non expose | Clic droit sur le param dans l'Inspector > Expose |
| Sons identiques repetitifs | Pas de variation pitch/volume | Utiliser Audio Random Container ou randomiser manuellement |
