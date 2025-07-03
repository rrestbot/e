import json, os

def save_user(user_id):
    path = "data/users.json"
    users = []
    if os.path.exists(path):
        with open(path) as f:
            users = json.load(f)
    if user_id not in users:
        users.append(user_id)
        with open(path, "w") as f:
            json.dump(users, f)

def is_banned(user_id):
    path = "data/banned.json"
    if not os.path.exists(path):
        return False
    with open(path) as f:
        banned = json.load(f)
    return user_id in banned

def log_vote(user_id, vote):
    print(f"{user_id} voted {vote}")
