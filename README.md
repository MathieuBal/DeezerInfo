# DeezerInfo

[![Licence](https://img.shields.io/badge/license-MIT-green.svg)]  
[![Python](https://img.shields.io/badge/python-3.x-blue.svg)]  

## Description

**DeezerInfo** est un script Python qui utilise l'API Deezer pour afficher et archiver la musique en cours de lecture :
- Il récupère les pistes d'une playlist nommée **stream**.
- Il compare l'historique de lecture pour déterminer le morceau joué.
- Écrit dans le fichier `current_song.txt` le titre, l'artiste et l'album du morceau suivant.
- Peut ensuite être utilisé pour alimenter une bannière défilante ou tout autre affichage.

## Objectifs

1. Simuler un « scroller » affichant la musique en cours, fonctionnalité absente de l'API Deezer.
2. Automatiser la récupération et l'archivage des métadonnées des morceaux.  
3. Usage personnel pour enrichir son lecteur Deezer local.

## Installation

```bash
# 1. Cloner le dépôt
git clone https://github.com/MathieuBal/deezerinfo.git
cd deezerinfo

# 2. (Optionnel) Créer et activer un environnement virtuel
python3 -m venv .venv
# Sous macOS/Linux
source .venv/bin/activate
# Sous Windows (PowerShell)
.venv\Scripts\Activate.ps1

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Définir les variables d'environnement pour l'API Deezer
export APP_ID=<votre_app_id>
export APP_SECRET=<votre_app_secret>
```

> **Note :** `webbrowser`, `time`, `json` et `os` sont inclus dans la stdlib Python.

## Utilisation

```bash
python infostream.py
```

1. À la première exécution, le script ouvrira ton navigateur pour autoriser l'accès via OAuth Deezer.
2. Saisis le code reçu dans la console.  
3. Le script stockera le token dans le fichier dist/deezer_token.txt et les données de la playlist dans le fichier dist/deezer_data.json.  
4. Le fichier `current_song.txt` sera mis à jour toutes les 5 secondes avec les informations du morceau en cours.


## Statut du projet

** En pause ** – Quelques bugs d'usage restent à corriger (mappings d'historique, robustesse des requêtes).

## Licence

MIT

---

## Améliorations futures

- Créer automatiquement le dossier dist/ s'il n'existe pas.  
- Gérer les erreurs réseau et les tokens expirés.  
- Ajouter une interface graphique ou une bannière défilante en temps réel.  
- Emballer en exécutable cross-platform (PyInstaller).
