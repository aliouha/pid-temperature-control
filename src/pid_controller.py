class PIDController:
    """
    Régulateur PID discret.
    
    Formule :
    u[k] = Kp * e[k] + Ki * Te * sum(e) + Kd/Te * (e[k] - e[k-1])
    """

    def __init__(self, Kp=0.5, Ki=0.01, Kd=0.1, Te=1.0):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.Te = Te

        # Variables internes
        self.integral   = 0.0
        self.prev_error = 0.0
        self.output     = 0.0

    def reset(self):
        """Remet le PID à zéro."""
        self.integral   = 0.0
        self.prev_error = 0.0
        self.output     = 0.0

    def compute(self, setpoint, mesure):
        """
        Calcule la commande u à partir de la consigne et de la mesure.
        
        setpoint : température désirée (°C)
        mesure   : température actuelle (°C)
        """
        # Calcul de l'erreur
        error = setpoint - mesure

        # Terme Proportionnel
        P = self.Kp * error

        # Terme Intégral (avec anti-windup : saturation entre 0 et 1)
        self.integral += error * self.Te
        I = self.Ki * self.integral

        # Terme Dérivé
        D = self.Kd * (error - self.prev_error) / self.Te
        self.prev_error = error

        # Commande totale saturée entre 0 et 1 (0% à 100% du brûleur)
        self.output = P + I + D
        self.output = max(0.0, min(1.0, self.output))

        return self.output, P, I, D