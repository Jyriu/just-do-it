import pytest
from flask import json

def test_complete_post_interaction_flow(client, create_user, create_topic):
    """Test un scénario complet d'interaction avec un post."""
    # 1. Créer deux utilisateurs
    user1_data = {
        'username': 'user1',
        'email': 'user1@test.com',
        'password': 'TestPass123'
    }
    user2_data = {
        'username': 'user2',
        'email': 'user2@test.com',
        'password': 'TestPass123'
    }
    
    # Enregistrer les utilisateurs
    client.post('/register', json=user1_data)
    client.post('/register', json=user2_data)
    
    # 2. Connecter le premier utilisateur
    login_response = client.post('/login', json={
        'username': user1_data['username'],
        'password': user1_data['password']
    })
    login_data = json.loads(login_response.data)
    user1_token = login_data['access_token']
    user1_headers = {'Authorization': f'Bearer {user1_token}'}
    
    # 3. Créer un topic
    topic = create_topic("Test Topic")
    
    # 4. User1 crée un post
    post_response = client.post('/create_post',
        headers=user1_headers,
        json={
            'title': 'Integration Test Post',
            'content': 'This is a test post for integration testing',
            'topic_id': topic.id
        }
    )
    assert post_response.status_code == 201
    
    # 5. Récupérer les posts et vérifier que le nouveau post est présent
    posts_response = client.get('/posts')
    posts_data = json.loads(posts_response.data)
    assert len(posts_data['posts']) == 1
    post_id = posts_data['posts'][0]['id']
    
    # 6. User1 ajoute une réponse à son propre post
    reply_response = client.post(f'/reply_post/{post_id}',
        headers=user1_headers,
        json={'content': 'Self reply to test'}
    )
    assert reply_response.status_code == 201
    
    # 7. Connecter le deuxième utilisateur
    login_response2 = client.post('/login', json={
        'username': user2_data['username'],
        'password': user2_data['password']
    })
    login_data2 = json.loads(login_response2.data)
    user2_token = login_data2['access_token']
    user2_headers = {'Authorization': f'Bearer {user2_token}'}
    
    # 8. User2 ajoute une réponse
    reply_response2 = client.post(f'/reply_post/{post_id}',
        headers=user2_headers,
        json={'content': 'Reply from another user'}
    )
    assert reply_response2.status_code == 201
    
    # 9. User2 like le post
    like_response = client.post(f'/like/{post_id}',
        headers=user2_headers
    )
    assert like_response.status_code == 201
    
    # 10. Vérifier que le post a bien un like
    posts_response = client.get('/posts')
    posts_data = json.loads(posts_response.data)
    post = next(p for p in posts_data['posts'] if p['id'] == post_id)
    assert post['likes_count'] == 1
    
    # 11. User2 ne peut pas modifier le post
    update_response = client.put(f'/update_post/{post_id}',
        headers=user2_headers,
        json={
            'title': 'Trying to update',
            'content': 'This should not work'
        }
    )
    assert update_response.status_code == 401
    
    # 12. User1 peut modifier son post
    update_response = client.put(f'/update_post/{post_id}',
        headers=user1_headers,
        json={
            'title': 'Updated Title',
            'content': 'Updated content'
        }
    )
    assert update_response.status_code == 200
    
    # Vérifier que le contenu a bien été mis à jour
    posts_response = client.get('/posts')
    posts_data = json.loads(posts_response.data)
    updated_post = next(p for p in posts_data['posts'] if p['id'] == post_id)
    assert updated_post['title'] == 'Updated Title'
    assert updated_post['content'] == 'Updated content' 