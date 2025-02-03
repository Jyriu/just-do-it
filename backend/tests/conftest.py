import os
import sys
import pytest
from datetime import datetime, UTC

# Add 'backend' directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from extensions import db, bcrypt
from models.user import User
from models.topic import Topic
from models.post import Post
from models.reply import Reply
from models.like import Like

@pytest.fixture
def app():
    """Configure the application for testing."""
    app = create_app()
    
    # Test-specific configuration
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "postgresql://postgres:password@localhost/test_db",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "JWT_SECRET_KEY": "test_secret_key"
    })

    # Create application context
    ctx = app.app_context()
    ctx.push()

    db.create_all()  # Create all tables for testing
    
    yield app
    
    db.session.remove()
    db.drop_all()  # Clean up after tests
    ctx.pop()  # Remove application context

@pytest.fixture
def client(app):
    """Provide a test HTTP client."""
    return app.test_client()

@pytest.fixture
def app_context(app):
    """Provide an application context."""
    with app.app_context():
        yield

@pytest.fixture
def create_user(app):
    """Fixture to create a test user."""
    def _create_user(username, email, password):
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        return user
    return _create_user

@pytest.fixture
def auth_headers(client, create_user):
    """Provide authentication headers with JWT token."""
    user = create_user("testuser", "test@test.com", "TestPass123")
    response = client.post('/login', json={
        'username': 'testuser',
        'password': 'TestPass123'
    })
    token = response.json['access_token']
    return {'Authorization': f'Bearer {token}', 'user_id': user.id}

@pytest.fixture
def create_topic(app):
    """Fixture to create a test topic."""
    def _create_topic(title, description="Test description"):
        topic = Topic(title=title, description=description)
        db.session.add(topic)
        db.session.commit()
        return topic
    return _create_topic

@pytest.fixture
def create_post(app):
    """Fixture to create a test post."""
    def _create_post(title, content, user_id, topic_id):
        post = Post(
            title=title,
            content=content,
            user_id=user_id,
            topic_id=topic_id,
            created_at=datetime.now(UTC)
        )
        db.session.add(post)
        db.session.commit()
        return post
    return _create_post

@pytest.fixture
def create_reply(app):
    """Fixture to create a test reply."""
    def _create_reply(content, post_id, user_id):
        reply = Reply(
            content=content,
            post_id=post_id,
            user_id=user_id,
            created_at=datetime.now(UTC)
        )
        db.session.add(reply)
        db.session.commit()
        return reply
    return _create_reply

@pytest.fixture
def create_like(app):
    """Fixture to create a test like."""
    def _create_like(user_id, post_id=None, reply_id=None):
        like = Like(
            user_id=user_id,
            post_id=post_id,
            reply_id=reply_id
        )
        db.session.add(like)
        db.session.commit()
        return like
    return _create_like

@pytest.fixture
def sample_data(app, create_user, create_topic, create_post, create_reply):
    """Fixture that creates a complete set of test data."""
    user = create_user("testuser", "test@test.com", "TestPass123")
    topic = create_topic("Test Topic")
    post = create_post(
        title="Test Post",
        content="Test Content",
        user_id=user.id,
        topic_id=topic.id
    )
    reply = create_reply(
        content="Test Reply",
        post_id=post.id,
        user_id=user.id
    )
    
    return {
        'user': user,
        'topic': topic,
        'post': post,
        'reply': reply
    }