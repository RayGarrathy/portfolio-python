import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QLineEdit, QComboBox,
    QCheckBox, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox, QMessageBox
)
from PySide6.QtGui import QFont, QIcon, QRegularExpressionValidator
from PySide6.QtCore import QRegularExpression


class DilutionApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Aide labo - Calculs de dilution")
        self.resize(700, 650)
        self.setWindowIcon(QIcon("./data_aide_labo/ballon.ico"))

        # ------------------- DONNÉES ACIDES -------------------
        self.acides = {
            "Acide chlorhydrique": {"M": 36.461, "densite": 1.07, "purete": 37},
            "Acide nitrique": {"M": 63.01, "densite": 1.39, "purete": 65},
            "Acide sulfurique": {"M": 98.079, "densite": 1.84, "purete": 98},
            "Acide phosphorique": {"M": 97.994, "densite": 1.69, "purete": 85},
        }

        # Layout principal
        main_layout = QVBoxLayout(self)

        # --- Barre du haut ---
        top_bar = QHBoxLayout()
        self.titre_general = QLabel("Aide labo - Calculs de dilution")
        self.titre_general.setFont(QFont("Calibri", 16))
        top_bar.addWidget(self.titre_general)
        top_bar.addStretch()

        # Bouton Reset
        self.btn_reset = QPushButton("Reset")
        self.style_bouton(self.btn_reset, couleur="lightcoral", couleur_pressed="red")
        self.btn_reset.clicked.connect(self.reset_fields)
        top_bar.addWidget(self.btn_reset)

        main_layout.addLayout(top_bar)

        # --- Sections ---
        main_layout.addWidget(self.create_section_acide())
        main_layout.addWidget(self.create_section_poudre())
        main_layout.addWidget(self.create_section_c1v1())

    # ------------------- UTILITAIRES -------------------
    def style_bouton(self, btn, couleur="skyblue", couleur_pressed="deepskyblue"):
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {couleur};
                color: black;
                font-weight: bold;
                border-radius: 5px;
                padding: 5px;
            }}
            QPushButton:pressed {{
                background-color: {couleur_pressed};
                padding-top: 6px;
                padding-left: 6px;
            }}
        """)

    def error_message(self, msg):
        QMessageBox.warning(self, "Erreur", msg)

    def normalize_decimal(self, text):
        """Remplace virgule → point dans tous les champs."""
        sender = self.sender()
        if isinstance(sender, QLineEdit) and "," in text:
            sender.setText(text.replace(",", "."))

#Affichage intelligent des décimales en fonction du nombre
    def smart_format(self, value):
        """Affichage 'intelligent' pour concentrations / volumes."""
        if value is None:
            return ""
        abs_v = abs(value)
        if abs_v < 0.001:
            return f"{value:.4f}"
        if abs_v < 0.1:
            return f"{value:.3f}"
        if abs_v < 1:
            return f"{value:.3f}"
        if abs_v < 10:
            return f"{value:.2f}"
        if abs_v < 20:
            return f"{value:.1f}"
        return f"{value:.0f}"
    

    def smart_format_mass(self, value: float) -> str:
        """Format pour pesées — précision adaptée aux balances (mg pour <1 g)."""
        if value is None:
            return ""
        try:
            v = float(value)
        except (TypeError, ValueError):
            return ""

        abs_v = abs(v)

        # < 0.01 g  -> afficher 4 décimales (0.0001 g)
        if abs_v < 0.01:
            return f"{v:.4f}"
        # 0.01 g - 1 g -> afficher au milligramme (3 décimales)
        if abs_v < 1:
            return f"{v:.3f}"
        # 1 g - 20 g -> centigramme (3 décimales)
        if abs_v < 20:
            return f"{v:.3f}"
        # 20 g - 200 g -> décigramme (2 décimale)
        if abs_v < 200:
            return f"{v:.2f}"
        # >= 200 g -> entier
        return f"{round(v):.0f}"

    def apply_lineedit_style(self, widgets):
        """Uniformise hauteur et police des QLineEdit."""
        for w in widgets:
            w.setFixedHeight(28)
            w.setFont(QFont("Calibri", 12))

    # ------------------- SECTION ACIDE -------------------
    def create_section_acide(self):
        group = QGroupBox("Dilution à partir d'un acide")
        group.setFont(QFont("Calibri", 12))
        layout = QGridLayout()

        # Choix de l’acide
        self.combo_acide = QComboBox()
        self.combo_acide.addItems(self.acides.keys())
        self.combo_acide.currentTextChanged.connect(self.prefill_acide)
        layout.addWidget(QLabel("Acide :"), 0, 0)
        layout.addWidget(self.combo_acide, 0, 1)

        # Densité
        self.saisie_densite = QLineEdit()
        regex = QRegularExpression(r'^\d+([,.]\d{0,3})?$')
        self.saisie_densite.setValidator(QRegularExpressionValidator(regex))
        self.saisie_densite.textChanged.connect(self.normalize_decimal)
        layout.addWidget(QLabel("Densité :"), 1, 0)
        layout.addWidget(self.saisie_densite, 1, 1)

        # Pureté
        self.saisie_purete = QLineEdit()
        regex_purete = QRegularExpression(r'^\d+([,.]\d{0,2})?$')
        self.saisie_purete.setValidator(QRegularExpressionValidator(regex_purete))
        self.saisie_purete.textChanged.connect(self.normalize_decimal)
        layout.addWidget(QLabel("Pureté (%) :"), 2, 0)
        layout.addWidget(self.saisie_purete, 2, 1)

        # Volume final
        self.saisie_volume = QLineEdit()
        # Autorise point ou virgule
        regex_vol = QRegularExpression(r'^\d*([.,]\d{0,4})?$')
        self.saisie_volume.setValidator(QRegularExpressionValidator(regex_vol))
        self.saisie_volume.textChanged.connect(self.normalize_decimal)
        layout.addWidget(QLabel("Volume final (mL) :"), 3, 0)
        layout.addWidget(self.saisie_volume, 3, 1)

        # Concentration finale — accepte . et ,
        self.saisie_concentration = QLineEdit()
        regex_conc = QRegularExpression(r'^\d+([.,]\d{0,6})?$')
        self.saisie_concentration.setValidator(QRegularExpressionValidator(regex_conc))
        self.saisie_concentration.textChanged.connect(self.normalize_decimal)
        layout.addWidget(QLabel("Concentration finale (mol/L) :"), 4, 0)
        layout.addWidget(self.saisie_concentration, 4, 1)

        # Résultats
        self.result_c_acide = QLineEdit()
        self.result_c_acide.setReadOnly(True)
        self.result_c_acide.setStyleSheet("background-color: #E0F7FA; color: red; font-weight: bold;")
        layout.addWidget(QLabel("Concentration acide (mol/L) :"), 5, 0)
        layout.addWidget(self.result_c_acide, 5, 1)

        self.result_v_prelever = QLineEdit()
        self.result_v_prelever.setReadOnly(True)
        self.result_v_prelever.setStyleSheet("background-color: #E0F7FA; color: red; font-weight: bold;")
        layout.addWidget(QLabel("Volume à prélever (mL) :"), 6, 0)
        layout.addWidget(self.result_v_prelever, 6, 1)

        # Bouton Calculer
        btn_calcul = QPushButton("Calculer")
        self.style_bouton(btn_calcul)
        btn_calcul.clicked.connect(self.calcul_acide)
        layout.addWidget(btn_calcul, 7, 0, 1, 2)

        group.setLayout(layout)
        self.prefill_acide()
        self.apply_lineedit_style([
            self.saisie_densite, self.saisie_purete,
            self.saisie_volume, self.saisie_concentration,
            self.result_c_acide, self.result_v_prelever
        ])
        return group

    def prefill_acide(self):
        choix = self.combo_acide.currentText()
        info = self.acides[choix]
        self.saisie_densite.setText(str(info["densite"]))
        self.saisie_purete.setText(str(info["purete"]))

    def calcul_acide(self):
        try:
            choix = self.combo_acide.currentText()
            M = self.acides[choix]["M"]
            densite = float(self.saisie_densite.text())
            purete = float(self.saisie_purete.text())
            v2_ml = float(self.saisie_volume.text())
            c2 = float(self.saisie_concentration.text())
        except ValueError:
            self.error_message("Champs incomplets ou invalides.")
            return

        # Calcul exact (sans arrondir pour le calcul)
        c1 = (densite * 1000 / M) * (purete / 100)

        # Affichage intelligent (arrondi uniquement pour l'affichage)
        self.result_c_acide.setText(self.smart_format(c1))

        # Calcul exact V1
        v1_L = (c2 * (v2_ml / 1000)) / c1
        # Affichage intelligent
        self.result_v_prelever.setText(self.smart_format(v1_L * 1000))

    # ------------------- SECTION POUDRE -------------------
    def create_section_poudre(self):
        group = QGroupBox("Dilution à partir d'une poudre")
        group.setFont(QFont("Calibri", 12))
        layout = QGridLayout()

        self.check_mgL = QCheckBox("Utiliser mg/L (soluté)")
        self.check_mgL.stateChanged.connect(self.toggle_unite_concentration)
        layout.addWidget(self.check_mgL, 0, 0, 1, 2)

        # Concentration cible
        self.saisie_concentration_p = QLineEdit()
        self.saisie_concentration_p.textChanged.connect(self.normalize_decimal)
        layout.addWidget(QLabel("Concentration cible :"), 1, 0)
        layout.addWidget(self.saisie_concentration_p, 1, 1)
        self.label_unite_concentration = QLabel("mol/L")
        self.label_unite_concentration.setFont(QFont("Calibri", 10))
        layout.addWidget(self.label_unite_concentration, 2, 1)

        # Volume
        self.saisie_volume_p = QLineEdit()
        # Autorise point ou virgule
        regex_vol = QRegularExpression(r'^\d*([.,]\d{0,4})?$')
        self.saisie_volume_p.setValidator(QRegularExpressionValidator(regex_vol))
        self.saisie_volume_p.textChanged.connect(self.normalize_decimal)
        layout.addWidget(QLabel("Volume (mL) :"), 3, 0)
        layout.addWidget(self.saisie_volume_p, 3, 1)

        # Masse molaire poudre
        self.saisie_M_poudre = QLineEdit()
        self.saisie_M_poudre.textChanged.connect(self.normalize_decimal)
        layout.addWidget(QLabel("Masse molaire poudre (g/mol) :"), 4, 0)
        layout.addWidget(self.saisie_M_poudre, 4, 1)

        # Masse molaire soluté
        self.saisie_M_solute = QLineEdit("1")
        self.saisie_M_solute.textChanged.connect(self.normalize_decimal)
        layout.addWidget(QLabel("Masse molaire soluté (g/mol) :"), 5, 0)
        layout.addWidget(self.saisie_M_solute, 5, 1)

        # Résultat
        self.result_masse = QLineEdit()
        self.result_masse.setReadOnly(True)
        self.result_masse.setStyleSheet("background-color: #E0F7FA; color: red; font-weight: bold;")
        layout.addWidget(QLabel("Masse à peser (g) :"), 6, 0)
        layout.addWidget(self.result_masse, 6, 1)

        # Bouton Calculer
        btn_calcul = QPushButton("Calculer")
        self.style_bouton(btn_calcul)
        btn_calcul.clicked.connect(self.calcul_poudre)
        layout.addWidget(btn_calcul, 7, 0, 1, 2)

        group.setLayout(layout)
        self.apply_lineedit_style([
            self.saisie_concentration_p, self.saisie_volume_p,
            self.saisie_M_poudre, self.saisie_M_solute, self.result_masse
        ])
        self.toggle_unite_concentration()
        return group

    def calcul_poudre(self):
        try:
            c = float(self.saisie_concentration_p.text())
            v_L = float(self.saisie_volume_p.text()) / 1000
            M_p = float(self.saisie_M_poudre.text())
            M_s = float(self.saisie_M_solute.text())
        except ValueError:
            self.error_message("Champs incomplets ou invalides.")
            return

        if self.check_mgL.isChecked():
            masse = (c / 1000) * v_L * (M_p / M_s)
        else:
            masse = c * v_L * M_p

        # affichage adapté pour pesée
        self.result_masse.setText(self.smart_format_mass(masse))

    def toggle_unite_concentration(self):
        if self.check_mgL.isChecked():
            self.label_unite_concentration.setText("mg/L")
            self.saisie_M_solute.setEnabled(True)
        else:
            self.label_unite_concentration.setText("mol/L")
            self.saisie_M_solute.setEnabled(False)
            self.saisie_M_solute.setText("1")

    # ------------------- SECTION C1V1 -------------------
    def create_section_c1v1(self):
        group = QGroupBox("Dilution simple : C1 V1 = C2 V2")
        group.setFont(QFont("Calibri", 12))
        layout = QGridLayout()

        self.c1 = QLineEdit()
        self.c1.textChanged.connect(self.normalize_decimal)
        layout.addWidget(QLabel("C1 :"), 0, 0)
        layout.addWidget(self.c1, 0, 1)

        self.v1 = QLineEdit()
        self.v1.textChanged.connect(self.normalize_decimal)
        layout.addWidget(QLabel("V1 :"), 1, 0)
        layout.addWidget(self.v1, 1, 1)

        self.c2 = QLineEdit()
        self.c2.textChanged.connect(self.normalize_decimal)
        layout.addWidget(QLabel("C2 :"), 2, 0)
        layout.addWidget(self.c2, 2, 1)

        self.v2 = QLineEdit()
        self.v2.textChanged.connect(self.normalize_decimal)
        layout.addWidget(QLabel("V2 :"), 3, 0)
        layout.addWidget(self.v2, 3, 1)

        btn_calcul = QPushButton("Calculer")
        self.style_bouton(btn_calcul)
        btn_calcul.clicked.connect(self.calc_c1v1_dynamic)
        layout.addWidget(btn_calcul, 4, 0, 1, 2)

        group.setLayout(layout)
        self.apply_lineedit_style([self.c1, self.v1, self.c2, self.v2])
        return group

    def calc_c1v1_dynamic(self):
        champs = {"C1": self.c1, "V1": self.v1, "C2": self.c2, "V2": self.v2}
        vide = [k for k, w in champs.items() if w.text().strip() == ""]
        if len(vide) != 1:
            self.error_message("Veuillez laisser exactement un champ vide pour le calcul.")
            return

        try:
            C1 = float(self.c1.text()) if self.c1.text() else None
            V1 = float(self.v1.text()) if self.v1.text() else None
            C2 = float(self.c2.text()) if self.c2.text() else None
            V2 = float(self.v2.text()) if self.v2.text() else None
        except ValueError:
            self.error_message("Certains champs contiennent des valeurs invalides.")
            return

        champ = vide[0]
        try:
            if champ == "C1":
                self.c1.setText(self.smart_format((C2 * V2) / V1))
            elif champ == "V1":
                self.v1.setText(self.smart_format((C2 * V2) / C1))
            elif champ == "C2":
                self.c2.setText(self.smart_format((C1 * V1) / V2))
            elif champ == "V2":
                self.v2.setText(self.smart_format((C1 * V1) / C2))
        except ZeroDivisionError:
            self.error_message("Impossible de diviser par zéro.")
            return

        champs[champ].setStyleSheet(
            "background-color: #DFF0D8; font-weight: bold; color: darkgreen;"
        )

    # ------------------- RESET -------------------
    def reset_fields(self):
        for widget in self.findChildren(QLineEdit):
            widget.clear()
        self.saisie_M_solute.setText("1")
        self.prefill_acide()
        self.toggle_unite_concentration()


# ------------------- MAIN -------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = DilutionApp()
    win.show()
    sys.exit(app.exec())

# V1.1, J.MANIA, le 12/12/2025
