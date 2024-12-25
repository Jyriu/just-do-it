import pytest
from flask import json

def test_like_post_success(client, auth_headers, create_topic, create_post):
    """Test le like réussi d'un post."""
    # Créer un post à liker
    topic = create_topic("Test Topic")
    post = create_post(
        title="Test Post",
        content="Test Content",
        user_id=auth_headers['user_id'],
        topic_id=topic.id
    )
    
    response = client.post(f'/like/{post.id}',
        headers=auth_headers
    )
    assert response.status_code == 201
    assert "message" in json.loads(response.data)

def test_like_post_twice(client, auth_headers, create_topic, create_post):
    """Test la tentative de liker un post deux fois."""
    # Créer un post
    topic = create_topic("Test Topic")
    post = create_post(
        title="Test Post",
        content="Test Content",
        user_id=auth_headers['user_id'],
        topic_id=topic.id
    )
    
    # Premier like
    client.post(f'/like/{post.id}', headers=auth_headers)
    
    # Deuxième like
    response = client.post(f'/like/{post.id}', headers=auth_headers)
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "already liked" in data.get("error", "").lower()

def test_like_nonexistent_post(client, auth_headers):
    """Test le like d'un post inexistant."""
    response = client.post('/like/999', headers=auth_headers)
    assert response.status_code == 404

def test_like_post_without_auth(client, create_topic, create_post, create_user):
    """Test le like d'un post sans authentification."""
    # Créer un post
    user = create_user("postuser", "post@test.com", "TestPass123")
    topic = create_topic("Test Topic")
    post = create_post(
        title="Test Post",
        content="Test Content",
        user_id=user.id,
        topic_id=topic.id
    )
    
    response = client.post(f'/like/{post.id}')
    assert response.status_code == 401

def test_like_reply_success(client, auth_headers, create_topic, create_post, create_reply):
    """Test le like réussi d'une réponse."""
    # Créer un post et une réponse
    topic = create_topic("Test Topic")
    post = create_post(
        title="Test Post",
        content="Test Content",
        user_id=auth_headers['user_id'],
        topic_id=topic.id
    )
    reply = create_reply(
        content="Test Reply",
        post_id=post.id,
        user_id=auth_headers['user_id']
    )
    
    response = client.post(f'/like_reply/{reply.id}',
        headers=auth_headers
    )
    assert response.status_code == 201
    assert "message" in json.loads(response.data)

def test_like_reply_twice(client, auth_headers, create_topic, create_post, create_reply):
    """Test la tentative de liker une réponse deux fois."""
    # Créer un post et une réponse
    topic = create_topic("Test Topic")
    post = create_post(
        title="Test Post",
        content="Test Content",
        user_id=auth_headers['user_id'],
        topic_id=topic.id
    )
    reply = create_reply(
        content="Test Reply",
        post_id=post.id,
        user_id=auth_headers['user_id']
    )
    
    # Premier like
    client.post(f'/like_reply/{reply.id}', headers=auth_headers)
    
    # Deuxième like
    response = client.post(f'/like_reply/{reply.id}', headers=auth_headers)
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "already liked" in data.get("error", "").lower()

def test_like_nonexistent_reply(client, auth_headers):
    """Test le like d'une réponse inexistante."""
    response = client.post('/like_reply/999', headers=auth_headers)
    assert response.status_code == 404
