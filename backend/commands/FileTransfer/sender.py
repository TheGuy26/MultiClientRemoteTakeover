import socket
import pathlib
from queue import Queue
from threading import Thread

from backend.commandResponse import CommandResponse
from backend.client import Client

def transfer(source_path: str, host: socket.socket):
    queue: Queue[bytes] = Queue()
    parameters = {"source_path": source_path, "queue": queue}
    load_data_thread = Thread(target=load_file_data, kwargs=parameters, daemon=True)
    load_data_thread.start()
    send_file_data(host=host, queue=queue)


def load_file_data(source_path: str, queue: Queue[bytes]):
    file_path = pathlib.Path(source_path)
    chuck_size = 2048
    with file_path.open("rb") as file:
        is_finished = False
        while not is_finished:
            chunk = file.read(chuck_size)
            if not chunk:
                is_finished = True
            else:
                queue.put(chunk)
    queue.put(b'<end>')


def send_file_data(host: socket.socket, queue: Queue[bytes]):
    is_finished = False
    while not is_finished:
        if not queue.empty():
            data = queue.get()
            host.sendall(data)
            if data == b'<end>':
                is_finished = True

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

def master_send(source_path: str, host: Client, destination_path: str, file_name: str) -> CommandResponse:
    if not check_if_exists(source_path):
        return CommandResponse(request_id=host.current_id, status_code=2, body=f"Source path of {source_path} isn't a path or isn't a file.")
    file_size, file_extension = get_size(source_path), get_extension(source_path)
    parameters = {"destination_path": destination_path, "file_size": file_size,
                  "file_name": (file_name + file_extension)}
    check_response = host.send_request(uri="receive", parameters=parameters, continue_keeping_alive=False)
    if check_response.status_code != 1:
        host.continue_keeping_alive()
        return check_response
    transfer(source_path, host.client_socket)

    transfer_response = CommandResponse.load(host.client_socket.recv(2048))

    host.continue_keeping_alive()
    return transfer_response

def client_send(source_path: str, host: socket.socket) -> CommandResponse:
    request_id = get_request_id()
    if not check_if_exists(source_path=source_path):
        return CommandResponse(request_id=request_id, status_code=2,
                                     body=f"Source path of {source_path} doesn't exist or isn't a file")
    client_response = CommandResponse(request_id=request_id, status_code=1,
                                      body=f"{get_size(source_path)};{get_extension(source_path)}")
    host.sendall(client_response.dump())
    buffer = 2048
    master_response = CommandResponse.load(host.recv(buffer))
    if master_response.status_code == 1:
        transfer(source_path=source_path, host=host)
        master_response = CommandResponse.load(host.recv(buffer))
        if master_response.status_code != 1:
            return CommandResponse(request_id=request_id, status_code=2, body="Encountered errors at host machine.")
        return CommandResponse(request_id=request_id, status_code=1, body="file sent")
    return CommandResponse(request_id=request_id, status_code=2, body="file wasn't transferred do to host problems.")

def get_request_id() -> int:
    from client.management import get_current_id
    return get_current_id()


