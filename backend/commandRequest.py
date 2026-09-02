from backend.JsonConverter import jsonDumper
from backend.JsonConverter import jsonLoader

class CommandRequest:
    uri: str
    parameters: dict
    id: int

    def __init__(self, uri: str, parameters: dict, id: int = 0):
        self.uri = uri
        self.parameters = parameters
        self.id = id

    def dump(self) -> bytes:
        return jsonDumper.convert_custom_instance(instance=self)

    @staticmethod
    def load(command_request_json: bytes) -> "CommandRequest":
        decoded_dict = jsonLoader.convert_dict(command_request_json)
        attributes = {"uri": str, "parameters": dict, "id": int}
        decoded_values = dict()
        for attr, attr_type in attributes.items():
            if attr in decoded_dict and isinstance(decoded_dict[attr], attr_type):
                decoded_values[attr] = decoded_dict[attr]
            else:
                raise ValueError(f"Couldn't cast item with the key of {attr}")
        return CommandRequest(uri=decoded_values["uri"], parameters=decoded_values["parameters"], id=decoded_values["id"])

