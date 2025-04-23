# Gestion Piscine

Ce projet est une application de gestion pour les piscines, permettant de réaliser des analyses, des nettoyages et des rapports pour l'ARS (Agence Régionale de Santé). L'application est développée en **Python** avec **PyQt6** pour l'interface graphique et **ReportLab** pour la génération de fichiers PDF.

---

## Fonctionnalités

### 1. **MainApp**
- Interface principale avec des boutons pour lancer les différents modules :
  - **Pool Analyser** : Analyse des données de la piscine.
  - **Nettoyage Bassin** : Gestion des nettoyages et interventions.
  - **ARS** : Génération de rapports pour l'ARS.
  - **Save to CSV** : Convertit les données texte en fichier CSV.

### 2. **Pool Analyser**
- Permet de saisir les données d'analyse de la piscine :
  - pH, chlore, DPD1, DPD total, etc.
  - Calcul automatique de la chloramine.
- Génère un fichier texte et un PDF avec les résultats.
- Affiche des statuts (Bonne, À Surveiller, Mauvaise) en fonction des valeurs saisies.

### 3. **Nettoyage Bassin**
- Gestion des interventions de nettoyage :
  - Saisie des produits utilisés, actions effectuées, observations, etc.
  - Génération d'un rapport PDF avec les détails de l'intervention.
  - Possibilité de planifier une prochaine intervention.

### 4. **ARS**
- Génération de rapports spécifiques pour l'ARS.
- Saisie des données d'analyse et génération d'un PDF avec mise en forme spécifique.

### 5. **Text to CSV**
- Convertit les données sauvegardées dans un fichier texte (`save_val.txt`) en un fichier CSV.

---

## Installation

### Prérequis
- **Python 3.10+**
- Bibliothèques Python :
  - `PyQt6`
  - `reportlab`

### Installation des dépendances
Exécutez la commande suivante pour installer les dépendances :
```bash
pip install PyQt6 reportlab
```
### Auteur
[Damman Alexandre](https://github.com/kaldex0)