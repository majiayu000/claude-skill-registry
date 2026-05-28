---
name: image-to-3d-pipeline
description: "Transformez une image 2D en modèle 3D animé prêt pour le web ou le jeu en moins de 30 minutes, en utilisant le workflow Dilum Sanjaya (Hunyuan3D + Mixamo). Use when: **Créer un personnage 3D pour un site web** - Mascotte, avatar, illustration interactive; **Prototyper un asset de jeu** - Character design, props, environnements; **Produire du contenu marketing 3D** - Produits rotatifs, personnages animés; **Convertir des illustrations existantes** - Logo, mascotte, character design → 3D; **Tes..."
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Image to 3D Pipeline

> Transformez une image 2D en modèle 3D animé prêt pour le web ou le jeu en moins de 30 minutes, en utilisant le workflow Dilum Sanjaya (Hunyuan3D + Mixamo).

## When to Use This Skill

- **Créer un personnage 3D pour un site web** - Mascotte, avatar, illustration interactive
- **Prototyper un asset de jeu** - Character design, props, environnements
- **Produire du contenu marketing 3D** - Produits rotatifs, personnages animés
- **Convertir des illustrations existantes** - Logo, mascotte, character design → 3D
- **Tester une idée rapidement** - Prototype 3D en 30 minutes au lieu de jours

## Methodology Foundation

**Source**: Dilum Sanjaya (@DilumSanjaya) - Game Character Pipeline (2025-2026)

**Core Principle**: "L'image 2D est votre blueprint. Hunyuan3D génère le mesh, Mixamo ajoute le rig automatiquement. En 30 minutes, vous avez un personnage animé utilisable dans Three.js ou Unity."

**Why This Matters**: Traditionnellement, passer d'un concept 2D à un modèle 3D riggé prenait des jours de travail de modélisation. Ce workflow réduit le temps à moins d'une heure tout en produisant des assets de qualité suffisante pour la production.


## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Structures video workflow | Final creative vision |
| Suggests shot compositions | Equipment selection |
| Creates storyboard templates | Brand aesthetics |
| Generates script frameworks | Final approval |
| Identifies technical requirements | Budget allocation |

## What This Skill Does

1. **Guide le choix de l'outil 3D** - Hunyuan3D vs Tripo vs Meshy selon le use case
2. **Structure le workflow complet** - De l'image source au modèle exporté
3. **Optimise le mesh généré** - Réduction de polygones, correction de textures
4. **Automatise le rigging** - Configuration Mixamo pour personnages
5. **Prépare l'export** - Formats GLB/FBX selon la destination

## How to Use

### Convertir un character design en personnage 3D animé
```
J'ai cette image de personnage [joindre image]. Aide-moi à la convertir en modèle 3D animé avec le skill image-to-3d-pipeline.
```

### Créer un produit 3D rotatif
```
Je veux créer un modèle 3D de mon produit [description] à partir de photos. Guide-moi avec le pipeline image-to-3d.
```

### Prototyper une mascotte de marque
```
Voici le design de notre mascotte [image]. Je veux la transformer en 3D pour notre site web avec des animations idle.
```

## Instructions

Quand vous aidez à convertir une image 2D en 3D, suivez ce processus :

### Step 1: Évaluer l'image source

```
## Analyse de l'Image Source

**Type d'image:**
[ ] Character design / Personnage
[ ] Objet / Produit
[ ] Illustration / Logo
[ ] Photo réelle

**Qualité pour conversion 3D:**
[ ] ✅ Vue frontale claire
[ ] ✅ Fond simple ou transparent
[ ] ✅ Couleurs/textures distinctes
[ ] ✅ Proportions cohérentes
[ ] ⚠️ Détails complexes (peut perdre en conversion)

**Complexité estimée:**
[ ] Simple - Forme géométrique basique
[ ] Moyenne - Personnage ou objet organique
[ ] Complexe - Détails fins, accessoires multiples
```

**Points clés:**
- Les vues frontales donnent de meilleurs résultats
- Les fonds transparents/blancs simplifient le traitement
- Les personnages avec membres distincts se riggent mieux

---

### Step 2: Choisir l'outil de conversion

| Outil | Forces | Idéal pour | Limitations |
|-------|--------|------------|-------------|
| **Hunyuan3D** | Meilleure texture, open source | Personnages, objets détaillés | Cleanup parfois nécessaire |
| **Tripo AI** | UX simple, rigging auto | Prototypes rapides | Moins de contrôle |
| **Meshy** | Bon pour stylisé | Assets cartoon/low-poly | Textures moins réalistes |
| **Rodin Gen-1** | Vitesse, topology game-ready | Game assets | Moins de fidélité |
| **CSM** | Multi-view consistency | Objets complexes | Plus lent |

