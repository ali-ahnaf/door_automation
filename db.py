USERS = {
    2872243011: {"name": "Ali Ahnaf", "flat": "4"},
    2787032179: {"name": "Samia Haque", "flat": "4"},
    3456789012: {"name": "Mike Wilson", "flat": "103"},
    4567890123: {"name": "Emily Davis", "flat": "201"},
    5678901234: {"name": "Building Manager", "flat": "Office"},
}

def get_user(rfid_id):
    return USERS.get(rfid_id, None)
