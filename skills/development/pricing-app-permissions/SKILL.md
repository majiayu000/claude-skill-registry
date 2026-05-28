---
name: pricing-app-permissions
description: Hybrid permission system - role-based + user overrides, frontend/backend patterns
license: MIT
metadata:
  author: pricing-app
  version: "1.0.0"
  scope: [backend, frontend, root]
  auto_invoke:
    - "Implementing permission checks"
    - "Using PermisosContext"
    - "Checking user permissions in backend"
    - "Managing user permission overrides"
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# Pricing App - Permission System

---

## CRITICAL RULES - NON-NEGOTIABLE

### Backend Permission Checks
- ALWAYS: Check authentication first (`Depends(get_current_user)`)
- ALWAYS: Check permissions for write operations
- ALWAYS: Use `PermisosService.tiene_permiso(user, "permiso.codigo")`
- ALWAYS: Handle SUPERADMIN special case (has all permissions)
- NEVER: Skip permission checks on sensitive endpoints

### Frontend Permission Checks
- ALWAYS: Use `usePermisos()` hook from PermisosContext
- ALWAYS: Hide/disable UI elements user can't access
- ALWAYS: Check permissions on action handlers (buttons, forms)
- NEVER: Trust client-side checks alone (always validate backend)

### Permission Codes
- ALWAYS: Use namespaced format: `{resource}.{action}` (e.g., `productos.editar_precios`)
- ALWAYS: Define permissions in database (`permisos` table)
- ALWAYS: Map permissions to roles (`rol_permiso_base` table)
- NEVER: Hardcode permission strings (use constants)

### Hybrid System
- ALWAYS: Start with role-based permissions
- ALWAYS: Allow user-level overrides (`usuario_permiso_override`)
- ALWAYS: Cache permission lookups for performance
- NEVER: Modify role permissions at runtime (use overrides)

---

## TECH STACK

Backend: SQLAlchemy + FastAPI Depends | Frontend: React Context + Custom Hook

---

## ARCHITECTURE

```
┌─────────────────────────────────────────┐
│          Permission System              │
└─────────────────────────────────────────┘
                  │
        ┌─────────┴─────────┐
        │                   │
   ┌────▼────┐       ┌──────▼──────┐
   │  Roles  │       │   Permisos  │
   │  (Base) │       │   (Catalog) │
   └────┬────┘       └──────┬──────┘
        │                   │
        └─────────┬─────────┘
                  │
         ┌────────▼──────────┐
         │ RolPermisoBase    │
         │ (Role → Permiso)  │
         └────────┬──────────┘
                  │
         ┌────────▼──────────────┐
         │ Usuario               │
         │ (rol_id + overrides)  │
         └────────┬──────────────┘
                  │
         ┌────────▼──────────────────┐
         │ UsuarioPermisoOverride    │
         │ (concedido: true/false)   │
         └───────────────────────────┘
```

---

## BACKEND PATTERNS

### Permission Service

```python
from typing import Set
from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.models.permiso import Permiso, RolPermisoBase, UsuarioPermisoOverride

class PermisosService:
    """Service for permission checks"""
    
    def __init__(self, db: Session):
        self.db = db
        self._cache = {}
    
    def obtener_permisos_usuario(self, usuario: Usuario) -> Set[str]:
        """
        Get all effective permissions for user.
        Combines role permissions + user overrides.
        
        Returns:
            Set of permission codes (e.g., {"productos.ver", "ventas.crear"})
        """
        # SUPERADMIN has ALL permissions
        if usuario.es_superadmin:
            todos = self.db.query(Permiso.codigo).all()
            return {p.codigo for p in todos}
        
        # Get base role permissions
        permisos_rol = self._obtener_permisos_rol(usuario.rol_id)
        
        # Get user overrides
        overrides = self.db.query(UsuarioPermisoOverride).filter(
            UsuarioPermisoOverride.usuario_id == usuario.id
        ).all()
        
        # Apply overrides
        permisos_finales = set(permisos_rol)
        
        for override in overrides:
            permiso = self.db.query(Permiso).filter(
                Permiso.id == override.permiso_id
            ).first()
            
            if permiso:
                if override.concedido:
                    permisos_finales.add(permiso.codigo)
                else:
                    permisos_finales.discard(permiso.codigo)
        
        return permisos_finales
    
    def tiene_permiso(self, usuario: Usuario, permiso_codigo: str) -> bool:
        """
        Check if user has specific permission.
        
        Args:
            usuario: User object
            permiso_codigo: Permission code (e.g., "productos.editar_precios")
        
        Returns:
            True if user has permission
        """
        if usuario.es_superadmin:
            return True
        
        permisos = self.obtener_permisos_usuario(usuario)
        return permiso_codigo in permisos
    
    def _obtener_permisos_rol(self, rol_id: int) -> list[str]:
        """Get base permissions for role (with caching)"""
        cache_key = f"rol_{rol_id}"
        
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        permisos = self.db.query(Permiso.codigo).join(
            RolPermisoBase, RolPermisoBase.permiso_id == Permiso.id
        ).filter(
            RolPermisoBase.rol_id == rol_id
        ).all()
        
        codigos = [p.codigo for p in permisos]
        self._cache[cache_key] = codigos
        return codigos
```

