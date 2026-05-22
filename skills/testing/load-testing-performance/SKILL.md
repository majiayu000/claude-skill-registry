# ⚡ Skill: Load Testing & Performance

## 📋 Metadata

| Atributo | Valor |
|----------|-------|
| **ID** | `sre-load-testing-performance` |
| **Nivel** | 🔴 Avanzado |
| **Versión** | 1.0.0 |
| **Keywords** | `load-testing`, `performance`, `k6`, `jmeter`, `stress-testing`, `capacity-planning`, `benchmarking`, `rust` |
| **Referencia** | [k6 Documentation](https://k6.io/docs/), [JMeter](https://jmeter.apache.org/) |

## 🔑 Keywords para Invocación

- `load-testing`
- `performance-testing`
- `stress-testing`
- `k6`
- `jmeter`
- `capacity-planning`
- `benchmarking`
- `rust`
- `@skill:load-testing`

### Ejemplos de Prompts

```
Implementa load testing con k6 para APIs
```

```
Configura stress testing y capacity planning
```

```
Setup performance benchmarking y profiling
```

```
@skill:load-testing - Estrategia completa de testing de carga
```

```
Implementa profiling y benchmarking para backend Rust
```

## 📖 Descripción

Load testing y performance optimization son esenciales para entender los límites de un sistema. Este skill cubre herramientas de load testing (k6, JMeter), estrategias de testing, capacity planning, profiling, y optimización de performance.

### ✅ Cuándo Usar Este Skill

- Antes de releases importantes
- Capacity planning
- Performance optimization
- SLA validation
- Stress testing
- Finding bottlenecks

### ❌ Cuándo NO Usar Este Skill

- Prototipos tempranos
- Sistemas sin usuarios reales
- Aplicaciones sin requisitos de performance

## 🏗️ Tipos de Testing

```
Load Testing
    ├── Baseline (Expected load)
    ├── Stress (Beyond capacity)
    ├── Spike (Sudden load increase)
    ├── Endurance (Extended duration)
    └── Volume (Large data sets)
```

## 💻 Implementación

> **📁 Scripts Ejecutables:** Este skill incluye scripts ejecutables en la carpeta [`scripts/`](scripts/):
> - **k6 Tests:** [`scripts/k6/`](scripts/k6/) - Scripts de load testing (JavaScript)
> - **Node.js Profiling:** [`scripts/nodejs/`](scripts/nodejs/) - Herramientas de profiling (JavaScript)
> - **Rust Benchmarks:** [`scripts/rust/`](scripts/rust/) - Benchmarks con Criterion (Rust)
> - **Python Capacity Planning:** [`scripts/python/`](scripts/python/) - Calculadora de capacidad (Python)
> 
> Ver [`scripts/README.md`](scripts/README.md) para documentación de uso completa.

### 1. k6 Load Testing

#### 1.1 Basic Test Script

**Script ejecutable:** [`scripts/k6/basic-load.js`](scripts/k6/basic-load.js)

Script básico de load testing con k6 para APIs. Incluye métricas personalizadas, thresholds y stages configurables.

**Cuándo ejecutar:**
- Testing de carga básico de APIs
- Validación de SLA de respuesta
- Baseline de performance

**Uso:**
```bash
# Ejecutar test básico
k6 run scripts/k6/basic-load.js

# Con variables de entorno
k6 run scripts/k6/basic-load.js \
  --env BASE_URL=https://api.example.com \
  --env API_TOKEN=your-token
```

**Características:**
- ✅ Stages configurables (ramp up/down)
- ✅ Thresholds de latencia y error rate
- ✅ Métricas personalizadas (error rate, request duration)
- ✅ Variables de entorno para configuración

#### 1.2 Advanced Test with Scenarios

**Script ejecutable:** [`scripts/k6/advanced-scenarios.js`](scripts/k6/advanced-scenarios.js)

Test avanzado con múltiples escenarios simulando diferentes comportamientos de usuarios (browse, checkout, search).

**Cuándo ejecutar:**
- Testing de escenarios realistas
- Simulación de diferentes tipos de usuarios
- Testing de e-commerce o aplicaciones complejas

**Uso:**
```bash
# Ejecutar todos los escenarios
k6 run scripts/k6/advanced-scenarios.js

# Ejecutar escenario específico
k6 run scripts/k6/advanced-scenarios.js --env SCENARIO=browse_products
```

**Características:**
- ✅ Múltiples escenarios simultáneos
- ✅ Diferentes tipos de executors (ramping-vus, constant-arrival-rate, shared-iterations)
- ✅ Thresholds por escenario
- ✅ Simulación de comportamiento realista

#### 1.3 Stress Test

**Script ejecutable:** [`scripts/k6/stress-test.js`](scripts/k6/stress-test.js)

Stress test que incrementa gradualmente la carga más allá de la capacidad normal para encontrar puntos de quiebre.

**Cuándo ejecutar:**
- Encontrar límites del sistema
- Identificar puntos de quiebre
- Testing de recovery después de stress

**Uso:**
```bash
k6 run scripts/k6/stress-test.js
k6 run scripts/k6/stress-test.js --env BASE_URL=https://api.example.com
```

**Características:**
- ✅ Incremento gradual de carga
- ✅ Thresholds relajados para stress testing
- ✅ Período de recovery incluido

### 2. Performance Profiling

#### 2.1 Application Profiling (Node.js)

**Script ejecutable:** [`scripts/nodejs/performance-profiler.js`](scripts/nodejs/performance-profiler.js)

Herramienta de CPU profiling para aplicaciones Node.js usando v8-profiler.

**Cuándo ejecutar:**
- Identificar cuellos de botella de CPU
- Profiling de funciones específicas
- Análisis de performance de Node.js

**Uso:**
```bash
cd scripts/nodejs
npm install

# Profiling por duración
node performance-profiler.js --profile-name my-app --duration=60

# Programático (en tu código)
const profiler = require('./performance-profiler');
const profilerInstance = new profiler();
await profilerInstance.profileFunction(slowFunction, 'slow-function-profile');
```

**Características:**
- ✅ CPU profiling con v8-profiler
- ✅ Exportación a formato .cpuprofile (Chrome DevTools)
- ✅ Profiling de funciones específicas
- ✅ CLI y uso programático

#### 2.2 Memory Profiling

**Script ejecutable:** [`scripts/nodejs/memory-profiler.js`](scripts/nodejs/memory-profiler.js)

Herramienta de memory profiling y monitoreo para aplicaciones Node.js.

**Cuándo ejecutar:**
- Detectar memory leaks
- Monitoreo continuo de memoria
- Análisis de uso de heap

**Uso:**
```bash
# Monitoreo continuo
node memory-profiler.js --monitor --interval=5000

# Tomar snapshot
node memory-profiler.js --snapshot --filename=heap.heapsnapshot

# Ver uso actual
node memory-profiler.js
```

**Características:**
- ✅ Heap snapshots (.heapsnapshot para Chrome DevTools)
- ✅ Monitoreo continuo de memoria
- ✅ Métricas detalladas (RSS, heap, external)

#### 2.3 Performance Profiling (Rust)

**Script ejecutable:** [`scripts/rust/benches/my_benchmark.rs`](scripts/rust/benches/my_benchmark.rs)

Benchmarks de performance para código Rust usando Criterion.

**Cuándo ejecutar:**
- Benchmarking de funciones críticas
- Comparación de implementaciones
- Validación de optimizaciones

**Uso:**
```bash
cd scripts/rust

# Ejecutar benchmarks
cargo bench

# Con profiling integrado
cargo bench -- --profile-time=10

# Ver reportes HTML
open target/criterion/report/index.html
```

**Características:**
- ✅ Benchmarks con Criterion
- ✅ Reportes HTML detallados
- ✅ Comparación entre ejecuciones
- ✅ Estadísticas avanzadas (percentiles, outliers)

#### 2.4 CPU Profiling con perf (Rust)

```bash
# Instalar herramientas de profiling
sudo apt-get install linux-perf

# Compilar con símbolos de debug (optimizado pero con símbolos)
RUSTFLAGS="-g" cargo build --release

# Profiling con perf
perf record --call-graph dwarf ./target/release/my-service

# Ver resultados
perf report

# Generar flamegraph
perf script | stackcollapse-perf.pl | flamegraph.pl > flamegraph.svg
```

```rust
// src/profiling.rs
use std::time::Instant;
use tracing::{info, debug};

pub struct PerformanceProfiler {
    start_time: Instant,
}

impl PerformanceProfiler {
    pub fn new() -> Self {
        Self {
            start_time: Instant::now(),
        }
    }

    pub fn elapsed(&self) -> u64 {
        self.start_time.elapsed().as_millis() as u64
    }

    pub fn log_elapsed(&self, operation: &str) {
        let elapsed = self.elapsed();
        info!(
            operation = operation,
            duration_ms = elapsed,
            "Operation completed"
        );
    }
}

impl Drop for PerformanceProfiler {
    fn drop(&mut self) {
        debug!(
            total_duration_ms = self.elapsed(),
            "Profiler dropped"
        );
    }
}

// Uso
pub async fn process_user_request(user_id: &str) -> Result<(), Error> {
    let _profiler = PerformanceProfiler::new();
    
    // Tu código aquí
    let user = fetch_user(user_id).await?;
    _profiler.log_elapsed("fetch_user");
    
    let result = process_data(&user).await?;
    _profiler.log_elapsed("process_data");
    
    Ok(())
}
```

#### 2.5 Memory Profiling (Rust)

```toml
# Cargo.toml
[dependencies]
dhat = "0.3"  # Para memory profiling
```

```rust
// src/lib.rs (solo para profiling)
#[cfg(feature = "dhat-heap")]
#[global_allocator]
static ALLOC: dhat::Alloc = dhat::Alloc;

// En main.rs o tests
#[cfg(feature = "dhat-heap")]
{
    let _profiler = dhat::Profiler::new_heap();
    
    // Tu código aquí
    run_application().await;
}
```

```bash
# Compilar con dhat feature
cargo build --release --features dhat-heap

# Ejecutar - generará dhat-heap.json
./target/release/my-service

# Analizar con dhat
dhat-view dhat-heap.json
```

#### 2.6 Flamegraph Profiling (Rust)

```bash
# Instalar cargo-flamegraph
cargo install flamegraph

# Generar flamegraph
cargo flamegraph --bin my-service

# Con opciones específicas
cargo flamegraph --dev --example my-example -- --test-input

# Para servicios web (necesita requests)
cargo flamegraph --dev --bin my-service &
# Hacer requests con k6 o curl
k6 run load-test.js
# Ctrl+C para detener flamegraph
```

#### 2.7 Performance Metrics en Rust (Actix Web)

```toml
# Cargo.toml
[dependencies]
actix-web = "4"
actix-web-prom = "0.6"
prometheus = "0.13"
```

```rust
// src/metrics.rs
use actix_web::web;
use actix_web_prom::PrometheusMetricsBuilder;
use prometheus::{Counter, Histogram, Registry, Opts};

lazy_static::lazy_static! {
    pub static ref HTTP_REQUESTS_TOTAL: Counter = Counter::with_opts(
        Opts::new("http_requests_total", "Total HTTP requests")
            .const_label("service", "my-service")
    ).unwrap();

    pub static ref HTTP_REQUEST_DURATION: Histogram = Histogram::with_opts(
        prometheus::HistogramOpts::new(
            "http_request_duration_seconds",
            "HTTP request duration"
        )
        .buckets(vec![0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0])
        .const_label("service", "my-service")
    ).unwrap();
}

pub fn init_metrics() -> Result<(), Box<dyn std::error::Error>> {
    let registry = Registry::new();
    registry.register(Box::new(HTTP_REQUESTS_TOTAL.clone()))?;
    registry.register(Box::new(HTTP_REQUEST_DURATION.clone()))?;
    Ok(())
}
```

```rust
// src/main.rs
use actix_web::{web, App, HttpServer, middleware};
use actix_web_prom::PrometheusMetricsBuilder;
use crate::metrics::init_metrics;

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    init_metrics().unwrap();

    let prometheus = PrometheusMetricsBuilder::new("api")
        .endpoint("/metrics")
        .build()
        .unwrap();

    HttpServer::new(move || {
        App::new()
            .wrap(prometheus.clone())
            .wrap(middleware::Logger::default())
            .route("/health", web::get().to(health))
            .route("/api/users", web::get().to(get_users))
    })
    .bind("0.0.0.0:8080")?
    .run()
    .await
}
```

#### 2.8 Load Testing Rust Backend con k6

**Script ejecutable:** [`scripts/k6/rust-api-load.js`](scripts/k6/rust-api-load.js)

Test de carga optimizado para APIs Rust con thresholds más estrictos debido al mejor rendimiento esperado.

**Uso:**
```bash
k6 run scripts/k6/rust-api-load.js --env BASE_URL=http://localhost:8080
```

#### 2.9 Performance Comparison Testing

**Script ejecutable:** [`scripts/k6/performance-comparison.js`](scripts/k6/performance-comparison.js)

Test de comparación de performance entre diferentes backends (Rust vs Node.js, etc.).

**Uso:**
```bash
k6 run scripts/k6/performance-comparison.js \
  --env RUST_API=http://rust-api:8080 \
  --env NODE_API=http://node-api:3000
```

### 3. Capacity Planning

**Script ejecutable:** [`scripts/python/capacity_calculator.py`](scripts/python/capacity_calculator.py)

Calculadora de capacidad para planificación de recursos basada en métricas de uso.

**Cuándo ejecutar:**
- Planificación de escalado
- Estimación de recursos necesarios
- Análisis de capacidad actual

**Uso:**
```bash
cd scripts/python

# Generar reporte de capacidad
python capacity_calculator.py --report

# Calcular recursos para usuarios objetivo
python capacity_calculator.py \
  --target-users 5000 \
  --current-users 1000 \
  --max-throughput 1000.0 \
  --current-instances 3
```

**Características:**
- ✅ Cálculo de capacity headroom
- ✅ Estimación de usuarios máximos
- ✅ Cálculo de recursos necesarios
- ✅ Reportes detallados

### 4. CI/CD Integration

```yaml
# .github/workflows/load-test.yml
name: Load Test

on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM
  workflow_dispatch:

jobs:
  load-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install k6
        run: |
          sudo gpg -k
          sudo gpg --no-default-keyring --keyring /usr/share/keyrings/k6-archive-keyring.gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69
          echo "deb [signed-by=/usr/share/keyrings/k6-archive-keyring.gpg] https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
          sudo apt-get update
          sudo apt-get install k6

      - name: Run load test
        run: |
          k6 run tests/load/basic-load.js
        env:
          API_TOKEN: ${{ secrets.API_TOKEN }}

      - name: Upload results
        uses: actions/upload-artifact@v3
        with:
          name: k6-results
          path: results/
```

### 5. Performance Monitoring

```yaml
# prometheus/performance-metrics.yml
scrape_configs:
  - job_name: 'k6'
    static_configs:
      - targets: ['k6:6565']
```

```javascript
// k6 output to Prometheus
import { Counter, Gauge, Trend } from 'k6/metrics';

const customCounter = new Counter('custom_errors');
const customGauge = new Gauge('custom_active_users');
const customTrend = new Trend('custom_request_duration');

export default function () {
  customGauge.set(100);
  customCounter.add(1);
  customTrend.add(123);
}
```

## 🎯 Mejores Prácticas

### 1. Test Design

✅ **DO:**
- Start with baseline tests
- Gradually increase load
- Test realistic scenarios
- Monitor during tests
- Test failure scenarios

❌ **DON'T:**
- Start with maximum load
- Ignore resource limits
- Test unrealistic scenarios
- Skip monitoring

### 2. Test Data

✅ **DO:**
- Use realistic test data
- Parameterize requests
- Use unique data per user
- Clean up test data

❌ **DON'T:**
- Use production data
- Hardcode test values
- Share data between users

### 3. Analysis

✅ **DO:**
- Compare against baselines
- Identify bottlenecks
- Document findings
- Share results with team

❌ **DON'T:**
- Ignore anomalies
- Skip root cause analysis
- Test without objectives

## 🚨 Troubleshooting

### Tests Failing

1. Check test configuration
2. Verify test data
3. Check network connectivity
4. Review application logs

### Performance Degradation

1. Identify bottlenecks
2. Profile application
3. Check resource usage
4. Review recent changes

## 📚 Recursos Adicionales

- [k6 Documentation](https://k6.io/docs/)
- [JMeter Best Practices](https://jmeter.apache.org/usermanual/best-practices.html)
- [Performance Testing Guide](https://www.guru99.com/performance-testing.html)

---

**Versión:** 1.0.0  
**Última actualización:** Diciembre 2025  
**Total líneas:** 1,100+

