---
name: mapa-social
description: Mapeamento social territorial e desertos de assistência
---

Visualização geoespacial de indicadores sociais, equipamentos SUAS e "desertos de assistência social".

## Contexto

- PostGIS já está no stack do projeto (geometrias de municípios carregadas)
- Dados geoespaciais são subutilizados para planejamento social
- "Desertos de assistência social" = áreas sem CRAS/CREAS adequados
- Censo 2022 tem dados por setor censitário

## Camadas do Mapa

### Camadas de Dados
```python
CAMADAS_MAPA = {
    "indicadores": [
        {"id": "idh_m", "nome": "IDH Municipal", "fonte": "IPEA", "tipo": "choropleth"},
        {"id": "taxa_pobreza", "nome": "Taxa de Pobreza", "fonte": "IBGE", "tipo": "choropleth"},
        {"id": "cobertura_bf", "nome": "Cobertura Bolsa Família", "fonte": "MDS", "tipo": "choropleth"},
        {"id": "cobertura_cadunico", "nome": "Cobertura CadÚnico", "fonte": "MDS", "tipo": "choropleth"},
        {"id": "gini", "nome": "Desigualdade (Gini)", "fonte": "IPEA", "tipo": "choropleth"},
        {"id": "saneamento", "nome": "Acesso a Saneamento", "fonte": "IBGE", "tipo": "choropleth"},
    ],
    "equipamentos": [
        {"id": "cras", "nome": "CRAS", "icone": "🏛", "tipo": "pontos"},
        {"id": "creas", "nome": "CREAS", "icone": "🛡", "tipo": "pontos"},
        {"id": "caps", "nome": "CAPS", "icone": "🧠", "tipo": "pontos"},
        {"id": "centro_pop", "nome": "Centro POP", "icone": "🏠", "tipo": "pontos"},
        {"id": "farmacia_popular", "nome": "Farmácia Popular", "icone": "💊", "tipo": "pontos"},
        {"id": "ubs", "nome": "UBS", "icone": "🏥", "tipo": "pontos"},
    ],
    "analise": [
        {"id": "deserto_social", "nome": "Desertos de Assistência", "tipo": "heatmap"},
        {"id": "vulnerabilidade", "nome": "Score de Vulnerabilidade", "tipo": "heatmap"},
    ],
}
```

## API GeoJSON

### Endpoint de Camadas
```python
# backend/app/routers/geo.py (expandir existente)
@router.get("/api/v1/geo/mapa-social")
async def mapa_social(
    camada: str,             # id da camada
    nivel: str = "municipio", # municipio, estado, regiao
    uf: str = None,          # filtrar por UF
    bbox: str = None,        # bounding box para viewport
) -> GeoJSON:
    """Retorna GeoJSON com dados para a camada solicitada."""
    if camada in ["idh_m", "taxa_pobreza", "cobertura_bf", "gini"]:
        return await gerar_choropleth(camada, nivel, uf, bbox)
    elif camada in ["cras", "creas", "caps", "farmacia_popular"]:
        return await gerar_pontos(camada, uf, bbox)
    elif camada == "deserto_social":
        return await gerar_heatmap_desertos(uf, bbox)
```

### Desertos de Assistência Social
```python
# backend/app/services/mapa/desertos.py
async def identificar_desertos(uf: str = None) -> list[dict]:
    """
    Identifica áreas sem cobertura adequada de equipamentos SUAS.

    Parâmetro SUAS: 1 CRAS a cada 5.000 famílias em vulnerabilidade.
    Deserto = município onde a razão famílias/CRAS excede 150% do recomendado.
    """
    query = """
        SELECT
            m.ibge_code,
            m.name,
            m.state,
            m.population,
            COALESCE(c.total_cras, 0) AS total_cras,
            COALESCE(f.familias_cadunico, 0) AS familias_vulneraveis,
            CASE
                WHEN COALESCE(c.total_cras, 0) = 0 THEN 'SEM_COBERTURA'
                WHEN f.familias_cadunico / c.total_cras > 7500 THEN 'CRITICO'
                WHEN f.familias_cadunico / c.total_cras > 5000 THEN 'INSUFICIENTE'
                ELSE 'ADEQUADO'
            END AS classificacao,
            ST_AsGeoJSON(m.geometry) AS geojson
        FROM municipalities m
        LEFT JOIN (
            SELECT municipality_ibge, COUNT(*) AS total_cras
            FROM equipamentos_suas WHERE tipo = 'cras'
            GROUP BY municipality_ibge
        ) c ON m.ibge_code = c.municipality_ibge
        LEFT JOIN (
            SELECT municipality_ibge, SUM(total_families) AS familias_cadunico
            FROM beneficiary_data WHERE program_code = 'cadunico'
            GROUP BY municipality_ibge
        ) f ON m.ibge_code = f.municipality_ibge
        WHERE (:uf IS NULL OR m.state = :uf)
        ORDER BY classificacao DESC, familias_vulneraveis DESC
    """
    return await db.execute(text(query), {"uf": uf})
```

