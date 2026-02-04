---
name: "Business Forge Engineer"
description: "Especialista en Business Forge: gestión de assets post-magia, Fusion Engine y generación de visuales."
trigger: "forge, business forge, assets, fusion, canvas, catalog, visuals, images"
scope: "FORGE"
auto-invoke: true
---

# Business Forge Engineer - Platform AI Solutions

## 1. Concepto: The Business Forge

### Filosofía
El **Business Forge** es el **estudio post-magia** donde los usuarios refinan y utilizan los assets generados por el proceso de "Hacer Magia".

### Capacidades
- **Canvas**: Visualizar assets generados (branding, scripts, ROI, visuals)
- **Smart Catalog**: Browser de productos brutos de Tienda Nube
- **Fusion Engine**: Generación de imágenes publicitarias on-demand
- **Reality vs Dream Mode**: Overlay de producto real sobre fondo IA

### Arquitectura
```
Frontend (BusinessForge.tsx)
    ↓
Tab System (Canvas | Smart Catalog)
    ↓
Canvas → GET /admin/assets (filtrado por type)
    ↓
Smart Catalog → GET /admin/products
    ↓
Fusion Engine → POST /admin/generate-image
    ↓
Google Imagen 3 → Visual Asset
```

## 2. Frontend: Tab System

### BusinessForge Component
```tsx
const BusinessForge: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'canvas' | 'catalog'>('canvas');
  const [assets, setAssets] = useState<Asset[]>([]);
  const [products, setProducts] = useState<Product[]>([]);
  
  useEffect(() => {
    if (activeTab === 'canvas') {
      loadAssets();
    } else {
      loadProducts();
    }
  }, [activeTab]);
  
  const loadAssets = async () => {
    const data = await useApi<Asset[]>({
      method: 'GET',
      url: '/admin/assets'
    });
    setAssets(data);
  };
  
  const loadProducts = async () => {
    const data = await useApi<Product[]>({
      method: 'GET',
      url: '/admin/products'
    });
    setProducts(data);
  };
  
  return (
    <div className="forge-container">
      {/* Tab Navigation */}
      <div className="tabs">
        <button
          className={activeTab === 'canvas' ? 'active' : ''}
          onClick={() => setActiveTab('canvas')}
        >
          🎨 Canvas
        </button>
        <button
          className={activeTab === 'catalog' ? 'active' : ''}
          onClick={() => setActiveTab('catalog')}
        >
          📦 Smart Catalog
        </button>
      </div>
      
      {/* Content */}
      <div className="forge-content">
        {activeTab === 'canvas' ? (
          <CanvasView assets={assets} />
        ) : (
          <CatalogView products={products} />
        )}
      </div>
    </div>
  );
};
```

## 3. Canvas View (Assets Generados)

### Filtrado por Tipo
```tsx
const CanvasView: React.FC<{ assets: Asset[] }> = ({ assets }) => {
  const [filter, setFilter] = useState<AssetType>('all');
  
  const filteredAssets = filter === 'all'
    ? assets
    : assets.filter(a => a.type === filter);
  
  return (
    <div className="canvas-view">
      {/* Filtros */}
      <div className="filters">
        <button onClick={() => setFilter('all')}>All</button>
        <button onClick={() => setFilter('branding')}>🧬 Branding</button>
        <button onClick={() => setFilter('scripts')}>📝 Scripts</button>
        <button onClick={() => setFilter('roi')}>💰 ROI</button>
        <button onClick={() => setFilter('visuals')}>🎨 Visuals</button>
      </div>
      
      {/* Asset Grid */}
      <div className="asset-grid">
        {filteredAssets.map(asset => (
          <AssetCard key={asset.id} asset={asset} />
        ))}
      </div>
    </div>
  );
};
```

