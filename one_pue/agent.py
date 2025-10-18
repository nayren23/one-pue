"""Agent Mother Class"""

from pyModbusTCP.client import ModbusClient
import struct as s


class Agent:
    """Classe mère représentant un agent générique (capteur, sonde, etc.)."""

    modbus_client: ModbusClient
    modbus_host: str

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

    def init_modbus_connection(self, modbus_port):
        """TCP auto connect on first modbus request"""
        return ModbusClient(host=self.modbus_host, port=modbus_port, unit_id=1, auto_open=True)

    def format_value_modbus(self, first_regs, second_regs):
        """Format de la valeur récupérer via modbus poru la mettre dans le bon format"""
        return s.unpack(">I", s.pack(">HH", *first_regs))[0] + second_regs[0] / 10000
