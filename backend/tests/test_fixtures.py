def test_sample_data_creation(sample_data):
    """Test que la fixture sample_data crée correctement toutes les entités."""
    assert sample_data['user'].username == "testuser"
    assert sample_data['topic'].title == "Test Topic"
    assert sample_data['post'].title == "Test Post"
    assert sample_data['reply'].content == "Test Reply"

def test_user_creation(create_user):
    """Test la création d'un utilisateur via la fixture."""
    user = create_user("newuser", "new@test.com", "Password123")
    assert user.username == "newuser"
    assert user.email == "new@test.com"

def test_post_creation(create_user, create_topic, create_post):
    """Test la création d'un post avec les relations correctes."""
    user = create_user("postuser", "post@test.com", "Password123")
    topic = create_topic("Post Topic")
    post = create_post(
        title="New Post",
        content="Post Content",
        user_id=user.id,
        topic_id=topic.id
    )
    assert post.title == "New Post"
    assert post.user_id == user.id
    assert post.topic_id == topic.id

def test_reply_creation(create_user, create_topic, create_post, create_reply):
    """Test la création d'une réponse avec les relations correctes."""
    user = create_user("replyuser", "reply@test.com", "Password123")
    topic = create_topic("Reply Topic")
    post = create_post(
        title="Reply Post",
        content="Post Content",
        user_id=user.id,
        topic_id=topic.id
    )
    reply = create_reply(
        content="Reply Content",
        post_id=post.id,
        user_id=user.id
    )
    assert reply.content == "Reply Content"
    assert reply.post_id == post.id
    assert reply.user_id == user.id

def test_like_creation(create_user, create_topic, create_post, create_like):
    """Test la création d'un like sur un post."""
    user = create_user("likeuser", "like@test.com", "Password123")
    topic = create_topic("Like Topic")
    post = create_post(
        title="Like Post",
        content="Post Content",
        user_id=user.id,
        topic_id=topic.id
    )
    like = create_like(user_id=user.id, post_id=post.id)
    assert like.user_id == user.id
    assert like.post_id == post.id 