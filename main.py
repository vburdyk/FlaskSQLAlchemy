from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ReprMixin:
    def __repr__(self):
        d = {k: v for k, v in vars(self).items()
                if not k.startswith('_')}
        basic = super().__repr__()
        if not d:
            return basic
        basic, cut = basic[:-1], basic[-1]

        add = ', '.join([f'{k}={v!r}' for k, v in d.items()])

        res = f'{basic} ~ ({add}){cut}'
        return res


class User(ReprMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(24), nullable=False)
    email = db.Column(db.String(50))


class Post(ReprMixin, db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255))
    created_at = db.Column(db.DateTime(timezone=True))
    author_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    user = db.relationship("User", backref='posts')


class Comment(ReprMixin, db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255))
    created_at = db.Column(db.DateTime(timezone=True))
    author_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    user = db.relationship("User", backref='authors')
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'))
    post = db.relationship("Post", backref='comments')


if __name__ == '__main__':
    from flask import Flask
    import datetime

    dummyapp = Flask(__name__)
    dummyapp.config['SQLALCHEMY_DATABASE_URI'] = (
        'sqlite:///database.sqlite')
    db.init_app(dummyapp)

    ctx = dummyapp.app_context()
    ctx.__enter__()

    db.create_all()

    admin = User(username='vburdyk',
                 password='volodya123',
                 email='burdikv1991@gmail.com')

    simple_user = User(username='banana',
                       password='banana123',
                       email='banana@gmail.com')

    admin_post = Post(text="Hello everyone, today i`m speak pasky",
                      created_at=datetime.datetime.now(),
                      author_id=1)

    comment = Comment(text="Wow, your day is really good",
                      created_at=datetime.datetime.now(),
                      author_id=2,
                      post_id=1)

    db.session.add(admin)
    db.session.add(simple_user)
    db.session.add(admin_post)
    db.session.add(comment)

    db.session.commit()

    res = db.session.execute(db.select(User))
    users = res.scalars().all()
    users = list(users)
