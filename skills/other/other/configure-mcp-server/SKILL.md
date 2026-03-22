---
name: configure-mcp-server
description: Configure un serveur MCP (Model Context Protocol) dans Cursor en ajoutant l'entrée appropriée dans le fichier mcp.json. Supporte les serveurs Supabase Edge Functions, n8n et les serveurs locaux via npx. Utilise ce skill lorsque l'utilisateur demande d'ajouter, modifier ou configurer un serveur MCP dans Cursor.
license: MIT
metadata:
  author: somtech-pack
  version: "1.2.0"
  project: generic
---

# Configuration d'un Serveur MCP dans Cursor

Ce skill guide la configuration d'un serveur MCP (Model Context Protocol) dans Cursor pour permettre à l'agent d'accéder à des outils et ressources externes.

## Quand utiliser ce skill

Utilisez ce skill lorsque :
- L'utilisateur demande d'ajouter un nouveau serveur MCP (Supabase Edge Functions)
- Il faut configurer un serveur MCP Supabase Edge Function
- Il faut configurer un serveur MCP n8n
- Il faut configurer un serveur MCP local via npx (pour développement)
- Il faut modifier une configuration MCP existante
- Il faut vérifier ou corriger une configuration MCP

⚠️ **Note** : Adaptez les URLs, noms de serveurs et tokens à votre environnement. Les exemples Supabase ci-dessous utilisent `votre-project-id` comme placeholder.

## Emplacement du fichier de configuration

Le fichier de configuration MCP pour Cursor se trouve à :
- **Linux/Mac** : `~/.cursor/mcp.json`
- **Windows** : `%APPDATA%\Cursor\mcp.json`
- **Gitpod** : `~/.cursor/mcp.json` (peut aussi utiliser `.cursor/mcp.json.gitpod` comme référence)

⚠️ **Important** : Le fichier `mcp.json` peut contenir des tokens secrets. Ne jamais le commiter dans Git avec des secrets. Utiliser `.gitignore` si nécessaire.

## Types de serveurs MCP supportés

### 1. Supabase Edge Functions ⭐ (Méthode principale recommandée)

Les serveurs MCP peuvent être déployés sur Supabase Edge Functions. Chaque domaine peut posséder sa propre Edge Function.

**Structure de base** :
```json
{
  "mcpServers": {
    "nom-serveur": {
      "url": "https://votre-project-id.supabase.co/functions/v1/{module}-mcp/mcp"
    }
  }
}
```

**Exemples de serveurs** (adaptez selon votre projet) :
- `{domaine}-mcp` : domaine métier (ex: `contacts-mcp`, `documents-mcp`)
- `docs-reader` : lecture de documentation (si applicable)

**URL complète** : `https://votre-project-id.supabase.co/functions/v1/{module}-mcp/mcp`

**Pour Agent Builder** : Utiliser l'endpoint `/sse` au lieu de `/mcp` :
- URL : `https://votre-project-id.supabase.co/functions/v1/{module}-mcp/sse`
- Auth : Header `Authorization: Bearer <JWT>` + `apikey: <SUPABASE_ANON_KEY>`

**Exemple complet** :
```json
{
  "mcpServers": {
    "contacts": {
      "url": "https://votre-project-id.supabase.co/functions/v1/contacts-mcp/mcp"
    },
    "documents": {
      "url": "https://votre-project-id.supabase.co/functions/v1/documents-mcp/mcp"
    }
  }
}
```

### 2. n8n MCP

n8n expose un serveur MCP pour permettre aux clients MCP d'exécuter des workflows n8n.

**Configuration** :
```json
{
  "mcpServers": {
    "n8n": {
      "type": "streamable-http",
      "url": "https://votre-instance-n8n.up.railway.app/mcp-server/http",
      "headers": {
        "Authorization": "Bearer YOUR_N8N_MCP_ACCESS_TOKEN"
      }
    }
  }
}
```

