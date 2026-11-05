import socket
from threading import Thread
from typing import Callable

from backend.client import Client
from backend.database import Database

class ClientManagement:
    clients: dict[str, Client] # ip as key
    server_socket: socket.socket
    running_thread: Thread

    database: Database

    add_to_frontend: Callable
    disable_client_gui: Callable

    def __init__(self, ip: str, port: int, add_to_frontend: Callable, disable_client_gui: Callable):
        self.clients = dict()
        self.running_thread = Thread(target=self.listen, daemon=False) # Change to True
        self.server_socket = socket.socket()
        try:
            self.server_socket.bind((ip, port))
        except OSError:
            raise ValueError(f"Server couldn't bind to address ({ip}, {port})")
        self.running_thread.start()

        self.database = Database(name="database.db")

        self.add_to_frontend = add_to_frontend
        self.disable_client_gui = disable_client_gui

    def listen(self):
        self.server_socket.listen()
        while True:
            client_socket, client_address = self.server_socket.accept()
            client = Client(client_socket=client_socket, database=self.database, update_gui=self.disable_client_gui)
            self.clients[client_address[0]] = client
            self.add_to_frontend(ip=client_address[0], port=client_address[1])


    def get_client(self, ip: str) -> Client:
        if ip in self.clients.keys():
            return self.clients[ip]
        raise ValueError(f"Client with the ip of {ip} couldn't be found.")


