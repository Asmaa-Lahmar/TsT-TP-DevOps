# SmartCampus — FastAPI pour le backend ?

Oui, FastAPI est utilisable : l'énoncé n'impose aucun langage, et la stack du cahier des charges est une « proposition à confirmer ». À vérifier avec l'encadrant qu'il n'attend pas du Java.

## 1. Exemple : connexion SC-11 en FastAPI

```python
# app/main.py
from datetime import datetime, timedelta, timezone
import bcrypt, jwt
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr

app = FastAPI(title="SmartCampus API")
SECRET_KEY = "a-lire-depuis-une-variable-d-environnement"

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# Pour l'exemple ; en vrai : table User dans PostgreSQL (SQLAlchemy)
USERS = {"etudiant@campus.ma": bcrypt.hashpw(b"secret123", bcrypt.gensalt())}

@app.post("/api/auth/login")
def login(req: LoginRequest):
    hashed = USERS.get(req.email)
    if hashed is None or not bcrypt.checkpw(req.password.encode(), hashed):
        raise HTTPException(401, "E-mail ou mot de passe incorrect")  # EF-AUTH-03
    exp = datetime.now(timezone.utc) + timedelta(minutes=30)          # ENF-02
    token = jwt.encode({"sub": req.email, "exp": exp}, SECRET_KEY, algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}
```

```python
# tests/test_login.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_connexion_ok():
    r = client.post("/api/auth/login", json={"email": "etudiant@campus.ma", "password": "secret123"})
    assert r.status_code == 200 and "access_token" in r.json()

def test_mauvais_mot_de_passe():
    r = client.post("/api/auth/login", json={"email": "etudiant@campus.ma", "password": "faux"})
    assert r.status_code == 401
```

**Paquets (`requirements.txt`)** : `fastapi`, `uvicorn`, `pydantic[email]`, `bcrypt`, `PyJWT`, `httpx`, `pytest`, `pytest-cov`, `ruff`.

**Lancement** : `uvicorn app.main:app --reload`. La documentation Swagger apparaît automatiquement sur `/docs`.

**Équivalent Spring Boot** : contrôleur, service, DTO, classe de configuration Spring Security et filtre JWT. La configuration de la sécurité est la partie la plus longue.

## 2. Comparaison FastAPI / Spring Boot

| Critère | FastAPI | Spring Boot |
| --- | --- | --- |
| Prise en main | Rapide si l'équipe connaît Python | Plus longue : annotations, injection de dépendances, Spring Security |
| Quantité de code | Faible | Nettement plus élevée |
| Sécurité (JWT, rôles) | À assembler soi-même (PyJWT + dépendances FastAPI) | Spring Security complet mais complexe |
| Base de données | SQLAlchemy + Alembic (migrations) | JPA/Hibernate + Flyway |
| Tâches planifiées (rappels, RG-06, RG-09) | Rien d'intégré : APScheduler ou CronJob Kubernetes | `@Scheduled` intégré |
| Documentation API | Swagger automatique | À ajouter (springdoc-openapi) |
| Détection des erreurs | À l'exécution, sauf avec ruff et mypy | À la compilation |
| Image Docker | Plus légère, démarrage rapide | Plus lourde (JVM), démarrage plus lent |

**Recommandation** : le cours porte sur DevOps, donc un backend plus simple laisse plus de temps pour Jenkins, Docker et Kubernetes. FastAPI est un bon choix si l'équipe est à l'aise en Python ; Spring Boot reste préférable si l'encadrant attend du Java/Maven.

## 3. FastAPI et Jenkins

Pas de problème de fond : Jenkins exécute des commandes shell quel que soit le langage. Seules les commandes changent (`pip` et `pytest` au lieu de `mvn`).

```groovy
pipeline {
  agent { docker { image 'python:3.14-slim' } }
  stages {
    stage('Installer') {
      steps { sh 'python -m venv .venv && .venv/bin/pip install -r requirements.txt' }
    }
    stage('Qualité') {
      steps { sh '.venv/bin/ruff check app tests' }
    }
    stage('Tests') {
      steps { sh '.venv/bin/pytest --junitxml=rapport-tests.xml --cov=app --cov-report=xml --cov-fail-under=70' }
    }
  }
  post { always { junit 'rapport-tests.xml' } }
}
```

`--cov-fail-under=70` applique directement l'exigence ENF-11 (couverture de 70 % au moins).

### Pièges à connaître

- **Droits dans le conteneur** : Jenkins lance le conteneur avec son propre utilisateur, sans droits root. Un `pip install` direct échoue avec « Permission denied ». D'où l'environnement virtuel `.venv` créé dans le workspace.
- **SonarQube** : utiliser `sonar-scanner` au lieu du plugin Maven, avec `sonar.python.coverage.reportPaths=coverage.xml`.
- **DevSecOps (étape 8)** : `pip-audit` pour les dépendances (le support Python d'OWASP Dependency-Check est limité), Bandit ou Semgrep pour l'analyse du code. Trivy et Gitleaks fonctionnent sans changement.
