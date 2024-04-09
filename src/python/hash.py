import bcrypt

"""
    @var
        plain_text_password - (string encoded to bytes) string should be encoded using encode('utf-8')
    @return
        - returns hashed password
"""
def get_hashed_password(plain_text_password):
    # Hash a password for the first time
    #   (Using bcrypt, the salt is saved into the hash itself)
    return bcrypt.hashpw(plain_text_password, bcrypt.gensalt())

"""
    @var
        plain_text_password - (string encoded to bytes) string should be encoded using encode('utf-8')
        hashed_password - (hashed password)
    @return
        - returns true if password matches
        - returns false if password does not match
"""
def check_password(plain_text_password, hashed_password):
    # Check hashed password. Using bcrypt, the salt is saved into the hash itself
    return bcrypt.checkpw(plain_text_password, hashed_password)
