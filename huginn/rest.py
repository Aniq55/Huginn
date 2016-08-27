"""
The huginn.rest module contains the rest interface endpoints
"""
from logging import getLogger

from flask import request
from flask_restful import Resource, reqparse, marshal_with, abort
from tinydb import Query

from huginn.schemas import (AccelerationsSchema, VelocitiesSchema,
                            OrientationSchema, AtmosphereShema, ForcesSchema,
                            InitialConditionSchema, PositionSchema,
                            AirspeedIndicatorSchema, AltimeterSchema,
                            AttitudeIndicatorSchema, HeadingIndicatorSchema,
                            VerticalSpeedIndicatorSchema)

from huginn.fdm import (Accelerations, Velocities, Orientation, Atmosphere,
                        Forces, InitialCondition, Position)

from huginn import request_models
from huginn import request_parsers


logger = getLogger(__name__)


class FDMResource(Resource):
    """The FDMResource will return the data from the flight dynamics model"""

    def __init__(self, fdm, aircraft):
        """Create a new FDMResource object

        Arguments:
        fdm: an FDM object
        aircraft: an aircraft object
        """
        self.fdm = fdm
        self.aircraft = aircraft

    def get(self):
        """Get the fdm data"""
        sensors = self.aircraft.sensors

        flight_data = {
            "time": self.fdm.fdmexec.GetSimTime(),
            "dt": self.fdm.fdmexec.GetDeltaT(),
            "latitude": self.fdm.position.latitude,
            "longitude": self.fdm.position.longitude,
            "altitude": self.fdm.position.altitude,
            "airspeed": self.fdm.velocities.true_airspeed,
            "heading": self.fdm.orientation.psi,
            "x_acceleration": self.fdm.accelerations.x,
            "y_acceleration": self.fdm.accelerations.y,
            "z_acceleration": self.fdm.accelerations.z,
            "roll_rate": self.fdm.velocities.p,
            "pitch_rate": self.fdm.velocities.q,
            "yaw_rate": self.fdm.velocities.r,
            "temperature": self.fdm.atmosphere.temperature,
            "static_pressure": self.fdm.atmosphere.pressure,
            "total_pressure": sensors.pitot_tube.true_pressure,
            "roll": self.fdm.orientation.phi,
            "pitch": self.fdm.orientation.theta,
            "climb_rate": self.fdm.velocities.climb_rate
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
            "running": not self.simulator.is_paused(),
            "crashed": self.simulator.crashed
        }

        return simulator_state

    def execute_command(self, command, params=None):
        """Execute the simulator command

        Arguments:
        command: the command to execute
        params: the parameters of the command
        """
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
        elif command == "start_paused":
            self.simulator.start_paused = True

            response = {"result": "ok",
                        "command": "start_paused"}
        elif command == "start_running":
            self.simulator.start_paused = False

            response = {"result": "ok",
                        "command": "start_running"}
        else:
            response = {"error": "unknown command",
                        "command": command}

        return response

    def post(self):
        """Execute a command on the simulator"""
        parser = reqparse.RequestParser()

        parser.add_argument("command", type=str, required=True)
        parser.add_argument("time_to_run", type=float)
        parser.add_argument("paused", type=bool)

        args = parser.parse_args()

        command = args.command

        params = {}

        if args.time_to_run:
            params["time_to_run"] = args.time_to_run

        if args.paused:
            params["paused"] = args.paused

        return self.execute_command(command, params)


class ObjectResource(Resource):
    """The ObjectResource is using an object and a marshmallow schema to return
    the representation of an object"""

    def __init__(self, obj, schema):
        """Create a new ObjectResource object

        Arguments:
        obj: the object to encode
        schema: the marshmallow schema object
        """
        self.obj = obj
        self.schema = schema

    def get(self):
        """return the object data when a GET request is executed"""
        result = self.schema.dump(self.obj)

        return result.data


class AccelerationsResource(ObjectResource):
    """The AccelerationsResource object returns the fdm accelerations"""

    def __init__(self, fdmexec):
        """Create a new AccelerationsResource object

        Arguments:
        fdmexec: a jsbsim FGFDMExec object
        """
        self.fdmexec = fdmexec
        self.accelerations = Accelerations(self.fdmexec)
        self.acceleration_schema = AccelerationsSchema()

        super(AccelerationsResource, self).__init__(self.accelerations,
                                                    self.acceleration_schema)


