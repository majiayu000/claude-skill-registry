---
name: commit
description: Usar al preparar cualquier commit. Genera mensaje siguiendo Conventional Commits.
---

## Cuándo usar esta skill

- Al finalizar una tarea y preparar el commit
- Cuando el usuario pida "commitear" o "preparar commit"
- Después de que todas las validaciones pasen

## Contexto necesario antes de empezar

1. Verificar que `ruff check .` pasa
2. Verificar que `ruff format --check .` pasa
3. Listar archivos modificados con `git status`
4. Entender qué cambio se hizo y por qué

## Pasos

1. **Ejecutar validaciones**
   ```bash
   ruff check .
   ruff format --check .
   python -c "from app import app"
   ```

2. **Revisar cambios**
   ```bash
   git status
   git diff --stat
   ```

3. **Determinar tipo de commit**
   - `feat`: Nueva funcionalidad
   - `fix`: Corrección de bug
   - `docs`: Solo documentación
   - `style`: Formato sin cambio de lógica
   - `refactor`: Refactorización
   - `test`: Tests
   - `chore`: Mantenimiento

4. **Determinar scope** (basado en archivos tocados)
   - `api`: blueprints/main.py
   - `energy`, `pihole`, `mealie`, `settleup`: clientes específicos
   - `ui`: templates/, static/css/
   - `js`: static/js/
   - `config`: config.py, .env
   - `deps`: requirements.txt

5. **Generar mensaje**
   ```
   <tipo>(<scope>): <descripción imperativa max 72 chars>
   
   [cuerpo opcional explicando el qué y por qué]
   ```

<patrones_criticos>
SIEMPRE:
- Descripción en imperativo ("añadir", no "añadido")
- Máximo 72 caracteres en primera línea
- Scope en minúsculas

NUNCA:
- Punto final en la descripción
- Commits sin tipo
- Mezclar múltiples cambios no relacionados

PREFERENTEMENTE:
- Un commit por cambio lógico
- Cuerpo si el cambio no es obvio
</patrones_criticos>

## Ejemplos de commits del proyecto

```bash
feat(api): añadir endpoint /api/network para dispositivos WiFi
fix(energy): manejar estado 'unavailable' de sensores HA
refactor(pihole): extraer lógica de auth a método separado
docs(readme): actualizar instrucciones de instalación NAS
chore(deps): actualizar Flask a 3.0.3
test(api): añadir tests para endpoint /api/status
```

## Checklist de validación

- [ ] `ruff check .` pasa sin errores
- [ ] `ruff format --check .` pasa
- [ ] La app arranca correctamente
- [ ] El mensaje sigue formato Conventional Commits
- [ ] La descripción es clara y en imperativo
