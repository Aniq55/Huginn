from huginn.protocols import TelemetryDataListener

class MockAuxiliary(object):
    def __init__(self):
        self.v_true = 375.453302
        self.total_pressure = 12233.2
        self.euler_rates = [1.1, 2.2, 3.3]
        self.accelerations = [0.1, 0.2, 0.3]

    def GetVtrueFPS(self):
        return self.v_true

    def GetTotalPressure(self):
        return self.total_pressure

    def GetEulerRates(self, index):
        return self.euler_rates[index-1]

    def GetPilotAccel(self, index):
        return self.accelerations[index-1]

class MockEuler(object):
    def __init__(self):
        self.entries = [0.1, 0.2, 0.3]

    def Entry(self, index):
        return self.entries[index-1]

class MockPropagate(object):
    def __init__(self):
        self.latitude = 37.34567
        self.longitude = 21.63457
        self.altitude = 10000.0
        self.euler = MockEuler()

    def GetLatitudeDeg(self):
        return self.latitude

    def GetLongitudeDeg(self):
        return self.longitude

    def GetAltitudeASLmeters(self):
        return self.altitude

    def GetEuler(self):
        return self.euler

class MockFCS(object):
    def __init__(self):
        self.aileron_cmd = 0.55
        self.elevator_cmd = 0.23
        self.rudder_cmd = 0.7
        self.throttle_cmd  = 0.86

    def GetDaCmd(self):
        return self.aileron_cmd

    def GetDeCmd(self):
        return self.elevator_cmd

    def GetDrCmd(self):
        return self.rudder_cmd

    def GetThrottleCmd(self, index):
        return self.throttle_cmd

    def SetThrottleCmd(self, idex, throttle_cmd):
        self.throttle_cmd = throttle_cmd

    def SetDeCmd(self, elevator):
        self.elevator = elevator

    def SetDrCmd(self, rudder_cmd):
        self.rudder_cmd = rudder_cmd

    def SetDaCmd(self, aileron_cmd):
        self.aileron_cmd = aileron_cmd

class MockAtmosphere(object):
    def __init__(self):
        self.temperature = 567.32
        self.pressure = 456.39

    def GetTemperature(self):
        return self.temperature

    def GetPressure(self):
        return self.pressure

class MockThruster(object):
    def __init__(self):
        self.thrust = 3452.87

    def GetThrust(self):
        return self.thrust

class MockEngine(object):
    def __init__(self):
        self.thruster = MockThruster()
        self.throttle = 0.48

    def GetThruster(self):
        return self.thruster

class MockPropulsion(object):
    def __init__(self):
        self.engine = MockEngine()

    def GetEngine(self, index):
        return self.engine 

    def GetNumEngines(self):
        return 1

class MockFDMExec(object):
    def __init__(self):
        self.propagate = MockPropagate()
        self.auxiliary = MockAuxiliary()
        self.fcs = MockFCS()
        self.atmosphere = MockAtmosphere()
        self.propulsion = MockPropulsion()
        self.sim_time = 32.45
        self.dt = 1.0 / 60.0

        self.properties = {
            "simulation/sim-time-sec": self.sim_time,
            "atmosphere/P-psf": 456.39,
            "atmosphere/T-R": 567.32,
            "aero/qbar-psf": 12233.2,
            "velocities/p-rad_sec": 1.1,
            "velocities/q-rad_sec": 2.2,
            "velocities/r-rad_sec": 3.3,
            "attitude/heading-true-rad": 0.3,
            "position/long-gc-deg": 21.63457,
            "position/lat-gc-deg": 37.34567,
            "position/h-sl-ft": 32808.4,
            "velocities/vtrue-kts": 222.45,
            "propulsion/engine/thrust-lbs": 3452.87,
            "fcs/throttle-cmd-norm": 0.86,
            "fcs/rudder-cmd-norm": 0.7,
            "fcs/elevator-cmd-norm": 0.23,
            "fcs/aileron-cmd-norm": 0.55,
            "accelerations/a-pilot-x-ft_sec2": 0.1,
            "accelerations/a-pilot-y-ft_sec2": 0.2,
            "accelerations/a-pilot-z-ft_sec2": 0.3
        }

    def GetPropulsion(self):
        return self.propulsion

    def GetAtmosphere(self):
        return self.atmosphere

    def GetAuxiliary(self):
        return self.auxiliary

    def GetPropagate(self):
        return self.propagate

    def GetSimTime(self):
        return self.sim_time

    def GetDeltaT(self):
        return self.dt

    def GetFCS(self):
        return self.fcs

    def Resume(self):
        pass

    def RunIC(self):
        return True

    def Run(self):
        return True

    def ProcessMessage(self):
        pass

    def CheckIncrementalHold(self):
        pass

    def Hold(self):
        pass

    def GetPropertyValue(self, property_name):
        return self.properties[property_name]

class MockFDMModel(object):
    def __init__(self):
        self.properties = {"fcs/aileron-cmd-norm": 0.5555,
                           "fcs/elevator-cmd-norm": 0.6666,
                           "fcs/rudder-cmd-norm": 0x1111,
                           "propulsion/engine/engine-rpm": 2011.0,
                           "propulsion/engine/thrust-lbs": 750.0,
                           "propulsion/engine/power-hp": 27.0,
                           "fcs/throttle-cmd-norm": 0.76,
                           "position/lat-gc-deg": 23.34567,
                           "position/long-gc-deg": 45.65433,
                           "velocities/vtrue-kts": 65.3,
                           "position/h-sl-ft": 1200.35,
                           "attitude/heading-true-rad": 125.43,
                           "accelerations/a-pilot-x-ft_sec2": 12.34,
                           "accelerations/a-pilot-y-ft_sec2": 13.34,
                           "accelerations/a-pilot-z-ft_sec2": 14.34,
                           "velocities/p-rad_sec": 1.234,
                           "velocities/q-rad_sec": 2.234,
                           "velocities/r-rad_sec": 3.234,
                           "atmosphere/T-R": 12345.0,
                           "atmosphere/P-psf": 456.543,
                           "aero/qbar-psf": 12.88,
                           "attitude/roll-rad": 1.456,
                           "attitude/pitch-rad": 2.567,
                           "simulation/dt": 0.01,
                           "simulation/sim-time-sec": 100.2}
    
    def get_property_value(self, property_name):
        return self.properties[property_name]
    
    def set_property_value(self, property_name, value):
        pass
    
    def resume(self):
        pass

    def pause(self):
        pass

    def reset(self):
        pass

    def run(self):
        pass
    
class MockRequest(object):
    def __init__(self):
        self.args = {}

class MockTelemetryDataListener(TelemetryDataListener):
    def __init__(self):
        TelemetryDataListener.__init__(self)

    def received_telemetry_header(self, header):
        pass

    def received_telemetry_data(self, data):
        pass
