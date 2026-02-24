# PID Temperature Control — Four Industriel

**Simulation et régulation de température d'un four industriel via un contrôleur PID discret, avec dashboard interactif.**

Projet réalisé dans le cadre d'un Master en Automatique et Informatique Industrielle.

---

## Présentation

Ce projet implémente un système complet de **contrôle de température** pour un four industriel simulé. Il illustre les concepts fondamentaux de l'automatique :

- **Modélisation physique** d'un système thermique du 1er ordre
- **Régulation PID discrète** avec anti-windup
- **Rejet de perturbations** — simulation d'un choc thermique externe
- **Visualisation interactive** via un dashboard Streamlit

L'objectif est de maintenir la température du four à une consigne choisie (50°C à 500°C), malgré les perturbations, en ajustant les gains Kp, Ki, Kd en temps réel.

---

## Démonstration

Le dashboard permet de visualiser en temps réel :

- La **réponse du système** — suivi de consigne et rejet de perturbation
- Le **signal de commande** — ouverture du brûleur (0% à 100%)
- La **décomposition des termes P, I, D** — contribution de chaque action

---

## Modèle Physique

Le four est modélisé comme un système du **1er ordre non-linéaire** avec pertes thermiques :

$$\frac{dT}{dt} = \frac{1}{\tau} \left( K \cdot u - (T - T_{amb}) \right)$$

| Paramètre | Valeur | Description |
|---|---|---|
| K | 200 | Gain statique (°C / unité de commande) |
| τ | 120 s | Constante de temps thermique |
| T_amb | 25 °C | Température ambiante |
| Te | 1 s | Période d'échantillonnage |

---

## Régulateur PID Discret

La commande est calculée à chaque pas de temps selon :

$$u[k] = K_p \cdot \varepsilon[k] + K_i \cdot T_e \cdot \sum\varepsilon + \frac{K_d}{T_e} \cdot (\varepsilon[k] - \varepsilon[k-1])$$

Un **anti-windup** est intégré pour éviter la saturation de l'intégrateur — la commande est bornée entre 0 et 1 (0% à 100% d'ouverture du brûleur).

---

## Stack Technique

| Domaine | Technologie |
|---|---|
| Langage | Python 3.10+ |
| Interface | Streamlit |
| Visualisation | Matplotlib |
| Calcul numérique | NumPy |

---

## Structure du Projet

```
pid-temperature-control/
├── src/
│   ├── four_model.py        # Modèle physique du four (système 1er ordre)
│   ├── pid_controller.py    # Régulateur PID discret avec anti-windup
│   └── __init__.py
├── app.py                   # Dashboard interactif Streamlit
├── requirements.txt         # Dépendances Python
└── README.md
```

---

## Installation et Lancement

### 1. Cloner le dépôt

```bash
git clone https://github.com/aliou-harber/pid-temperature-control.git
cd pid-temperature-control
```

### 2. Créer l'environnement virtuel

**Windows :**
```bash
python -m venv venv
.\venv\Scripts\activate
```

**Linux / macOS :**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Lancer le dashboard

```bash
streamlit run app.py
```

---

## Résultats

Les tests montrent qu'avec un réglage Kp=0.5, Ki=0.05, Kd=0.1 :

- **Erreur statique** inférieure à 0.5°C en régime permanent
- **Rejet de perturbation** — récupération complète après un choc de -50°C
- **Stabilité** maintenue sur toute la plage de consigne (50°C à 500°C)

**Observation :** L'action intégrale est essentielle pour annuler l'erreur statique due à la non-linéarité du modèle. L'action dérivée améliore la rapidité de rejet des perturbations.

---

## Auteur

**Aliou Harber**
Master Automatique et Informatique Industrielle

[LinkedIn](https://linkedin.com/in/aliou-harber) · [GitHub](https://github.com/aliou-harber)

---

*Les contributions sont les bienvenues via Pull Request.*