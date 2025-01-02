import pytest
from flask import json

def test_create_post_success(client, auth_headers, create_topic):
    """Test la création réussie d'un post."""
    # Créer un topic d'abord
    topic = create_topic("Test Topic")
    
    response = client.post('/create_post', 
        headers=auth_headers,
        json={
            'title': 'Test Post',
            'content': 'Test Content',
            'topic_id': topic.id
        }
    )
    assert response.status_code == 201
    assert 'message' in json.loads(response.data)

def test_create_post_without_auth(client, create_topic):
    """Test la création d'un post sans authentification."""
    topic = create_topic("Test Topic")
    
    response = client.post('/create_post', json={
        'title': 'Test Post',
        'content': 'Test Content',
        'topic_id': topic.id
    })
    assert response.status_code == 401

def test_create_post_invalid_topic(client, auth_headers):
    """Test la création d'un post avec un topic invalide."""
    response = client.post('/create_post',
        headers=auth_headers,
        json={
            'title': 'Test Post',
            'content': 'Test Content',
            'topic_id': 999  # ID inexistant
        }
    )
    assert response.status_code == 404

def test_reply_to_post_success(client, auth_headers, create_topic, create_post):
    """Test la création réussie d'une réponse à un post."""
    # Créer les données nécessaires
    topic = create_topic("Test Topic")
    post = create_post(
        title="Original Post",
        content="Original Content",
        user_id=auth_headers['user_id'],
        topic_id=topic.id
    )
    
    response = client.post(f'/reply_post/{post.id}',
        headers=auth_headers,
        json={'content': 'Test Reply'}
    )
    assert response.status_code == 201

def test_reply_to_nonexistent_post(client, auth_headers):
    """Test la réponse à un post inexistant."""
    response = client.post('/reply_post/999',
        headers=auth_headers,
        json={'content': 'Test Reply'}
    )
    assert response.status_code == 404

def test_get_posts_pagination(client, create_user, create_topic, create_post):
    """Test la pagination des posts."""
    user = create_user("testuser", "test@test.com", "TestPass123")
    topic = create_topic("Test Topic")
    
    # Créer plusieurs posts
    for i in range(15):  # Créer 15 posts
        create_post(
            title=f"Post {i}",
            content=f"Content {i}",
            user_id=user.id,
            topic_id=topic.id
        )
    
    # Tester la première page
    response = client.get('/posts?page=1&limit=10')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert len(data['posts']) == 10
    assert data['total_pages'] == 2
    assert data['current_page'] == 1
    assert data['has_next'] is True
    
    # Tester la deuxième page
    response = client.get('/posts?page=2&limit=10')
    data = json.loads(response.data)
    assert len(data['posts']) == 5
    assert data['has_next'] is False

def test_update_post_success(client, auth_headers, create_topic, create_post):
    """Test la mise à jour réussie d'un post."""
    topic = create_topic("Test Topic")
    post = create_post(
        title="Original Title",
        content="Original Content",
        user_id=auth_headers['user_id'],
        topic_id=topic.id
    )
    
    response = client.put(f'/update_post/{post.id}',
        headers=auth_headers,
        json={
            'title': 'Updated Title',
            'content': 'Updated Content'
        }
    )
    assert response.status_code == 200

def test_update_others_post(client, auth_headers, create_user, create_topic, create_post):
    """Test la tentative de mise à jour du post d'un autre utilisateur."""
    # Créer un autre utilisateur et son post
    other_user = create_user("otheruser", "other@test.com", "TestPass123")
    topic = create_topic("Test Topic")
    post = create_post(
        title="Other's Post",
        content="Other's Content",
        user_id=other_user.id,
        topic_id=topic.id
    )
    
    response = client.put(f'/update_post/{post.id}',
        headers=auth_headers,
        json={
            'title': 'Trying to Update',
            'content': 'Trying to Update Content'
        }
    )
    assert response.status_code == 401

def test_get_topics(client, create_topic):
    """Test la récupération des topics."""
    # Créer quelques topics
    create_topic("Topic 1")
    create_topic("Topic 2")
    
    response = client.get('/topics')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]['title'] == "Topic 1"
    assert data[1]['title'] == "Topic 2"

def test_delete_post_success(client, auth_headers, create_topic, create_post):
    """Test la suppression réussie d'un post par son auteur."""
    topic = create_topic("Test Topic")
    post = create_post(
        title="Post to delete",
        content="Content to delete",
        user_id=auth_headers['user_id'],
        topic_id=topic.id
    )
    
    response = client.delete(f'/posts/{post.id}',
        headers=auth_headers
    )
    assert response.status_code == 200
    assert 'message' in json.loads(response.data)
    
    # Vérifier que le post n'existe plus
    get_response = client.get(f'/posts/{post.id}')
    assert get_response.status_code == 404

def test_delete_others_post(client, auth_headers, create_user, create_topic, create_post):
    """Test la tentative de suppression du post d'un autre utilisateur."""
    other_user = create_user("otheruser", "other@test.com", "TestPass123")
    topic = create_topic("Test Topic")
    post = create_post(
        title="Other's Post",
        content="Other's Content",
        user_id=other_user.id,
        topic_id=topic.id
    )
    
    response = client.delete(f'/posts/{post.id}',
        headers=auth_headers
    )
    assert response.status_code == 401

def test_delete_post_with_replies(client, auth_headers, create_topic, create_post, create_reply):
    """Test la suppression d'un post avec des réponses."""
    topic = create_topic("Test Topic")
    post = create_post(
        title="Post with replies",
        content="Main content",
        user_id=auth_headers['user_id'],
        topic_id=topic.id
    )
    
    # Ajouter quelques réponses
    reply1 = create_reply(
        content="First reply",
        post_id=post.id,
        user_id=auth_headers['user_id']
    )
    reply2 = create_reply(
        content="Second reply",
        post_id=post.id,
        user_id=auth_headers['user_id']
    )
    
    response = client.delete(f'/posts/{post.id}',
        headers=auth_headers
    )
    assert response.status_code == 200
    
    # Vérifier que les réponses sont également supprimées
    get_reply1 = client.get(f'/replies/{reply1.id}')
    get_reply2 = client.get(f'/replies/{reply2.id}')
    assert get_reply1.status_code == 404
    assert get_reply2.status_code == 404

def test_delete_reply_success(client, auth_headers, create_topic, create_post, create_reply):
    """Test la suppression réussie d'une réponse par son auteur."""
    topic = create_topic("Test Topic")
    post = create_post(
        title="Post with reply",
        content="Main content",
        user_id=auth_headers['user_id'],
        topic_id=topic.id
    )
    
    reply = create_reply(
        content="Reply to delete",
        post_id=post.id,
        user_id=auth_headers['user_id']
    )
    
    response = client.delete(f'/replies/{reply.id}',
        headers=auth_headers
    )
    assert response.status_code == 200
    
    # Vérifier que la réponse n'existe plus
    get_response = client.get(f'/replies/{reply.id}')
    assert get_response.status_code == 404

def test_delete_others_reply(client, auth_headers, create_user, create_topic, create_post, create_reply):
    """Test la tentative de suppression de la réponse d'un autre utilisateur."""
    other_user = create_user("otheruser", "other@test.com", "TestPass123")
    topic = create_topic("Test Topic")
    post = create_post(
        title="Post",
        content="Content",
        user_id=other_user.id,
        topic_id=topic.id
    )
    
    reply = create_reply(
        content="Other's reply",
        post_id=post.id,
        user_id=other_user.id
    )
    
    response = client.delete(f'/replies/{reply.id}',
        headers=auth_headers
    )
    assert response.status_code == 401
