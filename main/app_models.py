from flask_sqlalchemy import SQLAlchemy
import jwt

db = SQLAlchemy()

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
        return '<User:{}, email:{}>'.format(self.username, self.email)

    def returnJson(self):
        reviewJsonFormat = {'username':self.username, 'email':self.email, 'id':self.id, 'password':self.password}
        return reviewJsonFormat
        

############### BUSINESS MODEL #################
class Business(db.Model):
    """Business class handles all the business details"""
    __tablename__ = 'businesses'
    id = db.Column(db.Integer, primary_key = True)
    business_name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    location = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    reviews = db.relationship('Review', backref='business', lazy='dynamic', cascade='all, delete-orphan')

    def __init__(self, user_id, business_name, location, category, description):
        self.business_name = business_name
        self.user_id = user_id
        self.location= location
        self.category = category
        self.description = description
        # self.date_created = date_created
        # self.date_modified = date_modified

    def __repr__(self):
        return '<Business {}>'.format(self.business_name)

    def returnJson(self):
        businessJsonFormat = {'id':self.id, 'business_name':self.business_name, 'userId':self.user_id, 'location':self.location, 'category':self.category, 'description':self.description}
        return businessJsonFormat

    

############### REVIEW MODEL #################
class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key = True)
    review = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    business_id = db.Column(db.Integer, db.ForeignKey('businesses.id'))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __init__(self, review, user_id, business_id):
        # self.id = id
        self.review = review
        self.user_id = user_id
        self.business_id = business_id
        # self.date_created= date_created
        # self.date_modified = date_modified

    def __repr__(self):
        return '<Review {}>'.format(self.review)

    @staticmethod
    def check_business_exists(id):
        id = id
        biz = Business.query.get(id)
        if biz:
            return biz
        else:
            return None

    def returnJson(self):
        reviewJsonFormat = {'id':self.id, 'user_id':self.user_id, 'business_id':self.business_id, 'Author':User.query.get(self.user_id).username, 'Review':self.review, 'dateCreated':self.date_created, 'dateModified':self.date_modified}
        return reviewJsonFormat


####################################
### class for blacklisted tokens ###
####################################

class BlackListToken(db.Model):
    """
    Class to blacklist expired tokens
    """
    __tablename__ = 'blacklist_tokens'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, token):
        self.token = token

    
    def __repr__(self):
        return '<id: token: {}'.format(self.token)


######################################################
### class for reset user password via email ###
######################################################

class ResetPassword(db.Model):
    """
    Class to reset user password via email
    """
    __tablename__ = 'reset_password'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(500), unique=True, nullable=False)
    reset_time = db.Column(db.DateTime, default=db.func.current_timestamp())
    secret_code = db.Column(db.String(10), nullable=False)

    def __init__(self, username, secret_code):
        self.username = username
        self.secret_code = secret_code
    
    def __repr__(self):
        return '<username:{} reset_time: {} secret_code:{}'.format(self.username, self.reset_time, self.secret_code)