**Recommandation par use case:**
- **Personnage pour web** → Hunyuan3D + Mixamo
- **Prototype rapide** → Tripo AI
- **Asset jeu stylisé** → Meshy ou Rodin
- **Produit réaliste** → Hunyuan3D + post-processing

---

### Step 3: Pipeline de conversion

```
## Pipeline Standard (Hunyuan3D)

### A. Préparation de l'image
1. Supprimer le fond (remove.bg ou outil intégré)
2. Recadrer serré sur le sujet
3. Résolution recommandée: 1024x1024 minimum
4. Sauvegarder en PNG (préserver transparence)

### B. Génération 3D
1. Uploader sur Hunyuan3D (hunyuan3d.tencent.com)
2. Sélectionner mode: "Image to 3D"
3. Paramètres recommandés:
   - Quality: High
   - Texture: Enable
   - Multi-view: Enable (si disponible)
4. Générer et télécharger (GLB ou OBJ)

### C. Validation du mesh
- Ouvrir dans Blender ou viewer en ligne
- Vérifier: topology, textures, scale
- Identifier problèmes: trous, textures manquantes
```

---

### Step 4: Optimisation et nettoyage

```
## Checklist Optimisation

### Mesh
[ ] Poly count acceptable (< 50k pour web, < 100k pour jeu)
[ ] Pas de faces inversées
[ ] Pas de vertices orphelins
[ ] Mesh manifold (étanche)

### Textures
[ ] UV map correcte
[ ] Résolution appropriée (1024x1024 ou 2048x2048)
[ ] Pas de stretching visible
[ ] Couleurs fidèles à l'original

### Scale
[ ] Proportions correctes
[ ] Orientation (Y-up ou Z-up selon destination)
[ ] Centré sur origin
```

**Outils de cleanup:**
- **Blender** (gratuit) - Decimate modifier, texture paint
- **Meshlab** (gratuit) - Réparation automatique
- **gltf-transform** (CLI) - Optimisation GLB pour web

---

### Step 5: Rigging avec Mixamo (personnages uniquement)

```
## Workflow Mixamo

1. Exporter le mesh en FBX (sans textures embarquées)
2. Uploader sur mixamo.com
3. Positionner les markers:
   - Chin
   - Wrists
   - Elbows
   - Knees
   - Groin
4. Sélectionner "Auto-Rig"
5. Choisir animations:
   - Idle (standing, breathing)
   - Walk
   - Run
   - Autres selon besoin
6. Télécharger en FBX avec skin
```

**Animations recommandées pour web:**
- `Idle` - Animation de base
- `Walking` - Pour déplacements
- `Waving` - Interaction
- `Talking` - Si voix-off

---

### Step 6: Export et intégration

| Destination | Format | Notes |
|-------------|--------|-------|
| **Three.js / Web** | GLB | Format recommandé, embedde textures |
| **Unity** | FBX | Import natif, configurer materials |
| **Unreal** | FBX | Nécessite skeleton retargeting |
| **React Three Fiber** | GLB | Utiliser gltfjsx pour composant |

```bash
# Optimisation GLB pour web (gltf-transform)
npx @gltf-transform/cli optimize input.glb output.glb --compress draco
```

**Taille cible:**
- Hero 3D (première chose visible): < 2MB
- Asset secondaire: < 500KB
- Personnage animé: < 5MB

## Examples

### Example 1: Personnage de jeu - Character Selection Screen

**Input**: Concept art de personnage (style cartoon)

**Process**:
1. Nano Banana → Génération character sheet cohérent
2. Hunyuan3D → Conversion en mesh 3D
3. Blender → Cleanup rapide (5 min)
4. Mixamo → Auto-rig + animations idle/select
5. Three.js → Intégration avec rotation au survol

**Output**: Personnage 3D interactif avec 3 animations
**Temps total**: ~45 minutes

**Code Three.js basique:**
```jsx
import { useGLTF, useAnimations } from '@react-three/drei'

function Character({ url }) {
  const { scene, animations } = useGLTF(url)
  const { actions } = useAnimations(animations, scene)

  useEffect(() => {
    actions['idle']?.play()
  }, [])

  return <primitive object={scene} />
}
```

---

### Example 2: Mascotte de marque pour landing page

