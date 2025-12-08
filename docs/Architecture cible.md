


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
│    Traefik      │   │          Keycloak            │     │         Airflow         │
│ Reverse Proxy   │   │   AuthN/AuthZ · OIDC · MFA   │     │ Scheduler · Worker      │
│ TLS, WAF, OIDC  │   └───────────────┬──────────────┘     │ Webserver · Flower UI   │
└──────┬──────────┘                   │                    └───────────┬────-────────┘
       │ HTTPS                         │ OIDC / Tokens                 │ REST / APIs
       ▼                               ▼                               ▼
┌──────────────────────────────────────────────────────────┐     ┌───────────────────────┐
│                     FastAPI Backend                       │     │      DAGs Airflow      │
│ - Ingestion API                                           │     │                       │
│ - CRUD Data                                               │     │  • ingest_csv          │
│ - Auth Keycloak (OIDC)                                    │     │  • ingest_api          │
│ - Validation / Pydantic                                   │     │  • ingest_scraper      │
│ - Serve data → Streamlit                                  │     │  • ingest_assetto      │
└──────────┬───────────────────────────────────────────────┘     └───────────┬───────────┘
           │ DB Access (TLS)                                         │ Writes to DB
           │                                                         │
           ▼                                                         ▼
     ┌──────────────────────────────┐                        ┌──────────────────────────┐
     │         PostgreSQL           │◀───────────────────────▶│       RAW / CLEAN        │
     │  - Schemas RAW + CLEAN       │                        │  · Normalized datasets   │
     │  - Least Privilege Accounts  │                        │  · History + metadata    │
     └──────────────┬───────────────┘                        └──────────────────────────┘
                    │
                    ▼
          ┌───────────────────────────────┐
          │        Streamlit Frontend      │
          │  - Visualisation Dashboards    │
          │  - Login Keycloak (OIDC)       │
          │  - App UI / Graphs / KPIs      │
          └───────────────────────────────┘

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