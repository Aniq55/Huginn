"""
The huginn.rest module contains the rest interface endpoints
"""

from flask_restful import Resource, reqparse


class FDMResource(Resource):
    """The FDMResource will return the data from the flight dynamics model"""

    def __init__(self, fdmexec, aircraft):
        """Create a new FDMResource object

        Arguments:
        fdmexec: A jsbsim FGFDMExec object
        aircraft: an aircraft object
        """
        self.fdmexec = fdmexec
        self.aircraft = aircraft

    def get(self):
        """Get the fdm data"""
        sensors = self.aircraft.sensors

        flight_data = {
            "time": self.fdmexec.GetSimTime(),
            "dt": self.fdmexec.GetDeltaT(),
            "latitude": self.aircraft.instruments.gps.latitude,
            "longitude": self.aircraft.instruments.gps.longitude,
            "altitude": self.aircraft.instruments.gps.altitude,
            "airspeed": self.aircraft.instruments.gps.airspeed,
            "heading": self.aircraft.instruments.gps.heading,
            "x_acceleration": sensors.accelerometer.true_x,
            "y_acceleration": sensors.accelerometer.true_y,
            "z_acceleration": sensors.accelerometer.true_z,
            "roll_rate": sensors.gyroscope.true_roll_rate,
            "pitch_rate": sensors.gyroscope.true_pitch_rate,
            "yaw_rate": sensors.gyroscope.true_yaw_rate,
            "temperature": sensors.thermometer.true_temperature,
            "static_pressure": sensors.pressure_sensor.true_pressure,
            "total_pressure": sensors.pitot_tube.true_pressure,
            "roll": sensors.inertial_navigation_system.true_roll,
            "pitch": sensors.inertial_navigation_system.true_pitch,
            "thrust": self.aircraft.engine.thrust,
            "aileron": self.aircraft.controls.aileron,
            "elevator": self.aircraft.controls.elevator,
            "rudder": self.aircraft.controls.rudder,
            "throttle": self.aircraft.engine.throttle,
        }

        return flight_data


class AircraftResource(Resource):
    """The AircraftResource returns infomration about the aircraft"""

    def __init__(self, aircraft):
        """Create a new AircraftResource object

        Arguments:
        aircraft: an Aircraft object
        """
        self.aircraft = aircraft

    def get(self):
        """Get the aircraft information"""
        return {"type": self.aircraft.type}


class GPSResource(Resource):
    """The GPSResource returns the gps data"""

    def __init__(self, gps):
        """Create a new GPSResource object

        Arguments:
        gps: A GPS object
        """
        self.gps = gps

    def get(self):
        """Return the gps data"""
        gps_data = {
            "latitude": self.gps.latitude,
            "longitude": self.gps.longitude,
            "altitude": self.gps.altitude,
            "airspeed": self.gps.airspeed,
            "heading": self.gps.heading
        }

        return gps_data


class AccelerometerResource(Resource):
    """The AccelerometerResource returns the accelerometer measurements"""

    def __init__(self, accelerometer):
        """Create a new AccelerometerResource object

        Arguments:
        accelerometer: an Accelerometer object
        """
        self.accelerometer = accelerometer

    def get(self):
        """Returns the accelerometer measurements"""
        accelerometer_data = {
            "x": self.accelerometer.x,
            "y": self.accelerometer.y,
            "z": self.accelerometer.z,
        }

        return accelerometer_data


class GyroscopeResource(Resource):
    """The GyroscopeResource returns the data from the gyroscope sensor"""

    def __init__(self, gyroscope):
        """Create a new GyroscopeResource object

        Arguments:
        gyroscope: A Gyroscope object
        """
        self.gyroscope = gyroscope

    def get(self):
        """Returns the gyroscope measurements"""
        gyroscope_data = {
            "roll_rate": self.gyroscope.roll_rate,
            "pitch_rate": self.gyroscope.pitch_rate,
            "yaw_rate": self.gyroscope.yaw_rate
        }

        return gyroscope_data


class ThermometerResource(Resource):
    """The ThermometerResource class contains the measurements from the
    temperature sensor"""

    def __init__(self, thermometer):
        """Create a new ThermometerResource object

        Arguments:
        thermometer: a Thermometer object
        """
        self.thermometer = thermometer

    def get(self):
        """Returns the thermometer measurements"""
        thermometer_data = {
            "temperature": self.thermometer.temperature,
        }

        return thermometer_data


