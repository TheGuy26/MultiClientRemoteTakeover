import socket

from backend.endpoint import Endpoint
from backend.api import API
from backend.commands.FileTransfer.client_file_transfer import FileTransfer
from backend.commands import commands

def set_api(host: socket.socket) -> API:

    # functions:
    file_transfer = FileTransfer(host)

    # endpoints:
    endpoints = [
        Endpoint(uri="receive", endpoint=file_transfer.receive, basic=False),
        Endpoint(uri="send", endpoint=file_transfer.send, basic=False),
        Endpoint(uri="run_command", endpoint=commands.run_command, basic=False)
    ]

    # API:
    api = API()
    for endpoint in endpoints:
        api.add(endpoint)
    return api