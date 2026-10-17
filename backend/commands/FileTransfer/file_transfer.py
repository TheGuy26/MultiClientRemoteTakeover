import socket

from sender import send
from receiver import receive, receive_precheck
from backend.commandResponse import CommandResponse

class FileTransfer:
    host: socket.socket

    def __init__(self, host: socket.socket):
        self.host = host

    #def send(self, source_path: str, destination_path: str, file_name: str):
        #send(source_path=source_path, host=self.host, destination_path=destination_path, file_name=file_name)

    def receive_precheck(self, destination_path: str, file_size: int) -> CommandResponse:
        return receive_precheck(destination_path=destination_path, file_size=file_size)

    def receive(self, destination_path: str, file_size: int, file_name: str) -> CommandResponse:
        return receive(destination_path=destination_path, file_size=file_size,
                       file_name=file_name, host=self.host)