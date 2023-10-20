from passlib.context import CryptContext # for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # Specifying default algorythm


def hash(password: str): # define a function we can call -  pass in password of type string
    return pwd_context.hash(password) # return hashed password

def verify (plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)