from flask_sqlalchemy import SQLAlchemy

db= SQLAlchemy()

################ USER MODEL ####################
class User(db.Model):
    """User class is responsible for handling user data"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    businesses = db.relationship('Business', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    def __init__(self, username, email, password):
        self.username= username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User {}, {}>'.format(self.username, self.email, self.password)
    
    # @staticmethod
    # def getAllUsers():
    #     user = User.query.all()
    #     return user

    def returnJson(self):
        reviewJsonFormat = {'username':self.username, 'email':self.email, 'id':self.id, 'password':self.password}
        return reviewJsonFormat    
        

############### BUSINESS MODEL #################
class Business(db.Model):
    """Business class handles all the business details"""
    __tablename__ = 'businesses'
    id = db.Column(db.Integer, primary_key = True)
    bizname = db.Column(db.String(50), nullable=False)
    userid = db.Column(db.String(50), db.ForeignKey('users.id'))
    location = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    reviews = db.relationship('Review', backref='business', lazy='dynamic', cascade='all, delete-orphan')

    def __init__(self, userid, bizname, category, description, date_created, date_modified):
        self.bizname = bizname
        self.userid = userid
        self.category = category
        self.description = description
        self.date_created = date_created
        self.date_modified = date_modified        

    def __repr__(self):
        return '<Business {}>'.format(self.bizname)

    def returnJson(self):
        businessJsonFormat = {'id':self.id, 'userid':self.userid, 'location':self.location, 'category':self.category, 'description':self.description}
        return businessJsonFormat
        

############### REVIEW MODEL #################
class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key = True)
    review = db.Column(db.Text, nullable=False)
    userid = db.Column(db.Integer, db.ForeignKey('users.id'))
    bizid = db.Column(db.Integer, db.ForeignKey('businesses.id'))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __init__(self, review, userid, bizid, date_created, date_modified):
        self.id = id
        self.review = review
        self.userid = userid
        self.bizid = bizid
        self.date_created= date_created
        self.date_modified = date_modified

    def __repr__(self):
        return '<Review {}>'.format(self.review)

    def returnJson(self):
        reviewJsonFormat = {'Creator':User.query.get(self.userid).username, 'Review':self.review, 'dateCreated':self.date_created, 'dateModified':self.date_modified}
        return reviewJsonFormat


class BlackList(db.Model):
    """class for blacklisted tokens"""
    __tablename__ = 'blacklist'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(256), nullable=False, unique=True)

    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return '<Token {}>'.format(self.token)

    def returnJson(self):
        tokenJsonformat = {'token':self.token}
        return tokenJsonformat