---
name: "Unity Rapid Proto"
description: "Prototypage instantane de gameplay Unity. Triggers: /proto, /prototype, 'prototyper', 'idee de jeu', 'tester une mechanique', 'rapid proto'. Transforme une idee de gameplay en scene jouable avec le minimum de code. Produit 1-3 scripts MonoBehaviour, les instructions de setup scene, et une checklist de test. Aucune architecture, aucun planning -- juste du code jouable."
---

# Unity Rapid Proto

## Ce que fait cette skill

Transforme une idee de gameplay brute en prototype jouable Unity. Pas de GDD, pas de planning, pas d'architecture. On va droit au code minimum pour tester la mechanique.

Produit :
- 1 a 3 scripts C# (MonoBehaviour uniquement)
- Les instructions de setup scene (hierarchy, components, valeurs)
- Une checklist "press Play" pour verifier que ca marche

## Prerequis

- Projet Unity existant
- Un dossier `Assets/Prototypes/` (sera cree si absent)
- Connaissance du concept a prototyper en 1-2 phrases

## Arbre de decision

```
Type de prototype ?
|
+-- 3D gameplay ?
|   +-- Deplacement + exploration --> Template 3D Platformer
|   +-- Tir / combat --> Template FPS
|   +-- Placement strategique --> Template Tower Defense
|   +-- Course automatique --> Template Runner / Endless
|
+-- 2D gameplay ?
|   +-- Deplacement top-down --> Template Top-Down 2D
|   +-- Puzzle / grille --> Template Puzzle (grid-based)
|   +-- Platformer 2D --> Adapter Template 3D Platformer en 2D
|
+-- Pas sur ?
    +-- Commencer en 3D (plus visuel, plus facile a debloquer)
```

## Demarrage rapide

1. L'utilisateur decrit son idee en 1-2 phrases
2. Identifier LA mechanique centrale
3. Generer les scripts (max 3, max 100 lignes chacun)
4. Ecrire les instructions de setup scene
5. Fournir la checklist de test

## Guide etape par etape

### Etape 1 : Comprendre l'idee

Demander a l'utilisateur de decrire son idee en 1-2 phrases maximum. Ne PAS demander de details supplementaires. Ne PAS produire de document de design.

Extraire :
- Le verbe principal (sauter, tirer, placer, esquiver, collecter)
- Le contexte spatial (2D/3D, vue camera)
- La condition de fin (score, timer, survie, puzzle resolu)

### Etape 2 : Identifier la mechanique core

Choisir UNE seule mechanique a prototyper. Si l'idee contient plusieurs mecaniques, prendre celle qui definit le gameplay loop principal.

Exemples de reduction :
- "Un jeu ou on construit des tours pour defendre une base contre des vagues d'ennemis" -> Mechanique core : placement de tourelles + path following
- "Un platformer avec des pouvoirs magiques et du crafting" -> Mechanique core : mouvement + saut (le reste viendra apres)
- "Un FPS multijoueur avec des classes" -> Mechanique core : deplacement + tir raycast

### Etape 3 : Generer le code minimal

Structure type :
- `PlayerController.cs` : mouvement + action principale (max 80 lignes)
- 1-2 scripts gameplay selon le besoin (max 60 lignes chacun)

Regles de code :
```
- MonoBehaviour uniquement, pas de ScriptableObject
- Input.GetKey / Input.GetAxis (ancien systeme, plus simple)
- Valeurs hardcodees (pas de SerializeField sauf si vraiment utile)
- Visuels = primitives Unity (Cube, Sphere, Capsule, Plane)
- Pas de namespace, pas de pattern, pas d'event system
- Un seul fichier = une seule responsabilite evidente
- 1 commentaire par bloc non-evident, pas plus
```

> **Note Input System (Unity 6+)** : Si le projet utilise le New Input System (defaut dans Unity 6), remplacer les appels `Input.*` :
> - `Input.GetKey(KeyCode.Space)` → `Keyboard.current[Key.Space].isPressed`
> - `Input.GetKeyDown(KeyCode.Space)` → `Keyboard.current[Key.Space].wasPressedThisFrame`
> - `Input.GetAxis("Horizontal")` → `Gamepad.current.leftStick.x.ReadValue()` ou InputAction
> - `Input.GetMouseButton(0)` → `Mouse.current.leftButton.isPressed`
>
> Pour un prototype rapide, le old Input Manager reste plus simple. Verifier `Edit > Project Settings > Player > Active Input Handling`.

### Etape 4 : Ecrire les instructions de setup

Fournir dans cet ordre exact :
1. Scene : creer une nouvelle scene ou utiliser SampleScene
2. Objets a creer (avec nom, primitive, position, scale)
3. Components a ajouter sur chaque objet
4. Hierarchy parent/enfant si necessaire
5. Tags et Layers necessaires
6. Camera setup (position, rotation)

