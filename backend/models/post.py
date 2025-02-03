from extensions import db
from models.user import User

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    views_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    replies = db.relationship('Reply', backref='post', lazy=True, 
                            cascade='all, delete-orphan')
    likes = db.relationship('Like', backref='post', lazy=True,
                          primaryjoin="and_(Post.id==Like.post_id, Like.reply_id==None)",
                          cascade='all, delete-orphan')

    @property
    def likes_count(self):
        return len(self.likes)

    @property
    def replies_count(self):
        return len(self.replies)

    def to_dict(self, include_replies=False):
        author = User.query.get(self.user_id)

        post_data = {
            'id': self.id,
            'user_id': self.user_id,
            'author': author.username,
            'topic_id': self.topic_id,
            'title': self.title,
            'content': self.content,
            'created_at': self.created_at.isoformat(),
            'views_count': self.views_count,
            'likes_count': self.likes_count,
            'replies_count': self.replies_count
        }

        if include_replies:
            sorted_replies = sorted(self.replies, key=lambda x: x.created_at, reverse=True)
            post_data['replies'] = [reply.to_dict() for reply in sorted_replies]

        return post_data

    def is_liked_by(self, user_id):
        """Check if a user has liked this post."""
        return any(like.user_id == user_id for like in self.likes)