### Asset Card (Polymorphic Renderer)
```tsx
const AssetCard: React.FC<{ asset: Asset }> = ({ asset }) => {
  const renderContent = () => {
    switch (asset.type) {
      case 'branding':
        return <BrandingAsset content={asset.content} />;
      
      case 'scripts':
        return <ScriptsAsset content={asset.content} />;
      
      case 'roi':
        return <ROIAsset content={asset.content} />;
      
      case 'visuals':
        return <VisualsAsset content={asset.content} />;
      
      default:
        return <JSONView data={asset.content} />;
    }
  };
  
  return (
    <div className="asset-card">
      <div className="asset-header">
        <h3>{asset.type}</h3>
        <span className="timestamp">
          {new Date(asset.created_at).toLocaleDateString()}
        </span>
      </div>
      
      <div className="asset-body">
        {renderContent()}
      </div>
    </div>
  );
};
```

### Branding Asset
```tsx
const BrandingAsset: React.FC<{ content: BrandingContent }> = ({ content }) => {
  return (
    <div className="branding-asset">
      <div className="section">
        <h4>MISIÓN</h4>
        <p>{content.mission}</p>
      </div>
      
      <div className="section">
        <h4>VISIÓN</h4>
        <p>{content.vision}</p>
      </div>
      
      <div className="section">
        <h4>VOZ DE MARCA</h4>
        <p>{content.voice}</p>
      </div>
      
      <div className="section">
        <h4>VALORES</h4>
        <ul>
          {content.values.map((v, i) => (
            <li key={i}>{v}</li>
          ))}
        </ul>
      </div>
      
      <div className="color-palette">
        <h4>PALETA DE COLORES</h4>
        <div className="colors">
          {content.color_palette.map((color, i) => (
            <div
              key={i}
              className="color-swatch"
              style={{ backgroundColor: color }}
              title={color}
            />
          ))}
        </div>
      </div>
    </div>
  );
};
```

### Visuals Asset (Social Posts)
```tsx
const VisualsAsset: React.FC<{ content: VisualsContent }> = ({ content }) => {
  return (
    <div className="visuals-grid">
      {content.social_posts.map((post, i) => (
        <FusionItem key={i} post={post} />
      ))}
    </div>
  );
};
```

## 4. Fusion Engine (Generación On-Demand)

### FusionItem Component
```tsx
interface FusionPost {
  product_id: string;
  product_name: string;
  image_url: string;  // URL de la imagen generada por IA
  base_image?: string;  // URL original del producto (para overlay)
  prompt_used: string;
}

const FusionItem: React.FC<{ post: FusionPost }> = ({ post }) => {
  const [viewMode, setViewMode] = useState<'dream' | 'reality'>('dream');
  
  return (
    <div className="fusion-item">
      <div className="image-container">
        {viewMode === 'dream' ? (
          // Imagen pura de IA (puede alucinar detalles)
          <img src={post.image_url} alt={post.product_name} />
        ) : (
          // Overlay: fondo IA + producto real
          <div className="reality-overlay">
            <img
              src={post.image_url}
              className="background"
              alt="AI Background"
            />
            <img
              src={post.base_image}
              className="product-overlay"
              alt={post.product_name}
              style={{
                position: 'absolute',
                top: '50%',
                left: '50%',
                transform: 'translate(-50%, -50%)',
                maxWidth: '60%',
                maxHeight: '60%',
                mixBlendMode: 'multiply'
              }}
            />
          </div>
        )}
      </div>
      
      <div className="fusion-controls">
        <button
          onClick={() => setViewMode(viewMode === 'dream' ? 'reality' : 'dream')}
        >
          {viewMode === 'dream' ? '🌟 Dream' : '✨ Reality'}
        </button>
      </div>
      
      <div className="product-info">
        <h4>{post.product_name}</h4>
        <p className="prompt-hint">{post.prompt_used}</p>
      </div>
    </div>
  );
};
```

### Generar Nueva Imagen (Fusion Button)
```tsx
const ProductCard: React.FC<{ product: Product }> = ({ product }) => {
  const [generating, setGenerating] = useState(false);
  
  const handleIgniteFusion = async () => {
    setGenerating(true);
    
    try {
      const prompt = `
