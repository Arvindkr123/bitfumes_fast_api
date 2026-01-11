from passlib.hash import pbkdf2_sha256

class Hash():
    def bcrypt(password: str):
        return pbkdf2_sha256.hash(password)