**Input**: Illustration 2D de mascotte entreprise

**Process**:
1. Cleanup fond (remove.bg)
2. Hunyuan3D → Mesh 3D avec textures
3. Pas de rigging (statique)
4. Export GLB optimisé
5. Spline ou Three.js → Animation CSS/JS simple (rotation, bounce)

**Output**: Mascotte 3D tournante en hero section
**Temps total**: ~20 minutes

---

### Example 3: Produit e-commerce 360°

**Input**: 4 photos du produit (face, dos, côtés)

**Process**:
1. CSM → Multi-view reconstruction (meilleur pour objets)
2. Cleanup Blender → Simplifier geometry
3. Bake textures hautes résolution
4. Export GLB
5. model-viewer → Viewer 3D responsive

**Output**: Viewer 3D interactif avec zoom/rotation
**Temps total**: ~1 heure

**Code model-viewer:**
```html
<model-viewer
  src="product.glb"
  ar
  auto-rotate
  camera-controls
  shadow-intensity="1"
></model-viewer>
```

## Checklists & Templates

### Checklist Pré-Conversion

```
## Image Source
[ ] Résolution suffisante (min 1024x1024)
[ ] Fond transparent ou uniforme
[ ] Sujet bien délimité
[ ] Style cohérent (pas de mix photo/illustration)

## Objectif
[ ] Destination claire (web/jeu/vidéo)
[ ] Poly budget défini
[ ] Animations nécessaires identifiées
[ ] Format d'export choisi
```

### Template Brief 3D

```
## Brief Conversion 2D → 3D

**Image source:** [joindre]
**Type:** [ ] Personnage [ ] Objet [ ] Logo [ ] Autre

**Destination finale:**
- Plateforme: _______________
- Interaction: [ ] Statique [ ] Rotation [ ] Animation complète
- Taille max: ___ MB

**Style souhaité:**
- [ ] Fidèle à l'original
- [ ] Stylisé/Low-poly
- [ ] Réaliste

**Animations (si personnage):**
- [ ] Idle
- [ ] Walk
- [ ] Autres: _______________

**Contraintes:**
- _______________
```

## Tool Comparison Matrix

| Critère | Hunyuan3D | Tripo AI | Meshy | Rodin | CSM |
|---------|-----------|----------|-------|-------|-----|
| **Qualité texture** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Vitesse** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **Facilité** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Cleanup requis** | Moyen | Faible | Faible | Faible | Moyen |
| **Prix** | Gratuit | Freemium | Freemium | Payant | Freemium |
| **Best for** | Personnages | Prototypes | Stylisé | Jeux | Multi-view |

## Troubleshooting

| Problème | Cause probable | Solution |
|----------|----------------|----------|
| Mesh "explosé" | Fond non transparent | Retirer le fond avant upload |
| Textures manquantes | Export sans embedde | Re-exporter avec textures packées |
| Rigging échoue | Pose non T-pose | Modifier pose dans Blender avant Mixamo |
| Fichier trop lourd | Trop de polygones | Utiliser Decimate modifier |
| Animations saccadées | FPS incompatible | Re-exporter à 30fps |

## Skill Boundaries

### What This Skill Does Well
- Structuring video production workflows
- Creating storyboard frameworks
- Suggesting technical approaches
- Providing creative direction templates

### What This Skill Cannot Do
- Replace professional videography
- Edit video files directly
- Make final creative judgments
- Guarantee audience engagement

## References

### Outils
- [Hunyuan3D](https://hunyuan3d.tencent.com) - Tencent, gratuit
- [Tripo AI](https://www.tripo3d.ai) - Freemium
- [Meshy](https://www.meshy.ai) - Freemium
- [Mixamo](https://www.mixamo.com) - Adobe, gratuit
- [gltf-transform](https://gltf-transform.donmccurdy.com) - CLI optimisation

### Tutorials
- Dilum Sanjaya: Character to 3D workflows (X/Twitter)
- Three.js Fundamentals: Loading 3D models
- React Three Fiber: useGLTF documentation

### Research
- `docs/research-ai-design-workflows-2026-01.md` - Deep research 75+ sources

## Related Skills

- `character-design-ai/` - Générer des images de personnages cohérentes (input pour ce skill)
- `vibe-coding-design/` - Méthodologie itérative rapide
- `ai-ui-generation/` - Intégrer le 3D dans une interface générée

---

*Skill version: 1.0*
*Last updated: 2026-01-28*
*Category: ai-design*