### Correlações Visuais
```python
async def gerar_correlacao(
    indicador_x: str,  # ex: "cobertura_bf"
    indicador_y: str,  # ex: "taxa_pobreza"
    nivel: str = "municipio",
) -> dict:
    """Gera dados para scatter plot de correlação entre indicadores."""
    dados = await buscar_indicadores_pareados(indicador_x, indicador_y, nivel)
    correlacao = calcular_correlacao(dados)

    return {
        "indicador_x": indicador_x,
        "indicador_y": indicador_y,
        "pontos": dados,
        "correlacao": correlacao,
        "interpretacao": interpretar_correlacao(indicador_x, indicador_y, correlacao),
    }
```

## Frontend (Leaflet/MapLibre)

### Componente de Mapa
```tsx
// frontend/src/components/MapaSocial.tsx
import { MapContainer, TileLayer, GeoJSON } from 'react-leaflet';

export function MapaSocial() {
  const [camadaAtiva, setCamadaAtiva] = useState('cobertura_bf');
  const [dados, setDados] = useState<GeoJSON.FeatureCollection | null>(null);

  useEffect(() => {
    fetch(`/api/v1/geo/mapa-social?camada=${camadaAtiva}`)
      .then(r => r.json())
      .then(setDados);
  }, [camadaAtiva]);

  return (
    <div className="h-screen">
      {/* Seletor de camadas */}
      <div className="absolute top-4 right-4 z-10 bg-white p-4 rounded shadow">
        <h3 className="font-bold mb-2">Camadas</h3>
        {CAMADAS_MAPA.indicadores.map(c => (
          <button
            key={c.id}
            onClick={() => setCamadaAtiva(c.id)}
            className={camadaAtiva === c.id ? 'font-bold' : ''}
          >
            {c.nome}
          </button>
        ))}
      </div>

      {/* Mapa */}
      <MapContainer center={[-14.235, -51.925]} zoom={4}>
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        {dados && (
          <GeoJSON
            data={dados}
            style={(feature) => estiloChoropleth(feature, camadaAtiva)}
            onEachFeature={(feature, layer) => {
              layer.bindPopup(gerarPopup(feature, camadaAtiva));
            }}
          />
        )}
      </MapContainer>
    </div>
  );
}
```

### Paleta de Cores
```typescript
const PALETAS = {
  cobertura_bf: {
    // Verde = boa cobertura, Vermelho = baixa
    cores: ['#d73027', '#f46d43', '#fdae61', '#fee08b', '#d9ef8b', '#a6d96a', '#66bd63', '#1a9850'],
    breaks: [10, 20, 30, 40, 50, 60, 70, 80],
    unidade: '%',
  },
  idh_m: {
    // Vermelho = baixo IDH, Azul = alto
    cores: ['#d73027', '#f46d43', '#fdae61', '#fee08b', '#d9ef8b', '#a6d96a', '#66bd63', '#1a9850'],
    breaks: [0.4, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8],
    unidade: '',
  },
};
```

## Arquivos Relacionados
- `backend/app/routers/geo.py` - Endpoints GeoJSON (existente, expandir)
- `backend/app/services/mapa/desertos.py` - Análise de desertos sociais
- `backend/app/services/mapa/choropleth.py` - Geração de choropleth
- `backend/app/models/municipality.py` - Geometrias PostGIS
- `frontend/src/components/MapaSocial.tsx` - Componente do mapa

## Dependências
```bash
# Backend
pip install geoalchemy2  # já instalado (PostGIS)

# Frontend
npm install react-leaflet leaflet @types/leaflet
```

## Referências
- PostGIS: https://postgis.net/
- Leaflet: https://leafletjs.com/
- IBGE Geociências: https://www.ibge.gov.br/geociencias/
- Atlas de Vulnerabilidade Social: http://ivs.ipea.gov.br/