class PressureSensorResource(Resource):
    """The PressureSensorResource class returns the pressure sensor
    measurements"""

    def __init__(self, pressure_sensor):
        """Create a new PressureSensorResource object

        Arguments:
        pressure_sensor: a PressureSensor object
        """
        self.pressure_sensor = pressure_sensor

    def get(self):
        """Returns the pressure sensor data"""
        pressure_sensor_data = {
            "static_pressure": self.pressure_sensor.pressure,
        }

        return pressure_sensor_data


class PitotTubeResource(Resource):
    """The PitotTubeResource returns the measurements from the pitot tube"""

    def __init__(self, pitot_tube):
        """Create a new PitotTubeResource object

        Arguments:
        pitot_tube: A PitotTube object
        """
        self.pitot_tube = pitot_tube

    def get(self):
        """Returns the pitot tube measurements"""
        pitot_tube_data = {
            "total_pressure": self.pitot_tube.pressure,
        }

        return pitot_tube_data


class InertialNavigationSystemResource(Resource):
    """The InertialNavigationSystemResource returns the measurements from the
    inertial navigation system"""

    def __init__(self, inertial_navigation_system):
        """Create a new InertialNavigationSystemResource object

        Arguments:
        inertial_navigation_system: An InertialNavigationSystem object
        """
        self.inertial_navigation_system = inertial_navigation_system

    def get(self):
        """Returns the ins measurements"""
        inertial_navigation_system_data = {
            "latitude": self.inertial_navigation_system.latitude,
            "longitude": self.inertial_navigation_system.longitude,
            "altitude": self.inertial_navigation_system.altitude,
            "airspeed": self.inertial_navigation_system.airspeed,
            "heading": self.inertial_navigation_system.heading,
            "roll": self.inertial_navigation_system.roll,
            "pitch": self.inertial_navigation_system.pitch,
        }

        return inertial_navigation_system_data


class EngineResource(Resource):
    """The EngineResource class returns the engine data"""
    def __init__(self, engine):
        """Create a new EngineResource object

        Arguments:
        engine: An Engine object
        """
        self.engine = engine

    def get(self):
        """Returns the engine data"""
        engine_data = {
            "thrust": self.engine.thrust,
            "throttle": self.engine.throttle,
        }

        return engine_data


class FlightControlsResource(Resource):
    """The FlightControlsResource return the flight controls values"""

    def __init__(self, controls):
        """Create a new FlightControlsResource object

        Arguments:
        controls: A Controls object
        """
        self.controls = controls

    def get(self):
        """returns the flight controls values"""
        flight_controls_data = {
            "aileron": self.controls.aileron,
            "elevator": self.controls.elevator,
            "rudder": self.controls.rudder,
            "throttle": self.controls.throttle,
        }

        return flight_controls_data


class SimulatorControlResource(Resource):
    """The SimulatorControlResource provides the endpoint that is used to
    control the simulator"""

    def __init__(self, simulator):
        """Create a new SimulatorControlResource object

        Arguments:
        simulator: a Simulator object
        """
        self.simulator = simulator

    def get(self):
        """Returns the simulator state"""
        simulator_state = {
            "time": self.simulator.simulation_time,
            "dt": self.simulator.dt,
            "running": not self.simulator.is_paused()
        }

        return simulator_state

    def execute_command(self, command, params=None):
        if command == "reset":
            self.simulator.reset()

            response = {"result": "ok",
                        "command": command}
        elif command == "pause":
            self.simulator.pause()

            response = {"result": "ok",
                        "command": command}
        elif command == "resume":
            self.simulator.resume()

            response = {"result": "ok",
                        "command": command}
        elif command == "step":
            self.simulator.step()

            response = {"result": "ok",
                        "command": command}
        elif command == "run_for":
            if params:
                time_to_run = params["time_to_run"]
            else:
                time_to_run = None

            if not time_to_run:
                response = {"error": "no time to run provided",
                            "command": command}
            else:
                self.simulator.run_for(time_to_run)

                response = {"result": "ok",
                            "command": "run_for"}
        else:
            response = {"error": "unknown command",
                        "command": command}

        return response

    def post(self):
        """Execute a command on the simulator"""
        parser = reqparse.RequestParser()

        parser.add_argument("command", type=str, required=True)
        parser.add_argument("time_to_run", type=float)

        args = parser.parse_args()

        command = args.command

        params = None
        if args.time_to_run:
            params = {"time_to_run": args.time_to_run}

        return self.execute_command(command, params)
