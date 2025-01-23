import os
import pandas as pd
import sys

from colorama import Fore, Style, init
from dotenv import load_dotenv
from tabulate import tabulate
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename



################
##### Load #####
################
# Charger variables d'environnement
load_dotenv()

# Créer instance de Tk
tkInstance = Tk()
tkInstance.withdraw()

# Initialiser colorama
init()


##############################################
##### Fonction pour quitter le programme #####
##############################################
def leave():
  print(f"{Style.BRIGHT}{Fore.BLUE}👋 Programme terminé.{Style.RESET_ALL}")
  sys.exit(0)



#############################################################################
##### Fonction pour choisir le fichier CSV dans le dossier "data_frame" #####
#############################################################################
def select_file():
  # Chemin du dossier "data_frame"
  data_dir = os.path.join(os.getcwd(), "data_frame")

  # Vérifier si le dossier "data_frame" existe
  if not os.path.exists(data_dir):
    print(f"{Style.BRIGHT}{Fore.RED}⚠️ Le dossier 'data_frame' est introuvable... Créer le dossier et y ajouter un fichier au format CSV !{Style.RESET_ALL}")
    leave()

  # Lister les fichiers CSV dans le dossier "data_frame"
  csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]

  # Aucun fichier CSV trouvé
  if not csv_files:
    print(f"{Style.BRIGHT}{Fore.RED}⚠️ Aucun fichier CSV trouvé dans le dossier 'data_frame'. Ajouter un fichier avant de relancer le programme !{Style.RESET_ALL}")
    leave()

  # Un seul fichier CSV trouvé => le charger automatiquement
  if len(csv_files) == 1:
    return os.path.join(data_dir, csv_files[0])

  file_path = askopenfilename(
    title="Choisir un fichier CSV",
    filetypes=[("Fichiers CSV", "*.csv")],
    initialdir=data_dir
  )

  if not file_path:
    print(f"{Style.BRIGHT}{Fore.RED}❌ Aucun fichier sélectionné.{Style.RESET_ALL}")
    leave()

  return file_path



########################################################
##### Fonction pour enregistrer le fichier modifié #####
########################################################
def save_file(df, existing_filename):
  try:
    print("📂 Veuillez sélectionner un emplacement pour sauvegarder le fichier.")
    save_path = asksaveasfilename(
      title="Enregistrer le fichier modifié",
      defaultextension=".csv",
      filetypes=[("Fichiers CSV", "*.csv")],
      initialfile=existing_filename,
      initialdir=os.path.join(os.getcwd(), "data_frame")
    )

    if save_path:
      # Ajouter automatiquement l'extension ".csv" si absente
      if not save_path.endswith(".csv"):
        save_path += ".csv"

      # Extraire le nom de fichier et l'extension
      filename, extension = os.path.splitext(os.path.basename(save_path))

      # Sauvegarder le DataFrame au chemin sélectionné
      df.to_csv(save_path, index=False)
      print(f"{Style.BRIGHT}{Fore.GREEN}📄 {filename}{extension} enregistré sous: {save_path}{Style.RESET_ALL}")
      return True
    else:
      print(f"{Style.BRIGHT}{Fore.RED}❌ Action annulée par l'utilisateur.{Style.RESET_ALL}")
      return False

  except PermissionError:
    print(f"{Style.BRIGHT}{Fore.RED}💣 Fichier ouvert, assurez-vous que celui-ci est fermé !{Style.RESET_ALL}")
    return False

  except Exception as e:
    print(f"{Style.BRIGHT}{Fore.RED}💣 Erreur lors de la sauvegarde : {e}{Style.RESET_ALL}")
    return False



###################################################################################
##### Fonction pour supprimer une colonne de toutes les lignes et de l'entête #####
###################################################################################
def delete_column(df):
  while True:
    # Supprimer une colonne
    response = input("🏁 Souhaitez-vous supprimer une colonne ? (O/n): ").strip().lower()

    if response not in ["o", ""]:
      break

    while True:
      col_to_delete = input("💬 Indiquez le nom de la colonne à supprimer (ou 'fin' pour ignorer) : ").strip()

      if col_to_delete == "fin":
        return df

      # Vérifier si la colonne existe dans le DataFrame
      if col_to_delete in df.columns:
        df.drop(columns=[col_to_delete], inplace=True)
        print(f"{Style.BRIGHT}{Fore.GREEN}✔️ Colonne '{col_to_delete}' supprimée avec succès.{Style.RESET_ALL}")
      else:
        print(f"{Style.BRIGHT}{Fore.RED}⚠️ La colonne '{col_to_delete}' n'existe pas !{Style.RESET_ALL}")

      # Demander si l'utilisateur souhaite supprimer une autre colonne après une suppression réussie
      response = input("🏁 Souhaitez-vous supprimer une autre colonne ? (O/n): ").strip().lower()
      if response == "n":
        return df
      if response not in ["o", ""]:
        break

  return df



