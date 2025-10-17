"""Agent pour récupérer les données météo"""

# weather_agent.py
from datetime import datetime
import requests
from one_pue.agent import Agent
from one_pue.agent_dto import AgentDTO


class WeatherAgent(Agent):
    """Classe fille pour récupérer la météo (température horaire)."""

    # Ajouter constructeur pour set tout sauf value
    def __init__(self, interval, name, agent_type, metric_type):
        """
        interval : intervalle de mise à jour (s ou min)
        name     : nom de l'agent (ex: 'Station Berlin')
        type     : type d'agent (ex: 'Weather Agent')
        metric_type     : metric_type (ex: 'Puissance')
        date     : date associée (string 'YYYY-MM-DD' ou ISO)
        latitude/longitude : position utilisée pour l'appel API
        """
        super().__init__(interval, name, agent_type, metric_type)

        self.latitude = 52.52
        self.longitude = 13.41

    def get_data(self):
        """
        Récupère la température horaire via Open-Meteo et retourne un AgentDTO.
        Si l'API échoue, value sera None et time/date resteront ceux de l'instance.
        """
        url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={self.latitude}&longitude={self.longitude}"
            "&hourly=temperature_2m"
        )

        value = None

        try:
            resp = requests.get(url, timeout=5)
            resp.raise_for_status()
            payload = resp.json()

            hourly = payload.get("hourly", {})
            times = hourly.get("time", [])
            temps = hourly.get("temperature_2m", [])

            if times and temps and len(times) == len(temps):
                # On prend la valeur correspondant à l'heure courante ou la prochaine disponible
                # (simple fallback : premier créneau futur sinon dernier connu)
                now_iso_hour = datetime.utcnow().replace(minute=0, second=0, microsecond=0).isoformat()

                pick_idx = None
                for i, t in enumerate(times):
                    if t >= now_iso_hour:
                        pick_idx = i
                        break
                if pick_idx is None:
                    pick_idx = len(times) - 1

                value = temps[pick_idx]

        except Exception:
            # En cas d'erreur réseau/API, on renverra value=None
            pass

        return value


# iggromérie, temp ensoleliement , durée ensolielment
