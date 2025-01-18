import os
import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askdirectory
from dotenv import load_dotenv

# Charger variables d'environnement
load_dotenv()

# Chemin fichier modèle de données
PATH_DATAMODEL = os.getenv('DATAMODEL')

# Charger fichier CSV
df = pd.read_csv(PATH_DATAMODEL)

# Afficher les colonnes du CSV avec le type associé
print("Colonnes et types de données associés :")
print(df.dtypes)

# Demander à l'utilisateur s'il souhaite modifier les données
reponse = input("\nSouhaitez-vous modifier ces données ? (oui/non) : ").strip().lower()

if reponse == "oui" or reponse == "o":
  print("\nOptions disponibles :")
  print("1. Renommer une colonne")
  print("2. Changer le type de données d'une colonne")
  choix = input("Entrez le numéro de l'option souhaitée : ").strip()

  if choix == "1":
    ancienne_colonne = input("Entrez le nom de la colonne à renommer : ").strip()
    nouvelle_colonne = input("Entrez le nouveau nom pour cette colonne : ").strip()
    if ancienne_colonne in df.columns:
      df.rename(columns={ancienne_colonne: nouvelle_colonne}, inplace=True)
      print(f"La colonne '{ancienne_colonne}' a été renommée en '{nouvelle_colonne}'.")
    else:
      print("Nom de colonne invalide.")

  elif choix == "2":
    colonne = input("Entrez le nom de la colonne dont vous souhaitez changer le type : ").strip()
    nouveau_type = input("Entrez le nouveau type (exemple : int, float, str) : ").strip()
    if colonne in df.columns:
      try:
        df[colonne] = df[colonne].astype(nouveau_type)
        print(f"Le type de la colonne '{colonne}' a été changé en '{nouveau_type}'.")
      except Exception as e:
        print(f"Erreur lors du changement de type : {e}")
    else:
      print("Nom de colonne invalide.")

  else:
    print("Option invalide.")

else:
  print("Aucune modification n'a été effectuée.")

# Afficher les données après modification (le cas échéant)
print("\nDonnées actuelles :")
print(df)

# Ouvrir une fenêtre Windows pour choisir un dossier
root = Tk()
root.withdraw()  # Masquer la fenêtre principale de Tkinter
dossier = askdirectory(title="Choisissez un dossier pour sauvegarder le fichier CSV")

if dossier:  # Vérifier si un dossier a été sélectionné
  nom_fichier = input("Entrez le nom du fichier (sans extension) : ").strip()
  chemin_complet = os.path.join(dossier, f"{nom_fichier}.csv")

  # Sauvegarder le fichier dans le dossier sélectionné
  df.to_csv(chemin_complet, index=False)
  print(f"Données sauvegardées dans {chemin_complet}.")
else:
  print("Sauvegarde annulée.")



