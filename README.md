# UrbanHub Park – Documentation CI/CD
## EC03 – Piloter l’intégration et le déploiement continus
### Bloc 3 – Intégration et Déploiement Continus (CI/CD)

---

## Sommaire

1. [Présentation générale](#1-présentation-générale)  
2. [Contexte du projet](#2-contexte-du-projet)  
3. [Objectifs du pipeline CI/CD](#3-objectifs-du-pipeline-cicd)  
4. [Architecture technique](#4-architecture-technique)  
5. [Conteneurisation de l’application](#5-conteneurisation-de-lapplication)  
6. [Orchestration avec Docker Compose](#6-orchestration-avec-docker-compose)  
7. [Présentation du pipeline GitLab CI/CD](#7-présentation-du-pipeline-gitlab-cicd)  
8. [Détail des jobs du pipeline](#8-détail-des-jobs-du-pipeline)  
9. [Stratégie de test](#9-stratégie-de-test)  
10. [Pratiques DevSecOps](#10-pratiques-devsecops)  
11. [Correspondance avec les compétences évaluées](#11-correspondance-avec-les-compétences-évaluées)  
12. [Risques et limites](#12-risques-et-limites)  
13. [Recommandations d’amélioration](#13-recommandations-damélioration)  
14. [Conclusion](#14-conclusion)  
15. [Annexes](#15-annexes)  

---

# 1. Présentation générale

Ce document présente la solution de **pipeline CI/CD** mise en place pour le projet **UrbanHub Park**, dans le cadre de l’épreuve **EC03 – Piloter l’intégration et le déploiement continus**.

L’objectif est de démontrer la capacité à :

- automatiser la validation du code,
- intégrer les tests,
- intégrer des contrôles de sécurité,
- automatiser le déploiement,
- documenter la solution de manière professionnelle et exploitable.

Ce document constitue la **Partie 2 – Documentation technique du pipeline**.

---

# 2. Contexte du projet

## 2.1 Présentation du module UrbanHub Park

UrbanHub Park est un module applicatif du projet **UrbanHub**, orienté vers la **gestion du stationnement**.

Dans un contexte de ville intelligente, ce service peut être utilisé pour :

- suivre l’état des places de stationnement,
- exposer des données via une API,
- centraliser des informations liées au stationnement urbain.

Dans le cadre de cette épreuve, l’application est représentée sous la forme d’une **API Flask** simple, conteneurisée et déployable automatiquement.

---

## 2.2 Enjeux DevOps / CI/CD

Le projet doit répondre à plusieurs exigences :

- garantir des déploiements reproductibles,
- éviter les erreurs manuelles,
- automatiser la validation technique,
- intégrer des contrôles de sécurité,
- permettre une maintenance simple et rapide.

La mise en place d’un pipeline CI/CD permet donc de répondre à ces besoins en structurant le cycle de vie du projet.

---

# 3. Objectifs du pipeline CI/CD

Le pipeline mis en œuvre a pour objectif de fournir une chaîne automatisée capable de :

1. **Vérifier la validité du code source**
2. **Exécuter automatiquement les tests**
3. **Analyser la sécurité des dépendances**
4. **Déployer automatiquement l’application**
5. **Garantir un environnement de déploiement cohérent et reproductible**

Cette logique s’inscrit dans une démarche :

- **CI** : Intégration Continue
- **CD** : Déploiement Continu
- **DevSecOps** : Intégration de la sécurité dans le cycle de livraison

---

# 4. Architecture technique

## 4.1 Technologies utilisées

La solution repose sur les composants suivants :

- **GitLab** : hébergement du dépôt et exécution du pipeline
- **GitLab CI/CD** : orchestration des jobs
- **Python 3.11** : langage de développement
- **Flask** : framework de l’API
- **SQLite** : base de données locale
- **Docker** : conteneurisation
- **Docker Compose** : orchestration du service
- **pytest** : exécution des tests
- **pip-audit** : audit de sécurité des dépendances

---

## 4.2 Vue logique de l’architecture

L’application repose sur :

- un **conteneur Docker** contenant l’API Flask,
- un **volume Docker** pour persister les données SQLite,
- un **fichier `.env`** pour la configuration,
- un **pipeline GitLab CI/CD** pour automatiser les opérations.

---

## 4.3 Flux de fonctionnement global

Le flux général est le suivant :

1. Le développeur pousse le code sur GitLab
2. Le pipeline CI/CD se déclenche automatiquement
3. Les étapes de validation s’exécutent
4. Si les contrôles sont valides, l’application est déployée
5. Un test de disponibilité final vérifie que l’application fonctionne

---

# 5. Conteneurisation de l’application

## 5.1 Objectif du Dockerfile

Le `Dockerfile` permet de construire une image exécutable de l’application.

Cette approche présente plusieurs avantages :

- portabilité,
- reproductibilité,
- standardisation de l’environnement,
- simplification du déploiement.

---

## 5.2 Dockerfile retenu

```dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /app/requirements.txt

COPY app.py /app/app.py
COPY database.py /app/database.py
COPY models.sql /app/models.sql

RUN groupadd -r appuser && useradd -r -g appuser -d /app -s /usr/sbin/nologin appuser

RUN mkdir -p /app/data \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 5000

CMD ["python", "app.py"]
```

---

## 5.3 Analyse technique du Dockerfile

### a) Image de base

```dockerfile
FROM python:3.11-slim
```

Cette image a été choisie pour :

- sa compatibilité avec Python 3.11,
- sa légèreté,
- sa pertinence pour une API Flask.

---

### b) Variables d’environnement Python

```dockerfile
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
```

Ces variables permettent :

- d’éviter la génération de fichiers `.pyc`,
- d’assurer un affichage immédiat des logs dans le conteneur.

---

### c) Répertoire de travail

```dockerfile
WORKDIR /app
```

Cela permet de définir un espace de travail cohérent dans le conteneur.

---

### d) Installation des dépendances

```dockerfile
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /app/requirements.txt
```

Le fichier `requirements.txt` est copié avant les sources pour optimiser le **cache Docker**.

---

### e) Copie du code applicatif

```dockerfile
COPY app.py /app/app.py
COPY database.py /app/database.py
COPY models.sql /app/models.sql
```

Ces instructions injectent les fichiers nécessaires à l’exécution de l’API.

---

### f) Sécurisation de l’exécution

```dockerfile
RUN groupadd -r appuser && useradd -r -g appuser -d /app -s /usr/sbin/nologin appuser
USER appuser
```

L’application ne s’exécute pas en **root**, ce qui constitue une bonne pratique de sécurité.

---

### g) Répertoire de données

```dockerfile
RUN mkdir -p /app/data \
    && chown -R appuser:appuser /app
```

Le dossier `/app/data` est prévu pour accueillir les données SQLite.

---

### h) Port exposé et démarrage

```dockerfile
EXPOSE 5000
CMD ["python", "app.py"]
```

L’API écoute sur le port `5000`.

---

# 6. Orchestration avec Docker Compose

## 6.1 Objectif du fichier `compose.yml`

Le fichier `compose.yml` permet de lancer l’application dans un environnement cohérent et reproductible.

Il facilite :

- le démarrage du service,
- l’injection de variables d’environnement,
- la persistance des données,
- le redémarrage automatique.

---

## 6.2 Fichier `compose.yml` retenu

```yaml
services:
  api:
    image: flask-api:latest
    env_file:
      - .env
    ports:
      - "5000:5000"
    volumes:
      - sqlite_data:/app/data
    restart: unless-stopped

volumes:
  sqlite_data:
```

---

## 6.3 Analyse technique du compose.yml

### a) Service principal

```yaml
services:
  api:
```

Le service principal déployé est l’API Flask.

---

### b) Image utilisée

```yaml
image: flask-api:latest
```

Le service utilise l’image Docker construite localement lors du déploiement.

---

### c) Variables d’environnement

```yaml
env_file:
  - .env
```

Cela permet de séparer la **configuration** du **code source**.

---

### d) Exposition du port

```yaml
ports:
  - "5000:5000"
```

L’API est accessible via le port `5000` de la machine hôte.

---

### e) Persistance des données

```yaml
volumes:
  - sqlite_data:/app/data
```

Cette configuration permet de conserver les données SQLite même si le conteneur est recréé.

---

### f) Redémarrage automatique

```yaml
restart: unless-stopped
```

Cette politique améliore la disponibilité du service.

---

# 7. Présentation du pipeline GitLab CI/CD

## 7.1 Objectif du pipeline

Le pipeline GitLab CI/CD permet d’automatiser les opérations suivantes :

- validation du code,
- exécution des tests,
- contrôle de sécurité,
- déploiement de l’application.

Le pipeline est défini dans le fichier :

```bash
.gitlab-ci.yml
```

---

## 7.2 Structure générale du pipeline

Le pipeline est structuré en quatre **stages** :

```yaml
stages:
  - build
  - test
  - security
  - deploy
```

Cette organisation suit une logique de progression naturelle :

1. **Construire / vérifier**
2. **Tester**
3. **Sécuriser**
4. **Déployer**

---

# 8. Détail des jobs du pipeline

## 8.1 Fichier `.gitlab-ci.yml` retenu

```yaml
stages:
  - build
  - test
  - security
  - deploy

variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"
  DB_PATH: "/tmp/app.db"
  APP_DIR: "/home/gitlab-runner/flask_api"

cache:
  paths:
    - .cache/pip

.python_setup:
  before_script:
    - rm -rf .venv
    - python3 -m venv .venv
    - source .venv/bin/activate
    - pip install -r requirements.txt

build:
  stage: build
  extends: .python_setup
  script:
    - python -m py_compile app.py database.py
  rules:
    - if: '$CI_COMMIT_BRANCH == "develop"'
    - if: '$CI_COMMIT_BRANCH == "main"'

unit_tests:
  stage: test
  extends: .python_setup
  script:
    - export PYTHONPATH="$CI_PROJECT_DIR"
    - pytest -q tests/test_api.py
  rules:
    - if: '$CI_COMMIT_BRANCH == "develop"'
    - if: '$CI_COMMIT_BRANCH == "main"'

security_scan:
  stage: security
  extends: .python_setup
  script:
    - pip-audit -r requirements.txt --ignore-vuln GHSA-5239-wwwm-4pmq
  rules:
    - if: '$CI_COMMIT_BRANCH == "develop"'
    - if: '$CI_COMMIT_BRANCH == "main"'

deploy:
  stage: deploy
  script:
    - echo "Déploiement dans $APP_DIR"
    - |
      if [ ! -d "$APP_DIR/.git" ]; then
        echo "Clone initial..."
        git clone "$CI_REPOSITORY_URL" "$APP_DIR"
      fi
    - cd "$APP_DIR"
    - git checkout main
    - git pull origin main
    - |
      if [ ! -f .env ]; then
        echo "Création du .env depuis .env.example"
        cp .env.example .env
      fi
    - docker compose down || true
    - docker build --network=host -t flask-api:latest .
    - docker compose up -d
    - sleep 5
    - docker ps
    - docker logs $(docker ps -q --filter "name=api") || true
    - curl --fail http://localhost:5000/ || (echo "App non joignable" && exit 1)
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'
```

---

## 8.2 Variables globales

```yaml
variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"
  DB_PATH: "/tmp/app.db"
  APP_DIR: "/home/gitlab-runner/flask_api"
```

### Rôle des variables :
- `PIP_CACHE_DIR` : accélère l’installation des dépendances
- `DB_PATH` : définit un chemin de base de données
- `APP_DIR` : définit le répertoire de déploiement sur la VM

---

## 8.3 Cache CI

```yaml
cache:
  paths:
    - .cache/pip
```

Ce cache permet de réduire les temps d’exécution du pipeline.

---

## 8.4 Template réutilisable `.python_setup`

```yaml
.python_setup:
  before_script:
    - rm -rf .venv
    - python3 -m venv .venv
    - source .venv/bin/activate
    - pip install -r requirements.txt
```

Ce bloc permet de mutualiser la préparation de l’environnement Python.

Il évite de répéter les mêmes instructions dans chaque job.

---

## 8.5 Job `build`

### Objectif
Valider que le code Python est syntaxiquement correct.

### Script exécuté

```bash
python -m py_compile app.py database.py
```

### Rôle
Ce job détecte rapidement :

- erreurs de syntaxe,
- fichiers Python invalides,
- erreurs bloquantes simples.

---

## 8.6 Job `unit_tests`

### Objectif
Exécuter automatiquement les tests de l’API.

### Script exécuté

```bash
export PYTHONPATH="$CI_PROJECT_DIR"
pytest -q tests/test_api.py
```

### Rôle
Ce job permet de vérifier que les comportements attendus de l’API sont respectés.

---

## 8.7 Job `security_scan`

### Objectif
Analyser les dépendances Python à la recherche de vulnérabilités connues.

### Script exécuté

```bash
pip-audit -r requirements.txt --ignore-vuln GHSA-5239-wwwm-4pmq
```

### Rôle
Ce job permet d’intégrer la sécurité dans le pipeline dès la phase d’intégration continue.

---

## 8.8 Job `deploy`

### Objectif
Déployer automatiquement l’application sur la machine cible.

### Principales actions du job

Le job de déploiement :

1. clone le dépôt si nécessaire,
2. récupère la dernière version de `main`,
3. crée `.env` si absent,
4. reconstruit l’image Docker,
5. relance les conteneurs,
6. vérifie que l’application répond.

### Vérification finale

```bash
curl --fail http://localhost:5000/
```

Cette commande agit comme un **smoke test post-déploiement**.

---

## 8.9 Règles de déclenchement

### Branches concernées

- `build`, `unit_tests`, `security_scan` s’exécutent sur :
  - `develop`
  - `main`

- `deploy` s’exécute uniquement sur :
  - `main`

### Intérêt
Cette logique permet :

- de tester en environnement de développement,
- de réserver le déploiement aux branches stables.

---

# 9. Stratégie de test

## 9.1 Objectif

La stratégie de test vise à garantir qu’aucune version défectueuse ne soit déployée sans contrôle minimal.

---

## 9.2 Types de validation mis en œuvre

### a) Validation syntaxique

```bash
python -m py_compile app.py database.py
```

Cette étape détecte les erreurs bloquantes de syntaxe.

---

### b) Tests automatisés de l’API

```bash
pytest -q tests/test_api.py
```

Cette étape permet de vérifier les comportements applicatifs attendus.

---

### c) Vérification post-déploiement

```bash
curl --fail http://localhost:5000/
```

Cette étape vérifie que l’application est réellement accessible après déploiement.

---

## 9.3 Forces de la stratégie actuelle

La stratégie actuelle permet de :

- détecter rapidement les erreurs,
- bloquer les déploiements défectueux,
- sécuriser le cycle de livraison.

---

## 9.4 Limites

Les tests actuels ne couvrent pas encore :

- les tests de charge,
- les tests de performance,
- les tests d’intégration multi-services,
- les tests de sécurité dynamiques,
- les scénarios fonctionnels avancés.

---

# 10. Pratiques DevSecOps

## 10.1 Intégration de la sécurité dans le pipeline

La sécurité n’est pas traitée après coup : elle est intégrée directement dans le pipeline CI/CD.

Cette approche est conforme à une logique **DevSecOps**.

---

## 10.2 Mécanismes de sécurité mis en place

### a) Audit des dépendances

```bash
pip-audit -r requirements.txt --ignore-vuln GHSA-5239-wwwm-4pmq
```

Permet de détecter les vulnérabilités connues dans les bibliothèques Python.

---

### b) Exécution non root dans Docker

```dockerfile
USER appuser
```

Permet de réduire les privilèges du processus applicatif.

---

### c) Séparation de la configuration

```yaml
env_file:
  - .env
```

Permet de ne pas coder directement la configuration dans l’application.

---

### d) Déploiement contrôlé par branche

```yaml
rules:
  - if: '$CI_COMMIT_BRANCH == "main"'
```

Empêche un déploiement automatique depuis une branche non stable.

---

## 10.3 Apport de la démarche DevSecOps

Cette intégration permet :

- une meilleure anticipation des risques,
- une meilleure qualité de livraison,
- une réduction des erreurs de sécurité en production.

---

# 11. Correspondance avec les compétences évaluées

## 11.1 C16 — Mettre en œuvre un pipeline CI/CD opérationnel

### Élément démontré
- pipeline GitLab fonctionnel,
- jobs organisés par étapes,
- déploiement automatisé,
- environnement reproductible avec Docker.

### Preuves
- `.gitlab-ci.yml`
- `Dockerfile`
- `compose.yml`

---

## 11.2 C17 — Automatiser les tests fonctionnels et non fonctionnels

### Élément démontré
- tests intégrés au pipeline,
- exécution automatique des validations,
- contrôle de disponibilité après déploiement.

### Preuves
- job `build`
- job `unit_tests`
- vérification finale `curl`

---

## 11.3 C18 — Intégrer des pratiques DevSecOps

### Élément démontré
- audit des dépendances,
- exécution non root,
- contrôle des branches,
- séparation configuration / code.

### Preuves
- job `security_scan`
- Dockerfile sécurisé
- gestion du `.env`

---

# 12. Risques et limites

## 12.1 Risques identifiés

### a) SQLite
SQLite est adapté à un projet simple ou pédagogique, mais présente des limites :

- concurrence réduite,
- scalabilité faible,
- usage limité dans des architectures plus complexes.

---

### b) Déploiement direct sur VM
Le déploiement est simple mais moins robuste qu’une approche avec :

- registre d’images,
- staging,
- promotion d’artefacts.

---

### c) Couverture de test partielle
La stratégie de test reste limitée à un périmètre raisonnable pour l’épreuve, mais non exhaustive.

---

### d) Gestion des vulnérabilités
Une vulnérabilité est explicitement ignorée dans `pip-audit`, ce qui doit être documenté et maîtrisé.

---

# 13. Recommandations d’amélioration

## 13.1 Améliorations CI/CD

Il serait pertinent de :

- publier l’image dans un **registry Docker**,
- ajouter des **artefacts CI**,
- mettre en place un **staging**,
- ajouter un **rollback automatisé**.

---

## 13.2 Améliorations qualité

Il serait utile d’ajouter :

- **flake8** ou **pylint**,
- **bandit** pour la sécurité Python,
- des **tests d’intégration**,
- des **tests de charge**.

---

## 13.3 Améliorations sécurité

Les améliorations possibles incluent :

- scan de l’image Docker,
- détection de secrets,
- durcissement du conteneur,
- politique de correction formalisée.

---

# 14. Conclusion

La solution CI/CD mise en place pour **UrbanHub Park** répond aux objectifs attendus dans l’épreuve **EC03**.

Elle permet de démontrer :

- la mise en œuvre d’un pipeline CI/CD opérationnel,
- l’automatisation des tests,
- l’intégration de pratiques DevSecOps,
- la reproductibilité du déploiement.

Le pipeline proposé constitue une base technique cohérente, exploitable et évolutive, conforme aux attentes d’un environnement DevOps moderne.

---

# 15. Annexes

---

## 15.1 Dockerfile

```dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /app/requirements.txt

COPY app.py /app/app.py
COPY database.py /app/database.py
COPY models.sql /app/models.sql

RUN groupadd -r appuser && useradd -r -g appuser -d /app -s /usr/sbin/nologin appuser

RUN mkdir -p /app/data \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 5000

CMD ["python", "app.py"]
```

---

## 15.2 compose.yml

```yaml
services:
  api:
    image: flask-api:latest
    env_file:
      - .env
    ports:
      - "5000:5000"
    volumes:
      - sqlite_data:/app/data
    restart: unless-stopped

volumes:
  sqlite_data:
```

---

## 15.3 .gitlab-ci.yml

```yaml
stages:
  - build
  - test
  - security
  - deploy

variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"
  DB_PATH: "/tmp/app.db"
  APP_DIR: "/home/gitlab-runner/flask_api"

cache:
  paths:
    - .cache/pip

.python_setup:
  before_script:
    - rm -rf .venv
    - python3 -m venv .venv
    - source .venv/bin/activate
    - pip install -r requirements.txt

build:
  stage: build
  extends: .python_setup
  script:
    - python -m py_compile app.py database.py
  rules:
    - if: '$CI_COMMIT_BRANCH == "develop"'
    - if: '$CI_COMMIT_BRANCH == "main"'

unit_tests:
  stage: test
  extends: .python_setup
  script:
    - export PYTHONPATH="$CI_PROJECT_DIR"
    - pytest -q tests/test_api.py
  rules:
    - if: '$CI_COMMIT_BRANCH == "develop"'
    - if: '$CI_COMMIT_BRANCH == "main"'

security_scan:
  stage: security
  extends: .python_setup
  script:
    - pip-audit -r requirements.txt --ignore-vuln GHSA-5239-wwwm-4pmq
  rules:
    - if: '$CI_COMMIT_BRANCH == "develop"'
    - if: '$CI_COMMIT_BRANCH == "main"'

deploy:
  stage: deploy
  script:
    - echo "Déploiement dans $APP_DIR"
    - |
      if [ ! -d "$APP_DIR/.git" ]; then
        echo "Clone initial..."
        git clone "$CI_REPOSITORY_URL" "$APP_DIR"
      fi
    - cd "$APP_DIR"
    - git checkout main
    - git pull origin main
    - |
      if [ ! -f .env ]; then
        echo "Création du .env depuis .env.example"
        cp .env.example .env
      fi
    - docker compose down || true
    - docker build --network=host -t flask-api:latest .
    - docker compose up -d
    - sleep 5
    - docker ps
    - docker logs $(docker ps -q --filter "name=api") || true
    - curl --fail http://localhost:5000/ || (echo "App non joignable" && exit 1)
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'
```

---

# Auteur
**Nom du projet :** UrbanHub Park  
**Épreuve :** EC03 – Piloter l’intégration et le déploiement continus  
**Bloc évalué :** Bloc 3 – CI/CD  
**Livrable :** Documentation technique du pipeline