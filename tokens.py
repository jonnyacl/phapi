import datetime
import jwt

import phapienv.db_talker as db


def make_token(user, token_type):
    print(user)
    payload = {
        'some' : 'payload',
        'id' : str(user['userId']),
        'firstname' : str(user['firstName']),
        'lastname' : str(user['lastName']),
        'email' : str(user['email']),
        'username' : str(user['userName'])
    }

    created = datetime.datetime.utcnow()
    secret = str(created)
    expiry = created.replace(year = created.year + 5)

    token = jwt.encode(payload, secret, algorithm='HS256')
    db.insert_item("usertoken", jwt=token, utType=token_type, created=created,
                                        expiry=expiry, userId=user['userId'])

    return token.decode(encoding="utf-8", errors="strict")