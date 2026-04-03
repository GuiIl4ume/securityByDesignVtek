# 🚗 VTEK — Architecture Automobile Sécurisée

[![Security by Design](https://img.shields.io/badge/Security-by%20Design-blue)](docs/Architecture%20cible.md)
[![OWASP Top 10](https://img.shields.io/badge/OWASP-A02%20A03%20A05%20A06%20A09-orange)](SECURITY_UPDATE_SUMMARY.md)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-green)](vtek-project/requirements.txt)
[![Docker Compose](https://img.shields.io/badge/Docker-Compose-2496ED)](vtek-project/docker-compose.yml)

> **Plateforme intelligente de collecte et analyse de performances automobiles** avec garanties de sécurité, intégrité et confidentialité par conception.

## 🎯 À propos

VTEK collecte automatiquement les données de véhicules (`puissance`, `poids`, `aérodynamisme`, etc.) et entraîne un modèle ML pour prédire les performances. L'application repose sur une **architecture 3-tiers sécurisée** avec validation stricte des entrées, gestion des secrets externalisée, et conteneurs non-root.

### 📐 Architecture Tier 3

```
┌─────────────────────────────────────────────────────┐
│  Tier 1 : Présentation (Streamlit Frontend)         │
│  Port 8501 - Interface utilisateur interactive      │
└────────────────┬────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────┐
│  Tier 2 : Application (FastAPI Backend)             │
│  Port 8000 - API REST avec validation Pydantic      │
│  ├─ /cars (GET) - Récupérer les automobiles         │
│  ├─ /cars/ingest (POST) - Insérer les données       │
│  ├─ /predict/max_speed (POST) - Prédiction ML       │
│  └─ /model/train (POST) - Entraînement              │
└────────────────┬────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────┐
│  Tier 3 : Données (PostgreSQL 17)                   │
│  Port 5432 - Base relationnelle sécurisée           │
│  ├─ Authentification BD isolée                      │
│  ├─ Health checks automatiques                      │
│  └─ Volumes persistants chiffrés                    │
└─────────────────────────────────────────────────────┘
```

## 👥 Équipe

| Rôle | Contributeur | Responsabilité |
|------|---|---|
| 🔒 Sécurité | Guillaume A. | Conformité OWASP, gestion des risques |
| 🏗️ Tech Lead | Simon R. | Architecture système, reviews |
| 🧪 QA | Eric J. | Tests, validation, CI/CD |
| 📊 PM | Nicolas P. | Planning, documentation, stakeholders |

## 📚 Documentation

| Document | Accès | Contenu |
|----------|-------|---------|
| **Architecture Cible** | [docs/Architecture cible.md](docs/Architecture%20cible.md) | Principes Security by Design, modèle threat |
| **Tableau de Bord** | [docs/VTEK - Kanban.md](docs/VTEK%20-%20Kanban.md) | Tâches par rôle, sprint planning |
| **Work Breakdown** | [docs/VTEK - WBS.md](docs/VTEK%20-%20WBS.md) | Décomposition du projet, jalons |
| **Schéma Visuel** | [docs/draw/architecture.excalidraw.md](docs/draw/architecture.excalidraw.md) | Diagramme détaillé des flux |
| **Mise à Jour Sécu** | [SECURITY_UPDATE_SUMMARY.md](SECURITY_UPDATE_SUMMARY.md) | 9 commits OWASP A02-A09 |

## 🚀 Démarrage Rapide

### Prérequis

- **Docker** ≥ 24.0 et **Docker Compose** ≥ 2.20
- **Git** pour cloner le dépôt
- Pas de dépendances Python locales requises (tout dans les conteneurs)

### Installation & Lancement

```bash
# 1. Cloner et entrer dans le dépôt
git clone https://github.com/GuiIl4ume/securityByDesignVtek.git
cd securityByDesignVtek

# 2. Configurer les secrets
cp vtek-project/.env.example vtek-project/.env
# ⚠️ Édite vtek-project/.env et remplace CHANGE_ME_IN_PRODUCTION par un mot de passe fort
nano vtek-project/.env

# 3. Démarrer les services
cd vtek-project
docker-compose up -d

# 4. Accéder aux applications
# Frontend    : http://localhost:8501 (Streamlit)
# Backend API : http://localhost:8000 (FastAPI docs)
# Database    : localhost:5432 (PostgreSQL)

# 5. Vérifier la santé
docker-compose ps
```

### Arrêt gracieux

```bash
cd vtek-project
docker-compose down
```

## 🔐 Sécurité — Mises à jour Récentes

La branche `main` inclut **9 commits de sécurité** corrigeant les vulnérabilités OWASP :

| Vulnérabilité | Fix | Commit |
|---|---|---|
| **A02** - Cryptographic Failures | Secrets externalisés, `.env.example` | 3 commits |
| **A03** - Injection | Validation stricte Pydantic + `Literal` | 1 commit |
| **A05** - Security Misconfiguration | Python 3.12-slim, conteneurs non-root, timeouts HTTP | 2 commits |
| **A06** - Vulnerable Components | Dépendances épinglées, versions fixes | 1 commit |
| **A09** - Logging & Monitoring | Erreurs masquées, exceptions typées | 2 commits |

👉 Détails : [SECURITY_UPDATE_SUMMARY.md](SECURITY_UPDATE_SUMMARY.md)

## 🛠️ Contribution

### Configuration Locale (Développement)

### Workflow Pull Request

1. **Fork puis clone le dépôt** (ou crée une branche si collaborateur)
   ```bash
   git clone https://github.com/YOUR_USERNAME/securityByDesignVtek.git
   cd securityByDesignVtek
   ```

2. **Créer une branche feature/fix**
   ```bash
   git checkout -b feature/nom-de-votre-tache
   # ou
   git checkout -b fix/nom-du-bug
   ```

3. **Développer & commiter**
   ```bash
   git add .
   git commit -m "feat: description claire respectant Conventional Commits"
   ```
   
   Format recommandé : `feat|fix|refactor|docs|security: message`

4. **Pousser & créer une PR**
   ```bash
   git push origin feature/nom-de-votre-tache
   # Ouvrir la PR sur GitHub avec description détaillée
   ```

5. **Code Review**
   - Au moins 1 review obligatoire avant merge
   - Tous les checks GitHub Actions doivent passer
   - Squash & merge recommandé pour garder un historique propre

### Bonnes Pratiques

✅ **À Faire**
- Travailler sur une branche dédiée par feature
- Commits atomiques avec messages clairs
- Mettre à jour `vtek-project/.env.example` si nouvelles variables
- Tester localement avec Docker Compose avant de pousser
- Synchroniser régulièrement : `git pull origin main`

❌ **À Éviter**
- Ne JAMAIS committer `.env` (utiliser `.gitignore`)
- Éviter les secrets en dur dans le code
- Pas de gros commits sans description
- Pas de merge à main sans PR

## 🎓 Points d'Apprentissage

Ce projet démontre :

- **Architecture microservices** avec Docker Compose et orchestration
- **Security by Design** : validation en entrée, secrets externalisés, non-root
- **ML en production** : scikit-learn avec joblib, réentraînement dynamique
- **API REST moderne** : FastAPI avec dépendances, validation Pydantic v2
- **Frontend interactif** : Streamlit pour visualisation temps réel
- **CI/CD** : GitHub Actions, branchement, PR workflow

## 🛡️ Principes Security by Design

### Modèle Zéro Confiance (Zero Trust)

- Aucune confiance implicite, validation à chaque couche
- Chaque requête authentifiée et autorisée
- Segmentation réseau via Docker networks isolés

### Gestion des Secrets

```
❌ AVANT: DATABASE_URL="postgresql://user:password@host:5432/db"
✅ APRÈS: Chargé depuis .env → variables d'environnement Docker
```

- `.env` jamais commité (`.gitignore`)
- `.env.example` comme template pour l'onboarding
- Support des secrets Docker Swarm/Kubernetes

### Sécurité des Dépendances

- **Versions épinglées** : Empêche les résolutions vers des versions vulnérables
- **Python 3.12-slim** : Version stable avec tous les patchs OpenSSL
- **Scanning régulier** : `pip-audit` ou Dependabot recommandés

### Validation des Entrées (OWASP A03)

```python
class CarSchema(BaseModel):
    power: int = Field(..., gt=0, le=5000)           # Validé à l'entrée
    fuel_type: Literal["Gasoline", "Diesel", ...]   # Enum stricte
    year: int = Field(..., ge=1886, le=2100)        # Bornes métier
```

### Conteneurs Non-Root

```dockerfile
RUN useradd -r -s /sbin/nologin appuser
USER appuser  # ← Pas d'exécution en root
```

### Gestion des Erreurs

```python
# ❌ Avant
raise HTTPException(status_code=500, detail=str(e))  # Fuite de la stack trace

# ✅ Après
raise HTTPException(status_code=500, detail="Erreur lors du traitement")
```

### Timeouts & Résilience

- Requêtes HTTP sortantes : timeout 30s (prévient les blocages infinis)
- Health checks PostgreSQL : 5s interval
- Retry logic sur ETL : Gestion des défaillances réseau

> En savoir plus : [Architecture cible.md](docs/Architecture%20cible.md)

## 📞 Support & Contact

- 🐛 **Bug Report** : Créer une issue sur GitHub
- 💡 **Feature Request** : Discussion tab du repo
- 📧 **Email** : Voir les collaborators du projet
- 📖 **Questions** ? Consulte le [Kanban](docs/VTEK%20-%20Kanban.md) ou la documentation

## 📄 Licence

Ce projet est fourni à titre d'exemple pédagogique pour les principes **Security by Design**.

---

**Dernière mise à jour** : avril 2026 | **Version** : 2.0 (Sécurité renforcée)


