from flask import Blueprint, request, jsonify
from extensions import db, bcrypt
from models import User, Post, Reply, Topic
import logging
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from utils.return_error import error_response

logging.basicConfig(level=logging.DEBUG)

post_bp = Blueprint('post_bp', __name__)
topic_bp = Blueprint('topic_bp', __name__)

@post_bp.route('/create_post', methods=['POST'])
@jwt_required()
def create_post():
    data = request.get_json()

    # Vérifier la présence du topic_id et son existence
    if 'topic_id' not in data:
        return error_response('Topic ID is required', 400)

    topic = db.session.get(Topic, data['topic_id'])
    if not topic:
        return error_response('Invalid topic ID', 404)

    user_id = get_jwt_identity()

    # Ajouter le post à la base de données
    post = Post(title=data['title'], content=data['content'], user_id=user_id, topic_id=data['topic_id'])
    db.session.add(post)
    db.session.commit()

    # Retourner l'ID du post créé
    return jsonify({
        'message': 'Post successfully created',
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'topic_id': post.topic_id,
        'user_id': post.user_id,
        'created_at': post.created_at.isoformat() if post.created_at else None
    }), 201


@post_bp.route('/reply_post/<int:post_id>', methods=['POST'])
@jwt_required()
def reply_post(post_id):
    user_id = get_jwt_identity()
    data = request.get_json()

    # check if post exists
    post = db.session.get(Post, post_id)
    if not post:
        return error_response('Post not found', 404)
    
    # add reply to db
    reply = Reply(content=data['content'], user_id=user_id, post_id=post_id)
    db.session.add(reply)
    db.session.commit()

    return jsonify({'message': 'Reply successfully created.'}), 201

@post_bp.route('/reply_reply/<int:reply_id>', methods=['POST'])
@jwt_required()
def reply_to_reply(reply_id):
    data = request.get_json()

    # check needed data
    if 'parent_reply_id' not in data or 'content' not in data:
        return error_response('Missing parent_reply_id or content', 400)
    
    user_id = get_jwt_identity()

    parent_reply = db.session.get(Reply, data['parent_reply_id'])
    if not parent_reply:
        return error_response('Parent reply not found', 404)
    
    reply = Reply(post_id=parent_reply.post_id, user_id=user_id, content=data['content'], parent_reply_id=data['parent_reply_id'])
    db.session.add(reply)
    db.session.commit()

    return jsonify({'message': 'Reply to reply successfully created'}), 201

@post_bp.route('/posts', methods=['GET'])
def get_posts():
    # get params for pagination
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)

    # get paginated posts
    posts = Post.query.paginate(page=page, per_page=limit)

    # check if include_replies is true then include replies
    include_replies = request.args.get('include_replies', 'false').lower() == 'true'
    return jsonify({
        'posts': [post.to_dict(include_replies=include_replies) for post in posts.items],
        'total_pages': posts.pages,
        'total_items': posts.total,
        'current_page': posts.page,
        'per_page': posts.per_page,
        'has_next': posts.has_next,
        'has_prev': posts.has_prev
    })

@post_bp.route('/update_post/<int:post_id>', methods=['PUT'])
@jwt_required()
def update_post(post_id):
    user_id = get_jwt_identity()
    # Convertir user_id en entier car get_jwt_identity() retourne une chaîne
    user_id = int(user_id)
    
    post = db.session.get(Post, post_id)
    if not post:
        return error_response('Post not found', 404)
    
    # Log pour le débogage
    logging.debug(f"User ID from token: {user_id} (type: {type(user_id)})")
    logging.debug(f"Post user_id: {post.user_id} (type: {type(post.user_id)})")
    
    if post.user_id != user_id:
        return error_response('Unauthorized', 401)
    
    data = request.get_json()
    if 'title' not in data or 'content' not in data:
        return error_response('Title and content are required', 400)
    
    post.title = data['title']
    post.content = data['content']
    db.session.commit()
    
    # Retourner le post mis à jour
    return jsonify({
        'message': 'Post updated successfully',
        'post': post.to_dict()
    }), 200

@post_bp.route('/update_reply/<int:reply_id>', methods=['PUT'])
@jwt_required()
def update_reply(reply_id):
    user_id = get_jwt_identity()
    reply = db.session.get(Reply, reply_id)

    if not reply:
        return error_response('Reply not found', 404)
    
    if reply.user_id != user_id:
        return error_response('Unauthorized', 401)
    
    data = request.get_json()

    if 'content' not in data:
        return error_response('Content is required', 400)
    
    reply.content = data['content']
    db.session.commit()

    return jsonify({'message': 'Reply updated successfully'}), 200

@post_bp.route('/topics', methods=['GET'])
def get_topics():
    topics = Topic.query.all()
    return jsonify([{'id': topic.id, 'name': topic.name, 'description': topic.description} for topic in topics])

# create a topic (only for admin)
@post_bp.route('/create_topic', methods=['POST'])
@jwt_required()
def create_topic():
    user_id = get_jwt_identity()
    user = db.session.get(User, user_id)

    if not user.is_admin:
        return error_response('Unauthorized', 401)
    
    data = request.get_json()

    if 'name' not in data or 'description' not in data:
        return error_response('Name and description are required', 400)
    
    topic = Topic(name=data['name'], description=data['description'])
    db.session.add(topic)
    db.session.commit()

    return jsonify({'message': 'Topic created successfully'}), 201