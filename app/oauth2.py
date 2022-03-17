from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import time

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# try:
from . import database, models, schemas
from .config import settings
# except:
#   import database, models, schemas
#   from config import settings

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
      credentials : HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
      if credentials:
        if not credentials.scheme == "Bearer":
          raise HTTPException(status_code=403, detail="Invalid or expired token scheme")
        return credentials.credentials
      else:
        raise HTTPException(status_code=403, detail="Invalid or expired token")
    
    def verify_jwt(self, jwtoken: str):
      isTokenValid:bool = False
      payload = decodeJWT(jwtoken)
      if payload:
        isTokenValid = True
      return isTokenValid



      

OAuth2_scheme = JWTBearer()
# OAuth2PasswordBearer(tokenUrl="login")

ALGORITHM = settings.algorithm
SECRET_KEY = settings.secret_key
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

#access token function
def create_access_token(data: dict):
  to_encode = data.copy()

  expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  to_encode.update({"exp": expire})

  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

  return encoded_jwt

#verificação do token
def verify_access_token(token: str, credentials_exception):

  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    id = payload.get("user_id")

    if id is None:
      raise credentials_exception

    token_data = schemas.TokenData(id=id)

  except JWTError:
    raise credentials_exception

  return token_data


def get_current_user(token: str = Depends(OAuth2_scheme), db: Session = Depends(database.get_db)):

  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, 
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"}
    )

  token_data = verify_access_token(token, credentials_exception)
  user = db.query(models.User).filter(models.User.id == token_data.id).first()

  return user

def decodeJWT(token: str):
  try:
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    return decoded_token if decoded_token["exp"] > time.time() else None
  except JWTError:
    return {"message": "Invalid token"}
  
