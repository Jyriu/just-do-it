from flask import Blueprint, jsonify
from extensions import db
from models import Post, Reply, Like
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.return_error import error_response

like_bp = Blueprint('like_bp', __name__)

@like_bp.route('/like/<int:post_id>', methods=['POST'])
@jwt_required()
def like_post(post_id):
    user_id = get_jwt_identity()
    
    # Vérifier si le post existe
    post = db.session.get(Post, post_id)
    if not post:
        return error_response('Post not found', 404)
    
    # Vérifier si l'utilisateur n'a pas déjà liké ce post
    existing_like = Like.query.filter_by(user_id=user_id, post_id=post_id, reply_id=None).first()
    if existing_like:
        return error_response('You have already liked this post', 400)
    
    # Créer le like
    like = Like(user_id=user_id, post_id=post_id)
    db.session.add(like)
    db.session.commit()
    
    return jsonify({'message': 'Post liked successfully'}), 201

@like_bp.route('/like/reply/<int:reply_id>', methods=['POST'])
@jwt_required()
def like_reply(reply_id):
    user_id = get_jwt_identity()
    
    # Vérifier si la réponse existe
    reply = db.session.get(Reply, reply_id)
    if not reply:
        return error_response('Reply not found', 404)
    
    # Vérifier si l'utilisateur n'a pas déjà liké cette réponse
    existing_like = Like.query.filter_by(user_id=user_id, reply_id=reply_id).first()
    if existing_like:
        return error_response('You have already liked this reply', 400)
    
    # Créer le like
    like = Like(user_id=user_id, post_id=reply.post_id, reply_id=reply_id)
    db.session.add(like)
    db.session.commit()
    
    return jsonify({'message': 'Reply liked successfully'}), 201

@like_bp.route('/unlike/<int:post_id>', methods=['DELETE'])
@jwt_required()
def unlike_post(post_id):
    user_id = get_jwt_identity()
    
    like = Like.query.filter_by(user_id=user_id, post_id=post_id).first()
    if not like:
        return error_response("You haven't liked this post", 404)
    
    db.session.delete(like)
    db.session.commit()
    
    return jsonify({"message": "Post unliked successfully"}), 200

@like_bp.route('/unlike_reply/<int:reply_id>', methods=['DELETE'])
@jwt_required()
def unlike_reply(reply_id):
    user_id = get_jwt_identity()
    
    like = Like.query.filter_by(user_id=user_id, reply_id=reply_id).first()
    if not like:
        return error_response("You haven't liked this answer", 404)
    
    db.session.delete(like)
    db.session.commit()
    
    return jsonify({"message": "Answer unliked successfully"}), 200