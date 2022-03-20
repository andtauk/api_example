##Quando nesse arquivo, não é necessário importar para dentro dos tested

from app.schemas import UserCreate
from app.models import Post, Vote
from app.oauth2 import create_access_token
import pytest
from app.main import app
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.database import get_db
from app.database import Base
import pytest



SQLALQUEMY_DATABASE_URL = f"""postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"""

engine = create_engine(SQLALQUEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

client = TestClient(app)

@pytest.fixture
def test_user(client):
  user1 = UserCreate(
    name="username",
    email="email@email.com",
    password="password"
  )
  user_data = user1.dict()
  res = client.post("/users/", json=user_data)

  assert res.status_code == 201
  new_user = res.json()
  new_user["password"] = user_data["password"]
  return new_user

@pytest.fixture
def test_second_user(client):
  user1 = UserCreate(
    name="username",
    email="email2@email.com",
    password="password"
  )
  user_data = user1.dict()
  res = client.post("/users/", json=user_data)

  assert res.status_code == 201
  new_user = res.json()
  new_user["password"] = user_data["password"]
  return new_user


@pytest.fixture(scope="function")
def session():
  Base.metadata.drop_all(bind=engine)
  Base.metadata.create_all(bind=engine)
  ###Utilizando alembic
  ##utilizar sqlalchemy é mais simples
  # command.downgrade("base")
  # command.upgrade("head")
  db = TestingSessionLocal()
  try:
      yield db
  finally:
      db.close()

@pytest.fixture
def client(session):
  def override_get_db():
    try:
      yield session
    finally:
      session.close()
  app.dependency_overrides[get_db] = override_get_db 
  yield TestClient(app)

@pytest.fixture
def token(test_user):
  data = {"user_id" :  test_user["id"]}
  return create_access_token(data)


@pytest.fixture
def authorized_client(client, token):
  ##o cabecaço de autorização é acrescentado ao client
  client.headers.update({"Authorization": f"Bearer {token}"})
  return client

@pytest.fixture
def test_post(test_user, test_second_user, session):
  post_data = [
    Post(content="post1", title= "title1", owner_id=test_user["id"]),
    Post(content="post2", title= "title2", owner_id=test_user["id"]),
    Post(content="post3", title= "title3", owner_id=test_user["id"]),
    Post(content="post4", title= "title4", owner_id=test_second_user["id"]),
    ]
  session.add_all(post_data)
  session.commit()
  posts = session.query(Post).all()
  return posts
  
@pytest.fixture
def user_1_vote_on_post_1(session, test_post):
  vote_direction = 1
  vote = Vote(post_id=test_post[0].id, user_id=test_post[0].owner_id)
  session.add(vote)
  session.commit()
  return vote