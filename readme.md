# DATASCRUB

## SOMMAIRE
- [INTRODUCTION](#introduction)
- [PYTHON](#python)
- [REQUIREMENTS](#requirements)
- [GETTING STARTED](#getting-started)
- [TO DO](#to-do)

## INTRODUCTION
DataScrub a pour objectif de nettoyer un jeu de données (DataFrame) au format CSV en éliminant les doublons et les valeurs manquantes. Il applique une série d'opérations de prétraitement :  
- Elimination des doublons
- Elimination des lignes comportants des valeurs manquantes  

Ce nettoyage est essentiel pour garantir la qualité et la fiabilité des analyses ultérieures ou des modèles d'apprentissage automatique qui seront utilisés sur ces données.  
De plus il est possible de changer le nom des colonnes ainsi que leur type associé.

## PYTHON
[Guide d'installation Python](https://github.com/EmmanuelLefevre/Documentations/blob/master/Tutorials/python_install.md)  

## REQUIREMENTS
- Colorama
- Pandas
- Python-dotenv
- Tabulate

## GETTING STARTED
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
3. Placer votre modèle de données .csv dans le dossier (data_frame) prévu à cet effet...
4. Lancer l'application python
```bash
python app.py
```

## TO DO
- Supprimer les données aberrantes.
- Contrôle champ de saisie "modifier une autre colonne" si saisi différente de O/n.
- Le print "print(f"{Style.BRIGHT}{Fore.GREEN}✔️ Toutes les lignes avec des valeurs manquantes ont été supprimées !{Style.RESET_ALL}")" pas toujours affiché.

***

⭐⭐⭐ I hope you enjoy it, if so don't hesitate to leave a like on this repository and on the [Dotfiles](https://github.com/EmmanuelLefevre/Dotfiles) one (click on the "Star" button at the top right of the repository page). Thanks 🤗

