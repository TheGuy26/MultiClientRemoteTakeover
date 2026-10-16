import socket
import pathlib
import os
import shutil

from backend.commandResponse import CommandResponse

def load(destination_path: str, file_size: int, file_name: str, host: socket.socket):
    file_path = pathlib.Path(destination_path + '/' + file_name)
    buffer = 2048
    count = 0
    data = b''

    while count < file_size:
        data += host.recv(buffer)

    try:
        file_path.write_bytes(data)
    except OSError:
        pass # update GUI


def precheck(destination_path: str, file_size: int) -> bool:
    directory_path = pathlib.Path(destination_path)
    if not directory_path.is_dir():
        return False
    bites_left = shutil.disk_usage(directory_path).free
    if not bites_left > file_size + 1000:
        return False
    return True

def receive(destination_path: str, file_size: int, file_name: str, host: socket.socket) -> CommandResponse:
    if precheck(destination_path, file_size):
        host.sendall(b'1')
    else:
        host.sendall(b'2')
    load(destination_path, file_size, file_name, host)

    response = CommandResponse(request_id=0, status_code=1, body="ok")
    return response
