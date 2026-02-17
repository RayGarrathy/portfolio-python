# BalancePrint - Automatisation de la récupération de pesées via RS232

Ce projet modernise un ancien système de pesée basé sur une balance de laboratoire connectée à une imprimante à rouleau.
L’objectif : intercepter la donnée RS232, déclenchée par l’imprimante, et l’envoyer automatiquement dans Excel via un script Python.

## 🎯 Objectifs du projet
Comprendre et exploiter un protocole série ancien (DIN 9 broches + RS232)

Intercepter un flux de données initialement destiné à une imprimante

Automatiser la récupération de pesées dans Excel

Moderniser un équipement sans modifier son fonctionnement utilisateur

## ⚙️ Fonctionnement du système

1) Configuration d’origine
La balance est reliée à une imprimante à rouleau.
L’imprimante possède un bouton PRINT.
Lorsqu’on appuie sur PRINT :
L’imprimante envoie un signal électrique via un câble DIN 9 broches vers la balance.
La balance envoie la donnée de pesée via RS232 vers l’imprimante.
L’imprimante imprime la valeur sur le rouleau.

2) Nouvelle architecture
Le câble DIN reste entre l’imprimante et la balance.
Le câble RS232 est désormais connecté à un PC.
Le PC intercepte la donnée envoyée par la balance.

3) Nouveau fonctionnement
L’utilisateur appuie toujours sur PRINT.
L’imprimante envoie le signal DIN à la balance.
La balance envoie la donnée via RS232.
Le script Python lit la donnée et l’envoie automatiquement dans Excel.

## Schéma ASCII – Flux de fonctionnement

                   ┌──────────────────────────┐
                   │   Imprimante à rouleau   │
                   │        (bouton PRINT)    │
                   └──────────────┬───────────┘
                                  │
                                  │ 1) Signal d'appel
                                  │    (câble DIN 9 broches)
                                  ▼
                         ┌────────────────┐
                         │    Balance     │
                         │  de laboratoire│
                         └───────┬────────┘
                                 │
                                 │ 2) Donnée de pesée (RS232)
                                 │
                 ┌───────────────┴────────────────┐
                 │                                │
                 │ Configuration d'origine         │
                 │                                │
                 ▼                                ▼
        ┌──────────────────┐             ┌──────────────────┐
        │  Imprimante      │             │        PC         │
        │ (réception RS232 │             │ (interception     │
        │   + impression)  │             │     RS232)        │
        └──────────────────┘             └─────────┬────────┘
                                                    │
                                                    │ 3) Traitement Python
                                                    ▼
                                           ┌──────────────────┐
                                           │      Python       │
                                           │ (lecture + envoi  │
                                           │     vers Excel)   │
                                           └─────────┬────────┘
                                                     │
                                                     │ 4) Export automatique
                                                     ▼
                                           ┌──────────────────┐
                                           │      Excel        │
                                           │ (mise à jour du   │
                                           │   fichier .xlsx)  │
                                           └──────────────────┘

## 📸 Captures d’écran
