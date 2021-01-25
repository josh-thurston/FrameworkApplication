import uuid
import re
import string
import random
from passlib.handlers.sha2_crypt import sha512_crypt as crypto
from data.classes import User
from services.accounts_service import find_user
from datetime import datetime
from typing import Optional
from data.db_session import db_auth


users = ['josh', 'alisha', 'addison', 'ayla', 'ashtyn']


def main():
    create_lockout_password()


def create_lockout_password():
    length = int(32)
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    num = string.digits
    symbols = string.punctuation
    mixer = lower + upper + num + symbols
    randomize = random.sample(mixer, length)
    text = "".join(randomize)
    hashed_password = hash_text(text)
    print(hashed_password)
    graph.run(f"MATCH (x:User) WHERE x.user_id='{user_id} SET x.hashed_password='{hashed_password}'")


def hash_text(text: str) -> str:
    hashed_text = crypto.encrypt(text, rounds=171204)
    return hashed_text


if __name__ == '__main__':
    main()
