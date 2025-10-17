###########################################
#                                         #
#                  Main                   #
#                                         #
###########################################

# ---------------- Imports --------------- #
from sender_bot import SenderBot, CustomDataHandler
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

# -----------  Functions ----------------- #



# --------------- Main Logic -------------- #

if __name__ == "__main__":
    
    # créer une instance de SenderBot
    DirisA40 = SenderBot(name="Diris A40", host=MODBUS_HOST, port=MODBUS_PORT, unit_id=MODBUS_UNIT_ID)
    DirisA40.update_registers(address=1000, value=POWER_BASE_VALUE)  # Energy value at address 1000
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