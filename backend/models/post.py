from extensions import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    replies = db.relationship('Reply', backref='post', lazy=True)

    def to_dict(self, include_replies=False):
        post_data = {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'content': self.content,
            'created_at': self.created_at.isoformat()
        }

        if include_replies:
            post_data['replies'] = [reply.to_dict() for reply in self.replies]

        return post_data