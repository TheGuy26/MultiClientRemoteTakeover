from JsonConverter import JsonDumper
from JsonConverter import JsonLoader

class CommandResponse:
    request_id: int
    status_code: int
    body_type: str
    body: str # Change later

    def __init__(self, request_id: int, status_code: int, body_type: str, body: str = None):
        if body is None:
            body = "No Body"
        self.request_id = request_id
        self.status_code = status_code
        self.body_type = body_type
        self.body = body

    def dump(self) -> bytes:
        return JsonDumper.convert_custom_instance(instance=self)

    @staticmethod
    def load(command_response_json: bytes):
        decoded_dict = JsonLoader.convert_dict(command_response_json)
        attributes = {"request_id": int, "status_code": int, "body_type": str, "body": str} # Change body typing
        decoded_values = dict()
        for attr, attr_type in attributes.items():
            if attr in decoded_dict and isinstance(decoded_dict[attr], attr_type):
                decoded_values[attr] = decoded_dict[attr]
            else:
                raise ValueError(f"Couldn't cast item with the key of {attr}")
        return CommandResponse(request_id=decoded_values["request_id"], status_code=decoded_values["status_code"],
                               body_type=decoded_values["body_type"], body=decoded_values["body"])
