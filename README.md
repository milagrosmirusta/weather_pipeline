# Weather Data Pipeline

ETL pipeline completo para ingestión, transformación y carga de datos meteorológicos con orquestación en Dagster, almacenamiento en PostgreSQL y modelo dimensional para análisis BI.

## Tabla de Contenidos

- [Descripción del Proyecto](#descripcion-del-proyecto)
- [Arquitectura](#arquitectura)
- [Tecnologías Utilizadas](#tecnologias-utilizadas)
- [Modelo de Datos](#modelo-de-datos)
- [Requisitos Previos](#requisitos-previos)
- [Instalación y Configuración](#instalacion-y-configuracion)
- [Ejecución del Pipeline](#ejecucion-del-pipeline)
- [Generación de Datos Históricos](#generacion-de-datos-historicos)
- [Scheduling Automático](#scheduling-automatico)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Mejoras Futuras](#mejoras-futuras)

---

## Descripción del Proyecto

Pipeline de datos end-to-end que:
1. **Ingesta** datos meteorológicos de múltiples ciudades argentinas desde OpenWeather API
2. **Transformación** los datos crudos en un modelo dimensional (esquema estrella)
3. **Carga** los datos en un Data Warehouse PostgreSQL
4. **Orquesta** la ejecución automática mediante Dagster con scheduling horario


---

## Arquitectura
```
┌─────────────────┐
│ OpenWeather API │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│  Dagster Asset Pipeline │
│  ┌──────────────────┐   │
│  │ 1. ingest_weather│   │ ─── Extrae datos de la API
│  └─────────┬────────┘   │
│            ▼             │
│  ┌──────────────────────┐│
│  │ 2. transform_weather││ ─── Crea dims + facts
│  └─────────┬────────────┘│
│            ▼             │
│  ┌──────────────────┐   │
│  │ 3. load_to_dw    │   │ ─── Inserta en Postgres
│  └──────────────────┘   │
└─────────┬───────────────┘
          │
          ▼
┌───────────────────────┐
│   PostgreSQL DW       │
│   (Modelo Estrella)   │
│                       │
│  ┌─────────────────┐ │
│  │ dim_conditions  │ │
│  │ dim_city        │ │
│  │ fact_weather    │ │
│  └─────────────────┘ │
└───────────────────────┘
          │
          ▼
    ┌─────────────┐
    │  Power BI   │ (opcional)
    │  Dashboard  │
    └─────────────┘
```

**Flujo de Datos**:
- **Raw Zone**: Archivos Parquet locales (`data/raw/`) para auditoría
- **Transformación**: Pandas para limpieza y estructuración
- **SQL**: PostgreSQL con modelo dimensional optimizado para analytics

---

## Tecnologías Utilizadas

| Categoría | Tecnología | Versión |
|-----------|-----------|---------|
| **Orquestación** | Dagster | 1.7.16 |
| **Base de Datos** | PostgreSQL | 15 |
| **Procesamiento** | Pandas | 2.1.3 |
| **Procesamiento** | Polars | 0.19.13 |
| **Containerización** | Docker | - |
| **API** | OpenWeather API | Free tier |
| **Lenguaje** | Python | 3.12 |

---

## Modelo de Datos

### Esquema Estrella (Star Schema)
```sql
┌─────────────────────┐
│     dim_conditions  │
├─────────────────────┤
│ condition_id (PK)   │
│ main                │
│ description         │
└─────────────────────┘
          ▲
          │
          │ FK
          │
┌─────────┴───────────────────────────────────────┐
│                   fact_weather                  │
├─────────────────────────────────────────────────┤
│ id (PK)                                         │
│ city_id (FK) ────────────────────────┐          │
│ condition_id (FK)                    │          │
│ date                                 │          │
│ temp                                 │          │
│ feels_like                           │          │
│ humidity                             │          │
│ wind_speed                           │          │
│ wind_deg                             │          │
│ pressure                             │          │
│ visibility                           │          │
│ created_at                           │          │
└──────────────────────────────────────┼──────────┘
                                       │
                                       │ FK
                                       ▼
                  ┌──────────────────────────┐
                  │         dim_city         │
                  ├──────────────────────────┤
                  │ city_id (PK)             │
                  │ city_name                │
                  │ country                  │
                  │ latitude                 │
                  │ longitude                │
                  └──────────────────────────┘

```


## Requisitos Previos

- **Python 3.12+**
- **Docker Desktop** (para PostgreSQL)
- **Git**
- **OpenWeather API Key** (gratuita): [Registrarse aquí](https://openweathermap.org/api)

---

## Instalación y Configuración

### 1. Clonar el repositorio
```bash
git clone https://github.com/milagrosmirusta/weather_pipeline.git
cd weather_pipeline
```

### 2. Crear entorno virtual e instalar dependencias
```bash
# Crear virtual environment
python -m venv venv

# Activar (Windows)
venv\Scripts\activate

# Activar (Linux/Mac)
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Levantar PostgreSQL con Docker
```bash
docker run --name weather_postgres \
  -e POSTGRES_PASSWORD=weather123 \
  -e POSTGRES_DB=weather_dw \
  -p 5432:5432 \
  -d postgres:15
```

**Verificar** que esté corriendo:
```bash
docker ps
```

### 4. Configurar variables de entorno

Crear archivo `.env` en la raíz del proyecto:
```env
# OpenWeather API
OPENWEATHER_API_KEY=tu_api_key_aqui

# PostgreSQL
DB_HOST=localhost
DB_PORT=5432
DB_NAME=weather_dw
DB_USER=postgres
DB_PASSWORD=weather123
```

> ⚠️ **Importante**: Nunca commitear el archivo `.env` a Git (ya está en `.gitignore`)

### 5. Inicializar las tablas en PostgreSQL
```bash
python sql/init_db.py
python sql/migrate_add_columns.py

(Esto fue por un error, lo correcto sería modificar init_db y agregar en create_tables.sql todas las columnas incluidas en add_columns.sql, pero como el proyecto ya estaba "productivo" lo solucioné de esta manera)
```

### 6. Configurar DAGSTER_HOME

**Windows (PowerShell)**:
```powershell
$env:DAGSTER_HOME = "$PWD\dagster_home"
```

**Linux/Mac**:
```bash
export DAGSTER_HOME=$(pwd)/dagster_home
```

>  **Tip**: Crear un script `set_env.ps1` o `set_env.sh` para automatizar esto.

---

## Ejecución del Pipeline

### Ejecución Manual (una vez)

**Opción A: Desde Dagster UI**

1. Iniciar el webserver:
```bash
dagster dev
```

2. Abrir navegador en `http://localhost:3000`

3. Ir a **Assets** → **Materialize all**

**Opción B: Desde CLI**
```bash
dagster asset materialize -m dagster_project --select "*"
```

### Verificar los datos
```bash
python check_data.py
```

Output esperado:
```
Datos en el Data Warehouse:
========================================
dim_conditions: X registros
dim_city: Y registros
fact_weather: Z registros
```

---

## Generación de Datos Históricos (Backfill)

Para simular un ambiente productivo con datos históricos de los últimos 30 días:
```bash
python dagster_project/backfill_historical_data.py
```

Este script:
- Genera datos para **30 días** hacia atrás
- Consulta la API de OpenWeather y simula variaciones históricas
- Inserta **~210 registros** (7 ciudades × 30 días)
- Tiempo de ejecución: ~2-3 minutos

> **Nota**: En producción real, esto se reemplazaría por una API histórica o acumulación natural de datos a lo largo del tiempo.

---

## Scheduling Automático

El pipeline está configurado para ejecutarse **automáticamente cada hora**.

### Activar el Schedule

**1. Iniciar el Dagster Daemon** (en una terminal separada):
```bash
# Terminal 1: Webserver
dagster dev

# Terminal 2: Daemon (ejecutor de schedules)
dagster-daemon run
```

**2. Activar el schedule en la UI**:
- Ir a `http://localhost:3000`
- Click en **Overview** → **Schedules**
- Activar el toggle de **weather_hourly**

**3. Verificar**:
- El schedule correrá en el **minuto 0 de cada hora** (ej: 14:00, 15:00, etc.)
- Ver ejecuciones en la pestaña **Runs**

### Configuración del Schedule
```python
# dagster_project/__init__.py

weather_schedule = ScheduleDefinition(
    name="weather_hourly",
    job=weather_job,
    cron_schedule="0 * * * *"  
)
```
---

## Estructura del Proyecto
```
weather_pipeline/
├── dagster_project/           # Código principal del pipeline
│   ├── __init__.py           # Definiciones de Dagster (assets, jobs, schedules)
│   ├── assets/               # Assets del pipeline (ETL steps)
│   │   ├── __init__.py
│   │   ├── ingestion.py      # Ingestión desde API
│   │   ├── transformation.py # Transformación a modelo estrella
│   │   └── load.py           # Carga a PostgreSQL
│   ├── resources/            # Clientes reutilizables
│   │   ├── __init__.py
│   │   ├── api_client.py     # Cliente OpenWeather API
│   │   └── db_client.py      # Cliente PostgreSQL
│   └── backfill_historical_data.py  # Script para generar datos históricos
│
├── data/                     # Zona de datos locales
│   ├── raw/                  # Archivos Parquet crudos (auditoría)
│   └── processed/            # Datos procesados (opcional)
│
├── sql/                      # Scripts SQL
│   ├── create_tables.sql     # DDL del modelo dimensional
│   └── init_db.py            # Script de inicialización de DB
│
├── dagster_home/             # Metadata de Dagster (generado)
│
├── .env                      # Variables de entorno (NO commitear)
├── .gitignore
├── requirements.txt          # Dependencias Python
├── pyproject.toml            # Configuración de Dagster
├── README.md                 # Este archivo
├── check_data.py             # Utilidad para verificar datos en DB
└── set_env.ps1               # Script helper para DAGSTER_HOME (Windows)
```

---

## Workflow Típico

### Desarrollo Local
```bash
# 1. Levantar infraestructura
docker start weather_postgres

# 2. Activar entorno
venv\Scripts\activate
$env:DAGSTER_HOME = "$PWD\dagster_home"

# 3. Desarrollar/probar assets
dagster dev

# 4. Ejecutar manualmente desde UI
# (materializar assets individualmente para debugging)
```

### Simulación de Producción
```bash
# 1. Backfill de datos históricos
python dagster_project/backfill_historical_data.py

# 2. Iniciar servicios
dagster dev                # Terminal 1
dagster-daemon run         # Terminal 2

# 3. Activar schedule en UI

# 4. Dejar corriendo para acumular datos
# (configurar PC para no suspender)
```

---

## Mejoras Futuras / Roadmap

### Corto Plazo
- [ ] **Dashboard Power BI** con métricas clave (temperatura promedio, tendencias, comparaciones)
- [ ] **Alertas** via email/Slack si falla el pipeline
- [ ] **Tests unitarios** para funciones de transformación
- [ ] **Data quality checks** (valores nulos, rangos válidos, etc.)

### Mediano Plazo
- [ ] **Particionamiento** de `fact_weather` por mes para mejor performance
- [ ] **Retry logic** con backoff exponencial
- [ ] **Monitoring** con métricas de Dagster (duración, success rate)
- [ ] **CI/CD** con GitHub Actions (tests, linting, deploy)

### Producción
- [ ] **Deployment en AWS**:
  - ECS/EKS para Dagster
  - RDS para PostgreSQL
  - S3 para raw data
  - CloudWatch para logs
- [ ] **Secrets management** con AWS Secrets Manager o HashiCorp Vault
- [ ] **Infraestructura como código** con Terraform
- [ ] **API histórica** para backfill real (vs simulación)
- [ ] **Escalamiento horizontal** para múltiples pipelines simultáneos

---

## Notas Técnicas


### Limitaciones 

- **API gratuita** limitada a 1000 llamadas/día (suficiente para este proyecto)
- **Backfill simulado** (no usa API histórica real por costos)
- **Single-threaded**: Procesa ciudades secuencialmente (paralelizable si se necesita)
- **Sin autenticación**: Dagster UI expuesta sin auth (ok para local, NO para prod)

---

## Contribuciones

Este es un proyecto de portfolio personal, pero sugerencias y feedback son bienvenidos:
- Abrir un **Issue** para bugs o preguntas
- Enviar **Pull Request** con mejoras

---

