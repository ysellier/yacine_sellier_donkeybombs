import numpy as np
from agents.kart_agent import KartAgent

class Agent1HalfTurn(KartAgent):
    """
    Agent 'HalfTurn'
    Ce wrapper permet de faire un demi-tour
    """
    def __init__(self, env, pilot, conf):
        """
        Initialise le module de sauvetage

        Args:
            env (obj): L'environnement de simulation
            conf (OmegaConf): Configuration contenant les seuils de blocage et durée de recul
        """
        self.pilot = pilot
        super().__init__(env)
        self.conf = conf
        self.origin = -1

    def choose_action(self, obs):
        """
        Effectue le demi-tour

        Args:
            obs (dict): Observations courantes

        Returns:
            dict: Action marche arrière, sinon appel de MidPilot
        """
        if self.origin == -1 : #Connaître la direction pour laquelle le kart pointe au début de la course
            self.origin = obs["front"][2] 
        
        if obs["front"][2] != -self.origin : #Effectuer la marche arrière jusqu'à qu'on pointe vers la direction opposée que le début de la course
            return {
                "acceleration": 0,
                "steer": 0.25,
                "brake": True,
                "drift": False, "nitro": False, "rescue": False, "fire": False
            }

        return self.pilot.choose_action(obs)