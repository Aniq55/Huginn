import logging
from argparse import ArgumentParser
import signal
import os

from twisted.internet.error import CannotListenError
from twisted.internet import reactor
from twisted.internet.task import LoopingCall

from huginn import configuration
from huginn.simulator import Simulator
from huginn.validators import port_number, fdm_data_endpoint, telemetry_endpoint
from huginn.fdm import create_fdmexec
from huginn.aircraft import Aircraft
from huginn.servers import SimulationServer
from huginn.console import SimulatorStatePrinter

def get_arguments():
    parser = ArgumentParser(description="Huginn flight simulator")

    parser.add_argument("--dt", action="store", type=float, default=configuration.DT, help="The simulation timestep")
    
    parser.add_argument("--telemetry", 
                        action="store", 
                        type=telemetry_endpoint, 
                        default="%s,%f" % (configuration.TELEMETRY_PORT,
                                           configuration.TELEMETRY_DT),
                        help="The telemetry endpoint")
    
    parser.add_argument("--web", action="store", type=port_number, default=configuration.WEB_SERVER_PORT, help="The web server port")
    
    parser.add_argument("--fdm",
                        action="store",
                        type=fdm_data_endpoint,
                        default="%s,%d,%f" % (configuration.FDM_CLIENT_ADDRESS, configuration.FDM_CLIENT_PORT, configuration.FDM_CLIENT_DT), 
                        help="The fdm data endpoint")
    
    parser.add_argument("--controls", action="store", type=port_number, default=configuration.CONTROLS_PORT, help="The controls port")
    parser.add_argument("jsbsim", action="store", help="The path to jsbsim source code")
    parser.add_argument("script", action="store", help="The script to load")

    return parser.parse_args()

def main():
    logging.basicConfig(format="%(asctime)s - %(module)s:%(levelname)s:%(message)s",
                        filename="huginn.log",
                        filemode="a",
                        level=logging.DEBUG)

    logging.info("Starting the Huginn flight simulator")

    args = get_arguments()

    jsbsim_path = args.jsbsim

    fdmexec = create_fdmexec(jsbsim_path, args.script, args.dt)

    if not fdmexec:
        logging.error("Failed to create flight model")
        print("Failed to create flight model")
        exit(-1)

    aircraft = Aircraft(fdmexec)

    simulator = Simulator(fdmexec, aircraft)

    simulator_state_printer = SimulatorStatePrinter()
    simulator.add_simulator_event_listener(simulator_state_printer)

    fdm_client_address, fdm_client_port, fdm_client_update_rate = args.fdm 

    telemetry_port, telemetry_update_rate = args.telemetry

    simulator_server = SimulationServer(simulator)

    simulator_server.fdm_client_address = fdm_client_address
    simulator_server.fdm_client_port = fdm_client_port
    simulator_server.fdm_client_update_rate = fdm_client_update_rate

    simulator_server.telemetry_port = telemetry_port
    simulator_server.telemetry_update_rate = telemetry_update_rate

    simulator_server.controls_port = args.controls
    
    simulator_server.web_server_port = args.web

    simulator_server.start()

if __name__ == "__main__":
    main()
