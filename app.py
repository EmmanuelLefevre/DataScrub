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

# Afficher nombre de lignes du data model
print("================================")
print(f"🔗 Data model: {len(df)} lignes")
print("================================")

# Nettoyer les doublons
before_cleaning_duplicates = len(df)
df.drop_duplicates(inplace=True)
after_cleaning_duplicates = len(df)

duplicates_removed = before_cleaning_duplicates - after_cleaning_duplicates

if before_cleaning_duplicates == after_cleaning_duplicates:
  print("✔️ Aucun doublon trouvé.")
else:
  plural = "s" if duplicates_removed > 1 else ""
  print(f"✔️ {duplicates_removed} doublon{plural} supprimé{plural}. Nombre de lignes restantes : {after_cleaning_duplicates}")

# Afficher les colonnes du CSV avec le type associé
print("=========================")
print("🚀 Tableau des données 🚀")
print("=========================")
print(tabulate(df.dtypes.reset_index(), headers=["Colonne", "Type"], tablefmt="grid"))

# Demander à l'utilisateur s'il souhaite modifier les données
print("\n")
response = input("Souhaitez-vous modifier ces données ? (O/n): ").strip().lower()
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
  new_col_name = input(f"Nouveau nom pour la colonne '{col_to_modify}': ").strip()
  df.rename(columns={col_to_modify: new_col_name}, inplace=True)
  print(f"✔️ Colonne '{col_to_modify}' modifiée en '{new_col_name}'.")

  # Proposer de modifier le type de la colonne
  modify_type = input(f"Souhaitez-vous modifier le type de la colonne '{new_col_name}' ? (o/N): ").strip().lower()
  # Si réponse vide
  if not response:
    response = "N"
  print("❌")
  if modify_type in ["O","o"]:
    print("Types de données disponibles : int, float, str, bool")
    new_col_type = input(f"Nouveau type pour '{new_col_name}': ").strip().lower()

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


  # Demander si l'utilisateur souhaite modifier une autre colonne
  response = input("Souhaitez-vous modifier une autre colonne ? (O/n) : ").strip().lower()

# Afficher le tableau final
print("=============================================")
print("     🚀 Tableau des nouvelles données 🚀     ")
print("=============================================")
print(tabulate(df.dtypes.reset_index(), headers=["Colonne", "Type de données"], tablefmt="grid"))

print("👌 Toutes les modifications ont été effectuées. Programme terminé.")

