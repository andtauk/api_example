from fastapi import APIRouter, Depends, HTTPException, status
from typing import List as ListType

try:
    from .. import models, schemas, database, utils
except:
    import database, utils, models, schemas

router = APIRouter(
    prefix="/users",
    tags=["users"],
    )

# acrescentar um novo post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut, )
def create_post(user: schemas.UserCreate, db: database.SessionLocal = Depends(database.get_db)):

    user_password = utils.hash_password(user.password)
    user.password = user_password

    new_user = models.User(**user.dict())  # criou um novo posto
    db.add(new_user)  # add o novo posto ao banco de dados
    db.commit()  # salva o novo posto no banco de dados
    db.refresh(new_user)  # atualiza o novo posto com os dados do banco de dados

    return new_user

# recuperar todos os posts
@router.get("/", response_model=ListType[schemas.UserOut])
def root(db: database.SessionLocal = Depends(database.get_db)):
    users = db.query(models.User).all()
    return users


@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: database.SessionLocal = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found"
        )
    return user