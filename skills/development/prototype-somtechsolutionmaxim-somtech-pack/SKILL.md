---
name: prototype
description: Creer un prototype React + Tailwind heberge sur GitHub Pages. Utiliser quand on veut demarrer un nouveau prototype pour un client.
argument-hint: [nom-du-projet] [description-optionnelle]
---

# Creer un prototype React + Tailwind sur GitHub Pages

Creer un prototype complet pret a deployer sur GitHub Pages a partir du nom de projet fourni dans $ARGUMENTS.

## Etapes a suivre

### 1. Parser les arguments

- Le premier argument est le nom du projet (ex: `inventaire-prototype`)
- Le reste est une description optionnelle du projet
- Si aucun argument n'est fourni, demander le nom du projet

### 2. Creer le repertoire local

```bash
mkdir -p ~/projets/<nom-du-projet>
cd ~/projets/<nom-du-projet>
git init
```

### 3. Creer le fichier .gitignore

```
.DS_Store
node_modules/
```

### 4. Creer le fichier index.html

Generer un fichier `index.html` avec cette structure de base:

```html
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>[Nom du projet]</title>
  <script src="https://unpkg.com/react@18/umd/react.development.js" crossorigin></script>
  <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js" crossorigin></script>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body>
  <div id="root" class="h-screen"></div>
  <script>
const { useState, useEffect, useRef } = React;

// ============================================================
// ICON COMPONENTS (inline SVG - no external dependency)
// ============================================================
const createIcon = (paths) => {
  return function IconComponent(props) {
    const { className = '', size = 24, ...rest } = props || {};
    return React.createElement('svg', {
      xmlns: 'http://www.w3.org/2000/svg',
      width: size,
      height: size,
      viewBox: '0 0 24 24',
      fill: 'none',
      stroke: 'currentColor',
      strokeWidth: 2,
      strokeLinecap: 'round',
      strokeLinejoin: 'round',
      className: className,
      ...rest
    }, ...paths.map((p, i) => {
      if (typeof p === 'string') return React.createElement('path', { key: i, d: p });
      return React.createElement(p.tag, { key: i, ...p.attrs });
    }));
  };
};

// Ajouter les icones necessaires au projet ici
// Exemple:
// const Search = createIcon([{tag:'circle',attrs:{cx:11,cy:11,r:8}},{tag:'line',attrs:{x1:21,y1:21,x2:16.65,y2:16.65}}]);
// const Plus = createIcon([{tag:'line',attrs:{x1:12,y1:5,x2:12,y2:19}},{tag:'line',attrs:{x1:5,y1:12,x2:19,y2:12}}]);
// const X = createIcon([{tag:'line',attrs:{x1:18,y1:6,x2:6,y2:18}},{tag:'line',attrs:{x1:6,y1:6,x2:18,y2:18}}]);

// ============================================================
// APP COMPONENT
// ============================================================
function App() {
  return React.createElement('div', { className: 'min-h-screen bg-gray-50 p-8' },
    React.createElement('h1', { className: 'text-3xl font-bold text-gray-900' }, '[Nom du projet]'),
    React.createElement('p', { className: 'mt-2 text-gray-600' }, 'Prototype en cours de developpement...')
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(React.createElement(App, null));
  </script>
</body>
</html>
```

### 5. Creer le repo GitHub et activer Pages

```bash
cd ~/projets/<nom-du-projet>
git add .
git commit -m "Initial prototype setup"
gh repo create SomtechSolutionMAxime/<nom-du-projet> --public --source=. --push
gh api repos/SomtechSolutionMAxime/<nom-du-projet>/pages -X POST -f "build_type=workflow" -f "source[branch]=main" -f "source[path]=/" 2>/dev/null || true
```

Si l'API Pages echoue, activer via:
```bash
gh repo edit SomtechSolutionMAxime/<nom-du-projet> --enable-pages
```

### 6. Afficher le resultat

Afficher:
- URL du repo: `https://github.com/SomtechSolutionMAxime/<nom-du-projet>`
- URL GitHub Pages: `https://somtechsolutionmaxime.github.io/<nom-du-projet>/`
- Rappeler que GitHub Pages peut prendre 1-2 minutes pour se deployer

## Regles importantes

- **JAMAIS utiliser lucide-react via CDN** - le build UMD est casse. Toujours utiliser les icones SVG inline avec la fonction `createIcon`.
- **JAMAIS utiliser Babel CDN** pour compiler du JSX - trop lent et instable pour des gros fichiers. Ecrire directement en `React.createElement`.
- **Attention aux `</script>` dans les template literals** - les echapper avec `<\/script>`.
- Le fichier HTML doit etre autonome (pas de dependances npm).
- Utiliser Tailwind CSS via le Play CDN pour le styling.
- Si le prototype est base sur un fichier JSX existant, le pre-compiler en React.createElement (pas de JSX dans le HTML final).