Professional advertising shot of ${product.name}.
Luxury aesthetic, soft lighting, minimal background.
High-end product photography, studio quality.
`;
      
      const response = await useApi({
        method: 'POST',
        url: '/admin/generate-image',
        data: {
          prompt: prompt,
          image_url: product.image_url
        }
      });
      
      if (response.status === 'success') {
        // Guardar en assets
        await saveGeneratedVisual(response.url, product);
        alert('Visual generated!');
      }
      
    } catch (error) {
      alert('Generation failed');
    } finally {
      setGenerating(false);
    }
  };
  
  return (
    <div className="product-card">
      <img src={product.image_url} alt={product.name} />
      <h3>{product.name}</h3>
      <p>${product.price}</p>
      
      <button
        onClick={handleIgniteFusion}
        disabled={generating}
        className="fusion-btn"
      >
        {generating ? 'Generating...' : '🔥 Ignite Fusion'}
      </button>
    </div>
  );
};
```

## 5. Backend: Fusion Engine

### generate-image Endpoint
```python
# orchestrator_service/app/api/v1/endpoints/forge.py

@router.post("/admin/generate-image")
async def generate_image(
    payload: ImageGenerationRequest,
    current_user = Depends(verify_admin_token)
):
    """
    Genera imagen publicitaria usando Google Imagen 3
    """
    tenant_id = await resolve_tenant(current_user.id)
    
    # Validar credencial de Google
    google_key = await get_tenant_credential(
        tenant_id=tenant_id,
        category="google",
        name="API_KEY"
    )
    
    if not google_key:
        raise HTTPException(
            status_code=400,
            detail="Google API key not configured"
        )
    
    # Opcionalmente, descargar imagen base para context
    base_image_data = None
    if payload.image_url:
        img_response = await httpx.get(payload.image_url)
        base_image_data = img_response.content
    
    # Llamar a Google Imagen 3
    try:
        response = await httpx.post(
            "https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0:generate",
            headers={
                "Authorization": f"Bearer {google_key}",
                "Content-Type": "application/json"
            },
            json={
                "prompt": payload.prompt,
                "num_images": 1,
                "aspect_ratio": "1:1",
                "safety_filter": "medium"
            },
            timeout=60.0
        )
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Google Imagen API error: {response.text}"
            )
        
        data = response.json()
        generated_url = data['images'][0]['url']
        
        return {
            "status": "success",
            "url": generated_url
        }
        
    except Exception as e:
        logger.error(f"Image generation failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Generation failed: {str(e)}"
        )
```

## 6. Smart Catalog (Product Browser)

### Catalog View
```tsx
const CatalogView: React.FC<{ products: Product[] }> = ({ products }) => {
  const [categoryFilter, setCategoryFilter] = useState<string | null>(null);
  
  // Extraer categorías únicas
  const categories = Array.from(
    new Set(products.map(p => p.category).filter(Boolean))
  );
  
  const filteredProducts = categoryFilter
    ? products.filter(p => p.category === categoryFilter)
    : products;
  
  return (
    <div className="catalog-view">
      {/* Filtro de categorías */}
      <div className="category-filters">
        <button
          className={!categoryFilter ? 'active' : ''}
          onClick={() => setCategoryFilter(null)}
        >
          All Products
        </button>
        {categories.map(cat => (
          <button
            key={cat}
            className={categoryFilter === cat ? 'active' : ''}
            onClick={() => setCategoryFilter(cat)}
          >
            {cat}
          </button>
        ))}
      </div>
      
      {/* Grid de productos */}
      <div className="product-grid">
        {filteredProducts.map(product => (
          <ProductCard key={product.id} product={product} />
        ))}
      </div>
    </div>
  );
};
```

## 7. Persistencia de Assets

