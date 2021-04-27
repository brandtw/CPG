from alicat import FlowController

flow_controller = FlowController.is_connected(port='COM4')
print(flow_controller)