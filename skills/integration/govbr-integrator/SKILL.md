---
name: govbr-integrator
description: Integração Gov.br (Login Único + APIs Conecta)
---

Integração com o ecossistema Gov.br: Login Único (OAuth 2.0/OpenID Connect), APIs do Conecta Gov.br e princípio "once-only".

## Contexto

- 166 milhões de usuários no Gov.br (2025)
- Contas Ouro (biometria) superaram Bronze pela primeira vez
- Conecta Gov.br: 1,1 bilhão de transações de dados em 2025
- Princípio: "Não pedir ao cidadão dado que o governo já tem" (Lei 13.726/2018)

## Login Único (OAuth 2.0 / OpenID Connect)

### Fluxo de Autenticação
```
Cidadão → Tá na Mão → Redireciona Gov.br → Login → Callback → Token → Dados
```

### 1. Registro da Aplicação
```
Portal: https://acesso.gov.br/roteiro-tecnico/
Tipo: Web Application
Redirect URI: https://api.tanamao.com.br/auth/callback
Scopes: openid profile email govbr_confiabilidades
```

### 2. Iniciar Login
```python
# backend/app/routers/auth.py
from authlib.integrations.starlette_client import OAuth

oauth = OAuth()
oauth.register(
    name="govbr",
    client_id=settings.GOVBR_CLIENT_ID,
    client_secret=settings.GOVBR_CLIENT_SECRET,
    server_metadata_url="https://sso.acesso.gov.br/.well-known/openid-configuration",
    client_kwargs={"scope": "openid profile email govbr_confiabilidades"},
)

@router.get("/auth/login")
async def login(request: Request):
    redirect_uri = request.url_for("auth_callback")
    return await oauth.govbr.authorize_redirect(request, redirect_uri)
```

### 3. Callback e Token
```python
@router.get("/auth/callback")
async def auth_callback(request: Request):
    token = await oauth.govbr.authorize_access_token(request)
    userinfo = token.get("userinfo", {})

    # Dados retornados pelo Gov.br
    cpf = userinfo.get("sub")  # CPF é o "sub" no Gov.br
    nome = userinfo.get("name")
    email = userinfo.get("email")
    phone = userinfo.get("phone_number")
    nivel = userinfo.get("govbr_confiabilidades")  # bronze/prata/ouro

    # Criar ou atualizar sessão
    session = await create_session(cpf=cpf, nome=nome, nivel=nivel)
    return RedirectResponse(url=f"/dashboard?session={session.id}")
```

### 4. Níveis de Confiabilidade
```python
class NivelGovBr(str, Enum):
    BRONZE = "bronze"   # Cadastro básico (CPF + validação facial)
    PRATA = "prata"     # Validação com banco ou biometria DENATRAN
    OURO = "ouro"       # Biometria TSE ou certificado digital

# Funcionalidades por nível
PERMISSOES_POR_NIVEL = {
    NivelGovBr.BRONZE: ["consultar_beneficios", "ver_checklist", "buscar_cras"],
    NivelGovBr.PRATA: ["consultar_cadunico", "gerar_carta", "pedir_medicamento"],
    NivelGovBr.OURO: ["assinar_documento", "atualizar_cadastro", "portabilidade"],
}
```

## APIs Conecta Gov.br

### Catálogo de APIs Disponíveis
```
Base URL: https://api.conectagov.estaleiro.serpro.gov.br

APIs relevantes:
├── /api-cadunico-servicos/v1/        → CadÚnico (situação cadastral)
├── /api-cadunico-servicos-dados/v1/  → CadÚnico (dados familiares)
├── /api-cpf-light/v2/               → Validação CPF (nome, nascimento)
├── /api-cep/v1/                     → Consulta CEP
└── /api-cnpj/v2/                    → Consulta CNPJ (cooperativas)
```

### Autenticação nas APIs
```python
# backend/app/services/conecta_govbr.py
import httpx

class ConectaGovBrService:
    def __init__(self):
        self.base_url = settings.CONECTA_GOVBR_URL
        self.client_id = settings.CONECTA_GOVBR_CLIENT_ID
        self.client_secret = settings.CONECTA_GOVBR_CLIENT_SECRET
        self._token = None
        self._token_expires = None

    async def _get_token(self) -> str:
        """Obtém ou renova token OAuth2 client_credentials."""
        if self._token and datetime.now() < self._token_expires:
            return self._token

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/oauth2/jwt-token",
                data={"grant_type": "client_credentials"},
                auth=(self.client_id, self.client_secret),
            )
            data = response.json()
            self._token = data["access_token"]
            self._token_expires = datetime.now() + timedelta(seconds=data["expires_in"] - 60)
            return self._token

    async def get(self, endpoint: str, params: dict = None) -> dict:
        """GET autenticado em qualquer API do Conecta."""
        token = await self._get_token()
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}{endpoint}",
                headers={"Authorization": f"Bearer {token}"},
                params=params,
            )
            response.raise_for_status()
            return response.json()
```

## Princípio "Once-Only"

### Auto-preenchimento de Formulários
```python
async def auto_preencher_perfil(cpf: str, token_govbr: str) -> dict:
    """
    Preenche automaticamente dados do cidadão usando APIs Gov.br.
    Cidadão não precisa digitar o que o governo já sabe.
    """
    conecta = ConectaGovBrService()

    # CPF → nome, data nascimento
    dados_cpf = await conecta.get(f"/api-cpf-light/v2/{cpf}")

    # CadÚnico → renda, composição familiar
    dados_cadunico = await conecta.get(
        f"/api-cadunico-servicos-dados/v1/dp/dadosFamiliar/{cpf}"
    )

    return {
        "nome": dados_cpf.get("nome"),
        "nascimento": dados_cpf.get("nascimento"),
        "renda_per_capita": dados_cadunico.get("rendaFamiliarPerCapita"),
        "membros_familia": dados_cadunico.get("quantidadeMembros"),
        "municipio": dados_cadunico.get("municipio"),
        "uf": dados_cadunico.get("uf"),
        "fonte": "govbr_conecta",
    }
```

## Variáveis de Ambiente
```bash
# .env
GOVBR_CLIENT_ID=seu_client_id_login_unico
GOVBR_CLIENT_SECRET=seu_client_secret_login_unico
GOVBR_REDIRECT_URI=https://api.tanamao.com.br/auth/callback
CONECTA_GOVBR_URL=https://api.conectagov.estaleiro.serpro.gov.br
CONECTA_GOVBR_CLIENT_ID=seu_client_id_conecta
CONECTA_GOVBR_CLIENT_SECRET=seu_client_secret_conecta
```

## Arquivos Relacionados
- `backend/app/routers/auth.py` - Rotas de autenticação
- `backend/app/services/conecta_govbr.py` - Serviço Conecta Gov.br
- `backend/app/core/config.py` - Configurações
- `backend/app/models/user.py` - Modelo de usuário

## Segurança
- Tokens Gov.br NUNCA em logs
- Sessão com TTL curto (Redis)
- PKCE obrigatório para fluxo mobile
- Validar `state` parameter contra CSRF
- Nível mínimo Bronze para qualquer operação

## Referências
- Roteiro de Integração: https://acesso.gov.br/roteiro-tecnico/
- Catálogo APIs: https://www.gov.br/conecta/catalogo/
- OpenID Configuration: https://sso.acesso.gov.br/.well-known/openid-configuration
