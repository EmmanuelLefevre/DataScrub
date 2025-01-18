import os
import pandas as pd
from tabulate import tabulate
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
print(tabulate(df.dtypes.reset_index(), headers=["Colonne", "Type de données"], tablefmt="grid"))

# Demander à l'utilisateur s'il souhaite modifier les données
response = input("\nSouhaitez-vous modifier ces données ? (O/n): ").strip().lower()
# Si réponse vide
if not response:
  response = "O"

while response in ["O","o"]:
  col_to_modify = input("🏁 Quelle colonne souhaitez-vous modifier ? ").strip()

  # Vérifier si la colonne existe
  while col_to_modify not in df.columns:
    print(f"⚠️ La colonne '{col_to_modify}' n'existe pas. Veuillez saisir un nom de colonne valide!")
    col_to_modify = input("💬 Quelle colonne souhaitez-vous modifier ? ").strip()

  # Demander un nouveau nom pour la colonne
  new_col_name = input(f"Nouveau nom pour '{col_to_modify}':").strip()
  df.rename(columns={col_to_modify: new_col_name}, inplace=True)
  print(f"✔️ Colonne '{col_to_modify}' modifiée en '{new_col_name}'.")

  # Proposer de modifier le type de la colonne
  modify_type = input(f"Souhaitez-vous modifier le type de la colonne '{new_col_name}' ? (O/n): ").strip().lower()
  if modify_type in ["O","o"]:
    print("Types de données disponibles : int, float, str, bool")
    new_col_type = input(f"Nouveau type pour '{new_col_name}' : ").strip().lower()

    # Convertir le type de la colonne
    try:
      if new_col_type == "int":
        df[new_col_name] = df[new_col_name].astype(int)
      elif new_col_type == "float":
        df[new_col_name] = df[new_col_name].astype(float)
      elif new_col_type == "str":
        df[new_col_name] = df[new_col_name].astype(str)
      elif new_col_type == "bool":
        df[new_col_name] = df[new_col_name].astype(bool)
      else:
        print("⚠️ Type de données non reconnu. Aucune modification effectuée!")

      print(f"✔️ Type de la colonne '{new_col_name}' modifié en '{new_col_type}'.")
    except Exception as e:
      print(f"💣 Erreur lors de la conversion : {e}")

  # Afficher le tableau final
  print("🚀 Format des nouvelles données :")
  print(tabulate(df.dtypes.reset_index(), headers=["Colonne", "Type de données"], tablefmt="grid"))

  # Demander si l'utilisateur souhaite modifier une autre colonne
  response = input("\nSouhaitez-vous modifier une autre colonne ? (O/n) : ").strip().lower()

print("👌 Toutes les modifications ont été effectuées. Programme terminé.")

