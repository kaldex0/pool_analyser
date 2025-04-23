import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QFormLayout, QLineEdit, QPushButton,
    QVBoxLayout, QComboBox, QLabel, QHBoxLayout, QTextEdit, QCheckBox, QGridLayout
)
from PyQt6.QtGui import QIntValidator, QDoubleValidator
from PyQt6.QtCore import Qt, QDate
from reportlab.pdfgen import canvas
from datetime import datetime


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nettoyage Bassin")
        self.setGeometry(100, 100, 500, 800)

        # Widget central et layout principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Date d'intervention
        date_layout = QHBoxLayout()
        self.jour_input = self.create_line_edit(QIntValidator(1, 31), "Jour")
        self.mois_input = self.create_line_edit(QIntValidator(1, 12), "Mois")
        self.annee_input = self.create_line_edit(QIntValidator(2020, 2100), "Année")
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

        # Technicien
        self.technicien_input = QComboBox()
        self.technicien_input.addItems(["Technicien 1", "Technicien 2", "Technicien 3", "Autre"])

        # Type d'intervention
        self.type_intervention = QComboBox()
        self.type_intervention.addItems([
            "Nettoyage hebdomadaire", 
            "Nettoyage mensuel", 
            "Intervention d'urgence", 
            "Maintenance préventive"
        ])
        
        # Produits utilisés
        self.produits_grid = QGridLayout()
        self.produits_grid.addWidget(QLabel("Produit"), 0, 0)
        self.produits_grid.addWidget(QLabel("Quantité (L)"), 0, 1)
        
        self.produit1_check = QCheckBox("Chlore liquide")
        self.produit1_qte = self.create_line_edit(QDoubleValidator(0.0, 100.0, 2))
        self.produits_grid.addWidget(self.produit1_check, 1, 0)
        self.produits_grid.addWidget(self.produit1_qte, 1, 1)
        
        self.produit2_check = QCheckBox("Régulateur pH")
        self.produit2_qte = self.create_line_edit(QDoubleValidator(0.0, 100.0, 2))
        self.produits_grid.addWidget(self.produit2_check, 2, 0)
        self.produits_grid.addWidget(self.produit2_qte, 2, 1)
        
        self.produit3_check = QCheckBox("Anti-algues")
        self.produit3_qte = self.create_line_edit(QDoubleValidator(0.0, 100.0, 2))
        self.produits_grid.addWidget(self.produit3_check, 3, 0)
        self.produits_grid.addWidget(self.produit3_qte, 3, 1)
        
        self.produit4_check = QCheckBox("Floculant")
        self.produit4_qte = self.create_line_edit(QDoubleValidator(0.0, 100.0, 2))
        self.produits_grid.addWidget(self.produit4_check, 4, 0)
        self.produits_grid.addWidget(self.produit4_qte, 4, 1)
        
        # Actions effectuées
        self.actions_layout = QVBoxLayout()
        self.actions_layout.addWidget(QLabel("Actions effectuées:"))
        
        self.action1 = QCheckBox("Nettoyage des skimmers")
        self.actions_layout.addWidget(self.action1)
        
        self.action2 = QCheckBox("Nettoyage des parois")
        self.actions_layout.addWidget(self.action2)
        
        self.action3 = QCheckBox("Nettoyage du fond")
        self.actions_layout.addWidget(self.action3)
        
        self.action4 = QCheckBox("Nettoyage de la ligne d'eau")
        self.actions_layout.addWidget(self.action4)
        
        self.action5 = QCheckBox("Contrôle du système de filtration")
        self.actions_layout.addWidget(self.action5)
        
        self.action6 = QCheckBox("Lavage du filtre")
        self.actions_layout.addWidget(self.action6)
        
        # État du bassin avant intervention
        self.etat_avant = QComboBox()
        self.etat_avant.addItems(["Bon", "Moyen", "Mauvais", "Critique"])
        
        # État du bassin après intervention
        self.etat_apres = QComboBox()
        self.etat_apres.addItems(["Bon", "Moyen", "Mauvais", "À surveiller"])
        
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
        form_layout.addRow("Produits utilisés :", self.produits_grid)
        form_layout.addRow("Actions :", self.actions_layout)
        form_layout.addRow("État avant intervention :", self.etat_avant)
        form_layout.addRow("État après intervention :", self.etat_apres)
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

        central_widget.setLayout(layout)

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
            edit.setStyleSheet("background-color: #F0F0F0;")
        edit.setFixedHeight(30)
        return edit

    def effacer_formulaire(self):
        # Date conservée, réinitialisation des autres champs
        self.heure_debut_input.clear()
        self.minute_debut_input.clear()
        self.heure_fin_input.clear()
        self.minute_fin_input.clear()
        self.technicien_input.setCurrentIndex(0)
        self.type_intervention.setCurrentIndex(0)
        
        # Réinitialisation des produits
        self.produit1_check.setChecked(False)
        self.produit1_qte.clear()
        self.produit2_check.setChecked(False)
        self.produit2_qte.clear()
        self.produit3_check.setChecked(False)
        self.produit3_qte.clear()
        self.produit4_check.setChecked(False)
        self.produit4_qte.clear()
        
        # Réinitialisation des actions
        self.action1.setChecked(False)
        self.action2.setChecked(False)
        self.action3.setChecked(False)
        self.action4.setChecked(False)
        self.action5.setChecked(False)
        self.action6.setChecked(False)
        
        # États et observations
        self.etat_avant.setCurrentIndex(0)
        self.etat_apres.setCurrentIndex(0)
        self.observations.clear()
        self.date_prochaine.clear()

    def recuperer_donnees(self):
        # Récupération des données
        date = f"{self.jour_input.text()}/{self.mois_input.text()}/{self.annee_input.text()}"
        horaire = f"{self.heure_debut_input.text()}:{self.minute_debut_input.text()} à {self.heure_fin_input.text()}:{self.minute_fin_input.text()}"
        technicien = self.technicien_input.currentText()
        type_interv = self.type_intervention.currentText()
        
        # Produits utilisés
        produits = []
        if self.produit1_check.isChecked():
            produits.append(f"Chlore liquide: {self.produit1_qte.text()} L")
        if self.produit2_check.isChecked():
            produits.append(f"Régulateur pH: {self.produit2_qte.text()} L")
        if self.produit3_check.isChecked():
            produits.append(f"Anti-algues: {self.produit3_qte.text()} L")
        if self.produit4_check.isChecked():
            produits.append(f"Floculant: {self.produit4_qte.text()} L")
        
        # Actions effectuées
        actions = []
        if self.action1.isChecked():
            actions.append("Nettoyage des skimmers")
        if self.action2.isChecked():
            actions.append("Nettoyage des parois")
        if self.action3.isChecked():
            actions.append("Nettoyage du fond")
        if self.action4.isChecked():
            actions.append("Nettoyage de la ligne d'eau")
        if self.action5.isChecked():
            actions.append("Contrôle du système de filtration")
        if self.action6.isChecked():
            actions.append("Lavage du filtre")
        
        etat_avant = self.etat_avant.currentText()
        etat_apres = self.etat_apres.currentText()
        observations = self.observations.toPlainText()
        prochaine = self.date_prochaine.text()
        
        # Sauvegarde dans un fichier
        with open("nettoyage_bassin.txt", "w") as file:
            file.write(f"Date d'intervention: {date}\n")
            file.write(f"Horaire: {horaire}\n")
            file.write(f"Technicien: {technicien}\n")
            file.write(f"Type d'intervention: {type_interv}\n")
            file.write("Produits utilisés:\n")
            for produit in produits:
                file.write(f"- {produit}\n")
            file.write("Actions effectuées:\n")
            for action in actions:
                file.write(f"- {action}\n")
            file.write(f"État avant intervention: {etat_avant}\n")
            file.write(f"État après intervention: {etat_apres}\n")
            file.write(f"Observations: {observations}\n")
            file.write(f"Prochaine intervention (jours): {prochaine}\n")
            
        print("Données sauvegardées dans nettoyage_bassin.txt")
        
        # Génération du PDF
        self.generer_pdf(date, horaire, technicien, type_interv, produits, actions, 
                         etat_avant, etat_apres, observations, prochaine)

    def generer_pdf(self, date, horaire, technicien, type_interv, produits, actions, 
                   etat_avant, etat_apres, observations, prochaine):
        pdf_file = f"rapport_nettoyage_{date.replace('/', '-')}.pdf"
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
        c.drawRightString(550, 780, f"Généré le : {horodatage}")

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

        # État du bassin
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "État du bassin:")
        y -= 20
        c.setFont("Helvetica", 11)
        c.drawString(70, y, f"Avant intervention: {etat_avant}")
        y -= 20
        c.drawString(70, y, f"Après intervention: {etat_apres}")
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