###########################################
#                                         #
#                  Main                   #
#                                         #
###########################################

# ---------------- Imports --------------- #
from senderBot import SenderBot

# ----------- Constants ------------------ #
MODBUS_HOST = "172.18.146.98"
MODBUS_PORT = 502
MODBUS_UNIT_ID = 1
POWER_AVERAGE = 450
POWER_BASE_VALUE = POWER_AVERAGE * 24 * 365

# -----------  Functions ----------------- #



# --------------- Main Logic -------------- #

if __name__ == "__main__":
    
    DirisA40 = SenderBot(name="Diris A40", host=MODBUS_HOST, port=MODBUS_PORT, unit_id=MODBUS_UNIT_ID)
    print(DirisA40)

   