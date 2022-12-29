from consts import *

def check_char(char: str):
    if len(char) == 4:
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
    elif len(char) == 3:
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


def implicit_cast(start, target):
    if start == target:
        return True
    if start == CONST_INT and target == INT:
        return True
    if start == INT and target == CONST_INT:
        return True
    if start == CONST_CHAR and target == CHAR:
        return True
    if start == CHAR and target == CONST_CHAR:
        return True
    if start == CONST_CHAR and target == INT:
        return True
    if start == CHAR and target == INT:
        return True
    if start == CHAR and target == CONST_INT:
        return True
    if start == CONST_CHAR and target == CONST_INT:
        return True

    if start == NIZ_CHAR and target == NIZ_CONST_CHAR:
        return True
    if start == NIZ_INT and target == NIZ_CONST_INT:
        return True
    if start == NIZ_CHAR and target == NIZ_CONST_INT:
        return True
    return False


def explicit_cast(start, target):
    if implicit_cast(start, target):
        return True
    if start == INT and target == CHAR:
        return True
    if start == INT and target == CONST_CHAR:
        return True
    if start == CONST_INT and target == CHAR:
        return True
    if start == CONST_INT and target == CONST_CHAR:
        return True
    return False


def remove_niz_from_niz_x(niz_x):
    if niz_x == NIZ_CHAR:
        return CHAR
    if niz_x == NIZ_INT:
        return INT
    if niz_x == NIZ_CONST_CHAR:
        return CONST_CHAR
    if niz_x == NIZ_CONST_INT:
        return CONST_INT


def remove_const_from_const_x(const_x):
    if const_x == CONST_CHAR:
        return CHAR
    if const_x == CONST_INT:
        return INT


def is_const_x(T: str):
    if not T:
        return False
    return T.startswith("const")


def is_niz_x(niz: str):
    return (niz == NIZ_INT or niz == NIZ_CHAR or
            niz == NIZ_CONST_INT or niz == NIZ_CONST_CHAR)


def make_const(x: str):
    return "const(" + x + ")"

def make_niz(x: str):
    return "niz(" + x + ")"