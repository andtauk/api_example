from fastapi import APIRouter, Depends, HTTPException, Response, status
from typing import List as ListType, Optional

from sqlalchemy import func

try:
    from .. import models, oauth2
    from ..schemas import PostCreate, Post, PostVotes
    from ..database import get_db, SessionLocal
except:
  import models, oauth2
  from schemas import PostCreate, Post, PostVotes
  from database import get_db, SessionLocal

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
    )


# recuperar todos os posts
@router.get("/", response_model=ListType[PostVotes])
def root(
    db: SessionLocal = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    search: Optional[str] = "",
    skip: int = 0,):

    # cursor.execute("""
    # SELECT *
    # FROM posts
    # """)
    # posts = cursor.fetchall()
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    results = db.query(
        models.Post, func.count(models.Vote.post_id).label("votes")
        ).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True
        ).group_by(
            models.Post.id
        ).filter(
            models.Post.title.contains(search)
        ).limit(limit).offset(skip).all()

    return results


# acrescentar um novo post
#current_user: int = Depends(oauth2.get_current_user) é utilizado para verificar se o usuário está autenticado
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_post(post: PostCreate, db: SessionLocal = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
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
    new_post.owner_id = current_user.id
    db.add(new_post)  # add o novo posto ao banco de dados
    db.commit()  # salva o novo posto no banco de dados
    db.refresh(new_post)  # atualiza o novo posto com os dados do banco de dados

    return new_post


# recuperar um post especifico
@router.get("/{id}", response_model=PostVotes)
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

    post = db.query(
        models.Post, func.count(models.Vote.post_id).label("votes")
        ).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True
        ).group_by(
            models.Post.id
        ).filter(models.Post.id == id).first()
        
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    return post


@router.delete("/{id}")
def delete_post(id: int, db: SessionLocal = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
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
    post = deleted_post.first()

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to delete this post"
        )

    deleted_post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=Post)
def update_post(id: int, updated_post: PostCreate, db: SessionLocal = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
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
    
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to delete this post"
        )

    new_post = updated_post.dict()

    # for key, _ in new_post.items():
    #     if key not in post.__dict__:
    #         new_post[key] = post[key]

    post_query.update(new_post, synchronize_session=False)
    db.commit()

    return post_query.first()