"""
The huginn.servers module contains classes that can be used to create
a simulator that transmits and receives data from/to the network
"""
import logging
import pkg_resources

from twisted.internet import reactor
from twisted.web import server
from twisted.web.static import File
from twisted.internet.task import LoopingCall

from huginn import configuration
from huginn.http import GPSData, AccelerometerData,\
                        GyroscopeData, ThermometerData, PressureSensorData,\
                        PitotTubeData, InertialNavigationSystemData,\
                        EngineData, FlightControlsData, SimulatorControl,\
                        FDMData, AircraftIndex, MapData
from huginn.protocols import ControlsProtocol, FDMDataProtocol,\
                             SensorDataFactory

class SimulationServer(object):
    """This class is the network front-end for the simulator. It will create
    and initialize the interfaces that can be used to control and receive
    simulation data."""
    def __init__(self, simulator):
        self.simulator = simulator
        self.fdm = simulator.fdm
        self.aircraft = simulator.aircraft
        self.dt = simulator.fdm.get_dt()
        self.controls_port = configuration.CONTROLS_PORT
        self.fdm_clients = []
        self.web_server_port = configuration.WEB_SERVER_PORT
        self.sensors_port = configuration.SENSORS_PORT
        self.logger = logging.getLogger("huginn")

    def _initialize_web_server(self):
        """Initialize the web server"""
        self.logger.debug("Starting web server at port %d", self.web_server_port)

        root = File(pkg_resources.resource_filename("huginn", "/static"))  # @UndefinedVariable

        aircraft_root = AircraftIndex()

        aircraft_root.putChild("gps", GPSData(self.aircraft))
        aircraft_root.putChild("accelerometer", AccelerometerData(self.aircraft))
        aircraft_root.putChild("gyroscope", GyroscopeData(self.aircraft))
        aircraft_root.putChild("thermometer", ThermometerData(self.aircraft))
        aircraft_root.putChild("pressure_sensor", PressureSensorData(self.aircraft))
        aircraft_root.putChild("pitot_tube", PitotTubeData(self.aircraft))
        aircraft_root.putChild("ins", InertialNavigationSystemData(self.aircraft))
        aircraft_root.putChild("engine", EngineData(self.aircraft))
        aircraft_root.putChild("flight_controls", FlightControlsData(self.aircraft))

        root.putChild("aircraft", aircraft_root)
        root.putChild("simulator", SimulatorControl(self.simulator))
        root.putChild("fdm", FDMData(self.fdm, self.aircraft))
        root.putChild("map", MapData())

        frontend = server.Site(root)

        reactor.listenTCP(self.web_server_port, frontend)  # @UndefinedVariable

    def _initialize_controls_server(self):
        """Initialize the controls server"""
        self.logger.debug("Starting aircraft controls server at port %d",
                     self.controls_port)

        controls_protocol = ControlsProtocol(self.fdm)

        reactor.listenUDP(self.controls_port, controls_protocol)  # @UndefinedVariable

    def _initialize_fdm_data_server(self):
        """Initialize the fdm data server"""
        for fdm_client in self.fdm_clients:
            client_address, client_port, dt = fdm_client
            self.logger.debug("Sending fdm data to %s:%d", client_address, client_port)

            fdm_data_protocol = FDMDataProtocol(self.fdm, self.aircraft, client_address, client_port)

            reactor.listenUDP(0, fdm_data_protocol)  # @UndefinedVariable

            fdm_data_updater = LoopingCall(fdm_data_protocol.send_fdm_data)
            fdm_data_updater.start(dt)

    def _run_simulator(self):
        result = self.simulator.run()

        if not result:
            self.logger.error("The simulator has failed to run")
            reactor.stop()  # @UndefinedVariable

    def _initialize_simulator_updater(self):
        fdm_updater = LoopingCall(self._run_simulator)
        fdm_updater.start(self.dt)

    def _initialize_sensors_server(self):
        self.logger.debug("Starting the sensor server at port %d", self.sensors_port)

        sensor_data_factory = SensorDataFactory(self.aircraft)

        reactor.listenTCP(self.sensors_port, sensor_data_factory)  # @UndefinedVariable

    def start(self):
        """Start the simulator server"""
        self._initialize_controls_server()
        self._initialize_fdm_data_server()
        self._initialize_web_server()
        self._initialize_sensors_server()
        self._initialize_simulator_updater()

        self.logger.info("Starting the simulator server")
        reactor.run()  # @UndefinedVariable
        self.logger.info("The simulator server has stopped")

    def stop(self):
        """Stop the simulator server"""
        self.logger.info("Shutting down the simulator server")
        reactor.stop()  # @UndefinedVariable
