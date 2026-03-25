import numpy as np
import random
from utils.track_utils import compute_curvature, compute_slope
from agents.kart_agent import KartAgent
from .agent1_MidPilot import Agent1Mid
from .agent1_HalfTurn import Agent1HalfTurn
from omegaconf import OmegaConf 
import os

class Agent1(KartAgent):
    """
    Agent principal 'Donkey Bombs' (Team 5).
    Cette classe agit comme un orchestrateur (Wrapper global) qui assemble les différents 
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
        self.pilot = Agent1Mid(env, self.conf, path_lookahead)

        self.rescue = Agent1HalfTurn(env, self.pilot, self.conf)

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

    def choose_action(self, obs):
        """
        Méthode d'entrée principale du simulateur. 
        Elle appelle soit le wrapper qui permet d'avancer, soit le wrapper qui permet de reculer.

        Args:
            obs (dict): Dictionnaire contenant les observations de l'environnement (vitesse, position, etc.).

        Returns:
            dict: Dictionnaire d'actions (steer, acceleration, brake, drift, nitro, etc.).
        """

        return self.rescue.choose_action(obs) #On effectue le demi-tour, et une fois effectué, c'est ce wrapper qui appelera notre agentMid

