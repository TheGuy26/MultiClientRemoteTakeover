import socket

from backend.commands.FileTransfer.sender import client_send
from backend.commands.FileTransfer.receiver import client_receive, precheck
from backend.commandResponse import CommandResponse

class FileTransfer:
    host: socket.socket

    def __init__(self, host: socket.socket):
        self.host = host

    def send(self, source_path: str):
        client_send(source_path=source_path, host=self.host)

    #def receive_precheck(self, destination_path: str, file_size: int) -> CommandResponse:
        #return precheck(destination_path=destination_path, file_size=file_size)

    def receive(self, destination_path: str, file_size: int, file_name: str) -> CommandResponse:
        return client_receive(destination_path=destination_path, file_size=file_size,
                       file_name=file_name, host=self.host)