import sys
import subprocess
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout,
                             QWidget, QHBoxLayout)
from PyQt6.QtCore import Qt
import webbrowser


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion Piscine")
        self.setGeometry(100, 100, 500, 300)

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal horizontal
        main_layout = QHBoxLayout()

        # Layout pour les contrôles et boutons
        controls_layout = QVBoxLayout()

        # Bouton pour lancer pool_analyser
        self.pool_analyser_button = QPushButton("Lancer Pool Analyser")
        self.pool_analyser_button.clicked.connect(self.launch_pool_analyser)
        controls_layout.addWidget(self.pool_analyser_button)

        # Bouton pour lancer nettoyage_bassin
        self.nettoyage_bassin_button = QPushButton("Lancer Nettoyage Bassin")
        self.nettoyage_bassin_button.clicked.connect(self.launch_nettoyage_bassin)
        controls_layout.addWidget(self.nettoyage_bassin_button)

        # Bouton pour lancer ars
        self.ars_button = QPushButton("Lancer ARS")
        self.ars_button.clicked.connect(self.launch_ars)
        controls_layout.addWidget(self.ars_button)

        # Bouton procrastinateur (caché au départ)
        self.procrastinateur_button = QPushButton("Lancer Procrastination")
        self.procrastinateur_button.setStyleSheet("background-color: yellow; color: black; font-weight: bold;")
        self.procrastinateur_button.clicked.connect(self.procrastinateur)
        self.procrastinateur_button.setVisible(False)
        controls_layout.addWidget(self.procrastinateur_button)

        # Bouton secret (caché au départ)
        self.secret_button = QPushButton("Panic Button!")
        self.secret_button.setStyleSheet("background-color: red; color: white; font-weight: bold;")
        self.secret_button.clicked.connect(self.launch_secret_script)
        self.secret_button.setVisible(False)
        controls_layout.addWidget(self.secret_button)

        # Widget transparent pour les clics cachés
        self.click_counter = 0
        self.placeholder_widget = QPushButton("")
        self.placeholder_widget.setStyleSheet("background-color: transparent; border: none;")
        self.placeholder_widget.clicked.connect(self.increment_click_counter)
        controls_layout.addWidget(self.placeholder_widget)
        
        #boutton save to csv
        self.save_to_csv_button = QPushButton("Save to CSV")
        self.save_to_csv_button.clicked.connect(self.text_to_csv)
        controls_layout.addWidget(self.save_to_csv_button)

        # Ajouter les contrôles au layout principal
        main_layout.addLayout(controls_layout)
        central_widget.setLayout(main_layout)

        # Konami code tracking
        self.konami_code = ["up", "up", "down", "down", "left", "right", "left", "right", "b", "a"]
        self.konami_progress = []

        # Permettre à la fenêtre de recevoir le focus clavier
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def keyPressEvent(self, event):
        """Traiter les événements clavier pour le Konami code"""
        key = event.key()
        print(f"Touche pressée: {key}")

        self.process_konami_code(key)

        if key in [Qt.Key.Key_Up, Qt.Key.Key_Down, Qt.Key.Key_Left, Qt.Key.Key_Right, 
                   Qt.Key.Key_A, Qt.Key.Key_B]:
            event.accept()
        else:
            super().keyPressEvent(event)

    def process_konami_code(self, key):
        """Traiter une touche pour le code Konami"""
        key_mapping = {
            Qt.Key.Key_Up: "up",
            Qt.Key.Key_Down: "down",
            Qt.Key.Key_Left: "left",
            Qt.Key.Key_Right: "right",
            Qt.Key.Key_A: "a",
            Qt.Key.Key_B: "b"
        }

        if key in key_mapping:
            pressed_key = key_mapping[key]

            # Gestion des touches "up"
            if pressed_key == "up":
                if not self.konami_progress or self.konami_progress[-1] == "up":
                    if len(self.konami_progress) == 0:
                        self.konami_progress = ["up"]
                    else:
                        self.konami_progress.append("up")
                else:
                    self.konami_progress = ["up"]

            # Gestion des autres touches
            elif self.konami_progress:
                expected_key = self.konami_code[len(self.konami_progress)]
                if pressed_key == expected_key:
                    self.konami_progress.append(pressed_key)
                else:
                    self.konami_progress = ["up"] if pressed_key == "up" else []

            print(f"Progression Konami: {self.konami_progress}")

            # Si le code est complet
            if len(self.konami_progress) == len(self.konami_code):
                self.activate_konami_code()

    def activate_konami_code(self):
        """Activer le bouton Procrastination"""
        print("CODE KONAMI ACTIVÉ!")
        self.procrastinateur_button.setVisible(True)
        self.konami_progress = []

    def increment_click_counter(self):
        """Incrémenter le compteur et afficher le bouton secret après 5 clics"""
        self.click_counter += 1
        print(f"Nombre de clics : {self.click_counter}")
        if self.click_counter >= 5:
            self.secret_button.setVisible(True)
            self.placeholder_widget.setVisible(False)

    def launch_pool_analyser(self):
        """Lancer le script pool_analyser.py"""
        try:
            subprocess.Popen(["python", "pool_analyser.py"])
        except Exception as e:
            print(f"Erreur lors du lancement de pool_analyser.py : {e}")

    def launch_nettoyage_bassin(self):
        """Lancer le script nettoyage_bassin.py"""
        try:
            subprocess.Popen(["python", "nettoyage_bassin.py"])
        except Exception as e:
            print(f"Erreur lors du lancement de nettoyage_bassin.py : {e}")

    def launch_ars(self):
        """Lancer le script ars.py"""
        try:
            subprocess.Popen(["python", "ars.py"])
        except Exception as e:
            print(f"Erreur lors du lancement de ars.py : {e}")

    def launch_secret_script(self):
        """Lancer l'easter egg vidéo"""
        try:
            webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        except Exception as e:
            print(f"Erreur lors de l'ouverture de la vidéo : {e}")

    def procrastinateur(self):
        """Lancer un faux écran de mise à jour Windows"""
        try:
            webbrowser.open("https://www.whitescreen.online/fr/ecran-fausse-mise-a-jour-windows-11/")
        except Exception as e:
            print(f"Erreur lors du lancement de procrastinateur : {e}")

    def showEvent(self, event):
        """Donner le focus à l'application au démarrage"""
        super().showEvent(event)
        self.setFocus()
        self.activateWindow()
        
    def text_to_csv(self):
        """Convertir le fichier texte en CSV"""
        try:
            subprocess.Popen(["python", "text_to_csv.py"])
        except Exception as e:
            print(f"Erreur lors du lancement de text_to_csv.py : {e}")
    
    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
