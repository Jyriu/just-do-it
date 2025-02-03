import pytest
from flask import json
import time

def test_rate_limit_login(client):
    """Test login attempt rate limiting."""
    # Repeated login attempts
    for i in range(7):  # 7 attempts (beyond the limit of 5/minute)
        response = client.post('/login', json={
            'username': f'test_user_{i}',
            'password': 'wrong_password'
        })
        if i < 5:
            assert response.status_code in [401, 400]  # Normal login failure
        else:
            assert response.status_code == 429  # Too Many Requests

def test_rate_limit_post_creation(client, auth_headers, create_topic):
    """Test post creation rate limiting."""
    topic = create_topic("Test Topic")
    
    # Repeated post creation attempts
    for i in range(5):  # 5 attempts (beyond the limit of 3/minute)
        response = client.post('/create_post',
            headers=auth_headers,
            json={
                'title': f'Test Post {i}',
                'content': 'Test content',
                'topic_id': topic.id
            }
        )
        if i < 3:
            assert response.status_code == 201  # Successful creation
        else:
            assert response.status_code == 429  # Too Many Requests

def test_csrf_protection(client):
    """Test CSRF protection on non-exempt routes."""
    # Create a new test route in the application that is not CSRF exempt
    response = client.post('/test_csrf')
    assert response.status_code == 400  # Bad Request (missing CSRF token)

def test_cors_origins(client):
    """Test CORS configuration."""
    response = client.options('/login', headers={
        'Origin': 'http://localhost:5173',
        'Access-Control-Request-Method': 'POST'
    })
    assert response.headers.get('Access-Control-Allow-Origin') == 'http://localhost:5173'
    
    # Test with unauthorized origin
    response = client.options('/login', headers={
        'Origin': 'http://unauthorized-domain.com',
        'Access-Control-Request-Method': 'POST'
    })
    assert response.headers.get('Access-Control-Allow-Origin') != 'http://unauthorized-domain.com'

def test_rate_limit_reset(client):
    """Test that rate limits reset after the defined period."""
    # Make 5 login attempts
    for i in range(5):
        client.post('/login', json={
            'username': f'test_user_{i}',
            'password': 'wrong_password'
        })
    
    # Wait 60 seconds (1 minute)
    time.sleep(60)
    
    # Next attempt should succeed (in terms of rate limiting)
    response = client.post('/login', json={
        'username': 'test_user_6',
        'password': 'wrong_password'
    })
    assert response.status_code != 429  # Should not be rate limited 