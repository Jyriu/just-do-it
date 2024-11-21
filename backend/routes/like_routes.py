from flask import Blueprint, request, jsonify
from models import db, Like, User, Post, Reply
from extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.return_error import error_response

like_bp = Blueprint('like_routes', __name__)

@like_bp.route('/like/<int:post_id>', methods=['POST'])
@jwt_required()
def like_post(post_id):
    user_id = get_jwt_identity()

    # check if user already liked the post
    existing_like = Like.query.filter_by(user_id=user_id, post_id=post_id).first()
    if existing_like:
        return error_response(400, "You have already liked this post.")

    # add like
    new_like = Like(user_id=user_id, post_id=post_id)
    db.session.add(new_like)
    db.session.commit()

    return jsonify({"message": "Post liked successfully."}), 201

@like_bp.route('/like_reply/<int:reply_id>', methods=['POST'])
@jwt_required()
def like_reply(reply_id):
    user_id = get_jwt_identity()

    # check if user already liked the reply
    existing_like = Like.query.filter_by(user_id=user_id, reply_id=reply_id).first()
    if existing_like:
        return error_response(400, "You have already liked this answer.")

    # add like
    new_like = Like(user_id=user_id, reply_id=reply_id)
    db.session.add(new_like)
    db.session.commit()

    return jsonify({"message": "Answer liked successfully."}), 201