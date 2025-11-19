# CORFO IDIE Los Ríos – ETL + Visualizaciones

Pipeline para extraer, transformar y cargar información de proyectos CORFO priorizando principios de Clean Code y SOLID. Además, el repositorio incluye visualizaciones interactivas en `docs/` para consumo rápido por analistas y para su publicación en la web institucional.

## Estructura del proyecto

```
corfo-idie-los-rios-analytics/
├── config/                 # Archivos de configuración declarativa (YAML, JSON)
├── data/
│   ├── raw/                # Datos originales (solo lectura)
│   ├── interim/            # Salidas temporales/no versionadas
│   └── processed/          # Entregables del ETL (no versionados)
├── docs/                   # Visualizaciones HTML y documentación funcional
├── notebooks/              # Exploración ad-hoc (mantener limpios)
├── scripts/                # Entrypoints/CLI del proyecto
├── src/
│   ├── core/               # Configuración y utilidades compartidas
│   ├── etl/                # Capas Extract/Transform/Load
│   └── pipelines/          # Orquestadores de ETL
└── tests/                  # Pruebas unitarias
```

## Requisitos

- macOS / Linux
- Python 3.11+
- `pip` actualizado

## Configuración del entorno

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Crear un archivo `.env` (opcional) para sobreescribir rutas del ETL; cualquier variable definida ahí prevalece sobre `config/settings.yaml`.

## Ejecución del ETL

1. Ajusta `config/settings.yaml` si necesitas cambiar rutas de entrada/salida.
2. Ejecuta el script principal:
   ```bash
   python scripts/run_etl.py --config config/settings.yaml
   ```
3. El resultado se genera como `data/processed/corfo_projects.parquet` y `data/processed/corfo_projects.csv`.

## Visualizaciones interactivas (carpeta `docs/`)

- `docs/index.html` concentra los tres gráficos principales (financiamiento acumulado, evolución del financiamiento y proyectos adjudicados). Cada vista se abre desde el navbar y cuenta con botón de tema claro/oscuro y animación de carga.
- También se mantienen las páginas individuales (`docs/los_rios_financiamiento_bar.html`, `docs/los_rios_financiamiento_innova.html`, `docs/los_rios_proyectos_line.html`) por si se necesita incrustarlas de forma independiente.
- Para previsualizar localmente las visualizaciones basta con levantar un servidor estático desde la carpeta `docs/`:
   ```bash
   cd docs
   python -m http.server 8000
   ```
   Luego abre `http://localhost:8000/index.html` en tu navegador.

## Publicación / Deploy

1. Cada vez que se actualicen los datos del ETL, vuelve a generar los artefactos en `docs/` si es necesario.
2. Sube el contenido del repositorio al remoto `https://github.com/ObservaLosRios/corfo-idie-los-rios-analytics.git` para compartirlo con el equipo CER.
3. Opcional: habilita GitHub Pages apuntando a la carpeta `docs/` para exponer las visualizaciones públicamente.

## Calidad y buenas prácticas

- Código organizado por responsabilidad (SRP) y utilizando inyección de dependencias mínima via objetos de configuración.
- Conversores puros en la capa `transform` permiten test unitarios sencillos.
- Validación temprana de esquemas y normalización de tipos para impedir valores ambiguos.
- Logging estructurado y manejo explícito de errores para cada etapa del pipeline.

## Próximos pasos sugeridos

- Agregar CI (por ejemplo, GitHub Actions) para ejecutar pruebas automáticamente.
- Incorporar validaciones de datos con `great_expectations` o `pandera` si se requiere chequeo estadístico periódico.
- Automatizar la publicación de `docs/` (GitHub Pages o flujo de despliegue hacia el sitio ObservaLosRíos) después de cada corrida de ETL.
