import pandas as pd

def add_accounts(email, password, username):
    try:
        users_df = pd.read_csv("user_data.csv")
    except FileNotFoundError:
        users_df = pd.DataFrame(columns=["id", "username", "email", "password"])
        users_df.set_index("id", inplace=True)
        users_df.to_csv("user_data.csv", index=True)

    new_user = pd.DataFrame({"username": [username], "email": [email], "password": [password]})
    users_df = pd.concat([users_df, new_user], ignore_index=True)

def check_login(username, password):
    pass