from commandRequest import CommandRequest
from commandResponse import CommandResponse
from endpoint import Endpoint


class API:
    endpoints: dict[str, Endpoint]

    def __init__(self):
        self.endpoints = dict()

    def add(self, endpoint: Endpoint):
        key = endpoint.uri
        if key not in self.endpoints.keys():
            self.endpoints[key] = endpoint
        else:
            raise ValueError(f"The endpoint with the uri of {key} is already present.")

    def remove(self, endpoint: Endpoint):
        key = endpoint.uri
        if key in self.endpoints.keys():
            del self.endpoints[key]
        else:
            raise ValueError(f"No endpoint with the uri of {key}.")

    def respond(self, request: CommandRequest) -> CommandResponse:
        key = request.uri
        if key not in self.endpoints.keys():
            return CommandResponse(request_id=request.id, status_code=404, body="Not Found")
        endpoint = self.endpoints[key]
        try:
            return endpoint.Call(request=request)
        except Exception:
            return CommandResponse(request_id=request.id, status_code=504, body="Internal Server Error")
