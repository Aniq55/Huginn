from unittest import TestCase

from huginn.rest import (FDMResource, AccelerometerResource, GyroscopeResource,
                         GPSResource, ThermometerResource, PitotTubeResource,
                         PressureSensorResource, EngineResource,
                         InertialNavigationSystemResource, AircraftResource,
                         FlightControlsResource, SimulatorControlResource,
                         ObjectResource, AccelerationsResource,
                         VelocitiesResource, OrientationResource,
                         AtmosphereResource)

from huginn import configuration

from huginn.fdm import (FDMBuilder, Accelerations, Velocities, Orientation,
                        Atmosphere)

from huginn.aircraft import Aircraft
from huginn.simulator import Simulator
from huginn.schemas import AccelerationsSchema
from huginn.unit_conversions import convert_feet_to_meters


class FDMResourceTests(TestCase):
    def test_get_fdm_data(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        aircraft = Aircraft(fdmexec)

        resource = FDMResource(fdmexec, aircraft)

        fdm_data = resource.get()

        self.assertAlmostEqual(fdmexec.GetSimTime(), fdm_data["time"], 3)
        self.assertAlmostEqual(fdmexec.GetDeltaT(), fdm_data["dt"], 3)
        self.assertAlmostEqual(aircraft.instruments.gps.latitude, fdm_data["latitude"], 3)
        self.assertAlmostEqual(aircraft.instruments.gps.longitude, fdm_data["longitude"], 3)
        self.assertAlmostEqual(aircraft.instruments.gps.altitude, fdm_data["altitude"], 3)
        self.assertAlmostEqual(aircraft.instruments.gps.airspeed, fdm_data["airspeed"], 3)
        self.assertAlmostEqual(aircraft.instruments.gps.heading, fdm_data["heading"], 3)
        self.assertAlmostEqual(aircraft.sensors.accelerometer.true_x, fdm_data["x_acceleration"], 3)
        self.assertAlmostEqual(aircraft.sensors.accelerometer.true_y, fdm_data["y_acceleration"], 3)
        self.assertAlmostEqual(aircraft.sensors.accelerometer.true_z, fdm_data["z_acceleration"], 3)
        self.assertAlmostEqual(aircraft.sensors.gyroscope.true_roll_rate, fdm_data["roll_rate"], 3)
        self.assertAlmostEqual(aircraft.sensors.gyroscope.true_pitch_rate, fdm_data["pitch_rate"], 3)
        self.assertAlmostEqual(aircraft.sensors.gyroscope.true_yaw_rate, fdm_data["yaw_rate"], 3)
        self.assertAlmostEqual(aircraft.sensors.thermometer.true_temperature, fdm_data["temperature"], 3)
        self.assertAlmostEqual(aircraft.sensors.pressure_sensor.true_pressure, fdm_data["static_pressure"], 3)
        self.assertAlmostEqual(aircraft.sensors.pitot_tube.true_pressure, fdm_data["total_pressure"], 3)
        self.assertAlmostEqual(aircraft.sensors.inertial_navigation_system.true_roll, fdm_data["roll"], 3)
        self.assertAlmostEqual(aircraft.sensors.inertial_navigation_system.true_pitch, fdm_data["pitch"], 3)
        self.assertAlmostEqual(aircraft.engine.thrust, fdm_data["thrust"], 3)
        self.assertAlmostEqual(aircraft.controls.aileron, fdm_data["aileron"], 3)
        self.assertAlmostEqual(aircraft.controls.elevator, fdm_data["elevator"], 3)
        self.assertAlmostEqual(aircraft.controls.rudder, fdm_data["rudder"], 3)
        self.assertAlmostEqual(aircraft.engine.throttle, fdm_data["throttle"], 3)

        climb_rate = convert_feet_to_meters(-fdmexec.GetPropagate().GetVel(3))
        
        self.assertAlmostEqual(climb_rate, fdm_data["climb_rate"], 3)

class AccelerometerResourceTests(TestCase):
    def test_get_accelerometer_data(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        aircraft = Aircraft(fdmexec)

        resource = AccelerometerResource(aircraft.sensors.accelerometer)

        accelerometer_data = resource.get()

        self.assertAlmostEqual(aircraft.sensors.accelerometer.x, accelerometer_data["x"], 3)
        self.assertAlmostEqual(aircraft.sensors.accelerometer.y, accelerometer_data["y"], 3)
        self.assertAlmostEqual(aircraft.sensors.accelerometer.z, accelerometer_data["z"], 3)

class GyroscopeResourceTests(TestCase):
    def test_get_gyroscope_data(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        aircraft = Aircraft(fdmexec)

        resource = GyroscopeResource(aircraft.sensors.gyroscope)

        gyroscope_data = resource.get()

        self.assertAlmostEqual(aircraft.sensors.gyroscope.roll_rate, gyroscope_data["roll_rate"], 3)
        self.assertAlmostEqual(aircraft.sensors.gyroscope.pitch_rate, gyroscope_data["pitch_rate"], 3)
        self.assertAlmostEqual(aircraft.sensors.gyroscope.yaw_rate, gyroscope_data["yaw_rate"], 3)

class GPSResourceTests(TestCase):
    def test_get_gps_data(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        aircraft = Aircraft(fdmexec)

        resource = GPSResource(aircraft.instruments.gps)

        gps_data = resource.get()

        self.assertAlmostEqual(aircraft.instruments.gps.latitude, gps_data["latitude"], 3)
        self.assertAlmostEqual(aircraft.instruments.gps.longitude, gps_data["longitude"], 3)
        self.assertAlmostEqual(aircraft.instruments.gps.altitude, gps_data["altitude"], 3)
        self.assertAlmostEqual(aircraft.instruments.gps.airspeed, gps_data["airspeed"], 3)
        self.assertAlmostEqual(aircraft.instruments.gps.heading, gps_data["heading"], 3)

class ThermometerResourceTests(TestCase):
    def test_get_thermometer_data(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        aircraft = Aircraft(fdmexec)

        resource = ThermometerResource(aircraft.sensors.thermometer)

        thermometer_data = resource.get()

        self.assertAlmostEqual(aircraft.sensors.thermometer.temperature, thermometer_data["temperature"], 3)

class PressureResourceTests(TestCase):
    def test_get_pressure_data(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        aircraft = Aircraft(fdmexec)

        resource = PressureSensorResource(aircraft.sensors.pressure_sensor)

        pressure_sensor_data = resource.get()

        self.assertAlmostEqual(aircraft.sensors.pressure_sensor.pressure, pressure_sensor_data["static_pressure"], 3)

class PitotTubeResourceTests(TestCase):
    def test_get_pitot_tube_data(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        aircraft = Aircraft(fdmexec)

        resource = PitotTubeResource(aircraft.sensors.pitot_tube)

        pitot_tube_data = resource.get()

        self.assertAlmostEqual(aircraft.sensors.pitot_tube.pressure, pitot_tube_data["total_pressure"], 3)

class InertialNavigationSystemResourceTests(TestCase):
    def test_get_ins_data(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        aircraft = Aircraft(fdmexec)

        resource = InertialNavigationSystemResource(aircraft.sensors.inertial_navigation_system)

        inertial_navigation_system_data = resource.get()

        self.assertAlmostEqual(aircraft.sensors.inertial_navigation_system.latitude, inertial_navigation_system_data["latitude"], 3)
        self.assertAlmostEqual(aircraft.sensors.inertial_navigation_system.longitude, inertial_navigation_system_data["longitude"], 3)
        self.assertAlmostEqual(aircraft.sensors.inertial_navigation_system.altitude, inertial_navigation_system_data["altitude"], 3)
        self.assertAlmostEqual(aircraft.sensors.inertial_navigation_system.airspeed, inertial_navigation_system_data["airspeed"], 3)
        self.assertAlmostEqual(aircraft.sensors.inertial_navigation_system.heading, inertial_navigation_system_data["heading"], 3)
        self.assertAlmostEqual(aircraft.sensors.inertial_navigation_system.roll, inertial_navigation_system_data["roll"], 3)
        self.assertAlmostEqual(aircraft.sensors.inertial_navigation_system.pitch, inertial_navigation_system_data["pitch"], 3)

class EngineResourceTests(TestCase):
    def test_get_engine_data(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        aircraft = Aircraft(fdmexec)

        resource = EngineResource(aircraft.engine)

        engine_data = resource.get()

        self.assertAlmostEqual(aircraft.engine.thrust, engine_data["thrust"], 3)

class FlightControlsResourceTests(TestCase):
    def test_get_flight_controls(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        aircraft = Aircraft(fdmexec)

        resource = FlightControlsResource(aircraft.controls)

        flight_controls_data = resource.get()

        self.assertAlmostEqual(aircraft.controls.aileron, flight_controls_data["aileron"], 3)
        self.assertAlmostEqual(aircraft.controls.elevator, flight_controls_data["elevator"], 3)
        self.assertAlmostEqual(aircraft.controls.rudder, flight_controls_data["rudder"], 3)
        self.assertAlmostEqual(aircraft.engine.throttle, flight_controls_data["throttle"], 3)

class SimulatorControlResourceTests(TestCase):
    def test_get_simulator_state(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        simulator = Simulator(fdmexec)

        simulator_control_resource = SimulatorControlResource(simulator)

        response = simulator_control_resource.get()
        
        self.assertTrue(response["running"])
        self.assertAlmostEqual(response["dt"], configuration.DT, 3)
        self.assertAlmostEqual(response["time"], fdmexec.GetSimTime(), 3)

    def test_pause_simulator(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        simulator = Simulator(fdmexec)

        self.assertFalse(simulator.is_paused())

        simulator_control_resource = SimulatorControlResource(simulator)

        response = simulator_control_resource.execute_command("pause")

        self.assertDictEqual(response,
                             {"result": "ok",
                              "command": "pause"})

        self.assertTrue(simulator.is_paused())

    def test_resume_simulator(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        simulator = Simulator(fdmexec)
        simulator.pause()

        self.assertTrue(simulator.is_paused())

        simulator_control_resource = SimulatorControlResource(simulator)

        response = simulator_control_resource.execute_command("resume")

        self.assertDictEqual(response,
                             {"result": "ok",
                              "command": "resume"})

        self.assertFalse(simulator.is_paused())

    def test_step_simulator(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        simulator = Simulator(fdmexec)

        start_time = simulator.simulation_time

        simulator_control_resource = SimulatorControlResource(simulator)

        response = simulator_control_resource.execute_command("step")

        self.assertDictEqual(response,
                             {"result": "ok",
                              "command": "step"})

        self.assertGreater(simulator.simulation_time, start_time)

    def test_run_for_simulator(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        simulator = Simulator(fdmexec)

        start_time = simulator.simulation_time

        simulator_control_resource = SimulatorControlResource(simulator)

        response = simulator_control_resource.execute_command("run_for", {"time_to_run": 1.0})

        self.assertDictEqual(response,
                             {"result": "ok",
                              "command": "run_for"})

        self.assertGreater(simulator.simulation_time, start_time + 1.0)

    def test_reset_simulator(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        simulator = Simulator(fdmexec)

        simulator_control_resource = SimulatorControlResource(simulator)

        simulator_control_resource.execute_command("run_for", {"time_to_run": 1.0})

        start_time = simulator.simulation_time

        response = simulator_control_resource.execute_command("reset")

        self.assertDictEqual(response,
                            {"result": "ok",
                              "command": "reset"})

        self.assertAlmostEqual(simulator.simulation_time, fdmexec.GetSimTime(), 3)
        self.assertLess(simulator.simulation_time, start_time)

class AircraftResourceTests(TestCase):
    def test_get_aircraft_information(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        aircraft = Aircraft(fdmexec)

        resource = AircraftResource(aircraft)

        aircraft_data = resource.get()

        self.assertDictEqual(aircraft_data, {"type": "Rascal"})

class ObjectResourceTests(TestCase):
    def test_get_object_resource_data(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        accelerations = Accelerations(fdmexec)
        accelerations_schema = AccelerationsSchema()

        object_resource = ObjectResource(accelerations, accelerations_schema)

        response = object_resource.get()

        expected_result = {
            "x": accelerations.x,
            "y": accelerations.y,
            "z": accelerations.z,
            "p_dot": accelerations.p_dot,
            "q_dot": accelerations.q_dot,
            "r_dot": accelerations.r_dot,
            "u_dot": accelerations.u_dot,
            "v_dot": accelerations.v_dot,
            "w_dot": accelerations.w_dot,
            "gravity": accelerations.gravity
        }

        self.assertDictEqual(response, expected_result)

class AccelerationsResourceTests(TestCase):
    def test_get_accelerations(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        accelerations_resource = AccelerationsResource(fdmexec)

        response = accelerations_resource.get()

        accelerations = Accelerations(fdmexec)
        
        self.assertAlmostEqual(response["x"], accelerations.x, 3)
        self.assertAlmostEqual(response["y"], accelerations.y, 3)
        self.assertAlmostEqual(response["z"], accelerations.z, 3)
        self.assertAlmostEqual(response["p_dot"], accelerations.p_dot, 3)
        self.assertAlmostEqual(response["q_dot"], accelerations.q_dot, 3)
        self.assertAlmostEqual(response["r_dot"], accelerations.r_dot, 3)
        self.assertAlmostEqual(response["u_dot"], accelerations.u_dot, 3)
        self.assertAlmostEqual(response["v_dot"], accelerations.v_dot, 3)
        self.assertAlmostEqual(response["w_dot"], accelerations.w_dot, 3)
        self.assertAlmostEqual(response["gravity"], accelerations.gravity, 3)

class VelocitiesResourceTests(TestCase):
    def test_get_velocities(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        velocities_resource = VelocitiesResource(fdmexec)

        response = velocities_resource.get()

        velocities = Velocities(fdmexec)

        self.assertAlmostEqual(response["u"], velocities.u, 3)
        self.assertAlmostEqual(response["v"], velocities.v, 3)
        self.assertAlmostEqual(response["w"], velocities.w, 3)
        self.assertAlmostEqual(response["p"], velocities.p, 3)
        self.assertAlmostEqual(response["q"], velocities.q, 3)
        self.assertAlmostEqual(response["r"], velocities.r, 3)
        self.assertAlmostEqual(response["climb_rate"], velocities.climb_rate, 3)
        self.assertAlmostEqual(response["true_airspeed"], velocities.true_airspeed, 3)
        self.assertAlmostEqual(response["calibrated_airspeed"], velocities.calibrated_airspeed, 3)
        self.assertAlmostEqual(response["equivalent_airspeed"], velocities.equivalent_airspeed, 3)
        self.assertAlmostEqual(response["ground_speed"], velocities.ground_speed, 3)


class OrientationResourceTests(TestCase):
    def test_get_orientation_data(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        orientation_resource = OrientationResource(fdmexec)

        response = orientation_resource.get()

        orientation = Orientation(fdmexec)

        self.assertAlmostEqual(response["phi"], orientation.phi)
        self.assertAlmostEqual(response["theta"], orientation.theta)
        self.assertAlmostEqual(response["psi"], orientation.psi)


class AtmosphereResourceTests(TestCase):
    def test_get_atmospheric_data(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        atmosphere_resource = AtmosphereResource(fdmexec)

        response = atmosphere_resource.get()

        atmosphere = Atmosphere(fdmexec)

        self.assertAlmostEqual(response["pressure"], atmosphere.pressure)
        self.assertAlmostEqual(response["sea_level_pressure"], atmosphere.sea_level_pressure)
        self.assertAlmostEqual(response["temperature"], atmosphere.temperature)
        self.assertAlmostEqual(response["sea_level_temperature"], atmosphere.sea_level_temperature)
        self.assertAlmostEqual(response["density"], atmosphere.density)
        self.assertAlmostEqual(response["sea_level_density"], atmosphere.sea_level_density)
