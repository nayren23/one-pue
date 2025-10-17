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
        self._data_registers[address] = value

    def get_registers(self, address, length):
        """Récupère les registres demandés par le Maître Modbus."""
        
        # Gérer le cas des floats 32-bit (2 registres)
        if address in self._data_registers and length == 2:
            float_value = self._data_registers[address]
            return self.float_to_modbus_registers(float_value)
        
        # Gérer le cas où l'adresse n'est pas connue
        raise ValueError(f"Adresse {address} non reconnue ou nombre de registres incorrect.")
    
    def get_uptime(self):
        """Retourne le temps de fonctionnement en secondes."""
        return int(time.time() - self.inital_tick)