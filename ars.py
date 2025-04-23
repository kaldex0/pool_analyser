import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QFormLayout, QLineEdit, QPushButton,
    QVBoxLayout, QComboBox, QLabel, QHBoxLayout
)
from PyQt6.QtGui import QIntValidator, QDoubleValidator
from PyQt6.QtCore import Qt
from reportlab.pdfgen import canvas
from datetime import datetime


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Analyse Piscine ARS")
        self.setGeometry(100, 100, 400, 700)

        # Widget central et layout principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Champs de formulaire
        self.cumule_input = self.create_line_edit(QIntValidator())
        self.report_input = self.create_line_edit(read_only=True)

        # Heure de prélèvement (Heure + Minute)
        self.heure_input = self.create_line_edit(QIntValidator(0, 99), "Heures")
        self.minute_input = self.create_line_edit(QIntValidator(0, 99), "Minutes")
        heure_layout = QHBoxLayout()
        heure_layout.addWidget(self.heure_input)
        heure_layout.addWidget(self.minute_input)

        # Autres champs
        self.point_input = QComboBox()
        self.point_input.addItems(["Bord piscine", "Centre piscine"])

        self.trans_input = self.create_line_edit()
        self.temp_air_input = self.create_line_edit(QIntValidator())
        self.temp_eau_input = self.create_line_edit(QIntValidator())
        self.ph_input = self.create_line_edit(QDoubleValidator(0.0, 14.0, 2))
        self.chlore_input = self.create_line_edit(QDoubleValidator(0.0, 14.0, 2))
        self.dpd1_input = self.create_line_edit()
        self.chlore_actif_input = self.create_line_edit()
        self.total_dpd_input = self.create_line_edit()
        # self.chloramine_input = self.create_line_edit()

        self.ph_status = QLabel()
        self.chlore_status = QLabel()

        # Form layout
        form_layout = QFormLayout()
        form_layout.addRow("Cumul à ce jour :", self.cumule_input)
        form_layout.addRow("Report de la veille :", self.report_input)
        form_layout.addRow("Heure de prélèvement :", heure_layout)
        form_layout.addRow("Point de prélèvement :", self.point_input)
        form_layout.addRow("Transparence :", self.trans_input)
        form_layout.addRow("Température Air (°C) :", self.temp_air_input)
        form_layout.addRow("Température Eau (°C) :", self.temp_eau_input)
        form_layout.addRow("pH :", self.ph_input)
        form_layout.addRow("pH Statut :", self.ph_status)
        form_layout.addRow("Chlore (mg/L) :", self.chlore_input)
        form_layout.addRow("Chlore Statut :", self.chlore_status)
        form_layout.addRow("DPD1 :", self.dpd1_input)
        form_layout.addRow("Chlore Actif :", self.chlore_actif_input)
        form_layout.addRow("Total (DPD1 + DPD3) :", self.total_dpd_input)
        # form_layout.addRow("Chloramine :", self.chloramine_input)

        layout.addLayout(form_layout)

        # Bouton
        self.submit_button = QPushButton("Générer Rapport")
        self.submit_button.setFixedHeight(40)
        self.submit_button.setStyleSheet("font-weight: bold; background-color: #87CEFA;")
        layout.addWidget(self.submit_button, alignment=Qt.AlignmentFlag.AlignCenter)

        central_widget.setLayout(layout)

        self.load_report_value()

        # Connexions
        self.submit_button.clicked.connect(self.recuperer_donnees)
        self.submit_button.clicked.connect(self.backup_donnees)
        self.submit_button.clicked.connect(self.recuperer_donnees_pdf)

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

    def load_report_value(self):
        try:
            with open("backup.txt", "r") as file:
                for line in file:
                    if line.startswith("Cumul à ce jour:"):
                        self.report_input.setText(line.split(":")[1].strip())
                        break
        except FileNotFoundError:
            self.report_input.setText("Fichier non trouvé")
        except Exception as e:
            self.report_input.setText(f"Erreur: {e}")

    def generer_pdf(self, data):
        """Génère un fichier PDF avec les données du formulaire, avec mise en forme spécifique."""
        month_name = datetime.now().strftime("%B")
        date_du_jour = datetime.now().strftime("%Y-%m-%d")
        pdf_file = f"./{month_name}/controle_ars_{date_du_jour}.pdf"
        c = canvas.Canvas(pdf_file)
        c.setPageSize((595, 842))  # A4 portrait
    
        # Titre
        c.setFont("Helvetica-Bold", 20)
        c.setStrokeColorRGB(0, 0.5, 1)
        c.setFillColorRGB(0.9, 0.9, 0.9)
        c.rect(40, 770, 515, 40, stroke=1, fill=1)
        c.setFillColorRGB(0, 0, 0)
        c.drawString(50, 780, "controle piscine ars")
    
        # Date et Horodatage
        c.setFont("Helvetica", 11)
        horodatage = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
        # Statut général
        statut, couleur = self.calcul_statut(data)
        c.setStrokeColorRGB(*couleur)
        c.setFillColorRGB(*couleur)
        c.rect(40, 720, 515, 30, stroke=1, fill=0)
        c.setFont("Helvetica-Bold", 13)
        c.setFillColorRGB(0, 0, 0)
        c.drawString(50, 730, f"Statut Générale : {statut}")
    
        # Encadrés pH et Chlore
        self.draw_param_box(c, "pH", data["pH"], 650, *self.couleur_ph(float(data["pH"])))
        self.draw_param_box(c, "Chlore", data["Chlore"], 600, *self.couleur_chlore(float(data["Chlore"])))
    
        # Autres données
        c.setFont("Helvetica", 11)
        y = 550
        for key, value in data.items():
            if key not in ["pH", "Chlore"]:
                c.drawString(50, y, f"{key} : {value}")
                y -= 20
    
        # Ajouter l'image tampon.jpg en bas du PDF
        try:
            c.drawImage("tampon.jpg", 395, 40, width=150, height=75)  # Position en bas à droite avec taille ajustée
        except Exception as e:
            print(f"Erreur lors de l'ajout de l'image : {e}")
    
        # Ajouter l'horodatage sous l'image
        c.setFont("Helvetica", 10)
        c.drawString(250, 40, f"Horodatage : {horodatage}")
    
        c.save()
        print(f"PDF généré : {pdf_file}")

    def draw_param_box(self, c, label, value, y, r, g, b):
        c.setStrokeColorRGB(r, g, b)
        c.setFillColorRGB(r, g, b)
        c.rect(40, y, 250, 30, stroke=1, fill=0)
        c.setFillColorRGB(0, 0, 0)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y + 10, f"{label} : {value}")

    def calcul_statut(self, data):
        ph = float(data["pH"])
        chlore = float(data["Chlore"])
        if 7 <= ph <= 7.4 and 0.4 <= chlore <= 1.3:
            return "Bonne", (0, 1, 0)
        elif (6.5 <= ph < 7 or 7.4 < ph <= 8) or (0.3 <= chlore < 0.4 or 1.3 < chlore <= 1.5):
            return "À Surveiller", (1, 0.5, 0)
        else:
            return "Mauvaise", (1, 0, 0)

    def couleur_ph(self, ph):
        if 7 <= ph <= 7.4:
            return (0, 1, 0)
        elif 6.5 <= ph < 7 or 7.4 < ph <= 8:
            return (1, 0.5, 0)
        else:
            return (1, 0, 0)

    def couleur_chlore(self, chlore):
        if 0.4 <= chlore <= 0.8:
            return (1, 0.5, 0)
        elif 0.81 <= chlore <= 1.3:
            return (0, 1, 0)
        else:
            return (1, 0, 0)

    def recuperer_donnees(self):
        month_name = datetime.now().strftime("%B")
        cumule = self.cumule_input.text()
        report = self.report_input.text()
        heure = self.heure_input.text()
        minute = self.minute_input.text()
        point = self.point_input.currentText()
        transparence = self.trans_input.text()
        temp_air = self.temp_air_input.text()
        temp_eau = self.temp_eau_input.text()
        ph = self.ph_input.text()
        chlore = self.chlore_input.text()
        dpd1 = self.dpd1_input.text()
        chlore_actif = self.chlore_actif_input.text()
        total_dpd = self.total_dpd_input.text()

        # Calculer la chloramine avec gestion des erreurs
        try:
            if dpd1 and total_dpd:  # Vérifier que les deux champs ne sont pas vides
                dpd1_val = float(dpd1)
                total_dpd_val = float(total_dpd)
                chloramine = f"{total_dpd_val - dpd1_val:.2f}"
            else:
                chloramine = "N/A"
        except ValueError:
            chloramine = "Erreur de calcul"

        self.validate_ph(ph)
        self.validate_chlore(chlore)
        
        if not os.path.exists(month_name):
            os.makedirs(month_name)
        
        file_path = os.path.join(month_name, "save_val.txt")

        with open(file_path, "w") as file:
            file.write(f"Cumul à ce jour: {cumule}\n")
            file.write(f"Report de la veille: {report}\n")
            file.write(f"Heure de prélèvement: {heure}:{minute}\n")
            file.write(f"Point de prélèvement: {point}\n")
            file.write(f"Transparence: {transparence}\n")
            file.write(f"Température Air: {temp_air}\n")
            file.write(f"Température Eau: {temp_eau}\n")
            file.write(f"pH: {ph}\n")
            file.write(f"Chlore: {chlore}\n")
            file.write(f"DPD1: {dpd1}\n")
            file.write(f"Chlore Actif: {chlore_actif}\n")
            file.write(f"Total (DPD1 + DPD3): {total_dpd}\n")
            file.write(f"Chloramine: {chloramine}\n")
            file.write(f"Date: {datetime.now().strftime('%Y-%m-%d')}\n")
        print("Données sauvegardées dans save_val.txt")
        
    def backup_donnees(self):
        month_name = datetime.now().strftime("%B")
        cumule = self.cumule_input.text()
        report = self.report_input.text()
        heure = self.heure_input.text()
        minute = self.minute_input.text()
        point = self.point_input.currentText()
        transparence = self.trans_input.text()
        temp_air = self.temp_air_input.text()
        temp_eau = self.temp_eau_input.text()
        ph = self.ph_input.text()
        chlore = self.chlore_input.text()
        dpd1 = self.dpd1_input.text()
        chlore_actif = self.chlore_actif_input.text()
        total_dpd = self.total_dpd_input.text()

        # Calculer la chloramine avec gestion des erreurs
        try:
            if dpd1 and total_dpd:  # Vérifier que les deux champs ne sont pas vides
                dpd1_val = float(dpd1)
                total_dpd_val = float(total_dpd)
                chloramine = f"{total_dpd_val - dpd1_val:.2f}"
            else:
                chloramine = "N/A"
        except ValueError:
            chloramine = "Erreur de calcul"

        self.validate_ph(ph)
        self.validate_chlore(chlore)
        
        if not os.path.exists(month_name):
            os.makedirs(month_name)
        
        file_path = os.path.join("backup.txt")

        with open(file_path, "w") as file:
            file.write(f"Cumul à ce jour: {cumule}\n")
            file.write(f"Report de la veille: {report}\n")
            file.write(f"Heure de prélèvement: {heure}:{minute}\n")
            file.write(f"Point de prélèvement: {point}\n")
            file.write(f"Transparence: {transparence}\n")
            file.write(f"Température Air: {temp_air}\n")
            file.write(f"Température Eau: {temp_eau}\n")
            file.write(f"pH: {ph}\n")
            file.write(f"Chlore: {chlore}\n")
            file.write(f"DPD1: {dpd1}\n")
            file.write(f"Chlore Actif: {chlore_actif}\n")
            file.write(f"Total (DPD1 + DPD3): {total_dpd}\n")
            file.write(f"Chloramine: {chloramine}\n")
            file.write(f"Date: {datetime.now().strftime('%Y-%m-%d')}\n")
        print("Données sauvegardées dans save_val.txt")
    

    def validate_ph(self, ph):
        try:
            ph_value = float(ph)
            if 7 <= ph_value <= 7.4:
                self.ph_status.setText("OK")
                self.ph_status.setStyleSheet("color: green;")
            else:
                self.ph_status.setText("Pas bon")
                self.ph_status.setStyleSheet("color: red;")
        except ValueError:
            self.ph_status.setText("Valeur invalide")
            self.ph_status.setStyleSheet("color: red;")

    def validate_chlore(self, chlore):
        try:
            chlore_value = float(chlore)
            if 0.4 <= chlore_value <= 0.8:
                self.chlore_status.setText("Orange")
                self.chlore_status.setStyleSheet("color: orange;")
            elif 0.81 <= chlore_value <= 1.3:
                self.chlore_status.setText("Vert")
                self.chlore_status.setStyleSheet("color: green;")
            else:
                self.chlore_status.setText("Rouge")
                self.chlore_status.setStyleSheet("color: red;")
        except ValueError:
            self.chlore_status.setText("Valeur invalide")
            self.chlore_status.setStyleSheet("color: red;")

    def recuperer_donnees_pdf(self):
        """Récupère les données du formulaire, calcule la chloramine et génère un PDF."""
        # Calcul de la chloramine avec gestion des erreurs
        try:
            dpd1_text = self.dpd1_input.text()
            total_dpd_text = self.total_dpd_input.text()
            
            if dpd1_text and total_dpd_text:  # Vérifier que les champs ne sont pas vides
                dpd1 = float(dpd1_text)
                total_dpd = float(total_dpd_text)
                chloramine = f"{total_dpd - dpd1:.2f}"
            else:
                chloramine = "N/A"
        except ValueError:
            chloramine = "Erreur de calcul"
        
        # Préparer les données pour le PDF
        data = {
            "Cumul à ce jour": self.cumule_input.text() or "N/A",
            "Report de la veille": self.report_input.text() or "N/A",
            "Heure de prélèvement": f"{self.heure_input.text() or '00'}:{self.minute_input.text() or '00'}",
            "Point de prélèvement": self.point_input.currentText(),
            "Transparence": self.trans_input.text() or "N/A",
            "Température Air": self.temp_air_input.text() or "N/A",
            "Température Eau": self.temp_eau_input.text() or "N/A",
            "pH": self.ph_input.text() or "0.0",  # Valeur par défaut pour éviter les erreurs
            "Chlore": self.chlore_input.text() or "0.0",  # Valeur par défaut pour éviter les erreurs
            "DPD1": self.dpd1_input.text() or "N/A",
            "Chlore Actif": self.chlore_actif_input.text() or "N/A",
            "Total (DPD1 + DPD3)": self.total_dpd_input.text() or "N/A",
            "Chloramine": chloramine,
        }
        
        # Vérifier les valeurs numériques nécessaires pour le calcul du statut
        try:
            float(data["pH"])
            float(data["Chlore"])
        except ValueError:
            # Remplacer par des valeurs par défaut si les conversions échouent
            data["pH"] = "7.0"  # Valeur neutre
            data["Chlore"] = "0.0"
        
        # Générer le PDF avec les données
        self.generer_pdf(data)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
