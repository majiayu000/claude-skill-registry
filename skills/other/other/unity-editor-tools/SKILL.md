---
name: "Unity Editor Tools"
description: "Cree des outils custom pour l'editeur Unity : inspectors personnalises, fenetres d'outils, drawers, menu items, wizards et asset processors. Triggers: /unity-editor-tools, /editor, 'custom inspector', 'editor window', 'property drawer', 'menu item', 'editor tool', 'outil editeur'. Produit des scripts C# dans le dossier Editor avec assembly definition correcte."
---

# Unity Editor Tools

## Ce que fait cette skill

Cette skill genere des outils personnalises pour l'editeur Unity afin d'accelerer les workflows de developpement. Elle couvre tous les types d'extensions editor : CustomEditor, PropertyDrawer, EditorWindow, MenuItem, ScriptableWizard et AssetPostprocessor.

## Prerequis

- Projet Unity avec une structure `Assets/Scripts/` existante
- Connaissance du composant ou du workflow a outiller
- Pas de dependance MCP Unity : utilise uniquement Read, Write, Edit, Grep, Glob, Bash

## Demarrage rapide

1. Identifier le workflow a accelerer dans l'editeur
2. Choisir le type d'outil via l'arbre de decision
3. Verifier la structure assembly Editor
4. Generer le script avec le template adapte
5. Verifier visuellement dans Unity

## Arbre de decision

Quel type d'outil editor creer ?

| Besoin | Type | Classe de base |
|--------|------|----------------|
| Personnaliser l'affichage d'un composant dans l'Inspector | `CustomEditor` | `Editor` |
| Personnaliser le rendu d'un type de champ specifique | `PropertyDrawer` | `PropertyDrawer` |
| Creer une fenetre d'outil autonome | `EditorWindow` | `EditorWindow` |
| Ajouter une action rapide dans un menu | `MenuItem` | attribut statique |
| Creer un assistant etape par etape | `ScriptableWizard` | `ScriptableWizard` |
| Traiter les assets a l'import | `AssetPostprocessor` | `AssetPostprocessor` |

## Guide etape par etape

### Etape 1 : Identifier le workflow a accelerer

Analyser le besoin utilisateur. Scanner les composants existants :

```
Glob : Assets/Scripts/**/*.cs
Grep : "class.*MonoBehaviour" dans les fichiers trouves
```

Questions cles : quel composant editer plus facilement ? Quelle action automatiser ? Quel feedback visuel manque ?

### Etape 2 : Verifier la structure assembly Editor

Avant de generer du code, verifier que l'infrastructure Editor existe :

```
1. Glob : Assets/**/Editor/*.asmdef OR Assets/**/Editor.asmdef
2. Si absent : creer le dossier Assets/Scripts/Editor/
3. Creer Game.Editor.asmdef avec reference a Game.Runtime
4. Verifier que le .asmdef cible uniquement la plateforme Editor
```

Structure du fichier `Game.Editor.asmdef` :

```json
{
    "name": "Game.Editor",
    "rootNamespace": "",
    "references": ["Game.Runtime"],
    "includePlatforms": ["Editor"],
    "excludePlatforms": [],
    "allowUnsafeCode": false,
    "overrideReferences": false
}
```

Si aucun `Game.Runtime.asmdef` n'existe, verifier avec Glob dans `Assets/Scripts/` et en creer un si necessaire.

### Etape 3 : Generer le script editor

Templates disponibles dans `references/editor-templates.md` :

| Template | Base class | Usage |
|----------|------------|-------|
| CustomEditor (IMGUI) | `Editor` | Inspector personnalise, compatible toutes versions |
| CustomEditor (UI Toolkit) | `Editor` | Inspector complexe Unity 6+, binding auto |
| PropertyDrawer | `PropertyDrawer` | Rendu custom d'un type de champ |
| EditorWindow | `EditorWindow` | Fenetre d'outil avec tabs et toolbar |
| MenuItem | Attribut statique | Action rapide dans un menu Unity |

**Pour Unity 6+**, preferer UI Toolkit a IMGUI pour les EditorWindow et CustomEditor complexes. IMGUI reste acceptable pour les PropertyDrawer simples.

### Etape 4 : Verification visuelle

Apres generation du script :

1. Verifier que le fichier est dans le bon dossier (`Assets/Scripts/Editor/` ou `Assets/Editor/`)
2. Verifier l'absence d'erreurs de compilation : chercher les dependances manquantes
3. S'assurer que le `using UnityEditor;` est present
4. Confirmer que le script ne reference aucun type Editor depuis un assembly Runtime

## Regles strictes

- **TOUJOURS** placer les scripts editor dans `Assets/Scripts/Editor/` ou `Assets/Editor/`
- **TOUJOURS** utiliser un assembly definition `Game.Editor` avec `includePlatforms: ["Editor"]`
- **TOUJOURS** utiliser `serializedObject.Update()` et `ApplyModifiedProperties()` dans les CustomEditor
- **TOUJOURS** utiliser `Undo.RecordObject()` avant de modifier un objet via bouton
- **TOUJOURS** utiliser `EditorGUI.BeginProperty/EndProperty` dans les PropertyDrawer
- **JAMAIS** referencer du code Editor depuis un assembly Runtime
- **JAMAIS** utiliser `target` sans cast dans un CustomEditor (utiliser `(T)target` ou `serializedObject`)
- **JAMAIS** oublier le `GUIContent.none` quand on dessine des sous-champs dans un Drawer
- **JAMAIS** creer de fichier editor a la racine de `Assets/Scripts/`

## Skills connexes

- Generer le composant avant de creer son inspector ? Utiliser `/unity-code-gen` (Unity Code Gen)
- Creer une UI runtime (pas editor) ? Utiliser `/uitk` (Unity UI Toolkit)
- Tester les outils editor ? Utiliser `/unity-test` (Unity Test)

## Troubleshooting

| Probleme | Solution |
|----------|----------|
| `The type or namespace 'Editor' could not be found` | Le script n'est pas dans un dossier Editor ou l'assembly def manque `includePlatforms: ["Editor"]` |
| L'inspector custom ne s'affiche pas | Verifier que `typeof(TargetComponent)` correspond exactement au type cible et que le script compile |
| `NullReferenceException` dans `OnEnable` | Le nom de propriete dans `FindProperty()` ne correspond pas au champ `[SerializeField]` (sensible a la casse) |
| Le PropertyDrawer ne s'applique pas | Verifier que l'attribut `[CustomPropertyDrawer(typeof(T))]` cible le bon type, pas le champ |
| `Multiple editors` warning | Deux CustomEditor ciblent le meme type. Grep pour `CustomEditor(typeof(X))` dans tout le projet |
| Le MenuItem est grise | La methode `Validate` retourne `false`. Verifier les conditions de validation |
| Changements non annulables (Ctrl+Z) | Ajouter `Undo.RecordObject()` avant chaque modification directe |
