import socket
import pathlib
import os
import shutil

from backend.commandResponse import CommandResponse

def load(destination_path: str, file_size: int, file_name: str, host: socket.socket) -> CommandResponse:
    file_path = pathlib.Path(destination_path + '/' + file_name)
    buffer = 2048
    done = False
    file_bytes = bytearray()

    while not done:
        data = host.recv(buffer)
        if data[-5:] != b'<end>':
            file_bytes += data

    try:
        file_path.write_bytes(file_bytes)
    except OSError:
        return CommandResponse(request_id=0, status_code=2, body="Couldn't load or write file to destination.") # update GUI
    return CommandResponse(request_id=0, status_code=1, body="ok")

def precheck(destination_path: str, file_size: int) -> CommandResponse:
    directory_path = pathlib.Path(destination_path)
    if not directory_path.is_dir(): # Path is not a directory
        return CommandResponse(request_id=0, status_code=2, body=f"Destination path of {destination_path} doesn't exist or isn't a directory")
    bites_left = shutil.disk_usage(directory_path).free
    if not bites_left > file_size + 5 * 10**8: # file size + 0.5 GB
        return CommandResponse(request_id=0, status_code=3, body=f"Not enough space on destination directory")
    return CommandResponse(request_id=0, status_code=1, body=f"ok")

def receive(destination_path: str, file_size: int, file_name: str, host: socket.socket) -> CommandResponse:
    precheck_response = precheck(destination_path=destination_path, file_size=file_size)
    if precheck_response.status_code != 1:
        return precheck_response
    host.sendall(precheck_response.dump())
    return load(destination_path, file_size, file_name, host)


