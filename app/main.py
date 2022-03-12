# from passlib.context import CryptContext
import time
from typing import List as ListType
from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from psycopg2.extras import RealDictCursor

# try:
from .database import get_db, SessionLocal, engine
from . import models
from .schemas import PostBase, PostCreate, Post, UserOut, UserCreate
# except:
#     from utils import hash_password
#     from database import get_db, SessionLocal, engine
#     import models
#     from schemas import PostBase, PostCreate, Post, UserOut, UserCreate

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# def hash_password(plaintext_password):
#     return pwd_context.hash(plaintext_password)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(post.router)
# app.include_router(user.router)
# app.include_router(auth.router)
# app.include_router(vote.router)


while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fast_api",
            user="postgres",
            password="postgres",
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("Connected to the database")
        break

    except Exception as e:
        print("Unable to connect to the database")
        print("Error: ", e)
        time.sleep(2)


# a ordem das funções importadas é importante
# somente a primeira que for chamado será o primeiro a ser executado


@app.get("/")
def root():
    return {"message": "Hellow World"}


# recuperar todos os posts
@app.get("/posts", response_model=ListType[Post])
def root(db: SessionLocal = Depends(get_db)):
    # cursor.execute("""
    # SELECT *
    # FROM posts
    # """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts


# acrescentar um novo post
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_post(post: PostCreate, db: SessionLocal = Depends(get_db)):
    # cursor.execute(
    #     """
    #     INSERT INTO posts (title, content, published)
    #     VALUES (%s, %s, %s)
    #     RETURNING id, title, content, published
    #     """,
    #     (post.title, post.content, post.published))
    # post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.dict())  # criou um novo posto
    db.add(new_post)  # add o novo posto ao banco de dados
    db.commit()  # salva o novo posto no banco de dados
    db.refresh(new_post)  # atualiza o novo posto com os dados do banco de dados

    return new_post


# recuperar um post especifico
@app.get("/posts/{id}", response_model=Post)
# posso passar esse id como str que o fastapi vai converter para inteiro
def get_post(id: int, db: SessionLocal = Depends(get_db)):
    # cursor.execute(
    #     """
    #     SELECT *
    #     FROM posts
    #     WHERE id = %s
    #     """,
    #     (str(id),))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    return post


@app.delete("/posts/{id}")
def delete_post(id: int, db: SessionLocal = Depends(get_db)):
    # cursor.execute(
    #     """
    #     DELETE FROM posts
    #     WHERE id = %s
    #     RETURNING id
    #     """,
    #     (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    if deleted_post.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    deleted_post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", response_model=Post)
def update_post(id: int, updated_post: PostCreate, db: SessionLocal = Depends(get_db)):
    # cursor.execute(
    #     """
    #     UPDATE posts
    #     SET title = %s, content = %s, published = %s
    #     WHERE id = %s
    #     RETURNING id, title, content, published
    #     """,
    #     (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    new_post = updated_post.dict()

    # for key, _ in new_post.items():
    #     if key not in post.__dict__:
    #         new_post[key] = post[key]

    post_query.update(new_post, synchronize_session=False)
    db.commit()

    return post_query.first()


##User CRUD___________________________________________________________________________________________

# acrescentar um novo post
@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_post(user: UserCreate, db: SessionLocal = Depends(get_db)):

    # user_password = hash_password(user.password)
    # user.password = user_password

    new_user = models.Users(**user.dict())  # criou um novo posto
    db.add(new_user)  # add o novo posto ao banco de dados
    db.commit()  # salva o novo posto no banco de dados
    db.refresh(new_user)  # atualiza o novo posto com os dados do banco de dados

    return new_user


# %%