### Endpoint with Permission Check

```python
from fastapi import APIRouter, Depends, HTTPException, status
from app.core.deps import get_current_user
from app.services.permisos_service import PermisosService
from app.core.database import get_db

router = APIRouter()

@router.put("/productos/{producto_id}/precio")
async def actualizar_precio(
    producto_id: int,
    nuevo_precio: int,
    current_user = Depends(get_current_user),
    db = Depends(get_db)
):
    """Update product price. Requires 'productos.editar_precios' permission."""
    
    # Check permission
    permisos_service = PermisosService(db)
    if not permisos_service.tiene_permiso(current_user, "productos.editar_precios"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para editar precios"
        )
    
    # Update price logic...
    return {"success": True}
```

---

## FRONTEND PATTERNS

### PermisosContext

```jsx
import { createContext, useContext, useState, useEffect } from 'react';
import { useAuthStore } from '@/store/authStore';

const PermisosContext = createContext();

export function PermisosProvider({ children }) {
  const { user } = useAuthStore();
  const [permisos, setPermisos] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (user) {
      // Fetch user permissions from API
      fetchPermisos(user.id);
    } else {
      setPermisos([]);
      setLoading(false);
    }
  }, [user]);

  const fetchPermisos = async (userId) => {
    try {
      const response = await api.get(`/usuarios/${userId}/permisos`);
      setPermisos(response.data.permisos);
    } catch (err) {
      console.error('Error fetching permisos:', err);
    } finally {
      setLoading(false);
    }
  };

  const tienePermiso = (codigo) => {
    // SUPERADMIN has all permissions
    if (user?.es_superadmin) return true;
    
    return permisos.includes(codigo);
  };

  const tieneAlgunPermiso = (codigos) => {
    if (user?.es_superadmin) return true;
    return codigos.some(c => permisos.includes(c));
  };

  return (
    <PermisosContext.Provider value={{ permisos, loading, tienePermiso, tieneAlgunPermiso }}>
      {children}
    </PermisosContext.Provider>
  );
}

export const usePermisos = () => useContext(PermisosContext);
```

### Component with Permission Check

```jsx
import { usePermisos } from '@/contexts/PermisosContext';

function ProductosPage() {
  const { tienePermiso } = usePermisos();

  const handleEditPrice = async (producto) => {
    if (!tienePermiso('productos.editar_precios')) {
      alert('No tienes permiso para editar precios');
      return;
    }

    // Edit price logic...
  };

  return (
    <div>
      <h1>Productos</h1>
      
      {/* Conditional rendering */}
      {tienePermiso('productos.editar_precios') && (
        <button onClick={() => handleEditPrice(producto)}>
          Editar Precio
        </button>
      )}
      
      {/* Disabled button */}
      <button 
        onClick={() => handleEditPrice(producto)}
        disabled={!tienePermiso('productos.editar_precios')}
      >
        Editar Precio
      </button>
    </div>
  );
}
```

---

## PERMISSION CODES (EXAMPLES)

```
productos.ver             - View products
productos.crear           - Create products
productos.editar          - Edit product details
productos.editar_precios  - Edit prices
productos.eliminar        - Delete products

ventas.ver                - View sales
ventas.crear              - Create sales
ventas.editar             - Edit sales
ventas.anular             - Cancel sales

config.ver                - View configuration
config.editar             - Edit configuration
config.usuarios           - Manage users
config.permisos           - Manage permissions

reportes.ver              - View reports
reportes.exportar         - Export reports
reportes.avanzados        - Access advanced reports
```

---

## DATABASE SCHEMA

```sql
-- Permission catalog
CREATE TABLE permisos (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(100) UNIQUE NOT NULL,
    descripcion VARCHAR(255),
    categoria VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Roles
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    nombre VARCHAR(100),
    descripcion TEXT
);

-- Role → Permission mapping
CREATE TABLE rol_permiso_base (
    id SERIAL PRIMARY KEY,
    rol_id INTEGER REFERENCES roles(id) ON DELETE CASCADE,
    permiso_id INTEGER REFERENCES permisos(id) ON DELETE CASCADE,
    UNIQUE(rol_id, permiso_id)
);

-- User permission overrides
CREATE TABLE usuario_permiso_override (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES tb_usuarios(id) ON DELETE CASCADE,
    permiso_id INTEGER REFERENCES permisos(id) ON DELETE CASCADE,
    concedido BOOLEAN NOT NULL,  -- true=grant, false=revoke
    UNIQUE(usuario_id, permiso_id)
);
```

---

## COMMON PITFALLS

- ❌ Don't check permissions only in frontend → Always validate backend
- ❌ Don't forget SUPERADMIN case → Always returns true
- ❌ Don't skip caching → Permission checks are expensive
- ❌ Don't hardcode permission strings → Use constants or enum
- ❌ Don't modify role permissions → Use user overrides instead
- ❌ Don't forget to refresh permissions → Logout/login or API refresh

---

## REFERENCES

- Backend service: `backend/app/services/permisos_service.py`
- Frontend context: `frontend/src/contexts/PermisosContext.jsx`
- Frontend hook: `frontend/src/hooks/usePermisos.js`
- Permission models: `backend/app/models/permiso.py`
- Role models: `backend/app/models/rol.py`
