---
name: "Unity UI Toolkit"
description: "Creation d'interfaces utilisateur avec UI Toolkit (UXML, USS, C# bindings). Genere des ecrans complets avec structure UXML, styling USS et presenter C#. Triggers: /uitk, /ui, 'UI Toolkit', 'UXML', 'USS', 'UIDocument', 'data binding UI', 'runtime UI', 'menu principal', 'HUD', 'interface utilisateur Unity'."
---

# Unity UI Toolkit

## Ce que fait cette skill

Creer des interfaces Unity avec UI Toolkit, le systeme UI moderne d'Unity 6+.
Genere la structure UXML (layout), le styling USS (apparence) et le code C#
presenter/controller (logique). Couvre runtime UI (jeu) et Editor UI (outils).
Remplace progressivement UGUI avec une approche web : separation structure/style/logique, flexbox, pseudo-classes CSS.

## Prerequis

- **Unity 6+** (UI Toolkit inclus nativement, runtime-ready)
- **UIDocument** component attache a un GameObject dans la scene
- **PanelSettings** asset (sort order, scale mode, screen match)

## Demarrage rapide

1. Analyser le besoin UI (quel ecran, quelles interactions)
2. Choisir les controls adaptes (voir `references/uitk-controls.md`)
3. Creer le `.uxml` (structure) → `.uss` (style) → C# presenter (logique)
4. Attacher UIDocument + PanelSettings dans la scene

## Arbre de decision

```
Quel type d'UI ?
+-- Runtime UI (jeu) ?
|   +-- HUD simple (health bar, score) → UXML + USS + C# direct query
|   +-- Menu / ecran complet → UXML + USS + C# presenter + navigation stack
|   +-- UI world-space → UIDocument sur GO + PanelSettings world-space
+-- Editor UI ?
|   +-- Custom Inspector → CreateInspectorGUI() + UXML (voir /unity-editor-tools)
|   +-- EditorWindow → CreateGUI() + UXML
+-- Legacy UGUI existant → evaluer migration ou coexistence
```

## Guide etape par etape

### Step 1 : Fichier UXML (structure)

```xml
<ui:UXML xmlns:ui="UnityEngine.UIElements">
    <ui:VisualElement name="root" class="screen">
        <ui:VisualElement name="header" class="header">
            <ui:Label name="title" text="Game Title" class="title-text" />
        </ui:VisualElement>
        <ui:VisualElement name="menu-buttons" class="button-container">
            <ui:Button name="btn-play" text="Play" class="menu-button" />
            <ui:Button name="btn-settings" text="Settings" class="menu-button" />
            <ui:Button name="btn-quit" text="Quit" class="menu-button" />
        </ui:VisualElement>
    </ui:VisualElement>
</ui:UXML>
```

### Step 2 : Fichier USS (style)

```css
.screen {
    flex-grow: 1;
    justify-content: center;
    align-items: center;
    background-color: rgb(20, 20, 30);
}
.title-text {
    font-size: 48px;
    color: rgb(230, 230, 240);
    -unity-font-style: bold;
    -unity-text-align: middle-center;
}
.button-container {
    flex-direction: column;
    align-items: center;
}
.menu-button {
    width: 300px;
    height: 60px;
    margin: 8px;
    font-size: 24px;
    color: rgb(220, 220, 230);
    background-color: rgb(40, 40, 55);
    border-radius: 8px;
    border-width: 0;
    transition: scale 0.15s ease-in-out, background-color 0.15s ease-in-out;
}
.menu-button:hover {
    scale: 1.05;
    background-color: rgb(60, 60, 80);
}
.menu-button:active {
    scale: 0.97;
    background-color: rgb(50, 100, 180);
}
```

### Step 3 : C# presenter (logique)

```csharp
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UIElements;

[RequireComponent(typeof(UIDocument))]
public class MainMenuPresenter : MonoBehaviour
{
    private void Awake()
    {
        var root = GetComponent<UIDocument>().rootVisualElement;
        root.Q<Button>("btn-play").clicked += OnPlay;
        root.Q<Button>("btn-settings").clicked += OnSettings;
        root.Q<Button>("btn-quit").clicked += OnQuit;
    }

    private void OnPlay() => SceneManager.LoadScene("Game");
    private void OnSettings() { /* push settings screen */ }
    private void OnQuit()
    {
#if UNITY_EDITOR
        UnityEditor.EditorApplication.isPlaying = false;
#else
        Application.Quit();
#endif
    }
}
```

### Step 4 : Setup dans la scene

1. Creer un GameObject vide "UI"
2. Ajouter le component `UIDocument`
3. Assigner le `.uxml` dans Source Asset
4. Assigner un `PanelSettings` (Assets > Create > UI Toolkit > Panel Settings Asset)
5. Configurer : Scale Mode = Scale With Screen Size, Reference Resolution
6. Attacher le script presenter sur le meme GameObject
7. Ajuster le Sort Order si plusieurs UIDocuments coexistent

## Regles strictes

- **TOUJOURS** utiliser `Q<T>("name")` pour querier les elements (jamais `Query` sans type)
- **TOUJOURS** utiliser des classes USS pour le styling (pas de styles inline C# sauf dynamique)
- **JAMAIS** de nesting UXML > 5 niveaux (refactoriser en sous-templates)
- **TOUJOURS** flexbox pour le layout (pas de position absolute sauf overlays)
- **TOUJOURS** separer UXML (structure), USS (style), C# (logique) — MVC
- **PREFERER** `[UxmlElement]` / `[UxmlAttribute]` pour custom controls (Unity 6+)
- **TOUJOURS** tester responsive en redimensionnant le Game view
- **JAMAIS** de logique metier dans le presenter — deleguer aux services/managers
- **TOUJOURS** unregister les callbacks dans OnDisable/OnDestroy si necessaire
- **PREFERER** les transitions USS aux animations C# pour effets simples

## Organisation des fichiers

```
Assets/UI/
├── Screens/          MainMenu.uxml/.uss, Settings.uxml/.uss, HUD.uxml/.uss
├── Components/       PlayerCard.uxml/.uss, HealthBar.uxml
├── Themes/           Variables.uss, DarkTheme.tss
└── PanelSettings/    RuntimePanel.asset, WorldSpacePanel.asset
```

## Skills connexes

- `/unity-editor-tools` — Editor UI avec UI Toolkit (Custom Inspectors, EditorWindows)
- `/unity-code-gen` — generer automatiquement les presenters C# a partir du UXML

## Troubleshooting

| Symptome | Cause probable | Solution |
|----------|---------------|----------|
| Element pas visible | Pas de flex-grow ou dimensions a 0 | Ajouter `flex-grow: 1` ou width/height explicites |
| Style pas applique | Nom de classe incorrect / specificity | Verifier orthographe, inspecter avec UI Debugger |
| Click pas detecte | picking-mode: Ignore | Mettre `picking-mode: Position` |
| DataBinding pas update | Manque [CreateProperty] | Ajouter attribut + INotifyBindablePropertyChanged |
| Text tronque | white-space: nowrap par defaut | `white-space: normal` ou `text-overflow: ellipsis` |
| USS transitions saccadees | Trop d'elements animes | Limiter aux :hover/:active |
| UI floue | Scale mode incorrect | Scale With Screen Size + reference resolution |
| Z-order incorrect | Sort Order UIDocument | Augmenter le Sort Order |
