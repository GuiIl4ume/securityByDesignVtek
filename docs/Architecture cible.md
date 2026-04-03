


> **État d'implémentation (avril 2026)** : Les composants marqués ✅ sont déployés et opérationnels. Les composants sans marqueur font partie de l'architecture cible.

```
                                         ┌──────────────────────────┐
                                         │        GitHub Repo       │
                                         │  Code: Front, Back, ETL  │
                                         └───────────────┬──────────┘
                                                         │
                                                         ▼
                                     ┌─────────────────────────────────────┐
                                     │         GitHub Actions CI/CD        │
                                     │  - Tests / Lint / SAST (Bandit)     │
                                     │  - Build Docker images              │
                                     │  - Trivy Scan + Cosign Signature    │
                                     │  - Deploy (SSH / K8s / Compose)     │
                                     └───────────────┬─────────────────────┘
                                                     │
                                                     ▼
        ┌─────────────────────────────────────────────────────────────────-─────────┐
        │                         Infrastructure Containerisée                      │
        │                          (Docker Compose / Kubernetes)                    │
        └───────────┬───────────────────────────────────────────────────────────────┘
                    │
   ┌────────────────┼─────────────────────────────────────────────────┐
   │                │                                                 │
   ▼                ▼                                                 ▼
┌────────────-────┐   ┌──────────────────────────────┐     ┌──────────────-──────────┐
│  KrakenD ✅     │   │          Keycloak            │     │         Airflow         │
│ API Gateway     │   │   AuthN/AuthZ · OIDC · MFA   │     │ Scheduler · Worker      │
│ :8080 (déployé) │   └───────────────┬──────────────┘     │ Webserver · Flower UI   │
│ Rate limit, CORS│                   │                    └───────────┬────-────────┘
│ Security headers│                   │                               │ REST / APIs
│ Prometheus tel. │                   │                               │
└──────┬──────────┘                   │                               │
       │ (backend isolé)              │ OIDC / Tokens                 │
       ▼                               ▼                               ▼
┌──────────────────────────────────────────────────────────┐     ┌───────────────────────┐
│               FastAPI Backend ✅                          │     │      DAGs Airflow      │
│ - Ingestion API                                           │     │                       │
│ - CRUD Data                                               │     │  • ingest_csv          │
│ - Auth Keycloak (OIDC)                                    │     │  • ingest_api          │
│ - Validation / Pydantic ✅                                │     │  • ingest_scraper      │
│ - Serve data → Streamlit                                  │     │  • ingest_assetto      │
│ - /health + /metrics ✅                                   │     │                       │
└──────────┬───────────────────────────────────────────────┘     └───────────┬───────────┘
           │ DB Access (TLS)                                         │ Writes to DB
           │                                                         │
           ▼                                                         ▼
     ┌──────────────────────────────┐                        ┌──────────────────────────┐
     │       PostgreSQL 17 ✅       │◀───────────────────────▶│       RAW / CLEAN        │
     │  - Schemas RAW + CLEAN       │                        │  · Normalized datasets   │
     │  - Least Privilege Accounts  │                        │  · History + metadata    │
     └──────────────┬───────────────┘                        └──────────────────────────┘
                    │
                    ▼
          ┌───────────────────────────────┐     ┌───────────────────────────────┐
          │    Streamlit Frontend ✅       │     │   Prometheus + Grafana ✅     │
          │  - Visualisation Dashboards    │     │  - Métriques backend/gateway  │
          │  - Login Keycloak (OIDC)       │     │  - Audit logs structurés      │
          │  - App UI / Graphs / KPIs      │     │  - Alertes 4xx/5xx            │
          └───────────────────────────────┘     └───────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────────────

                Ingestion Sources (déclenchées par ETL Airflow)

                       ┌─────────────── Source 1 ───────────────┐
                       ▼                                         │
             ┌──────────────────┐                                │
             │ CSV Upload / S3  │───────────────┐                │
             │ Validation / RAW │               │                │
             └──────────────────┘               ▼                │
                                                (Airflow DAG ingest_csv)
                       ┌─────────────── Source 2 ───────────────┐
                       ▼                                         │
      ┌──────────────────────────────────────────────────┐       │
      │ APIs externes (auth token / OAuth2 / partners)   │───────┘
      └──────────────────────────────────────────────────┘
                                         ▼
                       (Airflow DAG ingest_api)

                       ┌─────────────── Source 3 ───────────────┐
                       ▼                                         │
           ┌───────────────────────────────────────┐            │
           │ Web Scraping (Requests/Playwright)     │────────────┘
           └───────────────────────────────────────┘
                                         ▼
                       (Airflow DAG ingest_scraper)

                       ┌─────────────── Source 4 ───────────────┐
                       ▼                                         │
     ┌────────────────────────────────────────────────────────┐   │
     │ Assetto Corsa Telemetry (UDP plugin → microservice)   │────┘
     └────────────────────────────────────────────────────────┘
                                         ▼
                       (Airflow DAG ingest_assetto)
```