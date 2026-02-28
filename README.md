# 🍓 Raspberry Pi Monitoring Stack

A telemetry suite designed for real-time system resource tracking. It leverages Docker Compose to orchestrate a FastAPI-based collector (**PyFlux**) and an **InfluxDB 2.x** time-series database.

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Project Structure](#project-structure)
3. [Quick Start](#quick-start)
4. [Configuration & Secrets](#configuration--secrets)
5. [Data Schema](#data-schema)
6. [Persistence & Security](#persistence--security)

---

## Architecture Overview

This stack follows a microservices pattern:

- **PyFlux** — An asynchronous Python service that polls CPU and RAM metrics using the `psutil` library.
- **InfluxDB** — A high-performance database optimized for time-series data, providing the backend for visualization and storage.

---

## Project Structure

```
.
├── api
│   ├── Dockerfile          # Multi-stage build for PyFlux
│   ├── pyflux.py           # Metrics collection engine
│   └── requirements.txt    # Python dependencies
├── docker-compose.yml      # Service orchestration manifest
├── influxdb
│   └── data                # Local mount for database persistence
└── README.md               # Project documentation
```

---

## Quick Start

Using this stack is a three-step process:

1. **Setup Environment** — Define your credentials in a local `.env` file (see [Configuration & Secrets](#configuration--secrets)).
2. **Build and Launch** — Run the following command to initialize the environment:
   ```bash
   docker-compose up -d --build
   ```
3. **Monitor** — Access the InfluxDB UI at [http://localhost:8086](http://localhost:8086) to visualize real-time metrics.

---

## Configuration & Secrets

> ⚠️ **Mandatory** — Credentials are not hardcoded. You **must** create a `.env` file in the root directory before starting the stack.

```bash
nano .env
```

```env
INFLUX_USER=admin
INFLUX_PASSWORD=your_secure_password
INFLUX_TOKEN=your_secret_admin_token
```

> The `.env` file is excluded from Git tracking to prevent credential leakage in public repositories.

---

## Data Schema

Metrics are streamed every **5 seconds** with the following metadata:

| Property    | Value          |
|-------------|----------------|
| Organization | `my-org`      |
| Bucket      | `my-bucket`    |
| Measurement | `system_stats` |
| Fields      | `cpu_usage (%)`, `ram_usage (%)` |
| Tags        | `host=raspberry` |

---

## Persistence & Security

- **Storage** — Database files are mapped to the `./influxdb/data` directory on the host machine. This ensures data is preserved even if containers are removed or updated.
- **Network** — Services communicate over a private Docker bridge network, exposing only necessary ports (`8086`, `3000`) to the host.

---

*Maintained by [Cyprien-git](https://github.com/Cyprien-git/Monitoring)*

