# ☁️ Skill: Microsoft Azure Backend

## 📋 Metadata

| Atributo | Valor |
|----------|-------|
| **ID** | `cicd-azure` |
| **Nivel** | 🔴 Avanzado |
| **Versión** | 1.0.0 |
| **Keywords** | `azure`, `aks`, `azure-functions`, `cosmos-db` |

## 🔑 Keywords

- `azure`, `aks`, `azure-functions`, `cosmos-db`, `azure-sql`, `@skill:azure`

## 📖 Descripción

Azure proporciona servicios cloud para backends Flutter: AKS (Kubernetes), Azure Functions (serverless), Azure SQL, Cosmos DB, Blob Storage y más.

## 💻 Servicios Principales

### 1. AKS (Azure Kubernetes Service)

```bash
# Create resource group
az group create --name myapp-prod --location eastus

# Create AKS cluster
az aks create \
  --resource-group myapp-prod \
  --name myapp-aks \
  --node-count 3 \
  --enable-addons monitoring \
  --enable-managed-identity \
  --generate-ssh-keys

# Get credentials
az aks get-credentials --resource-group myapp-prod --name myapp-aks
```

### 2. Azure Functions (Serverless)

```javascript
// index.js
module.exports = async function (context, req) {
  context.log('Processing request');

  const name = req.query.name || (req.body && req.body.name);
  const responseMessage = name
    ? `Hello, ${name}!`
    : 'Hello from Azure Function!';

  context.res = {
    status: 200,
    body: responseMessage
  };
};
```

```bash
# Deploy function
func azure functionapp publish myapp-functions
```

### 3. Azure SQL Database

```bash
# Create SQL server
az sql server create \
  --name myapp-sql-server \
  --resource-group myapp-prod \
  --location eastus \
  --admin-user sqladmin \
  --admin-password SecurePassword123!

# Create database
az sql db create \
  --resource-group myapp-prod \
  --server myapp-sql-server \
  --name myapp_prod \
  --service-objective S0 \
  --backup-storage-redundancy Local
```

### 4. Cosmos DB (NoSQL)

```bash
# Create Cosmos DB account
az cosmosdb create \
  --name myapp-cosmos \
  --resource-group myapp-prod \
  --kind GlobalDocumentDB \
  --locations regionName=eastus failoverPriority=0

# Create database
az cosmosdb sql database create \
  --account-name myapp-cosmos \
  --resource-group myapp-prod \
  --name myapp_db
```

### 5. Azure Blob Storage

```bash
# Create storage account
az storage account create \
  --name myappstorage \
  --resource-group myapp-prod \
  --location eastus \
  --sku Standard_LRS

# Create container
az storage container create \
  --name uploads \
  --account-name myappstorage \
  --public-access blob
```

### 6. Azure Key Vault

```bash
# Create key vault
az keyvault create \
  --name myapp-keyvault \
  --resource-group myapp-prod \
  --location eastus

# Store secret
az keyvault secret set \
  --vault-name myapp-keyvault \
  --name DatabasePassword \
  --value "SecurePassword123!"

# Retrieve secret
az keyvault secret show \
  --name DatabasePassword \
  --vault-name myapp-keyvault \
  --query value -o tsv
```

## 🎯 Mejores Prácticas

1. Use **Managed Identities** para autenticación
2. **Azure Key Vault** para secrets
3. **Application Insights** para monitoring
4. **Azure Front Door** para CDN y WAF
5. **Azure DevOps** para CI/CD
6. **RBAC** para control de acceso
7. **Private Endpoints** para seguridad

## 📚 Recursos

- [Azure Documentation](https://docs.microsoft.com/azure/)
- [AKS Best Practices](https://docs.microsoft.com/azure/aks/best-practices)

---

**Versión:** 1.0.0
