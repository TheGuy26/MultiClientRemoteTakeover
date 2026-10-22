import socket

from client import commands
from backend.api import API
from backend.commandRequest import CommandRequest
from backend.commandResponse import CommandResponse

current_request_id = -1

class Management:
    host: socket.socket
    api: API

    def __init__(self, ip: str, port: int):
        host = socket.socket()
        try:
            host.connect((ip, port))
        except OSError:
            raise RuntimeError(f"Couldn't connect to {ip}:{port}")
        print("Connected successfully")
        self.host = host
        self.api = commands.set_api(self.host)
        self.current_request_id = -1
        self.listen()

    def listen(self):
        buffer = 2048
        while True:
            message = self.host.recv(buffer)
            if message == b"Is alive?":
                self.host.sendall(b"I'm alive")
                continue
            command_request = CommandRequest.load(message)
            global current_request_id
            current_request_id = command_request.id
            command_response = self.api.respond(command_request)
            self.host.sendall(command_response.dump())


def get_current_id():
    return current_request_id