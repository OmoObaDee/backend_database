# import jwt
# import Jwt
# from dotenv import load_dotenv
# import os
# from fastapi import Request, HTTPException
# from starlette.middleware.base import BaseHTTPMiddleware  
# from fastapi import requests
# import jwt 
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials  
# from dateline import datetime, timedelta   

# bearer_scheme = HTTPBearer()



# load_dotenv()
# SECRET_KEY = os.getenv("SECRET_KEY")
# ALGORITHM = os.getenv("ALGORITHM")
# ACCESS_TOKEN_EXPIRE_MINUTES = 30
# def create_token(details: dict, expiry_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES):
#     to_encode = details.copy()
#     expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     details.update({"exp": expire})
#     encoded_jwt = Jwt.encode(details, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt
# def verify_token(request: Request):
#     payload = request.headers.get("Authorization")
#     token = payload.split(" ")[1]  # Assuming "Bearer <token>"
#     jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])




    
#     auth_header = request.headers.get("Authorization")
#     if not auth_header:
#         raise HTTPException(status_code=401, detail="Authorization header missing")
    
#     token = auth_header.split(" ")[1]  # Assuming "Bearer <token>"
#     try:
#         payload = Jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         return payload
#     except Jwt.ExpiredSignatureError:
#         raise HTTPException(status_code=401, detail="Token has expired")
#     except Jwt.InvalidTokenError:
#         raise HTTPException(status_code=401, detail="Invalid token")
# class AuthMiddleware(BaseHTTPMiddleware):


# import jwt
# from dotenv import load_dotenv
# import os
# from datetime import datetime, timedelta
# from fastapi import Request
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# from fastapi import Security
# bearer = HTTPBearer()
# load_dotenv()
# secret_key = os.getenv("secret_key")

# def create_token(details: dict, expiry:int):
#     expiry = datetime.now() + timedelta(minutes=expiry)
#     details.update({"exp": expiry})
#     encoded_jwt = jwt.encode(details, secret_key)
#     return encoded_jwt
# def verify_token(request: HTTPAuthorizationCredentials = Security(bearer)):
#     token = request.credentials
#     #payload = request.headers.get("Authorization")
#     #token = payload.split(" ")[1]
#     verified_token = jwt.decode(token, secret_key, algorithms=["HS256"])
#     #expiry_time = verify_token.get("exp")
    
#     return {
#         "email": verified_token.get("email"),
#         "userType": verified_token.get("userType"),
#         "userId": verified_token.get("id")
#     }


import jwt
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Load environment variables
load_dotenv()

# Constants
SECRET_KEY = os.getenv("secret_key").strip("'").strip('"')   # clean up extra quotes
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = int(os.getenv("token_time", 30))

# Bearer authentication scheme
bearer = HTTPBearer()

# Create JWT token
def create_token(details: dict, expiry: int = TOKEN_EXPIRE_MINUTES):
    payload = details.copy()
    expire = datetime.utcnow() + timedelta(minutes=expiry)
    payload.update({"exp": expire})
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Verify JWT token
def verify_token(credentials: HTTPAuthorizationCredentials = Security(bearer)):
    token = credentials.credentials
    try:
        verified = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {
            "email": verified.get("email"),
            "userType": verified.get("userType"),
            "userId": verified.get("id")
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired. Please login again.")
    except jwt.InvalidSignatureError:
        raise HTTPException(status_code=401, detail="Invalid token signature. Wrong secret key.")
    except jwt.DecodeError:
        raise HTTPException(status_code=401, detail="Malformed or invalid token.")