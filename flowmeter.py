import alicat
import serial
A is air (19200), C is decane (5120), B is propane(3213), D is nitrogen (36)
flow_controller = alicat.FlowController(port = "COM4", address = "B")
command = '{addr}{setpoint}\r'.format(addr="B", setpoint=1000.239458)
flow_controller._test_controller_open()
retries = 2
line = flow_controller._write_and_read(command, retries)