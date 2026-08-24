from CommandRequest import CommandRequest
from JsonConverter import JsonLoader

request = CommandRequest(uri="test", parameters={1: "first", 2: False})
print(request.dump().decode())

#print(CommandRequest.load(request.dump()))

test_2 = b'''{
\t"name": "Frieda",
\t"isDog": true,
\t"hobbies": ["eating", "sleeping", "barking"],
\t"age": 8,
\t"address": {
\t\t"work": null,
\t\t"home": ["Berlin", "Germany"]
\t},
\t"friends": [
\t\t{
\t\t\t"name": "Philipp",
\t\t\t"hobbies": ["eating", "sleeping", "reading"]
\t\t},
\t\t{
\t\t\t"name": "Mitch",
\t\t\t"hobbies": ["running", "snacking"]
\t\t}
\t]
}'''
print(JsonLoader.convert_dict(test_2))