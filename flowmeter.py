from alicat import FlowController

flow_controller = FlowController(port = "COM7", address = A)
print(flow_controller.get())