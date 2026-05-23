---
name: "Unity 2D"
description: "Guide complet pour le developpement 2D dans Unity 6+ : Tilemap, Sprite, 2D platformer, top-down 2D, 2D physics, Light2D, Sprite Atlas, pixel art, 2D game, jeu 2D, tile, Rule Tile. Commandes : /unity-2d, /2d"
---

# Unity 2D

## Ce que fait cette skill

Guide le developpement de jeux 2D dans Unity 6+ : mise en place de Tilemaps et Rule Tiles, physics 2D (Rigidbody2D, Collider2D), gestion des sprites et Sprite Atlas, eclairage 2D avec URP (Light2D, Shadow Caster 2D), configuration camera avec Cinemachine, et patterns de gameplay (platformer, top-down, puzzle). Couvre aussi le pixel art, le parallax scrolling et l'optimisation des Tilemaps.

## Prerequis

- Unity 6.0+ avec **URP** configure en **2D Renderer**
- Package **2D Tilemap Extras** (Rule Tiles, Animated Tiles)
- Package **Cinemachine** pour la camera 2D
- Package **2D Sprite** et **2D Animation** si Sprite Swap necessaire

## Demarrage rapide

1. **Configurer URP 2D** : Dans le URP Renderer Asset, ajouter un **2D Renderer Data**. L'assigner dans les Graphics Settings du projet.
2. **Creer un Tilemap** : GameObject > 2D Object > Tilemap > Rectangular. Ouvrir la Tile Palette (Window > 2D > Tile Palette) et peindre.
3. **Ajouter la physique** : Tilemap Collider 2D + Composite Collider 2D sur le Tilemap de collision. Rigidbody2D (Static) sur le Tilemap.
4. **Configurer la camera** : Ajouter CinemachineCamera avec CinemachinePositionComposer. Follow = joueur. Ajouter CinemachineConfiner2D avec un CompositeCollider2D pour les limites.
5. **Importer les sprites** : Filter Mode = Point (pixel art) ou Bilinear. PPU = taille de tuile (16, 32...). Creer un Sprite Atlas pour le batching.

## Arbre de decision

```
Type de jeu 2D ?
|
+-- Platformer ?
|   +-- Classique ----------> Rigidbody2D + Tilemap + Coyote time
|   |                         (voir references/2d-patterns.md et 2d-advanced.md)
|   +-- Metroidvania -------> idem + abilities unlock
|                              + Cinemachine Confiner2D par zone
|
+-- Top-down ?
|   +-- Action (Zelda) -----> Rigidbody2D, 8-dir, GravityScale=0
|   +-- RPG / exploration --> idem + Tilemap layers + dialogue system
|
+-- Puzzle / match ?
|   +-- Grid-based ---------> Tilemap ou Grid custom, pas de physics
|
+-- Visual novel / UI-heavy ?
|   +-- --------------------> UI Toolkit (/uitk), pas de physics 2D
|
+-- Besoin de lumiere / ombres ?
    +-- --------------------> URP 2D Renderer + Light2D
                              (voir references/2d-rendering.md)
```

## Guide etape par etape

### Etape 1 : Setup URP 2D Renderer

Creer un **2D Renderer Data** asset (Create > Rendering > URP 2D Renderer). Dans le URP Asset, l'assigner comme Renderer par defaut. Verifier que la camera utilise bien le **Renderer 2D** dans son inspecteur.

### Etape 2 : Creer les Tilemaps

Organiser en **layers** sur un seul Grid :
- `Tilemap_Background` (Sorting Layer: Background, Order 0)
- `Tilemap_Ground` (Sorting Layer: Tilemap, Order 0) + Tilemap Collider 2D + Composite Collider 2D
- `Tilemap_Foreground` (Sorting Layer: Foreground, Order 0)

Utiliser des **Rule Tiles** (2D Tilemap Extras) pour l'auto-tiling des plateformes et murs.

### Etape 3 : Configurer la physique 2D

Sur le joueur : Rigidbody2D (Dynamic, Freeze Rotation Z). Ajouter un CapsuleCollider2D ou BoxCollider2D. Sur les plateformes : Composite Collider 2D (Geometry Type = Polygons) avec Rigidbody2D Static. Utiliser des Physics Material 2D pour le friction/bounce.

### Etape 4 : Setup camera Cinemachine

CinemachineCamera avec **CinemachinePositionComposer** (Dead Zone, Lookahead). Ajouter **CinemachineConfiner2D** lie a un PolygonCollider2D/CompositeCollider2D qui definit les limites du niveau. Pour le pixel art : activer **Pixel Perfect Camera** (package 2D Pixel Perfect).

### Etape 5 : Import et optimisation des sprites

Importer les spritesheets. Configurer le **Sprite Editor** pour le slice (Grid by Cell Size). Creer un **Sprite Atlas** par zone/categorie (voir references/2d-rendering.md). Pour le pixel art : Filter = Point, Compression = None, PPU = taille de tuile.

## Regles strictes

- **TOUJOURS** utiliser `Rigidbody2D.linearVelocity` (Unity 6+), jamais `velocity`
- **TOUJOURS** mettre la physique dans `FixedUpdate`, les inputs dans `Update`
- **TOUJOURS** utiliser Composite Collider 2D sur les Tilemaps de collision
- **TOUJOURS** organiser les Sorting Layers (Background < Tilemap < Characters < Foreground < UI)
- **JAMAIS** de Rigidbody2D Dynamic sur un Tilemap (utiliser Static ou Kinematic)
- **JAMAIS** de sprites individuels sans Sprite Atlas en production
- **JAMAIS** melanger Rigidbody 3D et 2D sur le meme GameObject
- **JAMAIS** de scale negatif pour flip sprite : utiliser `SpriteRenderer.flipX`

## Skills connexes

- `/proto` : Prototypage rapide de gameplay 2D
- `/unity-code-gen` : Generation de scripts C# (controllers, spawners)
- `/anim` : Animator, Sprite Animation, Timeline
- `/shader` : Shaders 2D custom (outline, dissolve, water)
- `/perf-audit` : Optimisation draw calls, batching, Sprite Atlas

## Troubleshooting

| Probleme | Cause | Solution |
|----------|-------|----------|
| Sprite invisible | Sorting Layer/Order incorrect | Verifier Sorting Layer et Order in Layer dans SpriteRenderer |
| Tilemap collision traversee | Pas de Composite Collider | Ajouter Composite Collider 2D + Rigidbody2D Static au Tilemap |
| Joueur glisse sur les murs | Friction avec les tiles laterales | Physics Material 2D avec Friction=0 sur le joueur |
| Lumiere 2D sans effet | Pas de 2D Renderer | Verifier que le URP Asset utilise un 2D Renderer Data |
| Sprite flou (pixel art) | Mauvais import settings | Filter Mode = Point, Compression = None |
| Camera saccadee | Mouvement hors FixedUpdate | Interpolation = Interpolate sur Rigidbody2D |
| Tiles avec gaps visuels | Anti-aliasing sur les bords | PPU coherent, Pixel Snap active, pas de scale fractionnaire |
| Draw calls eleves | Pas de batching | Creer un Sprite Atlas, verifier le Dynamic Batching URP |
