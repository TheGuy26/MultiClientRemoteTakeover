import time
from time import sleep
import socket
from threading import Thread, Event
from backend.commandRequest import CommandRequest
from backend.commandResponse import CommandResponse


class Client:
    ip: str
    port: int
    client_socket: socket.socket
    current_id: int = 1
    should_keep_alive: Event
    can_send_request: Event
    is_alive: bool = True
    running_thread: Thread

    def __init__(self, client_socket: socket.socket):
        client_address = client_socket.getpeername()
        self.ip = client_address[0]
        self.port = client_address[1]
        self.client_socket = client_socket
        self.current_id = 1
        self.is_alive = True
        self.should_keep_alive = Event()
        self.should_keep_alive.set()
        self.can_send_request = Event()
        self.running_thread = Thread(target=self.keep_alive, daemon=False)
        self.running_thread.start()

    def send_request(self, uri: str, parameters: dict) -> CommandResponse:
        self.can_send_request.wait()
        self.should_keep_alive.clear()
        command_request = CommandRequest(uri=uri, parameters=parameters, id=self.current_id)
        self.client_socket.sendall(command_request.dump())
        buffer = 8192 # Add BHP
        encoded_response = self.client_socket.recv(buffer)
        self.current_id += 1
        self.should_keep_alive.set()
        return CommandResponse.load(encoded_response)


    def keep_alive(self):
        while True:
            self.should_keep_alive.wait()
            self.can_send_request.clear()
            self.client_socket.sendall(b'Is alive?')
            try:
                self.client_socket.settimeout(5.0)
                message = self.client_socket.recv(1024)
            except socket.timeout:
                self.is_alive = False
                #Update GUI
                self.client_socket.close()
                break

            self.client_socket.settimeout(None)
            self.can_send_request.set()
            time.sleep(30.0)

