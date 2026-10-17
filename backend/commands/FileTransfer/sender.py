import socket
import pathlib

from backend.commandResponse import CommandResponse
from backend.client import Client

def transfer(source_path: str, host: socket.socket):
        file_path = pathlib.Path(source_path)
        buffer = 1024
        file_data = file_path.read_bytes()
        host.sendall(file_data + b'<end>')

def check_if_exists(source_path: str) -> bool:
    file_path = pathlib.Path(source_path)
    if not file_path.is_file():  # Check if the path is a file
        return False
    return True

def get_size(source_path: str) -> int:
    file_path = pathlib.Path(source_path)
    return file_path.stat().st_size # Return file size


def get_extension(source_path: str) -> str:
    file_path = pathlib.Path(source_path)
    return file_path.suffix  # Return file extension

def send(source_path: str, host: Client, destination_path: str, file_name: str):
    if not check_if_exists(source_path):
        return # update GUI
    file_size, file_extension = get_size(source_path), get_extension(source_path)
    parameters = {"destination_path": destination_path, "file_size": file_size,
                  "file_name": (file_name + file_extension)}
    check_response = host.send_request(uri="receive", parameters=parameters, continue_keeping_alive=False)
    if check_response.status_code != 1:
        host.continue_keeping_alive()
        return # update GUI
    transfer(source_path, host.client_socket)

    transfer_response = CommandResponse.load(host.client_socket.recv(2048))

    host.continue_keeping_alive()
    return # update GUI

