import numpy as np
import random
from utils.track_utils import compute_curvature, compute_slope
from agents.kart_agent import KartAgent
from .agent7_MidPilot import Agent7Mid
from .agent7_RescuePilot import Agent7Rescue
from omegaconf import OmegaConf 
import os

class Agent7(KartAgent):
    """
    Agent principal 'Donkey Bombs' (Team 5).
    Cette classe agit comme un orchestrateur (Wrapper global) qui assemble les différents 
    modules de pilotage (Mid, Nitro, Drift, Banana, Item) selon une hiérarchie de priorité.
    """
    def __init__(self, env, path_lookahead=3, cfg=None):
        """
        Initialise l'agent complet en chargeant la configuration YAML et en 
        emboîtant les différents pilotes les uns dans les autres.

        Args:
            env (obj): L'environnement de simulation SuperTuxKart.
            path_lookahead (int): Nombre de points de cheminement à anticiper (défaut: 3).
        """
        super().__init__(env)
        self.path_lookahead = path_lookahead
        self.name = "YacineSELLIER"
        self.isEnd = False

        # On trouve le chemin de notre fichier actuel
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # On créer le chemin /src/agent/team7/config.yaml
        config_path = os.path.join(current_dir, "config.yaml")

        # On charge le fichier conf avec ce chemin
        self.conf = OmegaConf.load(config_path)
        if cfg is not None:
            self.conf = cfg
        
        # On crée le Pilote qui suit la piste 
        self.pilot = Agent7Mid(env, self.conf, path_lookahead)

        self.rescue = Agent7Rescue(env, self.conf, path_lookahead)

    def endOfTrack(self):
        """
        Indique si le kart a atteint la fin de la piste.

        Returns:
            bool: True si la fin de la piste est atteinte, False sinon.
        """
        return self.isEnd

    def reset(self):
        """Réinitialise la chaîne complète des pilotes (Brain et couches inférieures)."""
        self.brain.reset()  

    def choose_action(self, obs, step):
        """
        Méthode d'entrée principale du simulateur. 
        Elle appelle soit le wrapper qui permet d'avancer, soit le wrapper qui permet de reculer.

        Args:
            obs (dict): Dictionnaire contenant les observations de l'environnement (vitesse, position, etc.).

        Returns:
            dict: Dictionnaire d'actions (steer, acceleration, brake, drift, nitro, etc.).
        """

        if step < 200 : 
            return self.pilot.choose_action(obs) #On avance dans les 200 premiers pas de temps
        else :
            return self.rescue.choose_action(obs) #On recule dans les 200 suivants
