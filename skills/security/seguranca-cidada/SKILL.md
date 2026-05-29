---
name: seguranca-cidada
description: Protecao de dados do cidadao (LGPD+)
---

Implementacao completa de protecao de dados pessoais conforme LGPD, com consentimento granular e portabilidade.

## Contexto

- CPF e dado ultrassensivel -- base de todo o sistema
- LGPD (Lei 13.709/2018) e obrigatoria para qualquer tratamento de dados pessoais
- Confianca do cidadao e pre-requisito para adocao da plataforma
- Dados de saude e beneficios sao dados sensiveis (Art. 5o, II)

## Dados Tratados pelo Ta na Mao

### Classificacao por Sensibilidade
```
DADOS PESSOAIS (Art. 5o, I):
├── CPF
├── Nome completo
├── Data de nascimento
├── Endereco / CEP
├── Telefone
├── NIS (Numero de Inscricao Social)
└── Composicao familiar

DADOS SENSIVEIS (Art. 5o, II):
├── Dados de saude (receitas medicas, CID)
├── Condicao de deficiencia
├── Situacao de violencia
├── Orientacao sexual / genero
└── Origem racial/etnica (IBGE)

DADOS DE MENORES (Art. 14):
├── Dados de criancas/adolescentes
└── Requer consentimento do responsavel

DADOS FINANCEIROS:
├── Renda familiar
├── Valores de beneficios
├── Dados de dinheiro esquecido (PIS/PASEP/FGTS)
└── Historico de pagamentos
```

## Consentimento Granular

### Tela de Consentimento
```python
# backend/app/models/consentimento.py
class Consentimento(Base):
    __tablename__ = "consentimentos"

    id: Mapped[int] = mapped_column(primary_key=True)
    cpf_hash: Mapped[str] = mapped_column(index=True)
    finalidade: Mapped[str]           # consulta_beneficio, farmacia, pesquisa
    dados_autorizados: Mapped[list]   # ["cpf", "renda", "composicao_familiar"]
    data_consentimento: Mapped[datetime]
    data_expiracao: Mapped[datetime | None]
    canal: Mapped[str]                # app, whatsapp, web
    revogado: Mapped[bool] = mapped_column(default=False)
    data_revogacao: Mapped[datetime | None]
    ip_hash: Mapped[str | None]
```

### Finalidades de Tratamento
```python
FINALIDADES = {
    "consulta_beneficio": {
        "descricao": "Consultar seus beneficios sociais",
        "dados_necessarios": ["cpf"],
        "dados_opcionais": ["nome", "endereco"],
        "base_legal": "consentimento",  # Art. 7o, I
        "retencao": "durante_sessao",
    },
    "elegibilidade": {
        "descricao": "Verificar quais beneficios voce tem direito",
        "dados_necessarios": ["cpf", "renda", "composicao_familiar"],
        "dados_opcionais": ["endereco", "trabalho"],
        "base_legal": "consentimento",
        "retencao": "24_horas",
    },
    "farmacia": {
        "descricao": "Pedir medicamentos na Farmacia Popular",
        "dados_necessarios": ["cpf", "receita_medica"],
        "dados_opcionais": ["localizacao"],
        "base_legal": "consentimento",
        "dados_sensiveis": True,
        "retencao": "30_dias",
    },
    "encaminhamento_cras": {
        "descricao": "Gerar carta de encaminhamento para o CRAS",
        "dados_necessarios": ["cpf", "nome", "endereco"],
        "base_legal": "consentimento",
        "retencao": "90_dias",
    },
    "pesquisa": {
        "descricao": "Responder pesquisa para melhorar o app (anonimo)",
        "dados_necessarios": [],
        "dados_opcionais": ["municipio"],
        "base_legal": "consentimento",
        "retencao": "indefinida_anonimizada",
    },
}
```

### Verificacao de Consentimento
```python
# backend/app/middleware/consentimento.py
async def verificar_consentimento(cpf_hash: str, finalidade: str) -> bool:
    """Verifica se cidadao consentiu para esta finalidade."""
    consentimento = await db.query(Consentimento).filter(
        Consentimento.cpf_hash == cpf_hash,
        Consentimento.finalidade == finalidade,
        Consentimento.revogado == False,
        or_(
            Consentimento.data_expiracao == None,
            Consentimento.data_expiracao > datetime.utcnow()
        )
    ).first()
    return consentimento is not None
```

## Portabilidade de Dados (Art. 18, V)

### Export de Dados
```python
# backend/app/routers/lgpd.py
@router.get("/api/v1/meus-dados/exportar")
async def exportar_dados(cpf: str = Depends(auth_cidadao), formato: str = "json"):
    """Exporta todos os dados do cidadao em formato legivel."""
    cpf_hash = hash_cpf(cpf)

    dados = {
        "titular": {
            "cpf_parcial": f"***{cpf[3:9]}**",
            "data_export": datetime.utcnow().isoformat(),
        },
        "consentimentos": await buscar_consentimentos(cpf_hash),
        "consultas_realizadas": await buscar_historico_consultas(cpf_hash),
        "beneficios_encontrados": await buscar_beneficios_historico(cpf_hash),
        "atendimentos": await buscar_atendimentos(cpf_hash),
        "dados_armazenados": await listar_dados_armazenados(cpf_hash),
    }

    if formato == "json":
        return JSONResponse(dados)
    elif formato == "pdf":
        return await gerar_pdf_dados(dados)
```