Format :
```
## Setup Scene

1. Creer un objet **Player** : Capsule a position (0, 1, 0)
   - Ajouter `PlayerController.cs`
   - Ajouter Rigidbody (Use Gravity: true, Freeze Rotation X/Z)

2. Creer un objet **Ground** : Plane a position (0, 0, 0), scale (5, 1, 5)
   - Tag: "Ground"
```

### Etape 5 : Checklist "press Play"

Lister exactement ce qui doit se passer quand on appuie sur Play :
```
## Test checklist

- [ ] Le joueur se deplace avec WASD/fleches
- [ ] Le joueur saute avec Space et retombe
- [ ] Les ennemis apparaissent toutes les 3 secondes
- [ ] Le score augmente quand on touche un ennemi
- [ ] Game Over s'affiche quand la vie atteint 0
```

## Templates par genre

6 templates pre-configures dans `references/proto-templates.md` :

| Genre | Scripts | Objets cles |
|-------|---------|-------------|
| 3D Platformer | PlayerController + MovingPlatform | Capsule + CharacterController, Planes, Cubes |
| FPS | FPSController + EnemyHealth + Spawner | Capsule + Camera enfant, Cubes rouges |
| Top-Down 2D | PlayerMovement2D + Bullet + EnemyPatrol2D | Sprites, Rigidbody2D, Camera ortho |
| Puzzle (grid) | GridManager + Tile | Quads generes, UI Text victoire |
| Runner / Endless | RunnerPlayer + ObstacleSpawner + ScoreManager | Capsule auto-avance, 3 lanes |
| Tower Defense | Turret + EnemyPath + TurretPlacer | Waypoints, OverlapSphere, InvokeRepeating |

## Skills connexes

- Le prototype fonctionne et on veut passer en production ? Utiliser `/unity-code-gen` (Unity Code Gen) pour restructurer avec les bons patterns
- Bug dans le prototype ? Utiliser `/unity-debug` (Unity Debug)
- Besoin d'un shader custom pour le prototype ? Utiliser `/shader` (Unity Shader Generator)
- Prototype 2D (platformer, top-down) ? Utiliser `/2d` (Unity 2D) pour les patterns detailles

## Regles strictes

**TOUJOURS :**
- Utiliser des primitives Unity pour les visuels (Cube, Sphere, Capsule, Plane)
- Inclure une condition de victoire/defaite ou un feedback loop
- Utiliser `Input.GetKey` / `Input.GetAxis` (ancien input system)
- Garder les valeurs hardcodees (vitesse, vie, degats)
- Ecrire le code dans `Assets/Prototypes/<NomPrototype>/`
- Tester mentalement chaque script : est-ce que ca compile ? est-ce que ca fait quelque chose de visible ?

**JAMAIS :**
- Plus de 3 scripts par prototype
- Plus de 100 lignes par script (80 pour le PlayerController)
- D'architecture : pas de SO, pas d'events, pas de managers, pas de singletons
- De documentation ou README
- De commentaires abondants (1 ligne par bloc non-evident maximum)
- De SerializeField sauf si absolument necessaire pour le workflow scene
- De namespace, d'interface, de classe abstraite, de generics
- D'asset externe, de package additionnel, d'Asset Store

## Troubleshooting

| Probleme | Solution |
|----------|----------|
| Le joueur ne bouge pas | Verifier que le script est attache au bon GameObject. Verifier que `CharacterController` ou `Rigidbody` est present. |
| Le joueur tombe a travers le sol | Verifier que le sol a un Collider. Verifier que le joueur a un Collider + Rigidbody (ou CharacterController). |
| Le saut ne fonctionne pas | Verifier le ground check : le raycast doit pointer vers `Vector3.down` avec une distance legerement superieure a la moitie de la hauteur du joueur. |
| Les collisions ne detectent pas | Verifier qu'au moins un des deux objets a un Rigidbody. Si on utilise `OnTriggerEnter`, le Collider doit etre marque "Is Trigger". |
| La camera tremble | Deplacer la logique camera dans `LateUpdate` au lieu de `Update`. |
| Les ennemis n'apparaissent pas | Verifier que le prefab est assigne ou que `Instantiate` utilise le bon reference. Verifier que `InvokeRepeating` est appele dans `Start`. |
| Le score ne s'affiche pas | Verifier la reference au `Text` ou `TextMeshProUGUI`. Verifier que le Canvas a un EventSystem. |
| Le prototype est trop lent | Supprimer les `Debug.Log` dans Update. Verifier qu'on ne fait pas d'Instantiate/Destroy massif (passer a un pool basique si necessaire). |
