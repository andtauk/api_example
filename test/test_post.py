from app.schemas import PostCreate, PostVotes
from app.models import Post
import pytest

def test_get_posts_empty(authorized_client):
  response = authorized_client.get("/posts/")
  assert response.status_code == 200
  assert response.json() == []

def test_get_all_posts(authorized_client, test_user, test_post):

  post_data = [
    Post(content="post1", title= "title1", owner_id=test_user["id"]),
    Post(content="post2", title= "title2", owner_id=test_user["id"]),
    Post(content="post3", title= "title3", owner_id=test_user["id"]),
    ]

  response = authorized_client.get("/posts/")
  list_post_out = [PostVotes(**x).Post for x in response.json()]

  for post in list_post_out:
    for post_in in post_data:
      if post.id == post_in.id:
        assert post.title == post_in.title
        assert post.content == post_in.content
        assert post.owner_id == post_in.owner_id


  assert response.status_code == 200

def test_unauthorized_get_all_posts(client):
  response = client.get("/posts/")
  assert response.status_code == 403

def test_unauthorized_get_one_post(client, test_post):
  assert client.get(f"/posts/{test_post[0].id}").status_code == 403
  assert client.get(f"/posts/{test_post[1].id}").status_code == 403
  assert client.get(f"/posts/{test_post[2].id}").status_code == 403

def test_post_not_found(authorized_client):
  assert authorized_client.get("/posts/0").status_code == 404


@pytest.mark.parametrize("post_id", [0, 1, 2])
def test_get_one_post(authorized_client, test_post, test_user, post_id):

  post_data = [
    Post(content="post1", title= "title1", owner_id=test_user["id"]),
    Post(content="post2", title= "title2", owner_id=test_user["id"]),
    Post(content="post3", title= "title3", owner_id=test_user["id"]),
    ]

  response = authorized_client.get(f"/posts/{test_post[post_id].id}")
  assert response.status_code == 200
  post_out = PostVotes(**response.json()).Post
  assert post_out.title == post_data[post_id].title
  assert post_out.content == post_data[post_id].content
  assert post_out.owner_id == post_data[post_id].owner_id

def test_create_post(authorized_client, test_user):
  post_data = {
    "title": "title",
    "content": "content",
    "owner_id": test_user["id"],
    "published":True
  }
  response = authorized_client.post("/posts/", json=post_data)
  assert response.status_code == 201
  post_out = PostCreate(**response.json())
  assert post_out.title == post_data["title"]
  assert post_out.content == post_data["content"]
  assert post_out.published == post_data["published"]

def test_unauthorized_user_create_post(client):
  post_data = {
    "title": "title",
    "content": "content",
    "owner_id": 1,
    "published":True
  }
  response = client.post("/posts/", json=post_data)
  assert response.status_code == 403

def test_unauthorized_user_delete_post(client, test_post):
  response = client.delete(f"/posts/{test_post[0].id}")
  assert response.status_code == 403
  response = client.delete(f"/posts/{test_post[1].id}")
  assert response.status_code == 403
  response = client.delete(f"/posts/{test_post[2].id}")
  assert response.status_code == 403

@pytest.mark.parametrize("post_id", [0, 1, 2])
def test_user_delete_post(authorized_client, test_post, post_id):
  response = authorized_client.delete(f"/posts/{test_post[post_id].id}")
  assert response.status_code == 204

def test_user_delete_post_not_found(authorized_client):
  response = authorized_client.delete("/posts/0")
  assert response.status_code == 404

def test_delete_other_user_post(authorized_client, test_post):
  response = authorized_client.delete(f"/posts/{test_post[3].id}")
  assert response.status_code == 403

def test_update_post(authorized_client, test_post):
  post_data = {
    "title": "title updated",
    "content": "content updated",
    "owner_id": test_post[0].owner_id,
    "published":True
  }
  response = authorized_client.put(f"/posts/{test_post[0].id}", json=post_data)
  assert response.status_code == 200
  post_out = PostCreate(**response.json())
  assert post_out.title == post_data["title"]
  assert post_out.content == post_data["content"]
  assert post_out.published == post_data["published"]

def test_update_post_unauthorized_user(client, test_post):
  post_data = {
    "title": "title updated",
    "content": "content updated",
    "owner_id": test_post[0].owner_id,
    "published":True
  }
  response = client.put(f"/posts/{test_post[0].id}", json=post_data)
  assert response.status_code == 403

def test_update_post_from_another_user(authorized_client, test_post):
  post_data = {
    "title": "title updated",
    "content": "content updated",
    "owner_id": test_post[3].owner_id,
    "published":True
  }
  response = authorized_client.put(f"/posts/{test_post[3].id}", json=post_data)
  assert response.status_code == 403

def test_update_post_not_found(authorized_client, test_post):
  post_data = {
    "title": "title updated",
    "content": "content updated",
    "owner_id": test_post[0].owner_id,
    "published":True
  }
  response = authorized_client.put("/posts/0", json=post_data)
  assert response.status_code == 404