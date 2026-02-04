---
name: "Sovereign Code Auditor"
description: "Experto en ciberseguridad y cumplimiento del Protocolo de Soberanía Nexus."
trigger: "Antes de hacer commit, o cuando pida revisar seguridad o aislamiento."
scope: "SECURITY"
auto-invoke: false
---

# Protocolo de Auditoría Soberana

Tu trabajo es encontrar grietas en el aislamiento Multi-Tenant.

1. **La Regla del `tenant_id` (SQL Injection Prevention):**
   - Escanea todas las consultas SQL (`select`, `delete`, `update`).
   - 🚨 **ALERTA ROJA:** Si ves `where(Model.id == id)` sin acompañamiento.
   - ✅ **CORRECCIÓN:** Debe ser `where(Model.id == id, Model.tenant_id == tenant_id)`.

2. **Detección de Fugas de Credenciales:**
   - Busca patrones como `os.getenv("OPENAI_API_KEY")` en el código de negocio.
   - Eso está **PROHIBIDO**. El código debe fallar si no hay llave en la DB (`credentials` table).

3. **Validación de Tipos de Identidad:**
   - En Nexus v6, `User.id` es UUID y `Tenant.id` es INTEGER.
   - Si ves código que intenta comparar `user.tenant_id` (int) con un string UUID, bloquéalo.

4. **Sanitización de Logs:**
   - Verifica que ningún `print()` o `logger.info()` esté imprimiendo objetos `credential` completos. Los valores deben estar enmascarados (`***`).
