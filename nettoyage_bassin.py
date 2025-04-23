import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QFormLayout, QLineEdit, QPushButton,
    QVBoxLayout, QComboBox, QLabel, QHBoxLayout, QTextEdit, QCheckBox, QGridLayout, QScrollArea
)
from PyQt6.QtGui import QIntValidator, QDoubleValidator
from PyQt6.QtCore import Qt, QDate
from reportlab.pdfgen import canvas
from datetime import datetime


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nettoyage Bassin")
        self.setGeometry(100, 100, 500, 600)


        # Widget central et layout principal
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        layout = QVBoxLayout(scroll_content)

        scroll_area.setWidget(scroll_content)
        self.setCentralWidget(scroll_area)

        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Date d'intervention (automatique)
        self.jour_input = self.create_line_edit(QIntValidator(1, 31), "Jour", read_only=True)
        self.mois_input = self.create_line_edit(QIntValidator(1, 12), "Mois", read_only=True)
        self.annee_input = self.create_line_edit(QIntValidator(2020, 2100), "Année", read_only=True)
        date_layout = QHBoxLayout()
        date_layout.addWidget(self.jour_input)
        date_layout.addWidget(self.mois_input)
        date_layout.addWidget(self.annee_input)

        # Heure d'intervention
        heure_layout = QHBoxLayout()
        self.heure_debut_input = self.create_line_edit(QIntValidator(0, 23), "Heure début")
        self.minute_debut_input = self.create_line_edit(QIntValidator(0, 59), "Min début")
        self.heure_fin_input = self.create_line_edit(QIntValidator(0, 23), "Heure fin")
        self.minute_fin_input = self.create_line_edit(QIntValidator(0, 59), "Min fin")
        heure_layout.addWidget(self.heure_debut_input)
        heure_layout.addWidget(self.minute_debut_input)
        heure_layout.addWidget(QLabel("à"))
        heure_layout.addWidget(self.heure_fin_input)
        heure_layout.addWidget(self.minute_fin_input)

        # Technicien (maintenant un champ de texte)
        self.technicien_input = QLineEdit()
        self.technicien_input.setPlaceholderText("Nom du technicien")
        self.technicien_input.setFixedHeight(30)

        # Type d'intervention
        self.type_intervention = QComboBox()
        self.type_intervention.addItems([
            "Nettoyage hebdomadaire", 
            "Nettoyage mensuel", 
            "Intervention d'urgence", 
            "Maintenance préventive"
        ])
        
        # Produits utilisés (modifiés)
        self.produits_grid = QGridLayout()
        self.produits_grid.addWidget(QLabel(" "), 0, 0)
        self.produits_grid.addWidget(QLabel("raison"), 0, 1)
        
        self.produit1_check = QCheckBox("Nettoyage bassin")
        self.produit1_qte = self.create_line_edit()
        self.produits_grid.addWidget(self.produit1_check, 1, 0)
        self.produits_grid.addWidget(self.produit1_qte, 1, 1)
        
        self.produit2_check = QCheckBox("Borkler")
        self.produit2_qte = self.create_line_edit()
        self.produits_grid.addWidget(self.produit2_check, 2, 0)
        self.produits_grid.addWidget(self.produit2_qte, 2, 1)
        
        # Actions effectuées
        self.actions_layout = QVBoxLayout()
        self.actions_layout.addWidget(QLabel("Actions effectuées:"))
        
        self.action6 = QCheckBox("Lavage du filtre")
        self.actions_layout.addWidget(self.action6)
        
        # Nouvel élément: Préfiltre
        self.action7 = QCheckBox("Nettoyage du préfiltre")
        self.actions_layout.addWidget(self.action7)
        
        # Nouvel élément: Filtre
        self.action8 = QCheckBox("Nettoyage du filtre")
        self.actions_layout.addWidget(self.action8)
        
        # Nouvel élément: Apport d'eau
        self.apport_eau_layout = QHBoxLayout()
        self.apport_eau_check = QCheckBox("Apport d'eau")
        self.apport_eau_qte = self.create_line_edit(QIntValidator(0, 10000), "Litres")
        self.apport_eau_layout.addWidget(self.apport_eau_check)
        self.apport_eau_layout.addWidget(self.apport_eau_qte)
        self.actions_layout.addLayout(self.apport_eau_layout)
        
        self.autre = QLineEdit()
        self.autre.setPlaceholderText("Autres actions")
        
        # État du bassin avant intervention
        self.etat_avant = QComboBox()
        self.etat_avant.addItems(["Bon", "Moyen", "Mauvais", "Critique"])
        
        # Observations
        self.observations = QTextEdit()
        self.observations.setPlaceholderText("Observations et commentaires supplémentaires...")
        self.observations.setMaximumHeight(100)
        
        # Prochaine intervention
        self.date_prochaine = self.create_line_edit(QIntValidator())
        
        # Form layout
        form_layout = QFormLayout()
        form_layout.addRow("Date d'intervention :", date_layout)
        form_layout.addRow("Horaire :", heure_layout)
        form_layout.addRow("Technicien :", self.technicien_input)
        form_layout.addRow("Type d'intervention :", self.type_intervention)
        form_layout.addRow("Nettoyage bassin :", self.produits_grid)
        form_layout.addRow("Actions :", self.actions_layout)
        form_layout.addRow("Autres actions :", self.autre)
        form_layout.addRow("État avant intervention :", self.etat_avant)
        form_layout.addRow("Observations :", self.observations)
        form_layout.addRow("Prochaine intervention (jours) :", self.date_prochaine)

        layout.addLayout(form_layout)

        # Boutons
        buttons_layout = QHBoxLayout()
        
        self.submit_button = QPushButton("Générer Rapport")
        self.submit_button.setFixedHeight(40)
        self.submit_button.setStyleSheet("font-weight: bold; background-color: #87CEFA;")
        buttons_layout.addWidget(self.submit_button)
        
        self.clear_button = QPushButton("Effacer")
        self.clear_button.setFixedHeight(40)
        self.clear_button.setStyleSheet("font-weight: bold; background-color: #FFA07A;")
        buttons_layout.addWidget(self.clear_button)
        
        layout.addLayout(buttons_layout)


        # Pré-remplir la date du jour
        today = datetime.now()
        self.jour_input.setText(str(today.day))
        self.mois_input.setText(str(today.month))
        self.annee_input.setText(str(today.year))

        # Connexions
        self.submit_button.clicked.connect(self.recuperer_donnees)
        self.clear_button.clicked.connect(self.effacer_formulaire)

    def create_line_edit(self, validator=None, placeholder="", read_only=False):
        edit = QLineEdit()
        if validator:
            edit.setValidator(validator)
        if placeholder:
            edit.setPlaceholderText(placeholder)
        if read_only:
            edit.setReadOnly(True)
            edit.setStyleSheet("background-color: black;")
        edit.setFixedHeight(30)
        return edit

    def effacer_formulaire(self):
        # Date conservée, réinitialisation des autres champs
        self.heure_debut_input.clear()
        self.minute_debut_input.clear()
        self.heure_fin_input.clear()
        self.minute_fin_input.clear()
        self.technicien_input.clear()
        self.type_intervention.setCurrentIndex(0)
        
        # Réinitialisation des produits
        self.produit1_check.setChecked(False)
        self.produit1_qte.clear()
        self.produit2_check.setChecked(False)
        self.produit2_qte.clear()
        
        # Réinitialisation des actions
        self.action6.setChecked(False)
        self.action7.setChecked(False)
        self.action8.setChecked(False)
        self.apport_eau_check.setChecked(False)
        self.apport_eau_qte.clear()
        
        self.autre.clear()
        self.autre.setPlaceholderText("Autres actions")
        
        # États et observations
        self.etat_avant.setCurrentIndex(0)
        self.observations.clear()
        self.date_prochaine.clear()

    def recuperer_donnees(self):
        # Récupération des données
        date = f"{self.jour_input.text()}/{self.mois_input.text()}/{self.annee_input.text()}"
        horaire = f"{self.heure_debut_input.text()}:{self.minute_debut_input.text()} à {self.heure_fin_input.text()}:{self.minute_fin_input.text()}"
        technicien = self.technicien_input.text()
        type_interv = self.type_intervention.currentText()
        
        # Produits utilisés
        produits = []
        
        
        # Actions effectuées
        actions = []
        if self.action6.isChecked():
            actions.append("Lavage du filtre")
        if self.action7.isChecked():
            actions.append("Nettoyage du préfiltre")
        if self.action8.isChecked():
            actions.append("Nettoyage du filtre")
        
        # Apport d'eau
        apport_eau = ""
        if self.apport_eau_check.isChecked():
            apport_eau = f"{self.apport_eau_qte.text()} L"
            
        autre = ''
        if self.autre.text():
            autre = self.autre.text()
        
        etat_avant = self.etat_avant.currentText()
        observations = self.observations.toPlainText()
        prochaine = self.date_prochaine.text()
        
        # Sauvegarde dans un fichier
        with open("nettoyage_bassin.txt", "w") as file:
            file.write(f"Date d'intervention: {date}\n")
            file.write(f"Horaire: {horaire}\n")
            file.write(f"Technicien: {technicien}\n")
            file.write(f"Type d'intervention: {type_interv}\n")
            file.write("nettoyage fait :\n")
            for produit in produits:
                file.write(f"- {produit}\n")
            file.write("Actions effectuées:\n")
            for action in actions:
                file.write(f"- {action}\n")
            if apport_eau:
                file.write(f"Apport d'eau: {apport_eau}\n")
            file.write(f"Autres actions: {autre}\n")
            file.write(f"État avant intervention: {etat_avant}\n")
            file.write(f"Observations: {observations}\n")
            file.write(f"Prochaine intervention (jours): {prochaine}\n")
            
        print("Données sauvegardées dans nettoyage_bassin.txt")
        
        # Génération du PDF
        self.generer_pdf(date, horaire, technicien, type_interv, produits, actions, 
                         etat_avant, observations, prochaine, apport_eau, autre)

    def generer_pdf(self, date, horaire, technicien, type_interv, produits, actions, 
                   etat_avant, observations, prochaine, apport_eau, autre):
        month_name = datetime.now().strftime("%B")
        pdf_file = f"./{month_name}/rapport_nettoyage_{date.replace('/', '-')}.pdf"
        c = canvas.Canvas(pdf_file)
        c.setPageSize((595, 842))  # A4 portrait

        # Titre
        c.setFont("Helvetica-Bold", 20)
        c.setStrokeColorRGB(0, 0.5, 1)
        c.setFillColorRGB(0.9, 0.9, 0.9)
        c.rect(40, 770, 515, 40, stroke=1, fill=1)
        c.setFillColorRGB(0, 0, 0)
        c.drawString(50, 780, "Rapport de Nettoyage Bassin")

        # Date et Horodatage
        c.setFont("Helvetica", 11)
        horodatage = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Ajouter l'image tampon.jpg en bas du PDF
        try:
            c.drawImage("tampon.jpg", 395, 40, width=150, height=75)  # Position en bas à droite avec taille ajustée
        except Exception as e:
            print(f"Erreur lors de l'ajout de l'image : {e}")
    
        # Ajouter l'horodatage sous l'image
        c.setFont("Helvetica", 10)
        c.drawString(50, 55, f"Horodatage : {horodatage}")

        # Informations principales
        y = 730
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Informations d'intervention")
        y -= 20
        
        c.setFont("Helvetica", 11)
        c.drawString(50, y, f"Date d'intervention: {date}")
        y -= 20
        c.drawString(50, y, f"Horaire: {horaire}")
        y -= 20
        c.drawString(50, y, f"Technicien: {technicien}")
        y -= 20
        c.drawString(50, y, f"Type d'intervention: {type_interv}")
        y -= 30

        # Produits utilisés
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Produits utilisés:")
        y -= 20
        c.setFont("Helvetica", 11)
        if not produits:
            c.drawString(70, y, "Aucun produit utilisé")
            y -= 20
        else:
            for produit in produits:
                c.drawString(70, y, produit)
                y -= 20
        y -= 10

        # Actions effectuées
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Actions effectuées:")
        y -= 20
        c.setFont("Helvetica", 11)
        if not actions:
            c.drawString(70, y, "Aucune action effectuée")
            y -= 20
        else:
            for action in actions:
                c.drawString(70, y, action)
                y -= 20
        y -= 10

        # Apport d'eau
        if apport_eau:
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y, "Apport d'eau:")
            y -= 20
            c.setFont("Helvetica", 11)
            c.drawString(70, y, apport_eau)
            y -= 30
        
        # Autres actions
        if autre:
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y, "Autres actions:")
            y -= 20
            c.setFont("Helvetica", 11)
            c.drawString(70, y, autre)
            y -= 30
        
        # État du bassin
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "État du bassin:")
        y -= 20
        c.setFont("Helvetica", 11)
        c.drawString(70, y, f"Avant intervention: {etat_avant}")
        y -= 30

        # Observations
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Observations:")
        y -= 20
        c.setFont("Helvetica", 11)
        
        # Gestion du texte multilignes
        if observations:
            text_object = c.beginText(70, y)
            text_object.setFont("Helvetica", 11)
            
            # Découper le texte en lignes de 70 caractères max
            words = observations.split()
            lines = []
            current_line = ""
            
            for word in words:
                if len(current_line + " " + word) <= 70:
                    current_line += " " + word if current_line else word
                else:
                    lines.append(current_line)
                    current_line = word
            
            if current_line:
                lines.append(current_line)
                
            for line in lines:
                text_object.textLine(line)
                
            c.drawText(text_object)
            y -= (len(lines) * 15 + 20)
        else:
            c.drawString(70, y, "Aucune observation")
            y -= 30

        # Prochaine intervention
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Prochaine intervention:")
        y -= 20
        c.setFont("Helvetica", 11)
        if prochaine:
            date_future = datetime.now()
            try:
                jours = int(prochaine)
                date_intervention = datetime.now()
                from datetime import timedelta
                date_future = date_intervention + timedelta(days=jours)
                date_future_str = date_future.strftime("%d/%m/%Y")
                c.drawString(70, y, f"Dans {prochaine} jours (le {date_future_str})")
            except ValueError:
                c.drawString(70, y, f"Dans {prochaine} jours")
        else:
            c.drawString(70, y, "Non planifiée")

        # Pied de page
        c.setFont("Helvetica-Oblique", 9)
        c.drawString(50, 50, "Ce document est généré automatiquement par l'application Nettoyage Bassin.")
        c.drawString(50, 35, "Contactez le service technique pour toute question.")

        c.save()
        print(f"PDF généré : {pdf_file}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())