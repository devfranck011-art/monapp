# 🚀  CI/CD Pipeline

## 📌 Présentation

UrbanHub Park est un module de gestion intelligente de stationnement développé dans le cadre de l’épreuve ** Intégration et Déploiement Continus**.

L’objectif est de mettre en place un pipeline CI/CD complet permettant :

* l’automatisation des tests,
* l’analyse de qualité du code,
* l’intégration de pratiques DevSecOps,
* le déploiement automatique de l’application.

---

## 🧱 Stack Technique

* **Backend** : Python / Flask
* **Tests** : Pytest
* **CI/CD** : GitLab CI
* **Conteneurisation** : Docker / Docker Compose
* **Qualité** : Flake8
* **Sécurité (DevSecOps)** : Bandit, pip-audit

---

## 📁 Structure du projet

```bash
urbanhub-park/
│
├── app/                # Code source
├── tests/              # Tests unitaires
├── Dockerfile          # Image Docker
├── docker-compose.yml  # Orchestration
├── requirements.txt    # Dépendances
├── run.py              # Point d’entrée
├── .gitlab-ci.yml      # Pipeline CI/CD
└── README.md
```

---

## ⚙️ Installation locale

### 1. Cloner le projet

```bash
git clone <repo>
cd urbanhub-park
```

### 2. Créer un environnement virtuel

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Lancer l’application

```bash
python run.py
```

👉 Accès : http://localhost:5000

---

## 🐳 Lancer avec Docker

```bash
docker-compose up --build
```

👉 Application accessible sur :
http://localhost:5000

---

## 🔁 Pipeline CI/CD

Le pipeline est défini dans `.gitlab-ci.yml` et contient les stages suivants :

### 🔹 1. Build

* Installation des dépendances

### 🔹 2. Test (C17)

* Exécution des tests avec Pytest

```bash
pytest
```

---

### 🔹 3. Quality

* Analyse du code avec Flake8

```bash
flake8 .
```

---

### 🔹 4. Security (DevSecOps - C18)

#### Scan du code :

```bash
bandit -r app/
```

#### Scan des dépendances :

```bash
pip-audit
```

---

### 🔹 5. Deploy (C16)

* Déploiement avec Docker Compose

```bash
docker-compose up -d
```

---

## 🧪 Stratégie de test

* Tests unitaires
* Tests API

Objectifs :

* validation du bon fonctionnement
* prévention des régressions

---

## 🔐 Sécurité – DevSecOps

Les pratiques suivantes sont intégrées :

* analyse statique de sécurité (Bandit)
* audit des dépendances (pip-audit)

✔ Permet de détecter les vulnérabilités en amont

---

## ⚠️ Risques et limites

### Risques

* erreurs dans le pipeline
* dépendances vulnérables

### Limites

* couverture de test limitée
* sécurité basique

---

## 💡 Recommandations

* ajouter SonarQube pour analyse avancée
* améliorer la couverture de tests
* intégrer des tests end-to-end
* déployer avec Kubernetes

---

## 🎯 Objectifs pédagogiques

Ce projet permet de valider :

* **C16** : Mise en œuvre d’un pipeline CI/CD
* **C17** : Automatisation des tests
* **C18** : Intégration DevSecOps

---

## ✅ Conclusion

Ce projet met en place un pipeline CI/CD complet, automatisé et sécurisé, répondant aux exigences de l’épreuve EC03.

Il garantit :

* une meilleure qualité du code,
* une détection précoce des erreurs,
* un déploiement fiable et reproductible.

---
