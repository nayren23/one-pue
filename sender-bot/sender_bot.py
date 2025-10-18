###########################################
#                                         #
#           Sender Bot Class              #
#                                         #
###########################################

# ---------------- Imports --------------- #
import pyModbusTCP
import time
import struct
from pyModbusTCP.server import ModbusServer, DataHandler
from CONSTANTS import *

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
        self.modbus_server = None
        self.modbus_handler = None


    def __str__(self):
        return (
            f"SenderBot('{self.name}')\n"
            f"  Host: {self.host}:{self.port}\n"
            f"  Unit ID: {self.unit_id}\n"
            f"  Uptime: {self.get_uptime()}s\n"
            f"  Data registers: {len(self.data_registers)}"
        )

    def float_to_modbus_registers(self, float_value) -> DataHandler.Return:
        """Convertit un float 32-bit en deux mots (registres Modbus) - Big Endian"""
        # 'f': float 32 bits, '>': Big-Endian
        four_bytes = struct.pack('>f', float_value)
        # Décomposer les 4 octets en 2 entiers de 16 bits
        reg1, reg2 = struct.unpack('>HH', four_bytes)
        print(reg1, reg2)
        print(bin(reg1), bin(reg2))
        return DataHandler.Return(0, [reg1, reg2])
    
    def u32_to_modbus_registers(self, u32_value) -> DataHandler.Return:
        """Convertit un entier non signé 32-bit en deux mots (registres Modbus) - Big Endian"""
        # Pack the 32-bit int as 4 bytes (big-endian)
        packed = struct.pack('>I', u32_value)

        # Unpack those bytes into two 16-bit big-endian words
        reg_high, reg_low = struct.unpack('>HH', packed)
        return DataHandler.Return(0, [reg_high, reg_low])
    
    def u16_to_modbus_registers(self, u16_value) -> DataHandler.Return:
        """Convertit un entier non signé 16-bit en deux mots (registres Modbus) - Big Endian"""

        assert 0 <= u16_value <= 0xFFFF, "La valeur doit être un entier non signé de 16 bits."
        return DataHandler.Return(0, [u16_value])

    def update_registers(self, address, value, value_type='u32'):
        # value_type peut être 'u32', 'u16' ou 'f32' (float)
        self.data_registers[address] = [value, value_type]

    def get_registers(self, address: int):
        """Récupère les registres demandés par le Maître Modbus."""
        
        if address in self.data_registers:
            value, val_size = self.data_registers[address]
            print(f"Getting registers for address {address}: value={value}, type={val_size}")
            if val_size == 'f32':
                return self.float_to_modbus_registers(value)
            elif val_size == 'u16':
                return self.u16_to_modbus_registers(value)
            elif val_size == 'u32':
                return self.u32_to_modbus_registers(value)
            else:
                raise ValueError(f"Type de valeur inconnu: {val_size}")
        
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

    def read_h_regs(self, address: int, count: int, unit_id: ModbusServer.ServerInfo):
        """
        Intercepte la requête de lecture des registres de maintien (Fonction 0x03).
        """

        print(address, self.simulator.data_registers)
        try:
            registers = self.simulator.get_registers(address)

            return registers
        except ValueError as e:
            print(f"Erreur interne lors de la lecture: {e}")
            return super().read_h_regs(address, count, unit_id)