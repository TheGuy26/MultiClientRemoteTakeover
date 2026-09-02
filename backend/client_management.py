import socket
from threading import Thread

from backend.client import Client

class ClientManagement:
    clients: set[Client]
    server_socket: socket.socket
    running_thread: Thread

    def __init__(self, ip: str, port: int):
        self.clients = set()
        self.running_thread = Thread(target=self.listen, daemon=False) # Change to True
        self.server_socket = socket.socket()
        try:
            self.server_socket.bind((ip, port))
        except OSError:
            raise ValueError(f"Server couldn't bind to address ({ip}, {port})")
        self.running_thread.start()

    def listen(self):
        self.server_socket.listen()
        while True:
            client_socket = self.server_socket.accept()[0]
            client = Client(client_socket=client_socket)
            self.clients.add(client)

