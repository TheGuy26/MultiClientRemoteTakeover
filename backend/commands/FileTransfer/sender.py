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
    file_path = pathlib.Path(source_path) # add try, except
    if not file_path.is_file():  # Check if the path is a file
        return False
    return True

def get_size(source_path: str) -> int:
    file_path = pathlib.Path(source_path)
    return file_path.stat().st_size # Return file size


def get_extension(source_path: str) -> str:
    file_path = pathlib.Path(source_path)
    return file_path.suffix  # Return file extension

def master_send(source_path: str, host: Client, destination_path: str, file_name: str):
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

def client_send(source_path: str, host: socket.socket) -> CommandResponse:
    if not check_if_exists(source_path=source_path):
        return CommandResponse(request_id=1, status_code=2,
                                     body=f"Source path of {source_path} doesn't exist or isn't a file")
    client_response = CommandResponse(request_id=1, status_code=1,
                                      body=f"{get_size(source_path)};{get_extension(source_path)}")
    host.sendall(client_response.dump())
    buffer = 2048
    master_response = CommandResponse.load(host.recv(buffer))
    if master_response.status_code == 1:
        transfer(source_path=source_path, host=host)
        master_response = CommandResponse.load(host.recv(buffer))
        if master_response.status_code != 1:
            return CommandResponse(request_id=1, status_code=2, body="Encountered errors at host machine.")
        return CommandResponse(request_id=1, status_code=1, body="Sent file")
    return CommandResponse(request_id=1, status_code=2, body="file wasn't transferred do to host problems.")



