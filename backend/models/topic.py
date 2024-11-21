class Topic(db.Model):
    # id, title, description and a relation with posts
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    posts = db.relationship('Post', backref='topic', lazy=True)