class VelocitiesResource(ObjectResource):
    """The VelocitiesResource object returns the fdm velocities"""

    def __init__(self, fdmexec):
        """Create a new VelocitiesResource object

        Arguments:
        fdmexec: a jsbsim FGFDMExec object
        """
        self.fdmexec = fdmexec
        self.velocities = Velocities(self.fdmexec)
        self.velocities_schema = VelocitiesSchema()

        super(VelocitiesResource, self).__init__(self.velocities,
                                                 self.velocities_schema)


class OrientationResource(ObjectResource):
    """The OrientationResource object returns the orientations of the
    aircraft"""

    def __init__(self, fdmexec):
        """Create a new OrientationResource object

        Arguments:
        fdmexec: a jsbsim FGFDMExec object
        """
        self.fdmexec = fdmexec
        self.orientation = Orientation(fdmexec)
        self.orientation_schema = OrientationSchema()

        super(OrientationResource, self).__init__(self.orientation,
                                                  self.orientation_schema)


class AtmosphereResource(ObjectResource):
    """The AtmosphereResource object return the fdm atmospheric data"""

    def __init__(self, fdmexec):
        """Create a new AtmosphereResource object

        Arguments:
        fdmexec: a jsbsim FGFDMExec object
        """
        self.fdmexec = fdmexec
        self.atmosphere = Atmosphere(fdmexec)
        self.atmosphere_schema = AtmosphereShema()

        super(AtmosphereResource, self).__init__(self.atmosphere,
                                                 self.atmosphere_schema)


class ForcesResource(ObjectResource):
    """The ForcesResource object contains the forces that act on the
    aircraft"""

    def __init__(self, fdmexec):
        """Create a new ForcesResource object

        Arguments:
        fdmexec: a jsbsim FGFDMExec object
        """
        self.fdmexec = fdmexec
        self.forces = Forces(fdmexec)
        self.forces_schema = ForcesSchema()

        super(ForcesResource, self).__init__(self.forces,
                                             self.forces_schema)


class InitialConditionResource(ObjectResource):
    """The InitialConditionResource object contain the simulator initial
    conditions"""

    def __init__(self, fdmexec):
        """Create a new InitialConditionResource object

        Arguments:
        fdmexec: a jsbsim FGFDMExec object
        """
        self.fdmexec = fdmexec
        self.initial_condition = InitialCondition(fdmexec)
        self.initial_condition_schema = InitialConditionSchema()

        super(InitialConditionResource, self).__init__(
            self.initial_condition,
            self.initial_condition_schema
        )

    def update_initial_conditions(self, initial_condition):
        """Update the simulator initial conditions

        Arguments:
        initial_conditions: a dictionary with the initial conditions of the
            simulator
        """
        if "latitude" in initial_condition:
            self.initial_condition.latitude = initial_condition["latitude"]

        if "longitude" in initial_condition:
            self.initial_condition.longitude = initial_condition["longitude"]

        if "airspeed" in initial_condition:
            self.initial_condition.airspeed = initial_condition["airspeed"]

        if "altitude" in initial_condition:
            self.initial_condition.altitude = initial_condition["altitude"]

        if "heading" in initial_condition:
            self.initial_condition.heading = initial_condition["heading"]

    def post(self):
        """Update the simulator condition when a POST request is executed"""
        data = request.json

        ic_schema = InitialConditionSchema()

        initial_condition = ic_schema.load(data)

        self.update_initial_conditions(initial_condition.data)

        return {"result": "ok"}


class PositionResource(ObjectResource):
    """The PositionResource object contain the aircraft position data"""

    def __init__(self, fdmexec):
        """Create a new PositionResource object

        Arguments:
        fdmexec: a jsbsim FGFDMExec object
        """
        self.fdmexec = fdmexec
        self.position = Position(fdmexec)
        self.position_schema = PositionSchema()

        super(PositionResource, self).__init__(
            self.position,
            self.position_schema
        )


