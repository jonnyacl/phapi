import hashlib

def hash(to_hash):
    to_hash = to_hash.encode('utf-8')
    hashed = hashlib.sha3_256(to_hash)
    return hashed.hexdigest()
