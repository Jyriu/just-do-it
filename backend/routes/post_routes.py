from flask import Blueprint, request, jsonify
from extensions import db, bcrypt
from models import User, Post, Reply
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

logging.basicConfig(level=logging.DEBUG)

post_bp = Blueprint('post_bp', __name__)

@post_bp.route('/create_post', methods=['POST'])
@jwt_required()
def create_post():
    # get data send by user
    data = request.get_json()

    # get user from token
    user_id = get_jwt_identity()

    # add post to db
    post = Post(title=data['title'], content=data['content'], user_id=user_id)
    db.session.add(post)
    db.session.commit()

    return jsonify({'message': 'Post successfully created'}), 201

@post_bp.route('/reply_post', methods=['POST'])
@jwt_required()
def reply_post():
    user_id = get_jwt_identity()
    data = request.get_json()

    # check if post exists
    post = Post.query.get(post_id)
    if not post:
        return jsonify({"message": "Post introuvable"}), 404
    
    # add reply to db
    reply = Reply(content=data['content'], user_id=user_id, post_id=post_id)
    db.session.add(reply)
    db.session.commit()

    return jsonify({"message": "Réponse créée avec succès."}), 201

@post_bp.route('/reply_reply', methods=['POST'])
@jwt_required()
def reply_to_reply():
    data = request.get_json()

    # check needed data
    if 'parent_reply_id' not in data or 'content' not in data:
        return jsonify({'error': 'Missing parent_reply_id or content'}), 400
    
    user_id = get_jwt_identity()

    parent_reply = Reply.query.get(data['parent_reply_id'])
    if not parent_reply:
        return jsonify({'error': 'Parent reply not found'}), 404
    
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

    