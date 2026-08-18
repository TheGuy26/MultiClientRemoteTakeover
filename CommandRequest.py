import JsonConvertor

class CommandRequest:
    endpoint: str # Endpoint, need to add later
    parameters: dict
    id: int

    def __init__(self, endpoint: str, parameters: dict):
        self.endpoint = endpoint
        self.parameters = parameters
        self.id = 0 # need to link to database

    def dump(self) -> bytes:
        return JsonConvertor.convert_custom_instance(self)

