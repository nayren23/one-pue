###########################################
#                                         #
#           Sender Bot Class              #
#                                         #
###########################################

# ---------------- Imports --------------- #
import pyModbusTCP
import random
import time
import struct
from pyModbusTCP.server import ModbusServer, DataHandler
from typing import Dict, Any, List

# ----------- Constants ------------------ #
MODBUS_HOST = "172.18.146.98"
MODBUS_PORT = 502
MODBUS_UNIT_ID = 1
POWER_AVERAGE = 450
POWER_BASE_VALUE = POWER_AVERAGE * 24 * 365
REGISTRE_ENERGIE = 1000

# ---------- Sender Bot Class ------------ #

class SenderBot:
    
    """
    Classe de base pour gérer les données et la conversion Modbus.
    """

    def __init__(self, name: str,  host: str, port: int, unit_id: int):
        self.name = name
        self.host = host
        self.port = port
        self.unit_id = unit_id
        self.inital_tick = time.time()
        self.data_registers = {}


    def __str__(self):
        return (
            f"SenderBot('{self.name}')\n"
            f"  Host: {self.host}:{self.port}\n"
            f"  Unit ID: {self.unit_id}\n"
            f"  Uptime: {self.get_uptime()}s\n"
            f"  Data registers: {len(self.data_registers)}"
        )

    def float_to_modbus_registers(float_value):
        """Convertit un float 32-bit en deux mots (registres Modbus) - Big Endian"""
        # 'f': float 32 bits, '>': Big-Endian
        four_bytes = struct.pack('>f', float_value)
        # Décomposer les 4 octets en 2 entiers de 16 bits
        reg1 = struct.unpack('>H', four_bytes[0:2])[0]
        reg2 = struct.unpack('>H', four_bytes[2:4])[0]
        return [reg1, reg2]

    def update_registers(self, address, value):
        """Met à jour les registres avec de nouvelles valeurs."""
        self.data_registers[address] = value

    def get_registers(self, address, length):
        """Récupère les registres demandés par le Maître Modbus."""
        
        # Gérer le cas des floats 32-bit (2 registres)
        if address in self.data_registers and length == 2:
            float_value = self.data_registers[address]
            return self.float_to_modbus_registers(float_value)
        
        # Gérer le cas où l'adresse n'est pas connue
        raise ValueError(f"Adresse {address} non reconnue ou nombre de registres incorrect.")
    
    def get_uptime(self):
        """Retourne le temps de fonctionnement en secondes."""
        return int(time.time() - self.inital_tick)
    


# --- Gestionnaire de Données Personnalisé ---
class CustomDataHandler(DataHandler):
    """
    Gère les requêtes Modbus en utilisant l'instance DirisA40.
    """
    def __init__(self, simulator: SenderBot):
        super().__init__()
        self.simulator = simulator

    def read_holding_registers(self, address: int, count: int, unit_id: int) -> List[int]:
        """
        Intercepte la requête de lecture des registres de maintien (Fonction 0x03).
        """
        
        # 1. Vérifie l'UNIT_ID
        if unit_id != self.simulator.unit_id:
            print(f"Erreur: UNIT_ID {unit_id} incorrecte (attendu {self.simulator.unit_id})")
            return super().read_holding_registers(address, count, unit_id)

        # 2. Vérifie si l'adresse est celle que nous gérons (1000)
        if address == REGISTRE_ENERGIE:
            try:
                # Récupère les registres de l'instance SenderBot
                registers = self.simulator.get_registers(address, count)
                
                # Optionnel: Simulation de l'incrémentation de l'énergie pour le prochain tick
                # Ceci simule le temps qui passe
                self.simulator.data_registers[REGISTRE_ENERGIE] += (POWER_AVERAGE / 3600) # + Power par seconde
                
                print(f"[{time.strftime('%H:%M:%S')}] Lecture OK de l'UNIT_ID {unit_id}, Reg {address}. Valeur float envoyée: {self.simulator.data_registers[REGISTRE_ENERGIE]:.2f} kWh")
                return registers
            
            except ValueError as e:
                print(f"Erreur interne lors de la lecture: {e}")
                return super().read_holding_registers(address, count, unit_id)

        # 3. Pour toute autre adresse, retourne l'erreur par défaut
        return super().read_holding_registers(address, count, unit_id)