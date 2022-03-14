from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

try:
  from .. import database, schemas, utils, models, oauth2
except:
  import database, schemas, utils, models, oauth2

router = APIRouter(
    tags=["Authentication"],
)

@router.post("/login", response_model=schemas.Token)
def login(user_crentials:OAuth2PasswordRequestForm = Depends(), db:Session = Depends(database.get_db)):

    ##user_crentials contém os campos username e password, username é relativo a email no nosso caso
    user = db.query(models.User).filter(models.User.email == user_crentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            # headers={"WWW-Authenticate": "Bearer"},
        )
    if not utils.check_password(user_crentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            # headers={"WWW-Authenticate": "Bearer"},
        )

    ##data são todas as informações enviadas junto ao pacote
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
