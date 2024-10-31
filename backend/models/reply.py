from extensions import db

class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    parent_reply_id = db.Column(db.Integer, db.ForeignKey('reply.id'))
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    children = db.relationship('Reply', backref=db.backref('parent', remote_side=[id], lazy=True))

    def __repr__(self):
        return f"<Reply by User {self.user_id} on Post {self.post_id}>" if not self.parent_reply_id else f"<Reply to Reply {self.parent_reply_id}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'post_id': self.post_id,
            'parent_reply_id': self.parent_reply_id,
            'content': self.content,
            'created_at': self.created_at.isoformat()
        }