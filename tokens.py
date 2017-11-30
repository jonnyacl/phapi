import datetime
import jwt

import phapienv.db_talker as db


def make_token(user, token_type):
    payload = {
        'some' : 'payload',
        'aud' : str(user['userId'])
    }

    created = datetime.datetime.utcnow()
    secret = str(created)
    expiry = created.replace(year = created.year + 5)

    token = jwt.encode(payload, secret, algorithm='HS256')
    db.insert_item("usertoken", jwt=token, utType=token_type, created=created,
                                        expiry=expiry, userId=user['userId'])

    return token.decode(encoding="utf-8", errors="strict")