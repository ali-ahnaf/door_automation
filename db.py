USERS = {
    "XXXX": {"name": "Guard", "flat": "0"}
}

def get_user(pin):
    return USERS.get(pin, None)