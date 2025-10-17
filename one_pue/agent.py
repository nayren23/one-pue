"""Agent Mother Class"""

from abc import ABC, abstractmethod


class Agent(ABC):
    """Classe mère représentant un agent générique (capteur, sonde, etc.)."""

    interval: float
    name: str
    agent_type: str
    metric_type: str
    date: str

    def __init__(
        self,
        interval,
        name,
        agent_type,
        metric_type,
    ):
        """
        Constructeur de la classe Agent.

        Paramètres :
        - interval : intervalle de mesure ou de mise à jour
        - name : nom de l'agent
        - agent_type : type d'agent (ex : capteur, actionneur)
        - metric_type : Type de la métrique de mesure (ex : Puissance)
        """

        self.interval = interval  # Intervalle de mesure/mise à jour
        self.name = name  # Nom de l'agent
        self.agent_type = agent_type  # Type d’agent
        self.metric_type = metric_type  # Type de la métrique (Puissance)

    @abstractmethod
    def get_data(self):
        """Méthode abstraite : Récupération des informations des sondes ou capteurs"""
