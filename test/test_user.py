from app.schemas import UserCreate, UserOut, Token
import pytest
from jose import jwt
from app.config import settings

def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    # assert response.json().get("message") == "Hello World"


user1 = UserCreate(email="email@example.com", name="username", password="password")
def test_create_user(client):
    response = client.post("/users/", json=user1.dict())
    new_user = UserOut(**response.json())
    assert response.status_code == 201
    assert new_user.email == user1.email
    assert new_user.name == user1.name

def test_login_user(test_user, client):
    res = client.post("/login", data={"username": test_user["email"], "password": test_user["password"]})
    login_res = Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=settings.algorithm)
    id = payload["user_id"]

    print(payload)
    assert res.status_code == 200
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"

@pytest.mark.parametrize(
    "email, password, status_code", [
    ("email@email.com", "passworderrado", 401,),
    ("emailerrado@email.com", "password", 401,),
    ("emailerrado@email.com", "passworderrado", 401,),
    (None, "password", 422),
    ("email@email.com", None, 422)
    ])
def test_incorrect_login(client, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})
    assert res.status_code == status_code

