---
name: "Unity Shader Generator"
description: "Genere des shaders Unity (HLSL/ShaderLab) pour effets visuels. Triggers: /shader, /shader-gen, 'creer un shader', 'effet visuel shader', 'dissolve', 'outline', 'toon shading', 'hologram', 'water shader'. Detecte automatiquement le render pipeline (URP/HDRP/Built-in) et produit un fichier .shader pret a l'emploi avec instructions de Material."
---

# Unity Shader Generator

## Ce que fait cette skill

Genere des shaders Unity complets (fichiers `.shader`) adaptes au render pipeline du projet. Couvre les effets courants : dissolve, outline, toon, hologram, force field, water, triplanar, vertex displacement. Produit du code HLSL/ShaderLab propre, optimise mobile, avec instructions de setup Material.

## Prerequis

- Un projet Unity existant avec un `Packages/manifest.json`
- Connaissance de l'effet souhaite (description textuelle ou reference visuelle)
- Acces en ecriture au dossier `Assets/`

## Arbre de decision

```
Type de shader demande ?
|
+-- Effet sur un materiau (dissolve, outline, toon, hologram) ?
|   +-- --> Recettes dans references/shader-recipes.md
|
+-- Post-processing / fullscreen effect ?
|   +-- URP 6.3+ --> Fullscreen Shader Graph (prefere, zero code)
|   +-- URP custom --> Custom render pass avec Render Graph API
|   +-- HDRP --> Custom Pass Volume
|
+-- Custom render pass (injection dans le pipeline) ?
|   +-- Unity 6+ --> Render Graph API (RecordRenderGraph)
|   +-- Pre-Unity 6 --> ScriptableRenderPass.Execute (deprecie)
|
+-- Modification de vertices (displacement, wind, snow) ?
    +-- --> Vertex shader avec noise (voir references/hlsl-utils.md)
```

## Demarrage rapide

1. L'utilisateur decrit l'effet voulu (ex: "un shader de dissolve avec bordure lumineuse")
2. Le skill detecte le render pipeline du projet
3. Le skill genere le fichier `.shader` et les instructions Material

## Guide etape par etape

### Etape 1 : Identifier l'effet desire

Analyser la demande utilisateur. Classifier l'effet parmi les recettes connues :
- **Dissolve** : destruction progressive avec seuil
- **Outline** : contour colore autour d'un objet
- **Toon/Cel-shading** : rendu cartoon avec paliers de lumiere
- **Hologram** : effet holographique avec scanlines et transparence
- **Force field** : bouclier energetique avec fresnel et intersection
- **Water surface** : eau avec vagues et transparence
- **Triplanar mapping** : projection UV en world-space
- **Vertex displacement** : deformation de vertices par noise
- **Custom** : combiner les techniques ci-dessus

Pour les recettes d'effets detaillees, voir `references/shader-recipes.md`.

### Etape 2 : Detecter le render pipeline

Utiliser Grep sur le fichier `manifest.json` du projet :

```
Grep "com.unity.render-pipelines.universal" dans Packages/manifest.json → URP
Grep "com.unity.render-pipelines.high-definition" dans Packages/manifest.json → HDRP
Aucun match → Built-in Render Pipeline
```

Cette detection est **obligatoire** avant de generer le moindre code.

### Etape 3 : Choisir le format shader

Selon le pipeline detecte, utiliser le template correspondant dans `references/shader-templates.md` :

| Pipeline | Format | Tags cles |
|----------|--------|-----------|
| Built-in | ShaderLab + CG/HLSL | `CGPROGRAM/ENDCG`, surface shader |
| URP | ShaderLab + HLSL | `"RenderPipeline"="UniversalPipeline"`, `CBUFFER_START(UnityPerMaterial)` |
| HDRP | ShaderLab + HLSL (HDRP includes) | Preferer Shader Graph |

**Important URP** : Toujours inclure `CBUFFER_START(UnityPerMaterial)` pour la compatibilite SRP Batcher.

### Etape 4 : Generer le shader

