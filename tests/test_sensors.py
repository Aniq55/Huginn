import math
from unittest import TestCase

from huginn import configuration
from huginn.unit_conversions import convert_feet_to_meters, convert_rankine_to_kelvin,\
                                    convert_psf_to_pascal
from huginn.fdm import FDMBuilder
from huginn.sensors import Sensors, Accelerometer, Gyroscope, Thermometer,\
                           PressureSensor, PitotTube, InertialNavigationSystem

class AccelerometerTests(TestCase):
    def test_accelerometer(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        accelerometer = Accelerometer(fdmexec)

        self.assertAlmostEqual(accelerometer.true_x, convert_feet_to_meters(fdmexec.GetAuxiliary().GetPilotAccel(1)), 3)
        self.assertAlmostEqual(accelerometer.true_y, convert_feet_to_meters(fdmexec.GetAuxiliary().GetPilotAccel(2)), 3)
        self.assertAlmostEqual(accelerometer.true_z, convert_feet_to_meters(fdmexec.GetAuxiliary().GetPilotAccel(3)), 3)

        self.assertAlmostEqual(accelerometer.x, accelerometer.true_x + accelerometer.bias + accelerometer.measurement_noise, 3)
        self.assertAlmostEqual(accelerometer.y, accelerometer.true_y + accelerometer.bias + accelerometer.measurement_noise, 3)
        self.assertAlmostEqual(accelerometer.z, accelerometer.true_z + accelerometer.bias + accelerometer.measurement_noise, 3)

    def test_accelerometer_bias_and_noise_modification_updates(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        accelerometer = Accelerometer(fdmexec)

        accelerometer._measurement_noise = 0.0

        fdmexec.Run()
        
        self.assertEqual(accelerometer.measurement_noise, 0.0)

        #make sure the model is not paused
        fdmexec.Resume()

        run_until = fdmexec.GetSimTime() + (1.0/accelerometer.update_rate) + 1.0
        while fdmexec.GetSimTime() < run_until:
            fdmexec.Run()

        self.assertAlmostEqual(accelerometer.x, accelerometer.true_x + accelerometer.bias + accelerometer.measurement_noise, 3)
        self.assertAlmostEqual(accelerometer.y, accelerometer.true_y + accelerometer.bias + accelerometer.measurement_noise, 3)
        self.assertAlmostEqual(accelerometer.z, accelerometer.true_z + accelerometer.bias + accelerometer.measurement_noise, 3)

        self.assertNotEqual(accelerometer.measurement_noise, 0.0)

class GyroscopeTests(TestCase):
    def test_gyroscope(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        gyroscope = Gyroscope(fdmexec)

        self.assertAlmostEqual(gyroscope.true_roll_rate, math.degrees(fdmexec.GetAuxiliary().GetEulerRates(1)), 3)
        self.assertAlmostEqual(gyroscope.true_pitch_rate, math.degrees(fdmexec.GetAuxiliary().GetEulerRates(2)), 3)
        self.assertAlmostEqual(gyroscope.true_yaw_rate, math.degrees(fdmexec.GetAuxiliary().GetEulerRates(3)), 3)

        self.assertAlmostEqual(gyroscope.roll_rate, gyroscope.true_roll_rate + gyroscope.roll_rate_bias + gyroscope.roll_rate_measurement_noise, 3)
        self.assertAlmostEqual(gyroscope.pitch_rate, gyroscope.true_pitch_rate + gyroscope.pitch_rate_bias + gyroscope.pitch_rate_measurement_noise, 3)
        self.assertAlmostEqual(gyroscope.yaw_rate, gyroscope.true_yaw_rate + gyroscope.yaw_rate_bias + gyroscope.yaw_rate_measurement_noise, 3)

    def test_gyroscope_bias_and_measurement_noise_update(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        gyroscope = Gyroscope(fdmexec)

        gyroscope._roll_rate_measurement_noise = 0.0

        fdmexec.Run()

        self.assertEqual(gyroscope._roll_rate_measurement_noise, 0.0)

        run_until = fdmexec.GetSimTime() + (1.0/gyroscope.update_rate) + 1.0
        while fdmexec.GetSimTime() < run_until:
            fdmexec.Run()

        self.assertNotEqual(gyroscope.roll_rate_measurement_noise, 0.0)

class ThermometerTests(TestCase):
    def test_thermometer(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        thermometer = Thermometer(fdmexec)

        self.assertAlmostEqual(thermometer.true_temperature, convert_rankine_to_kelvin(fdmexec.GetAtmosphere().GetTemperature()))
        self.assertAlmostEqual(thermometer.temperature, thermometer.true_temperature + thermometer.measurement_noise)

    def test_thermometer_meaurement_noise_update(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        thermometer = Thermometer(fdmexec)

        thermometer._measurement_noise = 0.0

        fdmexec.Run()
        
        self.assertEqual(thermometer._measurement_noise, 0.0)
        self.assertEqual(thermometer.measurement_noise, 0.0)

        run_until = fdmexec.GetSimTime() + (1.0/thermometer.update_rate) + 1.0
        while fdmexec.GetSimTime() < run_until:
            fdmexec.Run()

        self.assertNotEqual(thermometer.measurement_noise, 0.0)
        self.assertNotEqual(thermometer._measurement_noise, 0.0)

class PressureSensorTests(TestCase):
    def test_presure_sensor(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        pressure_sensor = PressureSensor(fdmexec)

        self.assertAlmostEqual(pressure_sensor.pressure, convert_psf_to_pascal(fdmexec.GetAtmosphere().GetPressure()))

class PitotTubeTests(TestCase):
    def test_pitot_tube(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        pitot_tube = PitotTube(fdmexec)

        self.assertAlmostEqual(pitot_tube.pressure, convert_psf_to_pascal(fdmexec.GetAuxiliary().GetTotalPressure()))

class InertialNavigationSystemTests(TestCase):
    def test_inertialNavigationSystem(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        ins = InertialNavigationSystem(fdmexec)

        self.assertAlmostEqual(ins.roll, fdmexec.GetPropagate().GetEulerDeg(1))
        self.assertAlmostEqual(ins.pitch, fdmexec.GetPropagate().GetEulerDeg(2))
        self.assertAlmostEqual(ins.latitude, fdmexec.GetPropagate().GetLatitudeDeg())
        self.assertAlmostEqual(ins.longitude, fdmexec.GetPropagate().GetLongitudeDeg())
        self.assertAlmostEqual(ins.altitude, fdmexec.GetPropagate().GetAltitudeASLmeters())
        self.assertAlmostEqual(ins.airspeed, convert_feet_to_meters(fdmexec.GetAuxiliary().GetVtrueFPS()))
        self.assertAlmostEqual(ins.heading, math.degrees(fdmexec.GetPropagate().GetEuler(3)))

class SensorTests(TestCase):
    def test_accelerometer(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        sensors = Sensors(fdmexec)

        self.assertAlmostEqual(sensors.accelerometer.true_x, convert_feet_to_meters(fdmexec.GetAuxiliary().GetPilotAccel(1)))
        self.assertAlmostEqual(sensors.accelerometer.true_y, convert_feet_to_meters(fdmexec.GetAuxiliary().GetPilotAccel(2)))
        self.assertAlmostEqual(sensors.accelerometer.true_z, convert_feet_to_meters(fdmexec.GetAuxiliary().GetPilotAccel(3)))

    def test_gyroscope(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        sensors = Sensors(fdmexec)

        self.assertAlmostEqual(sensors.gyroscope.true_roll_rate, math.degrees(fdmexec.GetAuxiliary().GetEulerRates(1)))
        self.assertAlmostEqual(sensors.gyroscope.true_pitch_rate, math.degrees(fdmexec.GetAuxiliary().GetEulerRates(2)))
        self.assertAlmostEqual(sensors.gyroscope.true_yaw_rate, math.degrees(fdmexec.GetAuxiliary().GetEulerRates(3)))

    def test_thermometer(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        sensors = Sensors(fdmexec)

        self.assertAlmostEqual(sensors.thermometer.true_temperature, convert_rankine_to_kelvin(fdmexec.GetAtmosphere().GetTemperature()))

    def test_presure_sensor(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        sensors = Sensors(fdmexec)

        self.assertAlmostEqual(sensors.pressure_sensor.pressure, convert_psf_to_pascal(fdmexec.GetAtmosphere().GetPressure()))

    def test_pitot_tube(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        sensors = Sensors(fdmexec)

        self.assertAlmostEqual(sensors.pitot_tube.pressure, convert_psf_to_pascal(fdmexec.GetAuxiliary().GetTotalPressure()))

    def test_inertialNavigationSystem(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        sensors = Sensors(fdmexec)

        self.assertAlmostEqual(sensors.inertial_navigation_system.roll, fdmexec.GetPropagate().GetEulerDeg(1))
        self.assertAlmostEqual(sensors.inertial_navigation_system.pitch, fdmexec.GetPropagate().GetEulerDeg(2))
        self.assertAlmostEqual(sensors.inertial_navigation_system.latitude, fdmexec.GetPropagate().GetLatitudeDeg())
        self.assertAlmostEqual(sensors.inertial_navigation_system.longitude, fdmexec.GetPropagate().GetLongitudeDeg())
        self.assertAlmostEqual(sensors.inertial_navigation_system.altitude, fdmexec.GetPropagate().GetAltitudeASLmeters())
        self.assertAlmostEqual(sensors.inertial_navigation_system.airspeed, convert_feet_to_meters(fdmexec.GetAuxiliary().GetVtrueFPS()))
        self.assertAlmostEqual(sensors.inertial_navigation_system.heading, math.degrees(fdmexec.GetPropagate().GetEuler(3)))
