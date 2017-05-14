from app import db

class User(db.Model):
    __tablename__='User'
    id=db.Column(db.Integer, primary_key = True)
    nickname=db.Column(db.String(64))
    password=db.Column(db.String(64))
    email=db.Column(db.String(64))
    role=db.Column(db.String(64))
    name=db.Column(db.String(64))
    second_name=db.Column(db.String(64))
    thriiid_name=db.Column(db.String(64))
    group=db.Column(db.String(64))
    predmet=db.Column(db.String(64))
    labs_id=db.Column(db.String(64), db.ForeignKey('Labs.id'))
    labs=db.relationship('Labs',
        backref=db.backref('users', lazy='dynamic'))
    name_avatar=db.Column(db.String(64))

    '''
    логин((((((((((((
    # def is_authenticated():
    #     return True

    # def is_active():
    #     return True

    # def is_anonymous():
    #     return False

    # def get_id(self):
    #     return str(self.id)
    '''

    def __repr__(self):
        return '<User %r>' % (self.nickname)

class Labs(db.Model):
    __tablename__='Labs'
    id=db.Column(db.Integer, primary_key=True)
    name_lab=db.Column(db.String(64))
    id_user=db.Column(db.String(64))
    path=db.Column(db.String(64))
    description=db.Column(db.String(1024))
    predmet=db.Column(db.String(64))

    def __repr__(self):
        return '<Labs %r>' % (self.name_lab)

class Programs(db.Model):
    __tablename__='Programs'
    id=db.Column(db.Integer, primary_key=True)
    name_lab=db.Column(db.String(64))
    who_upload=db.Column(db.Integer)
    path=db.Column(db.String(64))
    name_file=db.Column(db.String(64))
    date=db.Column(db.String(64))
    percent=db.Column(db.String(64))
    comment=db.Column(db.String(512))
    copycode=db.Column(db.String(1024))

    def __repr__(self):
        return '<Programs %r>' % (self.path)

class Roles(db.Model):
    __tablename__='Roles'
    id=db.Column(db.Integer, primary_key=True)
    description=db.Column(db.String(1024))

    def __repr__(self):
        return '<Roles %r>' % (self.name_lab)