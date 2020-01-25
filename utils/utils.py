import re

def name_to_module(name):
    return name.lower().translate({ord(c): "_" for c in " -"})

def check_valid_name(name):
    if re.match("[a-zA-z]([ \\-\\_]?[a-zA-z0-9]+)*$", name):
        return True
    return False
