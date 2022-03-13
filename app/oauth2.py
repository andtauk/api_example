from hashlib import algorithms_available
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

try:
  from . import database, models, schemas
except:
  import database, models, schemas

OAuth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

ALGORITHM = "HS256"
SECRET_KEY = "2kdnj385pmbvb48se2"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

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
  print(token_data.id)
  user = db.query(models.Users).filter(models.Users.id == token_data.id).first()

  return user
  