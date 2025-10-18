"""Lanceur"""

import time
from flask import Flask, render_template, request, redirect, url_for, jsonify, Blueprint
import os
import json

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

    def load_agents():
        """Lire les agents depuis le fichier JSON."""
        if not os.path.exists(DATA_FILE):
            return []
        with open(DATA_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []

    @agent.route("/all")
    def list_agents():
        return render_template("agents.html", agents=load_agents())

    def save_agents(agents):
        """Écrire la liste des agents dans le fichier JSON."""
        with open(DATA_FILE, "w") as f:
            json.dump(agents, f, indent=4)

    @agent.route("/create", methods=["GET", "POST"])
    def create_agent():
        if request.method == "POST":
            name = request.form["name"]
            metric_type = request.form["metric_type"]
            modbus_host = request.form["modbus_host"]
            modbus_port = int(request.form["modbus_port"])
            modbus_register = int(request.form["modbus_register"])

            agents = load_agents()
            agents.append(
                {
                    "name": name,
                    "metric_type": metric_type,
                    "modbus_host": modbus_host,
                    "modbus_port": modbus_port,
                    "modbus_register": modbus_register,
                }
            )
            save_agents(agents)

            # ✅ Endpoint du blueprint : "agent.list_agents"
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
