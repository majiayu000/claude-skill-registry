---
name: mcp-expose
description: Expose un module existant via MCP en generant automatiquement un MCP server Edge Function. Supporte deux modes — wrapper Edge Function existante OU CRUD direct PostgREST sur tables. Auth dual (OAuth + API key). Utiliser quand on dit "expose le module X par MCP", "creer un MCP pour le module Y", "mcp-expose", ou quand on veut rendre un module accessible aux agents.
license: MIT
metadata:
  author: somtech-pack
  version: "1.1.0"
  project: generic
---

# MCP Expose — Generer un MCP Server pour un Module

Ce skill genere un **MCP server Edge Function** qui expose un module Somtech via MCP. Il supporte deux modes :

- **Mode Edge Function** : wrappe une Edge Function API existante
- **Mode PostgREST** : genere un CRUD direct sur les tables du module via le client Supabase

Le MCP server supporte l'auth dual (OAuth prefere, API key en fallback) et est consommable par Claude Code, Claude Cowork, et les agents SDK Anthropic.

## Pre-requis

- Un projet avec Supabase configure
- (Optionnel) Table `external_api_keys` pour le support API key — voir `references/AUTH_PATTERNS.md`

## Workflow

### Etape 1 : Identifier le module et le mode

Demander a l'utilisateur quel module exposer. Determiner le mode automatiquement :

```bash
# Verifier si une Edge Function existe
ls supabase/functions/{module}/index.ts 2>/dev/null
```

| Situation | Mode |
|-----------|------|
| `supabase/functions/{module}/index.ts` existe | **Edge Function** — wrapper |
| Pas d'Edge Function, tables connues | **PostgREST** — CRUD direct |
| Pas d'Edge Function, tables inconnues | **PostgREST** — detecter via schema DB |

### Etape 2A : Analyser les endpoints (mode Edge Function)

Lire le code source de `supabase/functions/{module}/index.ts` et detecter les routes/operations :

**Patterns a chercher :**

1. **Routing par methode HTTP** :
   - `req.method === "GET"` / `"POST"` / `"PATCH"` / `"PUT"` / `"DELETE"`
   - `switch` / `if` sur la methode ou le path

2. **Operations Supabase** :
   - `.from("table").select(...)` → operation list ou get
   - `.from("table").insert(...)` → operation create
   - `.from("table").update(...)` → operation update
   - `.from("table").delete()` → operation delete
   - `.eq("id", ...)` → operation sur un element (get/update/delete)

3. **Parametres** :
   - `url.searchParams.get("...")` → parametres de filtre (list)
   - `await req.json()` → body (create/update)
   - Path segments → id (get/update/delete)

**Mapping :**

| Pattern | Tool MCP | Schema |
|---------|----------|--------|
| select() sans .eq('id') | `app_{module_plural}_list` | filtres optionnels + limit/offset |
| select().eq('id') | `app_{module_singular}_get` | id requis |
| insert() | `app_{module_singular}_create` | champs du body |
| update().eq('id') | `app_{module_singular}_update` | id requis + champs |
| delete().eq('id') | `app_{module_singular}_delete` | id requis |
| autre logique | `app_{module}_{action}` | a determiner |

**Fallback** : si la detection automatique ne trouve rien (code non standard, logique repartie), demander a l'utilisateur de lister les operations a exposer manuellement.

### Etape 2B : Detecter le schema (mode PostgREST)

Recuperer les informations des tables du module. Utiliser une de ces methodes (par ordre de preference) :

**Methode 1 — Via le MCP Supabase du projet** (si configure dans `.mcp.json` ou `.cursor/mcp.json`) :

Utiliser l'outil MCP Supabase `execute_sql` pour querier le schema :

```sql
SELECT
  c.table_name,
  c.column_name,
  c.data_type,
  c.is_nullable,
  c.column_default,
  tc.constraint_type,
  ccu.table_name AS foreign_table
FROM information_schema.columns c
LEFT JOIN information_schema.key_column_usage kcu
  ON c.table_name = kcu.table_name AND c.column_name = kcu.column_name
LEFT JOIN information_schema.table_constraints tc
  ON kcu.constraint_name = tc.constraint_name AND tc.constraint_type = 'FOREIGN KEY'
LEFT JOIN information_schema.constraint_column_usage ccu
  ON tc.constraint_name = ccu.constraint_name
WHERE c.table_schema = 'public'
  AND c.table_name IN ('table1', 'table2')
ORDER BY c.table_name, c.ordinal_position;
```

**Methode 2 — Via les types TypeScript generes** :

Lire le fichier de types genere par `supabase gen types typescript` (souvent `src/types/supabase.ts` ou `types/database.ts`). Chercher les interfaces `Tables` pour extraire les colonnes et types.

**Methode 3 — Demander a l'utilisateur** :

Si aucune des methodes precedentes n'est disponible, demander :
- Quelles tables exposer
- Pour chaque table : quelles colonnes sont filtrables, quels champs sont requis en creation