**Prérequis** :
1. Activer l'accès MCP au niveau de l'instance n8n (Settings > MCP Access)
2. Obtenir le MCP Access Token (Settings > MCP Access > Access Token)
3. Activer chaque workflow pour MCP (dans l'éditeur de workflow)

### 3. Serveur local via npx (pour développement)

Pour les serveurs MCP disponibles via npm/npx, principalement pour le développement local ou des outils externes.

Pour tout serveur MCP disponible via npm/npx :

```json
{
  "mcpServers": {
    "nom-serveur": {
      "command": "npx",
      "args": ["-y", "@package/nom-package"],
      "env": {
        "VARIABLE_ENV": "valeur"
      }
    }
  }
}
```

**Exemple : Supabase MCP local** :
```json
{
  "mcpServers": {
    "supabase-project": {
      "command": "npx",
      "args": [
        "-y",
        "@supabase/mcp-server-supabase@latest",
        "--project-ref=votre-project-id"
      ],
      "env": {
        "SUPABASE_ACCESS_TOKEN": "sbp_..."
      }
    }
  }
}
```

### 4. Railway MCP (optionnel)

Railway fournit un serveur MCP officiel pour gérer des déploiements depuis Cursor. Utilisez-le uniquement si votre projet utilise Railway.

**Configuration Railway (pour autres services)** :
```json
{
  "mcpServers": {
    "railway": {
      "type": "streamable-http",
      "url": "https://railway-mcp.railway.app/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_RAILWAY_TOKEN"
      }
    }
  }
}
```

## Processus de configuration

### Étape 1 : Identifier le type de serveur

Déterminer le type de serveur MCP à configurer :
- **Supabase Edge Function** ⭐ : Méthode principale recommandée
- **n8n** : Pour exécuter des workflows n8n
- **Local npx** : Pour les serveurs MCP disponibles via npm (développement)
- **Railway** : Pour gérer des services Railway (optionnel)

### Étape 2 : Localiser le fichier mcp.json

1. Vérifier si `~/.cursor/mcp.json` existe
2. Si le fichier n'existe pas, le créer avec une structure de base :
   ```json
   {
     "mcpServers": {}
   }
   ```

### Étape 3 : Ajouter ou modifier l'entrée

1. Lire le fichier `mcp.json` existant
2. Ajouter ou modifier l'entrée dans `mcpServers` selon le type de serveur
3. Utiliser un nom de serveur descriptif (ex: `contacts`, `documents`, `railway`)
4. Respecter la structure JSON valide

### Étape 4 : Gérer les secrets

⚠️ **Sécurité** :
- Ne jamais commiter `mcp.json` avec des tokens dans Git
- Utiliser des variables d'environnement quand possible
- Ajouter `mcp.json` à `.gitignore` si nécessaire
- Pour Gitpod, utiliser `.cursor/mcp.json.gitpod` comme référence (sans secrets)

### Étape 5 : Redémarrer Cursor

Après modification de `mcp.json` :
1. **Redémarrer Cursor complètement** (fermer et rouvrir)
2. Ou utiliser la palette de commandes : `Cmd+Shift+P` > "MCP: Restart Server"
3. Vérifier les logs : `Cmd+Shift+P` > "MCP: Show Server Logs"

## Exemples de configurations complètes

### Configuration complète (Supabase Edge Functions) ⭐ Recommandé

```json
{
  "mcpServers": {
    "contacts": {
      "url": "https://votre-project-id.supabase.co/functions/v1/contacts-mcp/mcp"
    },
    "documents": {
      "url": "https://votre-project-id.supabase.co/functions/v1/documents-mcp/mcp"
    },
    "api": {
      "url": "https://votre-project-id.supabase.co/functions/v1/api-mcp/mcp"
    }
  }
}
```

### Configuration mixte (Supabase + n8n)

```json
{
  "mcpServers": {
    "contacts": {
      "url": "https://votre-project-id.supabase.co/functions/v1/contacts-mcp/mcp"
    },
    "documents": {
      "url": "https://votre-project-id.supabase.co/functions/v1/documents-mcp/mcp"
    },
    "n8n": {
      "type": "streamable-http",
      "url": "https://votre-instance-n8n.up.railway.app/mcp-server/http",
      "headers": {
        "Authorization": "Bearer YOUR_N8N_MCP_ACCESS_TOKEN"
      }
    }
  }
}
```

## Vérification et dépannage

### Vérifier que le serveur fonctionne

1. **Redémarrer Cursor** après modification
2. **Vérifier les logs** : `Cmd+Shift+P` > "MCP: Show Server Logs"
3. **Tester les outils** : Demander à l'agent de lister les outils disponibles
4. **Vérifier les erreurs** : Chercher les erreurs de connexion dans les logs

### Problèmes courants

**Le serveur ne démarre pas** :
- Vérifier que le JSON est valide (utiliser un validateur JSON)
- Vérifier que les URLs sont correctes
- Vérifier que les tokens sont valides (pour Railway/n8n)
- Vérifier que les variables d'environnement sont définies (pour npx)

**Token invalide** :
- Régénérer le token sur la plateforme (Railway/n8n)
- Mettre à jour le token dans `mcp.json`
- Redémarrer Cursor

**Serveur non trouvé** :
- Vérifier que l'URL est correcte
- Vérifier que le serveur est déployé et accessible
- Tester l'URL avec `curl` ou un navigateur

**Erreur de connexion** :
- Vérifier les headers d'authentification
- Vérifier que le serveur accepte les connexions depuis Cursor
- Consulter les logs du serveur (Supabase/Railway)

## Références

- Exemple Orbit (optionnel) : `references/SERVEURS_ORBIT.md`

- [Documentation MCP officielle](https://modelcontextprotocol.io)
- [Documentation Cursor Skills](https://cursor.com/docs/context/skills)
- [Documentation Supabase Edge Functions](https://supabase.com/docs/guides/functions)
- [Documentation Railway MCP](https://github.com/railwayapp/railway-mcp-server)
- [Documentation n8n MCP](https://docs.n8n.io/advanced-ai/accessing-n8n-mcp-server/)
- Documentation projet : adaptez selon votre repo (ex: `docs/mcp/`, `docs/deployment/`)

## Notes d’adaptation (structure type)

- **Architecture modulaire** : chaque domaine peut exposer son propre serveur MCP
- **Déploiement** : Supabase Edge Functions est une option courante, mais adaptez selon votre plateforme
- **Code partagé** : si vous avez un core partagé, adaptez les chemins (ex: `supabase/functions/_shared/mcp-core/`)
- **Catalogue UI** : si vous avez une UI d’admin, adaptez les chemins (ex: `src/components/admin/AdminMCP.tsx`)
- **Agent Builder** : utiliser l’endpoint `/sse` pour compatibilité Agent Builder
- **OAuth** : Supabase Edge Functions s’appuie souvent sur OAuth/Bearer tokens (selon votre implémentation)
