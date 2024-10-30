from flask import Blueprint, request, jsonify
from extensions import db, bcrypt
from models import User, Post, Reply
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

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
    data = request.get_json()

    if 'post_id' not in data or 'content' not in data:
        return jsonify({'error': 'Missing post_id or content'}), 400
    
    user_id = get_jwt_identity()

    post = Post.query.get(data['post_id'])
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    
    reply = Reply(post_id=data['post_id'], user_id=user_id, content=data['content'])
    db.session.add(reply)
    db.session.commit()

    return jsonify({'message': 'Reply successfully created'}), 201

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