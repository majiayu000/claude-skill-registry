---
name: "Unity Build & CI/CD Configurator"
description: "Configure le pipeline de build Unity, CI/CD, et deployment. Triggers: /build-config, /ci, /deploy, 'configurer build', 'github actions unity', 'gitlab ci unity', 'gitignore unity', 'build automation'. Scanne le projet, genere les scripts de build C#, les workflows CI/CD, et les fichiers Git optimises."
---

# Unity Build & CI/CD Configurator

## Ce que fait cette skill

Configure l'ensemble du pipeline de build Unity : scripts de build C# automatises, workflows CI/CD (GitHub Actions ou GitLab CI), fichiers `.gitignore` et `.gitattributes` optimises avec Git LFS, et checklist pre-release par plateforme. Scanne le projet existant pour adapter la configuration.

## Prerequis

- Un projet Unity existant avec `ProjectSettings/` et `Assets/`
- Un repository Git (ou pret a etre initialise)
- Pour CI/CD : une licence Unity (Personal, Plus, Pro) stockee en secret

## Arbre de decision

```
Que configurer ?
|
+-- Build automatise seulement ?
|   +-- --> Etape 3 (script C# BuildAutomation)
|
+-- CI/CD complet ?
|   +-- GitHub ? --> Etape 4 Option A (GitHub Actions + game-ci)
|   +-- GitLab ? --> Etape 4 Option B (GitLab CI)
|
+-- Git setup (nouveau projet) ?
|   +-- --> Etape 5 (.gitignore + .gitattributes + LFS)
|
+-- Build Profiles (Unity 6+) ?
    +-- --> Section Build Profiles (etape 2)
```

## Demarrage rapide

1. L'utilisateur demande une configuration de build (ex: "configure CI/CD pour Windows et WebGL")
2. Le skill scanne le projet (scenes, packages, settings)
3. Le skill genere les fichiers de configuration adaptes

## Guide etape par etape

### Etape 1 : Identifier les plateformes cibles

Si l'utilisateur ne precise pas, demander les plateformes parmi :
- **Desktop** : StandaloneWindows64, StandaloneOSX, StandaloneLinux64
- **Mobile** : Android, iOS
- **Web** : WebGL
- **Console** : PS5, XboxSeriesX, Switch (necessite SDK proprietaire)

### Etape 2 : Scanner le projet existant

Collecter les informations du projet avec les outils Claude Code :

```
Glob "Assets/**/*.unity"               → lister les scenes
Glob "ProjectSettings/*"               → verifier les settings existants
Read "Packages/manifest.json"          → packages et version Unity
Read "ProjectSettings/ProjectSettings.asset" → scripting backend, company name
Grep "com.unity.render-pipelines"      → pipeline de rendu
Glob ".gitignore"                      → verifier si existant
Glob ".gitattributes"                  → verifier si LFS configure
```

### Build Profiles (Unity 6+)

Unity 6 remplace les Build Settings par des **Build Profiles** (assets `.buildprofile` configurables par plateforme). Permet plusieurs configs independantes, switchables sans reconfigurer manuellement. En CLI, utiliser `-activeBuildProfile` au lieu de `-buildTarget`.

Voir les details et exemples de code dans `references/build-templates.md` section "Build Profiles".

### Etape 3 : Generer le script de build C#

Creer `Assets/Editor/BuildAutomation.cs` avec une classe statique contenant : helper `GetEnabledScenes()`, methode generique `ExecuteBuild()`, et une methode par plateforme cible avec `[MenuItem]`. Inclure un entrypoint `BuildFromCommandLine()` pour le CI.

Voir le template complet dans `references/build-templates.md` section "BuildAutomation.cs".

### Etape 4 : Generer la configuration CI/CD

**Option A : GitHub Actions** (recommande) -- Utilise game-ci avec jobs test (EditMode + PlayMode) puis build en matrice multi-plateforme. Cache du dossier `Library/` et upload des artifacts.

**Option B : GitLab CI** -- Image `unityci/editor`, stages test puis build. Dupliquer le job build par plateforme cible.

Voir les templates YAML complets dans `references/build-templates.md` sections "GitHub Actions" et "GitLab CI".

### Etape 5 : Generer .gitignore et .gitattributes

Generer un `.gitignore` excluant Library/, Temp/, obj/, Builds/, IDE files, et keystores. Generer un `.gitattributes` configurant le YAML merge Unity et Git LFS pour les binaires (3D, textures, audio, video, packages).

Voir les templates complets dans `references/build-templates.md` sections ".gitignore" et ".gitattributes".

### Etape 6 : Pre-build checks

Ajouter une methode `PreBuildCheck()` dans `BuildAutomation.cs` qui valide : scenes presentes dans Build Settings, pas d'erreurs de compilation. Verifier aussi les references manquantes et les tests EditMode.

Voir le code dans `references/build-templates.md` section "Pre-build Checks".

Checklist pre-release par plateforme disponible dans `references/build-templates.md` section "Checklist pre-release".

## Regles strictes

- **TOUJOURS** scanner le projet existant avant de generer des configs
- **TOUJOURS** utiliser IL2CPP pour les builds release (pas Mono)
- **TOUJOURS** configurer Git LFS avant le premier commit d'assets binaires
- **TOUJOURS** mettre les secrets (licence Unity, keystore) dans les variables CI, jamais dans les fichiers
- **TOUJOURS** inclure un job de tests avant le job de build dans le CI
- **JAMAIS** hardcoder de licence Unity ou credentials dans les fichiers CI
- **JAMAIS** inclure `Library/`, `Temp/`, ou `obj/` dans le version control
- **JAMAIS** committer de fichiers `.keystore` (sauf `debug.keystore`)
- **PREFERER** GitHub Actions avec game-ci comme solution CI par defaut
- **PREFERER** le cache du dossier `Library/` pour accelerer les builds CI

## Skills connexes

- Le script BuildAutomation necessite un editor tool plus avance ? Utiliser `/unity-editor-tools` (Unity Editor Tools)
- Generer un script de build custom ? Utiliser `/unity-code-gen` (Unity Code Gen) pour le code C# Editor
- Shader custom a builder ? Utiliser `/shader` (Unity Shader Generator)

## Troubleshooting

| Probleme | Solution |
|----------|----------|
| Build CI echoue "No valid Unity license" | Configurer `UNITY_LICENSE` en secret. Generer via `unity-editor -createManualActivationFile` puis activer sur license.unity3d.com |
| Cache Library/ invalide | Changer la cle de cache ou la supprimer. Le cache depend de la version Unity |
| Build tres lent en CI | Activer le cache Library/, utiliser `il2CppCodeGeneration: OptimizeSize` pour les builds CI non-release |
| Erreur LFS "smudge filter" | Verifier que Git LFS est installe sur le runner CI (`git lfs install`) |
| WebGL build out of memory | Augmenter `PlayerSettings.WebGL.memorySize`, reduire les assets, activer le streaming |
| Android keystore introuvable | Utiliser un path relatif au projet ou une variable d'environnement pour le chemin du keystore |
| iOS signing echoue en CI | Utiliser `fastlane match` ou configurer les certificats via le Keychain du runner macOS |
| Scenes manquantes dans le build | Verifier `EditorBuildSettings.scenes` dans le script ou ajouter les scenes manuellement via le menu Build Settings |
