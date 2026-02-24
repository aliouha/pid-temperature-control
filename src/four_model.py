import numpy as np


class FourIndustriel:
    """
    Modèle physique d'un four industriel.
    Système du 1er ordre non-linéaire avec pertes thermiques.

    Equation différentielle :
    dT/dt = (1/tau) * (K * u - (T - T_ambiante)) + perturbation
    """

    def __init__(self):
        # Paramètres physiques du four
        self.K = 200.0  # Gain statique (°C / unité de commande)
        self.tau = 120.0  # Constante de temps (secondes)
        self.T_amb = 25.0  # Température ambiante (°C)
        self.T = 25.0  # Température initiale (°C)
        self.Te = 1.0  # Période d'échantillonnage (seconde)

    def reset(self):
        """Remet le four à la température ambiante."""
        self.T = self.T_amb

    def step(self, u, perturbation=0.0):
        """
        Calcule la température au prochain pas de temps.

        u            : commande (0 à 1 — ouverture du brûleur)
        perturbation : bruit ou choc thermique externe (°C)
        """
        # Équation différentielle discrétisée (méthode d'Euler)
        dT = (1 / self.tau) * (self.K * u - (self.T - self.T_amb))
        self.T += dT * self.Te + perturbation
        self.T = max(
            self.T_amb, self.T
        )  # La température ne peut pas descendre sous T_ambiante
        return self.T
