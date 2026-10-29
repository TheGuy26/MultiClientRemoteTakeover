import socket
from mss import MSS
from mss.tools import to_png
from os.path import join

from backend.commandResponse import CommandResponse
from backend.commands.commands import get_current_id
from backend.client import Client
from backend.commands.FileTransfer.receiver import precheck

class ClientScreenshot:
    host: socket.socket

    def __init__(self, host: socket.socket):
        self.host = host

    def client_send(self) -> CommandResponse:
        with MSS() as sct:
            all_monitors = sct.monitors[0]
            screenshot = sct.grab(all_monitors)

        request_id = get_current_id()
        size_response = CommandResponse(request_id=request_id, status_code=1,
                                        body=f"{len(screenshot.rgb)};{screenshot.width};{screenshot.height}")
        self.host.sendall(size_response.dump())
        buffer = 2048
        master_response = CommandResponse.load(self.host.recv(buffer))
        if master_response.status_code == 1:
            self.host.sendall(screenshot.rgb + b'<end>')
            master_response = CommandResponse.load(self.host.recv(buffer))
            if master_response.status_code != 1:
                return CommandResponse(request_id=request_id, status_code=2, body="Encountered errors at host machine.")
            return CommandResponse(request_id=request_id, status_code=1, body="screenshot sent")
        return CommandResponse(request_id=request_id, status_code=2, body="screenshot wasn't transferred do to host problems.")

def master_receive(host: Client, destination_path: str, file_name: str):
    host.send_request(uri="screenshot", continue_keeping_alive=False)
    buffer = 2048
    seperator = ';'
    file_size, width, height = CommandResponse.load(host.client_socket.recv(buffer)).body.split(seperator, maxsplit= 2)
    dimensions = (int(height), int(width))
    master_precheck_response = precheck(destination_path=destination_path, file_size=int(file_size))
    if master_precheck_response.status_code != 1:
        return master_precheck_response
    response = load_image(dimensions=dimensions, destination_path=destination_path,
                          file_name=file_name + '.png', host=host.client_socket)
    host.client_socket.sendall(response.dump())
    host.client_socket.recv(buffer)  # Client has to return a response

    host.continue_keeping_alive()
    return response

def load_image(dimensions: tuple[int, int], destination_path: str, file_name: str, host: socket.socket) -> CommandResponse:
    buffer = 8192
    done = False
    screenshot_rgb = bytearray()

    while not done:
        data = host.recv(buffer)
        screenshot_rgb += data
        if data[-5:] == b'<end>':
            del screenshot_rgb[-5:]
            done = True

    try:
        full_path = join(destination_path, file_name)
        to_png(screenshot_rgb,
               dimensions,
               output=full_path)
    except Exception:
        return CommandResponse(request_id=get_current_id(), status_code=2, body="Couldn't load or write screenshot to destination.") # update GUI
    return CommandResponse(request_id=get_current_id(), status_code=1, body="ok")


