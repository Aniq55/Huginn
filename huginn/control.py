import json

import requests

class SimulatorControlClient(object):
    """The SimulatorControlClient is used to remotely pause, resume and
    reset the simulator."""
    def __init__(self, huginn_host, simulator_control_port):
        self.huginn_host = huginn_host
        self.simulator_controls_port = simulator_control_port

    def _send_command(self, command):
        response = requests.post("http://%s:%d/simulator" % (self.huginn_host,
                                                             self.simulator_controls_port),
                                 data={"command": command})

        response_data = json.loads(response.text)

        return response_data

    def reset(self):
        """Reset the simulator"""
        response_data = self._send_command("reset")

        if response_data["result"] != "ok":
            return False

        return True

    def pause(self):
        """Pause the simulator"""
        response_data = self._send_command("pause")

        if response_data["result"] != "ok":
            return False

        return True

    def resume(self):
        """Resume the simulation"""
        response_data = self._send_command("resume")

        if response_data["result"] != "ok":
            return False

        return True
