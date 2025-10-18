"""Lanceur"""

import time

from one_pue.controller import Controller

if __name__ == "__main__":
    controller = Controller()
    controller.init_agents()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        controller.stop_prometheus_client()
