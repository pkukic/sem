def check_char(char: str):
    if len(char) == 2:
        valid = False
        if char == '\\t':
            valid = True
        elif char == '\\n':
            valid = True
        elif char == '\\0':
            valid = True
        elif char == "\\'":
            valid = True
        elif char == '\\"':
            valid = True
        elif char == '\\\\':
            valid = True
    elif len(char) == 1:
        valid = True
    else:
        valid = False
    return valid


def check_string(string: str):
    # begin and end with "
    if len(string) < 2:
        return False
    if string[0] != '"' or string[-1] != '"':
        return False
    
    i = 0
    while i < len(string):
        # if string is of format "...\"
        if string[i] == "\\" and i == len(string) - 2:
            return False
        if string[i] == "\\":
            if not check_char(string[i:i+2]):
                return False
            i += 1
        else:
            if not check_char(string[i]):
                return False
        i += 1
    
    return True