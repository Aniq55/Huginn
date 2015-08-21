import struct
from unittest import TestCase
from os import path
import inspect

from flightsimlib import FGFDMExec
from mock import MagicMock, ANY

import huginn
from huginn.protocols import FDMDataProtocol, FDMDataRequest, FDMDataResponse, FDM_DATA_PROTOCOL_PROPERTIES, ACCELEROMETER_DATA
from huginn.fdm import fdm_data_properties

def get_fdmexec():
    package_filename = inspect.getfile(huginn)
    package_path = path.dirname(package_filename)
    
    fdmexec = FGFDMExec()
    
    fdmexec.set_root_dir(package_path + "/data/")
    fdmexec.set_aircraft_path("aircraft")
    fdmexec.set_engine_path("engine")
    fdmexec.set_systems_path("systems")

    fdmexec.set_dt(1.0/60.0)

    fdmexec.load_model("c172p")

    fdmexec.load_ic("reset01")

    fdmexec.set_property_value("fcs/throttle-cmd-norm", 0.65)
    fdmexec.set_property_value("fcs/mixture-cmd-norm", 0.87)
    fdmexec.set_property_value("propulsion/magneto_cmd", 3.0)
    fdmexec.set_property_value("propulsion/starter_cmd", 1.0)

    initial_condition_result = fdmexec.run_ic()

    if not initial_condition_result:
        print("Failed to run initial condition")
        exit(-1)

    running = fdmexec.run()
    while running and fdmexec.get_sim_time() < 0.1:
        fdmexec.process_message()
        fdmexec.check_incremental_hold()

        running = fdmexec.run()
        
    result = fdmexec.trim()    
    if not result:
        print("Failed to trim the aircraft")
        exit(-1)
        
    return fdmexec

class FDMDataProtocolTests(TestCase):
    def test_decode_request(self):
        fdmexec = get_fdmexec()
        
        fdm_data_protocol = FDMDataProtocol(fdmexec)
        
        request_datagram = struct.pack("!c", chr(0x3f))
        host = "127.0.0.1"
        port = 12345
        
        request = fdm_data_protocol.decode_request(request_datagram, host, port)
        
        self.assertIsInstance(request, FDMDataRequest)
        self.assertEqual(request.host, host)
        self.assertEqual(request.port, port)
        self.assertEqual(request.command, 0x3f)
            
    def test_datagramReceived(self):
        fdmexec = get_fdmexec()
        
        fdm_data_protocol = FDMDataProtocol(fdmexec)
        
        host = "127.0.0.1"
        port = 12345
        
        fdm_data_protocol.transmit_datagram = MagicMock()
        
        fdm_data_request_datagram = struct.pack("!c", chr(ACCELEROMETER_DATA))
        
        fdm_data_protocol.datagramReceived(fdm_data_request_datagram, (host, port))
        
        fdm_property_values = [fdmexec.get_property_value(fdm_property) for fdm_property in FDM_DATA_PROTOCOL_PROPERTIES[ACCELEROMETER_DATA]]
        fdm_property_value_count = len(fdm_property_values)
        
        expected_responce_datagram = struct.pack("!c" + ("f" * fdm_property_value_count), chr(ACCELEROMETER_DATA), *fdm_property_values)
        
        fdm_data_protocol.transmit_datagram.assert_called_once_with(expected_responce_datagram, host, port)