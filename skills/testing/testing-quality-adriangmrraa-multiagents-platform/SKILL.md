---
name: "Nexus QA Engineer"
description: "Especialista en Pytest Asyncio y Vitest para arquitecturas aisladas."
trigger: "Cuando pida crear tests, probar una feature o corregir bugs."
scope: "QA"
auto-invoke: true
---

# Estándar de Testing Nexus

1. **Backend Tests (Pytest Asyncio):**
   - **Mocking de Bóveda:** Nunca uses credenciales reales. Mockea `app.core.credentials.get_decrypted_credential` para devolver una fake key `sk-test-123`.
   - **Database Fixtures:** Usa `conftest.py` para crear un `tenant` de prueba y un `user` de prueba al inicio de la sesión.
   - **Isolation:** Cada test debe limpiar sus datos o usar transacciones rollback.

2. **Frontend Tests (Vitest/RTL):**
   - **Mocking de useApi:** Los componentes nunca deben llamar al fetch real.
   - Testea que el componente maneje correctamente los estados de error `403 Forbidden` (Soberanía denegada).

3. **Regla de "No Flakiness":**
   - Si un test depende de `Redis`, asegúrate de que el contenedor de prueba esté levantado o mockeado.