## Direito ao Esquecimento (Art. 18, VI)

### Exclusao de Dados
```python
@router.delete("/api/v1/meus-dados/excluir")
async def excluir_dados(cpf: str = Depends(auth_cidadao), confirmar: bool = False):
    """Exclui todos os dados do cidadao da plataforma."""
    if not confirmar:
        return {
            "aviso": "Isso vai apagar TODOS os seus dados do Ta na Mao. "
                     "Voce nao vai perder seus beneficios, "
                     "so os dados que estao aqui no app.",
            "confirmar": "Envie novamente com confirmar=true para excluir.",
        }

    cpf_hash = hash_cpf(cpf)

    # Excluir dados de todas as tabelas
    await db.execute(delete(Consentimento).where(Consentimento.cpf_hash == cpf_hash))
    await db.execute(delete(HistoricoConsulta).where(HistoricoConsulta.cpf_hash == cpf_hash))
    await db.execute(delete(Atendimento).where(Atendimento.cpf_hash == cpf_hash))

    # Limpar cache Redis
    await redis.delete(f"session:{cpf_hash}")
    await redis.delete(f"wa_session:{cpf_hash}")

    # Registrar exclusao (sem dados pessoais, so o fato)
    await registrar_log_exclusao(cpf_hash)

    return {"mensagem": "Todos os seus dados foram excluidos com sucesso."}
```

## Auditoria de Acessos

### Log de Acesso a Dados
```python
# backend/app/middleware/auditoria.py
class AuditoriaMiddleware:
    async def __call__(self, request: Request, call_next):
        response = await call_next(request)

        # Registrar acesso a dados pessoais
        if self._acessa_dados_pessoais(request):
            await registrar_acesso(
                endpoint=request.url.path,
                metodo=request.method,
                ip_hash=hash_ip(request.client.host),
                timestamp=datetime.utcnow(),
                status_code=response.status_code,
                # NAO registrar payload ou dados pessoais
            )

        return response
```

### Simulacao de Vazamento
```python
# backend/app/services/incidente.py
PLANO_RESPOSTA_INCIDENTE = {
    "etapas": [
        {
            "passo": 1,
            "acao": "Identificar escopo do vazamento",
            "responsavel": "Equipe tecnica",
            "prazo": "2 horas",
        },
        {
            "passo": 2,
            "acao": "Conter o vazamento (revogar tokens, bloquear acesso)",
            "responsavel": "Equipe tecnica",
            "prazo": "4 horas",
        },
        {
            "passo": 3,
            "acao": "Notificar ANPD (Autoridade Nacional de Protecao de Dados)",
            "responsavel": "DPO",
            "prazo": "72 horas (obrigatorio)",
        },
        {
            "passo": 4,
            "acao": "Notificar titulares afetados",
            "responsavel": "DPO + Comunicacao",
            "prazo": "72 horas",
        },
        {
            "passo": 5,
            "acao": "Documentar incidente e medidas tomadas",
            "responsavel": "DPO",
            "prazo": "30 dias",
        },
    ],
    "contatos": {
        "anpd": "https://www.gov.br/anpd/pt-br",
        "dpo_email": "dpo@tanamao.com.br",
    },
}
```

## Mensagens ao Cidadao (Linguagem Simples)

### Consentimento
```
Para consultar seus beneficios, vou precisar do seu CPF.

O que eu faco com ele:
- Consulto seus beneficios
- Verifico se voce tem direito a outros
- NAO guardo seus dados depois
- NAO compartilho com ninguem
- NAO vendo seus dados

Voce pode apagar tudo a qualquer momento.

Posso continuar?
```

### Exclusao de Dados
```
Seus dados foram apagados do Ta na Mao.

Isso NAO afeta seus beneficios -- eles continuam normais.
So apagamos o que estava aqui no app.

Se quiser usar de novo no futuro, e so entrar normalmente.
```

## Arquivos Relacionados
- `backend/app/models/consentimento.py` - Modelo de consentimento
- `backend/app/middleware/consentimento.py` - Verificacao de consentimento
- `backend/app/middleware/auditoria.py` - Log de auditoria
- `backend/app/routers/lgpd.py` - Endpoints LGPD
- `backend/app/services/incidente.py` - Plano de resposta
- `.claude/skills/defense-in-depth/SKILL.md` - Skill de seguranca (complementar)

## Referencias
- LGPD: https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm
- ANPD: https://www.gov.br/anpd/pt-br
- Guia LGPD para Governo: https://www.gov.br/governodigital/pt-br/seguranca-e-protecao-de-dados/guias/guia-lgpd
