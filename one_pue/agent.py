"""Agent Mother Class"""

from pyModbusTCP.client import ModbusClient


class Agent:
    """Classe mère représentant un agent générique (capteur, sonde, etc.)."""

    modbus_client: ModbusClient
    modbus_host: str

    name: str
    metric_type: str
    date: str

    def __init__(
        self,
        name,
        metric_type,
    ):
        """
        Constructeur de la classe Agent.

        Paramètres :
        - name : nom de l'agent
        - metric_type : Type de la métrique de mesure (ex : Puissance)
        """

        self.name = name  # Nom de l'agent
        self.metric_type = metric_type  # Type de la métrique (Puissance)

    def init_modbus_connection(self, modbus_port):
        """TCP auto connect on first modbus request"""
        return ModbusClient(host=self.modbus_host, port=modbus_port, unit_id=1, auto_open=True)
