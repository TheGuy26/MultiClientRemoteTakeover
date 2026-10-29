import keyboard
from time import sleep

from backend.commandResponse import CommandResponse
from backend.commands.commands import get_current_id


def press_keys(keys_str: str) -> CommandResponse:
    key_list = keys_str.split()
    invalid_keys = list()
    for key in key_list:
        if is_valid_key(key=key):
            keyboard.send(key)
        else:
            invalid_keys.append(key)
    if invalid_keys:
        return CommandResponse(request_id=get_current_id(), status_code=2,
                               body=f"keys that couldn't be parsed:\n" + "\n".join(invalid_keys))
    return CommandResponse(request_id=get_current_id(), status_code=1, body="all keys were pressed")

def listen(timeout: str) -> CommandResponse:
    try:
        timeout = int(timeout)
    except ValueError:
        return CommandResponse(request_id=get_current_id(), status_code=2,
                               body=f"{timeout} is not a number")
    pressed_keys = list()

    def on_key_event(event: keyboard.KeyboardEvent):
        if event.event_type == keyboard.KEY_DOWN:
            pressed_keys.append(event.name)

    keyboard.hook(on_key_event)
    sleep(timeout)
    keyboard.unhook(on_key_event)
    if not pressed_keys:
        body = "no keys were pressed"
    else:
        body = "pressed keyes:\n" + "\n".join(pressed_keys)
    return CommandResponse(request_id=get_current_id(), status_code=1, body=body)


def is_valid_key(key: str) -> bool:
    try:
        keyboard.parse_hotkey(key)
        return True
    except ValueError:
        return False