### Backend: Assets Endpoint
```python
@router.get("/admin/assets")
async def list_assets(
    current_user = Depends(verify_admin_token),
    type_filter: Optional[str] = None,
    session: AsyncSession = Depends(get_session)
):
    """
    Lista assets generados
    """
    tenant_id = await resolve_tenant(current_user.id)
    
    # Query base
    stmt = select(BusinessAsset).where(
        BusinessAsset.tenant_id == tenant_id
    )
    
    # Filtro opcional por tipo
    if type_filter:
        stmt = stmt.where(BusinessAsset.type == type_filter)
    
    # Ordenar por más reciente
    stmt = stmt.order_by(BusinessAsset.created_at.desc())
    
    result = await session.execute(stmt)
    assets = result.scalars().all()
    
    return [
        {
            "id": a.id,
            "type": a.type,
            "content": a.content,
            "created_at": a.created_at.isoformat()
        }
        for a in assets
    ]
```

### Guardar Visual Generado
```python
@router.post("/admin/assets", status_code=201)
async def save_asset(
    payload: AssetCreate,
    current_user = Depends(verify_admin_token),
    session: AsyncSession = Depends(get_session)
):
    tenant_id = await resolve_tenant(current_user.id)
    
    asset = BusinessAsset(
        tenant_id=tenant_id,
        type=payload.type,
        content=payload.content
    )
    
    session.add(asset)
    await session.commit()
    await session.refresh(asset)
    
    return {
        "id": asset.id,
        "status": "saved"
    }
```

## 8. Reality vs Dream Mode (CSS Magic)

### CSS Implementation
```css
/* Reality Mode: Overlay */
.reality-overlay {
  position: relative;
  width: 100%;
  aspect-ratio: 1 / 1;
  overflow: hidden;
}

.reality-overlay .background {
  width: 100%;
  height: 100%;
  object-fit: cover;
  filter: brightness(0.9);  /* Oscurecer ligeramente fondo */
}

.reality-overlay .product-overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  max-width: 60%;
  max-height: 60%;
  object-fit: contain;
  mix-blend-mode: multiply;  /* Mezclar con fondo */
  filter: drop-shadow(0 10px 30px rgba(0,0,0,0.3));  /* Sombra realista */
}
```

## 9. Export & Download

### Exportar Asset
```tsx
const exportAsset = async (asset: Asset) => {
  if (asset.type === 'visuals') {
    // Descargar imagen
    const imageUrl = asset.content.social_posts[0].image_url;
    
    const link = document.createElement('a');
    link.href = imageUrl;
    link.download = `visual_${asset.id}.jpg`;
    link.click();
    
  } else {
    // Descargar JSON
    const blob = new Blob(
      [JSON.stringify(asset.content, null, 2)],
      { type: 'application/json' }
    );
    
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `${asset.type}_${asset.id}.json`;
    link.click();
  }
};
```

## 10. Troubleshooting

### "No se ve la imagen generada"
```
Causa: URL de Google Imagen tiene CORS restrictivo
Solución: Proxy la imagen a través del backend o guardarla en storage
```

### "Fusion falla silenciosamente"
```
Causa: Google API quota excedida
Solución: Verificar quota en Google Cloud Console
```

### "Overlay no se ve bien"
```
Causa: Imagen original tiene fondo blanco (no transparente)
Solución: Usar productos con PNGs transparentes o aplicar remove-bg
```

### "Assets no cargan"
```
Causa: tenant_id incorrecto
Solución: Verificar resolve_tenant en backend
```

## 11. Checklist de Implementación

### Frontend
- [ ] Tab system (Canvas / Catalog)
- [ ] Asset grid con filtros
- [ ] Polymorphic asset renderer
- [ ] Fusion button funcional
- [ ] Reality vs Dream toggle
- [ ] Category filters en Catalog
- [ ] Export/Download assets

### Backend
- [ ] GET /admin/assets (con filtros)
- [ ] POST /admin/generate-image
- [ ] GET /admin/products (desde TiendaNube)
- [ ] POST /admin/assets (guardar generados)
- [ ] Google Imagen 3 integration
- [ ] Validación de credenciales

### Visuals
- [ ] Branding asset renderer
- [ ] Scripts asset renderer
- [ ] ROI asset renderer
- [ ] Social posts grid
- [ ] CSS overlay effect
- [ ] Product cards con imagen

---

**Tip**: Para mejores resultados en Fusion, usar prompts específicos con estilo deseado (ej: "minimalist white background", "luxury studio lighting").
