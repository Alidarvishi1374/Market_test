
from market import db,login_manager,app
from sqlalchemy import ForeignKey
from market import bcrypt
from flask_login import UserMixin

#dowload itsdangerous
#from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#import User_table
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=30), nullable=False)
    Address = db.Column(db.String(length=250), nullable=False)
    Email = db.Column(db.String(length=30), nullable=False) 
    password_hash = db.Column(db.Integer)
    coin = db.Column(db.Integer)
    Phone = db.Column(db.Integer, nullable=False)
    item = db.relationship('Item', backref="owner_id",lazy=True)

    # def get_token(self):
    #     serial = Serializer(app.config['SECRET_KEY'], expires_in=300)
    
    # @staticmethod
    # def verify_token(token):
    #     serial = Serializer(app.config['SECRET_KEY'])
    #     try:
    #         user_id = serial.loads(token)['user_id']
    #     except:
    #         return None
    #     return User.query.get(user_id)

    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self,plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self,attempted_pass):
        return bcrypt.check_password_hash(self.password_hash,attempted_pass)
    



    # calling Item return name
    def __repr__(self):
        return f"item {self.name}"
    
    def can_buy(self,item_obj):
        return self.coin >= item_obj.price

    def can_sell(self,item_obj):
        return item_obj in self.item


#import item_table in database
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    barcode = db.Column(db.Integer(), nullable=False, unique=True)
    Number = db.Column(db.Integer())
    price = db.Column(db.Integer(), nullable=False)
    Description = db.Column(db.String(length=150))
    owner = db.Column(db.Integer(), ForeignKey('user.id'))
    
    def buy(self,user):
        self.owner = user.id
        user.coin -= self.price
        self.Number -= 1
        db.session.commit()
    
    def sell(self,user):
        self.owner = None
        user.coin += self.price
        self.Number += 1
        db.session.commit()

db.create_all()