Ecrire le fichier `.shader` complet dans le projet :
- **Emplacement** : `Assets/Shaders/` ou `Assets/Art/Shaders/`
- **Nommage** : `Game_Category_EffectName.shader` (ex: `Game_FX_Dissolve.shader`)
- Inclure : Properties, SubShader, Pass(es), vertex/fragment, Fallback

### Etape 5 : Instructions Material

Toujours fournir les instructions de setup Material :
1. Dans Unity : `Assets > Create > Material`
2. Assigner le shader dans le dropdown Material (chercher `Game/Category/EffectName`)
3. Configurer les Properties exposees (textures, couleurs, seuils)
4. Appliquer le Material sur le GameObject cible

## Render Graph API (Unity 6+)

Unity 6 utilise le **Render Graph** comme backend pour URP et HDRP. Les custom render passes doivent migrer vers `RecordRenderGraph` (l'ancien `Execute` est deprecie).

Pattern et migration detailles dans `references/shader-templates.md#render-graph-api`.

## ShadowCaster Pass URP

Pass **requis** pour que l'objet projette des ombres en URP. Template dans `references/shader-templates.md#shadowcaster-pass`.

## Regles strictes

- **TOUJOURS** detecter le render pipeline avant de generer du code
- **TOUJOURS** inclure un `Fallback` shader
- **TOUJOURS** exposer les parametres cles comme Properties (jamais de valeurs hardcodees)
- **TOUJOURS** fournir les instructions Material apres le shader
- **TOUJOURS** placer le fichier dans `Assets/Shaders/` ou sous-dossier
- **TOUJOURS** nommer le shader avec le pattern `Game/Category/EffectName`
- **TOUJOURS** inclure un pass `ShadowCaster` en URP (voir section dediee)
- **JAMAIS** melanger `CGPROGRAM/ENDCG` et `HLSLPROGRAM/ENDHLSL` dans le meme shader
- **JAMAIS** utiliser des surface shaders en URP/HDRP (vertex/fragment uniquement)
- **JAMAIS** oublier le `CBUFFER_START(UnityPerMaterial)` en URP (necessaire pour SRP Batcher)
- **PREFERER** `half` precision pour les targets mobiles
- **PREFERER** Shader Graph pour les artistes non-techniques (fournir une description nodale)

## Skills connexes

- Le shader est pour un prototype rapide ? Utiliser `/proto` (Unity Rapid Proto) pour le setup scene
- Configurer le build apres les shaders ? Utiliser `/build-config` (Unity Build & CI/CD Configurator)
- Problemes de performance shader ? Utiliser `/unity-perf-audit` pour l'audit de performance
- Performance de rendu ? Utiliser `/perf-audit` (Unity Perf Audit)

## Troubleshooting

| Probleme | Solution |
|----------|----------|
| Shader rose/magenta | Erreur de compilation : verifier les includes du pipeline, les noms de fonctions, les semantiques |
| SRP Batcher incompatible | Mettre toutes les Properties dans un `CBUFFER_START(UnityPerMaterial)` / `CBUFFER_END` |
| Shader ne fonctionne pas en URP | Verifier les tags `"RenderPipeline"="UniversalPipeline"` et `"LightMode"="UniversalForward"` |
| Transparence ne s'affiche pas | Ajouter `Tags { "Queue"="Transparent" }`, `Blend SrcAlpha OneMinusSrcAlpha`, `ZWrite Off` |
| Ombre absente | Ajouter un pass `ShadowCaster` avec les includes appropriees (voir section ShadowCaster) |
| Performance faible mobile | Reduire les samples texture, passer en `half`, supprimer les `if` dynamiques |
| Textures floues / tiling incorrect | Verifier `TRANSFORM_TEX(IN.uv, _MainTex)` et les `_ST` variables dans le CBUFFER |
| Depth intersection ne fonctionne pas | S'assurer que `_CameraDepthTexture` est active (URP : cocher Depth Texture dans le pipeline asset) |

## References

- Pour les recettes d'effets detaillees, voir `references/shader-recipes.md`
- Pour les fonctions utilitaires HLSL et l'optimisation mobile, voir `references/hlsl-utils.md`
