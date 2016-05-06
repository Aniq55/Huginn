"""
The huginn.fdm module contains classes and functions that can be used to
initialize the flight dynamics model and create a model for a simulated
aircraft
"""
from math import degrees
import logging

from PyJSBSim import FGFDMExec

from huginn import configuration
from huginn.unit_conversions import convert_meters_to_feet,\
    convert_meters_per_sec_to_knots, convert_feet_to_meters,\
    convert_rankine_to_kelvin, convert_psf_to_pascal,\
    convert_libra_to_newtons

class JSBSimFDM(object):
    def __init__(self, fdm, start_trimmed=False):
        self.fdm = fdm
        self.start_trimmed = start_trimmed
        self.logger = logging.getLogger("huginn")

    def run(self):
        return self.fdm.run()

    def reset(self):
        self.logger.debug("Reseting JSBSim to initial conditions")

        reset_result = self.fdm.reset()

        if not reset_result:
            self.logger.debug("Failed to reset the JSBSim model")

        self.fdm.set_aileron(0.0)
        self.fdm.set_elevator(0.0)
        self.fdm.set_rudder(0.0)
        self.fdm.set_throttle(0.0)

        self.fdm.start_engines()

        return reset_result

    def trim(self):
        return self.fdm.trim()

    def get_dt(self):
        return self.fdm.get_dt()

    def get_simulation_time(self):
        return self.fdm.get_sim_time()

    def update_aircraft(self, aircraft):
        self.update_gps(aircraft.gps)
        self.update_accelerometer(aircraft.accelerometer)
        self.update_gyroscope(aircraft.gyroscope)
        self.update_thermometer(aircraft.thermometer)
        self.update_pressure_sensor(aircraft.pressure_sensor)
        self.update_pitot_tube(aircraft.pitot_tube)
        self.update_inertial_navigation_system(aircraft.inertial_navigation_system)
        self.update_aircraft_controls(aircraft.controls)
        self.update_engine(aircraft.engine)

    def update_gps(self, gps):
        gps.latitude = self.fdm.get_latitude()
        gps.longitude = self.fdm.get_longitude()

        gps.altitude = self.fdm.get_altitude()

        airspeed_in_fps = self.fdm.get_airspeed()
        gps.airspeed = convert_feet_to_meters(airspeed_in_fps)
        #self.airspeed = convert_knots_to_meters_per_sec(airspeed_in_knots)

        gps.heading = degrees(self.fdm.get_heading())

    def update_accelerometer(self, accelerometer):
        accelerometer.x_acceleration = convert_feet_to_meters(self.fdm.get_x_acceleration())

        accelerometer.y_acceleration = convert_feet_to_meters(self.fdm.get_y_acceleration())

        accelerometer.z_acceleration = convert_feet_to_meters(self.fdm.get_z_acceleration())

    def update_gyroscope(self, gyroscope):
        gyroscope.roll_rate = degrees(self.fdm.get_roll_rate())

        gyroscope.pitch_rate = degrees(self.fdm.get_pitch_rate())

        gyroscope.yaw_rate = degrees(self.fdm.get_yaw_rate())

    def update_thermometer(self, thermometer):
        thermometer.temperature = convert_rankine_to_kelvin(self.fdm.get_temperature())

    def update_pressure_sensor(self, pressure_sensor):
        pressure_sensor.pressure = convert_psf_to_pascal(self.fdm.get_pressure())

    def update_pitot_tube(self, pitot_tube):
        pitot_tube.pressure = convert_psf_to_pascal(self.fdm.get_total_pressure())

    def update_inertial_navigation_system(self, ins):
        ins.roll = self.fdm.get_roll()

        ins.pitch = self.fdm.get_pitch()

        ins.heading = degrees(self.fdm.get_heading())

        ins.latitude = self.fdm.get_latitude()
        ins.longitude = self.fdm.get_longitude()

        airspeed_in_fps = self.fdm.get_airspeed()
        ins.airspeed = convert_feet_to_meters(airspeed_in_fps)

        ins.altitude = self.fdm.get_altitude()

    def update_aircraft_controls(self, controls):
        controls.elevator = self.fdm.get_elevator()
        controls.aileron = self.fdm.get_aileron()
        controls.rudder = self.fdm.get_rudder()
        controls.throttle = self.fdm.get_throttle()

    def update_engine(self, engine):
        engine.thrust = convert_libra_to_newtons(self.fdm.get_thrust())

        engine.throttle = self.fdm.get_throttle()

    def set_aircraft_controls(self, aileron, elevator, rudder, throttle):
        if aileron > 1.0:
            aileron = 1.0
        elif aileron < -1.0:
            aileron = -1.0

        self.fdm.set_aileron(aileron)

        if elevator > 1.0:
            elevator = 1.0
        elif elevator < -1.0:
            elevator = -1.0

        self.fdm.set_elevator(elevator)

        if rudder > 1.0:
            rudder = 1.0
        elif rudder < -1.0:
            rudder = -1.0

        self.fdm.set_rudder(rudder)

        if throttle > 1.0:
            throttle = 1.0
        elif throttle < 0.0:
            throttle = 0.0

        self.fdm.set_throttle(throttle)

