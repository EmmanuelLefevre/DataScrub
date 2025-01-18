import os
import sys
import pandas as pd
from tabulate import tabulate
from tkinter import Tk
from tkinter.filedialog import askdirectory, askopenfilename, asksaveasfilename
from dotenv import load_dotenv

# Charger variables d'environnement
load_dotenv()

# Fonction pour choisir le fichier CSV dans le dossier "data"
def select_file():
  # Créer une fenêtre tkinter
  Tk().withdraw()

  file_path = askopenfilename(
    title="Choisir un fichier CSV",
    filetypes=[("Fichiers CSV", "*.csv")],
    # Répertoire initial
    initialdir=os.path.join(os.getcwd(), "data")
  )

  return file_path

# Fonction pour enregistrer le fichier modifié
def save_file(df):
  # Créer une fenêtre tkinter
  Tk().withdraw()

  save_path = asksaveasfilename(
    title="Enregistrer le fichier modifié",
    defaultextension=".csv",
    filetypes=[("Fichiers CSV", "*.csv")],
    # Répertoire initial
    initialdir=os.path.join(os.getcwd(), "data")
  )

  if save_path:
    # Sauvegarder le DataFrame au chemin sélectionné
    df.to_csv(save_path, index=False)
    print(f"📄 Fichier enregistré sous: {save_path}")
  else:
    print("❌ Aucune sauvegarde effectuée. Programme terminé.")

# Fonction pour gérer le processus de nettoyage des valeurs manquantes
def handle_missing_values():
  try:
    # Eliminer les lignes comportant des valeurs manquantes
    response = input("🏁 Souhaitez-vous supprimer les lignes comportant des valeurs manquantes ? (O/n): ").strip().lower()

    # Si réponse vide
    if not response:
      response = "O"

    # Initialiser le total des lignes supprimées
    total_rows_removed = 0

    if response in ["O", "o"]:
      # Identifier les colonnes contenant des valeurs manquantes
      columns_with_missing = df.columns[df.isnull().any()].tolist()

      # Si des colonnes contiennent des valeurs manquantes
      if columns_with_missing:
        # Calculer le nombre de valeurs manquantes pour chaque colonne
        missing_values_count = df[columns_with_missing].isnull().sum()

        # Créer un tableau à afficher avec le nombre de valeurs manquantes par colonne
        missing_values_table = pd.DataFrame({
          "Colonne": columns_with_missing,
          "Valeurs manquantes": missing_values_count
        })

        # Afficher le tableau initial
        print(tabulate(missing_values_table, headers="keys", tablefmt="grid", showindex=False))
      else:
        print("✔️ Aucune colonne avec des valeurs manquantes.")

      # Initialiser valeurs manquantes
      after_cleaning_nullables = len(df)

      # Demander à l'utilisateur de choisir quelles colonnes nettoyer
      while True:
        col_to_clean = input(f"Pour quelle colonne souhaitez-vous effectuer cette opération ? ('fin' pour terminer): ").strip()

        if col_to_clean == 'fin':
          print("\n")
          break

        # Vérifier si la colonne existe
        if col_to_clean in columns_with_missing:
          # Calculer le nombre de lignes avant la suppression
          before_cleaning_nullables = len(df)

          # Supprimer les lignes où la colonne spécifiée a des valeurs manquantes
          df.dropna(subset=[col_to_clean], inplace=True)

          # Calculer le nombre de lignes après la suppression
          after_cleaning_nullables = len(df)

          # Calculer le nombre de lignes supprimées
          rows_removed = before_cleaning_nullables - after_cleaning_nullables

          # Ajouter le nombre de lignes supprimées au total
          total_rows_removed += rows_removed

          if rows_removed == 1:
            print(f"✔️ {rows_removed} ligne avec une valeur manquante dans '{col_to_clean}' a été supprimée.")
          else:
            print(f"✔️ {rows_removed} lignes avec une valeur manquante dans '{col_to_clean}' ont été supprimées.")

          # Recalculer les colonnes avec des valeurs manquantes et afficher le tableau mis à jour
          columns_with_missing = df.columns[df.isnull().any()].tolist()
          if columns_with_missing:
            missing_values_count = df[columns_with_missing].isnull().sum()
            missing_values_table = pd.DataFrame({
              "Colonne": columns_with_missing,
              "Valeurs manquantes": missing_values_count
            })
            print(tabulate(missing_values_table, headers="keys", tablefmt="grid", showindex=False))

        else:
          print(f"⚠️ La colonne '{col_to_clean}' n'a pas de valeurs manquantes ou n'existe pas.")

        # Vérifier si toutes les lignes ont été nettoyées
        if not df.isnull().any().any():
          print("✔️ Toutes les lignes avec des valeurs manquantes ont été supprimées!")
          break

        # Demander si l'utilisateur souhaite continuer
        response = input("Souhaitez-vous nettoyer une autre colonne ? (O/n): ").strip().lower()
        # Si réponse vide
        if not response:
          response = "O"
        if response not in ["O", "o"]:
          print("\n")
          break

    # Afficher le cumul de lignes supprimées
    plural = "s" if total_rows_removed > 1 else ""
    print("\n")
    print(f"💪 {total_rows_removed} ligne{plural} supprimé{plural}. Nombre de lignes restantes : {after_cleaning_nullables}")
    print("\n")

  except KeyboardInterrupt:
    print("💥 Opération interrompue par l'utilisateur. Le programme va maintenant se terminer.")
    sys.exit(0)

