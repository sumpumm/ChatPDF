from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

# hashed_password = get_password_hash("johndoe")
# print(hashed_password)

dic={}
if not dic:
    print("empty")