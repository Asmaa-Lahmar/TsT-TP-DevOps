# SmartCampus

Plateforme de réservation de salles du campus — projet fil rouge DevOps.
Backend : FastAPI (Python).

## Installation

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Linux / macOS
pip install -r requirements-dev.txt
```

## Lancer l'API

```bash
uvicorn src.main:app --reload
```

Documentation interactive : http://127.0.0.1:8000/docs

## Lancer les tests

```bash
pytest --cov=src
```

## Documentation

- [Cahier des charges](docs/Cahier_des_charges_SmartCampus.md) (version Word avec diagrammes : `docs/Cahier_des_charges_SmartCampus.docx`)
- [Comparatif FastAPI / Spring Boot](docs/FastAPI_vs_SpringBoot.md)
