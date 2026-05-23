---
name: cadunico-api
description: API CadÚnico via Conecta Gov.br para verificação de elegibilidade
---

Consumo da API oficial do CadÚnico para verificação de elegibilidade, consulta cadastral e monitoramento de saúde do cadastro.

## Contexto

- CadÚnico migrou para Dataprev em março/2025
- CPF substituiu NIS como identificador primário
- 41,6 milhões de famílias (~110 milhões de pessoas)
- 40+ programas federais usam CadÚnico como porta de entrada
- APIs disponíveis via Conecta Gov.br (1,1 bilhão de transações em 2025)

## Endpoints Principais

### Situação Cadastral (por NIS)
```
GET https://api.conectagov.estaleiro.serpro.gov.br/api-cadunico-servicos/v1/situacaoCadastral/nis/{nis}

Headers:
  Authorization: Bearer {token}
  Accept: application/json

Resposta:
{
  "nis": "12345678901",
  "situacaoCadastral": "CADASTRADO",
  "dataUltimaAtualizacao": "2024-11-15",
  "faixaRenda": "EXTREMA_POBREZA"
}
```

### Dados Familiares (por CPF)
```
GET https://api.conectagov.estaleiro.serpro.gov.br/api-cadunico-servicos-dados/v1/dp/dadosFamiliar/{cpf}

Headers:
  Authorization: Bearer {token}
  Accept: application/json

Resposta:
{
  "cpfResponsavel": "***456789**",
  "quantidadeMembros": 4,
  "rendaFamiliarPerCapita": 150.00,
  "municipio": "SAO PAULO",
  "uf": "SP",
  "dataUltimaAtualizacao": "2024-11-15"
}
```

### Autenticação (OAuth 2.0 - Conecta Gov.br)
```bash
# Obter token
curl -X POST https://h.conectagov.estaleiro.serpro.gov.br/oauth2/jwt-token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials" \
  -u "{client_id}:{client_secret}"
```

## Funcionalidades

### 1. Verificação Instantânea de Elegibilidade
```python
# backend/app/agent/tools/consultar_cadunico.py
async def consultar_cadunico(cpf: str) -> dict:
    """
    Consulta situação no CadÚnico via API Conecta Gov.br.
    Retorna: situação cadastral, faixa de renda, data última atualização.
    """
    token = await obter_token_conecta()
    response = await httpx_client.get(
        f"{CADUNICO_API_URL}/dadosFamiliar/{cpf}",
        headers={"Authorization": f"Bearer {token}"}
    )
    return response.json()
```

### 2. Monitor de Saúde Cadastral
```python
async def verificar_saude_cadastral(cpf: str) -> dict:
    """
    Verifica se cadastro precisa ser atualizado.
    CadÚnico exige atualização a cada 24 meses.
    """
    dados = await consultar_cadunico(cpf)
    ultima_atualizacao = parse_date(dados["dataUltimaAtualizacao"])
    meses_desde = (date.today() - ultima_atualizacao).days // 30

    if meses_desde >= 22:
        return {
            "status": "URGENTE",
            "mensagem": "Seu cadastro vai vencer em breve. Vá ao CRAS atualizar.",
            "meses_restantes": 24 - meses_desde
        }
    elif meses_desde >= 18:
        return {
            "status": "ATENCAO",
            "mensagem": "Seu cadastro vence em poucos meses. Planeje ir ao CRAS.",
            "meses_restantes": 24 - meses_desde
        }
    else:
        return {
            "status": "OK",
            "mensagem": "Seu cadastro está em dia.",
            "meses_restantes": 24 - meses_desde
        }
```

### 3. Elegibilidade Cruzada
```python
async def verificar_elegibilidade_cruzada(cpf: str) -> list:
    """
    Cruza dados do CadÚnico com todos os 229 benefícios.
    Retorna lista de benefícios que o cidadão provavelmente tem direito.
    """
    dados = await consultar_cadunico(cpf)
    beneficios_elegiveis = await eligibility_service.check_all(
        renda_per_capita=dados["rendaFamiliarPerCapita"],
        membros_familia=dados["quantidadeMembros"],
        municipio=dados["municipio"],
        uf=dados["uf"]
    )
    return beneficios_elegiveis
```

## Variáveis de Ambiente
```bash
# .env
CONECTA_GOVBR_CLIENT_ID=seu_client_id
CONECTA_GOVBR_CLIENT_SECRET=seu_client_secret
CONECTA_GOVBR_URL=https://api.conectagov.estaleiro.serpro.gov.br
CADUNICO_API_URL=https://api.conectagov.estaleiro.serpro.gov.br/api-cadunico-servicos-dados/v1/dp
```

## Arquivos Relacionados
- `backend/app/agent/tools/consultar_cadunico.py` - Tool do agente
- `backend/app/services/cadunico_service.py` - Serviço de integração
- `backend/app/services/eligibility_service.py` - Motor de elegibilidade
- `backend/app/core/config.py` - Configurações

## Segurança
- CPF NUNCA em logs (usar máscara `***456789**`)
- Tokens com TTL curto (cache Redis com expiração)
- Rate limiting: respeitar limites da API Conecta
- LGPD: consentimento explícito antes de consultar
- Dados consultados NÃO são persistidos (uso em memória)

## Tratamento de Erros
| Código | Significado | Ação |
|--------|------------|------|
| 401 | Token expirado | Renovar token automaticamente |
| 404 | CPF não encontrado no CadÚnico | Orientar cidadão a se cadastrar |
| 429 | Rate limit excedido | Retry com backoff exponencial |
| 500 | API indisponível | Fallback para base local |

## Mensagens ao Usuário (Linguagem Simples)
- **Cadastrado**: "Achei seu cadastro! Está tudo certo."
- **Desatualizado**: "Seu cadastro precisa ser atualizado. Vá ao CRAS com seus documentos."
- **Não encontrado**: "Não achei seu cadastro no CadÚnico. Você precisa se cadastrar no CRAS mais perto."
- **Erro**: "Não consegui consultar agora. Tente de novo em alguns minutos."

## Referências
- Catálogo API CadÚnico: https://www.gov.br/conecta/catalogo/apis/cadunico-servicos
- API Dados Familiares: https://www.gov.br/conecta/catalogo/apis/cadunico-servicos-dados-familiares
- Roteiro Conecta Gov.br: https://www.gov.br/conecta/catalogo/roteiro-de-integracao
