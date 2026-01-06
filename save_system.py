import json
import os

SAVE_FILE = "save_data.json"

def load_data():
    if not os.path.exists(SAVE_FILE):
        data = {"users": {}, "current_user": None}
        save_data(data)
        return data
    with open(SAVE_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=4)


def create_user(username):
    data = load_data()
    if username not in data["users"]:
        data["users"][username] = {"high_score": 0, "coins": 0}
        data["current_user"] = username
        save_data(data)
        return True
    return False

def login_user(username):
    data = load_data()
    if username in data["users"]:
        data["current_user"] = username
        save_data(data)
        return True
    return False  

def logout_user():
    data = load_data()
    data["current_user"] = None
    save_data(data)

def get_current_user():
    data = load_data()
    return data["current_user"]


def update_high_score(new_score):
    data = load_data()
    user = data["current_user"]
    if not user:
        return
    if new_score > data["users"][user]["high_score"]:
        data["users"][user]["high_score"] = int(new_score)
        save_data(data)

def add_coins(amount):
    data = load_data()
    user = data["current_user"]
    if not user:
        return
    data["users"][user]["coins"] += int(amount)
    save_data(data)

def get_high_score():
    data = load_data()
    user = data["current_user"]
    if not user:
        return 0
    return data["users"][user]["high_score"]

def get_total_coins():
    data = load_data()
    user = data["current_user"]
    if not user:
        return 0
    return data["users"][user]["coins"]

def get_all_users():
    data = load_data()
    return list(data["users"].keys())