import os
import sys
import pandas as pd
from tabulate import tabulate
from tkinter import Tk
from tkinter.filedialog import askdirectory, askopenfilename, asksaveasfilename
from dotenv import load_dotenv

# Charger variables d'environnement
load_dotenv()


#######################################################################
##### Fonction pour choisir le fichier CSV dans le dossier "data" #####
#######################################################################
def select_file():
  # Chemin du dossier "data"
  data_dir = os.path.join(os.getcwd(), "data")

  # Vérifier si le dossier "data" existe
  if not os.path.exists(data_dir):
    print("⚠️ Le dossier 'data' est introuvable... Créer le dossier et y ajouter un fichier au format CSV!")
    sys.exit(0)

  # Lister les fichiers CSV dans le dossier "data"
  csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]

  # Aucun fichier CSV trouvé
  if not csv_files:
    print("⚠️ Aucun fichier CSV trouvé dans le dossier 'data'. Ajouter un fichier avant de relancer le programme!")
    sys.exit(0)

  # Un seul fichier CSV trouvé => le charger automatiquement
  if len(csv_files) == 1:
    return os.path.join(data_dir, csv_files[0])

  # Si plusieurs fichiers => ouvrir la fenêtre de sélection
  Tk().withdraw()

  file_path = askopenfilename(
    title="Choisir un fichier CSV",
    filetypes=[("Fichiers CSV", "*.csv")],
    initialdir=data_dir
  )

  if not file_path:
    print("❌ Aucun fichier sélectionné.")
    sys.exit(0)

  return file_path



########################################################
##### Fonction pour enregistrer le fichier modifié #####
########################################################
def save_file(df):
  try:
    Tk().withdraw()

    save_path = asksaveasfilename(
      title="Enregistrer le fichier modifié",
      defaultextension=".csv",
      filetypes=[("Fichiers CSV", "*.csv")],
      initialdir=os.path.join(os.getcwd(), "data")
    )

    if save_path:
      # Ajouter automatiquement l'extension ".csv" si absente
      if not save_path.endswith(".csv"):
        save_path += ".csv"

      # Sauvegarder le DataFrame au chemin sélectionné
      df.to_csv(save_path, index=False)
      print(f"📄 Fichier enregistré sous: {save_path}")
    else:
      print("❌ Aucune sauvegarde effectuée. Programme terminé.")

  except Exception as e:
    print(f"💣 Erreur lors de la sauvegarde : {e}")



###################################################################################
##### Fonction pour supprimer une colonne de toutes les lignes et de l'entête #####
###################################################################################
def delete_column(df):
  try:
    while True:
      # Supprimer une colonne
      response = input("🏁 Souhaitez-vous supprimer une colonne ? (O/n): ").strip().lower()

      if response not in ["o", ""]:
        break

      col_to_delete = input("💬 Indiquez le nom de la colonne à supprimer (ou 'fin' pour ignorer) : ").strip()

      if col_to_delete == "fin":
        print("\n")
        return df

      # Vérifier si la colonne existe dans le CSV
      if col_to_delete in df.columns:
        df.drop(columns=[col_to_delete], inplace=True)
        print(f"✔️ Colonne '{col_to_delete}' supprimée avec succès.")
      else:
        print(f"⚠️ La colonne '{col_to_delete}' n'existe pas! Veuillez réessayer.")

    return df

  except KeyboardInterrupt:
    print("💥 Opération interrompue par l'utilisateur. Programme terminé.")
    sys.exit(0)



################################################################################
##### Fonction pour gérer le processus de nettoyage des valeurs manquantes #####
################################################################################
def handle_missing_values(df):
  try:
    # Eliminer les lignes comportant des valeurs manquantes
    response = input("🏁 Souhaitez-vous supprimer les lignes comportant des valeurs manquantes ? (O/n): ").strip().lower()

    # Initialiser le total des lignes supprimées
    total_rows_removed = 0

    # Nombre de lignes initial
    after_cleaning_nullables = len(df)

    if response in ["o", ""]:
      # Identifier les colonnes contenant des valeurs manquantes
      columns_with_missing = df.columns[df.isnull().any()].tolist()

      # Si aucunes colonnes contenant des valeurs manquantes
      if not columns_with_missing:
        print("✔️ Aucune colonne avec des valeurs manquantes.")
        return df

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

      # Initialiser valeurs manquantes
      after_cleaning_nullables = len(df)

      # Demander à l'utilisateur de choisir quelles colonnes nettoyer
      while True:
        col_to_clean = input(f"💬 Pour quelle colonne souhaitez-vous effectuer cette opération ? ('fin' pour terminer): ").strip()

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
        response = input("🏁 Souhaitez-vous nettoyer une autre colonne ? (O/n): ").strip().lower()

        if not response or response not in ["O", "o"]:
          print("\n")
          break

    # Afficher le cumul de lignes supprimées
    plural = "s" if total_rows_removed > 1 else ""
    print("\n")
    print(f"💪 {total_rows_removed} ligne{plural} supprimé{plural}. Nombre de lignes restantes : {after_cleaning_nullables}")
    print("\n")

    return df

  except KeyboardInterrupt:
    print("💥 Opération interrompue par l'utilisateur. Programme terminé.")
    sys.exit(0)