class AirspeedIndicatorResource(ObjectResource):
    """The AirspeedIndicatorResource object returns the aircraft's true
    airspeed"""

    def __init__(self, airspeed_indicator):
        """Create a new AirspeedindicatorResource object

        Arguments:
        airspeed_indicator: an AirspeedIndicator object
        """
        self.airspeed_indicator = airspeed_indicator
        self.airspeed_indicator_schema = AirspeedIndicatorSchema()

        super(AirspeedIndicatorResource, self).__init__(
            self.airspeed_indicator,
            self.airspeed_indicator_schema
        )


class AltimeterResource(ObjectResource):
    """The AltimeterResource object returns the aircraft's altimeter data"""

    def __init__(self, altimeter):
        """Create a new AltimeterResource object

        Arguments:
        altimeter: an Altimeter object
        """
        self.altimeter = altimeter
        self.altimeter_schema = AltimeterSchema()

        super(AltimeterResource, self).__init__(
            self.altimeter,
            self.altimeter_schema
        )


class AttitudeIndicatorResource(ObjectResource):
    """The AttitudeIndicatorResource object returns the aircraft's attitude
    indicator data"""

    def __init__(self, attitude_indicator):
        """Create a new AttitudeIndicatorResource object

        Arguments:
        attitude_indicator: an AttitudeIndicator object
        """
        self.attitude_indicator = attitude_indicator
        self.attitude_indicator_schema = AttitudeIndicatorSchema()

        super(AttitudeIndicatorResource, self).__init__(
            self.attitude_indicator,
            self.attitude_indicator_schema
        )


class HeadingIndicatorResource(ObjectResource):
    """The HeadingIndicatorResource object returns the aircraft's heading
    indicator data"""

    def __init__(self, heading_indicator):
        """Create a new HeadingIndicatorResource object

        Arguments:
        heading_indicator: a HeadingIndicator object
        """
        self.heading_indicator = heading_indicator
        self.heading_indicator_schema = HeadingIndicatorSchema()

        super(HeadingIndicatorResource, self).__init__(
            self.heading_indicator,
            self.heading_indicator_schema
        )


class VerticalSpeedIndicatorResource(ObjectResource):
    """The VerticalSpeedIndicatorResource object returns the aircraft's heading
    indicator data"""

    def __init__(self, vertical_speed_indicator):
        """Create a new VerticalSpeedIndicatorResource object

        Arguments:
        vertical_speed_indicator: a VerticalSpeedIndicator object
        """
        self.vertical_speed_indicator = vertical_speed_indicator
        self.vertical_speed_indicator_schema = VerticalSpeedIndicatorSchema()

        super(VerticalSpeedIndicatorResource, self).__init__(
            self.vertical_speed_indicator,
            self.vertical_speed_indicator_schema
        )


class WaypointResource(Resource):
    """The WaypointResource is used to ad, delete and update waypoints"""
    def __init__(self, db):
        self.db = db

    @marshal_with(request_models.waypoint)
    def get(self, name):
        """Get the waypoint's data"""
        Document = Query()

        waypoints = self.db.search(Document.type == "waypoints")[0]

        waypoint = waypoints["waypoints"].get(name)

        if waypoint is not None:
            return waypoint
        else:
            abort(404, error="waypoint doesn't exist", name=name)

    @marshal_with(request_models.waypoint)
    def post(self, name):
        """Add a new waypoint or update an existing waypoint's data"""
        waypoint = request_parsers.waypoint.parse_args()
        waypoint["name"] = name

        Document = Query()

        waypoints = self.db.search(Document.type == "waypoints")[0]

        waypoints["waypoints"][name] = waypoint

        self.db.update(waypoints, Document.type == "waypoints")

        return waypoint

    @marshal_with(request_models.waypoint)
    def delete(self, name):
        """Delete a waypoint"""
        Document = Query()

        waypoints = self.db.search(Document.type == "waypoints")[0]

        waypoint = waypoints["waypoints"].get(name)

        if waypoint is not None:
            del waypoints["waypoints"][name]
            return waypoint
        else:
            abort(404, error="waypoint doesn't exist", name=name)


class WaypointsResource(Resource):
    """The WaypointsResource is used to retrieve all the available waypoints"""
    def __init__(self, db):
        self.db = db

    @marshal_with(request_models.waypoint)
    def get(self):
        """Get a list of the available waypoints"""
        Document = Query()

        waypoints = self.db.search(Document.type == "waypoints")[0]

        return waypoints["waypoints"].values()
