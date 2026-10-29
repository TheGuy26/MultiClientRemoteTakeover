from pynput.mouse import Controller, Button

from backend.commandResponse import CommandResponse
from backend.commands.commands import get_current_id


def control(action_str: str):
    mouse = Controller()
    action_list = action_str.split()
    invalid_actions = list()
    for action in action_list:
        if len(action) >= 1 and action[-1] == ')':
            try:
                coordinates = find_coordinates(action)
            except ValueError:
                invalid_actions.append(action)
                continue

            if len(action) >= 3 and action[:3] == "set":
                mouse.position = coordinates
            elif len(action) >= 4 and action[:4] == "move":
                mouse.move(*coordinates)
            else:
                invalid_actions.append(action)

        elif action == "left":
            mouse.click(Button.left)
        elif action == "right":
            mouse.click(Button.right)
        elif action == "middle":
            mouse.click(Button.middle)
        else:
            invalid_actions.append(action)

    body = f"current location - {mouse.position}"
    if invalid_actions:
        body += "\ninvalid actions:\n" + "\n".join(invalid_actions)

    return CommandResponse(request_id=get_current_id(), status_code=1, body=body)


def find_coordinates(action: str) -> tuple[int, int]:
    if not('(' in action and ')' in action and ',' in action):
        raise ValueError(f"Couldn't find coordinates in {action}")
    start_index = action.find('(') + 1
    end_index = action.find(')')
    horizontal, vertical = action[start_index:end_index].split(',', maxsplit=1)
    try:
        return int(horizontal), int(vertical)
    except ValueError:
        raise ValueError(f"Couldn't find coordinates in {action}")