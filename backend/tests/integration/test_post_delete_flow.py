import pytest
from flask import json

def test_post_deletion_flow(client, create_user, create_topic):
    """Test un scénario complet de suppression de post et réponses."""
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
    
    # 2. Connecter les utilisateurs
    login_response1 = client.post('/login', json={
        'username': user1_data['username'],
        'password': user1_data['password']
    })
    login_data1 = json.loads(login_response1.data)
    user1_headers = {'Authorization': f'Bearer {login_data1["access_token"]}'}
    
    login_response2 = client.post('/login', json={
        'username': user2_data['username'],
        'password': user2_data['password']
    })
    login_data2 = json.loads(login_response2.data)
    user2_headers = {'Authorization': f'Bearer {login_data2["access_token"]}'}
    
    # 3. Créer un topic
    topic = create_topic("Test Topic")
    
    # 4. User1 crée un post
    post_response = client.post('/create_post',
        headers=user1_headers,
        json={
            'title': 'Post to test deletion',
            'content': 'This post will receive replies and then be deleted',
            'topic_id': topic.id
        }
    )
    assert post_response.status_code == 201
    post_data = json.loads(post_response.data)
    post_id = post_data['id']
    
    # 5. User2 ajoute une réponse
    reply_response = client.post(f'/reply_post/{post_id}',
        headers=user2_headers,
        json={'content': 'Reply from user2'}
    )
    assert reply_response.status_code == 201
    
    # 6. User2 tente de supprimer le post (doit échouer)
    delete_attempt = client.delete(f'/posts/{post_id}',
        headers=user2_headers
    )
    assert delete_attempt.status_code == 401
    
    # 7. User1 (auteur) supprime le post
    delete_response = client.delete(f'/posts/{post_id}',
        headers=user1_headers
    )
    assert delete_response.status_code == 200
    
    # 8. Vérifier que le post et ses réponses sont supprimés
    get_post = client.get(f'/posts/{post_id}')
    assert get_post.status_code == 404
    
    # 9. Vérifier que les posts de l'utilisateur sont mis à jour
    posts_response = client.get('/posts')
    posts_data = json.loads(posts_response.data)
    assert not any(post['id'] == post_id for post in posts_data['posts']) 