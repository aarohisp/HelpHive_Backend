from app import db
from sqlalchemy import Enum

class UserModel(db.Model):
    __tablename__ = 'UserModel'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True)
    uname = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))  # Ideally, this should be hashed
    email = db.Column(db.String(100), unique=True)

    def __repr__(self) -> str:
        return f'<User: {self.email}>'

class ItemModel(db.Model):
    __tablename__ = 'Item'  # Ensure it matches your table name
    item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_name = db.Column(db.String(25), nullable=False)
    descriptions = db.Column(db.String(100), nullable=False)
    time_used = db.Column(db.Integer, nullable=False)
    donor_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    category = db.Column(Enum('clothes', 'medicine', 'furniture', 'medical supplies', 'school essentials', 'stationery', name='category_enum'), nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    item_address = db.Column(db.String(100), nullable=False)
    image_info = db.Column(db.String(100), nullable=False)
    specification = db.Column(db.String(50), nullable=False)
    item_check = db.Column(db.Boolean, default=False)
    status_item = db.Column(Enum('open', 'closed', 'expired', name='status_item_enum'), nullable=False, default='open')
    org_id = db.Column(db.Integer, nullable=False)
    
    # Define a relationship to the UserModel
    donor = db.relationship('UserModel', backref='donated_items', foreign_keys=[donor_id])
