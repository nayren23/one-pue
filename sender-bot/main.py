###########################################
#                                         #
#                  Main                   #
#                                         #
###########################################

# ---------------- Imports --------------- #
from sender_bot import SenderBot, CustomDataHandler
from CONSTANTS import *
import random
import time
from pyModbusTCP.server import ModbusServer, DataHandler
import json

# --------- import JSON ------------ #
FILE_NAME = "conf.json"

try:
    # Lecture du fichier JSON
    with open(FILE_NAME, 'r') as f:
        data = json.load(f)
except FileNotFoundError:
    print(f"❌ Erreur: Le fichier '{FILE_NAME}' est introuvable. Assurez-vous qu'il est dans le même répertoire.")
    exit()
except json.JSONDecodeError as e:
    print(f"❌ Erreur lors du décodage JSON dans '{FILE_NAME}': {e}")
    exit()

# --------------- Functions --------------- #
def update_diris_a40_registers():
    """Met à jour les registres du Diris A40 avec des valeurs simulées."""
    # Simuler une fluctuation de puissance
    fluctuation_hour = POWER_AVERAGE * (1 + random.uniform(-POWER_FLUCTUATION, POWER_FLUCTUATION))

    # Mettre à jour les registres d'énergie
    DirisA40.data_registers[REGISTRE_ENERGIE][0] += int(fluctuation_hour // 1)
    DirisA40.data_registers[REGISTRE_ENERGIE_FRAC][0] = int((fluctuation_hour % 1) * 10000)

def update_pdu_schneider_registers():
    """Met à jour les registres du PDU Schneider avec des valeurs simulées."""
    # Simuler une fluctuation de puissance
    fluctuation_hour = PDU_AVERAGE * (1 + random.uniform(-PDU_FLUCTUATION, PDU_FLUCTUATION))

    # Mettre à jour les registres d'énergie
    PduSchneider.data_registers[REGISTRE_PDU_ENERGIE][0] += int(fluctuation_hour // 1)
    PduSchneider.data_registers[REGISTRE_PDU_ENERGIE_FRAC][0] = int((fluctuation_hour % 1) * 10000)

def update_register(capteur: SenderBot, index: int):
    """Met à jour un registre spécifique pour un capteur donné."""

    average_value = data["capteurs"][index]["simulation_parametres"]["average_value"]
    fluctuation_value = data["capteurs"][index]["simulation_parametres"]["fluctuation"]

    fluctuation = average_value * (1 + random.uniform(-fluctuation_value, fluctuation_value))

    int_part = int(fluctuation // 1)
    frac_part = int((fluctuation % 1) * 10000)
    

    if len(data["capteurs"][index]["registres"]) == 1:
        registre_address = int(data["capteurs"][index]["registres"][0]["adresse"])
        registre_size = data["capteurs"][index]["registres"][0]["taille"]

        print(capteur.data_registers)
        print(registre_address, registre_size)


    elif len(data["capteurs"][index]["registres"]) == 2:

        # recupérer les adresses et tailles des registres
        registre_address_int = data["capteurs"][index]["registres"][0]["adresse"]
        registre_address_frac = data["capteurs"][index]["registres"][1]["adresse"]
        registre_size_int = data["capteurs"][index]["registres"][0]["taille"]
        registre_size_frac = data["capteurs"][index]["registres"][1]["taille"]

        # mettre à jour les registres
        int_part += capteur.data_registers[registre_address_int][0]
        capteur.update_registers(address=registre_address_int, value=int_part, value_type=registre_size_int)
        capteur.update_registers(address=registre_address_frac, value=frac_part, value_type=registre_size_frac)


    return int_part, frac_part

if __name__ == "__main__":

    capteur_list = []

    for capteur in data["capteurs"]:
        capteur_list.append(SenderBot(
            name=capteur["nom"],
            host=data["host"],
            port=capteur["port"],
            unit_id=capteur["unit_id"])
        )
    
    for index, capteur in enumerate(capteur_list):

        # Initialisation des registres à zéro
        for registre in data["capteurs"][index]["registres"]:

           capteur.update_registers(address=registre["adresse"], value=registre["base_value"], value_type=registre["taille"])

        # Création du serveur Modbus TCP
        capteur.modbus_handler = CustomDataHandler(capteur)
        capteur.modbus_server = ModbusServer(
            host=capteur.host,
            port=capteur.port,
            no_block=True,
            data_hdl=capteur.modbus_handler
        )

        # Démarrage du serveur Modbus dans un thread séparé
        capteur.modbus_server.start()
        print(f" Serveur Modbus pour {capteur.name} démarré sur {capteur.host}:{capteur.port} (Unit ID: {capteur.unit_id})")
    
    while True:
        time.sleep(1)

        # Mettre à jour les registres périodiquement
        for index, capteur in enumerate(capteur_list):
            update_register(capteur, index)
            
            vl = []
            for k, v in capteur.data_registers.items():
                vl.append(v[0])
            
            print(f"{vl[0]}, {vl[1]}")