################################################################################
##### Fonction pour gérer le processus de nettoyage des valeurs manquantes #####
################################################################################
def handle_missing_values(df):
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
      print(f"{Style.BRIGHT}{Fore.GREEN}✔️ Aucune colonne avec des valeurs manquantes.{Style.RESET_ALL}")
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
      col_to_clean = input(f"💬 Sur quelle colonne souhaitez-vous effectuer cette opération (ou 'fin' pour ignorer) : ").strip()

      if col_to_clean == 'fin':
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
          print(f"{Style.BRIGHT}{Fore.GREEN}✔️ {rows_removed} ligne avec une valeur manquante dans '{col_to_clean}' a été supprimée.{Style.RESET_ALL}")
        else:
          print(f"{Style.BRIGHT}{Fore.GREEN}✔️ {rows_removed} lignes avec une valeur manquante dans '{col_to_clean}' ont été supprimées.{Style.RESET_ALL}")

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
        print(f"{Style.BRIGHT}{Fore.RED}⚠️ La colonne '{col_to_clean}' n'a pas de valeurs manquantes ou n'existe pas.{Style.RESET_ALL}")

      # Vérifier si toutes les lignes ont été nettoyées
      if not df.isnull().any().any():
        print(f"{Style.BRIGHT}{Fore.GREEN}✔️ Toutes les lignes avec des valeurs manquantes ont été supprimées !{Style.RESET_ALL}")
        break

      # Demander si l'utilisateur souhaite continuer
      response = input("🏁 Souhaitez-vous nettoyer une autre colonne ? (O/n): ").strip().lower()

      if response not in ["o", ""]:
        break

  # Afficher le cumul de lignes supprimées
  plural = "s" if total_rows_removed > 1 else ""
  print(f"{Style.BRIGHT}{Fore.GREEN}💪 {total_rows_removed} ligne{plural} supprimé{plural}. Nombre de lignes restantes : {after_cleaning_nullables}{Style.RESET_ALL}")

  return df



##########################################################################################################
##### Fonction pour demander à l'utilisateur s'il souhaite modifier les données et leur type associé #####
##########################################################################################################
def handle_modifications(df):
  # Demander à l'utilisateur s'il souhaite modifier les données
  response = input("Souhaitez-vous modifier ces données ? (O/n): ").strip().lower()

  while response in ["o", ""]:
    while True:
      col_to_modify = input("🏁 Quelle colonne souhaitez-vous modifier ? ").strip()

      # Vérifier si la colonne existe
      if col_to_modify not in df.columns:
        print(f"{Style.BRIGHT}{Fore.RED}⚠️ '{col_to_modify}' n'existe pas !{Style.RESET_ALL}")
        continue
      else:
        break

    # Demander un nouveau nom pour la colonne
    new_col_name = input(f"💬 Nouveau nom pour la colonne '{col_to_modify}' (ou 'fin' pour ignorer) : ").strip()

    if new_col_name == "fin":
      return df

    # Vérifier si le nouveau nom de colonne est vide
    if not new_col_name:
      print(f"{Style.BRIGHT}{Fore.RED}⚠️ Le nom de la colonne ne peut pas être vide !{Style.RESET_ALL}")
      continue

    # Vérifier si le nouveau nom de colonne existe déjà
    if new_col_name in df.columns:
      print(f"{Style.BRIGHT}{Fore.RED}⚠️ La colonne '{new_col_name}' existe déjà !{Style.RESET_ALL}")
      continue

    # Renommer la colonne
    df.rename(columns={col_to_modify: new_col_name}, inplace=True)
    print(f"{Style.BRIGHT}{Fore.GREEN}✔️ Colonne '{col_to_modify}' modifiée en '{new_col_name}'.{Style.RESET_ALL}")

    # Proposer de modifier le type de la colonne
    modify_type = input(f"🏁 Souhaitez-vous modifier le type de la colonne '{new_col_name}' ? (o/N): ").strip().lower()

    # Si réponse vide
    if not modify_type:
      modify_type = "n"

    if modify_type in ["O","o"]:
      print("Types de données disponibles : int, float, str, bool")
      new_col_type = input(f"💬 Nouveau type pour '{new_col_name}' (ou 'fin' pour ignorer) : ").strip().lower()

      if new_col_type == "fin":
        return df

      # Vérification du type de données avant conversion
      if new_col_type in ["int", "float", "str", "bool"]:
        try:
          df[new_col_name] = df[new_col_name].astype(new_col_type)
          print(f"{Style.BRIGHT}{Fore.GREEN}✔️ Type de la colonne '{new_col_name}' modifié en '{new_col_type}'.{Style.RESET_ALL}")
        except ValueError:
          print(f"{Style.BRIGHT}{Fore.RED}💣 Impossible de convertir la colonne '{new_col_name}' en type '{new_col_type}' !{Style.RESET_ALL}")
        except Exception as e:
          print(f"{Style.BRIGHT}{Fore.RED}💣 Erreur lors de la conversion : {e}{Style.RESET_ALL}")
      else:
        print(f"{Style.BRIGHT}{Fore.RED}⚠️ Type de données non reconnu. Aucune modification effectuée !{Style.RESET_ALL}")

    # Demander si l'utilisateur souhaite modifier une autre colonne
    response = input("🏁 Souhaitez-vous modifier une autre colonne ? (O/n) : ").strip().lower()

    # Si réponse vide
    if not response:
      response = "o"

  return df



