def test_vote_on_post(authorized_client, test_post):

  vote_direction = 1
  
  response = authorized_client.post(f"/vote/", json={"post_id": test_post[0].id, "direction": vote_direction})
  assert response.status_code == 201
  assert response.json()["message"] == "Vote created successfully"

def test_unvote_on_post(authorized_client, test_post, user_1_vote_on_post_1):
  
    vote_direction = 0
    
    response = authorized_client.post(f"/vote/", json={"post_id": test_post[0].id, "direction": vote_direction})
    assert response.status_code == 201
    assert response.json()["message"] == "Vote deleted"

def test_vote_on_post_voted(authorized_client, test_post, user_1_vote_on_post_1):

  vote_direction = 1
  
  response = authorized_client.post(f"/vote/", json={"post_id": test_post[0].id, "direction": vote_direction})
  assert response.status_code == 400
  assert response.json()["detail"] == "You can't like this post more than once"

def test_unvote_on_post_unvoted(authorized_client, test_post):
    
      vote_direction = 0
      
      response = authorized_client.post(f"/vote/", json={"post_id": test_post[0].id, "direction": vote_direction})
      assert response.status_code == 400
      assert response.json()["detail"] == "You can't dislike this post more than once"

def test_unauthorized_vote_on_post(client, test_post):

  vote_direction = 1
  
  response = client.post(f"/vote/", json={"post_id": test_post[0].id, "direction": vote_direction})
  assert response.status_code == 403

def test_unauthorized_unvote_on_post(client, test_post, user_1_vote_on_post_1):
  
    vote_direction = 0
    
    response = client.post(f"/vote/", json={"post_id": test_post[0].id, "direction": vote_direction})
    assert response.status_code == 403

def test_vote_on_post_not_found(authorized_client):

  vote_direction = 1
  
  response = authorized_client.post(f"/vote/", json={"post_id": 0, "direction": vote_direction})
  assert response.status_code == 404

