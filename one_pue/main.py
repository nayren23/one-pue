"""Lanceur"""

import time
from flask import Flask, render_template, request, redirect, url_for, jsonify, Blueprint
import json
from prometheus_client.registry import REGISTRY

from one_pue.controller import Controller

if __name__ == "__main__":
    controller = Controller()
    controller.init_agents()

    app = Flask(__name__)
    DATA_FILE = "agents.json"

    agent = Blueprint("agent", __name__, url_prefix="/agent")

    @agent.route("/test", methods=["GET"])
    def refresh():
        """Test"""
        response = jsonify(message="REFRESHED_SUCCESSFULLY")
        return response, 200

    @agent.route("/all")
    def list_agents():
        return render_template("agents.html", agents=controller.load_agents())

    def save_agents(agents):
        """Écrire la liste des agents dans le fichier JSON."""
        with open(DATA_FILE, "w") as f:
            json.dump(agents, f, indent=4)
        controller.stop_prometheus_client()
        for gage in controller.get_gauge_list():
            REGISTRY.unregister(gage)
        agents = controller.load_agents()
        for a in agents:
            controller.create_agent_gauge(
                a["name"],
                a["description"],
                a["modbus_host"],
                a["modbus_port"],
                a["modbus_register"],
            )
        controller.start_prometheus_client()

    @agent.route("/create", methods=["GET", "POST"])
    def create_agent():
        if request.method == "POST":
            name = request.form["name"].strip().lower().replace(" ", "_")
            description = request.form["description"]
            modbus_host = request.form["modbus_host"]
            modbus_port = int(request.form["modbus_port"])
            print("iciiiii")
            print(request.form)
            modbus_register_1 = int(request.form["modbus_register_1"], 16)
            modbus_register_2 = int(request.form["modbus_register_2"], 16)
            modbus_register = [modbus_register_1, modbus_register_2]

            agents = controller.load_agents()
            agents.append(
                {
                    "name": name,
                    "description": description,
                    "modbus_host": modbus_host,
                    "modbus_port": modbus_port,
                    "modbus_register": modbus_register,
                }
            )
            save_agents(agents)
            return redirect(url_for("agent.list_agents"))

        return render_template("create_agent.html")

    app.register_blueprint(agent)
    app.run(
        debug=True,
        host="localhost",
        port=5000,
    )

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        controller.stop_prometheus_client()
