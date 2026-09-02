from typing import Callable
from backend.commandResponse import CommandResponse
from backend.commandRequest import CommandRequest


class Endpoint:
    uri: str
    endpoint: Callable[..., CommandResponse] # A callable that returns a CommandResponse
    basic: bool = True

    def __init__(self, uri: str, endpoint: Callable[..., CommandResponse], basic: bool = True):
        self.uri = uri
        self.endpoint = endpoint
        self.basic = basic

    def Call(self, request: CommandRequest) -> CommandResponse:
        if self.basic:
            return self.endpoint(request)
        return self.endpoint(**request.parameters)


