import csv
from datetime import datetime

def text_to_csv(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as txt_file:
            lines = txt_file.readlines()

        # Extraction des colonnes et des valeurs
        data = []
        for line in lines:
            if ':' in line:  # Vérifie si la ligne contient une clé et une valeur
                key, value = map(str.strip, line.split(':', 1))
                data.append((key, value))

        # Écriture dans le fichier CSV
        file_exists = False
        try:
            with open(output_file, 'r', encoding='utf-8') as csv_file:
                file_exists = True
        except FileNotFoundError:
            pass

        with open(output_file, 'a', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            
            # Écriture des en-têtes (les clés) uniquement si le fichier n'existe pas
            if not file_exists:
                headers = [key for key, _ in data]
                writer.writerow(headers)
            
            # Écriture des valeurs
            values = [value for _, value in data]
            writer.writerow(values)

        print(f"Les données de {input_file} ont été ajoutées à {output_file}.")
    except Exception as e:
        print(f"Erreur : {e}")

# Exemple d'utilisation
month_name = datetime.now().strftime("%B")
input_file = 'save_val.txt'  # Remplacez par le chemin de votre fichier texte
output_file = f"./{month_name}/output.csv"  # Remplacez par le chemin de votre fichier CSV
text_to_csv(input_file, output_file)