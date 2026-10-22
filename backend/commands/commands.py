import subprocess

from backend.commandResponse import CommandResponse

current_id = -1


def run_command(command: str) -> CommandResponse:
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    return CommandResponse(request_id=current_id, status_code=1, body=result.stdout) # Return standard output

def update_current_id(id: int):
    global current_id
    current_id = id

def get_current_id() -> int:
    return current_id

