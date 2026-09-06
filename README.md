<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0f2027,50:2c5364,100:2F81F7&height=200&section=header&text=FilesNet&fontSize=60&fontColor=ffffff&animation=fadeIn&fontAlignY=35&desc=Partage%20de%20fichiers%20local%20en%20un%20clic&descAlignY=55&descSize=18" width="100%" />

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=500&size=16&pause=1000&color=2F81F7&center=true&vCenter=true&width=550&lines=Serveur+de+fichiers+local+en+quelques+secondes;Accessible+depuis+n'importe+quel+appareil+du+r%C3%A9seau;Simple%2C+rapide%2C+sans+configuration" alt="Typing SVG" />

<br/>

<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/PyQt5-41CD52?style=for-the-badge&logo=qt&logoColor=white" />
<img src="https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white" />
<img src="https://img.shields.io/badge/License-CC0%201.0-lightgrey?style=for-the-badge" />

</div>

<br/>

## À propos

**FilesNet** est une application Windows légère qui transforme n'importe quel dossier de ton PC en un mini serveur de fichiers accessible depuis tout appareil connecté au même réseau (PC, téléphone, tablette), directement depuis un navigateur web.

Pas d'installation lourde, pas de configuration réseau complexe : tu lances l'app, tu choisis un canal (port), et tu partages l'accès via une simple adresse IP ou un QR code à scanner.

## Fonctionnalités

- **Navigation de fichiers** dans le navigateur : parcours de dossiers, aperçu, arborescence
- **Téléchargement** de fichiers et de dossiers entiers (compressés en `.zip` à la volée)
- **Édition de fichiers texte** directement depuis l'interface web
- **Création, renommage et suppression** de fichiers et dossiers
- **QR Code automatique** pour se connecter instantanément depuis un mobile
- **Changement de canal (port)** à chaud sans redémarrer l'application
- **Interface flottante** compacte (PyQt5) avec démarrage/arrêt du serveur en un clic
- **Lancement automatique** au démarrage de Windows (raccourci créé automatiquement)

## Stack technique

<div align="center">

<img src="https://skillicons.dev/icons?i=python,html,css,js&perline=4" />

</div>

- **Backend** : Python (`http.server`, `asyncio`, `aiohttp`)
- **Interface native** : PyQt5 + pywebview
- **Frontend web** : HTML / CSS / JavaScript
- **Génération de QR Code** : `qrcode`

## Installation

```bash
# Cloner le dépôt
git clone https://github.com/SezTy/FilesNet.git
cd FilesNet

# Installer les dépendances
pip install -r FilesNet/Menu/System/requirement.txt

# Lancer l'application
FilesNet/FilesNet.bat
```

> Une release Windows prête à l'emploi (`.exe`) est également disponible dans le dépôt.

## Utilisation

1. Lance `FilesNet.bat` (ou l'exécutable `.exe`)
2. Choisis un canal (port) dans la barre supérieure de l'application
3. Scanne le QR Code généré ou entre l'adresse IP affichée depuis un autre appareil du réseau
4. Navigue, télécharge, édite ou partage tes fichiers depuis le navigateur


<p align="center"><img src="https://capsule-render.vercel.app/api?type=waving&color=2F81F7&height=100&width=100%25&reversal=true" width="100%" style="margin-top:-8px"/></p>

## Licence

Ce projet est distribué sous licence **CC0 1.0 Universal** — libre d'utilisation, de modification et de distribution.

<div align="center">

<a href="https://github.com/SezTy/FilesNet"><img src="https://img.shields.io/badge/GitHub-Voir%20le%20d%C3%A9p%C3%B4t-181717?style=for-the-badge&logo=github&logoColor=white" /></a>

</div>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:2F81F7,100:0f2027&height=100&section=footer" width="100%" />