##########################################################################################################
##### Fonction pour demander à l'utilisateur s'il souhaite modifier les données et leur type associé #####
##########################################################################################################
def handle_modifications(df):
  try:
    # Demander à l'utilisateur s'il souhaite modifier les données
    response = input("Souhaitez-vous modifier ces données ? (O/n): ").strip().lower()

    while response in ["o", ""]:
      col_to_modify = input("🏁 Quelle colonne souhaitez-vous modifier ? ").strip()

      # Vérifier si la colonne existe
      while col_to_modify not in df.columns:
        print(f"⚠️ '{col_to_modify}' n'existe pas. Veuillez saisir un nom de colonne valide!")
        col_to_modify = input("🏁 Quelle colonne souhaitez-vous modifier ? ").strip()

      # Demander un nouveau nom pour la colonne
      new_col_name = input(f"💬 Nouveau nom pour la colonne '{col_to_modify}': ").strip()
      df.rename(columns={col_to_modify: new_col_name}, inplace=True)
      print(f"✔️ Colonne '{col_to_modify}' modifiée en '{new_col_name}'.")

      # Proposer de modifier le type de la colonne
      modify_type = input(f"💬 Souhaitez-vous modifier le type de la colonne '{new_col_name}' ? (o/N): ").strip().lower()

      # Si réponse vide
      if not modify_type:
        modify_type = "n"
      print("❌")

      if modify_type in ["O","o"]:
        print("Types de données disponibles : int, float, str, bool")
        new_col_type = input(f"💬 Nouveau type pour '{new_col_name}': ").strip().lower()

        # Vérification du type de données avant conversion
        if new_col_type in ["int", "float", "str", "bool"]:
          try:
            df[new_col_name] = df[new_col_name].astype(new_col_type)
            print(f"✔️ Type de la colonne '{new_col_name}' modifié en '{new_col_type}'.")
          except Exception as e:
            print(f"💣 Erreur lors de la conversion : {e}")
        else:
          print("⚠️ Type de données non reconnu. Aucune modification effectuée!")

      # Demander si l'utilisateur souhaite modifier une autre colonne
      response = input("🏁 Souhaitez-vous modifier une autre colonne ? (O/n) : ").strip().lower()

      # Si réponse vide
      if not response:
        response = "O"

    return df

  except KeyboardInterrupt:
    print("💥 Opération interrompue par l'utilisateur. Programme terminé.")
    sys.exit(0)



#######################################################################################
##### Fonction pour demander à l'utilisateur s'il souhaite supprimer les doublons #####
#######################################################################################
def handle_duplicates(df):
  try:
    # Proposer de supprimer des doublons
    response = input("🏁 Souhaitez-vous supprimer les doublons ? (O/n): ").strip().lower()

    if response in ["O", ""]:
      before_cleaning_duplicates = len(df)
      df.drop_duplicates(inplace=True)
      after_cleaning_duplicates = len(df)

      duplicates_removed = before_cleaning_duplicates - after_cleaning_duplicates

      if before_cleaning_duplicates == after_cleaning_duplicates:
        print("✔️ Aucun doublon trouvé.")
      else:
        plural = "s" if duplicates_removed > 1 else ""
        print(f"✔️ {duplicates_removed} doublon{plural} supprimé{plural}. Nombre de lignes restantes : {after_cleaning_duplicates}")
      print("\n")

    return df

  except KeyboardInterrupt:
    print("💥 Opération interrompue par l'utilisateur. Programme terminé.")
    sys.exit(0)



################
##### Main #####
################
def main():
  # Demander à l'utilisateur de choisir un fichier CSV
  file_path = select_file()

  # Charger le fichier CSV
  try:
    df = pd.read_csv(file_path, encoding='utf-8')
  except Exception as e:
    print(f"💣 Erreur lors du chargement du fichier CSV : {e}")
    sys.exit(0)

  # Créer une copie du DataFrame initial pour détecter les modifications
  initial_df = df.copy()

  # Afficher nombre de lignes du DataFrame
  print("\n")
  print("=============================")
  print(f"🔗 DataFrame: {len(df)} lignes")
  print("=============================")

  # Afficher les colonnes du CSV avec le type associé
  print("=========================")
  print("📊 Tableau des données 📊")
  print("=========================")
  print(tabulate(df.dtypes.reset_index(), headers=["Colonne", "Type"], tablefmt="grid"))
  print("\n")

  # Appels des fonctions
  df = handle_duplicates(df)
  df = delete_column(df)
  df = handle_missing_values(df)
  df = handle_modifications(df)

  # Afficher le tableau final
  print("=============================================")
  print("     📊 Tableau des nouvelles données 📊     ")
  print("=============================================")
  print(tabulate(df.dtypes.reset_index(), headers=["Colonne", "Type de données"], tablefmt="grid"))


  # Sauvegarde si des modifications ont été effectuées
  if not df.equals(initial_df):
    save_file(df)
    print("👌 Toutes les modifications ont été effectuées. Programme terminé.")
  else:
    print("❌ Aucune modification n'a été effectuée. Aucune sauvegarde nécessaire...")



#####################
##### Execution #####
#####################
if __name__ == "__main__":
  main()