class FDMBuilder(object):
    """The FDMBuilder creates the flight dynamics model object that will be
    used by the simulator"""
    def __init__(self, data_path):
        self.data_path = data_path
        self.dt = configuration.DT

        self.aircraft = configuration.AIRCRAFT

        self.latitude = configuration.LATITUDE
        self.longitude = configuration.LONGITUDE
        self.altitude = configuration.ALTITUDE
        self.airspeed = configuration.AIRSPEED
        self.heading = configuration.HEADING

        self.trim = False

        self.logger = logging.getLogger("huginn")

    def create_fdm(self):
        """Create the flight dynamics model"""

        fdmexec = FGFDMExec()

        self.logger.debug("Using jsbsim data at %s", self.data_path)

        fdmexec.SetRootDir(self.data_path)
        fdmexec.SetAircraftPath("")
        fdmexec.SetEnginePath(self.data_path + "/Engines")
        fdmexec.SetSystemsPath(self.data_path + "/Systems")
        #fdm.set_data_path(self.data_path)

        self.logger.debug("JSBSim dt is %f", self.dt)
        fdmexec.Setdt(self.dt)
        #fdm.set_dt(self.dt)

        self.logger.debug("Using aircraft %s", self.aircraft)
        fdmexec.LoadModel(self.aircraft)
        #fdm.load_model(self.aircraft)

        self.logger.debug("starting the aircraft's engines")
        fdmexec.GetPropulsion().GetEngine(0).SetRunning(1)
        #fdm.start_engines()

        fdmexec.GetFCS().SetThrottleCmd(0, 0.0)
        #fdm.set_throttle(0.0)

        altitude_in_feet = convert_meters_to_feet(self.altitude)
        airspeed_in_knots = convert_meters_per_sec_to_knots(self.airspeed)

        self.logger.debug("Initial latitude: %f degrees", self.latitude)
        self.logger.debug("Initial longitude: %f degrees", self.longitude)
        self.logger.debug("Initial altitude: %f meters", self.altitude)
        self.logger.debug("Initial airspeed: %f meters/second", self.airspeed)
        self.logger.debug("Initial heading: %f degrees", self.heading)

        fdmexec.GetIC().SetLatitudeDegIC(self.latitude)
        fdmexec.GetIC().SetLongitudeDegIC(self.longitude)
        fdmexec.GetIC().SetAltitudeASLFtIC(altitude_in_feet)
        fdmexec.GetIC().SetPsiDegIC(self.heading)
        fdmexec.GetIC().SetVtrueKtsIC(airspeed_in_knots)
        #fdm.set_initial_condition(self.latitude, self.longitude, altitude_in_feet, airspeed_in_knots, self.heading)

        if not fdmexec.RunIC():
            self.logger.error("Failed to run initial condition")
            return None

        if self.trim:
            self.logger.warning("Trimming is not supported yet")

#        if self.trim:
#            self.logger.debug("Trimming the aircraft")
#            trim_result = fdm.trim()
#
#            if not trim_result:
#                self.logger.warning("Failed to trim the aircraft")

        # Run the simulation for 1 second in order to make sure that everything
        # is ok
#        while fdm.get_sim_time() < 1.0:
        while fdmexec.GetSimTime() < 1.0:
            fdmexec.ProcessMessage()
            fdmexec.CheckIncrementalHold()

            if not fdmexec.Run():
#            if not fdm.run():
                self.logger.error("Failed to execute initial run")
                return None

        fdmexec.PrintSimulationConfiguration()
        #fdm.print_simulation_configuration()

        fdmexec.GetPropagate().DumpState()
        #fdm.dump_state()

        return fdmexec

class Accelerations(object):
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec

    @property
    def x(self):
        """Returns the acceleration along the x axis of the aircraft in
        meters/sec^2"""
        return convert_feet_to_meters(self.fdmexec.GetAuxiliary().GetPilotAccel(1))

    @property
    def y(self):
        """Returns the acceleration along the y axis of the aircraft in
        meters/sec^2"""
        return convert_feet_to_meters(self.fdmexec.GetAuxiliary().GetPilotAccel(2))

    @property
    def z(self):
        """Returns the acceleration along the z axis of the aircraft in
        meters/sec^2"""
        return convert_feet_to_meters(self.fdmexec.GetAuxiliary().GetPilotAccel(3))

class Velocities(object):
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec

    @property
    def roll_rate(self):
        """Return the roll rate in degrees/sec"""
        return degrees(self.fdmexec.GetPropagate().GetPQR(1))

    @property
    def pitch_rate(self):
        """Return the pitch rate in degrees/sec"""
        return degrees(self.fdmexec.GetPropagate().GetPQR(2))

    @property
    def yaw_rate(self):
        """Return the yaw rate in degrees/sec"""
        return degrees(self.fdmexec.GetPropagate().GetPQR(3))

    @property
    def airspeed(self):
        """Return the airspeed in meters/second"""
        return convert_feet_to_meters(self.fdmexec.GetAuxiliary().GetVtrueFPS())

class Position(object):
    """The Position class contains data about the position of the aircraft"""
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec

    @property
    def latitude(self):
        """Returns the latitude in degrees"""
        return self.fdmexec.GetPropagate().GetLatitudeDeg()

    @property
    def longitude(self):
        """Returns the longitude in degrees"""
        return self.fdmexec.GetPropagate().GetLongitudeDeg()

    @property
    def altitude(self):
        """Returns the altitude in meters"""
        return self.fdmexec.GetPropagate().GetAltitudeASLmeters()

    @property
    def heading(self):
        """Returns the heading in degrees"""
        return degrees(self.fdmexec.GetPropagate().GetEuler(3))

class Orientation(object):
    """The Orientation class contains data about the orientation of the aircraft"""
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec

    @property
    def roll(self):
        """Return the roll angle in degrees"""
        return self.fdmexec.GetPropagate().GetEulerDeg(1)

    @property
    def pitch(self):
        """Return the pitch angle in degrees"""
        return self.fdmexec.GetPropagate().GetEulerDeg(2)

class FDM(object):
    """The FDM object is a wrapper around the JSBSim objects that contains the
    values of the flight dynamics model."""
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec
        self.accelerations = Accelerations(fdmexec)
        self.velocities = Velocities(fdmexec)
        self.position = Position(fdmexec)
        self.orientation = Orientation(fdmexec)
