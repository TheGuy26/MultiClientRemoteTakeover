def convert_number(num: bytes) -> int | float:
    try:
        if b'.' in num:
            return float(num)
        return int(num)
    except ValueError:
        raise ValueError("Couldn't cast num to int or float.")

def convert_string(string: bytes) -> str:
    return string.decode()[1:-1] # Remove double quotes

def convert_bool(boolean: bytes) -> bool:
    if boolean.decode() == "true":
        return True
    elif boolean.decode() == "false":
        return False
    raise ValueError("Couldn't cast value to bool.")

def convert_basic (value: bytes) -> int | float | str | bool | None:
    try:
        if bytes(value[:1]) == b'"':
            return convert_string(value)
        elif value[:1] == b't' or value[:1] == b'f':
            return convert_bool(value)
        elif value == b'null':
            return None
        else:
            return convert_number(value)
    except ValueError:
        raise ValueError("Couldn't convert value.")

def convert_array(array: bytes) -> list:
    seperator = b','
    encoded_list = array[1:-1].split(seperator) # Remove array first and last chars ('[' ']')
    merge_iterable_values(item_list=encoded_list, seperator=seperator)
    decoded_list = list()
    try:
        for value in encoded_list:
            value = value.strip() # Remove any whitespace
            if value[:1] == b'[':
                decoded_list.append(convert_array(value))
            elif value[:1] == b'{':
                decoded_list.append(convert_dict(value))
            else:
                decoded_list.append(convert_basic(value))
    except ValueError:
        raise ValueError("Couldn't cast array.")
    return decoded_list


def convert_dict(dictionary: bytes) -> dict:
    decoded_dict = dict()
    seperator = b','
    encoded_items = dictionary[1:-1].split(seperator)
    merge_iterable_values(item_list=encoded_items, seperator=seperator)
    merge_strings(item_list=encoded_items, seperator=seperator)
    for item in encoded_items:
        item = item.strip() # Remove any whitespace
        separated_item = item.split(b': ', maxsplit=1)
        value = separated_item[-1]
        try:
            key = convert_string(separated_item[0])
            if value[:1] == b'{':
                decoded_value = convert_dict(value)
            elif value[:1] == b'[':
                decoded_value = convert_array(value)
            else:
                decoded_value = convert_basic(value)
            decoded_dict[key] = decoded_value
        except ValueError:
            raise ValueError(f"Couldn't parse item of key {separated_item[0].decode()}")
    return  decoded_dict

def merge_iterable_values(item_list: list[bytes], seperator: bytes):
    for i in range(len(item_list)):
        if i >= len(item_list):
            break
        portion = item_list[i]
        if b'{' in portion or b'[' in portion:
            if is_first_char(portion.decode(), char='{', other_char='['):
                opener = b'{'
                closer = b'}'
            else:
                opener = b'['
                closer = b']'
            closing_pair_index = find_closing_pair_index(opener=opener, closer=closer, item_list=item_list, start_index=i)
            item_list[i:closing_pair_index+1] = [bytes(seperator.join(item_list[i:closing_pair_index+1]))] # Merge items

def find_closing_pair_index(opener: bytes, closer: bytes, item_list: list[bytes], start_index: int) -> int:
    portion = item_list[start_index]
    closers_to_find = (portion.count(opener) - portion.count(closer))
    if closers_to_find == 0:
        return start_index
    for i in range(start_index + 1, len(item_list)):
        portion = item_list[i]
        closers_to_find += (portion.count(opener) - portion.count(closer))
        if closers_to_find == 0:
            return i
    return len(item_list) - 1

def is_first_char(decoded_string: str, char: str, other_char: str) -> bool:
    for current_char in decoded_string:
        if current_char == char:
            return True
        elif current_char == other_char:
            return False
    return  False

def merge_strings(item_list: list[bytes], seperator: bytes):
    for i in range(len(item_list)):
        if i >= len(item_list):
            break
        portion = item_list[i]
        value = portion.split(b':', maxsplit=1)[-1].strip()
        first_char = value[:1]
        last_char = value[-1:]
        if value[:1] == b'"' and value[-1:] != b'"': # Uses slicing so won't return an integer
            closing_quote_index = find_closing_quote_index(item_list=item_list, start_index=i)
            item_list[i:closing_quote_index + 1] = [bytes(seperator.join(item_list[i:closing_quote_index + 1]))] # Merge items


def find_closing_quote_index(item_list: list[bytes], start_index: int) -> int:
    for i in range(start_index + 1, len(item_list)):
        portion = item_list[i]
        if b'"' in portion:
            return i
    return len(item_list) - 1


