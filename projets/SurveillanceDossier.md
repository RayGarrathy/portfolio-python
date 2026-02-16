# 👀📁 SurveillanceDossier

SurveillanceDossier est un agent Windows léger développé en Python.  
Il surveille en temps réel un dossier réseau et affiche une notification toast lorsqu’un nouveau fichier est créé.  
L’application tourne discrètement dans la zone de notification (systray) et peut être compilée en `.exe` pour un usage simple et transparent.

---

## ✨ Fonctionnalités principales

- Surveillance en temps réel d’un dossier réseau (UNC)
- Détection instantanée des nouveaux fichiers
- Notifications toast Windows avec icône personnalisée
- Icône dans la zone de notification (systray)
- Menu contextuel (Quitter)
- Fonctionnement silencieux en arrière‑plan
- Compatible avec un lancement automatique au démarrage de Windows
- Version `.exe` autonome via PyInstaller

---

## 🖼️ Capture d’écran
Exemple :

![Mini-notif](../images/Surveillancedossier2.png)
![Menu notification](../images/Surveillancedossier.png)


---
👉 [Voir le code source](py/surveillancedossier.py)


