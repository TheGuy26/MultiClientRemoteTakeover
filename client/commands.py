import socket

from backend.endpoint import Endpoint
from backend.api import API
from backend.commands.FileTransfer.file_transfer import FileTransfer

def set_api(host: socket.socket) -> API:

    # functions:
    file_transfer = FileTransfer(host)

    # endpoints:
    endpoints = [
    Endpoint(uri="receive", endpoint=file_transfer.receive, basic=False)
    ]

    # API:
    api = API()
    for endpoint in endpoints:
        api.add(endpoint)
    return api