**Pour chaque table detectee, generer les tools CRUD :**

| Tool | Description | inputSchema |
|------|-------------|-------------|
| `app_{table_plural}_list` | Liste avec filtres | colonnes filtrables + limit/offset |
| `app_{table_singular}_get` | Recupere par ID | id requis |
| `app_{table_singular}_create` | Cree un enregistrement | colonnes sans default/auto (id, created_at exclus) |
| `app_{table_singular}_update` | Met a jour par ID | id requis + colonnes modifiables |
| `app_{table_singular}_delete` | Supprime par ID | id requis |

**Colonnes a exclure du create/update** :
- `id` (auto-genere)
- `created_at`, `updated_at` (auto-generes)
- `created_by`, `updated_by` (auto-generes si RLS)

**Colonnes filtrables pour list** :
- Toutes les colonnes FK (`*_id`) → filtre exact `.eq()`
- Colonnes `text` → filtre recherche `.ilike()`
- Colonnes `enum`/`status` → filtre exact `.eq()`
- Toujours inclure `limit` (default 50) et `offset` (default 0)

### Etape 3 : Generer le MCP server

1. **Executer le script de generation** :

```bash
# Mode Edge Function (auto-detecte)
./scripts/mcp-expose.sh {module}

# Mode PostgREST avec tables specifiees
./scripts/mcp-expose.sh {module} --tables table1,table2
```

Ce script :
- Detecte le mode automatiquement
- Copie `mcp-core/` dans `_shared/` si absent (avec gestion de version)
- Cree `supabase/functions/{module}-mcp/index.ts` (squelette adapte au mode)
- Declare dans `supabase/config.toml`

2. **Remplir le squelette** avec les tools detectes :

Utiliser le template dans `references/TEMPLATE_MCP_WRAPPER.md` comme guide.

**Convention de nommage** :
- List : pluriel (`app_contacts_list`)
- CRUD unitaire : singulier (`app_contact_get`, `app_contact_create`)
- Custom : descriptif (`app_devis_generate_pdf`)

**Contexte disponible dans runTool** :
```typescript
ctx: {
  accessToken: string;   // JWT OAuth ou "api_key"
  userId: string;        // UUID user ou "api_key:{id}"
  clientId?: string;     // OAuth client_id ou "api_key:{id}"
  supabase: SupabaseClient; // User-bound (OAuth) ou service-role (API key)
}
```

Le `supabase` client est automatiquement configure selon le mode d'auth :
- **OAuth** : `createUserSupabaseClient(accessToken)` — RLS actif, filtrage automatique
- **API key** : `createServiceSupabaseClient()` — service-role, pas de RLS

**Important** : le `runTool` doit retourner les donnees brutes (pas de wrapping `{ content: [...] }`). Le handler `edgeMcpHandler.ts` wrappe automatiquement en format MCP.

**Exemple de tool CRUD PostgREST genere :**

```typescript
case "app_devis_list": {
  let query = supabase.from("devis").select("*, client:entreprises(nom)");
  if (args.client_id) query = query.eq("client_id", args.client_id);
  if (args.statut) query = query.eq("statut", args.statut);
  if (args.search) query = query.ilike("titre", `%${args.search}%`);
  query = query.order("created_at", { ascending: false });
  const { data, error } = await query.range(args.offset ?? 0, (args.offset ?? 0) + (args.limit ?? 50) - 1);
  if (error) throw error;
  return data;
}

case "app_devis_get": {
  const { data, error } = await supabase
    .from("devis")
    .select("*, lignes:ligne_devis(*), client:entreprises(nom, email)")
    .eq("id", args.id)
    .single();
  if (error) throw error;
  return data;
}

case "app_devis_create": {
  const { data, error } = await supabase
    .from("devis")
    .insert({ titre: args.titre, client_id: args.client_id, montant: args.montant })
    .select()
    .single();
  if (error) throw error;
  return data;
}
```

### Etape 4 : Valider

1. **Verification syntaxique** : s'assurer que le code genere est du TypeScript valide

2. **Tester localement** (si Supabase local tourne) :

```bash
# Health check
curl http://127.0.0.1:54321/functions/v1/{module}-mcp/health

# Tools listing (avec auth)
curl -X POST http://127.0.0.1:54321/functions/v1/{module}-mcp \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'
```

3. **Verifier config.toml** : s'assurer que le bloc `[functions.{module}-mcp]` est present avec `verify_jwt = false`

### Etape 5 : Informer l'utilisateur

Afficher un resume :
- Mode utilise (Edge Function ou PostgREST)
- Fichiers generes
- Tools MCP crees (avec liste)
- Tables exposees (mode PostgREST)
- Prochaines etapes (deploiement, configuration client via `configure-mcp-server`)

## References

- Template : `references/TEMPLATE_MCP_WRAPPER.md`
- Auth : `references/AUTH_PATTERNS.md`
- Lib : `lib/mcp-core/` (source de verite pour les fichiers runtime)
