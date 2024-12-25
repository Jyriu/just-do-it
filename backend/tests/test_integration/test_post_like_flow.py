import pytest
from flask import json
from datetime import datetime, timezone

def test_complete_post_interaction_flow(client, create_user, create_topic):
    """Test un scénario complet d'interaction avec un post."""
    # 1. Créer deux utilisateurs avec des données valides
    user1_data = {
        'username': 'testuser1',
        'email': 'testuser1@test.com',
        'password': 'TestPass123!'
    }
    user2_data = {
        'username': 'testuser2',
        'email': 'testuser2@test.com',
        'password': 'TestPass123!'
    }
    
    # Enregistrer les utilisateurs et vérifier le succès
    response1 = client.post('/register', json=user1_data)
    assert response1.status_code == 201, "L'enregistrement de l'utilisateur 1 a échoué"
    response2 = client.post('/register', json=user2_data)
    assert response2.status_code == 201, "L'enregistrement de l'utilisateur 2 a échoué"
    
    # 2. Connecter le premier utilisateur
    login_response = client.post('/login', json={
        'username': user1_data['username'],
        'password': user1_data['password']
    })
    assert login_response.status_code == 200, "La connexion de l'utilisateur 1 a échoué"
    login_data = json.loads(login_response.data)
    assert 'access_token' in login_data, "Le token d'accès est manquant dans la réponse"
    user1_token = login_data['access_token']
    user1_headers = {'Authorization': f'Bearer {user1_token}'}
    
    # 3. Créer un topic
    topic = create_topic("Test Topic")
    assert topic.id is not None, "La création du topic a échoué"
    
    # 4. User1 crée un post
    post_data = {
        'title': 'Integration Test Post',
        'content': 'This is a test post for integration testing',
        'topic_id': topic.id
    }
    post_response = client.post('/create_post',
        headers=user1_headers,
        json=post_data
    )
    assert post_response.status_code == 201, "La création du post a échoué"
    post_result = json.loads(post_response.data)
    
    # Vérifier toutes les informations retournées
    assert 'message' in post_result, "Le message de confirmation est manquant dans la réponse"
    assert post_result['message'] == 'Post successfully created', "Le message de confirmation est incorrect"
    assert 'id' in post_result, "L'ID du post est manquant dans la réponse"
    assert 'title' in post_result, "Le titre du post est manquant dans la réponse"
    assert 'content' in post_result, "Le contenu du post est manquant dans la réponse"
    assert 'topic_id' in post_result, "L'ID du topic est manquant dans la réponse"
    assert 'user_id' in post_result, "L'ID de l'utilisateur est manquant dans la réponse"
    assert 'created_at' in post_result, "La date de création est manquante dans la réponse"
    
    # Vérifier que les valeurs correspondent
    assert post_result['title'] == post_data['title'], "Le titre ne correspond pas"
    assert post_result['content'] == post_data['content'], "Le contenu ne correspond pas"
    assert post_result['topic_id'] == post_data['topic_id'], "L'ID du topic ne correspond pas"
    
    post_id = post_result['id']
    
    # 6. User1 ajoute une réponse à son propre post
    reply_data = {'content': 'Self reply to test'}
    reply_response = client.post(f'/reply_post/{post_id}',
        headers=user1_headers,
        json=reply_data
    )
    assert reply_response.status_code == 201, "La création de la réponse a échoué"
    
    # 7. Connecter le deuxième utilisateur
    login_response2 = client.post('/login', json={
        'username': user2_data['username'],
        'password': user2_data['password']
    })
    assert login_response2.status_code == 200, "La connexion de l'utilisateur 2 a échoué"
    login_data2 = json.loads(login_response2.data)
    assert 'access_token' in login_data2, "Le token d'accès est manquant pour l'utilisateur 2"
    user2_token = login_data2['access_token']
    user2_headers = {'Authorization': f'Bearer {user2_token}'}
    
    # 8. User2 ajoute une réponse
    reply_data2 = {'content': 'Reply from another user'}
    reply_response2 = client.post(f'/reply_post/{post_id}',
        headers=user2_headers,
        json=reply_data2
    )
    assert reply_response2.status_code == 201, "La création de la deuxième réponse a échoué"
    
    # 9. User2 like le post
    like_response = client.post(f'/like/{post_id}',
        headers=user2_headers
    )
    assert like_response.status_code == 201, "L'ajout du like a échoué"
    
    # 10. Vérifier que le post a bien un like
    posts_response = client.get('/posts')
    posts_data = json.loads(posts_response.data)
    found_post = next((p for p in posts_data['posts'] if p['id'] == post_id), None)
    assert found_post is not None, "Le post n'a pas été trouvé"
    assert found_post['likes_count'] == 1, "Le compteur de likes n'est pas correct"
    
    # 11. User2 ne peut pas modifier le post
    update_data = {
        'title': 'Trying to update',
        'content': 'This should not work'
    }
    update_response = client.put(f'/update_post/{post_id}',
        headers=user2_headers,
        json=update_data
    )
    assert update_response.status_code == 401, "La modification non autorisée aurait dû échouer"
    
    # 12. User1 peut modifier son post
    update_data = {
        'title': 'Updated Title',
        'content': 'Updated content'
    }
    update_response = client.put(f'/update_post/{post_id}',
        headers=user1_headers,
        json=update_data
    )
    assert update_response.status_code == 200, "La modification autorisée a échoué"
    
    # Vérifier que le contenu a bien été mis à jour
    posts_response = client.get('/posts')
    posts_data = json.loads(posts_response.data)
    updated_post = next((p for p in posts_data['posts'] if p['id'] == post_id), None)
    assert updated_post is not None, "Le post mis à jour n'a pas été trouvé"
    assert updated_post['title'] == update_data['title'], "Le titre n'a pas été mis à jour correctement"
    assert updated_post['content'] == update_data['content'], "Le contenu n'a pas été mis à jour correctement" 