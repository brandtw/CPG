import alicat
# A is air (19200), C is decane (5120), B is propane(3213), D is nitrogen (36)
flow_controller = alicat.FlowController(port = "COM7", address = "D")
# command = '{addr}$${setpoint:.2f}\r'.format(addr="D", setpoint=10.00)
# flow_controller._write_and_read(command)
print(flow_controller.get())