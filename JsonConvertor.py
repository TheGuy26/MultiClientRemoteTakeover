def convert_number(num: int | float) -> bytes:
    return str(num).encode()

def convert_str(string: str) -> bytes:
    return f'"{string}"'.encode()

def convert_bool(boolean: bool) -> bytes:
    test = str(boolean)
    test2 = test.lower()
    return str(boolean).lower().encode()

def convert_basic(item: int | float | str | bool | None) -> bytes:
    if isinstance(item, bool):
        return convert_bool(item)
    if isinstance(item, int | float):
        return convert_number(item)
    if isinstance(item, str):
        return convert_str(item)
    if item is None:
        return b'null'
    raise ValueError("Unsupported argument type")

def convert_array(array: list | tuple) -> bytes:
    converted_list = []
    seperator = b','
    for item in array:
        if isinstance(item, list | tuple):
            converted_list.append(convert_array(item))
        elif isinstance(item, dict):
            converted_list.append(convert_dict(item))
        elif isinstance(item, int | float | str | bool | None):
            converted_list.append(convert_basic(item))
        else:
            converted_list.append(convert_custom_instance(item))

    return b"[" + seperator.join(converted_list) + b']'

def convert_dict(dictionary: dict, tab_amount:int = 1) -> bytes:
    converted_list = []
    seperator = b',\n' + b'\t' * tab_amount
    for key, value in dictionary.items():
        current_bytes = convert_str(str(key)) + b': '
        if isinstance(value, list | tuple):
            current_bytes += convert_array(value)
        elif isinstance(value, dict):
            current_bytes += convert_dict(value, tab_amount=tab_amount + 1)
        elif isinstance(value, int | float | str | bool | None):
            current_bytes += convert_basic(value)
        else:
            current_bytes += convert_custom_instance(value)
        converted_list.append(current_bytes)
    return b'{\n' + b'\t' * tab_amount + seperator.join(converted_list) + b'\n' + b'\t' * (tab_amount-1) + b'}'

def convert_custom_instance(instance) -> bytes:
    try:
        return convert_dict(vars(instance))
    except Exception:
        raise ValueError("An error has occurred while converting instance to bytes. (Json formatted)")