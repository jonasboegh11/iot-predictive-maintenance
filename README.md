# IoT Predictive Maintenance

REST API Microservice til overvågning af vindmøller via sensordata. Systemet modtager sensordata fra IoT-enheder, analyserer værdierne mod definerede grænseværdier og genererer automatisk alarmer ved overskridelser.

---

## Forudsætninger

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Python 3.11](https://www.python.org/downloads/)
- En `.env` fil i projektets rodmappe (se herunder)

---

## Kom i gang

### 1. Opret `.env` fil

Kopiér `.env.example` til `.env` og udfyld dine egne passwords:

```bash
cp .env.example .env
```

### 2. Start hele stacken

```bash
docker-compose up -d
```

Databasen og tabellerne oprettes automatisk via `init.sql` ved første opstart.

### 3. Tjek at API'et kører

```
GET http://localhost:3000/api/health
```

---

## API Endpoints

### Sensordata

| Method | Endpoint | Beskrivelse |
|--------|----------|-------------|
| `POST` | `/api/sensors/` | Send sensordata fra IoT-device |
| `GET` | `/api/sensors/` | Hent seneste 50 sensor readings |

**Eksempel på POST body:**
```json
{
    "device_id": "windmill-01",
    "sensor_type": "temperature",
    "value": 95,
    "unit": "°C"
}
```

Støttede sensor typer: `temperature`, `rpm`, `power_output`

### Alerts

| Method | Endpoint | Beskrivelse |
|--------|----------|-------------|
| `GET` | `/api/alerts/` | Hent alle alerts |
| `GET` | `/api/alerts/?device_id=windmill-01` | Filtrer på device |
| `GET` | `/api/alerts/?resolved=false` | Filtrer på uløste alerts |
| `PUT` | `/api/alerts/<id>/resolve` | Marker alert som løst |

---

## Threshold-logik

Systemet genererer automatisk alerts når sensorværdier overskrides:

| Sensor | Normal (under) | Advarsel (MEDIUM) | Kritisk (HIGH) |
|--------|---------------|-------------------|----------------|
| Temperatur | 50°C | 70°C | 90°C |
| RPM | 1200 | 1600 | 1800 |
| Effekt (kW) | 1500 | 1800 | 2100 |

Systemet overvåger også **stigende trends** i pre-warning zonen (mellem normal og advarsel).
Hvis en sensor konsekvent stiger over de sidste 5 målinger og befinder sig i denne zone,
genereres en MEDIUM alert — så man kan reagere *før* advarselgrænsen overskrides.

---

## Tech Stack

| Komponent | Teknologi |
|-----------|-----------|
| API | Python / Flask |
| Database | MySQL 8.0 |
| Monitoring | Grafana + Prometheus |
| Containerisering | Docker / Docker Compose |
| CI/CD | GitHub Actions |

---

## Nyttige kommandoer

```bash
# Start stacken
docker-compose up -d

# Stop stacken (bevar data)
docker-compose down

# Stop stacken og slet al data
docker-compose down -v

# Kør tests
pytest tests/

# Genbyg API container
docker-compose up --build -d
```

---

## Tjenester

| Tjeneste | URL |
|----------|-----|
| API | http://localhost:3000 |
| Grafana | http://localhost:3001 |
| Prometheus | http://localhost:9090 |

Grafana login: `admin` / `admin`