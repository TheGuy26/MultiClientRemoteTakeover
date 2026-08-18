from CommandRequest import CommandRequest

request = CommandRequest(endpoint="test", parameters={1: "first", 2: False})
print(request.dump().decode())