#######################################################################################
##### Fonction pour demander à l'utilisateur s'il souhaite supprimer les doublons #####
#######################################################################################
def handle_duplicates(df):
  # Proposer de supprimer des doublons
  response = input("🏁 Souhaitez-vous supprimer les doublons ? (O/n): ").strip().lower()

  if response in ["o", ""]:
    before_cleaning_duplicates = len(df)
    df.drop_duplicates(inplace=True)
    after_cleaning_duplicates = len(df)

    duplicates_removed = before_cleaning_duplicates - after_cleaning_duplicates

    if before_cleaning_duplicates == after_cleaning_duplicates:
      print(f"{Style.BRIGHT}{Fore.GREEN}✔️ Aucun doublon trouvé.{Style.RESET_ALL}")
    else:
      plural = "s" if duplicates_removed > 1 else ""
      print(f"{Style.BRIGHT}{Fore.GREEN}✔️ {duplicates_removed} doublon{plural} supprimé{plural}. Nombre de lignes restantes : {after_cleaning_duplicates}{Style.RESET_ALL}")

  return df



################
##### Main #####
################
def main():
  # Demander à l'utilisateur de choisir un fichier CSV
  file_path = select_file()

  # Charger le fichier CSV
  try:
    df = pd.read_csv(file_path, encoding='utf-8')
  except UnicodeDecodeError:
    print(f"{Style.BRIGHT}{Fore.RED}💣 Erreur de décodage. Tentative avec ISO-8859-1 ...{Style.RESET_ALL}")
    df = pd.read_csv(file_path, encoding='ISO-8859-1')
  except Exception as e:
    print(f"{Style.BRIGHT}{Fore.RED}💣 Erreur lors du chargement du fichier CSV : {e}{Style.RESET_ALL}")
    leave()

  # Créer une copie du DataFrame initial pour détecter les modifications
  initial_df = df.copy()

  # Afficher nombre de lignes du DataFrame
  print(f"{Style.BRIGHT}{Fore.MAGENTA}🔗 DataFrame: {len(df)} lignes{Style.RESET_ALL}")

  # Afficher les colonnes du CSV avec le type associé
  print(f"{Style.BRIGHT}{Fore.CYAN}========================={Style.RESET_ALL}")
  print(f"{Style.BRIGHT}{Fore.CYAN}📊 Tableau des données 📊{Style.RESET_ALL}")
  print(f"{Style.BRIGHT}{Fore.CYAN}========================={Style.RESET_ALL}")
  print(tabulate(df.dtypes.reset_index(), headers=["Colonne", "Type"], tablefmt="grid"))
  print("\n")

  # Appels des fonctions
  df = handle_duplicates(df)
  df = delete_column(df)
  df = handle_missing_values(df)
  df = handle_modifications(df)

  # Afficher le tableau final
  print("\n")
  print(f"{Style.BRIGHT}{Fore.CYAN}============================================={Style.RESET_ALL}")
  print(f"{Style.BRIGHT}{Fore.CYAN}     📊 Tableau des nouvelles données 📊     {Style.RESET_ALL}")
  print(f"{Style.BRIGHT}{Fore.CYAN}============================================={Style.RESET_ALL}")
  print(tabulate(df.dtypes.reset_index(), headers=["Colonne", "Type de données"], tablefmt="grid"))


  # Sauvegarde si des modifications ont été effectuées
  if not df.equals(initial_df):
    # Extraire le nom de fichier à partir du chemin
    existing_filename = os.path.basename(file_path)
    saved = save_file(df, existing_filename)

    if saved:
      print(f"{Style.BRIGHT}{Fore.GREEN}👌 Toutes les modifications ont été effectuées. Programme terminé.{Style.RESET_ALL}")
    else:
      leave()
  else:
    print(f"{Style.BRIGHT}{Fore.RED}❌ Aucune modification n'a été effectuée. Aucune sauvegarde nécessaire...{Style.RESET_ALL}")



#####################
##### Execution #####
#####################
if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt:
    print(f"{Style.BRIGHT}{Fore.BLUE}👋 Opération interrompue par l'utilisateur. Programme terminé.{Style.RESET_ALL}")
  finally:
    tkInstance.quit()
    tkInstance.destroy()
    sys.exit(0)