## Icones disponibles (reference)

Voici les definitions des icones Lucide les plus courantes. Copier celles qui sont necessaires dans le projet:

```javascript
const Package = createIcon([{tag:'path',attrs:{d:'M16.5 9.4 7.55 4.24'}},{tag:'path',attrs:{d:'M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z'}},{tag:'polyline',attrs:{points:'3.27 6.96 12 12.01 20.73 6.96'}},{tag:'line',attrs:{x1:12,y1:22.08,x2:12,y2:12}}]);
const Users = createIcon([{tag:'path',attrs:{d:'M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2'}},{tag:'circle',attrs:{cx:9,cy:7,r:4}},{tag:'path',attrs:{d:'M22 21v-2a4 4 0 0 0-3-3.87'}},{tag:'path',attrs:{d:'M16 3.13a4 4 0 0 1 0 7.75'}}]);
const Bell = createIcon(['M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9',{tag:'path',attrs:{d:'M10.3 21a1.94 1.94 0 0 0 3.4 0'}}]);
const CheckCircle = createIcon([{tag:'path',attrs:{d:'M22 11.08V12a10 10 0 1 1-5.93-9.14'}},{tag:'polyline',attrs:{points:'22 4 12 14.01 9 11.01'}}]);
const AlertTriangle = createIcon(['M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z',{tag:'line',attrs:{x1:12,y1:9,x2:12,y2:13}},{tag:'line',attrs:{x1:12,y1:17,x2:12.01,y2:17}}]);
const Clock = createIcon([{tag:'circle',attrs:{cx:12,cy:12,r:10}},{tag:'polyline',attrs:{points:'12 6 12 12 16 14'}}]);
const Settings = createIcon([{tag:'path',attrs:{d:'M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z'}},{tag:'circle',attrs:{cx:12,cy:12,r:3}}]);
const Search = createIcon([{tag:'circle',attrs:{cx:11,cy:11,r:8}},{tag:'line',attrs:{x1:21,y1:21,x2:16.65,y2:16.65}}]);
const Plus = createIcon([{tag:'line',attrs:{x1:12,y1:5,x2:12,y2:19}},{tag:'line',attrs:{x1:5,y1:12,x2:19,y2:12}}]);
const X = createIcon([{tag:'line',attrs:{x1:18,y1:6,x2:6,y2:18}},{tag:'line',attrs:{x1:6,y1:6,x2:18,y2:18}}]);
const Filter = createIcon([{tag:'polygon',attrs:{points:'22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3'}}]);
const ChevronRight = createIcon([{tag:'polyline',attrs:{points:'9 18 15 12 9 6'}}]);
const ChevronDown = createIcon([{tag:'polyline',attrs:{points:'6 9 12 15 18 9'}}]);
const ArrowLeft = createIcon([{tag:'line',attrs:{x1:19,y1:12,x2:5,y2:12}},{tag:'polyline',attrs:{points:'12 19 5 12 12 5'}}]);
const Edit3 = createIcon([{tag:'path',attrs:{d:'M12 20h9'}},{tag:'path',attrs:{d:'M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z'}}]);
const Trash2 = createIcon([{tag:'polyline',attrs:{points:'3 6 5 6 21 6'}},{tag:'path',attrs:{d:'M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2'}},{tag:'line',attrs:{x1:10,y1:11,x2:10,y2:17}},{tag:'line',attrs:{x1:14,y1:11,x2:14,y2:17}}]);
const Eye = createIcon([{tag:'path',attrs:{d:'M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z'}},{tag:'circle',attrs:{cx:12,cy:12,r:3}}]);
const Download = createIcon([{tag:'path',attrs:{d:'M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4'}},{tag:'polyline',attrs:{points:'7 10 12 15 17 10'}},{tag:'line',attrs:{x1:12,y1:15,x2:12,y2:3}}]);
const Send = createIcon([{tag:'line',attrs:{x1:22,y1:2,x2:11,y2:13}},{tag:'polygon',attrs:{points:'22 2 15 22 11 13 2 9 22 2'}}]);
const Info = createIcon([{tag:'circle',attrs:{cx:12,cy:12,r:10}},{tag:'line',attrs:{x1:12,y1:16,x2:12,y2:12}},{tag:'line',attrs:{x1:12,y1:8,x2:12.01,y2:8}}]);
const Monitor = createIcon([{tag:'rect',attrs:{width:20,height:14,x:2,y:3,rx:2,ry:2}},{tag:'line',attrs:{x1:8,y1:21,x2:16,y2:21}},{tag:'line',attrs:{x1:12,y1:17,x2:12,y2:21}}]);
const Smartphone = createIcon([{tag:'rect',attrs:{width:14,height:20,x:5,y:2,rx:2,ry:2}},{tag:'line',attrs:{x1:12,y1:18,x2:12.01,y2:18}}]);
const Laptop = createIcon(['M20 16V7a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v9m16 0H4m16 0 1.28 2.55a1 1 0 0 1-.9 1.45H3.62a1 1 0 0 1-.9-1.45L4 16']);
const Calendar = createIcon([{tag:'rect',attrs:{width:18,height:18,x:3,y:4,rx:2,ry:2}},{tag:'line',attrs:{x1:16,y1:2,x2:16,y2:6}},{tag:'line',attrs:{x1:8,y1:2,x2:8,y2:6}},{tag:'line',attrs:{x1:3,y1:10,x2:21,y2:10}}]);
const BarChart3 = createIcon([{tag:'path',attrs:{d:'M3 3v18h18'}},{tag:'path',attrs:{d:'M18 17V9'}},{tag:'path',attrs:{d:'M13 17V5'}},{tag:'path',attrs:{d:'M8 17v-3'}}]);
const TrendingUp = createIcon([{tag:'polyline',attrs:{points:'23 6 13.5 15.5 8.5 10.5 1 18'}},{tag:'polyline',attrs:{points:'17 6 23 6 23 12'}}]);
const DollarSign = createIcon([{tag:'line',attrs:{x1:12,y1:1,x2:12,y2:23}},{tag:'path',attrs:{d:'M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6'}}]);
const Shield = createIcon(['M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z']);
const Camera = createIcon([{tag:'path',attrs:{d:'M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z'}},{tag:'circle',attrs:{cx:12,cy:13,r:3}}]);
const Check = createIcon([{tag:'polyline',attrs:{points:'20 6 9 17 4 12'}}]);
const AlertCircle = createIcon([{tag:'circle',attrs:{cx:12,cy:12,r:10}},{tag:'line',attrs:{x1:12,y1:8,x2:12,y2:12}},{tag:'line',attrs:{x1:12,y1:16,x2:12.01,y2:16}}]);
const RefreshCw = createIcon([{tag:'polyline',attrs:{points:'23 4 23 10 17 10'}},{tag:'polyline',attrs:{points:'1 20 1 14 7 14'}},{tag:'path',attrs:{d:'M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15'}}]);
const Archive = createIcon([{tag:'polyline',attrs:{points:'21 8 21 21 3 21 3 8'}},{tag:'rect',attrs:{width:23,height:5,x:.5,y:3,rx:1}},{tag:'line',attrs:{x1:10,y1:12,x2:14,y2:12}}]);
const UserPlus = createIcon([{tag:'path',attrs:{d:'M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2'}},{tag:'circle',attrs:{cx:8.5,cy:7,r:4}},{tag:'line',attrs:{x1:20,y1:8,x2:20,y2:14}},{tag:'line',attrs:{x1:23,y1:11,x2:17,y2:11}}]);
const QrCode = createIcon([{tag:'rect',attrs:{width:5,height:5,x:3,y:3,rx:1}},{tag:'rect',attrs:{width:5,height:5,x:16,y:3,rx:1}},{tag:'rect',attrs:{width:5,height:5,x:3,y:16,rx:1}},{tag:'path',attrs:{d:'M21 16h-3a2 2 0 0 0-2 2v3'}},{tag:'path',attrs:{d:'M21 21v.01'}},{tag:'path',attrs:{d:'M12 7v3a2 2 0 0 1-2 2H7'}},{tag:'path',attrs:{d:'M3 12h.01'}},{tag:'path',attrs:{d:'M12 3h.01'}},{tag:'path',attrs:{d:'M12 16v.01'}},{tag:'path',attrs:{d:'M16 12h1'}},{tag:'path',attrs:{d:'M21 12v.01'}},{tag:'path',attrs:{d:'M12 21v-1'}}]);
const Wrench = createIcon(['M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z']);
const HardDrive = createIcon([{tag:'line',attrs:{x1:22,y1:12,x2:2,y2:12}},{tag:'path',attrs:{d:'M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z'}},{tag:'line',attrs:{x1:6,y1:16,x2:6.01,y2:16}},{tag:'line',attrs:{x1:10,y1:16,x2:10.01,y2:16}}]);
const Phone = createIcon([{tag:'path',attrs:{d:'M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z'}}]);
const Tablet = createIcon([{tag:'rect',attrs:{width:16,height:20,x:4,y:2,rx:2,ry:2}},{tag:'line',attrs:{x1:12,y1:18,x2:12.01,y2:18}}]);
const Printer = createIcon([{tag:'polyline',attrs:{points:'6 9 6 2 18 2 18 9'}},{tag:'path',attrs:{d:'M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2'}},{tag:'rect',attrs:{width:12,height:8,x:6,y:14}}]);
```
