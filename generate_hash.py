import pickle
from pathlib import Path

import streamlit_authenticator as stauth

names = ["admin"]
usernames = ["admin"]
passwords = ["1234"]

hashed_passwords = stauth.Hasher(passwords).generate()

file_path = Path(__file__).parent / "hashed_passwords.pkl"
with file_path.open("wb") as file:
    credentials = {
        "names": names,
        "usernames": usernames,
        "passwords": hashed_passwords
    }
    pickle.dump(credentials, file)
    