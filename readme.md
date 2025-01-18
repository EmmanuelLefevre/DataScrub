# DATASCRUB

## SOMMAIRE
- [INTRODUCTION](#introduction)
- [PYTHON](#python)
- [REQUIREMENTS](#requirements)
- [PROCEDURE](#procedure)

## INTRODUCTION
DataScrub a pour objectif de nettoyer un jeu de données (en format CSV) en éliminant les doublons et les valeurs manquantes. Il applique une série d'opérations de prétraitement :  
- Elimination des doublons
- Elimination des lignes comportants des valeurs manquantes  

Ce nettoyage est essentiel pour garantir la qualité et la fiabilité des analyses ultérieures ou des modèles d'apprentissage automatique qui seront utilisés sur ces données.  
De plus il est possible de changer le nom des colonnes ainsi que leur type associé.

## PYTHON
[Télécharger Python 3.13.1](https://www.python.org/downloads/)  

⚠️ "Customize installation"  

Cocher les options =>  
- "pip"  
- "tcl/tk and IDLE"  
- "py launcher"  

![Installation Python 1](https://github.com/EmmanuelLefevre/MarkdownImg/blob/main/py_install.png)  

Puis dans la seconde fenêtre =>  
- "Associate files with Python"  
- "Add Python to environment variables".  

![Installation Python 2](https://github.com/EmmanuelLefevre/MarkdownImg/blob/main/py_install_2.png)  

- Vérifier l'installation de Python
```bash
python --version
```
- Vérifier l'installation de Pip
```bash
pip --version
```

## REQUIREMENTS
- Pandas
- Python-dotenv
- Tabulate

## PROCEDURE
1. Installer les librairies (en local dans python)
```bash
pip install -r requirements.txt
```
Vérifier l'installation des librairies
```bash
pip list
```
2. Créer un .env à partir du .env.template et changer **MANUELLEMENT** les valeurs pertinentes
```bash
cp .env.template .env
```
3. Placer votre modèle de données .csv dans le dossier (data) prévu à cet effet...
4. Lancer l'application python
```bash
python app.py
```

***

⭐⭐⭐ I hope you enjoy it, if so don't hesitate to leave a like on this repository and on the [Dotfiles](https://github.com/EmmanuelLefevre/Dotfiles) one (click on the "Star" button at the top right of the repository page). Thanks 🤗