# Fonction pour demander à l'utilisateur s'il souhaite modifier les données
def handle_modifications():
  try:
    # Demander à l'utilisateur s'il souhaite modifier les données
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
      # Si réponse vide
      if not response:
        response = "O"

  except KeyboardInterrupt:
    print("💥 Opération interrompue par l'utilisateur. Le programme va maintenant se terminer.")
    sys.exit(0)

# Demander à l'utilisateur de choisir un fichier CSV
file_path = select_file()

if file_path:
  # Charger le fichier CSV
  df = pd.read_csv(file_path)

  # Afficher nombre de lignes du data model
  print("\n")
  print("=============================")
  print(f"🔗 Data model: {len(df)} lignes")
  print("=============================")

  # Variable pour suivre si des modifications ont été effectuées
  has_modifications = False

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
    has_modifications = True
  print("\n")

  # Afficher les colonnes du CSV avec le type associé
  print("=========================")
  print("🚀 Tableau des données 🚀")
  print("=========================")
  print(tabulate(df.dtypes.reset_index(), headers=["Colonne", "Type"], tablefmt="grid"))
  print("\n")

  try:
    # Demander à l'utilisateur s'il souhaite supprimer les lignes comportant des valeurs manquantes
    handle_missing_values()
    has_modifications = True
  except KeyboardInterrupt:
    print("💥 Opération interrompue par l'utilisateur. Le programme va maintenant se terminer.")
    sys.exit(0)

  try:
    # Demander à l'utilisateur s'il souhaite modifier les données
    handle_modifications()
    has_modifications = True
  except KeyboardInterrupt:
    print("💥 Opération interrompue par l'utilisateur. Le programme va maintenant se terminer.")
    sys.exit(0)

  # Afficher le tableau final
  print("=============================================")
  print("     🚀 Tableau des nouvelles données 🚀     ")
  print("=============================================")
  print(tabulate(df.dtypes.reset_index(), headers=["Colonne", "Type de données"], tablefmt="grid"))

  print("👌 Toutes les modifications ont été effectuées. Programme terminé.")

  # Si des modifications ont été effectuées, proposer de sauvegarder
  if has_modifications:
    # Sauvegarder les modifications
    save_file(df)
  else:
    print("❌ Aucune modification n'a été effectuée. Aucune sauvegarde nécessaire...")

else:
  print("👿 Aucun fichier sélectionné. Programme terminé.")
