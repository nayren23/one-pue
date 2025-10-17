###########################################
#                                         #
#                  Main                   #
#                                         #
###########################################

# ---------------- Imports --------------- #
from sender_bot import SenderBot, CustomDataHandler, REGISTRE_ENERGIE, REGISTRE_ENERGIE_FRAC
import pyModbusTCP
import random
import time
import struct
from pyModbusTCP.server import ModbusServer, DataHandler
from typing import Dict, Any, List

# ----------- Constants ------------------ #
MODBUS_HOST = "10.123.173.118"
MODBUS_PORT = 5555
MODBUS_UNIT_ID = 1
POWER_AVERAGE = 450
POWER_BASE_VALUE = 1.5


if __name__ == "__main__":
    
    # créer une instance de SenderBot
    DirisA40 = SenderBot(name="Diris A40", host=MODBUS_HOST, port=MODBUS_PORT, unit_id=MODBUS_UNIT_ID)
    DirisA40.update_registers(address=REGISTRE_ENERGIE, value=int(str(POWER_BASE_VALUE).split('.')[0]), value_type='u32')
    DirisA40.update_registers(address=REGISTRE_ENERGIE_FRAC, value=int(str(POWER_BASE_VALUE).split('.')[-1]), value_type='u16')
    print(DirisA40)

    # Création du gestionnaire de données
    handler = CustomDataHandler(DirisA40)
    
    # Démarrage du serveur Modbus
    server = ModbusServer(
        host=MODBUS_HOST, 
        port=MODBUS_PORT, 
        no_block=True,
        data_hdl=handler 
    )

    
    print(f"📡 Démarrage du Serveur Modbus TCP sur {MODBUS_HOST}:{MODBUS_PORT}")
    print(f"Capteur simulé : {DirisA40.name} (UNIT_ID: {DirisA40.unit_id})")
    print(f"Registre 1000 initialisé avec: {POWER_BASE_VALUE} kWh")
    server.start()
    print("Serveur en cours d'exécution. En attente de requêtes du Maître...")

    # Boucle principale pour maintenir le serveur en vie
    while True:
        time.sleep(1)
        self.simulator.data_registers[REGISTRE_ENERGIE][0] += int(POWER_AVERAGE / 3600)
